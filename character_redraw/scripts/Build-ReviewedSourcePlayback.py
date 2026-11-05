"""Export original-speed and half-speed comparison MP4s from verified source bindings."""
import argparse
import json
from pathlib import Path
import runpy
import subprocess
from tempfile import TemporaryFile

from PIL import Image


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / "art/full_character_redraw_1080p_v01"
    out = args.output.resolve()
    out.relative_to(base / "coverage/review")
    helper_path = root / "scripts/Build-FirstDanceCurrentReview20261102.py"
    helper = runpy.run_path(str(helper_path))
    read, sha = helper["read_json"], helper["file_sha"]
    ledger = read(base / "coverage/EXPOSURE_LEDGER.json")
    registry = read(base / "ASSET_REGISTRY.json")
    ffmpeg = Path(r"D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\ffmpeg.exe")
    ffprobe = ffmpeg.with_name("ffprobe.exe")
    manifests = [path.resolve() for path in args.manifest]
    rows = []
    for path in manifests:
        manifest = read(path)
        assert manifest["source_time_base"] == ledger["time_base"] == "1/16000"
        assert manifest["verified_exposures"] == len(manifest["records"])
        rows.extend(manifest["records"])
    assert rows and all(right["frame"] == left["frame"] + 1 and right["pts"] == left["end_pts"]
                        for left, right in zip(rows, rows[1:]))
    start = rows[0]["pts"]
    span = f"F{rows[0]['frame']:04d}-F{rows[-1]['frame']:04d}"
    layers = {}
    samples = TemporaryFile()
    for row in rows:
        frame = ledger["frames"][row["frame"]]
        assert frame["actual_render_binding_verified"] and len(frame["selected_assets"]) == 1
        binding = frame["selected_assets"][0]
        assert binding["id"] == row["id"] and binding["image_sha256"] == row["image_sha256"]
        assert binding["image"] == row["image"]
        assert binding["selected_original_sha256"] == registry[row["id"]]["sha256"]
        assert all(frame[k] == row[k] for k in ("pts", "end_pts", "duration_ticks"))
        source = base / "coverage" / frame["source_frame"]
        assert sha(source) == row["source_sha256"]
        key = row["image_sha256"]
        if key not in layers:
            assert sha(Path(row["image"])) == key
            with Image.open(row["image"]) as layer:
                assert layer.mode == "RGBA" and layer.size == (1920, 1080)
                pink = Image.new("RGBA", layer.size, (212, 168, 168, 255))
                pink.alpha_composite(layer)
                layers[key] = pink.convert("RGB")
        with Image.open(source) as image:
            assert image.size == (1920, 1080)
            panel = Image.new("RGB", (3840, 1080))
            panel.paste(image.convert("RGB"), (0, 0))
            panel.paste(layers[key], (1920, 0))
            samples.write(panel.tobytes())

    out.mkdir(parents=True)
    videos = []
    for factor, label in ((1, "original_speed"), (2, "half_speed")):
        path = out / f"{span}_{label}.mp4"
        expected = [factor * (row["pts"] - start) for row in rows]
        helper_input = [{"pts": helper["CLIP_START"] + value} for value in expected]
        durations = [factor * row["duration_ticks"] for row in rows]
        command = list(map(str, [ffmpeg, "-hide_banner", "-v", "error", "-nostdin", "-n",
            "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", "3840x1080", "-framerate", "30",
            "-i", "pipe:0", "-vf", helper["exact_pts_filter"](helper_input), "-an", "-frames:v", len(rows),
            "-vsync", "0", "-c:v", "h264_mf", "-hw_encoding", "0", "-bf", "0", "-b:v", "36M",
            "-pix_fmt", "yuv420p", "-enc_time_base", "1:16000", "-video_track_timescale", "16000",
            "-use_editlist", "0", "-movflags", "+faststart", path]))
        (out / f"{label}_encode.json").write_text(json.dumps(command, ensure_ascii=False), encoding="utf-8")
        samples.seek(0)
        result = subprocess.run(command, stdin=samples, capture_output=True)
        (out / f"{label}_encode.log").write_bytes(result.stderr)
        result.check_returncode()
        timing = helper["exact_mp4_sample_durations"](path, durations)
        probe = subprocess.check_output([str(ffprobe), "-v", "error", "-select_streams", "v:0",
            "-show_entries", "packet=pts,duration:stream=time_base,duration_ts", "-of", "json", str(path)])
        (out / f"{label}_packets.json").write_bytes(probe)
        proof = json.loads(probe)
        assert proof["streams"][0]["time_base"] == "1/16000"
        assert int(proof["streams"][0]["duration_ts"]) == sum(durations)
        assert [(int(packet["pts"]), int(packet["duration"])) for packet in proof["packets"]] == list(zip(expected, durations))
        subprocess.run([str(ffmpeg), "-v", "error", "-nostdin", "-i", str(path), "-an", "-f", "null", "-"], check=True)
        videos.append({"path": str(path), "sha256": sha(path), "duration_ticks": sum(durations), "timing_rewrite": timing})

    samples.close()
    receipt = {"render_manifests": [{"path": str(p), "sha256": sha(p)} for p in manifests],
               "frames": [rows[0]["frame"], rows[-1]["frame"]], "source_pts_range": [start, rows[-1]["end_pts"]],
               "time_base": "1/16000", "actual_continuous_visual_playback_review": False,
               "user_accepted": False, "videos": videos}
    (out / "PREVIEW_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
