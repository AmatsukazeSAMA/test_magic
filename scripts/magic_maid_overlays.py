#!/usr/bin/env python3
"""Portable subtitle/effect RGBA tracks, with every original frame's exact PTS.

This is deliberately separate from the reversible RGB *partition* pipeline.
The extractors estimate reusable visible overlays from the flattened source;
they cannot recover the author's original alpha or resolve every occlusion.
PNG assets are full canvas, straight alpha, with zero RGB outside alpha.
Content deduplication never implies drawing identity or guessed exposure holds.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time

import numpy as np
from PIL import Image, ImageDraw

from magic_maid_frame_layers import scene_routes
from magic_maid_timeline import (
    PROJECT_DEFAULT, SOURCE_HASHES, PREVIEW_COLOR_METADATA, build_bindings,
    chapter_index, decode_frame_at_pts, encode_exact, inside, read_json,
    reject_symlink_components, require_new_output, sha256, validate_frame_cache,
    validate_source, validated_timeline, verify_movie, video_metadata, write_json,
)

SCHEMA = "magic-maid.subtitle-effect-overlays/1"
VERIFY_SCHEMA = "magic-maid.overlay-integrity/1"
METHOD_VERSION = "exact-pts-straight-rgba-content-addressed-v1"
CATEGORIES = ("subtitles", "effects")
EXTRACTORS = {"subtitles": "magic_maid_subtitle_overlays", "effects": "magic_maid_effect_overlays"}
PROTECTED = {"source", "frames", "reference_frames", "cels", "layers", "frame_labels", "frame_exports"}


def rgba_stats(rgba, dimensions=None):
    if not isinstance(rgba, np.ndarray) or rgba.dtype != np.uint8 or rgba.ndim != 3 or rgba.shape[2] != 4:
        raise ValueError("Overlay must be uint8 HxWx4 straight RGBA")
    if dimensions and [rgba.shape[1], rgba.shape[0]] != list(dimensions):
        raise ValueError("Overlay must retain the original full canvas")
    alpha = rgba[:, :, 3]
    if np.any(rgba[:, :, :3][alpha == 0]):
        raise ValueError("Transparent overlay pixels must have zero RGB")
    y, x = np.nonzero(alpha)
    return {
        "nonzero_alpha_pixels": int(len(x)),
        "partial_alpha_pixels": int(np.count_nonzero((alpha > 0) & (alpha < 255))),
        "opaque_pixels": int(np.count_nonzero(alpha == 255)),
        "bbox": [int(x.min()), int(y.min()), int(x.max()) + 1, int(y.max()) + 1] if len(x) else None,
    }


def normalize_metadata(metadata):
    if not isinstance(metadata, dict) or not isinstance(metadata.get("status"), str) or not metadata["status"]:
        raise ValueError("Extractor must explicitly declare a nonempty status")
    # Reject numpy scalars, NaN, and other nonportable metadata at the boundary.
    return json.loads(json.dumps(metadata, ensure_ascii=False, allow_nan=False))


def code_fingerprint():
    directory = Path(__file__).resolve().parent
    names = [Path(__file__).name, "magic_maid_timeline.py", "magic_maid_frame_layers.py", "magic_maid_layers.py"]
    names += [name + ".py" for name in EXTRACTORS.values()]
    return {"scripts/" + name: sha256(directory / name) for name in names}


def extractor_dependencies(project):
    """Hash any explicit temporal-template inputs as well as the Python code."""
    result = {}
    for module_name in EXTRACTORS.values():
        module = importlib.import_module(module_name)
        configure = getattr(module, "configure_project", None)
        if configure:
            configure(project)
        dependencies = getattr(module, "DATA_DEPENDENCIES", ())
        if not isinstance(dependencies, (list, tuple)):
            raise ValueError("Extractor DATA_DEPENDENCIES must enumerate project-relative files")
        for relative in dependencies:
            if not isinstance(relative, str):
                raise ValueError("Invalid extractor data dependency")
            result[relative] = sha256(safe_project_path(project, relative))
    return result


def load_timing(project):
    meta = video_metadata(project)
    rows = validated_timeline(read_json(project / "data/original_timeline.json"),
                              meta["time_base"], int(meta["duration_ts"]))
    chapters = chapter_index(read_json(project / "data/chapters.json"), len(rows))
    return rows, chapters, meta


def safe_project_path(project, relative):
    reject_symlink_components(project / relative)
    return inside(project, relative)


def prepare_build_paths(project, output_relative, manifest_relative, resume=False):
    output = safe_project_path(project, output_relative)
    manifest = safe_project_path(project, manifest_relative)
    output_parts = output.relative_to(project.resolve()).parts
    manifest_parts = manifest.relative_to(project.resolve()).parts
    if not output_parts or output_parts[0] in PROTECTED | {"data"}:
        raise ValueError("Overlay assets require a new dedicated output directory")
    if not manifest_parts or manifest_parts[0] in PROTECTED or manifest.suffix != ".json":
        raise ValueError("Manifest must be a new JSON path outside protected source/asset directories")
    require_new_output(manifest)
    partial = manifest.with_suffix(".partial.json")
    reject_symlink_components(partial)
    if not resume:
        require_new_output(partial)
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise ValueError("Refusing to overwrite existing overlay assets; select a new output directory")
    elif not partial.is_file():
        raise ValueError("Resume requires the matching incomplete checkpoint")
    return output, manifest, partial


def store_rgba(project, root, category, rgba):
    stats = rgba_stats(rgba)
    digest = hashlib.sha256(rgba.tobytes()).hexdigest()
    relative = f"{root}/{category}/{digest}.png"
    target = safe_project_path(project, relative)
    # Concurrent repeated frames can have the same asset. Link an exclusive
    # temporary file into place, never overwrite a pre-existing destination.
    if not target.exists():
        with tempfile.NamedTemporaryFile(prefix=".rgba-", suffix=".png", dir=target.parent, delete=False) as handle:
            temporary = Path(handle.name)
        try:
            Image.fromarray(rgba).save(temporary, compress_level=6)
            reject_symlink_components(target)
            try:
                os.link(temporary, target)
            except FileExistsError:
                pass
        finally:
            temporary.unlink(missing_ok=True)
    with Image.open(target) as image:
        if image.mode != "RGBA" or image.size != (rgba.shape[1], rgba.shape[0]):
            raise ValueError("Existing content-addressed asset has invalid mode/canvas")
        if hashlib.sha256(image.tobytes()).hexdigest() != digest:
            raise ValueError("Existing content-addressed asset was altered")
    return digest, {"path": relative, "rgba_sha256": digest, "png_sha256": sha256(target),
                    "bytes": target.stat().st_size, **stats}


def _build_frame(job):
    project_text, root, route, dimensions = job
    project = Path(project_text)
    frame = route["frame"]
    original_relative = f"frames/F{frame:06d}.png"
    original = safe_project_path(project, original_relative)
    with Image.open(original) as image:
        if image.size != tuple(dimensions):
            raise ValueError(f"Wrong original frame dimensions at F{frame}")
        rgb = np.array(image.convert("RGB"))
    # Neither extractor may modify source RGB handed to the other category.
    rgb.setflags(write=False)
    overlays, assets = {}, {}
    for category, module_name in EXTRACTORS.items():
        module = importlib.import_module(module_name)
        configure = getattr(module, "configure_project", None)
        if configure:
            configure(project)
        rgba, metadata = module.extract_overlay(rgb, frame, route["chapter_id"], route["group"])
        rgba_stats(rgba, dimensions)
        metadata = normalize_metadata(metadata)
        asset_id, asset = store_rgba(project, root, category, rgba)
        assets[category] = (asset_id, asset)
        overlays[category] = {"asset_id": asset_id, "status": metadata["status"],
                              "requires_review": True, "metadata": metadata}
    return ({**route, "original_frame": original_relative, "source_png_sha256": sha256(original),
             "source_rgb_sha256": hashlib.sha256(rgb.tobytes()).hexdigest(),
             "source_rgb_md5": hashlib.md5(rgb.tobytes()).hexdigest(), "overlays": overlays}, assets)


def make_exposures(frames):
    result = {}
    for category in CATEGORIES:
        runs = []
        for row in frames:
            asset = row["overlays"][category]["asset_id"]
            end_pts = row["pts"] + row["duration_ticks"]
            if runs and runs[-1]["asset_id"] == asset:
                runs[-1]["end_frame_exclusive"] = row["frame"] + 1
                runs[-1]["end_pts_exclusive"] = end_pts
            else:
                runs.append({"start_frame": row["frame"], "end_frame_exclusive": row["frame"] + 1,
                             "start_pts": row["pts"], "end_pts_exclusive": end_pts, "asset_id": asset})
        result[category] = runs
    return result


def summarize(frames, assets):
    categories = {}
    for category in CATEGORIES:
        selected = [assets[category][row["overlays"][category]["asset_id"]] for row in frames]
        categories[category] = {
            "unique_assets": len(assets[category]),
            "unique_nonempty_assets": sum(a["nonzero_alpha_pixels"] > 0 for a in assets[category].values()),
            "asset_bytes": sum(a["bytes"] for a in assets[category].values()),
            "nonempty_frames": sum(a["nonzero_alpha_pixels"] > 0 for a in selected),
            "empty_frames": sum(a["nonzero_alpha_pixels"] == 0 for a in selected),
            "frames_with_partial_alpha": sum(a["partial_alpha_pixels"] > 0 for a in selected),
            "status_counts": dict(Counter(row["overlays"][category]["status"] for row in frames)),
        }
    return {"categories": categories, "all_original_frames_mapped": True,
            "every_frame_requires_semantic_review": True,
            "empty_alpha_is_not_proof_that_no_overlay_exists": True,
            "original_author_alpha_recovered": False,
            "no_orchestrator_source_frame_fallback": True}


def build(project, output_relative="overlays", manifest_relative="data/overlay_manifest.json",
          workers=4, resume=False, ffmpeg="ffmpeg", ffprobe="ffprobe"):
    project = project.resolve()
    if workers < 1:
        raise ValueError("workers must be positive")
    output, manifest, partial = prepare_build_paths(project, output_relative, manifest_relative, resume)
    code = code_fingerprint()
    dependencies = extractor_dependencies(project)
    source = validate_source(project, ffprobe, verify_reference=False)
    bindings = build_bindings(project)
    routes = scene_routes(read_json(project / "data/panel_catalog.json"), bindings)
    original_paths = [safe_project_path(project, f"frames/F{i:06d}.png") for i in range(len(routes))]
    print("Independently checking all cached source RGB frames before extraction...", flush=True)
    cache = validate_frame_cache(project, original_paths, ffmpeg)
    base = {"schema": SCHEMA, "method_version": METHOD_VERSION,
            "source": "source/original.mp4", "source_sha256": SOURCE_HASHES["original"],
            "source_validation": source, "source_cache_verification": cache,
            "code_sha256": code, "extractor_data_sha256": dependencies,
            "extractor_versions": {category: getattr(importlib.import_module(name), "METHOD_VERSION", "undeclared")
                                   for category, name in EXTRACTORS.items()},
            "routing_inputs_sha256": {name: sha256(project / name) for name in
                                       ["data/chapters.json", "data/panel_catalog.json", "data/original_timeline.json"]},
            "asset_root": output_relative, "alpha_mode": "straight", "transparent_rgb": [0, 0, 0],
            "rgba_format": "uint8 RGBA PNG", "dimensions": bindings["dimensions"],
            "frame_count": len(routes), "time_base": bindings["time_base"],
            "video_duration_ticks": bindings["video_duration_ticks"],
            "production_ready": False, "original_alpha_recovered": False,
            "source_video_is_flattened": True, "reference_video_pixels_used": False,
            "content_deduplication_is_not_cel_identity": True,
            "limitations": ["Estimated visible overlays, not recovered original author layers.",
                            "Ambiguous and unsupported frames remain explicitly marked; transparent output does not assert absence.",
                            "Subtitles and effects are separate tracks; overlapping pixels may need manual order/matte correction.",
                            "Per-frame extractor evidence and limitations must be reviewed before production use."]}
    frames, assets = [], {name: {} for name in CATEGORIES}
    if resume:
        checkpoint = read_json(partial)
        for key in ("schema", "source_sha256", "code_sha256", "extractor_data_sha256", "routing_inputs_sha256", "asset_root",
                    "dimensions", "frame_count", "time_base", "video_duration_ticks"):
            if checkpoint.get(key) != base[key]:
                raise ValueError(f"Checkpoint {key} changed; use a new output directory")
        frames, assets = checkpoint["frames"], checkpoint["assets"]
        for index, row in enumerate(frames):
            if any(row.get(key) != routes[index][key] for key in routes[index]):
                raise ValueError("Checkpoint source route/timing mismatch")
            if sha256(original_paths[index]) != row["source_png_sha256"]:
                raise ValueError("Checkpoint source frame changed")
        for category in CATEGORIES:
            for asset_id, asset in assets[category].items():
                verify_asset(project, asset_id, asset, bindings["dimensions"], output_relative, category)
        print(f"Resuming verified overlay checkpoint at {len(frames)}/{len(routes)}", flush=True)
    for category in CATEGORIES:
        safe_project_path(project, f"{output_relative}/{category}").mkdir(parents=True, exist_ok=True)
    jobs = [(str(project), output_relative, route, bindings["dimensions"]) for route in routes[len(frames):]]
    initial_count, started = len(frames), time.perf_counter()
    pool = ProcessPoolExecutor(max_workers=workers)
    try:
        for row, new_assets in pool.map(_build_frame, jobs, chunksize=1):
            frames.append(row)
            for category, (asset_id, asset) in new_assets.items():
                if asset_id in assets[category] and assets[category][asset_id] != asset:
                    raise ValueError("Content-addressed overlay asset changed during build")
                assets[category][asset_id] = asset
            if len(frames) % 100 == 0 or len(frames) == len(routes):
                if code_fingerprint() != code or extractor_dependencies(project) != dependencies:
                    raise ValueError("Extractor code/data changed during generation; use a new output directory")
                elapsed = time.perf_counter() - started
                rate = (len(frames) - initial_count) / max(elapsed, 0.001)
                print(f"overlay frames: {len(frames)}/{len(routes)}; {rate:.2f} frames/s; {elapsed:.1f}s processing", flush=True)
                write_json(partial, {**base, "build_complete": False, "completed_frames": len(frames),
                                     "assets": assets, "frames": frames}, overwrite=True, expected_schema=SCHEMA)
    except BaseException:
        pool.shutdown(wait=True, cancel_futures=True)
        raise
    else:
        pool.shutdown(wait=True)
    consumed_chain = hashlib.sha256("\n".join(row["source_rgb_md5"] for row in frames).encode()).hexdigest()
    if consumed_chain != cache["rgb_frame_checksum_chain_sha256"]:
        raise ValueError("Source RGB changed between independent cache validation and overlay extraction")
    if code_fingerprint() != code or extractor_dependencies(project) != dependencies:
        raise ValueError("Code/data changed during generation")
    result = {**base, "build_complete": True, "completed_frames": len(frames), "assets": assets, "frames": frames,
              "summary": summarize(frames, assets), "exposures": make_exposures(frames)}
    write_json(manifest, result)
    partial.unlink()
    return {"manifest": str(manifest), **result["summary"]}


def verify_asset(project, asset_id, asset, dimensions, root, category):
    if len(asset_id) != 64 or any(c not in "0123456789abcdef" for c in asset_id):
        raise ValueError("Invalid overlay content hash")
    if asset.get("path") != f"{root}/{category}/{asset_id}.png" or asset.get("rgba_sha256") != asset_id:
        raise ValueError("Asset path/content identity mismatch")
    path = safe_project_path(project, asset["path"])
    if sha256(path) != asset["png_sha256"] or path.stat().st_size != asset["bytes"]:
        raise ValueError(f"PNG file changed: {asset['path']}")
    with Image.open(path) as image:
        if image.mode != "RGBA":
            raise ValueError("Overlay PNG is not RGBA")
        rgba = np.array(image)
    stats = rgba_stats(rgba, dimensions)
    if hashlib.sha256(rgba.tobytes()).hexdigest() != asset_id:
        raise ValueError("Decoded overlay RGBA checksum mismatch")
    if any(asset.get(key) != value for key, value in stats.items()):
        raise ValueError("Asset alpha/bounds statistics mismatch")
    return stats


def verify_manifest(project, manifest_path, check_source=True, check_cache=False):
    """Independent saved-PNG reader: does NOT call either extraction function.

    This proves saved RGBA integrity, mapped timing, and declared provenance;
    it deliberately does not use a partition roundtrip as semantic matte QA.
    """
    project = project.resolve()
    data = read_json(manifest_path)
    rows, chapters, meta = load_timing(project)
    if data.get("schema") != SCHEMA or data.get("build_complete") is not True:
        raise ValueError("Not a completed subtitle/effect overlay manifest")
    if (data.get("time_base") != meta["time_base"] or data.get("video_duration_ticks") != int(meta["duration_ts"])
            or data.get("dimensions") != [int(meta["width"]), int(meta["height"])]
            or data.get("frame_count") != len(rows) or data.get("completed_frames") != len(rows)
            or len(data.get("frames", [])) != len(rows)):
        raise ValueError("Overlay timeline/canvas differs from original")
    if data.get("alpha_mode") != "straight" or data.get("transparent_rgb") != [0, 0, 0]:
        raise ValueError("Undeclared/unsupported alpha convention")
    root = data["asset_root"]
    safe_project_path(project, root)
    if set(data["assets"]) != set(CATEGORIES):
        raise ValueError("Subtitle/effect categories must remain separate")
    if check_source:
        if data.get("source") != "source/original.mp4" or data.get("source_sha256") != SOURCE_HASHES["original"]:
            raise ValueError("Unexpected overlay pixel source")
        source_report = validate_source(project, verify_reference=False)
    else:
        source_report = {"status": "not_checked"}
    used = {category: set() for category in CATEGORIES}
    for index, (row, expected) in enumerate(zip(data["frames"], rows)):
        if any(row.get(key) != expected[key] for key in ("frame", "pts", "duration_ticks")):
            raise ValueError(f"Overlay frame/PTS/duration mismatch at {index}")
        if row.get("chapter_id") != chapters[index] or row.get("original_frame") != f"frames/F{index:06d}.png":
            raise ValueError("Overlay source mapping mismatch")
        for key, length in (("source_png_sha256", 64), ("source_rgb_sha256", 64), ("source_rgb_md5", 32)):
            value = row.get(key)
            if not isinstance(value, str) or len(value) != length or any(c not in "0123456789abcdef" for c in value):
                raise ValueError("Missing/invalid per-frame source provenance checksum")
        if set(row["overlays"]) != set(CATEGORIES):
            raise ValueError("Every original frame must map both overlay tracks, including empty frames")
        for category in CATEGORIES:
            ref = row["overlays"][category]
            if ref["asset_id"] not in data["assets"][category]:
                raise ValueError("Frame references a missing overlay asset")
            metadata = normalize_metadata(ref["metadata"])
            if ref.get("status") != metadata["status"] or ref.get("requires_review") is not True:
                raise ValueError("Per-frame overlay status/semantic review caveat missing")
            used[category].add(ref["asset_id"])
        if check_cache:
            path = safe_project_path(project, row["original_frame"])
            if sha256(path) != row["source_png_sha256"]:
                raise ValueError("Cached original PNG differs from the extracted input")
            with Image.open(path) as image:
                raw = image.convert("RGB").tobytes()
            if (hashlib.sha256(raw).hexdigest() != row["source_rgb_sha256"]
                    or hashlib.md5(raw).hexdigest() != row["source_rgb_md5"]):
                raise ValueError("Cached original RGB differs from overlay provenance")
    for category in CATEGORIES:
        if used[category] != set(data["assets"][category]):
            raise ValueError("Unreferenced/missing deduplicated overlay asset")
        directory = safe_project_path(project, f"{root}/{category}")
        actual_names = {path.name for path in directory.glob("*.png")}
        if actual_names != {asset_id + ".png" for asset_id in data["assets"][category]}:
            raise ValueError("Overlay directory contains missing or unindexed PNG assets")
        for asset_id, asset in data["assets"][category].items():
            verify_asset(project, asset_id, asset, data["dimensions"], root, category)
    consumed_chain = hashlib.sha256("\n".join(row["source_rgb_md5"] for row in data["frames"]).encode()).hexdigest()
    cache_proof = data.get("source_cache_verification", {})
    if (cache_proof.get("all_cached_rgb_equal_source_decode") is not True
            or cache_proof.get("frame_count") != len(rows)
            or cache_proof.get("rgb_frame_checksum_chain_sha256") != consumed_chain):
        raise ValueError("Consumed input RGB fingerprints differ from the independent source-decode proof")
    if data.get("exposures") != make_exposures(data["frames"]):
        raise ValueError("Content exposure runs differ from exact frame mappings")
    summary = summarize(data["frames"], data["assets"])
    if data.get("summary") != summary:
        raise ValueError("Overlay summary differs from independently counted PNG/frame contents")
    return {"schema": VERIFY_SCHEMA, "status": "pass", "manifest_sha256": sha256(manifest_path),
            "source_validation": source_report, "cached_source_png_and_rgb_checked": check_cache,
            "frame_count": len(rows), "time_base": data["time_base"],
            "video_duration_ticks": data["video_duration_ticks"],
            "final_frame_duration_ticks": rows[-1]["duration_ticks"],
            "all_frame_pts_and_durations_equal": True,
            "all_saved_rgba_content_and_file_hashes_equal": True,
            "consumed_source_rgb_chain_matches_build_source_decode_proof": True,
            "all_transparent_pixels_zero_rgb": True, "all_full_canvas_rgba": True,
            "exposure_mapping_verified": True, "summary": summary,
            "semantic_quality_verified": False, "original_author_alpha_recovered": False,
            "scope": "Independent saved-file/timing/alpha-contract verification, NOT clean-matte approval"}


def write_portable_concat(path, filenames, rows, time_base):
    """Relative paths keep exported sequences movable; sentinel is documented."""
    tb = Fraction(time_base)
    if tb.numerator != 1 or len(filenames) != len(rows) or not rows:
        raise ValueError("Invalid exact-timing PNG sequence")
    lines = ["ffconcat version 1.0"]
    for name, row in zip(filenames, rows):
        if "'" in name or "\n" in name or "\r" in name or Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError("Unsafe portable sequence filename")
        start = round(row["pts"] * tb * 1_000_000)
        end = round((row["pts"] + row["duration_ticks"]) * tb * 1_000_000)
        duration = end - start
        lines += [f"file '{name}'", f"option framerate {tb.denominator}",
                  f"duration {duration // 1_000_000}.{duration % 1_000_000:06d}"]
    lines += [f"file '{filenames[-1]}'", f"option framerate {tb.denominator}"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_sequence(project, manifest_path, output, category="both"):
    output = require_new_output(output)
    report = verify_manifest(project, manifest_path)
    data = read_json(manifest_path)
    categories = CATEGORIES if category == "both" else (category,)
    if any(c not in CATEGORIES for c in categories):
        raise ValueError("Unknown overlay category")
    output.mkdir(parents=True)
    for name in categories:
        destination = output / name
        destination.mkdir()
        filenames = []
        for row in data["frames"]:
            ref = data["assets"][name][row["overlays"][name]["asset_id"]]
            filename = f"F{row['frame']:06d}.png"
            # Real portable copies, not absolute symlinks or mutable hard links.
            shutil.copyfile(safe_project_path(project, ref["path"]), destination / filename)
            if sha256(destination / filename) != ref["png_sha256"]:
                raise ValueError("Exported sequence PNG copy failed verification")
            filenames.append(f"{name}/{filename}")
        write_portable_concat(output / f"{name}.ffconcat", filenames, data["frames"], data["time_base"])
    write_json(output / "sequence.json", {
        "schema": "magic-maid.overlay-sequence/1", "manifest_sha256": sha256(manifest_path),
        "categories": list(categories), "alpha_mode": "straight", "dimensions": data["dimensions"],
        "time_base": data["time_base"], "video_duration_ticks": data["video_duration_ticks"],
        "frame_count": data["frame_count"],
        "frames": [{key: row[key] for key in ("frame", "pts", "duration_ticks")} for row in data["frames"]],
        "ffconcat_final_duplicate_is_timing_sentinel_not_an_extra_source_frame": True,
        "import_note": "Use these integer PTS/durations, not a fixed 30fps image-sequence assumption. FFconcat ends with one timing sentinel; strip it after encoding as encode_exact does.",
        "integrity_verification": report,
    })
    return {"status": "pass", "output": str(output), "categories": list(categories),
            "frame_count_per_category": data["frame_count"]}


def checkerboard(width, height, cell=48):
    y, x = np.indices((height, width))
    shade = np.where(((x // cell) + (y // cell)) % 2, 78, 46).astype(np.uint8)
    return np.repeat(shade[:, :, None], 3, axis=2)


def composite_straight(rgba, background):
    rgba_stats(rgba, [background.shape[1], background.shape[0]])
    if background.dtype != np.uint8 or background.shape != rgba.shape[:2] + (3,):
        raise ValueError("Background must match overlay canvas")
    a = rgba[:, :, 3:4].astype(np.uint32)
    return ((rgba[:, :, :3].astype(np.uint32) * a + background.astype(np.uint32) * (255 - a) + 127) // 255).astype(np.uint8)


def _preview_frame(job):
    project_text, subtitle, effect, output_text, dimensions = job
    project = Path(project_text)
    width, height = dimensions
    background = checkerboard(width, height)
    canvas = Image.new("RGB", (width, height // 2 + 36), (24, 24, 24))
    for index, relative in enumerate((subtitle, effect)):
        with Image.open(safe_project_path(project, relative)) as image:
            rgba = np.array(image)
        composite = Image.fromarray(composite_straight(rgba, background))
        canvas.paste(composite.resize((width // 2, height // 2), Image.Resampling.LANCZOS), (index * (width // 2), 36))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 11), "SUBTITLES / estimated straight alpha / checkerboard / needs review", fill=(230, 230, 230))
    draw.text((width // 2 + 12, 11), "EFFECTS / estimated straight alpha / checkerboard / needs review", fill=(230, 230, 230))
    canvas.save(output_text, compress_level=1)
    return output_text


def verify_preview_samples(movie, frame_paths, rows, time_base, dimensions, ffmpeg="ffmpeg"):
    """Compare decoded viewing-copy samples to actual saved-overlay composites."""
    indices = sorted({0, len(rows) - 1} | {f for f in (89, 784, 1247, 2247, 4021, 4679) if f < len(rows)})
    samples = []
    for index in indices:
        with Image.open(frame_paths[index]) as image:
            expected = np.array(image.convert("RGB"))
        decoded = np.frombuffer(decode_frame_at_pts(movie, rows[index]["pts"], time_base, dimensions, ffmpeg),
                                dtype=np.uint8).reshape(dimensions[1], dimensions[0], 3)
        error = np.abs(expected.astype(np.int16) - decoded.astype(np.int16)).mean(axis=(0, 1))
        if float(error.max()) > 6:
            raise ValueError(f"Checker preview differs from saved RGBA composition at F{index}: {error.tolist()}")
        samples.append({"frame": index, "pts": rows[index]["pts"], "mean_absolute_rgb_error": error.tolist(),
                        "expected_composite_rgb_sha256": hashlib.sha256(expected.tobytes()).hexdigest()})
    return {"status": "pass", "sample_count": len(samples), "samples": samples,
            "maximum_per_channel_mean_error_allowed": 6,
            "scope": "Lossy checker-preview fidelity to saved overlay compositions, not semantic matte approval"}


def preview(project, manifest_path, output, workers=4, threads=4, ffmpeg="ffmpeg", ffprobe="ffprobe"):
    output = require_new_output(output)
    require_new_output(output.with_suffix(".verification.json"))
    integrity = verify_manifest(project, manifest_path)
    data = read_json(manifest_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".overlay-preview-", dir=output.parent) as temporary:
        temporary = Path(temporary)
        pairs, paths = {}, []
        jobs = []
        for row in data["frames"]:
            pair = tuple(row["overlays"][c]["asset_id"] for c in CATEGORIES)
            if pair not in pairs:
                path = temporary / f"P{len(pairs):06d}.png"
                pairs[pair] = path
                jobs.append((str(project), data["assets"]["subtitles"][pair[0]]["path"],
                             data["assets"]["effects"][pair[1]]["path"], str(path), data["dimensions"]))
            paths.append(pairs[pair])
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for index, _ in enumerate(pool.map(_preview_frame, jobs, chunksize=1), 1):
                if index % 250 == 0 or index == len(jobs):
                    print(f"checkerboard preview composites: {index}/{len(jobs)}", flush=True)
        encode_exact(paths, data["frames"], data["time_base"], output,
                     project / "source/original.mp4", ffmpeg, preview=True, threads=threads)
        dimensions = [data["dimensions"][0], data["dimensions"][1] // 2 + 36]
        verification = verify_movie(output, data["frames"], data["time_base"],
                                    source_audio=project / "source/original.mp4", ffmpeg=ffmpeg, ffprobe=ffprobe,
                                    expected_dimensions=dimensions, expected_color_metadata=PREVIEW_COLOR_METADATA)
        preview_pixels = verify_preview_samples(output, paths, data["frames"], data["time_base"], dimensions, ffmpeg)
    report = {"schema": "magic-maid.overlay-preview-verification/1", **verification,
              "manifest_sha256": sha256(manifest_path), "output_sha256": sha256(output),
              "output_bytes": output.stat().st_size, "integrity_verification": integrity,
              "decoded_overlay_composite_samples": preview_pixels,
              "background": "neutral dark checkerboard; no original flattened video behind overlays",
              "layout": "subtitles left, effects right; each 50% linear-size viewing copy",
              "alpha_in_this_mp4": False, "primary_alpha_assets": data["asset_root"],
              "semantic_quality_verified": False, "original_author_alpha_recovered": False}
    write_json(output.with_suffix(".verification.json"), report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT_DEFAULT)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="Extract both tracks from all exact original frames")
    build_parser.add_argument("--output", default="overlays", help="New project-relative asset directory")
    build_parser.add_argument("--manifest", default="data/overlay_manifest.json")
    build_parser.add_argument("--workers", type=int, default=4)
    build_parser.add_argument("--resume", action="store_true")
    verify_parser = commands.add_parser("verify", help="Independently reread saved RGBA, all mappings, and hashes")
    verify_parser.add_argument("--manifest", default="data/overlay_manifest.json")
    verify_parser.add_argument("--output", type=Path)
    verify_parser.add_argument("--check-cache", action="store_true")
    export_parser = commands.add_parser("export-sequence", help="Expand deduplicated tracks into ordinary fullcanvas PNG sequences")
    export_parser.add_argument("--manifest", default="data/overlay_manifest.json")
    export_parser.add_argument("--category", choices=["both", *CATEGORIES], default="both")
    export_parser.add_argument("--output", type=Path, required=True)
    preview_parser = commands.add_parser("preview", help="Fulltimeline two-track viewing movie over checkerboard, not source")
    preview_parser.add_argument("--manifest", default="data/overlay_manifest.json")
    preview_parser.add_argument("--output", type=Path, required=True)
    preview_parser.add_argument("--workers", type=int, default=4)
    preview_parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args(argv)
    project = args.project.resolve()
    if args.command == "build":
        result = build(project, args.output, args.manifest, args.workers, args.resume)
    else:
        manifest = safe_project_path(project, args.manifest)
        if args.command == "verify":
            if args.output:
                require_new_output(args.output)
            result = verify_manifest(project, manifest, check_cache=args.check_cache)
            if args.output:
                write_json(args.output, result)
        elif args.command == "export-sequence":
            result = export_sequence(project, manifest, args.output, args.category)
        else:
            result = preview(project, manifest, args.output, args.workers, args.threads)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
