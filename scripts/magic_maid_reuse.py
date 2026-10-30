#!/usr/bin/env python3
"""Source-safe reuse planning, recovered from the pre-reset implementation.

Numbered attachment-2 compositions are guidance, not independent drawings.
All old IDs survive. Only explicitly reviewed visible-art aliases stop creating
a second work item. Unknown original frames remain unknown. Rebuilding requires
the original source, original catalog/audits, and revalidated review evidence;
historical summary numbers are not an input from which to fabricate a manifest.
"""
from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
SOURCE_SHA = "ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1"
REFERENCE_SHA = "fe3031cd98c5488949f26194e503d41ba966e8261e1c8a280686e90651aad498"
NFRAMES, END_PTS = 4763, 2543333
CROP_REPORT = "data/crop_reuse_report.json"
CROP_CLASSES = ("confirmed_crop_reuse", "color_only_variant", "local_line_variant", "different_pose", "occlusion_uncertain")
IDENTITY_MATRIX = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
REVIEWS = ["drawing_spot_audit.json", "drawing_g12_audit.json", "drawing_g13_audit.json",
           "drawing_g33_audit.json", "drawing_red_audit.json", "drawing_g51_audit.json"]

# Reviewed common VISIBLE character art, not hidden pixels or author cels.
# Similar gray hand/plate/line variants are deliberately not merged further.
ALIAS_GROUPS = {
    "G06-02": ["G06-06", "G06-11"], "G06-04": ["G06-07", "G06-08"],
    "G06-05": ["G06-09", "G06-10"],
    "G07-03": ["G07-08", "G07-15"], "G07-04": ["G07-09", "G07-16"],
    "G07-05": ["G07-10", "G07-11", "G07-17"], "G07-06": ["G07-12"], "G07-07": ["G07-13"],
    "G10-01": ["G10-02"], "G10-03": ["G10-04"],
    "G11-04": ["G11-05"], "G11-06": ["G11-07", "G11-08", "G11-09"],
    "G12-01": ["G12-02", "G12-03"], "G12-04": ["G12-05"], "G12-06": ["G12-07"],
    "G26-04": ["G26-01", "G26-02", "G26-03"], "G51-18": ["G51-19"],
}
ALIASES = {alias: master for master, aliases in ALIAS_GROUPS.items() for alias in aliases}
NONCHAR = {"G03", "G04", "G05", "G14", "G16", "G30", "G31", "G46", "X03", "X04", "X05"}
BODY_POSE = {"G01", "G02", "G06", "G15", "G17", "G19", "G20", "G22", "G23", "G25",
             "G27", "G28", "G33", "G34", "G35", "G36", "G45", "G51", "X01"}
HEAD = {"G11", "G26", "G32", "G47"}
HAND = {"G08", "G10"}
NO_CHARACTER = [(0, 9), (170, 422), (778, 784), (1159, 1175), (1328, 1404),
                (1489, 1498), (1908, 1976), (3778, 4021), (4261, 4280),
                (4310, 4337), (4355, 4401), (4431, 4511)]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def safe_path(root: Path, value: str) -> Path:
    rel = Path(value)
    if not value or rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"not a project-relative path: {value!r}")
    path = root / rel
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"path escapes project: {value!r}")
    return path


def load(root: Path, name: str) -> Any:
    return json.loads(safe_path(root, name).read_text(encoding="utf-8"))


def art(panel: str) -> str:
    return "ART-" + ALIASES.get(panel, panel)


def kind(group: str) -> str:
    if group in BODY_POSE:
        return "body_pose"
    if group in HEAD:
        return "head_detail"
    if group in HAND:
        return "hand_detail"
    return "mouth_detail" if group == "G48" else "half_body"


def pts_end(timeline: list[dict], stop: int) -> int:
    return timeline[stop]["pts"] if stop < NFRAMES else END_PTS


def flatten_intervals(review: dict) -> list[dict]:
    rows = review["reviewed_intervals"]
    return [r for group in rows.values() for r in group] if isinstance(rows, dict) else rows


def panel_art_ids(panel: str, records: dict) -> list[str]:
    if "ART-" + panel not in records or records["ART-" + panel]["planning_status"] == "excluded_non_character":
        return []
    if panel.startswith("G32-"):
        return [art(f"G32-{i:02d}") for i in range(1, int(panel[-2:])+1)]
    return [art(panel)]


def conditional_pairs() -> list[dict]:
    """49 specific candidates; never reduce the conservative plan silently."""
    pairs = []
    for n in list(range(1, 32)) + list(range(46, 68)):
        target = 1 if n <= 3 else 2 if n <= 5 else 3 if n <= 7 else n-4
        from_id, to_id = art(f"G12-{n:02d}"), art(f"G33-{target:02d}")
        if any(p["from_id"] == from_id for p in pairs):
            continue
        pairs.append({"id": f"CROSS-{len(pairs)+1:02d}", "from_id": from_id, "to_id": to_id,
            "confirmed": False, "status": "reference_guided_visible_geometry_candidate",
            "possible_planning_reduction": 1, "transform_operations": ["scale", "translation", "crop"],
            "matrix": None, "mirror": "not_asserted", "evidence": ["N04", "data/reuse_review_evidence.json"],
            "reason": "同顺序头/手/服装轮廓相近；原尺寸缩放配准及字幕/遮挡区域尚未完全证实，不自动复用。"})
    return pairs


def validate_crop_transform(transform: dict) -> None:
    """Only the reviewed positive uniform scale and translation are admissible."""
    if (transform.get("direction") != "fullbody_to_halfbody" or transform.get("mirror") is not False
            or transform.get("rotation_deg") != 0 or transform.get("anisotropic_scale") is not False
            or transform.get("local_warp") is not False):
        raise ValueError("crop decision contains an unreviewed deformation")
    scale, translation = transform.get("scale"), transform.get("translation")
    if (not isinstance(scale, (int, float)) or isinstance(scale, bool) or not math.isfinite(scale)
            or scale <= 0 or not isinstance(translation, list) or len(translation) != 2
            or any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) for x in translation)):
        raise ValueError("invalid crop scale or translation")
    expected = [[scale, 0, translation[0]], [0, scale, translation[1]], [0, 0, 1]]
    matrix = transform.get("matrix")
    if (not isinstance(matrix, list) or len(matrix) != 3
            or any(not isinstance(row, list) or len(row) != 3 for row in matrix)
            or any(not isinstance(v, (int, float)) or not math.isfinite(v)
                   or abs(v - expected[i][j]) > 1e-10 for i, row in enumerate(matrix) for j, v in enumerate(row))):
        raise ValueError("crop matrix is not the stated uniform transform")


def validate_crop_decisions(report: dict) -> None:
    if report.get("schema") != "magic-maid.crop-reuse-review/1" or report.get("review_complete") is not True:
        raise ValueError("only a final complete crop review may change work items")
    if report.get("source_sha256") != SOURCE_SHA or report.get("reference_sha256") != REFERENCE_SHA:
        raise ValueError("crop report source identity mismatch")
    expected = {p["id"]: (p["from_id"], p["to_id"]) for p in conditional_pairs()}
    rows = report.get("pairs", [])
    if len(rows) != len(expected) or len({r.get("id") for r in rows}) != len(expected):
        raise ValueError("crop report must cover all unique nominated pairs")
    counts = Counter()
    for row in rows:
        if expected.get(row.get("id")) != (row.get("from_id"), row.get("to_id")):
            raise ValueError("crop pair identity changed without a reviewed mapping")
        classification = row.get("classification")
        if classification not in CROP_CLASSES or row.get("visual_reviewed") is not True:
            raise ValueError("crop reuse requires explicit visual decisions, not scores")
        if row.get("confirmed") is not (classification == "confirmed_crop_reuse"):
            raise ValueError("only pure crop reuse can remove a whole work item")
        validate_crop_transform(row.get("transform", {}))
        if not row.get("work_scope") or not row.get("partial_reuse_scope"):
            raise ValueError("crop decisions must define the remaining work")
        redraw, colors = row.get("redraw_regions", []), row.get("color_adjustment_regions", [])
        if classification == "confirmed_crop_reuse" and (redraw or colors):
            raise ValueError("pure crop reuse cannot require local edits")
        if classification == "color_only_variant" and (redraw or not colors):
            raise ValueError("color-only operation cannot invent linework")
        if classification in ("local_line_variant", "different_pose") and not redraw:
            raise ValueError("retained variant must identify redraw regions")
        if not row.get("evidence_paths") or set(row["evidence_paths"]) != set(row.get("evidence_sha256", {})):
            raise ValueError("crop decision lacks hashed source evidence")
        counts[classification] += 1
    if report.get("summary", {}).get("classification_counts") != {key: counts[key] for key in CROP_CLASSES}:
        raise ValueError("crop review classification summary mismatch")
    if report["summary"].get("recommended_whole_work_item_reduction") != counts["confirmed_crop_reuse"]:
        raise ValueError("crop review proposes an unsupported reduction")


def verify_crop_assets(root: Path, report: dict, timeline: list[dict]) -> dict:
    """Recheck evidence files and actual decoded source RGB, not a saved score."""
    from PIL import Image
    evidence, rgb = {}, {}
    for name, digest in report.get("supporting_report_sha256", {}).items():
        if sha(safe_path(root, name)) != digest:
            raise ValueError("crop supporting report changed: " + name)
        evidence[name] = digest
    for row in report["pairs"]:
        for name, digest in row["evidence_sha256"].items():
            if name not in evidence and sha(safe_path(root, name)) != digest:
                raise ValueError("crop evidence changed: " + name)
            if name in evidence and evidence[name] != digest:
                raise ValueError("inconsistent crop evidence hashes")
            evidence[name] = digest
        for side in ("half_body", "full_body"):
            frame = row["source_frames"][side]
            if (not isinstance(frame, int) or not 0 <= frame < len(timeline)
                    or row["source_pts"][side] != timeline[frame]["pts"]):
                raise ValueError("crop source frame/PTS mismatch")
            name = row["source_paths"][side]
            if name != f"frames/F{frame:06d}.png":
                raise ValueError("crop source frame/path mismatch")
            if name not in rgb:
                with Image.open(safe_path(root, name)) as im:
                    rgb[name] = hashlib.sha256(im.convert("RGB").tobytes()).hexdigest()
            if rgb[name] != row["source_rgb_sha256"][side]:
                raise ValueError("crop original-frame RGB changed: " + name)
    return {"evidence_files_verified": len(evidence), "original_rgb_samples_verified": len(rgb)}


def load_crop_review(root: Path, timeline: list[dict]) -> dict:
    report = load(root, CROP_REPORT)
    validate_crop_decisions(report)
    verify_crop_assets(root, report, timeline)
    return report


def resolve_alias(records: dict, identifier: str) -> tuple[str, list[str]]:
    chain, current = [], identifier
    while True:
        if current in chain:
            raise ValueError("cyclic drawing aliases")
        if current not in records:
            raise ValueError("alias target is missing")
        chain.append(current)
        target = records[current].get("alias_of")
        if not target:
            if not records[current]["count_in_conservative_plan"]:
                raise ValueError("alias ends at an uncounted item")
            return current, chain
        current = target


def crop_occurrence_transform(frame: dict, decision: dict) -> dict | None:
    """The crop matrix is not a license to guess another shot's camera motion."""
    old = frame.get("transform", {})
    same_canvas = (frame.get("chapter_id") == "M24"
        and frame.get("evidence") == "data/reuse_m24_review.json"
        and old.get("status") == "observed_same_source_canvas_geometry"
        and old.get("matrix") == IDENTITY_MATRIX and old.get("mirror") is False)
    direct = (frame.get("evidence") == "native_RGB_catalog_identity"
        or (frame.get("chapter_id") == "M09" and frame.get("evidence") == "data/drawing_g12_audit.json"))
    if not (same_canvas or direct):
        return None
    matrix = copy.deepcopy(decision["transform"]["matrix"])
    # M24's established same-canvas mapping is identity; I @ crop == crop.
    return {"status": "reviewed_crop_composed_with_observed_identity" if same_canvas else "reviewed_crop_source_canvas",
        "direction": "canonical_fullbody_source_canvas_to_occurrence_source_canvas",
        "operations": ["scale", "translation", "crop"], "matrix": matrix,
        "mirror": False, "rotation_deg": 0, "anisotropic_scale": False, "local_warp": False,
        "source_canonical_id": decision["to_id"], "via_half_body_id": decision["from_id"],
        "crop_review_pair_id": decision["id"], "evidence": [CROP_REPORT] + decision["evidence_paths"],
        "composition": ["identity_same_source_canvas", "reviewed_fullbody_to_halfbody"] if same_canvas else ["reviewed_fullbody_to_halfbody"]}


def integrate_crop_review(records: dict, frames: list[dict], report: dict) -> list[dict]:
    """Only confirmed pure crops become aliases. Variants remain actionable items."""
    validate_crop_decisions(report)
    pure = {r["from_id"]: r for r in report["pairs"] if r["classification"] == "confirmed_crop_reuse"}
    for row in records.values():
        row.setdefault("work_operation", "line_drawing" if row["count_in_conservative_plan"] else "not_counted")
        row.setdefault("line_drawing_required", bool(row["count_in_conservative_plan"]))
        row.setdefault("work_scope", "原片可见人物绘制工作项；按现有参考范围制作，不推定隐藏部分。")
    for decision in report["pairs"]:
        source, master = records[decision["from_id"]], records[decision["to_id"]]
        if (decision["source_frames"]["half_body"] not in source["source_frames"]
                or decision["source_frames"]["full_body"] not in master["source_frames"]):
            raise ValueError("crop report source sample is not owned by its drawing ID")
        source.update(work_scope=copy.deepcopy(decision["work_scope"]),
            partial_reuse_scope=copy.deepcopy(decision["partial_reuse_scope"]),
            redraw_regions=copy.deepcopy(decision.get("redraw_regions", [])),
            color_adjustment_regions=copy.deepcopy(decision.get("color_adjustment_regions", [])),
            crop_review_pair_id=decision["id"], crop_review_classification=decision["classification"],
            crop_review_evidence=[CROP_REPORT] + decision["evidence_paths"],
            reviewed_base_id=decision["to_id"], reviewed_base_to_half_transform=copy.deepcopy(decision["transform"]))
        classification = decision["classification"]
        if classification == "confirmed_crop_reuse":
            source.update(planning_status="confirmed_alias", count_in_conservative_plan=False,
                alias_of=master["id"], work_operation="crop_reuse_alias", line_drawing_required=False,
                confidence="source_reviewed_common_visible_crop_geometry_not_author_cel_identity")
            for key in ("reference_panel_ids", "source_frames", "source_images", "source_samples"):
                for value in source[key]:
                    if value not in master[key]:
                        master[key].append(copy.deepcopy(value))
            master["source_frames"] = sorted(master["source_frames"])
            master.setdefault("crop_reused_half_body_ids", []).append(source["id"])
            master.setdefault("crop_review_pair_ids", []).append(decision["id"])
        elif classification == "color_only_variant":
            source.update(work_operation="recolor_only", line_drawing_required=False)
        elif classification == "local_line_variant":
            source.update(work_operation="local_line_redraw", line_drawing_required=True)
        elif classification == "different_pose":
            source.update(work_operation="pose_redraw", line_drawing_required=True)
    # Snapshot chains before flattening so even old G12-02 -> G12-01 is retained.
    resolutions = {key: resolve_alias(records, key) for key, row in records.items()
        if row["count_in_conservative_plan"] or row.get("alias_of")}
    for identifier, (target, chain) in resolutions.items():
        row = records[identifier]
        if len(chain) > 1:
            row["alias_resolution_chain"] = chain
            row["alias_of"] = target
            row["line_drawing_required"] = False
            if any(key in pure for key in chain):
                decision = next(pure[key] for key in chain if key in pure)
                row.update(work_operation="crop_reuse_alias", crop_review_pair_id=decision["id"],
                    crop_review_classification="confirmed_crop_reuse",
                    crop_review_evidence=[CROP_REPORT] + decision["evidence_paths"],
                    work_scope="保留旧编号和源样本；经已核对的同画布别名链复用全身母稿，不新增整稿。")
    for frame in frames:
        original_ids = list(frame["canonical_ids"])
        original_candidates = list(frame["candidate_ids"])
        frame["canonical_ids"] = sorted({resolutions[x][0] for x in original_ids})
        frame["candidate_ids"] = sorted({resolutions[x][0] for x in original_candidates})
        if frame["canonical_ids"] != original_ids:
            frame["canonical_ids_before_crop_review"] = original_ids
            if "transform" in frame:
                frame["transform_before_crop_review"] = copy.deepcopy(frame["transform"])
            decisions = [pure[x] for x in original_ids if x in pure]
            frame["crop_review_pair_ids"] = [x["id"] for x in decisions]
            frame["crop_review_evidence"] = [CROP_REPORT]
            if len(decisions) == 1 and len(original_ids) == 1:
                transform = crop_occurrence_transform(frame, decisions[0])
                if transform:
                    frame["transform"] = transform
                else:
                    frame["transform"] = {"status": "crop_alias_identity_only_occurrence_camera_unestablished",
                        "matrix": None, "mirror": "not_asserted", "crop_review_pair_id": decisions[0]["id"]}
        if frame["candidate_ids"] != original_candidates:
            frame["candidate_ids_before_crop_review"] = original_candidates
            frame["candidate_identity_status"] = "unresolved_after_canonical_alias_remap"
            # In particular, never put the reviewed crop matrix on an unknown shot.
    unresolved = {r["id"] for r in report["pairs"] if r["classification"] == "occlusion_uncertain"}
    return [p for p in conditional_pairs() if p["id"] in unresolved]


def occurrence_signature(frame: dict) -> tuple:
    return (tuple(frame["canonical_ids"]), frame["chapter_id"],
        json.dumps(frame.get("transform", {}), sort_keys=True),
        tuple(frame.get("canonical_ids_before_crop_review", [])))


def validate(data: dict, timeline: list[dict]) -> None:
    if data.get("source_sha256") != SOURCE_SHA or data.get("reference_sha256") != REFERENCE_SHA or data.get("frame_count") != NFRAMES:
        raise ValueError("incorrect source identity")
    if data.get("all_author_drawings_proven_complete") is not False:
        raise ValueError("unsupported completeness claim")
    crop = data.get("crop_reuse_report", {})
    crop_rows = data.get("reviewed_crop_pairs", [])
    validate_crop_decisions({"schema": crop.get("schema"), "review_complete": crop.get("review_complete"),
        "source_sha256": data["source_sha256"], "reference_sha256": data["reference_sha256"],
        "pairs": crop_rows, "summary": {"classification_counts": data["summary"].get("reviewed_crop_classification_counts"),
            "recommended_whole_work_item_reduction": data["summary"].get("confirmed_crop_reuse_pairs")}})
    if crop.get("path") != CROP_REPORT or not re.fullmatch(r"[0-9a-f]{64}", crop.get("sha256", "")):
        raise ValueError("missing immutable final crop report pointer")
    records = {r["id"]: r for r in data["canonical_drawings"]}
    if len(records) != len(data["canonical_drawings"]):
        raise ValueError("duplicate drawing ID")
    counted = {key for key, row in records.items() if row["count_in_conservative_plan"]}
    crop_by_id = {p["id"]: p for p in crop_rows}
    for pair in crop_rows:
        source, target = records[pair["from_id"]], records[pair["to_id"]]
        if source.get("crop_review_classification") != pair["classification"]:
            raise ValueError("drawing crop decision was lost")
        if pair["confirmed"]:
            if source.get("alias_of") != target["id"] or source["id"] in counted or target["id"] not in counted:
                raise ValueError("pure crop must alias directly to its counted full-body master")
        elif source["id"] not in counted or source.get("alias_of"):
            raise ValueError("a color, line or pose variant was silently merged")
        if pair["classification"] == "color_only_variant" and (source.get("work_operation") != "recolor_only" or source.get("line_drawing_required") is not False):
            raise ValueError("color-only variant is not a separate recolor operation")
    for row in records.values():
        if row["planning_status"] == "confirmed_alias":
            if row["count_in_conservative_plan"] or row.get("alias_of") not in counted:
                raise ValueError("alias must point directly to a counted master")
        if any(not isinstance(f, int) or not 0 <= f < NFRAMES for f in row["source_frames"]):
            raise ValueError("invalid representative source frame")
        for sample in row.get("source_samples", []):
            if sample["frame"] not in row["source_frames"] or sample["pts"] != timeline[sample["frame"]]["pts"]:
                raise ValueError("representative sample PTS or frame mismatch")
        for occurrence in row["occurrences"]:
            a, b = occurrence["start_frame"], occurrence["end_frame_exclusive"]
            if not isinstance(a, int) or not isinstance(b, int) or not 0 <= a < b <= NFRAMES:
                raise ValueError("malformed exposure")
            if occurrence["start_pts"] != timeline[a]["pts"] or occurrence["end_pts_exclusive"] != pts_end(timeline, b):
                raise ValueError("wrong occurrence PTS")
    if [r["frame"] for r in data["frames"]] != list(range(NFRAMES)):
        raise ValueError("all original frames must appear exactly once")
    for frame, row in enumerate(data["frames"]):
        if row["pts"] != timeline[frame]["pts"]:
            raise ValueError("wrong frame PTS")
        if not set(row["canonical_ids"] + row["candidate_ids"]) <= counted:
            raise ValueError("frame binds missing, excluded, or alias drawing")
        if row["status"] == "unresolved_candidate" and row["canonical_ids"]:
            raise ValueError("unresolved candidate cannot be a confirmed binding")
        if "candidate_ids_before_crop_review" in row:
            if row["status"] != "unresolved_candidate" or row["canonical_ids"]:
                raise ValueError("candidate remapping must not establish identity")
            expected = sorted({resolve_alias(records, x)[0] for x in row["candidate_ids_before_crop_review"]})
            if row["candidate_ids"] != expected:
                raise ValueError("candidate alias remap lost provenance")
        if "canonical_ids_before_crop_review" in row:
            expected = sorted({resolve_alias(records, x)[0] for x in row["canonical_ids_before_crop_review"]})
            if row["canonical_ids"] != expected:
                raise ValueError("known alias remap lost provenance")
            transform = row.get("transform", {})
            if transform.get("matrix") is not None:
                pair = crop_by_id.get(transform.get("crop_review_pair_id"))
                if not pair or not pair["confirmed"] or transform["matrix"] != pair["transform"]["matrix"]:
                    raise ValueError("occurrence transform does not match its pure crop evidence")
                old_frame = dict(row, transform=row.get("transform_before_crop_review", {}))
                if crop_occurrence_transform(old_frame, pair) != transform:
                    raise ValueError("camera transform was inferred outside established source-canvas scope")
    exposure_by_id = {r["id"]: r for r in data["occurrences"]}
    if len(exposure_by_id) != len(data["occurrences"]):
        raise ValueError("duplicate occurrence ID")
    for occurrence in exposure_by_id.values():
        start, stop = occurrence["start_frame"], occurrence["end_frame_exclusive"]
        if not 0 <= start < stop <= NFRAMES or not set(occurrence["canonical_ids"]) <= counted:
            raise ValueError("invalid counted occurrence")
        signature = occurrence_signature(data["frames"][start])
        expected_transform = data["frames"][start].get("transform", {"status": "source_canvas_visible_binding", "matrix": None, "mirror": "not_asserted"})
        if occurrence["transform"] != expected_transform:
            raise ValueError("occurrence transform differs from its frame bindings")
        for frame in data["frames"][start:stop]:
            if occurrence_signature(frame) != signature or frame["occurrence_ids"] != [occurrence["id"]]:
                raise ValueError("occurrence crosses a transform/provenance boundary")
    for row in data["frames"]:
        if bool(row["canonical_ids"]) != bool(row["occurrence_ids"]):
            raise ValueError("known frames must have exactly one exposure binding")
        if row["occurrence_ids"] and (len(row["occurrence_ids"]) != 1 or row["occurrence_ids"][0] not in exposure_by_id):
            raise ValueError("frame occurrence is missing")
    for record in records.values():
        if any(occurrence != exposure_by_id.get(occurrence["id"]) for occurrence in record["occurrences"]):
            raise ValueError("record occurrence diverges from the canonical exposure table")
    summary, reductions = data["summary"], data["conditional_reuse_pairs"]
    if summary["planning_count"] != len(counted) or summary["max"] != len(counted):
        raise ValueError("planning count mismatch")
    colors = sum(records[x].get("work_operation") == "recolor_only" for x in counted)
    lines = sum(records[x].get("line_drawing_required") is True for x in counted)
    if (summary.get("color_only_count") != colors or summary.get("linework_count") != lines
            or lines + colors != len(counted)):
        raise ValueError("mixed linework/recolor count mismatch")
    if summary.get("confirmed_alias_records") != sum(r["planning_status"] == "confirmed_alias" for r in records.values()):
        raise ValueError("alias record count mismatch")
    sources = [p["from_id"] for p in reductions]
    if len(set(sources)) != len(sources) or any(p["confirmed"] for p in reductions):
        raise ValueError("conditional reductions overlap or masquerade as confirmed")
    if any(p["from_id"] not in counted or p["to_id"] not in counted for p in reductions):
        raise ValueError("conditional reduction refers to absent work item")
    if summary["min"] != summary["planning_count"]-len(reductions):
        raise ValueError("conditional planning range mismatch")
    if not {"ART-D001", "ART-D002", "ART-D003"} <= counted:
        raise ValueError("confirmed missing states must remain drawing tasks")


def nominate_reprises(root: Path = ROOT) -> dict:
    """Original-only hair-normalized nominees; NOT identity or warp proof."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    if sha(root / "source/original.mp4") != SOURCE_SHA:
        raise ValueError("source video changed")
    catalog = load(root, "data/panel_catalog.json")
    references = {g: [r for r in catalog if r["group"] == g] for g in ["G12", "G13"]}
    references["G13"].append({"id": "D001", "source_image": "drawing_candidates/D001/source.png"})

    def descriptor(path):
        with Image.open(path) as opened:
            im = opened.convert("RGB")
        a = np.asarray(im.resize((480, 270))).astype(np.int16)
        r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        red = (r > 110) & (g < 100) & (b < 80) & (r-g > 60) & (r-b > 70)
        labels, _ = ndimage.label(ndimage.binary_dilation(red, iterations=1))
        counts = np.bincount(labels.ravel())
        if len(counts) < 2:
            return None, None
        counts[0] = 0
        obj = ndimage.find_objects(labels)[int(counts.argmax())-1]
        x0, x1, y0, y1 = obj[1].start*4, obj[1].stop*4, obj[0].start*4, obj[0].stop*4
        width, height, cx = x1-x0, y1-y0, (x0+x1)/2
        box = [cx-.8*width, y0-.15*height, cx+.8*width, y0+2.1*height]
        crop = im.transform((120, 120), Image.Transform.AFFINE,
            ((box[2]-box[0])/120, 0, box[0], 0, (box[3]-box[1])/120, box[1]),
            resample=Image.Resampling.BILINEAR, fillcolor=(208, 164, 169))
        a = np.asarray(crop).astype(np.int16)
        r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        classes = ((r > 110) & (g < 100) & (b < 80) & (r-g > 60) & (r-b > 70)).astype(np.uint8)
        classes += 2*((r > 225) & (g > 180) & (b > 145) & (r-g > 15) & (g-b > 2) & (r-b > 25)).astype(np.uint8)
        classes += 3*(a.max(2) < 115).astype(np.uint8)
        return classes, box

    arrays = {g: np.stack([descriptor(safe_path(root, r["source_image"]))[0] for r in rows]) for g, rows in references.items()}
    results = []
    for start, stop, group in [(2801, 2959, "G12"), (3373, 3625, "G12"), (3625, 3778, "G13")]:
        for frame in range(start, stop):
            sample, box = descriptor(safe_path(root, f"frames/F{frame:06d}.png"))
            candidates = []
            if sample is not None:
                matrix = arrays[group]
                dist = (sample != matrix).sum((1, 2)) / np.maximum(((sample > 0) | (matrix > 0)).sum((1, 2)), 1)
                candidates = [{"panel_id": references[group][int(i)]["id"], "distance": round(float(dist[i]), 6)} for i in np.argsort(dist)[:3]]
            results.append({"frame": frame, "group": group, "normalized_crop_box": box, "candidates": candidates})
    output = {"schema": "magic-maid.reprise-nomination/1", "source_sha256": SOURCE_SHA,
        "method": "Original-only120x120 hair-normalized red/skin/dark descriptor; nearest3 within documented family. D001 included. NOT identity, transform registration, or author-cel proof.",
        "ranges": [[2801, 2959], [3373, 3625], [3625, 3778]], "frames": results}
    safe_path(root, "data/reuse_reprise_candidates.json").write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return {"candidate_frames": len(results), "identity_confirmations": 0}


def native_agreement(a, b) -> dict:
    """Exact recovered ROI metric; excluding white also excludes white garments."""
    import numpy as np
    from scipy import ndimage
    a, b = a.astype(np.int16), b.astype(np.int16)
    white = ((a.min(2) > 200) & (np.ptp(a, 2) < 35)) | ((b.min(2) > 200) & (np.ptp(b, 2) < 35))
    pink = np.all(np.abs(a-np.array([208, 164, 169])) < 30, axis=2) | np.all(np.abs(b-np.array([208, 164, 169])) < 30, axis=2)
    valid = ~ndimage.binary_dilation(white, iterations=3) & ~pink
    delta = np.abs(a-b).max(2)
    measured = {"valid_native_pixels": int(valid.sum()), "pixels_delta_gt20": int(((delta > 20) & valid).sum()),
                "pixels_delta_gt64": int(((delta > 64) & valid).sum())}
    return measured


def verify_m24_pixels(root: Path = ROOT) -> dict:
    """Recheck original pixels; never extend manual review using a threshold."""
    import functools
    import numpy as np
    from PIL import Image
    data = load(root, "data/reuse_m24_review.json")
    audit = load(root, "data/drawing_coverage_audit.json")
    catalog = {r["id"]: r for r in load(root, "data/panel_catalog.json")}
    if sha(root / "source/original.mp4") != SOURCE_SHA:
        raise ValueError("original video changed")

    @functools.lru_cache(8)
    def original_rgb(frame):
        with Image.open(safe_path(root, f"frames/F{frame:06d}.png")) as im:
            array = np.asarray(im.convert("RGB"))
        if hashlib.md5(array.tobytes()).hexdigest() != audit["frames"][frame]["decoded_rgb_md5"]:
            raise ValueError("frame cache is not the verified original RGB")
        return array[180:1050, 380:1540]

    accepted = set(data["accepted_exact_frames"])
    for row in data["frame_metrics"]:
        if row["frame"] not in accepted:
            continue
        info = row["best"]
        measured = native_agreement(original_rgb(row["frame"]), original_rgb(catalog[info["panel_id"]]["source_frame"]))
        if any(info[key] != value for key, value in measured.items()):
            raise ValueError("changed native M24 correspondence metrics")
    return {"status": "pass", "native_original_frame_pairs_rechecked": len(accepted),
            "scope": "common observable geometry; white/hidden regions not certified"}


def build(root: Path = ROOT) -> dict:
    if sha(root / "source/original.mp4") != SOURCE_SHA or sha(root / "source/reference.mp4") != REFERENCE_SHA:
        raise ValueError("source attachment identity changed")
    catalog = load(root, "data/panel_catalog.json")
    timeline = load(root, "data/original_timeline.json")
    crop_review = load_crop_review(root, timeline)
    chapters = load(root, "data/chapters.json")
    audit = load(root, "data/drawing_coverage_audit.json")
    review = load(root, "data/reuse_review_evidence.json")
    if review.get("recovery_pending", False):
        raise ValueError("recovery review inputs await source revalidation")
    notes = load(root, "data/reference_notes.json")
    if len(timeline) != NFRAMES or len(audit["frames"]) != NFRAMES:
        raise ValueError("unexpected source frame count")
    chapter_for = {f: r["id"] for r in chapters for f in range(r["start_frame"], r["end_frame_exclusive"])}
    group_for = {r["id"]: re.findall(r"[GX]\d{2}", r["groups"]) for r in chapters}
    inputs = ["data/panel_catalog.json", "data/original_timeline.json", "data/chapters.json",
        "data/drawing_coverage_audit.json", "data/reference_notes.json", "data/opening_exposures.json",
        "data/reuse_review_evidence.json", "data/reuse_reprise_candidates.json", "data/reuse_m24_review.json", CROP_REPORT] + ["data/"+p for p in REVIEWS]
    records = {}
    for panel in catalog:
        pid, group = panel["id"], panel["group"]
        excluded = group in NONCHAR or pid == "G10-06"
        row = {"id": "ART-"+pid, "title": panel["title"]+" · "+pid,
            "kind": "non_character" if excluded else kind(group), "group_id": group,
            "planning_status": "excluded_non_character" if excluded else "confirmed_alias" if pid in ALIASES else "retained_drawing_task",
            "count_in_conservative_plan": not excluded and pid not in ALIASES,
            "reference_panel_ids": [pid], "source_frames": [panel["source_frame"]],
            "source_images": [panel["source_image"]], "occurrences": [],
            "notes": [panel["note"], "工作项按可见人物内容编制，不等于作者独立原画或已完成重绘。"],
            "confidence": "retained_work_item_not_unique_identity_proof",
            "evidence": ["data/panel_catalog.json", "data/reuse_review_evidence.json"],
            "author_cel_identity": None, "hidden_pixels_recovered": False}
        if excluded:
            row["exclusion_reason"] = "No visible hand; spark-only reference" if pid == "G10-06" else "background/prop/typography/FX reference; not a main-character drawing task"
        elif pid in ALIASES:
            row["alias_of"] = art(pid)
            row["confidence"] = "reviewed_common_visible_art_only_hidden_regions_unknown"
            row["notes"].append("保留原编号；已核对的可见人物复用不新增稿。独立特效、文字和遮挡后信息不合并。")
        if group == "G47":
            row["notes"].append("原尺寸核对保留8种不同头发/眼睛/头饰线态；同一画面复制1/2/3个头像不增加张数。")
        if group == "G32":
            row["notes"].append("此项仅指新出现的第%d种头部，不重画前面已出现的头像。" % int(pid[-2:]))
        records[row["id"]] = row
    for alias, master in ALIASES.items():
        dest, source = records["ART-"+master], records["ART-"+alias]
        for key in ["reference_panel_ids", "source_frames", "source_images"]:
            dest[key] += source[key]
    for supplement in audit["supplemental_observed_states"]:
        if supplement["status"] != "confirmed_missing_visible_drawing_state":
            continue
        sid = supplement["id"]
        records["ART-"+sid] = {"id": "ART-"+sid, "title": supplement["title_zh"],
            "kind": "half_body" if sid == "D001" else "body_pose", "group_id": "G13" if sid == "D001" else "G51",
            "planning_status": "confirmed_gap_supplement", "count_in_conservative_plan": True,
            "reference_panel_ids": [], "source_frames": [supplement["source_frame"]], "source_images": [supplement["source_png"]],
            "occurrences": [], "notes": [supplement["finding_zh"]], "author_cel_identity": None, "hidden_pixels_recovered": False,
            "confidence": "confirmed_missing_visible_state_independently_cross_checked", "evidence": ["data/drawing_coverage_audit.json"]}
    samples = {p["source_image"]: {"frame": p["source_frame"], "pts": p["source_pts"], "image": p["source_image"]} for p in catalog}
    samples.update({p["source_png"]: {"frame": p["source_frame"], "pts": p["source_pts"], "image": p["source_png"]} for p in audit["supplemental_observed_states"]})
    for row in records.values():
        row["source_frames"] = sorted(set(row["source_frames"]))
        row["source_samples"] = [samples[name] for name in row["source_images"]]
    frames = []
    for raw in audit["frames"]:
        frame = raw["frame"]
        ids = sorted({did for pid in raw["exact_catalog_ids"] for did in panel_art_ids(pid, records)})
        nearest = raw.get("triage_nearest_catalog_id")
        family = ["G12"] if 2801 <= frame < 2959 or 3373 <= frame < 3625 else ["G13"] if 3625 <= frame < 3778 else group_for[chapter_for[frame]]
        candidates = panel_art_ids(nearest, records) if nearest and nearest.split("-")[0] in family else []
        frames.append({"frame": frame, "pts": raw["pts"], "chapter_id": chapter_for[frame],
            "status": "known_visible_state" if ids else "unresolved_candidate", "canonical_ids": ids,
            "candidate_ids": [] if ids else candidates, "candidate_family_ids": family, "occurrence_ids": [],
            "evidence": "native_RGB_catalog_identity" if ids else "source_descriptor_nomination_not_identity",
            "composition_representative_frame": raw["composition_representative_frame"],
            "exact_composition_repeat": raw["composition_representative_frame"] != frame,
            "source_locator": f"source/original.mp4#frame={frame}", "hidden_regions_resolved": False})
    for a, b in NO_CHARACTER:
        for row in frames[a:b]:
            if not row["canonical_ids"]:
                row.update(status="no_visible_character", candidate_ids=[], evidence="documented_source_scene_scope")
    for row in frames[2153:2278]:
        row.update(status="prop_or_emblem_only", canonical_ids=[], candidate_ids=[], evidence="G30_G31_accessory_portrait_optional_not_main_character_task")
    frames[1821].update(status="occluded_unobservable", canonical_ids=[], candidate_ids=[], evidence="native_black_reveal_sheet_F1821_fully_covered")
    for name in REVIEWS:
        for interval in flatten_intervals(load(root, "data/"+name)):
            a, b = interval["start_frame"], interval["end_frame_exclusive"]
            if not 0 <= a < b <= NFRAMES:
                raise ValueError("invalid bounded review exposure")
            pid, supplement = interval.get("catalog_panel_id"), interval.get("supplemental_observed_state_id")
            ids = ["ART-"+supplement] if supplement else panel_art_ids(pid, records) if pid else []
            label = str(interval.get("visible_state_label", ""))+str(interval.get("change_class", ""))
            for row in frames[a:b]:
                if audit["frames"][row["frame"]].get("review_identity_uncertainty") and not row["canonical_ids"]:
                    row.update(status="unresolved_candidate", canonical_ids=[], candidate_ids=ids, evidence="data/"+name)
                elif ids:
                    row.update(status="known_visible_state", canonical_ids=ids, candidate_ids=[], evidence="data/"+name)
                else:
                    state = "occluded_unobservable" if any(x in label for x in ["full_cover", "fully_occluded", "unobservable"]) else "no_visible_character"
                    row.update(status=state, canonical_ids=[], candidate_ids=[], evidence="data/"+name)
    for interval in load(root, "data/opening_exposures.json")["rows"]:
        for row in frames[interval["start_frame"]:interval["end_frame_exclusive"]]:
            row.update(status="known_visible_state", canonical_ids=[art(interval["state"])], candidate_ids=[], evidence="data/opening_exposures.json")
    for candidate in load(root, "data/reuse_reprise_candidates.json")["frames"]:
        row = frames[candidate["frame"]]
        if row["canonical_ids"]:
            continue
        ids = list(dict.fromkeys(art(c["panel_id"]) for c in candidate["candidates"]))
        row.update(status="unresolved_candidate", candidate_ids=ids,
            evidence="attachment2_family_guidance_and_normalized_original_pixels_not_identity",
            transform={"status": "candidate_only", "operations": ["scale", "translation", "crop"], "matrix": None, "mirror": "not_asserted"})
    m24 = load(root, "data/reuse_m24_review.json")
    if m24.get("recovery_pending", False):
        raise ValueError("M24 needs restored-source revalidation")
    accepted, reviewed = set(m24["accepted_exact_frames"]), set(m24["manual_reviewed_panel_ids"])
    for check in m24["frame_metrics"]:
        if check["frame"] not in accepted:
            continue
        best = check["best"]
        if not best or not best["candidate_threshold_pass"] or best["panel_id"] not in reviewed:
            raise ValueError("native threshold alone or unreviewed M24 state cannot establish reuse")
        frames[check["frame"]].update(status="known_visible_state", canonical_ids=[art(best["panel_id"])], candidate_ids=[],
            evidence="data/reuse_m24_review.json", transform={"status": "observed_same_source_canvas_geometry",
                "operations": [], "matrix": [[1,0,0],[0,1,0],[0,0,1]], "mirror": False},
            reuse_scope="common visible character geometry; not caption-covered/white/hidden-pixel recovery")
    for frame in m24["no_character_reviewed_frames"]:
        frames[frame].update(status="no_visible_character", canonical_ids=[], candidate_ids=[], evidence="data/reuse_m24_review.json")
    reductions = integrate_crop_review(records, frames, crop_review)
    occurrences, seen, index = [], set(), 0
    while index < NFRAMES:
        row = frames[index]
        if not row["canonical_ids"]:
            index += 1
            continue
        stop = index+1
        while stop < NFRAMES and occurrence_signature(frames[stop]) == occurrence_signature(row):
            stop += 1
        oid = f"O{len(occurrences)+1:04d}"
        repeat = all(did in seen for did in row["canonical_ids"])
        occurrence = {"id": oid, "chapter_id": row["chapter_id"], "start_frame": index, "end_frame_exclusive": stop,
            "start_pts": timeline[index]["pts"], "end_pts_exclusive": pts_end(timeline, stop),
            "canonical_ids": row["canonical_ids"], "status": "reused_visible_drawing" if repeat else "first_observed_exposure",
            "confidence": "bounded_visible_binding_not_hidden_or_author_cel_identity",
            "transform": row.get("transform", {"status": "source_canvas_visible_binding", "matrix": None, "mirror": "not_asserted"}),
            "evidence": sorted({e for f in frames[index:stop] for e in [f["evidence"], *f.get("crop_review_evidence", [])]}),
            "source_art_ids_before_crop_review": sorted({did for f in frames[index:stop]
                for did in f.get("canonical_ids_before_crop_review", f["canonical_ids"])}),
            "crop_review_pair_ids": sorted({pid for f in frames[index:stop] for pid in f.get("crop_review_pair_ids", [])}),
            "author_cel_identity": None}
        occurrences.append(occurrence)
        for did in row["canonical_ids"]:
            records[did]["occurrences"].append(occurrence)
            seen.add(did)
        for f in frames[index:stop]:
            f["status"], f["occurrence_ids"] = occurrence["status"], [oid]
            f["exposure_role"] = "exposure_start" if f["frame"] == index else "held_exposure"
        index = stop
    for row in records.values():
        if row["planning_status"] == "confirmed_alias":
            row["occurrences"] = records[row["alias_of"]]["occurrences"]
    counted = [r for r in records.values() if r["count_in_conservative_plan"]]
    n = len(counted)
    color_count = sum(r["work_operation"] == "recolor_only" for r in counted)
    linework_count = sum(r["line_drawing_required"] for r in counted)
    classification_counts = copy.deepcopy(crop_review["summary"]["classification_counts"])
    gap_count = sum(r["planning_status"] == "confirmed_gap_supplement" for r in records.values())
    data = {"schema": "magic-maid.reuse/2", "source_video": "source/original.mp4", "source_sha256": SOURCE_SHA,
        "reference_video": "source/reference.mp4", "reference_sha256": REFERENCE_SHA,
        "reference_role": "guidance_only_never_production_pixels", "time_base": "1/16000", "frame_count": NFRAMES,
        "all_author_drawings_proven_complete": False, "automatic_unverified_pixel_reuse": False,
        "count_unit": "main-character visible work items: linework tasks plus color-only operations, not new full-body drawings or author cels",
        "kind_definitions": {"body_pose": "整体人物动作稿；包括抱膝、坐姿、桌面/被窝遮挡，不等于完整站姿或保证可见双脚。",
            "half_body": "半身/胸像及手臂动作稿，以原图可见范围为准。", "head_detail": "头部/面部局部，部分含贴近面部的手。",
            "hand_detail": "手部局部；盒/蝴蝶结另层。", "mouth_detail": "嘴部与邻近轮廓局部。"},
        "summary": {"planning_count": n, "min": n-len(reductions), "max": n,
            "linework_count": linework_count, "color_only_count": color_count,
            "linework_kind_counts": dict(sorted(Counter(r["kind"] for r in counted if r["line_drawing_required"]).items())),
            "work_operation_counts": dict(sorted(Counter(r["work_operation"] for r in counted).items())),
            "reviewed_crop_classification_counts": classification_counts,
            "confirmed_crop_reuse_pairs": classification_counts["confirmed_crop_reuse"],
            "reviewed_crop_pairs": len(crop_review["pairs"]),
            "kind_counts": dict(sorted(Counter(r["kind"] for r in counted).items())), "catalog_compositions": len(catalog),
            "raw_character_candidates_including_three_gaps": sum(p["group"] not in NONCHAR for p in catalog)+gap_count,
            "confirmed_alias_records": sum(r["planning_status"] == "confirmed_alias" for r in records.values()),
            "excluded_non_character_records": sum(r["planning_status"] == "excluded_non_character" for r in records.values()),
            "conditional_reuse_pairs": len(reductions), "confirmed_gap_tasks": gap_count,
            "observed_exposures": len(occurrences), "reused_observed_exposures": sum(r["status"] == "reused_visible_drawing" for r in occurrences),
            "frame_status_counts": dict(Counter(r["status"] for r in frames)), "range_is_absolute_completeness_bound": False,
            "range_assumptions": ["当前保守工作项由含绘线项与仅改色操作组成；不是必须从零重画或全身稿数。",
                f"已完成原片裁切审查：仅{classification_counts['confirmed_crop_reuse']}对纯裁切去整稿重计；改色、改线与手势变体继续列为工作项。",
                "字幕、花瓣、橙色/黑白转场、幽灵、背景和道具另轨不计人物张数。",
                "未决原片状态仍保留，后续如果确认是新可见稿，张数需上调；max不是全片真正上限。"],
            "optional_additional_tasks": [{"id": "OPT-BROOCH-PORTRAIT", "count": 1, "scope": "若胸针肖像也换成新角色，则另加1个小头像；本轮主人物计数未包含饰物肖像。"}]},
        "reference_directives": notes, "alias_policy": {**review["alias_policy"],
            "crop_policy": "Only completed, visually reviewed pure crop decisions become aliases; color/local-line/pose variants remain work items; alias chains flatten to counted masters."},
        "conditional_reuse_pairs": reductions, "reviewed_crop_pairs": copy.deepcopy(crop_review["pairs"]),
        "crop_reuse_report": {"path": CROP_REPORT, "sha256": sha(safe_path(root, CROP_REPORT)),
            "schema": crop_review["schema"], "review_complete": True},
        "reuse_families": copy.deepcopy(review["reuse_families"]), "canonical_drawings": list(records.values()),
        "occurrences": occurrences, "frames": frames, "input_sha256": {name: sha(safe_path(root, name)) for name in inputs},
        "limitations": ["灰衣白色幽灵遮住的手/盘边不是恢复像素；相近但未证实的线态仍单列。",
            "G47原尺寸已确认8种头部态；不能把闭眼或开眼相同误当同稿。",
            "G12/G33不是整组一对一：中间32–45和尾部68–75仍有不同手势/头身组合。",
            "M24的235帧经过47态配对目视与逐帧原尺寸共同可见区检查；F3449仍未决，尾16帧无人物。M21/M25等变换后对应仅候选，禁止直接自动套用。",
            "原411构图快照、三个确证补漏与83个审计源样本均未删除。"]}
    for family in data["reuse_families"]:
        if family["id"] == "RF-CROSS":
            family.update(status="original_source_crop_review_complete_bounded_visible_geometry",
                evidence=CROP_REPORT, classification_counts=classification_counts,
                note_zh="纯裁切合并；改色、局部改线与手势变体仍保留工作项。不是全组一对一。")
    validate(data, timeline)
    safe_path(root, "data/reuse_manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    write_report(root, data)
    return data


def write_report(root: Path, data: dict) -> None:
    summary = data["summary"]
    c = summary["reviewed_crop_classification_counts"]
    names = {"body_pose": "整体人物动作（含坐姿、裁切或遮挡）", "half_body": "半身/胸像动作",
        "head_detail": "头部局部", "hand_detail": "手部局部", "mouth_detail": "嘴部局部"}
    lines = ["# 人物复用与绘制任务数", "",
        f"**当前保守工作量：{summary['planning_count']}项＝{summary['linework_count']}项含绘线工作＋{summary['color_only_count']}项仅校色操作。**", "",
        "这不是同数量的全身稿，也不是全部必须从零新画。含绘线工作包含局部衣纹、袖口和手势变体；可复用的头脸和主体应继续复用。",
        f"当前已裁定工作项范围为{summary['min']}–{summary['max']}项；它只是现有已编目工作范围，不是作者原画完整性上下限。未决原片状态以后若证实新稿，仍需追加。", "",
        "## 原片半身是否从全身裁切", "",
        f"已逐对核查{summary['reviewed_crop_pairs']}组原片G12/G33对应：", "",
        "| 原片审查结果 | 对数 | 执行动作 |", "|---|---:|---|",
        f"| 纯等比放大、平移及裁切 | {c['confirmed_crop_reuse']} | 全身母稿复用；半身不再新增整稿工作项 |",
        f"| 线形一致，仅局部填色不同 | {c['color_only_variant']} | 保留校色操作；不计新增线稿 |",
        f"| 局部衣纹/袖口/腰结线不同 | {c['local_line_variant']} | 保留局部改线任务，未变主体可复用 |",
        f"| 手势或双臂姿态不同 | {c['different_pose']} | 保留动作变体，不用非刚性变形冒充裁切 |",
        f"| 遮挡等原因仍未定 | {c['occlusion_uncertain']} | 保留候选，不自动合并 |", "",
        "结论是存在大量同源裁切，但不能整组照搬。统一几何配准不等于整张线稿完全一致；背景、字幕或相同头像不能替代对手指、手臂、衣纹的检查。",
        "[完整原片审查报告](data/crop_reuse_report.md)记录逐对源帧/PTS、变换、可复用区域、需改区域和实际证据；独立复核覆盖21个抽样配对，不冒称49对全部双重独立审查。", "",
        "## 按人物可见范围分配", "",
        "下表是混合工作项（包括仅校色），局部稿不等于全身稿工时。", "",
        "| 类型 | 当前工作项 | 含绘线项 |", "|---|---:|---:|"]
    for key, value in summary["kind_counts"].items():
        lines.append(f"| {names.get(key, key)} | {value} | {summary['linework_kind_counts'].get(key, 0)} |")
    lines += ["", "## ID、原图与时序保持", "",
        "- 保留所有原G/X编号、源样本、精确PTS和D001/D002/D003三个确证补漏；没有删原稿、改原视频或改冻结alpha。",
        "- 已核准纯裁切项的`alias_of`直接指向计数中的G33母稿；原G12内部别名链也展开到最终母稿，不形成别名指向别名。",
        "- `canonical_drawings`中`count_in_conservative_plan=true`表示工作项；`line_drawing_required`与`work_operation=recolor_only`区分绘线和校色。",
        "- 变体的`work_scope`、`partial_reuse_scope`、`redraw_regions`及`color_adjustment_regions`明确剩余工作；区域框只是审查定位，不是可直接投产蒙版。",
        "- `reviewed_crop_pairs`保留全部正式裁定和证据；`conditional_reuse_pairs`只保留真正仍未定的配对，不把已裁定反例继续说成待核准减量。",
        "- 4763帧的规范ID和候选ID已按母稿重映射，但未决状态保持未决。仅原G12有界源画布曝光和已确证同画布M24曝光附上裁切矩阵；未建立摄影机关系的镜头不猜变换。",
        "- M24原有235帧的同画布证明可与裁切矩阵组合；F3449继续未决，F3609–3624无人物；M21/M25等未决候选不能因此变成确认复用。",
        "- 不同变换或源ID链的曝光分别分组，帧号、PTS及旧规范ID定位保留。", "",
        "## 附件2指导与证据边界", "",
        "N04『这部分后面有全身动作』用于指导检索，不是逐对复用保证；N01/N02指导循环，N03/N06的单帧指素材，N05『重复动作未计入』位于G13手势段。附件2像素没有用于生产或原片配准。音轨未听，不能声称作者口头批准全部复用。",
        "[画面指令核查记录](data/REFERENCE_REUSE_INSTRUCTION_CHECK.json)。原片可见画面不能证明画外腿脚、裙摆、被挡手指或作者原始cel身份。", "",
        "## 可执行工作单", "",
        "- [复用清单](data/reuse_manifest.json)：全部4763原片帧、计数母稿、别名、变体、曝光和未决状态。",
        "- [复核结果](data/REUSE_VERIFICATION.json)：源文件、证据哈希、别名/计数/时序约束及测试。",
        "- [工作分包](work_sections/README.md)：完整黑裙舞蹈归s06，红裙动作归s14；按最终规范ID全局分配一次。", "",
        "字幕、花瓣、幽灵、星芒、变装色块、黑白转场、背景、茶具/盒/框等另轨制作，不混入人物工作项；若胸针小肖像也换新角色，另加1个局部头像。", "",
        "## 曝光不是新画张数", "",
        f"当前有{summary['observed_exposures']}段有证据的可见绑定，其中{summary['reused_observed_exposures']}段再次绑定到此前已观察的母稿。它们不是同数量的独立动作套数；未决帧也不等于已经确定要新画。", ""]
    safe_path(root, "复用与绘制任务说明.md").write_text("\n".join(lines), encoding="utf-8")


def verify(root: Path = ROOT) -> dict:
    data = load(root, "data/reuse_manifest.json")
    validate(data, load(root, "data/original_timeline.json"))
    for name, expected in data["input_sha256"].items():
        if sha(safe_path(root, name)) != expected:
            raise ValueError("changed reuse input: "+name)
    if sha(safe_path(root, data["source_video"])) != SOURCE_SHA or sha(safe_path(root, data["reference_video"])) != REFERENCE_SHA:
        raise ValueError("source video changed")
    if sha(safe_path(root, CROP_REPORT)) != data["crop_reuse_report"]["sha256"]:
        raise ValueError("final crop report changed")
    crop_report = load(root, CROP_REPORT)
    validate_crop_decisions(crop_report)
    if data["reviewed_crop_pairs"] != crop_report["pairs"]:
        raise ValueError("manifest crop decisions differ from the immutable report")
    crop_assets = verify_crop_assets(root, crop_report, load(root, "data/original_timeline.json"))
    originals = {p["source_image"]: p["source_png_sha256"] for p in load(root, "data/panel_catalog.json")}
    originals.update({p["source_png"]: p["png_sha256"] for p in load(root, "data/drawing_coverage_audit.json")["supplemental_observed_states"]})
    checked = set()
    for row in data["canonical_drawings"]:
        for name in row["source_images"]:
            path = safe_path(root, name)
            if name not in originals or not path.is_file():
                raise ValueError("missing or non-original source image")
            if name not in checked and sha(path) != originals[name]:
                raise ValueError("source image was modified")
            checked.add(name)
    for item in load(root, "data/reuse_review_evidence.json")["evidence_files"]:
        if sha(safe_path(root, item["path"])) != item["sha256"]:
            raise ValueError("reuse evidence image changed")
    return {"status": "pass", "frame_count": len(data["frames"]), "planning_count": data["summary"]["planning_count"],
            "linework_count": data["summary"]["linework_count"], "color_only_count": data["summary"]["color_only_count"],
            "manifest_sha256": sha(root / "data/reuse_manifest.json"), "crop_report_sha256": data["crop_reuse_report"]["sha256"],
            "source_image_files_verified": len(checked), "crop_asset_verification": crop_assets,
            "all_author_drawings_complete": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify", "nominate-reprises", "verify-m24-pixels"])
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = (build(args.root)["summary"] if args.command == "build" else nominate_reprises(args.root) if args.command == "nominate-reprises"
              else verify_m24_pixels(args.root) if args.command == "verify-m24-pixels" else verify(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
