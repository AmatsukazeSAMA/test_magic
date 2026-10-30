#!/usr/bin/env python3
"""Build a portable, local-only subtitle/FX/reuse review page.

No network, fetch(), source extraction, alpha estimation or source mutation.
The HTML embeds bounded metadata, not PNG/RGBA payloads. PNGs remain relative
files so the page works under file:// after the project folder is copied.

Usage:
  python scripts/magic_maid_overlay_viewer.py --project magic_maid_20261029
  python -m unittest discover -s tests -p 'test_magic_maid_overlay_viewer.py'

The page is a review tool, not a semantic/clean-alpha certification. Browser QA
must use the official preview/CUA workflow; this script does not launch browsers.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import tempfile
from typing import Any

SCHEMA = "magic-maid.subtitle-effect-overlays/1"
DEFAULT_OUTPUT = "字幕特效与复用工作台.html"
GENERATOR_MARKER = "<!-- generated-by: scripts/magic_maid_overlay_viewer.py; magic-maid.offline-overlay-viewer/1 -->"
OWNED_HTML_PREFIX = ("<!doctype html>\n" + GENERATOR_MARKER + "\n").encode("utf-8")
CATEGORIES = ("subtitles", "effects")
KIND_NAMES = {
    "body_pose": "身体动作", "half_body": "半身动作", "head_detail": "头部细节",
    "hand_detail": "手部细节", "mouth_detail": "口型细节",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def integer(value: Any, name: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{name}: expected integer >= {minimum}")
    return value


def no_symlinks(path: Path) -> None:
    for part in (path, *path.parents):
        require(not part.is_symlink(), f"Symlink paths are not allowed: {part}")


def project_root(path: Path | str) -> Path:
    root = Path(os.path.abspath(path))
    no_symlinks(root)
    require(root.is_dir(), f"Project directory does not exist: {root}")
    return root


def safe_relative(root: Path, value: Any, suffix: str | None = None) -> Path:
    require(isinstance(value, str) and bool(value), "Empty or non-string relative path")
    require(not any(ord(c) < 32 for c in value), "Control characters in relative path")
    require(not any(c in value for c in "\\:%?#"), f"Unsafe relative path: {value}")
    parts = value.split("/")
    require(not value.startswith("/") and all(x not in ("", ".", "..") for x in parts),
            f"Path must stay inside project: {value}")
    path = root.joinpath(*parts)
    no_symlinks(path)
    require(path.resolve().is_relative_to(root.resolve()), f"Path escaped project: {value}")
    if suffix:
        require(path.suffix.lower() == suffix, f"Expected {suffix} path: {value}")
    return path


def output_path(root: Path, relative: str) -> Path:
    path = safe_relative(root, relative, ".html")
    require(len(PurePosixPath(relative).parts) == 1,
            "HTML output must be directly in project root, never in protected source/data folders")
    require(not path.exists() or path.is_file(), "HTML output is not a regular file")
    if path.exists():
        require(path.stat().st_nlink == 1, "Refusing a hard-linked HTML output")
        with path.open("rb") as handle:
            prefix = handle.read(len(OWNED_HTML_PREFIX))
        require(prefix == OWNED_HTML_PREFIX,
                "Refusing to overwrite HTML not owned by this viewer builder (missing dedicated generator marker)")
    return path


def read_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-finite JSON value: {value}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, parse_constant=reject_constant)


def png_dimensions(path: Path, require_rgba: bool = False) -> tuple[int, int] | None:
    if not path.is_file():
        return None
    with path.open("rb") as handle:
        head = handle.read(26)
    if len(head) != 26 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"Not a PNG: {path}")
    if require_rgba:
        require(head[24] == 8 and head[25] == 6, f"Overlay PNG must be 8-bit RGBA: {path}")
    return struct.unpack(">II", head[16:24])


def bounded_metadata(value: Any, depth: int = 0) -> Any:
    """Do not accidentally inline extractor arrays or embedded image payloads."""
    if depth > 5:
        return "[更深层元数据省略；请查看原 JSON]"
    if isinstance(value, dict):
        result = {str(k)[:120]: bounded_metadata(v, depth + 1)
                  for k, v in list(value.items())[:60]}
        if len(value) > 60:
            result["_truncated"] = f"另有 {len(value) - 60} 项；查看原 JSON"
        return result
    if isinstance(value, list):
        result = [bounded_metadata(v, depth + 1) for v in value[:32]]
        if len(value) > 32:
            result.append(f"另有 {len(value) - 32} 项；查看原 JSON")
        return result
    if isinstance(value, str):
        if value.startswith("data:"):
            return "[内嵌数据未复制到工作台]"
        return value[:2400] + ("… [查看原 JSON]" if len(value) > 2400 else "")
    if value is None or type(value) in (bool, int, float):
        return value
    return str(value)[:2400]


def source_records(drawing: dict) -> list[tuple[int, str]]:
    """Only explicit frame/image correspondence, never temporal proximity."""
    records = []
    samples = drawing.get("source_samples")
    if isinstance(samples, list) and samples:
        for sample in samples:
            if isinstance(sample, dict) and type(sample.get("frame")) is int and isinstance(sample.get("image"), str):
                records.append((sample["frame"], sample["image"]))
        return records
    frames, images = drawing.get("source_frames", []), drawing.get("source_images", [])
    if isinstance(images, list):
        if images and all(isinstance(x, str) for x in images) and isinstance(frames, list) and len(frames) == len(images):
            records.extend((f, p) for f, p in zip(frames, images) if type(f) is int)
        else:
            for item in images:
                if isinstance(item, dict):
                    frame = item.get("source_frame", item.get("frame"))
                    path = item.get("source_image", item.get("path"))
                    if type(frame) is int and isinstance(path, str):
                        records.append((frame, path))
    return records


def optional_work_counts(data: dict, total: int, context: str, prefix: str = "") -> dict:
    """A missing old-format breakdown is unknown, never inferred as all new art."""
    keys = ("linework_count", "color_only_count")
    present = [prefix + key in data for key in keys]
    if not any(present):
        return dict.fromkeys(keys)
    require(all(present), f"{context}: linework/color-only breakdown must supply both counts")
    result = {key: integer(data[prefix + key], f"{context} {prefix + key}") for key in keys}
    require(sum(result.values()) == total, f"{context}: linework/color-only counts disagree with work budget")
    return result


def validate_drawing_source(root: Path, drawing: dict, frame: int, relative: str, pts: int) -> Path:
    """Allow audited supplement images only through an explicit exact-PTS sample.

    The directory name does not confirm reuse or drawing identity. This only
    authorizes displaying the recorded *same original frame*, without a warp,
    nearest-frame lookup, or reference-image substitution.
    """
    path = safe_relative(root, relative, ".png")
    parts = relative.split("/")
    category = parts[0]
    if category == "drawing_candidates":
        samples = drawing.get("source_samples", [])
        require(isinstance(samples, list) and any(
            isinstance(sample, dict) and type(sample.get("frame")) is int
            and sample["frame"] == frame and type(sample.get("pts")) is int
            and sample["pts"] == pts and sample.get("image") == relative
            for sample in samples),
            "drawing_candidates requires explicit exact-frame/PTS source_samples; no inferred fallback")
    else:
        require(category in ("cels", "drawing_audit", "frames"), f"Non-production drawing image: {relative}")
    if category == "frames":
        require(relative == f"frames/F{frame:06d}.png", "Wrong frame cache record")
    else:
        require(len(parts) == 3 and parts[-1] == "source.png",
                f"Production drawing source must be <directory>/<id>/source.png, never reference.png: {relative}")
    return path


def prepare_payload(root: Path, overlay: dict, reuse: dict, sections: dict,
                    catalog: list | dict | None = None, verify_assets: bool = False) -> dict:
    root = project_root(root)
    require(isinstance(overlay, dict) and overlay.get("schema") == SCHEMA, "Unsupported overlay schema")
    require(overlay.get("dimensions") == [1920, 1080], "Expected original 1920x1080 full canvas")
    require(overlay.get("time_base") == "1/16000", "Expected original time_base 1/16000")
    require(overlay.get("alpha_mode") == "straight", "Only explicitly declared straight alpha is supported")
    count = integer(overlay.get("frame_count"), "frame_count", 1)
    duration = integer(overlay.get("video_duration_ticks"), "video_duration_ticks", 1)
    rows = overlay.get("frames")
    require(isinstance(rows, list) and len(rows) == count, "Overlay frame_count mismatch")
    assets = overlay.get("assets")
    require(isinstance(assets, dict), "Missing overlay assets")
    warnings, normalized_assets = [], {}
    for category in CATEGORIES:
        entries = assets.get(category)
        require(isinstance(entries, dict), f"Missing {category} assets")
        normalized_assets[category] = {}
        for asset_id, asset in entries.items():
            require(isinstance(asset_id, str) and bool(HEX64.fullmatch(asset_id)), "Invalid RGBA asset ID")
            require(isinstance(asset, dict) and asset.get("rgba_sha256") == asset_id, "RGBA identity mismatch")
            require(isinstance(asset.get("png_sha256"), str) and bool(HEX64.fullmatch(asset["png_sha256"])), "Invalid PNG digest")
            path = safe_relative(root, asset.get("path"), ".png")
            require(path.name == asset_id + ".png", "Asset filename must be content-addressed by RGBA SHA256")
            byte_count = integer(asset.get("bytes"), "asset bytes", 1)
            nonzero = integer(asset.get("nonzero_alpha_pixels"), "nonzero_alpha_pixels")
            partial = integer(asset.get("partial_alpha_pixels"), "partial_alpha_pixels")
            opaque = integer(asset.get("opaque_pixels"), "opaque_pixels")
            require(nonzero == partial + opaque and nonzero <= 1920 * 1080, "Inconsistent alpha counts")
            bbox = asset.get("bbox")
            if nonzero:
                require(isinstance(bbox, list) and len(bbox) == 4 and all(type(x) is int for x in bbox)
                        and 0 <= bbox[0] < bbox[2] <= 1920 and 0 <= bbox[1] < bbox[3] <= 1080, "Invalid alpha bbox")
            else:
                require(bbox is None, "Empty overlay requires null bbox")
            dimensions = png_dimensions(path, require_rgba=True)
            if dimensions is None:
                warnings.append(f"缺少叠加 PNG：{asset['path']}")
            else:
                require(dimensions == (1920, 1080), f"Overlay canvas mismatch: {asset['path']}")
                require(path.stat().st_size == byte_count, f"Overlay PNG byte size mismatch: {asset['path']}")
                if verify_assets:
                    require(hashlib.sha256(path.read_bytes()).hexdigest() == asset["png_sha256"], f"Overlay PNG digest mismatch: {asset['path']}")
            normalized_assets[category][asset_id] = {k: asset[k] for k in
                ("path", "rgba_sha256", "png_sha256", "bytes", "nonzero_alpha_pixels", "partial_alpha_pixels", "opaque_pixels", "bbox")}
            normalized_assets[category][asset_id]["present_at_build"] = dimensions is not None
    frames = []
    expected_pts = 0
    for index, row in enumerate(rows):
        require(isinstance(row, dict) and row.get("frame") == index and type(row.get("frame")) is int,
                f"Frames must be complete and ordered: expected {index}")
        pts = integer(row.get("pts"), "frame PTS")
        ticks = integer(row.get("duration_ticks"), "frame duration_ticks", 1)
        require(pts == expected_pts, f"Non-contiguous PTS at frame {index}")
        expected_pts += ticks
        original = row.get("original_frame")
        require(original == f"frames/F{index:06d}.png", f"Original path is not this exact frame: {index}")
        safe_relative(root, original, ".png")
        for key in ("source_png_sha256", "source_rgb_sha256"):
            value = row.get(key)
            require(isinstance(value, str) and bool(HEX64.fullmatch(value)), f"Missing source digest {key} at {index}")
        chapter = row.get("chapter_id")
        require(isinstance(chapter, str) and bool(chapter), f"Missing chapter_id at {index}")
        normalized = {"frame": index, "pts": pts, "duration_ticks": ticks, "chapter_id": chapter,
                      "group": str(row.get("group") or ""), "original_frame": original,
                      "source_png_sha256": row["source_png_sha256"], "source_rgb_sha256": row["source_rgb_sha256"],
                      "sources": [{"path": original, "frame": index, "basis": "exact_original_frame_cache"}], "overlays": {}}
        require(isinstance(row.get("overlays"), dict), f"Missing frame overlays: {index}")
        for category in CATEGORIES:
            item = row["overlays"].get(category)
            require(isinstance(item, dict), f"Missing {category} reference: {index}")
            asset_id = item.get("asset_id")
            require(asset_id is None or asset_id in normalized_assets[category], f"Unknown {category} asset: {index}")
            require(isinstance(item.get("status"), str) and bool(item["status"]), f"Missing overlay status: {index}")
            require(type(item.get("requires_review")) is bool, f"Missing explicit requires_review: {index}")
            normalized["overlays"][category] = {"asset_id": asset_id, "status": item["status"],
                "requires_review": item["requires_review"], "metadata": bounded_metadata(item.get("metadata", {}))}
        frames.append(normalized)
    require(expected_pts == duration, "Final frame end differs from video_duration_ticks")
    require(isinstance(reuse, dict) and isinstance(reuse.get("canonical_drawings"), list), "Invalid reuse manifest")
    drawing_ids, drawings, exact_fallbacks = set(), [], {}
    for drawing in reuse["canonical_drawings"]:
        require(isinstance(drawing, dict), "Invalid canonical drawing")
        did = drawing.get("id")
        require(isinstance(did, str) and bool(did) and did not in drawing_ids, "Duplicate/missing drawing ID")
        drawing_ids.add(did)
        require(type(drawing.get("count_in_conservative_plan")) is bool, f"Missing drawing count flag: {did}")
        require(not drawing.get("alias_of") or not drawing["count_in_conservative_plan"], f"Alias cannot be counted: {did}")
        if "line_drawing_required" in drawing:
            require(type(drawing["line_drawing_required"]) is bool, f"Invalid line-drawing scope flag: {did}")
        if drawing.get("work_operation") == "crop_reuse_alias":
            require(bool(drawing.get("alias_of")) and not drawing["count_in_conservative_plan"]
                    and drawing.get("line_drawing_required") is False,
                    f"Confirmed crop reuse must be a non-counted, no-new-linework alias: {did}")
        records = []
        for frame, relative in source_records(drawing):
            integer(frame, "drawing source frame")
            require(frame < count, f"Drawing source frame outside timeline: {did}")
            validate_drawing_source(root, drawing, frame, relative, frames[frame]["pts"])
            records.append({"frame": frame, "path": relative})
            if not relative.startswith("frames/"):
                exact_fallbacks.setdefault(frame, []).append({"frame": frame, "path": relative,
                                                            "basis": f"reuse_manifest:{did}:explicit_frame_image_pair"})
        occurrences = drawing.get("occurrences", [])
        require(isinstance(occurrences, list), f"Invalid occurrences: {did}")
        normalized_occurrences = []
        for occurrence in occurrences:
            require(isinstance(occurrence, dict), "Invalid occurrence")
            s = integer(occurrence.get("start_frame"), "occurrence start")
            e = integer(occurrence.get("end_frame_exclusive"), "occurrence end", 1)
            require(s < e <= count, "Occurrence frame interval outside original")
            require(occurrence.get("start_pts") == frames[s]["pts"] and
                    occurrence.get("end_pts_exclusive") == (frames[e]["pts"] if e < count else duration), "Occurrence PTS mismatch")
            normalized_occurrences.append(bounded_metadata(occurrence))
        drawings.append({"id": did, "title": str(drawing.get("title", "")), "kind": str(drawing.get("kind", "unknown")),
                         "planning_status": str(drawing.get("planning_status", "")),
                         "count_in_conservative_plan": drawing["count_in_conservative_plan"],
                         "alias_of": drawing.get("alias_of"), "sources": records,
                         "occurrences": normalized_occurrences, "notes": bounded_metadata(drawing.get("notes", [])),
                         **{key: bounded_metadata(drawing.get(key)) for key in
                            ("work_scope", "partial_reuse_scope", "redraw_regions", "color_adjustment_regions",
                             "work_operation", "line_drawing_required", "crop_review_pair_id", "crop_review_evidence")}})
    for drawing in drawings:
        require(not drawing["alias_of"] or drawing["alias_of"] in drawing_ids, f"Alias target missing: {drawing['id']}")
    catalog_rows = catalog if isinstance(catalog, list) else (catalog or {}).get("panels", [])
    require(isinstance(catalog_rows, list), "Invalid optional panel catalog")
    for panel in catalog_rows:
        if not isinstance(panel, dict):
            continue
        frame, relative = panel.get("source_frame"), panel.get("source_image")
        if type(frame) is not int or not (0 <= frame < count) or not isinstance(relative, str):
            continue
        safe_relative(root, relative, ".png")
        require(relative.startswith("cels/") or relative.startswith("drawing_audit/"), "Catalog source is not a production cel/audit image")
        validate_drawing_source(root, {}, frame, relative, frames[frame]["pts"])
        exact_fallbacks.setdefault(frame, []).append({"frame": frame, "path": relative,
                                                    "basis": f"panel_catalog:{panel.get('id', '')}:exact_source_frame"})
    for frame, fallbacks in exact_fallbacks.items():
        seen = {frames[frame]["original_frame"]}
        for record in fallbacks:
            if record["path"] not in seen:
                frames[frame]["sources"].append(record)
                seen.add(record["path"])
    reuse_rows = reuse.get("frames")
    require(isinstance(reuse_rows, list) and len(reuse_rows) == count, "Reuse frames must cover whole original")
    for index, row in enumerate(reuse_rows):
        require(isinstance(row, dict) and type(row.get("frame")) is int and row["frame"] == index and
                row.get("pts") == frames[index]["pts"] and row.get("chapter_id") == frames[index]["chapter_id"],
                f"Reuse frame order/PTS/chapter mismatch: {index}")
        data = {}
        for key in ("canonical_ids", "candidate_ids", "candidate_family_ids", "occurrence_ids"):
            values = row.get(key, [])
            require(isinstance(values, list) and all(isinstance(x, str) for x in values), f"Invalid reuse {key}")
            if key == "canonical_ids":
                require(all(x in drawing_ids for x in values), f"Unknown confirmed canonical drawing at {index}")
            data[key] = values
        data["status"] = str(row.get("status", ""))
        data["evidence"] = bounded_metadata(row.get("evidence", []))
        frames[index]["reuse"] = data
    require(isinstance(sections, dict) and isinstance(sections.get("sections"), list), "Invalid work_sections")
    mapping = sections.get("frame_sections")
    require(isinstance(mapping, list) and len(mapping) == count, "S-section mapping must cover every frame")
    normalized_sections, occupied, section_ids = [], {}, set()
    conditional_pairs = reuse.get("conditional_reuse_pairs", [])
    require(isinstance(conditional_pairs, list), "Invalid conditional reuse pairs")
    conditional_ids = set()
    for pair in conditional_pairs:
        require(isinstance(pair, dict) and isinstance(pair.get("id"), str) and pair["id"] not in conditional_ids, "Invalid/duplicate conditional pair")
        require(pair.get("confirmed") is False, "Conditional pairs must remain explicitly unconfirmed")
        require(pair.get("from_id") in drawing_ids and pair.get("to_id") in drawing_ids, "Conditional pair drawing missing")
        conditional_ids.add(pair["id"])
    reviewed_pairs = reuse.get("reviewed_crop_pairs", [])
    require(isinstance(reviewed_pairs, list), "Invalid reviewed crop pairs")
    reviewed_ids = set()
    for pair in reviewed_pairs:
        require(isinstance(pair, dict), "Invalid reviewed crop pair")
        pair_id = pair.get("id", pair.get("pair_id"))
        require(isinstance(pair_id, str) and bool(pair_id) and pair_id not in reviewed_ids, "Invalid/duplicate reviewed crop pair ID")
        require(pair_id not in conditional_ids, "A reviewed crop pair cannot also remain a conditional candidate")
        require(type(pair.get("confirmed")) is bool, "Reviewed crop pair must explicitly state confirmed")
        if pair["confirmed"]:
            require(pair.get("classification") == "confirmed_crop_reuse", "Only pure crop-reuse pairs may be confirmed")
        reviewed_ids.add(pair_id)
    for drawing in drawings:
        pair_id = drawing["crop_review_pair_id"]
        require(pair_id is None or pair_id in reviewed_ids, f"Unknown drawing crop review pair: {drawing['id']}")
    section_id_keys = ("new_drawing_ids", "reused_drawing_ids", "observed_reused_drawing_ids", "observed_reused_exposure_ids",
                       "conditional_reuse_pair_ids", "reviewed_crop_pair_ids", "candidate_drawing_ids")
    for section in sections["sections"]:
        sid = section.get("id")
        require(isinstance(sid, str) and re.fullmatch(r"[A-Za-z0-9_-]+", sid) and sid not in section_ids, "Duplicate/missing/unsafe S-section ID")
        section_ids.add(sid)
        ranges = section.get("ranges")
        require(isinstance(ranges, list) and ranges, f"Missing ranges: {sid}")
        local_frame, local_pts, previous_end, clean_ranges = 0, 0, -1, []
        for span in ranges:
            s = integer(span.get("start_frame"), "section start")
            e = integer(span.get("end_frame_exclusive"), "section end", 1)
            require(previous_end <= s < e <= count, f"Unordered/invalid section ranges: {sid}")
            sp, ep = frames[s]["pts"], frames[e]["pts"] if e < count else duration
            require(span.get("start_pts") == sp and span.get("end_pts_exclusive") == ep, f"S-range PTS mismatch: {sid}")
            require(span.get("local_start_frame") == local_frame and span.get("local_start_pts") == local_pts,
                    f"S-local timeline must concatenate exact ranges: {sid}")
            clean_ranges.append({k: span[k] for k in ("start_frame", "end_frame_exclusive", "start_pts", "end_pts_exclusive", "local_start_frame", "local_start_pts")})
            for index in range(s, e):
                require(index not in occupied and mapping[index] == sid, f"Overlapping/mismatched S-section: {index}")
                occupied[index] = sid
                frames[index]["section_id"] = sid
                frames[index]["local_frame"] = local_frame + index - s
                frames[index]["local_pts"] = local_pts + frames[index]["pts"] - sp
            local_frame += e - s
            local_pts += ep - sp
            previous_end = e
        normalized = {"id": sid, "title": str(section.get("title", "")), "ranges": clean_ranges,
                      "duration_ticks": local_pts, "frame_count": local_frame,
                      "new_kind_counts": bounded_metadata(section.get("new_kind_counts", {}))}
        for key in section_id_keys:
            values = section.get(key, [])
            require(isinstance(values, list) and all(isinstance(x, str) for x in values), f"Invalid {sid} {key}")
            require(len(values) == len(set(values)), f"Duplicate {sid} {key}")
            if key in ("new_drawing_ids", "reused_drawing_ids", "observed_reused_drawing_ids"):
                require(all(x in drawing_ids for x in values), f"Unknown drawing in {sid} {key}")
            if key == "conditional_reuse_pair_ids":
                require(all(x in conditional_ids for x in values), f"Unknown conditional pair in {sid}")
            if key == "reviewed_crop_pair_ids":
                require(all(x in reviewed_ids for x in values), f"Unknown reviewed crop pair in {sid}")
            normalized[key] = values
        normalized["package_files"] = []
        for name, label in (("README.md", "分包说明"), ("timeline.csv", "逐帧 CSV"), ("drawings.json", "绘制 JSON"), ("assets.json", "透明层 JSON")):
            relative = f"work_sections/{sid}/{name}"
            path = safe_relative(root, relative)
            normalized["package_files"].append({"path": relative, "label": label, "present_at_build": path.is_file()})
        for key, ids_key in (("new_drawing_count", "new_drawing_ids"), ("reused_drawing_count", "reused_drawing_ids"),
                             ("observed_reused_drawing_count", "observed_reused_drawing_ids"),
                             ("observed_reused_exposure_count", "observed_reused_exposure_ids")):
            value = section.get(key, len(normalized[ids_key]))
            require(type(value) is int and value == len(normalized[ids_key]), f"S-section count mismatch: {sid}/{key}")
            normalized[key] = value
        normalized.update(optional_work_counts(section, normalized["new_drawing_count"], sid, prefix="new_"))
        if "new_linework_ids" in section or "new_color_only_ids" in section:
            work_ids = []
            for key, count_key in (("new_linework_ids", "linework_count"), ("new_color_only_ids", "color_only_count")):
                ids = section.get(key)
                require(isinstance(ids, list) and all(isinstance(x, str) for x in ids)
                        and len(ids) == normalized[count_key], f"Invalid {sid} {key}/count")
                work_ids.extend(ids)
            require(len(work_ids) == len(set(work_ids)) and set(work_ids) == set(normalized["new_drawing_ids"]),
                    f"{sid}: linework/color-only IDs must partition the budget")
        normalized_sections.append(normalized)
    require(len(occupied) == count, "Work sections leave original frames uncovered")
    planned = [d for d in drawings if d["count_in_conservative_plan"] and not d["alias_of"]]
    new_ids = [did for section in normalized_sections for did in section["new_drawing_ids"]]
    require(len(new_ids) == len(set(new_ids)) and set(new_ids) == {d["id"] for d in planned}, "Each planned non-alias drawing must belong to exactly one new-drawing S package")
    summary = bounded_metadata(reuse.get("summary", {}))
    declared_count = reuse.get("summary", {}).get("planning_count")
    if declared_count is not None:
        require(declared_count == len(planned), "Conservative planning count disagrees with non-alias drawing flags")
    confirmed_crop_count = integer(reuse.get("summary", {}).get("confirmed_crop_reuse_pairs", 0), "confirmed crop reuse count")
    confirmed_crop_ids = {p.get("id", p.get("pair_id")) for p in reviewed_pairs if p["confirmed"]}
    require(confirmed_crop_count == len(confirmed_crop_ids),
            "Confirmed crop reuse count disagrees with unique reviewed pairs (not alias-record count)")
    require(all(d["crop_review_pair_id"] in confirmed_crop_ids for d in drawings if d["work_operation"] == "crop_reuse_alias"),
            "A confirmed crop alias must link to a confirmed reviewed pair")
    return {"viewer_schema": "magic-maid.offline-overlay-viewer/1", "synthetic_fixture": overlay.get("synthetic_fixture") is True,
            "dimensions": [1920, 1080], "time_base": "1/16000", "frame_count": count,
            "video_duration_ticks": duration, "alpha_mode": "straight", "assets": normalized_assets, "frames": frames,
            "drawings": drawings, "sections": normalized_sections, "planning_count": len(planned),
            **optional_work_counts(reuse.get("summary", {}), len(planned), "reuse summary"),
            "kind_counts": dict(Counter(d["kind"] for d in planned)), "kind_names": KIND_NAMES,
            "reuse_summary": summary, "conditional_reuse_pairs": [bounded_metadata(p) for p in conditional_pairs],
            "reviewed_crop_pairs": [bounded_metadata(p) for p in reviewed_pairs],
            "confirmed_crop_reuse_count": confirmed_crop_count,
            "crop_reuse_report": bounded_metadata(reuse.get("crop_reuse_report")),
            "optional_brooch_portrait_count": integer(sections.get("optional_brooch_portrait_count", 0), "optional portrait count"),
            "warnings": warnings[:80], "warning_count": len(warnings)}


def safe_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def render_html(payload: dict) -> str:
    return HTML.replace("__GENERATOR_MARKER__", GENERATOR_MARKER, 1).replace("__MANIFEST_JSON__", safe_json(payload))


def build(project: Path | str, output: str = DEFAULT_OUTPUT, *, overlay_name: str = "data/overlay_manifest.json",
          reuse_name: str = "data/reuse_manifest.json", sections_name: str = "data/work_sections.json",
          catalog_name: str = "data/panel_catalog.json", verify_assets: bool = False) -> dict:
    root = project_root(project)
    target = output_path(root, output)
    overlay = read_json(safe_relative(root, overlay_name, ".json"))
    reuse = read_json(safe_relative(root, reuse_name, ".json"))
    sections = read_json(safe_relative(root, sections_name, ".json"))
    catalog_path = safe_relative(root, catalog_name, ".json")
    catalog = read_json(catalog_path) if catalog_path.is_file() else None
    payload = prepare_payload(root, overlay, reuse, sections, catalog, verify_assets)
    result = render_html(payload)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", prefix=".overlay-viewer-", suffix=".html", dir=root, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(result)
        output_path(root, output)
        os.replace(temporary, target)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return {"output": str(target), "frame_count": payload["frame_count"], "section_count": len(payload["sections"]),
            "planning_count": payload["planning_count"], "asset_count": sum(len(a) for a in payload["assets"].values()),
            "missing_asset_count": payload["warning_count"], "browser_qa": "not_run_by_builder",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


HTML = r'''<!doctype html>
__GENERATOR_MARKER__
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><title>魔法女仆 · 字幕、特效与复用工作台</title>
<style>
:root{--ink:#322b32;--muted:#71656d;--paper:#fbf7f5;--card:#fff;--line:#e5d8db;--pink:#a34c71;--soft:#f6e9ee;--warn:#8d4f0a;--bad:#9a2339;--good:#23674c;--radius:15px;font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:var(--ink);background:var(--paper);line-height:1.55}*{box-sizing:border-box}body{margin:0}a{color:#853355;text-underline-offset:3px}button,input,select{font:inherit}button,select,input[type=number],input[type=search]{border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);min-height:40px;padding:7px 11px}button{cursor:pointer}button:hover{background:var(--soft);border-color:#c08b9f}button:disabled{opacity:.45;cursor:default}button.primary{background:var(--pink);color:#fff;border-color:var(--pink)}:focus-visible{outline:3px solid #a56c91;outline-offset:3px}input[type=checkbox]{accent-color:var(--pink);width:17px;height:17px}input[type=range]{accent-color:var(--pink);width:100%;min-height:36px}h1,h2,h3,p{margin-top:0}h1{font-size:clamp(23px,3vw,36px);line-height:1.25;margin-bottom:10px}h2{font-size:21px;margin-bottom:14px}h3{font-size:16px;margin-bottom:9px}main{max-width:1512px;margin:auto;padding:30px 26px 60px}.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--pink);font-weight:750}.intro{max-width:1000px;color:var(--muted);font-size:14px}.notice,.error,.demo{padding:12px 16px;border:1px solid var(--line);border-left:4px solid var(--pink);border-radius:9px;background:#fff;margin:14px 0;font-size:13px}.order-warning{background:#fff4df;border-left-color:#be841d;color:var(--warn)}.error{border-color:#df9eaa;border-left-color:var(--bad);color:var(--bad);background:#fff5f6}.demo{background:#fff3d3;border-color:#dba74b;color:#6d4808;font-weight:700}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0}.stat,.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px}.stat strong{display:block;font-size:27px;line-height:1.2}.stat span{font-size:12px;color:var(--muted)}.stat small{display:block;margin-top:6px;font-size:12px}.muted{color:var(--muted)}.small{font-size:12px}.mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;word-break:break-word}.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.toolbar label{display:flex;gap:7px;align-items:center;font-size:13px}.toolbar select{max-width:290px}.navrow{display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center;margin:14px 0 8px}.frame-form{display:flex;gap:6px;align-items:center}.frame-form input{width:105px}.timing{display:flex;flex-wrap:wrap;gap:7px 22px;font-size:13px;margin:12px 0}.timing strong{font-weight:650}.stage-grid{display:grid;grid-template-columns:1fr;gap:16px}.stage-grid.split{grid-template-columns:1fr 1fr}.stage-panel[hidden], [hidden]{display:none!important}.stage-head{display:flex;justify-content:space-between;gap:12px;font-size:12px;color:var(--muted);padding:10px 0 6px}.stage{position:relative;aspect-ratio:16/9;isolation:isolate;overflow:hidden;border:1px solid #bcb1b7;border-radius:10px;background:#eee}.stage.checker{background-color:#eee;background-image:linear-gradient(45deg,#d5d0d3 25%,transparent 25%),linear-gradient(-45deg,#d5d0d3 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d5d0d3 75%),linear-gradient(-45deg,transparent 75%,#d5d0d3 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0}.stage.light{background:#fff}.stage.dark{background:#202027}.plane{position:absolute;inset:0}.plane img{display:block;width:100%;height:100%;object-fit:contain}.plane.effects{z-index:1}.plane.subtitles{z-index:2}.stage-placeholder{position:absolute;inset:0;display:grid;place-items:center;z-index:0;color:#635c64;font-size:13px;text-align:center;padding:30px;pointer-events:none}.stage.dark .stage-placeholder{color:#bbb}.legend{display:flex;gap:10px;flex-wrap:wrap;margin:11px 0;font-size:12px}.pill{display:inline-block;padding:3px 8px;border-radius:5px;background:var(--soft);color:#784b60;font-size:11px}.pill.warn{background:#fff0d9;color:var(--warn)}.pill.good{background:#e5f3eb;color:var(--good)}.asset-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}.asset-card{border:1px solid var(--line);border-radius:10px;padding:14px;font-size:12px;overflow-wrap:anywhere}.asset-card p{margin-bottom:7px}.status-line{min-height:22px}.status-line[data-state=error]{color:var(--bad)}.status-line[data-state=loaded]{color:var(--good)}details{margin-top:9px}summary{cursor:pointer;color:#784b60}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#faf6f8;border-radius:7px;padding:10px;font-size:11px;max-height:290px;overflow:auto}.reuse-current{border-top:1px solid var(--line);margin-top:16px;padding-top:14px}.chips{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0}.chip{font-size:11px;min-height:29px;padding:4px 8px}.sections,.drawings{margin-top:24px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:12px;min-width:880px}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}th{background:#fbf5f7;font-weight:650}td .jump{padding:2px 6px;min-height:28px;font-weight:700}caption{text-align:left;color:var(--muted);padding-bottom:10px}.drawing-filters{margin-bottom:14px}.drawing-filters input{min-width:250px;flex:1}.drawing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.drawing-card{border:1px solid var(--line);border-radius:11px;padding:15px;min-width:0}.drawing-card.current{outline:2px solid #be7899;outline-offset:-2px;background:#fffafd}.drawing-card h3{margin-bottom:6px}.drawing-card .links{display:flex;flex-wrap:wrap;gap:4px 12px}.drawing-card p{font-size:12px;margin-bottom:8px;overflow-wrap:anywhere}.drawing-card details{font-size:12px}.drawing-card ul{padding-left:18px}.drawing-card li{margin-bottom:7px}.drawing-card img{width:100%;aspect-ratio:16/9;object-fit:contain;border-radius:6px;border:1px solid var(--line);background:#f5eff2;margin:6px 0}.footer{font-size:12px;color:var(--muted);margin-top:24px}.sr-only{position:absolute;width:1px;height:1px;margin:-1px;clip:rect(0,0,0,0);overflow:hidden;white-space:nowrap}.empty{padding:22px;color:var(--muted);border:1px dashed var(--line);border-radius:10px}.topnav{display:flex;gap:18px;font-size:12px;margin:16px 0}.nowrap{white-space:nowrap}
@media(max-width:900px){main{padding:20px 15px 40px}.stats{grid-template-columns:1fr 1fr}.drawing-grid{grid-template-columns:1fr 1fr}.stage-grid.split{grid-template-columns:1fr}.navrow{grid-template-columns:1fr;gap:8px}.asset-cards{grid-template-columns:1fr}.toolbar select{max-width:220px}}
@media(max-width:560px){.drawing-grid{grid-template-columns:1fr}.card{padding:14px}.stats{gap:8px}.stat{padding:14px}.stat strong{font-size:23px}.toolbar{gap:8px}.toolbar label{flex-wrap:wrap}.toolbar select{max-width:100%}.drawing-filters input{min-width:0;width:100%}.timing{gap:6px 12px}.frame-form{flex-wrap:wrap}.topnav{gap:12px}}
</style>
</head>
<body>
<main>
<header><p class="eyebrow">MAGIC MAID / LOCAL REVIEW WORKBENCH</p><h1>字幕、特效与复用工作台</h1><p class="intro">附件 1 是唯一制作像素来源；附件 2 仅作为复用参考。逐帧检查独立透明叠加层与绘制计划，保留原片时间和分段局部时间。此页离线使用，不上传、不改动原稿。</p>
<div id="demoBanner" class="demo" hidden>合成测试夹具 · 仅用于 UI 与异常流程验证，不是原片成果，也不是正式绘制数量。</div>
<div class="notice"><strong>透明 PNG ≠ 已还原作者原始透明稿。</strong>字幕和特效的可复用程度仍按每帧提取状态复核；遮挡、混色或未知区域不会自动变成“完成”。复用候选、条件复用对与已确认项分开显示。</div>
<nav class="topnav" aria-label="页内导航"><a href="#review">逐帧检查</a><a href="#sections">语义 S 工作段</a><a href="#drawings">绘制与复用清单</a></nav></header>
<div id="fatal" class="error" role="alert" hidden></div><noscript><p class="error">此离线工作台需要 JavaScript。原始 JSON 与 PNG 文件仍可直接查看。</p></noscript>
<div id="stats" class="stats"></div>
<section id="review" class="card" aria-labelledby="reviewTitle"><h2 id="reviewTitle">逐帧叠加检查</h2>
<div class="toolbar"><label>工作段 S <select id="sectionSelect" aria-label="跳转语义工作段"></select></label><label>原镜头 M <select id="chapterSelect" aria-label="跳转原镜头"></select></label><label>显示 <select id="viewMode"><option value="overlay">仅透明叠加层</option><option value="split">叠加层 / 原片对照</option><option value="source">仅原片</option></select></label><label>叠加顺序 <select id="overlayOrder"><option value="auto">自动（按清单）</option><option value="fx_above">特效在字幕上</option><option value="fx_below">特效在字幕下</option></select></label><label>底色 <select id="background"><option value="checker">棋盘格</option><option value="light">白色</option><option value="dark">深色</option></select></label></div>
<div class="navrow"><div><label class="sr-only" for="frameSlider">原片帧号，从 0 开始</label><input id="frameSlider" type="range" min="0" max="0" value="0" step="1"></div><form id="frameForm" class="frame-form"><label for="frameInput" class="small">原片帧</label><input id="frameInput" type="number" min="0" max="0" value="0" step="1"><button type="submit">跳转</button></form></div>
<div class="toolbar"><button id="prevFrame" type="button" aria-label="上一帧">← 上一帧</button><button id="nextFrame" type="button" aria-label="下一帧">下一帧 →</button><button id="nextChange" type="button">下个叠加内容变化</button><label><input id="showSubtitles" type="checkbox" checked>字幕</label><label><input id="showEffects" type="checkbox" checked>特效</label><button id="retryImages" type="button">重试当前图片</button></div>
<div id="timing" class="timing" aria-live="polite"></div><p class="small muted">所有帧号从 0 开始，区间右端不包含；PTS 单位为 1/16000 秒。“下个变化”比较字幕 / 特效资源、提取状态及两轨层序，不把它当作人物新稿判定。</p>
<p id="overlayOrderStatus" class="small" aria-live="polite"></p><div id="stageGrid" class="stage-grid"><div id="overlayPanel" class="stage-panel"><div class="stage-head"><strong>独立透明叠加层</strong><span id="overlayOrderLabel"></span></div><div id="overlayStage" class="stage checker"><div class="stage-placeholder" id="overlayPlaceholder">正在读取当前帧的叠加资源…</div><div id="effectsPlane" class="plane effects"></div><div id="subtitlesPlane" class="plane subtitles"></div></div></div><div id="sourcePanel" class="stage-panel" hidden><div class="stage-head"><strong>同一原片帧</strong><span id="sourceBasis"></span></div><div id="sourceStage" class="stage checker"><div id="sourcePlaceholder" class="stage-placeholder">原片 PNG 缓存为可选</div><div id="sourcePlane" class="plane"></div></div><p id="sourceStatus" class="status-line small" aria-live="polite"></p><div id="sourceLinks" class="small"></div></div></div>
<div class="legend"><span class="pill">straight alpha · PNG 原尺寸链接</span><span class="pill warn">原片对照本身已含字幕 / FX，绝不再垫在叠加层下</span><span class="pill">缺图直接报错，不用邻近帧冒充</span></div>
<div class="asset-cards"><article id="subtitleCard" class="asset-card"></article><article id="effectCard" class="asset-card"></article></div>
<div class="reuse-current"><h3>当前帧：绘制与复用标记</h3><div id="frameReuse"></div></div><p id="announcement" class="sr-only" aria-live="polite"></p>
</section>
<section id="sections" class="card sections" aria-labelledby="sectionsTitle"><h2 id="sectionsTitle">语义 S 工作段</h2><p class="small muted">S 按完整语义动作组织，不等于每个镜头 M；跨镜头的整段黑裙舞蹈仍是同一个 S。局部帧 / PTS 按该 S 的实际范围顺序连续累计，原片坐标始终保留。</p><div class="table-wrap"><table><caption id="sectionCaption"></caption><thead><tr><th>S / 跳转</th><th>内容与原片区间</th><th>本段预算项</th><th>计划复用稿</th><th>观测复用曝光</th><th>已逐对复核</th><th>未决条件候选</th></tr></thead><tbody id="sectionRows"></tbody></table></div></section>
<section id="drawings" class="card drawings" aria-labelledby="drawingsTitle"><h2 id="drawingsTitle">绘制与复用清单</h2><p id="drawingExplanation" class="small muted"></p><div class="toolbar drawing-filters"><input id="drawingSearch" type="search" aria-label="搜索绘制清单" placeholder="搜索 ID、说明、备注…"><label>类别 <select id="kindFilter"><option value="">所有类型</option></select></label><label>计数 / 状态 <select id="planFilter"><option value="">全部</option><option value="planned">计入保守预算</option><option value="linework">线稿 / 局部项</option><option value="color_only">仅校色项</option><option value="crop">已确认裁切复用（不计新增）</option><option value="alias">别名（不计数）</option><option value="unplanned">未计入 / 待确认</option><option value="current">本帧已确认项</option><option value="candidate">本帧候选项</option></select></label><label>S 关联 <select id="drawingSection"><option value="">全部 S</option></select></label><label>段内关系 <select id="sectionRelation"><option value="all">全部关联</option><option value="new">本段预算项</option><option value="reused">计划复用稿</option><option value="observed">观测复用稿</option><option value="candidate">候选稿</option></select></label></div><p id="drawingResultCount" class="small muted" aria-live="polite"></p><div id="drawingGrid" class="drawing-grid"></div><button id="moreDrawings" type="button" style="margin-top:15px" hidden>再显示 36 项</button></section>
<details class="notice"><summary>文件、缺失资源与校验边界</summary><p class="small">本页内嵌清单元数据，不使用 fetch、CDN、远端字体或内嵌大幅 RGBA。PNG 必须随项目相对目录一起保存。构建器核验结构、帧序、PTS、路径与 straight-alpha 声明；这不代替像素完整性核验或人工语义检查。</p><div class="small"><a href="data/overlay_manifest.json">叠加清单 JSON</a> · <a href="data/reuse_manifest.json">复用清单 JSON</a> · <a href="data/work_sections.json">S 工作段 JSON</a></div><pre id="buildWarnings"></pre></details>
<footer class="footer">仅本地检查 · 只显示实际原片像素与清单记录 · 不生成遮挡后内容、不推定作者原稿身份、不自动确认候选复用。</footer>
</main>
<script id="viewerData" type="application/json">__MANIFEST_JSON__</script>
<script>
'use strict';
(function(){
const $=id=>document.getElementById(id);
const el=(tag,text,className)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=String(text);if(className)n.className=className;return n;};
const fmt=n=>Number(n).toLocaleString('zh-CN');
const pathURL=path=>path.split('/').map(encodeURIComponent).join('/');
const plain=v=>typeof v==='string'?v:JSON.stringify(v,null,2);
const statusLabels={no_text_expected:'清单判断此阶段预期无字幕',no_visible_text_detected:'未检测到可见文字；仍需核查',unsupported_scene:'当前场景未获支持',extracted_observed_regions:'已提取观测区域；请复核边缘与遮挡',extracted_with_review_regions:'已提取，但含待复核区域',partial_without_required_template:'所需时序模板缺失；仅保留直接像素部分',missing_required_template:'所需时序模板缺失；不是干净空字幕',partial_supported_effects:'仅提取受支持部分；不是完整特效保证',no_routed_effect_family:'未分配受支持特效类型；不代表没有特效',unsupported_visible_effect:'可见特效未获支持',no_supported_pixels_in_effect_phase:'特效阶段未取得受支持像素；仍需核查',synthetic_fixture_only:'合成测试，不是原片提取结果'};
const json=v=>JSON.stringify(v,null,2);
const contentKey=frame=>['subtitles','effects'].map(k=>{const v=frame.overlays[k];return JSON.stringify([v.asset_id,v.status,v.requires_review,k==='effects'?(v.metadata||{}).subtitle_relation||null:null]);}).join('|');
function nextContentChange(frames,index){const key=contentKey(frames[index]);for(let i=index+1;i<frames.length;i++)if(contentKey(frames[i])!==key)return i;return -1;}
function resolveOverlayOrder(metadata,override='auto'){const relation=metadata&&typeof metadata.subtitle_relation==='string'?metadata.subtitle_relation:null,known=relation==='above_subtitles'||relation==='below_subtitles',manual=override==='fx_above'||override==='fx_below',above=manual?override==='fx_above':relation==='above_subtitles';return {relation,known,manual,above,effective:above?'above_subtitles':'below_subtitles',warning:!known};}
function createLoadGate(){let current=0;return {next:()=>++current,isCurrent:token=>token===current,get token(){return current;}};}
// Pure helpers can be tested without a browser; no test hook changes production behaviour.
if(typeof module!=='undefined'&&module.exports){module.exports={contentKey,nextContentChange,resolveOverlayOrder,createLoadGate,pathURL};return;}
try{
const D=JSON.parse($('viewerData').textContent),frames=D.frames,last=frames.length-1;
const gate=createLoadGate();let current=0,visibleDrawings=36;
const drawMap=new Map(D.drawings.map(d=>[d.id,d])),sectionMap=new Map(D.sections.map(s=>[s.id,s]));
const chapterFirst=new Map();for(const f of frames)if(!chapterFirst.has(f.chapter_id))chapterFirst.set(f.chapter_id,f.frame);
const sourceBasisLabel=b=>b==='exact_original_frame_cache'?'精确原帧缓存':'清单记录的同一帧源图';
function setStatus(node,text,state){node.textContent=text;node.dataset.state=state||'';}
function link(path,text){const a=el('a',text);a.href=pathURL(path);a.target='_blank';a.rel='noopener';return a;}
function option(select,value,text){const o=el('option',text);o.value=value;select.append(o);}
function detail(label,value){const d=el('details');d.append(el('summary',label),el('pre',plain(value)));return d;}
function pill(text,warn){return el('span',text,'pill'+(warn?' warn':''));}
function jumpChip(id,candidate){const b=el('button',id,'chip'+(candidate?' candidate':''));b.type='button';b.addEventListener('click',()=>{$('drawingSearch').value=id;$('planFilter').value='';$('kindFilter').value='';$('drawingSection').value='';$('sectionRelation').value='all';visibleDrawings=36;renderDrawings();$('drawings').scrollIntoView({behavior:'smooth',block:'start'});});return b;}
function secSeconds(ticks){return (ticks/16000).toFixed(6).replace(/0+$/,'').replace(/\.$/,'');}
function imageLoad(path,token,onload,onerror){const im=new Image();im.decoding='async';im.onload=()=>{if(!gate.isCurrent(token))return;if(im.naturalWidth!==1920||im.naturalHeight!==1080){onerror('尺寸不是 1920 × 1080');return;}onload(im);};im.onerror=()=>{if(gate.isCurrent(token))onerror('PNG 缺失或无法解码');};im.src=pathURL(path);return im;}
function workBreakdown(data){return data.linework_count===null?'':data.linework_count+' 项线稿 / 局部 + '+data.color_only_count+' 项仅校色';}
function hasDetail(value){return value!==null&&value!==undefined&&value!==''&&(!Array.isArray(value)||value.length>0)&&(typeof value!=='object'||Object.keys(value).length>0);}
function renderStats(){const specs=[['原片视频帧',fmt(D.frame_count),'精确 PTS · '+secSeconds(D.video_duration_ticks)+' 秒'],['语义工作段',fmt(D.sections.length),'完整动作跨镜头仍归同一 S'],['保守工作预算',fmt(D.planning_count),workBreakdown(D)||'混合画幅 / 局部细节，不是全数全身稿'],['透明 PNG 资源',fmt(Object.values(D.assets).reduce((n,x)=>n+Object.keys(x).length,0)),'按 RGBA 内容哈希复用存储']];$('stats').replaceChildren(...specs.map(([label,num,note])=>{const c=el('div',undefined,'stat');c.append(el('span',label),el('strong',num),el('small',note));return c;}));}
function renderAsset(category,token){const item=frames[current].overlays[category],asset=item.asset_id?D.assets[category][item.asset_id]:null;
const title=category==='subtitles'?'字幕':'特效',card=$(category==='subtitles'?'subtitleCard':'effectCard'),plane=$(category+'Plane'),enabled=$(category==='subtitles'?'showSubtitles':'showEffects').checked;
plane.replaceChildren();card.replaceChildren();const heading=el('h3',title+'叠加层');heading.append(document.createTextNode(' '),pill(item.requires_review?'需要复核':'清单标记无需复核',item.requires_review));card.append(heading,el('p',statusLabels[item.status]||'此状态按原清单解释，不自动判为完成。','small'),el('p','提取状态：'+item.status,'mono small'));
const status=el('p','','status-line');status.setAttribute('aria-live','polite');card.append(status);
if(asset){card.append(el('p','alpha > 0：'+fmt(asset.nonzero_alpha_pixels)+' 像素 · 半透明：'+fmt(asset.partial_alpha_pixels)+' · 不透明：'+fmt(asset.opaque_pixels)));
const a=link(asset.path,'打开原尺寸 PNG ↗');a.download=asset.path.split('/').pop();card.append(a,el('p','RGBA SHA256 '+asset.rgba_sha256,'mono small'));
if(!enabled)setStatus(status,'显示已关闭；资源及状态仍保留。','');
else{setStatus(status,'正在读取当前帧资源…','loading');imageLoad(asset.path,token,im=>{im.alt='F'+String(current).padStart(6,'0')+' '+title+'透明叠加';plane.replaceChildren(im);setStatus(status,asset.nonzero_alpha_pixels?'PNG 已读取；是否可复用仍以状态和人工复核为准。':'此资源 alpha 全空；请同时查看提取状态，不能据此判定原片没有该内容。','loaded');updatePlaceholder();},reason=>{setStatus(status,reason+'：'+asset.path,'error');updatePlaceholder();});}}
else setStatus(status,'清单未提供此帧资源；状态为 '+item.status+'。不可用邻帧补齐。',item.requires_review?'error':'');
card.append(detail('提取证据 / 元数据',item.metadata));}
function updatePlaceholder(){const showing=$('subtitlesPlane').children.length+$('effectsPlane').children.length;$('overlayPlaceholder').hidden=showing>0;if(!showing)$('overlayPlaceholder').textContent=(!$('showSubtitles').checked&&!$('showEffects').checked)?'字幕与特效显示均已关闭。':'尚无可显示叠加资源；请查看下方读取状态。';}
function renderSource(token){$('sourcePlane').replaceChildren();$('sourceLinks').replaceChildren();$('sourcePlaceholder').hidden=false;$('sourceBasis').textContent='';
if($('viewMode').value==='overlay'){setStatus($('sourceStatus'),'原片对照未启用。','');return;}
const f=frames[current],choices=f.sources;let index=0;const failures=[];$('sourcePlaceholder').textContent='正在读取同一原片帧…';setStatus($('sourceStatus'),'仅尝试 F'+String(f.frame).padStart(6,'0')+' 的精确记录。','loading');
function attempt(){if(!gate.isCurrent(token))return;if(index>=choices.length){$('sourcePlaceholder').textContent='缺少这一帧的原片 PNG。不会显示邻近帧。';setStatus($('sourceStatus'),'精确帧不可用：'+failures.join('；'),'error');return;}const choice=choices[index++];imageLoad(choice.path,token,im=>{im.alt='精确原片帧 F'+String(f.frame).padStart(6,'0');$('sourcePlane').replaceChildren(im);$('sourcePlaceholder').hidden=true;$('sourceBasis').textContent=sourceBasisLabel(choice.basis);setStatus($('sourceStatus'),'F'+String(f.frame).padStart(6,'0')+' · '+sourceBasisLabel(choice.basis)+(failures.length?'；缓存未命中，使用已记录的同帧源图。':''),'loaded');$('sourceLinks').append(link(choice.path,'打开原尺寸同帧源图 ↗'),el('p',choice.basis,'mono small'));},reason=>{failures.push(choice.path+'（'+reason+'）');attempt();});}attempt();}
function renderFrameReuse(){const r=frames[current].reuse,target=$('frameReuse');target.replaceChildren(el('p','标记状态：'+r.status,'small mono'));
for(const [label,key,candidate] of [['已标记的规范稿','canonical_ids',false],['候选稿（未自动确认）','candidate_ids',true],['候选家族（不计作确认复用）','candidate_family_ids',true]]){const row=el('div',undefined,'small');row.append(el('span',label+'：'));const chips=el('div',undefined,'chips');if(!r[key].length)chips.append(el('span','—','muted'));else r[key].forEach(id=>chips.append(jumpChip(id,candidate)));row.append(chips);target.append(row);}target.append(el('p','曝光记录：'+(r.occurrence_ids.join('、')||'—'),'small mono'),detail('当前帧证据',r.evidence));}
function renderOverlayOrder(){const state=resolveOverlayOrder(frames[current].overlays.effects.metadata,$('overlayOrder').value);$('effectsPlane').style.zIndex=state.above?'2':'1';$('subtitlesPlane').style.zIndex=state.above?'1':'2';const effective=state.above?'特效在字幕上':'特效在字幕下',node=$('overlayOrderStatus');$('overlayOrderLabel').textContent=effective+' · 1920 × 1080';node.className=state.warning?'notice order-warning small':'small muted';node.dataset.effectiveOrder=state.effective;node.dataset.uncertain=String(state.warning);const declared=state.known?(state.relation==='above_subtitles'?'特效在字幕上':'特效在字幕下'):(state.relation||'未记录');let text=state.manual?'手动覆盖：'+effective+'；清单关系：'+declared+'。':'自动：'+(state.known?effective+'。':'层序混合 / 未确定（'+declared+'）；临时按特效在下显示，请手动核查或覆盖。');if(state.manual&&state.warning)text+=' 手动选择不等于已确认原片层序。';node.textContent=text+' 这里只排列字幕和特效两条透明轨；相对人物 / 原片的 recommended_stack_position 不参与此顺序，原片对照保持独立。';return state;}
function renderFrame(){const f=frames[current],token=gate.next(),mode=$('viewMode').value,bg=$('background').value;
$('frameSlider').value=String(current);$('frameInput').value=String(current);$('sectionSelect').value=f.section_id;$('chapterSelect').value=f.chapter_id;
$('prevFrame').disabled=current===0;$('nextFrame').disabled=current===last;$('nextChange').disabled=nextContentChange(frames,current)<0;
$('overlayPanel').hidden=mode==='source';$('sourcePanel').hidden=mode==='overlay';$('stageGrid').classList.toggle('split',mode==='split');$('overlayStage').className='stage '+bg;$('sourceStage').className='stage '+bg;
$('timing').replaceChildren(...[['原片','F'+String(f.frame).padStart(6,'0')+' / '+last],['原片 PTS',f.pts+' / 16000 = '+secSeconds(f.pts)+' s'],['本帧时长',f.duration_ticks+' ticks'],[f.section_id+' 局部','F'+String(f.local_frame).padStart(6,'0')+' · PTS '+f.local_pts+' / 16000'],['镜头 / 组',f.chapter_id+' / '+(f.group||'—')]].map(([label,value])=>{const s=el('span');s.append(el('strong',label+' '),document.createTextNode(value));return s;}));
renderOverlayOrder();$('overlayPlaceholder').hidden=false;renderAsset('effects',token);renderAsset('subtitles',token);updatePlaceholder();renderSource(token);renderFrameReuse();renderDrawings();}
function goToFrame(value){const number=Number(value);if(!Number.isInteger(number)||number<0||number>last){$('announcement').textContent='请输入 0 至 '+last+' 的整数帧号。';$('frameInput').setCustomValidity('请输入 0 至 '+last+' 的整数帧号');$('frameInput').reportValidity();return false;}$('frameInput').setCustomValidity('');current=number;renderFrame();return true;}
function renderSections(){const body=$('sectionRows');body.replaceChildren();$('sectionCaption').textContent=D.sections.length+' 个语义 S；保守预算 / 计划复用 / 观测复用 / 条件候选保持分栏，别名不重复计数。预算不代表每项都已确认必须另画。';
for(const s of D.sections){const tr=el('tr');tr.id='section-'+s.id;const first=el('td'),b=el('button',s.id,'jump');b.type='button';b.addEventListener('click',()=>{goToFrame(s.ranges[0].start_frame);$('review').scrollIntoView({behavior:'smooth'});});first.append(b);const content=el('td');content.append(el('strong',s.title));const packageLinks=el('div',undefined,'links small');for(const file of s.package_files)if(file.present_at_build){packageLinks.append(link(file.path,file.label),document.createTextNode(' · '));}if(!packageLinks.children.length)packageLinks.append(el('span','分包文件尚未生成','muted'));content.append(packageLinks);s.ranges.forEach(r=>content.append(el('div','F'+r.start_frame+'–'+(r.end_frame_exclusive-1)+' · PTS ['+r.start_pts+', '+r.end_pts_exclusive+')','mono small')));const newCell=el('td');const nb=el('button',s.new_drawing_count+' 项','jump');nb.type='button';nb.addEventListener('click',()=>{$('drawingSection').value=s.id;$('sectionRelation').value='new';$('planFilter').value='planned';$('drawingSearch').value='';visibleDrawings=36;renderDrawings();$('drawings').scrollIntoView({behavior:'smooth'});});if(workBreakdown(s))newCell.append(el('p',workBreakdown(s),'small'));newCell.append(nb,el('div',Object.entries(s.new_kind_counts).map(([k,v])=>(D.kind_names[k]||k)+' '+v).join(' · '),'small muted'));
tr.append(first,content,newCell,el('td',s.reused_drawing_count+' 稿'),el('td',s.observed_reused_exposure_count+' 次 / '+s.observed_reused_drawing_count+' 稿'),el('td',s.reviewed_crop_pair_ids.length+' 对'),el('td',s.conditional_reuse_pair_ids.length+' 对（未确认新增）'));body.append(tr);}}
function drawingMatches(d){const q=$('drawingSearch').value.trim().toLocaleLowerCase(),kind=$('kindFilter').value,filter=$('planFilter').value,sid=$('drawingSection').value,r=frames[current].reuse;
if(q&&!([d.id,d.title,d.kind,d.planning_status,plain(d.notes)].join(' ').toLocaleLowerCase().includes(q)))return false;if(kind&&d.kind!==kind)return false;if(filter==='planned'&&(!d.count_in_conservative_plan||d.alias_of))return false;if(filter==='linework'&&(!d.count_in_conservative_plan||d.line_drawing_required!==true))return false;if(filter==='color_only'&&(!d.count_in_conservative_plan||d.work_operation!=='recolor_only'))return false;if(filter==='crop'&&d.work_operation!=='crop_reuse_alias')return false;if(filter==='alias'&&!d.alias_of)return false;if(filter==='unplanned'&&(d.count_in_conservative_plan||d.alias_of))return false;if(filter==='current'&&!r.canonical_ids.includes(d.id))return false;if(filter==='candidate'&&!r.candidate_ids.includes(d.id))return false;
if(sid){const s=sectionMap.get(sid),relation=$('sectionRelation').value,byRelation={new:s.new_drawing_ids,reused:s.reused_drawing_ids,observed:s.observed_reused_drawing_ids,candidate:s.candidate_drawing_ids},ids=byRelation[relation]||[...s.new_drawing_ids,...s.reused_drawing_ids,...s.observed_reused_drawing_ids,...s.candidate_drawing_ids];if(!ids.includes(d.id))return false;}return true;}
function drawingCard(d){const currentDrawing=frames[current].reuse.canonical_ids.includes(d.id),article=el('article',undefined,'drawing-card'+(currentDrawing?' current':''));article.id='drawing-'+d.id;article.append(el('h3',d.id+' · '+d.title),pill(D.kind_names[d.kind]||d.kind),document.createTextNode(' '),pill(d.alias_of?'别名 → '+d.alias_of:d.count_in_conservative_plan?'计入保守预算':'未计入 / 待确认',!d.count_in_conservative_plan&&!d.alias_of),el('p',d.planning_status,'mono small'));
const links=el('div',undefined,'links small');for(const source of d.sources){links.append(link(source.path,'F'+source.frame+' 原像素 ↗'));}if(!d.sources.length)links.append(el('span','无显式源图记录','muted'));article.append(links);
if(d.work_operation==='crop_reuse_alias')article.append(el('p','已确认裁切复用 → '+d.alias_of+'；仅复用原片中已证实部分，不推断隐藏区域。','pill good'));
const notes=plain(d.notes);if(notes&&notes!=='[]')article.append(el('p',notes));
if(d.work_operation)article.append(el('p','工作归类：'+({line_drawing:'线稿 / 局部绘制',recolor_only:'仅校色，不需另画线稿',local_line_redraw:'局部线稿修改',pose_redraw:'姿态差异，保留绘制项',crop_reuse_alias:'已确认裁切复用，不计额外工作项'}[d.work_operation]||d.work_operation),'small'));
for(const [key,label] of [['work_scope','本项工作范围'],['partial_reuse_scope','局部复用范围（不是整稿复用）'],['redraw_regions','仍需另画 / 调整的区域'],['color_adjustment_regions','仅校色范围'],['crop_review_evidence','逐对复核证据']])if(hasDetail(d[key]))article.append(detail(label,d[key]));
const reviewed=D.reviewed_crop_pairs.filter(p=>(p.id||p.pair_id)===d.crop_review_pair_id);if(reviewed.length)article.append(detail('逐对复核结论（不是未决条件候选）',reviewed));
const pairs=D.conditional_reuse_pairs.filter(p=>p.from_id===d.id||p.to_id===d.id);if(pairs.length)article.append(detail('优先核查全身裁切复用候选，未确认新增（不授权替换素材）',pairs));
const details=el('details');details.append(el('summary','曝光 / 复用记录（'+d.occurrences.length+'）'));const list=el('ul');for(const o of d.occurrences){const li=el('li');const b=el('button','F'+o.start_frame+'–'+(o.end_frame_exclusive-1),'chip');b.type='button';b.addEventListener('click',()=>{goToFrame(o.start_frame);$('review').scrollIntoView({behavior:'smooth'});});li.append(b,el('div',(o.chapter_id||'')+' · '+(o.status||'')+' · PTS ['+o.start_pts+', '+o.end_pts_exclusive+')','mono small'),detail('变换与证据',{id:o.id,transform:o.transform,evidence:o.evidence}));list.append(li);}details.append(list);article.append(details);return article;}
function renderDrawings(){const filtered=D.drawings.filter(drawingMatches);$('drawingGrid').replaceChildren(...filtered.slice(0,visibleDrawings).map(drawingCard));if(!filtered.length)$('drawingGrid').append(el('p','没有符合当前筛选的规范稿。候选家族可能尚未登记为规范稿；请查看当前帧证据或复用 JSON。','empty'));$('drawingResultCount').textContent='显示 '+Math.min(filtered.length,visibleDrawings)+' / '+filtered.length+' 项；规范记录总数 '+D.drawings.length+'。候选不是确认复用，别名不计新增稿。';$('moreDrawings').hidden=visibleDrawings>=filtered.length;}
renderStats();$('demoBanner').hidden=!D.synthetic_fixture;
for(const s of D.sections){option($('sectionSelect'),s.id,s.id+' · '+s.title);option($('drawingSection'),s.id,s.id+' · '+s.title);}for(const [chapter] of chapterFirst)option($('chapterSelect'),chapter,chapter);for(const kind of [...new Set(D.drawings.map(d=>d.kind))].sort())option($('kindFilter'),kind,D.kind_names[kind]||kind);
$('frameSlider').max=String(last);$('frameInput').max=String(last);$('drawingExplanation').textContent='保守工作预算 '+D.planning_count+' 项'+(workBreakdown(D)?'（'+workBreakdown(D)+'）':'')+'：'+Object.entries(D.kind_counts).map(([k,v])=>(D.kind_names[k]||k)+' '+v).join('、')+'。身体动作也含坐姿、遮挡与裁切；这是混合工作量，不是 '+D.planning_count+' 张全身稿，也不是 '+D.planning_count+' 项必需新画，更不是全片绝对张数。来源像素同源不等于所有作者原稿身份已确认。别名不重复计数；未决原片状态仍可能增加工作量。'+(D.reviewed_crop_pairs.length?' 已逐对复核 '+D.reviewed_crop_pairs.length+' 对，其中 '+D.confirmed_crop_reuse_count+' 对已确认裁切复用，作为别名不计额外工作项；其他按局部修改、校色或姿态差异分别处理，不再混作未决条件候选。':'')+(D.conditional_reuse_pairs.length?' 当前 '+D.conditional_reuse_pairs.length+' 对：优先核查全身裁切复用候选，未确认新增。建议先画全身，再判断真正不同的半身；这是工作顺序建议，不是教程原文。':'')+(D.optional_brooch_portrait_count?' 胸针肖像如需替换角色，另加 '+D.optional_brooch_portrait_count+' 项（未计入上述预算）。':'');
$('buildWarnings').textContent=D.warning_count?('构建时缺失资源 '+D.warning_count+' 项：\n'+D.warnings.join('\n')):'构建时未发现缺失叠加 PNG。原片缓存为可选；浏览器仍会单独报告解码或读取失败。';
$('sectionSelect').addEventListener('change',e=>goToFrame(sectionMap.get(e.target.value).ranges[0].start_frame));$('chapterSelect').addEventListener('change',e=>goToFrame(chapterFirst.get(e.target.value)));
$('frameSlider').addEventListener('input',e=>goToFrame(e.target.value));$('frameForm').addEventListener('submit',e=>{e.preventDefault();goToFrame($('frameInput').value);});$('frameInput').addEventListener('input',()=> $('frameInput').setCustomValidity(''));
$('prevFrame').addEventListener('click',()=>goToFrame(Math.max(0,current-1)));$('nextFrame').addEventListener('click',()=>goToFrame(Math.min(last,current+1)));$('nextChange').addEventListener('click',()=>{const n=nextContentChange(frames,current);if(n>=0)goToFrame(n);else $('announcement').textContent='后续没有叠加内容变化。';});
for(const id of ['viewMode','background','showSubtitles','showEffects','overlayOrder'])$(id).addEventListener('change',renderFrame);$('retryImages').addEventListener('click',renderFrame);
for(const id of ['drawingSearch','kindFilter','planFilter','drawingSection','sectionRelation'])$(id).addEventListener(id==='drawingSearch'?'input':'change',()=>{visibleDrawings=36;renderDrawings();});$('moreDrawings').addEventListener('click',()=>{visibleDrawings+=36;renderDrawings();});
document.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||['INPUT','SELECT','TEXTAREA','BUTTON'].includes(e.target.tagName))return;if(e.key==='ArrowLeft'){e.preventDefault();goToFrame(Math.max(0,current-1));}if(e.key==='ArrowRight'){e.preventDefault();goToFrame(Math.min(last,current+1));}});
renderSections();renderFrame();
window.magicMaidViewer={goToFrame,getState:()=>({frame:current,generation:gate.token,section:frames[current].section_id,mode:$('viewMode').value,overlay_order:resolveOverlayOrder(frames[current].overlays.effects.metadata,$('overlayOrder').value).effective})};
}catch(error){$('fatal').hidden=false;$('fatal').textContent='工作台初始化失败：'+error.message+'。请检查清单和本地文件，未显示的数据不视为通过。';}
})();
</script>
</body></html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path("magic_maid_20261029"))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--overlay-manifest", default="data/overlay_manifest.json")
    parser.add_argument("--reuse-manifest", default="data/reuse_manifest.json")
    parser.add_argument("--sections", default="data/work_sections.json")
    parser.add_argument("--catalog", default="data/panel_catalog.json")
    parser.add_argument("--verify-assets", action="store_true", help="Also verify each available PNG file SHA256; does not certify semantic alpha quality")
    args = parser.parse_args()
    try:
        result = build(args.project, args.output, overlay_name=args.overlay_manifest, reuse_name=args.reuse_manifest,
                       sections_name=args.sections, catalog_name=args.catalog, verify_assets=args.verify_assets)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"overlay viewer: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
