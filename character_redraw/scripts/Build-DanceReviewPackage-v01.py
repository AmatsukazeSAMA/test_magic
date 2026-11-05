"""Build a source-accurate dance review ZIP from current reviewed character layers."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "art/full_character_redraw_1080p_v01"
OUT = ROOT / "deliverables/dance_review_20261031_v01"
ARCHIVE = OUT.parent / "舞蹈原片与替换帧_20261031_v01.zip"
BUILD = OUT.parent / "dance_review_20261031_v01_build"
FFMPEG = Path(r"D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\ffmpeg.exe")
FFPROBE = FFMPEG.with_name("ffprobe.exe")
IDS = ["ART-G12-34", "ART-G12-39", "ART-G13-03", "ART-G13-04",
       "ART-G37-01", "ART-G40-02", "ART-G43-02", "ART-G44-02"]
CLIPS = [
    ("01_upright_dance_F0834-F1327.mp4", 834, 1327, "正向舞蹈：全身及半身"),
    ("02_full_body_dance_F2306-F2632.mp4", 2306, 2632, "全身舞蹈"),
    ("03_dance_turns_F2801-F3287.mp4", 2801, 3287, "舞蹈转向及倒置构图"),
    ("04_upright_dance_reprise_F3373-F3777.mp4", 3373, 3777, "正向舞蹈再现：全身及半身"),
]

def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args, log: Path):
    result = subprocess.run([str(x) for x in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log.write_bytes(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"Command failed, see {log}: {result.stderr[-1200:].decode('utf-8', errors='replace')}")
    return result.stdout

def clock(seconds):
    return f"{int(seconds // 60):02d}:{seconds % 60:06.3f}"

OUT.mkdir(parents=True, exist_ok=True)
BUILD.mkdir(parents=True, exist_ok=True)
ledger = read(BASE / "coverage/EXPOSURE_LEDGER.json")
source = Path(ledger["source_video"])
assert sha(source) == ledger["source_sha256"], "Original PV hash changed"
assert ledger["time_base"] == "1/16000"
frames = ledger["frames"]
registry = read(BASE / "ASSET_REGISTRY.json")
exports = {r["id"]: r for r in read(BASE / "delivery_1080p_v01/INDEX.json")["records"]}

video_records = []
for filename, start, end, label in CLIPS:
    video = OUT / "01_original_clips" / filename
    video.parent.mkdir(parents=True, exist_ok=True)
    start_pts, end_pts = frames[start]["pts"], frames[end]["end_pts"]
    start_seconds, end_seconds = start_pts / 16000, end_pts / 16000
    filters = (f"[0:v]trim=start_frame={start}:end_frame={end + 1},setpts=PTS-STARTPTS[v];"
               f"[0:a]atrim=start={start_seconds:.9f}:end={end_seconds:.9f},asetpts=PTS-STARTPTS[a]")
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-n", "-i", source,
               "-filter_complex", filters, "-map", "[v]", "-map", "[a]",
               "-c:v", "mpeg4", "-q:v", "2", "-bf", "0", "-pix_fmt", "yuv420p",
               "-vsync", "0", "-video_track_timescale", "16000",
               "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", video]
    save(BUILD / (filename + ".command.json"), {"args": [str(x) for x in command], "filter": filters})
    if not video.exists():
        print(f"Encoding {filename} ({end-start+1} original frames)", flush=True)
        run(command, BUILD / (filename + ".encode.log"))
    probe = json.loads(run([FFPROBE, "-v", "error", "-count_frames", "-show_streams",
                            "-show_format", "-of", "json", video], BUILD / (filename + ".probe.log")))
    stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    assert [stream["width"], stream["height"]] == [1920, 1080]
    assert int(stream["nb_read_frames"]) == end-start+1, (filename, stream["nb_read_frames"])
    assert audio["codec_name"] == "aac"
    timing = json.loads(run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_frames",
                            "-show_entries", "frame=best_effort_timestamp", "-of", "json", video],
                           BUILD / (filename + ".timing.log")))
    actual_pts = [int(f["best_effort_timestamp"]) for f in timing["frames"]]
    assert len(actual_pts) == end-start+1
    expected_pts = [f["pts"]-start_pts for f in frames[start:end+1]]
    timestamp_error = max(abs(a-e) for a,e in zip(actual_pts, expected_pts))
    assert timestamp_error <= 32, (filename, "time quantization exceeds 2 ms", timestamp_error)
    record = {"file": video.relative_to(OUT).as_posix(), "description": label,
              "source_start_frame": start, "source_end_frame_inclusive": end,
              "frame_numbering": "zero-based source decode index",
              "source_start_pts": start_pts, "source_end_pts_exclusive": end_pts,
              "time_base": "1/16000", "source_start_time": clock(start_seconds),
              "source_end_time_exclusive": clock(end_seconds),
              "duration_seconds": (end_pts-start_pts)/16000,
              "decoded_frame_count": int(stream["nb_read_frames"]), "dimensions": [1920,1080],
              "output_timestamp_max_error_seconds": timestamp_error/16000,
              "source_audio_retained": True, "original_background_subtitles_effects_retained": True,
              "video_reencoded_for_frame_accurate_cut": True, "sha256": sha(video)}
    video_records.append(record)
    print(json.dumps({"verified_clip": filename, "frames": record["decoded_frame_count"]}, ensure_ascii=False), flush=True)

records = []
font = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)
small = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 17)
sheet = Image.new("RGB", (1520, 4*288+80), "#f2f3f4")
draw = ImageDraw.Draw(sheet)
draw.text((20, 14), "舞蹈替换帧预览 · 1080P 透明人物层见对应文件夹", font=font, fill="#222222")
for n, asset_id in enumerate(IDS):
    item, selected = exports[asset_id], registry[asset_id]
    assert selected["primary_static_pass"] and selected["independent_static_pass"], asset_id
    assert selected["sha256"] == item["image_sha256"] == sha(Path(item["image"])), asset_id
    if selected.get("requires_whole_imggen"):
        assert read(Path(selected["selected_run"]) / "BUILTIN_GENERATION.json")["mandatory_whole_redraw_after_local_repair_completed"]
    layer = Path(item["layer_1080"])
    assert sha(layer) == item["layer_sha256"]
    with Image.open(layer) as image:
        image.load()
        assert image.mode == "RGBA" and image.size == (1920,1080)
        assert image.getchannel("A").getextrema() == (0,255)
    stem = f"F{item['source_frame']:04d}_{asset_id}"
    copied = {}
    for key, folder, suffix in [
        ("layer_1080", "02_replacement_layers_1080p", ".png"),
        ("preview", "03_position_previews", "_preview.png"),
        ("source_comparison", "04_source_comparisons", "_comparison.png"),
        ("source_image", "05_original_source_frames", "_original.png"),
    ]:
        target = OUT / folder / (stem + suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item[key], target)
        copied[key] = target.relative_to(OUT).as_posix()
    placement = Path(item["layer_1080"]).parent / "PLACEMENT.json"
    shutil.copyfile(placement, OUT / "02_replacement_layers_1080p" / (stem + "_placement.json"))
    record = {"id": asset_id, "source_frame": item["source_frame"], "source_pts": item["source_pts"],
              "time_base": "1/16000", "source_time": clock(item["source_pts"] / 16000),
              "canonical_source_frame": item["canonical_source_frame"],
              "dimensions": [1920,1080], "mode": "RGBA", "files": copied,
              "raw_return_sha256": item["image_sha256"], "layer_sha256": item["layer_sha256"],
              "primary_static_pass": True, "sol_xhigh_static_pass": True,
              "source_comparison_actually_viewed_by_primary": True,
              "final_registration_validated": False, "continuous_playback_reviewed": False,
              "user_accepted": False}
    records.append(record)
    x, y = (n % 2)*760+12, (n // 2)*288+70
    with Image.open(item["preview"]) as preview:
        thumb = preview.convert("RGB")
        thumb.thumbnail((736,235), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x+(736-thumb.width)//2, y))
    draw.text((x+8, y+240), f"{stem}   {record['source_time']}", font=small, fill="#222222")
sheet.save(OUT / "00_preview_sheet.jpg", quality=92)

trial_dir = BASE / "drawings/ART-G51-01/v01/ending_palette_gray_green_trial_v01"
trial = trial_dir / "character_imggen_original.png"
trial_added = False
if trial.exists():
    target = OUT / "06_optional_ending_palette_trial"
    target.mkdir(exist_ok=True)
    shutil.copyfile(trial, target / "gray_green_trial_transparent.png")
    shutil.copyfile(trial_dir / "request_imggen.json", target / "TRIAL_REQUEST.json")
    red = BASE / "drawings/ART-G51-01/v01/whole_imggen_v01/character_imggen_original.png"
    shutil.copyfile(red, target / "red_reference_transparent.png")
    for name in ("qa_white.png", "qa_black.png"):
        if (trial_dir / name).exists():
            shutil.copyfile(trial_dir / name, target / name)
    save(target / "TRIAL_STATUS.json", {"trial_only": True, "production_selection_changed": False,
          "user_accepted": False, "description": "片尾灰绿色试色，供单独选择；不影响前面黑色女仆服。"})
    trial_added = True

manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
            "purpose": "舞蹈原片截取与已完成替换帧对照包",
            "source_video_sha256": ledger["source_sha256"], "source_frame_count": 4763,
            "source_frame_numbering": "zero-based source decode index",
            "clips": video_records, "replacement_frames": records,
            "optional_ending_gray_green_trial": trial_added,
            "whole_film_complete": False, "final_composite": False, "user_accepted": False}
save(OUT / "FRAME_INDEX.json", manifest)
lines = ["舞蹈原片与替换帧 · 2026-10-31 v01", "",
         "01_original_clips：4 段原 PV 舞蹈截取，1920×1080，保留原音轨、字幕、背景和特效。",
         "02_replacement_layers_1080p：8 张透明 RGBA 人物替换层，画布 1920×1080；附定位记录。",
         "03_position_previews：上述 8 张人物在纯粉底上的定位预览。",
         "04_source_comparisons：左边原片，右边替换人物定位，便于比较动作和裁切。",
         "05_original_source_frames：对应的 8 张原片完整截图。",
         "00_preview_sheet.jpg：8 张替换帧总览。", "",
         "截取范围（以下帧号为从 0 开始的原片解码帧号）："]
for clip in video_records:
    lines.append(f"  {clip['source_start_time']} — {clip['source_end_time_exclusive']}  F{clip['source_start_frame']:04d}–F{clip['source_end_frame_inclusive']:04d}，{clip['description']}")
lines += ["", "8 张替换帧已完成主代理和 Sol xhigh 静态看图评测，供查看和后续合成。",
          "这是阶段性对照包；尚未完成整段替换动画、最终配准及字幕/背景/特效合成，不能代表全片制作完成。",
          "G13 两张采用较宽的舞蹈再现镜头 F3628/F3630，原始姿势编号分别来自 F1178/F1180；文件名按实际定位原帧标注。",
          "详细帧号、真实 PTS、素材哈希及审查状态见 FRAME_INDEX.json。"]
if trial_added:
    lines += ["", "06_optional_ending_palette_trial：另附片尾灰绿色试色和红色参考，供比较，尚未作为生产配色采用。"]
(OUT / "请先读我.txt").write_bytes(("\r\n".join(lines)+"\r\n").encode("utf-8-sig"))

files = sorted(p for p in OUT.rglob("*") if p.is_file())
save(OUT / "FILE_HASHES.json", {p.relative_to(OUT).as_posix(): sha(p) for p in files})
files = sorted(p for p in OUT.rglob("*") if p.is_file())
temporary = ARCHIVE.with_suffix(".zip.building")
with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path in files:
        method = zipfile.ZIP_STORED if path.suffix.lower() in (".mp4", ".png", ".jpg") else zipfile.ZIP_DEFLATED
        z.write(path, f"{OUT.name}/{path.relative_to(OUT).as_posix()}", compress_type=method)
with zipfile.ZipFile(temporary) as z:
    assert z.testzip() is None
    assert len(z.infolist()) == len(files)
temporary.replace(ARCHIVE)
result = {"archive": str(ARCHIVE), "bytes": ARCHIVE.stat().st_size, "sha256": sha(ARCHIVE),
          "file_count": len(files), "original_clips": len(video_records), "replacement_frames": len(records),
          "decoded_video_frames": sum(r["decoded_frame_count"] for r in video_records),
          "optional_palette_trial": trial_added, "zip_crc_pass": True}
save(BUILD / "PACKAGE_VERIFICATION.json", result)
print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
