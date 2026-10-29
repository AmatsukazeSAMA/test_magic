#!/usr/bin/env python3
"""Compact per-frame visible-pixel partitions, never guessed cel holds.

Each indexed PNG labels the pixels of ONE original RGB frame.  Colour IDs are
not alpha mattes or recovered hidden art.  Reconstructing all observed pixels
checks integrity only: semantic boundaries still require visual correction.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import numpy as np
from PIL import Image

from magic_maid_layers import LAYER_ORDER, METHOD_VERSION, rgba_from_mask, split_visible_frame
from magic_maid_timeline import (PROJECT_DEFAULT, build_bindings, inside, read_json,
                                 sha256, validate_source, write_json, decode_frame_at_pts, SOURCE_HASHES)
from magic_maid_timeline import reject_symlink_components


SCHEMA = "magic-maid.frame-visible-partitions/1"
PALETTE = [
    213, 167, 169,  # observed background
    90, 139, 190,   # environment / props
    60, 182, 113,   # visible subject
    245, 245, 245,  # visible subtitles
    242, 163, 44,   # visible effects
    188, 70, 170,   # unresolved visible pixels
] + [0] * (768 - 18)

# These are documented SCENE classifiers only. No transform, drawing identity,
# hold length, or frame mask is copied from the referenced earlier scene.
CHAPTER_GROUPS = {
    "M15": ("X03", "documented black/white text and ring effects"),
    "M21": ("G12", "documented close-up recurrence; classify actual frame independently"),
    "M24": ("G12", "documented half-body recurrence; classify actual frame independently"),
    "M25": ("G13", "documented black-strip recurrence; classify actual frame independently"),
    "M26": ("X04", "documented clock/vine/title composition"),
    "M27": ("X05", "documented short text and petals; no visible character"),
    "M28": ("X01", "documented red-dress full-body original supplement"),
    "M29": ("X02", "documented red-dress half-body original supplement"),
    "M30": ("X05", "documented short text/heart interval outside G47 numbered range"),
    "M34": ("G03", "documented horizontal-frame recurrence with separately moving petals"),
}


def scene_routes(catalog, bindings):
    """Route by declared ranges, never by nearest image/pose or reference PTS."""
    ranges = {}
    for panel in catalog:
        if panel.get("source_search_range"):
            start, end = panel["source_search_range"]
            group = panel["group"]
            if not 0 <= start < end <= bindings["frame_count"]:
                raise ValueError(f"Invalid source_search_range for {panel['id']}")
            ranges[(start, end, group)] = True
    routes = []
    for row in bindings["frames"]:
        frame, chapter = row["frame"], row["chapter_id"]
        matches = [(start, end, group) for start, end, group in ranges if start <= frame < end]
        groups = {group for _, _, group in matches}
        if len(groups) == 1:
            group = next(iter(groups))
            evidence = "catalog.source_search_range (scene hint only; not character identity)"
        elif len(groups) > 1:
            group = ""
            evidence = "conflicting catalog scene ranges; foreground remains unresolved"
        elif frame in range(818, 834) and chapter == "M08":
            group = "G11"
            evidence = "documented M08 closing orange full-screen wipe continuation; no cel identity inferred"
        elif 2948 <= frame < 2959 and chapter == "M22":
            group = "G12"
            evidence = "new original-frame audit: F2948/F2954 still show two close-up black-maid states; F2959 starts vines. Scene classifier only, no drawing-identity merge"
        elif chapter in CHAPTER_GROUPS:
            group, evidence = CHAPTER_GROUPS[chapter]
        else:
            group = ""
            evidence = "no proved scene classifier; nonbackground/nonpetal pixels remain unresolved"
        routes.append({"frame": frame, "pts": row["pts"], "duration_ticks": row["duration_ticks"],
                       "chapter_id": chapter, "group": group, "routing_evidence": evidence,
                       "character_identity_inferred": False})
    return routes


def labels_from_masks(masks, shape):
    labels = np.zeros(shape, dtype=np.uint8)
    coverage = np.zeros(shape, dtype=np.uint8)
    if set(masks) != set(LAYER_ORDER):
        raise ValueError("Unexpected category mask set")
    for index, name in enumerate(LAYER_ORDER):
        mask = masks[name]
        if mask.dtype != np.bool_ or mask.shape != shape:
            raise ValueError(f"Invalid mask shape/type for {name}")
        coverage += mask
        labels[mask] = index
    if not np.all(coverage == 1):
        raise ValueError("Masks must partition every source pixel exactly once")
    return labels


def read_labels(path: Path, dimensions):
    with Image.open(path) as image:
        if image.mode not in {"P", "L"} or image.size != tuple(dimensions):
            raise ValueError(f"Expected a full-canvas indexed label PNG: {path}")
        labels = np.array(image)
    if labels.max(initial=0) >= len(LAYER_ORDER):
        raise ValueError("Label PNG contains unknown categories")
    return labels


def reconstruct_rgb(rgb, labels):
    if rgb.dtype != np.uint8 or labels.shape != rgb.shape[:2]:
        raise ValueError("RGB/label shape or dtype mismatch")
    if labels.dtype != np.uint8 or labels.max(initial=0) >= len(LAYER_ORDER):
        raise ValueError("Invalid label IDs")
    result = np.zeros_like(rgb)
    for index in range(len(LAYER_ORDER)):
        selected = labels == index
        result[selected] = rgb[selected]
    return result


def _build_one(job):
    project_str, output_relative, route = job
    project = Path(project_str)
    frame = route["frame"]
    original_relative = f"frames/F{frame:06d}.png"
    original = inside(project, original_relative)
    with Image.open(original) as image:
        rgb = np.array(image.convert("RGB"))
    masks, metadata = split_visible_frame(rgb, {
        "group": route["group"], "source_frame": frame,
        "source_chapter": route["chapter_id"], "kind": "per-frame scene classifier only",
    })
    labels = labels_from_masks(masks, rgb.shape[:2])
    reconstructed = reconstruct_rgb(rgb, labels)
    if not np.array_equal(reconstructed, rgb):
        raise AssertionError(f"Pixel partition changed original RGB at frame {frame}")
    target_relative = f"{output_relative}/F{frame:06d}.png"
    reject_symlink_components(project / target_relative)
    target = inside(project, target_relative)
    indexed = Image.fromarray(labels, mode="P")
    indexed.putpalette(PALETTE)
    with tempfile.NamedTemporaryFile(prefix=f".{target.stem}.", suffix=".png", dir=target.parent, delete=False) as handle:
        temporary_target = Path(handle.name)
    try:
        indexed.save(temporary_target, compress_level=9, optimize=False)
        reject_symlink_components(target)
        temporary_target.replace(target)
    finally:
        temporary_target.unlink(missing_ok=True)
    counts = np.bincount(labels.ravel(), minlength=len(LAYER_ORDER))
    return {
        **route, "original_frame": original_relative, "label_map": target_relative,
        "source_png_sha256": sha256(original), "label_png_sha256": sha256(target),
        "pixel_counts": {name: int(counts[i]) for i, name in enumerate(LAYER_ORDER)},
        "status": metadata["status"], "flags": metadata["flags"],
        "unresolved_pixel_count": int(counts[LAYER_ORDER.index("unresolved_visible")]),
        "semantic_review": "not_approved", "clean_character_claimed": False,
        "roundtrip": {"exact": True, "mismatched_pixels": 0,
                      "scope": "visible RGB partition integrity only, NOT semantic correctness"},
    }


def build(project: Path, output_relative="frame_labels", manifest_relative="data/frame_layer_manifest.json", workers=2, resume=False):
    source_validation = validate_source(project)
    reject_symlink_components(project / output_relative)
    reject_symlink_components(project / manifest_relative)
    output = inside(project, output_relative)
    if output == project or output_relative.split("/")[0] in {"source", "frames", "cels", "reference_frames", "data"}:
        raise ValueError("Frame-label output must be a new dedicated project directory")
    if output.exists() and any(output.iterdir()) and not resume:
        raise ValueError("Refusing to overwrite existing label maps; use a new output directory")
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = inside(project, manifest_relative)
    if manifest_path.exists():
        raise ValueError("Refusing to overwrite an existing frame-layer manifest")
    bindings = build_bindings(project)
    routes = scene_routes(read_json(project / "data/panel_catalog.json"), bindings)
    rows = []
    base = {
        "schema": SCHEMA, "method_version": METHOD_VERSION,
        "segmentation_code_sha256": sha256(Path(__file__).with_name("magic_maid_layers.py")),
        "source": bindings["source"], "source_sha256": bindings["source_sha256"],
        "source_validation": source_validation,
        "time_base": bindings["time_base"], "video_duration_ticks": bindings["video_duration_ticks"],
        "frame_count": bindings["frame_count"], "dimensions": bindings["dimensions"],
        "labels": [{"index": i, "name": name} for i, name in enumerate(LAYER_ORDER)],
        "semantic_review": "not_approved", "production_ready": False,
        "original_alpha_recovered": False, "hidden_pixels_recovered": False,
        "character_redesign_performed": False,
        "routing_policy": "Scene ranges/reuse classify each original frame independently. No nearest-pose mask/character reuse and no attachment-2 pixels.",
        "integrity_is_not_semantic_approval": True,
    }
    partial = manifest_path.with_suffix(".partial.json")
    if resume:
        if not partial.is_file():
            raise ValueError("--resume requires a matching incomplete checkpoint manifest")
        checkpoint = read_json(partial)
        for key in ("schema", "segmentation_code_sha256", "source_sha256", "time_base", "dimensions", "frame_count"):
            if checkpoint.get(key) != base[key]:
                raise ValueError(f"Checkpoint {key} differs; use a new directory for a changed algorithm/source")
        rows = checkpoint.get("frames", [])
        if len(rows) > len(routes):
            raise ValueError("Checkpoint has more frames than the original timeline")
        for index, row in enumerate(rows):
            if any(row.get(key) != routes[index][key] for key in routes[index]):
                raise ValueError("Checkpoint scene route / timeline mismatch")
            if row["label_map"] != f"{output_relative}/F{index:06d}.png":
                raise ValueError("Checkpoint output path mismatch")
            if sha256(inside(project, row["original_frame"])) != row["source_png_sha256"]:
                raise ValueError("Checkpoint source frame changed")
            if sha256(inside(project, row["label_map"])) != row["label_png_sha256"]:
                raise ValueError("Checkpoint label map changed")
        print(f"resuming verified checkpoint at frame {len(rows)}", flush=True)
    jobs = [(str(project), output_relative, route) for route in routes[len(rows):]]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        try:
            for row in pool.map(_build_one, jobs, chunksize=1):
                rows.append(row)
                if len(rows) % 50 == 0 or len(rows) == len(routes):
                    print(f"frame labels: {len(rows)}/{len(routes)}", flush=True)
                    write_json(partial, {**base, "build_complete": False, "completed_frames": len(rows), "frames": rows},
                               overwrite=True, expected_schema=SCHEMA)
        except BaseException:
            pool.shutdown(wait=False, cancel_futures=True)
            raise
    flag_counts = Counter(flag for row in rows for flag in row["flags"])
    result = {**base, "build_complete": True, "completed_frames": len(rows),
              "summary": {"all_frame_pixel_partitions_exact": True,
                          "source_fallback_frames": 0,
                          "semantically_approved_frames": 0,
                          "frames_with_unresolved_label_pixels": sum(row["unresolved_pixel_count"] > 0 for row in rows),
                          "unproven_scene_routing_frames": sum(not row["group"] for row in rows),
                          "flag_frame_counts": dict(flag_counts)},
              "frames": rows}
    write_json(manifest_path, result)
    partial.unlink(missing_ok=True)
    return {"manifest": str(manifest_path), **result["summary"], "frame_count": len(rows)}


def export_frame(project: Path, manifest_path: Path, frame: int, destination: Path):
    destination = reject_symlink_components(destination)
    manifest = read_json(manifest_path)
    if manifest.get("schema") != SCHEMA or not manifest.get("build_complete"):
        raise ValueError("Expected a complete frame partition manifest")
    if not 0 <= frame < len(manifest["frames"]):
        raise ValueError("Frame is outside manifest")
    row = manifest["frames"][frame]
    if row["frame"] != frame:
        raise ValueError("Frame manifest is not in exact timeline order")
    original = inside(project, row["original_frame"])
    label_path = inside(project, row["label_map"])
    if sha256(label_path) != row["label_png_sha256"]:
        raise ValueError("Label map checksum changed")
    with Image.open(original) as image:
        rgb = np.array(image.convert("RGB"))
    container_difference = sha256(original) != row["source_png_sha256"]
    if container_difference:
        # Regenerated PNG compression/metadata is allowed only when a fresh
        # accurate source-video decode proves the native RGB is unchanged.
        movie = project / "source/original.mp4"
        if sha256(movie) != SOURCE_HASHES["original"]:
            raise ValueError("Immutable original video checksum changed")
        decoded = decode_frame_at_pts(movie, row["pts"], manifest["time_base"], manifest["dimensions"])
        if rgb.tobytes() != decoded:
            raise ValueError("Cached frame RGB differs from original source at its exact PTS")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Refusing to overwrite existing RGBA export")
    destination.mkdir(parents=True, exist_ok=True)
    labels = read_labels(label_path, manifest["dimensions"])
    layers = []
    for index, name in enumerate(LAYER_ORDER):
        mask = labels == index
        if mask.any():
            path = destination / f"{name}.png"
            Image.fromarray(rgba_from_mask(rgb, mask)).save(path, compress_level=6)
            layers.append({"name": name, "file": path.name, "pixel_count": int(mask.sum()), "sha256": sha256(path)})
    provenance = {"source_frame": frame, "source_pts": row["pts"], "time_base": manifest["time_base"],
                  "status": row["status"], "semantic_review": "not_approved", "flags": row["flags"],
                  "source_png_sha256": row["source_png_sha256"], "layers": layers,
                  "source_png_container_differs_but_rgb_verified": container_difference,
                  "hidden_pixels_recovered": False, "original_alpha_recovered": False}
    write_json(destination / "PROVENANCE.json", provenance)
    return provenance


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT_DEFAULT)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build")
    build_parser.add_argument("--output", default="frame_labels")
    build_parser.add_argument("--manifest", default="data/frame_layer_manifest.json")
    build_parser.add_argument("--workers", type=int, default=2)
    build_parser.add_argument("--resume", action="store_true", help="Resume an unchanged, checksum-verified partial build")
    export_parser = commands.add_parser("export-frame")
    export_parser.add_argument("frame", type=int)
    export_parser.add_argument("--manifest", type=Path)
    export_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    project = args.project.resolve()
    if args.command == "build":
        if args.workers <= 0:
            parser.error("--workers must be positive")
        result = build(project, args.output, args.manifest, args.workers, args.resume)
    else:
        result = export_frame(project, args.manifest or project / "data/frame_layer_manifest.json",
                              args.frame, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
