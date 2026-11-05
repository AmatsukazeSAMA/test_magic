"""Copy exact neighboring drawings/PV frames and make read-only review sheets."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

root = Path(__file__).resolve().parent.parent
base = root / "art/full_character_redraw_1080p_v01"
out = root / "art/20261101_G33-15_neighbor_comparison_v01"
out.mkdir(parents=True, exist_ok=False)
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
registry = read(base / "ASSET_REGISTRY.json")
scope = read(base / "dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json")
font_path = "C:/Windows/Fonts/msyh.ttc"
font = lambda size: ImageFont.truetype(font_path, size)
entries = []

for order, wid, start, end, image, expected, title, crop in [
    (1, "ART-G33-14", 886, 888, Path(registry["ART-G33-14"]["image"]), "dcbaa05b8546b0887e6e0dba9af9dbb5223c0f5ddc87087ef8a13cdbfcd10b4c", "前一稿", [130, 0, 800, 930]),
    (2, "ART-G33-15", 889, 891, base / "drawings/ART-G33-15/v01/whole_imggen_original_source_far_left_root_occlusion_v02/character_imggen_original.png", "bacf374f6ba3200ecb8485bdfa31ed5fa948b6d5dbc0fe20197fdbb1efcb038d", "你发的这一版（待修复）", [140, 0, 800, 930]),
    (3, "ART-G12-20", 892, 894, Path(registry["ART-G12-20"]["image"]), "57171170293fbc210c8b4733d35f8f8f63d6eabec87ac8076556ba42ef834355", "后一稿", [200, 0, 900, 1040]),
]:
    if sha(image) != expected:
        raise SystemExit(f"Exact requested version changed: {image}")
    state = next(item for item in scope["states"] if item["id"] == wid)
    assert (state["first_frame"], state["last_frame"]) == (start, end)
    folder = out / f"{order:02d}_{wid}_F{start:04d}-{end:04d}"
    folder.mkdir()
    copies = []
    for source, name, role in [
        (image, "drawing_transparent_original.png", "Exact original returned drawing; copied without changing bytes."),
        (image.parent / "qa_white.png", "drawing_white.png", "Read-only white-background QA of that exact version."),
        (Path(state["original_source_master"]), f"original_PV_canonical_F{state['existing_source_canonical_frame']:04d}.png", "Original PV canonical source for this shared drawing state; not the first-dance frame number."),
    ]:
        target = folder / name
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copies.append({"file": str(target.relative_to(out)), "source": str(source), "sha256": sha(target), "role": role})
    for frame in range(start, end + 1):
        source = base / f"coverage/source_frames/F{frame:06d}.png"
        target = folder / f"original_PV_first_dance_F{frame:04d}.png"
        shutil.copyfile(source, target)
        assert sha(source) == sha(target)
        copies.append({"file": str(target.relative_to(out)), "source": str(source), "sha256": sha(target), "role": "Exact decoded original PV frame in first-dance order."})
    entries.append({"id": wid, "title": title, "first_dance_range": [start, end], "canonical_frame": state["existing_source_canonical_frame"], "native_image": str(image), "native_sha256": expected, "native_detail_crop_xyxy": crop, "original_first_frame": str(base / f"coverage/source_frames/F{start:06d}.png"), "files": copies, "current_user_rejected_or_root_repair": wid == "ART-G33-15", "dynamic_pass": False, "user_accepted": False})


def paste_fit(canvas, source, box):
    x, y, width, height = box
    im = ImageOps.contain(source.convert("RGBA"), (width, height), Image.Resampling.LANCZOS)
    canvas.alpha_composite(im, (x + (width - im.width) // 2, y + (height - im.height) // 2))


sheet = Image.new("RGBA", (2160, 1570), "white")
draw = ImageDraw.Draw(sheet)
draw.text((28, 18), "第一段舞蹈：前一稿 / 当前版本 / 后一稿", fill="#171717", font=font(40))
draw.text((28, 72), "上：对应原 PV 的头肩局部    下：现有人物稿局部（仅等比显示，未改原图）", fill="#454545", font=font(27))
for col, entry in enumerate(entries):
    x = col * 720
    draw.rectangle((x + 12, 125, x + 708, 1528), outline="#c2c2c2", width=2)
    draw.text((x + 28, 140), entry["title"], fill="#a52c2c" if col == 1 else "#171717", font=font(31))
    draw.text((x + 28, 187), f"{entry['id']}   F{entry['first_dance_range'][0]}–{entry['first_dance_range'][1]}", fill="#333333", font=font(25))
    draw.text((x + 28, 231), "原 PV（首段曝光）", fill="#333333", font=font(25))
    with Image.open(entry["original_first_frame"]) as im:
        paste_fit(sheet, im.crop((620, 80, 1300, 870)), (x + 28, 271, 664, 560))
    draw.text((x + 28, 858), "对应人物稿（现有版本）", fill="#333333", font=font(25))
    with Image.open(entry["native_image"]) as im:
        paste_fit(sheet, im.crop(tuple(entry["native_detail_crop_xyxy"])), (x + 28, 899, 664, 590))
draw.text((28, 1537), "当前 G33-15 是你刚发的 bb114610 版，仍待修复；静态候选不代表动态或用户验收。", fill="#8e3030", font=font(23))
sheet.convert("RGB").save(out / "01_head_shoulder_original_PV_and_drawings.png")

full = Image.new("RGBA", (2160, 1700), "white")
draw = ImageDraw.Draw(full)
draw.text((28, 20), "完整人物稿与原 PV 画面", fill="#171717", font=font(40))
draw.text((28, 76), "上：首段原 PV 完整画面    下：透明人物原图的完整幅度（未套用首段摄影缩放）", fill="#454545", font=font(26))
for col, entry in enumerate(entries):
    x = col * 720
    draw.text((x + 25, 135), f"{entry['title']} / F{entry['first_dance_range'][0]}", fill="#171717", font=font(28))
    with Image.open(entry["original_first_frame"]) as im:
        paste_fit(full, im, (x + 20, 185, 680, 383))
    draw.text((x + 25, 598), f"{entry['id']} 人物原图", fill="#171717", font=font(27))
    with Image.open(entry["native_image"]) as im:
        paste_fit(full, im, (x + 20, 650, 680, 980))
draw.text((28, 1650), "前两稿来自后续同动作全身母帧，首段中为放大裁切；各母帧原 PV 与首段原图均在各文件夹。", fill="#454545", font=font(24))
full.convert("RGB").save(out / "02_full_original_PV_and_complete_drawings.png")

manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "user_request": "这一版前后两张有吗，看看，和对应的原PV图", "requested_generated_image": "C:/Users/11515/.codex/generated_images/01a18c9e-c795-7c41-9eed-612ceab2f81f/exec-bb114610-8227-4e7d-92b7-e84f0610bd6a.png", "selection_basis": "Nearest preceding/current/following distinct drawing states in original first-dance PTS order, not numeric family order.", "first_dance_frame_range": [886, 894], "entries": entries, "comparison_only": True, "artwork_pixel_edits": False, "production_bindings_changed": False, "new_generation_calls": 0, "current_15_adopted": False, "continuous_playback_validated": False, "user_accepted": False}
(out / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "说明.txt").write_text("顺序为第一段实际曝光：G33-14 / F886–888 → G33-15 / F889–891 → G12-20 / F892–894。\n当前是你发的 exec-bb114610 版本，待修复，未绑定。前后稿已存在；它们的静态记录不代表整段动态验收。\n01 对照图查看头肩与卷发；02 查看原PV完整画面和人物原图幅度。\n每个文件夹含未改字节的透明人物、白底预览、对应首段原PV曝光帧和原PV母帧。母帧2362/2365在后续同动作段，不能当作首段摄影尺寸。\n对照图仅作裁切/等比排版，不修图、不镜像、不做新摄影绑定。\n", encoding="utf-8")
archive = out.with_suffix(".zip")
with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path in sorted(out.rglob("*")):
        if path.is_file():
            z.write(path, str(path.relative_to(out)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    count = len(z.infolist())
print(json.dumps({"directory": str(out), "preview": str(out / "01_head_shoulder_original_PV_and_drawings.png"), "zip": str(archive), "zip_bytes": archive.stat().st_size, "zip_sha256": sha(archive), "zip_entries": count, "raw_and_source_copies_verified": True, "production_bindings_changed": False}, ensure_ascii=False))
