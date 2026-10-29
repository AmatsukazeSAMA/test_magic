#!/usr/bin/env python3
"""Portable, evidence-preserving frame bindings and exact-PTS recomposition.

No inferred hold or reference-video pixels are substituted for an original frame.
Layer masks and indexed partitions apply only to their exact source frame; any
frame without a partition remains an explicit source fallback. A lossless RGB
master is a round-trip diagnostic, not proof that semantic boundaries, hidden
anatomy, or a redesign are complete.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from PIL import Image


PROJECT_DEFAULT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
SOURCE_HASHES = {
    "original": "ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1",
    "reference": "fe3031cd98c5488949f26194e503d41ba966e8261e1c8a280686e90651aad498",
}
SCHEMA = "magic-maid.frame-bindings/1"
FRAME_LABEL_NAMES = ("background_observed", "environment_or_props", "subject_visible",
                     "subtitles_visible", "effects_visible", "unresolved_visible")
PREVIEW_COLOR_METADATA = {"color_range": "tv", "color_space": "bt709",
                          "color_transfer": "bt709", "color_primaries": "bt709"}


def preview_color_args():
    """Use the source's BT.709 colour system, never an untagged RGB→YUV default.

    An untagged default conversion can use BT.601 while an HD player assumes
    BT.709, making the same compressed RGB-looking test appear orange in a
    player. Convert the full-range RGB explicitly, THEN tag that conversion.
    Merely assigning BT.709 metadata to BT.601-encoded YUV is not a fix.
    """
    return ["-vf", "format=gbrp,scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p,"
                   "setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709",
            "-colorspace", "bt709", "-color_trc", "bt709", "-color_primaries", "bt709", "-color_range", "tv"]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def reject_symlink_components(path: Path):
    """Never follow an output path (or its parent) through a symlink."""
    absolute = path if path.is_absolute() else Path.cwd() / path
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            raise ValueError(f"Refusing a symlink in output path: {current}")
    return absolute


def require_new_output(path: Path):
    path = reject_symlink_components(path)
    if path.exists():
        raise ValueError(f"Refusing to overwrite existing output: {path}")
    return path


def write_json(path: Path, value, *, overwrite=False, expected_schema=None):
    path = reject_symlink_components(path)
    if path.suffix.lower() != ".json":
        raise ValueError("JSON output filename must end in .json")
    if path.exists():
        if not overwrite or not expected_schema or not expected_schema.startswith("magic-maid."):
            raise ValueError(f"Refusing to overwrite existing JSON output: {path}")
        try:
            existing = read_json(path)
        except (ValueError, UnicodeError) as error:
            raise ValueError(f"Refusing to overwrite non-generated output: {path}") from error
        if not isinstance(existing, dict) or not isinstance(value, dict) or existing.get("schema") != expected_schema or value.get("schema") != expected_schema:
            raise ValueError(f"Refusing to overwrite an unknown JSON document: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        # A random exclusive temporary file cannot follow a planted .tmp link.
        with tempfile.NamedTemporaryFile(mode="w", prefix=f".{path.name}.", suffix=".tmp",
                                         dir=path.parent, encoding="utf-8", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        reject_symlink_components(path)
        temporary.replace(path)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def inside(project: Path, relative: str) -> Path:
    """Reject absolute paths, traversal, and symlinks that escape the project."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"Expected a project-relative file path: {relative!r}")
    candidate = (project / relative).resolve()
    if not candidate.is_relative_to(project.resolve()):
        raise ValueError(f"Path escapes project: {relative!r}")
    return candidate


def capture(args: list[str]) -> str:
    result = subprocess.run([str(a) for a in args], check=True, capture_output=True, text=True)
    return result.stdout


def probe(path: Path, ffprobe: str = "ffprobe", packets: str | None = None):
    args = [ffprobe, "-v", "error", "-show_streams", "-show_format"]
    if packets:
        args += ["-select_streams", packets, "-show_packets",
                 "-show_entries", "packet=pts,dts,duration,size"]
    return json.loads(capture(args + ["-of", "json", str(path)]))


def video_metadata(project: Path):
    metadata = read_json(project / "data/original_ffprobe.json")
    return next(s for s in metadata["streams"] if s["codec_type"] == "video")


def validated_timeline(rows, time_base: str, duration_ticks: int):
    """Use integer PTS differences, including the source's real final duration."""
    tb = Fraction(time_base)
    if tb <= 0 or not rows:
        raise ValueError("Empty timeline or non-positive time base")
    previous = None
    output = []
    for index, row in enumerate(rows):
        pts = row.get("pts")
        if row.get("frame") != index or type(pts) is not int:
            raise ValueError(f"Invalid frame number / integer PTS at index {index}")
        if previous is not None and pts <= previous:
            raise ValueError(f"PTS is not strictly increasing at frame {index}")
        if index == 0 and pts != 0:
            raise ValueError("This project requires source PTS to begin at zero")
        previous = pts
        output.append({"frame": index, "pts": pts})
    for index, row in enumerate(output):
        end = output[index + 1]["pts"] if index + 1 < len(output) else duration_ticks
        if end <= row["pts"]:
            raise ValueError("Video duration does not cover its last frame")
        row["duration_ticks"] = end - row["pts"]
        # Decimal display only; integer PTS/time_base are the source of truth.
        row["time_s"] = float(row["pts"] * tb)
    return output


def chapter_index(chapters, frame_count):
    by_frame = [None] * frame_count
    cursor = 0
    for chapter in chapters:
        start, end = chapter["start_frame"], chapter["end_frame_exclusive"]
        if start != cursor or end <= start or end > frame_count:
            raise ValueError(f"Non-contiguous or invalid chapter {chapter.get('id')}")
        if chapter.get("frame_count", end - start) != end - start:
            raise ValueError(f"Chapter frame count mismatch: {chapter.get('id')}")
        for frame in range(start, end):
            by_frame[frame] = chapter["id"]
        cursor = end
    if cursor != frame_count:
        raise ValueError("Chapters do not cover all frames")
    return by_frame


def audited_bindings(exposures, frame_count, panel_ids):
    bindings = {}
    for row in exposures["rows"]:
        start, end = row["start_frame"], row["end_frame_exclusive"]
        if row["state"] not in panel_ids or not 0 <= start < end <= frame_count:
            raise ValueError("Invalid audited exposure")
        if row.get("hold_frames", end - start) != end - start:
            raise ValueError("Audited hold length mismatch")
        for frame in range(start, end):
            if frame in bindings:
                raise ValueError(f"Overlapping audited exposures at frame {frame}")
            bindings[frame] = {
                "state_id": row["state"],
                "status": "audited_visible_pose_not_author_cel_identity",
                "evidence": row["evidence"],
                "exposure_start_frame": start,
                "exposure_end_frame_exclusive": end,
            }
    if len(bindings) != exposures["video_frames"]:
        raise ValueError("Audited exposure coverage mismatch")
    scope_start, scope_end = exposures["scope"]
    if set(bindings) != set(range(scope_start, scope_end)):
        raise ValueError("Audited exposures do not exactly cover their declared scope")
    return bindings


def layer_panels(manifest):
    if manifest is None:
        return []
    if isinstance(manifest, list):
        return manifest
    if not isinstance(manifest.get("panels"), list):
        raise ValueError("Layer manifest must contain a panels list")
    return manifest["panels"]


def supplemental_observations(project: Path, rows, video_duration_ticks):
    """Link explicit drawing-audit evidence without promoting it to author IDs."""
    relative = "data/drawing_coverage_audit.json"
    path = project / relative
    if not path.is_file():
        return {}, 0
    audit = read_json(path)
    entries = audit.get("supplemental_observed_states", [])
    links = defaultdict(list)
    seen = set()
    for entry in entries:
        identity = entry["id"]
        frame = entry["source_frame"]
        if identity in seen or type(frame) is not int or not 0 <= frame < len(rows):
            raise ValueError("Invalid/duplicate supplemental observation identity or source frame")
        seen.add(identity)
        if entry["source_pts"] != rows[frame]["pts"]:
            raise ValueError(f"Supplemental source PTS mismatch: {identity}")
        evidence_by_frame = {frame: [{"type": "exact_audited_source_frame"}]}
        for exposure in entry.get("observed_exposures", []):
            start, end = exposure["start_frame"], exposure["end_frame_exclusive"]
            if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(rows):
                raise ValueError("Supplemental exposure outside original timeline")
            expected_end = rows[end]["pts"] if end < len(rows) else video_duration_ticks
            if exposure.get("start_pts", rows[start]["pts"]) != rows[start]["pts"] or exposure.get("end_pts_exclusive", expected_end) != expected_end:
                raise ValueError("Supplemental exposure PTS does not match its explicit frame bounds")
            evidence = {"type": "explicit_audit_exposure_range", "start_frame": start,
                        "end_frame_exclusive": end, "evidence_level": exposure.get("evidence_level", "not_specified")}
            for covered_frame in range(start, end):
                evidence_by_frame.setdefault(covered_frame, []).append(evidence)
        for covered_frame, evidence in evidence_by_frame.items():
            links[covered_frame].append({"observation_id": identity, "audit_file": relative,
                                         "source_frame": frame, "source_pts": entry["source_pts"],
                                         "status": entry.get("status", "unreviewed"), "evidence": evidence,
                                         "author_cel_identity": None,
                                         "automatic_layer_or_transform_reuse": False})
    return dict(links), len(entries)


def build_bindings(project: Path, layer_manifest: Path | None = None, frame_layer_manifest: Path | None = None):
    meta = video_metadata(project)
    rows = validated_timeline(read_json(project / "data/original_timeline.json"),
                              meta["time_base"], int(meta["duration_ts"]))
    chapters = chapter_index(read_json(project / "data/chapters.json"), len(rows))
    panels = read_json(project / "data/panel_catalog.json")
    panel_by_id = {p["id"]: p for p in panels}
    if len(panel_by_id) != len(panels):
        raise ValueError("Duplicate catalog panel IDs")
    audited = audited_bindings(read_json(project / "data/opening_exposures.json"),
                               len(rows), panel_by_id)
    supplements, supplement_count = supplemental_observations(project, rows, int(meta["duration_ts"]))
    exact, candidates = defaultdict(list), defaultdict(list)
    for panel in panels:
        frame = panel["source_frame"]
        if not 0 <= frame < len(rows) or panel["source_pts"] != rows[frame]["pts"]:
            raise ValueError(f"Catalog source PTS mismatch: {panel['id']}")
        exact[frame].append(panel["id"])
        for candidate in panel.get("source_candidates", []):
            candidate_frame = candidate["frame"]
            if not 0 <= candidate_frame < len(rows):
                raise ValueError("Candidate frame outside timeline")
            candidates[candidate_frame].append(panel["id"])

    available = {}
    for panel in layer_panels(read_json(layer_manifest) if layer_manifest else None):
        panel_id = panel["panel_id"]
        if panel_id not in panel_by_id:
            raise ValueError(f"Unknown layer panel ID: {panel_id}")
        source = panel_by_id[panel_id]
        if panel["source_frame"] != source["source_frame"] or panel["source_pts"] != source["source_pts"]:
            raise ValueError(f"Layer manifest source identity mismatch: {panel_id}")
        if panel_id in available:
            raise ValueError(f"Duplicate layer panel ID: {panel_id}")
        available[panel_id] = panel

    frame_partitions = {}
    if frame_layer_manifest:
        partitions = read_json(frame_layer_manifest)
        if (partitions.get("schema") != "magic-maid.frame-visible-partitions/1" or
                not partitions.get("build_complete") or partitions.get("source_sha256") != SOURCE_HASHES["original"] or
                partitions.get("time_base") != meta["time_base"] or
                partitions.get("video_duration_ticks") != int(meta["duration_ts"]) or
                partitions.get("frame_count") != len(rows) or
                partitions.get("completed_frames") != len(rows) or
                partitions.get("dimensions") != [int(meta["width"]), int(meta["height"])] or
                len(partitions.get("frames", [])) != len(rows)):
            raise ValueError("Incomplete or mismatched all-frame partition manifest")
        if partitions.get("labels") != [{"index": i, "name": name} for i, name in enumerate(FRAME_LABEL_NAMES)]:
            raise ValueError("All-frame partition category index mapping mismatch")
        for row, partition in zip(rows, partitions["frames"]):
            if any(partition.get(k) != row[k] for k in ("frame", "pts", "duration_ticks")):
                raise ValueError("Frame partition order/PTS/duration mismatch")
            if partition.get("original_frame") != f"frames/F{row['frame']:06d}.png":
                raise ValueError("Frame partition original source path mismatch")
            frame_partitions[row["frame"]] = partition

    counts = Counter({"source_fallback": 0, "exact_source_layers": 0, "frame_visible_partition": 0})
    for row in rows:
        frame = row["frame"]
        row.update({
            "chapter_id": chapters[frame],
            "original_frame": f"frames/F{frame:06d}.png",
            "exact_source_panel_ids": exact[frame],
            "candidate_panel_ids": sorted(set(candidates[frame])),
            "character_binding": audited.get(frame),
            "supplemental_observations": supplements.get(frame, []),
        })
        selected = next((p for p in exact[frame] if p in available), None)
        if frame in frame_partitions:
            partition = frame_partitions[frame]
            row["composition"] = {
                "mode": "frame_visible_partition", "label_map": partition["label_map"],
                "semantic_status": partition.get("status", "unreviewed"),
                "does_not_imply_clean_cel": True,
            }
        elif selected:
            row["composition"] = {
                "mode": "exact_source_layers",
                "panel_id": selected,
                "semantic_status": available[selected].get("status", "unreviewed"),
                "does_not_imply_clean_cel": True,
            }
        else:
            row["composition"] = {"mode": "source_fallback", "does_not_imply_clean_cel": True}
        counts[row["composition"]["mode"]] += 1
    return {
        "schema": SCHEMA,
        "source": "source/original.mp4",
        "source_sha256": SOURCE_HASHES["original"],
        "time_base": meta["time_base"],
        "video_duration_ticks": int(meta["duration_ts"]),
        "dimensions": [int(meta["width"]), int(meta["height"])],
        "frame_count": len(rows),
        "identity_policy": "Only opening audit binds observed character states. Catalog candidates are not confirmed author-cel identities; never expand them into holds.",
        "supplemental_audit_policy": "Explicit supplemental source/range evidence is linked separately. It does not establish author-cel identity or authorize automatic layer/transform reuse.",
        "composition_policy": "Each selected layer composition or indexed per-frame partition is used ONLY at its recorded source_frame. Pixel-partition coverage is not semantic approval. Source fallbacks retain original dynamic subtitles/effects/camera motion and are not completed separation.",
        "summary": {**counts, "audited_character_bound_frames": len(audited),
                    "character_identity_unresolved_frames": len(rows) - len(audited),
                    "supplemental_observation_records": supplement_count,
                    "frames_with_supplemental_observation_links": len(supplements),
                    "catalog_panels": len(panels), "exact_catalog_source_frames": sum(bool(ids) for ids in exact.values())},
        "frames": rows,
    }


def validate_source(project: Path, ffprobe: str = "ffprobe", verify_reference: bool = True):
    bindings = build_bindings(project)
    names = SOURCE_HASHES if verify_reference else ["original"]
    hashes = {}
    for name in names:
        path = project / "source" / f"{name}.mp4"
        actual = sha256(path)
        if actual != SOURCE_HASHES[name]:
            raise ValueError(f"Immutable source checksum mismatch: {name}")
        hashes[name] = actual
    actual = probe(project / "source/original.mp4", ffprobe, "v:0")
    video = next(s for s in actual["streams"] if s["codec_type"] == "video")
    if video["time_base"] != bindings["time_base"]:
        raise ValueError("Source timebase differs from recorded timeline")
    if int(video["duration_ts"]) != bindings["video_duration_ticks"]:
        raise ValueError("Source duration differs from recorded timeline")
    packets = sorted(actual["packets"], key=lambda packet: int(packet["pts"]))
    if [int(p["pts"]) for p in packets] != [r["pts"] for r in bindings["frames"]]:
        raise ValueError("Actual source PTS/frame count differs from recorded timeline")
    return {"status": "pass", "source_hashes": hashes, "frame_count": len(packets),
            "time_base": video["time_base"], "video_duration_ticks": int(video["duration_ts"])}


def extract_frames(project: Path, ffmpeg: str = "ffmpeg", ffprobe: str = "ffprobe"):
    """Restore missing frame cache without overwriting a pre-existing cache."""
    report = validate_source(project, ffprobe)
    destination = project / "frames"
    if destination.exists():
        expected = [destination / f"F{i:06d}.png" for i in range(report["frame_count"])]
        if all(p.is_file() for p in expected) and len(list(destination.glob("*.png"))) == len(expected):
            return {**report, "frames": "already_present_not_overwritten"}
        raise ValueError("Existing incomplete frame cache: move it aside before extraction; no files overwritten")
    temporary = Path(tempfile.mkdtemp(prefix=".extract-", dir=project))
    try:
        subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i",
                        str(project / "source/original.mp4"), "-map", "0:v:0", "-an",
                        "-fps_mode", "passthrough", "-start_number", "0", "-compression_level", "3",
                        str(temporary / "F%06d.png")], check=True)
        if len(list(temporary.glob("*.png"))) != report["frame_count"]:
            raise ValueError("Decoded frame count mismatch")
        temporary.replace(destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {**report, "frames": "restored_from_immutable_original"}


def compose_layers(project: Path, panel, dimensions):
    layers = panel["layers"]
    if not isinstance(layers, list) or not layers:
        raise ValueError("Empty layer stack")
    canvas = Image.new("RGBA", tuple(dimensions), (0, 0, 0, 0))
    for layer in sorted(layers, key=lambda item: item.get("z_index", 0)):
        path = inside(project, layer.get("path", layer.get("file")))
        with Image.open(path) as image:
            if image.size != tuple(dimensions) or image.mode != "RGBA":
                raise ValueError(f"Layer must be full-canvas RGBA: {path}")
            canvas = Image.alpha_composite(canvas, image)
    if canvas.getchannel("A").getextrema() != (255, 255):
        raise ValueError(f"Incomplete opaque coverage for {panel['panel_id']}; missing pixels are not invented")
    return canvas.convert("RGB")


def compose_frame_partition(project: Path, partition, dimensions, cache_validation):
    """Recompose labels only after the original cache's RGB identity is proved."""
    if cache_validation.get("all_cached_rgb_equal_source_decode") is not True:
        raise ValueError("Frame partition composition requires independently verified original RGB cache")
    from magic_maid_frame_layers import read_labels, reconstruct_rgb
    import numpy as np
    original = inside(project, partition["original_frame"])
    label_path = inside(project, partition["label_map"])
    if sha256(label_path) != partition["label_png_sha256"]:
        raise ValueError(f"Changed label map at frame {partition['frame']}")
    container_difference = sha256(original) != partition["source_png_sha256"]
    labels = read_labels(label_path, dimensions)
    with Image.open(original) as source:
        source_rgb = np.array(source.convert("RGB"))
    reconstructed = reconstruct_rgb(source_rgb, labels)
    if not np.array_equal(reconstructed, source_rgb):
        raise ValueError(f"Per-frame partition reconstruction mismatch at {partition['frame']}")
    return Image.fromarray(reconstructed), container_difference


def rgb_md5(path: Path) -> str:
    with Image.open(path) as image:
        return hashlib.md5(image.convert("RGB").tobytes()).hexdigest()


def decoded_rgb_md5(movie: Path, ffmpeg="ffmpeg"):
    output = capture([ffmpeg, "-v", "error", "-i", str(movie), "-map", "0:v:0", "-an",
                      "-pix_fmt", "rgb24", "-fps_mode", "passthrough", "-f", "framemd5", "-"])
    return [line.split(",")[-1].strip() for line in output.splitlines()
            if line and not line.startswith("#")]


def decode_frame_at_pts(movie: Path, pts: int, time_base: str, dimensions, ffmpeg="ffmpeg"):
    """Accurate input seek to a known source PTS; return one native RGB frame."""
    time = float(pts * Fraction(time_base))
    result = subprocess.run([ffmpeg, "-v", "error", "-ss", f"{time:.9f}", "-i", str(movie),
                             "-map", "0:v:0", "-an", "-frames:v", "1", "-pix_fmt", "rgb24",
                             "-f", "rawvideo", "-"], check=True, capture_output=True)
    expected = int(dimensions[0]) * int(dimensions[1]) * 3
    if len(result.stdout) != expected:
        raise ValueError("Accurate frame seek returned an unexpected RGB byte count")
    return result.stdout


def validate_frame_cache(project: Path, frame_paths, ffmpeg="ffmpeg"):
    """Check every cached PNG against an independent decode, not its filename."""
    expected = decoded_rgb_md5(project / "source/original.mp4", ffmpeg)
    cached = [rgb_md5(path) for path in frame_paths]
    if cached != expected:
        unequal = [i for i, (a, b) in enumerate(zip(cached, expected)) if a != b]
        raise ValueError(f"Original frame cache differs from source decode: {len(cached)}/{len(expected)} frames; first mismatches {unequal[:12]}")
    return {"status": "pass", "frame_count": len(cached), "all_cached_rgb_equal_source_decode": True,
            "rgb_frame_checksum_chain_sha256": hashlib.sha256("\n".join(cached).encode()).hexdigest()}


def concat_quote(path: Path) -> str:
    value = str(path.resolve())
    if "\n" in value or "\r" in value:
        raise ValueError("Newline in frame filename")
    return "'" + value.replace("'", "'\\''") + "'"


def write_concat(path: Path, frame_paths, rows, time_base: str):
    tb = Fraction(time_base)
    if tb.numerator != 1:
        raise ValueError("PNG concat requires a reciprocal-integer source timebase")
    if len(frame_paths) != len(rows) or not rows:
        raise ValueError("Concat frame/timing count mismatch")
    lines = ["ffconcat version 1.0"]
    for frame_path, row in zip(frame_paths, rows):
        # The concat demuxer parses durations in microseconds.  Quantize
        # absolute endpoints, not each duration independently: this prevents
        # cumulative rounding drift for 62.5-microsecond source ticks.
        start_us = round(row["pts"] * tb * 1_000_000)
        end_us = round((row["pts"] + row["duration_ticks"]) * tb * 1_000_000)
        duration_us = end_us - start_us
        lines += ["file " + concat_quote(frame_path), f"option framerate {tb.denominator}",
                  f"duration {duration_us // 1_000_000}.{duration_us % 1_000_000:06d}"]
    # A sentinel communicates the actual last-frame duration to the encoder.
    # It is removed by packet-copy remux; final duration remains intact.
    lines += ["file " + concat_quote(frame_paths[-1]), f"option framerate {tb.denominator}"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def encode_exact(frame_paths, rows, time_base: str, output: Path, source_audio: Path | None,
                 ffmpeg: str = "ffmpeg", preview: bool = False, threads: int = 2):
    output = require_new_output(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".encode-", dir=output.parent) as temporary:
        temporary = Path(temporary)
        concat = temporary / "frames.ffconcat"
        write_concat(concat, frame_paths, rows, time_base)
        encoded = temporary / "with-sentinel.mp4"
        codec = (["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", *preview_color_args()] if preview else
                 ["-c:v", "libx264rgb", "-crf", "0", "-pix_fmt", "rgb24"])
        subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(concat), "-map", "0:v:0", *codec, "-preset", "veryfast" if preview else "ultrafast",
                        "-bf", "0", "-threads", str(threads), "-enc_time_base", time_base,
                        "-video_track_timescale", str(Fraction(time_base).denominator),
                        "-fps_mode", "passthrough", str(encoded)], check=True)
        # -frames:v can terminate muxing before a longer audio track finishes.
        # Remove the sentinel from VIDEO ONLY first, then mux all original audio
        # in a separate copy step with neither a frame limit nor -shortest.
        trimmed = temporary / "video-only.mp4"
        subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i", str(encoded),
                        "-map", "0:v:0", "-frames:v", str(len(rows)), "-c", "copy",
                        "-video_track_timescale", str(Fraction(time_base).denominator), str(trimmed)], check=True)
        ready = temporary / "ready.mp4"
        args = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i", str(trimmed)]
        if source_audio:
            args += ["-i", str(source_audio)]
        args += ["-map", "0:v:0"]
        if source_audio:
            args += ["-map", "1:a:0"]
        args += ["-c", "copy", "-video_track_timescale",
                 str(Fraction(time_base).denominator), "-movflags", "+faststart", str(ready)]
        subprocess.run(args, check=True)
        ready.replace(output)


def audio_signature(path: Path, ffmpeg="ffmpeg", ffprobe="ffprobe"):
    data = probe(path, ffprobe, "a:0")
    streams = data["streams"]
    if not streams:
        return None
    stream = streams[0]
    packets = [[p.get(k) for k in ("pts", "dts", "duration", "size")] for p in data["packets"]]
    payload = capture([ffmpeg, "-v", "error", "-i", str(path), "-map", "0:a:0", "-c", "copy",
                       "-f", "hash", "-hash", "sha256", "-"]).strip()
    return {"codec_name": stream["codec_name"], "time_base": stream["time_base"],
            "duration_ticks": int(stream["duration_ts"]), "packet_count": len(packets),
            "packet_timing_sha256": hashlib.sha256(json.dumps(packets).encode()).hexdigest(),
            "compressed_payload_hash": payload}


def transcode_preview(input_movie: Path, output: Path, time_base="1/16000", ffmpeg="ffmpeg", threads=2):
    """Transcode an already-timed master without re-running segmentation."""
    output = require_new_output(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".preview-", dir=output.parent) as temporary:
        ready = Path(temporary) / "preview.mp4"
        subprocess.run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-i", str(input_movie),
                        "-map", "0:v:0", "-map", "0:a:0?", "-c:v", "libx264", "-crf", "18",
                        "-preset", "veryfast", "-pix_fmt", "yuv420p", "-bf", "0", "-threads", str(threads),
                        *preview_color_args(),
                        "-enc_time_base", time_base, "-video_track_timescale", str(Fraction(time_base).denominator),
                        "-fps_mode", "passthrough", "-c:a", "copy", "-movflags", "+faststart", str(ready)], check=True)
        ready.replace(output)


def verify_preview_colors(movie: Path, reference_movie: Path, rows, time_base: str, dimensions,
                          ffmpeg="ffmpeg", sample_frames=None):
    """Check decoded colour at representative frames, independently of tags.

    This catches an incorrect matrix with superficially correct BT.709 labels.
    Lossy pixel identity and whole-film semantic approval are NOT claimed.
    """
    import numpy as np
    from scipy import ndimage
    indices = sample_frames if sample_frames is not None else [9, 784, 1000, 2247, 4021, 4511, 4762]
    indices = [index for index in indices if 0 <= index < len(rows)]
    if not indices:
        indices = [0, len(rows) - 1]
    samples = []
    for index in sorted(set(indices)):
        source = np.frombuffer(decode_frame_at_pts(reference_movie, rows[index]["pts"], time_base, dimensions, ffmpeg),
                               dtype=np.uint8).reshape(dimensions[1], dimensions[0], 3)
        output = np.frombuffer(decode_frame_at_pts(movie, rows[index]["pts"], time_base, dimensions, ffmpeg),
                               dtype=np.uint8).reshape(dimensions[1], dimensions[0], 3)
        difference = np.abs(output.astype(np.int16) - source.astype(np.int16))
        mean_error = difference.mean(axis=(0, 1))
        if float(mean_error.max()) > 6.0:
            raise ValueError(f"Preview decoded colour error exceeds tolerance at frame {index}: {mean_error.tolist()}")
        red = (source[:, :, 0] > 110) & (source[:, :, 1] < 60) & (source[:, :, 2] < 60)
        pink = np.max(np.abs(source.astype(np.int16) - [213, 167, 169]), axis=2) <= 5
        skin = ((source[:, :, 0] > 235) & (source[:, :, 1] > 200) & (source[:, :, 1] < 242)
                & (source[:, :, 2] > 180) & (source[:, :, 2] < 232))
        regions = []
        for name, mask in [("red_core", red), ("pink_background", pink), ("skin_fill", skin)]:
            mask = ndimage.binary_erosion(mask, iterations=2)
            pixels = int(mask.sum())
            if pixels < 50:
                continue
            source_median = np.median(source[mask], axis=0)
            output_median = np.median(output[mask], axis=0)
            delta = np.abs(source_median - output_median)
            if float(delta.max()) > 5.0:
                raise ValueError(f"Preview colour shift at frame {index}, {name}: source {source_median.tolist()}, preview {output_median.tolist()}")
            regions.append({"region": name, "pixels": pixels, "reference_rgb_median": source_median.tolist(),
                            "preview_rgb_median": output_median.tolist(), "max_median_channel_delta": float(delta.max())})
        samples.append({"frame": index, "pts": rows[index]["pts"], "mean_absolute_rgb_error": mean_error.tolist(),
                        "regions": regions})
    return {"status": "pass", "sample_count": len(samples), "samples": samples,
            "maximum_per_channel_mean_error_allowed": 6.0, "maximum_flat_region_median_delta_allowed": 5.0,
            "scope": "Sampled decoded colour fidelity only; not lossless identity or semantic art approval"}


def verify_movie(output: Path, rows, time_base: str, frame_paths=None, source_audio=None,
                 ffmpeg="ffmpeg", ffprobe="ffprobe", expected_dimensions=None, expected_color_metadata=None):
    data = probe(output, ffprobe, "v:0")
    stream = data["streams"][0]
    packets = sorted(data["packets"], key=lambda packet: int(packet["pts"]))
    expected_pts = [r["pts"] for r in rows]
    actual_pts = [int(p["pts"]) for p in packets]
    expected_duration = rows[-1]["pts"] + rows[-1]["duration_ticks"]
    if stream["time_base"] != time_base or actual_pts != expected_pts:
        raise ValueError("Rendered movie frame count or exact PTS mismatch")
    if int(stream["duration_ts"]) != expected_duration:
        raise ValueError("Rendered movie final-frame duration mismatch")
    if [int(p["duration"]) for p in packets] != [r["duration_ticks"] for r in rows]:
        raise ValueError("Rendered movie per-frame duration mismatch")
    dimensions = [int(stream["width"]), int(stream["height"])]
    if expected_dimensions and dimensions != list(expected_dimensions):
        raise ValueError("Rendered movie dimensions mismatch")
    color_metadata = {key: stream.get(key) for key in PREVIEW_COLOR_METADATA}
    if expected_color_metadata is not None and color_metadata != expected_color_metadata:
        raise ValueError(f"Rendered movie colour metadata mismatch: {color_metadata}")
    report = {"status": "pass", "frame_count": len(packets), "time_base": time_base,
              "all_frame_pts_equal": True, "all_frame_durations_equal": True,
              "video_duration_ticks": expected_duration, "final_frame_duration_ticks": rows[-1]["duration_ticks"],
              "dimensions": dimensions, "all_frame_rgb_equal": None,
              "color_metadata": color_metadata,
              "semantic_quality_verified": False, "continuous_art_review_completed": False}
    if frame_paths is not None:
        decoded = decoded_rgb_md5(output, ffmpeg)
        expected = [rgb_md5(path) for path in frame_paths]
        if decoded != expected:
            unequal = [i for i, (a, b) in enumerate(zip(decoded, expected)) if a != b]
            raise ValueError(f"Decoded RGB round-trip mismatch: {len(decoded)} frames; first mismatches {unequal[:12]}")
        report["all_frame_rgb_equal"] = True
        report["rgb_frame_checksum_chain_sha256"] = hashlib.sha256("\n".join(expected).encode()).hexdigest()
    if source_audio:
        original_audio = audio_signature(source_audio, ffmpeg, ffprobe)
        rendered_audio = audio_signature(output, ffmpeg, ffprobe)
        if rendered_audio != original_audio:
            raise ValueError(f"Original audio packets/timestamps changed: source={original_audio}, output={rendered_audio}")
        report["audio_packet_copy_equal"] = True
        report["audio"] = rendered_audio
    return report


def render(project: Path, output: Path, layer_manifest: Path | None, ffmpeg="ffmpeg", ffprobe="ffprobe",
           preview=False, threads=2, frame_layer_manifest: Path | None = None):
    output = require_new_output(output)
    require_new_output(output.with_suffix(".verification.json"))
    source_report = validate_source(project, ffprobe)
    bindings = build_bindings(project, layer_manifest, frame_layer_manifest)
    panel_by_id = {p["panel_id"]: p for p in layer_panels(read_json(layer_manifest) if layer_manifest else None)}
    frame_partitions = read_json(frame_layer_manifest)["frames"] if frame_layer_manifest else None
    original_paths = [inside(project, row["original_frame"]) for row in bindings["frames"]]
    missing = [str(p) for p in original_paths if not p.is_file()]
    if missing:
        raise ValueError(f"Missing original frame cache: {missing[:3]}; run extract first")
    cache_report = validate_frame_cache(project, original_paths, ffmpeg)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".compose-", dir=output.parent) as temporary:
        temporary = Path(temporary)
        frame_paths = []
        layer_roundtrips = []
        partition_roundtrip_count = 0
        source_png_container_mismatches = 0
        for row, original in zip(bindings["frames"], original_paths):
            composition = row["composition"]
            if composition["mode"] == "frame_visible_partition":
                partition = frame_partitions[row["frame"]]
                reconstructed, container_difference = compose_frame_partition(project, partition, bindings["dimensions"], cache_report)
                source_png_container_mismatches += int(container_difference)
                result = temporary / f"F{row['frame']:06d}.png"
                reconstructed.save(result, compress_level=1)
                frame_paths.append(result)
                partition_roundtrip_count += 1
                if partition_roundtrip_count % 250 == 0:
                    print(f"recomposed frame partitions: {partition_roundtrip_count}/{len(frame_partitions)}", flush=True)
            elif composition["mode"] == "exact_source_layers":
                panel = panel_by_id[composition["panel_id"]]
                image = compose_layers(project, panel, bindings["dimensions"])
                with Image.open(original) as source:
                    if image.tobytes() != source.convert("RGB").tobytes():
                        raise ValueError(f"Layer reconstruction differs from source frame {row['frame']} ({panel['panel_id']})")
                result = temporary / f"F{row['frame']:06d}.png"
                image.save(result, compress_level=1)
                frame_paths.append(result)
                layer_roundtrips.append(panel["panel_id"])
            else:
                frame_paths.append(original)
        encode_exact(frame_paths, bindings["frames"], bindings["time_base"], output,
                     project / "source/original.mp4", ffmpeg, preview, threads)
        report = verify_movie(output, bindings["frames"], bindings["time_base"],
                              None if preview else frame_paths, project / "source/original.mp4",
                              ffmpeg, ffprobe, bindings["dimensions"], PREVIEW_COLOR_METADATA if preview else None)
    report.update({
        "kind": "lossy_viewing_preview" if preview else "lossless_RGB_roundtrip_diagnostic",
        "source_validation": source_report,
        "original_frame_cache_validation": cache_report,
        "composition_summary": bindings["summary"],
        "layer_compositions_rgb_equal": True,
        "layer_compositions_verified_count": len(layer_roundtrips),
        "layer_compositions_verified_panel_ids": layer_roundtrips,
        "per_frame_partition_compositions_verified_count": partition_roundtrip_count,
        "source_png_container_differences_with_verified_identical_rgb": source_png_container_mismatches,
        "source_fallback_is_not_layer_completion": True,
        "source_files_modified": False,
        "character_redesign_performed": False,
        "output_sha256": sha256(output),
        "output_bytes": output.stat().st_size,
    })
    if preview:
        report["color_sample_verification"] = verify_preview_colors(output, project / "source/original.mp4",
                                                                    bindings["frames"], bindings["time_base"],
                                                                    bindings["dimensions"], ffmpeg)
    write_json(output.with_suffix(".verification.json"), report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT_DEFAULT)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="Check immutable sources and actual integer video PTS")
    commands.add_parser("extract", help="Restore all original PNG frames; never overwrite an existing cache")
    binding_parser = commands.add_parser("bindings", help="Write evidence-qualified per-frame bindings")
    binding_parser.add_argument("--layers", type=Path)
    binding_parser.add_argument("--frame-layers", type=Path)
    binding_parser.add_argument("--output", type=Path)
    render_parser = commands.add_parser("render", help="Lossless original-pixel recomposition (not semantic approval)")
    render_parser.add_argument("--layers", type=Path)
    render_parser.add_argument("--frame-layers", type=Path, help="Use every frame's indexed original-pixel partition")
    render_parser.add_argument("--output", type=Path, required=True)
    render_parser.add_argument("--preview", action="store_true", help="Small H.264 viewing copy; RGB equality not claimed")
    render_parser.add_argument("--threads", type=int, default=2)
    preview_parser = commands.add_parser("preview", help="Make a small viewing copy from an existing exact-PTS master")
    preview_parser.add_argument("movie", type=Path)
    preview_parser.add_argument("--output", type=Path, required=True)
    preview_parser.add_argument("--threads", type=int, default=2)
    verify_parser = commands.add_parser("verify", help="Verify a finished lossless roundtrip against the original frames")
    verify_parser.add_argument("movie", type=Path)
    verify_parser.add_argument("--preview", action="store_true", help="Check timing/audio only, not lossless pixels")
    args = parser.parse_args(argv)
    project = args.project.resolve()
    if args.command == "validate":
        result = validate_source(project, args.ffprobe)
    elif args.command == "extract":
        result = extract_frames(project, args.ffmpeg, args.ffprobe)
    elif args.command == "bindings":
        result = build_bindings(project, args.layers, args.frame_layers)
        output = args.output or project / "data/frame_bindings.json"
        write_json(output, result, overwrite=True, expected_schema=SCHEMA)
        result = {"output": str(output), **result["summary"]}
    elif args.command == "render":
        if args.threads <= 0:
            parser.error("--threads must be positive")
        result = render(project, args.output, args.layers, args.ffmpeg,
                        args.ffprobe, args.preview, args.threads, args.frame_layers)
    elif args.command == "preview":
        if args.threads <= 0:
            parser.error("--threads must be positive")
        require_new_output(args.output)
        require_new_output(args.output.with_suffix(".verification.json"))
        source_validation = validate_source(project, args.ffprobe)
        bindings = build_bindings(project)
        source = project / "source/original.mp4"
        verify_movie(args.movie, bindings["frames"], bindings["time_base"], source_audio=source,
                     ffmpeg=args.ffmpeg, ffprobe=args.ffprobe, expected_dimensions=bindings["dimensions"])
        transcode_preview(args.movie, args.output, bindings["time_base"], args.ffmpeg, args.threads)
        result = verify_movie(args.output, bindings["frames"], bindings["time_base"], source_audio=source,
                              ffmpeg=args.ffmpeg, ffprobe=args.ffprobe, expected_dimensions=bindings["dimensions"],
                              expected_color_metadata=PREVIEW_COLOR_METADATA)
        result.update({"kind": "lossy_viewing_preview_from_master", "source_validation": source_validation,
                       "input_movie_sha256": sha256(args.movie), "output_sha256": sha256(args.output),
                       "output_bytes": args.output.stat().st_size,
                       "color_processing": "full-range RGB to BT.709 limited-range YUV420p, with explicit BT.709 range/matrix/transfer/primaries tags",
                       "pixel_identity_not_claimed_for_lossy_preview": True})
        result["color_sample_verification"] = verify_preview_colors(args.output, args.movie, bindings["frames"],
                                                                    bindings["time_base"], bindings["dimensions"], args.ffmpeg)
        write_json(args.output.with_suffix(".verification.json"), result)
    else:
        source_validation = validate_source(project, args.ffprobe)
        bindings = build_bindings(project)
        paths = None if args.preview else [inside(project, row["original_frame"]) for row in bindings["frames"]]
        cache_validation = validate_frame_cache(project, paths, args.ffmpeg) if paths else None
        result = verify_movie(args.movie, bindings["frames"], bindings["time_base"], paths,
                              project / "source/original.mp4", args.ffmpeg, args.ffprobe,
                              bindings["dimensions"], PREVIEW_COLOR_METADATA if args.preview else None)
        result["source_validation"] = source_validation
        result["original_frame_cache_validation"] = cache_validation
        if args.preview:
            result["color_sample_verification"] = verify_preview_colors(args.movie, project / "source/original.mp4",
                                                                        bindings["frames"], bindings["time_base"],
                                                                        bindings["dimensions"], args.ffmpeg)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
