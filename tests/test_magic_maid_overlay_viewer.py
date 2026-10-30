"""Dependency-free fixture/contract tests, not browser or semantic-alpha QA."""
from __future__ import annotations

import copy
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("overlay_viewer", REPO / "scripts/magic_maid_overlay_viewer.py")
viewer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(viewer)
W, H = 1920, 1080


def png_bytes(raw: bytes, channels: int) -> bytes:
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    stride = W * channels
    filtered = b"".join(b"\0" + raw[y * stride:(y + 1) * stride] for y in range(H))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6 if channels == 4 else 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(filtered, 6)) + chunk(b"IEND", b"")


def rectangle_rgba(box, color):
    rgba = bytearray(W * H * 4)
    if box:
        x0, y0, x1, y1 = box
        row = bytes(color) * (x1 - x0)
        for y in range(y0, y1):
            start = (y * W + x0) * 4
            rgba[start:start + len(row)] = row
    return bytes(rgba)


def fixture(root: Path, write: bool = True):
    """Eight synthetic frames, two disjoint S packages, four M cuts, four records."""
    root.mkdir(parents=True, exist_ok=True)
    for folder in ("data", "frames", "cels/DEMO-A", "cels/DEMO-B"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    assets = {"subtitles": {}, "effects": {}}
    def asset(category, box, color):
        raw = rectangle_rgba(box, color)
        digest = hashlib.sha256(raw).hexdigest()
        encoded = png_bytes(raw, 4)
        relative = f"overlay_assets/{category}/{digest}.png"
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encoded)
        pixels = (box[2] - box[0]) * (box[3] - box[1]) if box else 0
        assets[category][digest] = {"path": relative, "rgba_sha256": digest, "png_sha256": hashlib.sha256(encoded).hexdigest(), "bytes": len(encoded), "nonzero_alpha_pixels": pixels, "partial_alpha_pixels": pixels if 0 < color[3] < 255 else 0, "opaque_pixels": pixels if color[3] == 255 else 0, "bbox": box}
        return digest
    subtitle_empty = asset("subtitles", None, (0, 0, 0, 0))
    subtitle_text = asset("subtitles", [200, 850, 1720, 900], (255, 255, 255, 160))
    effect_empty = asset("effects", None, (0, 0, 0, 0))
    effect_visible = asset("effects", [1200, 200, 1300, 500], (240, 40, 130, 128))
    rgb = bytes((190, 150, 165)) * (W * H)
    original_png = png_bytes(rgb, 3)
    for relative in ("frames/F000000.png", "cels/DEMO-A/source.png", "cels/DEMO-B/source.png"):
        (root / relative).write_bytes(original_png)
    durations = [528, 544, 528, 528, 544, 528, 544, 528]
    frames, pts = [], 0
    for frame, duration in enumerate(durations):
        sub = subtitle_text if frame in (0, 1, 4, 7) else subtitle_empty
        fx = effect_visible if frame in (2, 3, 4, 7) else effect_empty
        frames.append({"frame": frame, "pts": pts, "duration_ticks": duration, "chapter_id": f"M{frame // 2 + 1:02d}", "group": "DEMO", "original_frame": f"frames/F{frame:06d}.png", "source_png_sha256": hashlib.sha256(original_png).hexdigest(), "source_rgb_sha256": hashlib.sha256(rgb).hexdigest(), "overlays": {"subtitles": {"asset_id": sub if frame != 6 else None, "status": "unsupported_scene" if frame == 6 else "synthetic_fixture_only", "requires_review": True, "metadata": {"notice": "测试条块，不是原片字幕", "unsafe_test": "</script><script>alert('x')</script>"}}, "effects": {"asset_id": fx, "status": "synthetic_fixture_only", "requires_review": True, "metadata": {"notice": "测试条块，不是原片特效", "subtitle_relation": "above_subtitles" if frame in (2, 3, 7) else "mixed_or_uncertain" if frame == 4 else "below_subtitles" if frame in (0, 1) else "unknown", "recommended_stack_position": "above_subject"}}}})
        pts += duration
    overlay = {"schema": viewer.SCHEMA, "synthetic_fixture": True, "dimensions": [W, H], "time_base": "1/16000", "frame_count": len(frames), "video_duration_ticks": pts, "alpha_mode": "straight", "assets": assets, "frames": frames}
    def occurrence(oid, start, end, status):
        return {"id": oid, "chapter_id": frames[start]["chapter_id"], "start_frame": start, "end_frame_exclusive": end, "start_pts": frames[start]["pts"], "end_pts_exclusive": frames[end]["pts"] if end < 8 else pts, "status": status, "transform": {"type": "synthetic_fixture", "matrix": None}, "evidence": ["UI fixture only"]}
    drawings = [
        {"id": "DEMO-A", "title": "跨剪辑动作（测试）", "kind": "body_pose", "planning_status": "synthetic_planned", "count_in_conservative_plan": True, "source_frames": [0], "source_images": ["cels/DEMO-A/source.png"], "source_samples": [{"frame": 0, "pts": 0, "image": "cels/DEMO-A/source.png"}], "occurrences": [occurrence("EXP-A-1", 0, 2, "first_observed_exposure"), occurrence("EXP-A-2", 4, 6, "reused_visible_drawing")], "notes": ["仅供离线 UI 测试。"]},
        {"id": "DEMO-B", "title": "口型局部（测试）", "kind": "mouth_detail", "planning_status": "synthetic_planned", "count_in_conservative_plan": True, "source_frames": [3], "source_images": ["cels/DEMO-B/source.png"], "occurrences": [occurrence("EXP-B-1", 2, 4, "first_observed_exposure")], "notes": []},
        {"id": "DEMO-ALIAS", "title": "测试别名", "kind": "body_pose", "planning_status": "confirmed_alias", "count_in_conservative_plan": False, "alias_of": "DEMO-A", "source_frames": [0], "source_images": ["cels/DEMO-A/source.png"], "occurrences": [], "notes": ["不重复计数"]},
        {"id": "DEMO-C", "title": "未确认候选（测试）", "kind": "head_detail", "planning_status": "candidate_unresolved", "count_in_conservative_plan": False, "source_frames": [4], "source_images": ["drawing_audit/DEMO-C/source.png"], "occurrences": [], "notes": ["故意保留缺图，用于异常检查"]},
    ]
    reuse_frames = []
    for f in frames:
        i = f["frame"]
        reuse_frames.append({"frame": i, "pts": f["pts"], "chapter_id": f["chapter_id"], "status": "synthetic_only", "canonical_ids": ["DEMO-A"] if i in (0, 1, 4, 5) else ["DEMO-B"] if i in (2, 3) else [], "candidate_ids": ["DEMO-C"] if i == 4 else [], "candidate_family_ids": ["DEMO-FAMILY"] if i == 6 else [], "occurrence_ids": [], "evidence": ["合成测试，不是原片结果"]})
    reuse = {"canonical_drawings": drawings, "frames": reuse_frames, "summary": {"planning_count": 2, "kind_counts": {"body_pose": 1, "mouth_detail": 1}}, "conditional_reuse_pairs": [{"id": "DEMO-CROSS-01", "from_id": "DEMO-A", "to_id": "DEMO-C", "confirmed": False, "status": "candidate_only", "matrix": None, "reason": "测试条件对，不计确认复用"}]}
    sections = []
    mapping = [None] * 8
    for sid, title, spans, new, reused, candidates in [("S01", "整段跨镜头动作（测试）", [(0, 2), (4, 6)], ["DEMO-A"], ["DEMO-A"], ["DEMO-C"]), ("S02", "细节段（测试）", [(2, 4), (6, 8)], ["DEMO-B"], [], [])]:
        ranges, local_frame, local_pts = [], 0, 0
        for start, end in spans:
            sp, ep = frames[start]["pts"], frames[end]["pts"] if end < 8 else pts
            ranges.append({"start_frame": start, "end_frame_exclusive": end, "start_pts": sp, "end_pts_exclusive": ep, "local_start_frame": local_frame, "local_start_pts": local_pts})
            for index in range(start, end):
                mapping[index] = sid
            local_frame += end - start
            local_pts += ep - sp
        sections.append({"id": sid, "title": title, "ranges": ranges, "new_drawing_ids": new, "new_drawing_count": len(new), "new_kind_counts": {"body_pose" if sid == "S01" else "mouth_detail": 1}, "reused_drawing_ids": reused, "reused_drawing_count": len(reused), "observed_reused_drawing_ids": reused, "observed_reused_drawing_count": len(reused), "observed_reused_exposure_ids": ["EXP-A-2"] if reused else [], "observed_reused_exposure_count": 1 if reused else 0, "conditional_reuse_pair_ids": ["DEMO-CROSS-01"] if candidates else [], "candidate_drawing_ids": candidates})
    work = {"sections": sections, "frame_sections": mapping}
    catalog = [{"id": "DEMO-B", "source_frame": 3, "source_image": "cels/DEMO-B/source.png"}]
    if write:
        for name, content in (("overlay_manifest", overlay), ("reuse_manifest", reuse), ("work_sections", work), ("panel_catalog", catalog)):
            (root / "data" / (name + ".json")).write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return overlay, reuse, work, catalog


class ViewerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = tempfile.TemporaryDirectory(prefix="overlay-viewer-fixture-")
        cls.fixture_root = Path(cls.base.name)
        cls.inputs = fixture(cls.fixture_root)

    @classmethod
    def tearDownClass(cls):
        cls.base.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="overlay-viewer-test-")
        self.root = Path(self.tmp.name)
        shutil.copytree(self.fixture_root, self.root, dirs_exist_ok=True)
        self.o, self.r, self.s, self.c = copy.deepcopy(self.inputs)

    def tearDown(self):
        self.tmp.cleanup()

    def payload(self, **kwargs):
        return viewer.prepare_payload(self.root, self.o, self.r, self.s, self.c, **kwargs)

    def test_valid_exact_timing_counts_and_sources(self):
        p = self.payload(verify_assets=True)
        self.assertEqual(p["planning_count"], 2)
        self.assertEqual(p["kind_counts"], {"body_pose": 1, "mouth_detail": 1})
        self.assertEqual(p["frames"][4]["local_frame"], 2)
        self.assertEqual(p["frames"][4]["local_pts"], 1072)
        self.assertEqual([x["path"] for x in p["frames"][3]["sources"]], ["frames/F000003.png", "cels/DEMO-B/source.png"])
        self.assertEqual([x["path"] for x in p["frames"][2]["sources"]], ["frames/F000002.png"])

    def test_ordered_frames_required(self):
        self.o["frames"][0], self.o["frames"][1] = self.o["frames"][1], self.o["frames"][0]
        with self.assertRaisesRegex(ValueError, "ordered"):
            self.payload()

    def test_no_missing_frame(self):
        self.o["frames"].pop()
        with self.assertRaisesRegex(ValueError, "frame_count"):
            self.payload()

    def test_pts_contiguous_and_end_exact(self):
        self.o["frames"][2]["pts"] += 1
        with self.assertRaisesRegex(ValueError, "PTS"):
            self.payload()
        self.o = copy.deepcopy(self.inputs[0])
        self.o["video_duration_ticks"] += 1
        with self.assertRaisesRegex(ValueError, "Final frame"):
            self.payload()

    def test_alpha_must_be_straight(self):
        self.o["alpha_mode"] = "premultiplied"
        with self.assertRaisesRegex(ValueError, "straight"):
            self.payload()

    def test_bad_alpha_counts_and_bbox(self):
        a = next(iter(self.o["assets"]["subtitles"].values()))
        a["partial_alpha_pixels"] = 1
        with self.assertRaisesRegex(ValueError, "alpha counts"):
            self.payload()
        self.o = copy.deepcopy(self.inputs[0])
        a = next(a for a in self.o["assets"]["subtitles"].values() if a["nonzero_alpha_pixels"])
        a["bbox"][2] = W + 1
        with self.assertRaisesRegex(ValueError, "bbox"):
            self.payload()

    def test_path_traversal_and_remote_paths(self):
        for path in ("../source.png", "/tmp/a.png", "https://x/a.png", "cels/../a.png", "cels/%2e%2e/a.png", "cels\\a.png", "cels//a.png", "cels/a.png?x", "cels/a\x00.png"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                viewer.safe_relative(self.root, path, ".png")

    def test_content_hash_filename_enforced(self):
        next(iter(self.o["assets"]["subtitles"].values()))["path"] = "overlay_assets/a.png"
        with self.assertRaisesRegex(ValueError, "content-addressed"):
            self.payload()

    def test_missing_asset_is_explicit_not_silent(self):
        a = next(iter(self.o["assets"]["subtitles"].values()))
        (self.root / a["path"]).unlink()
        p = self.payload()
        self.assertEqual(p["warning_count"], 1)
        self.assertIn(a["path"], p["warnings"][0])
        self.assertFalse(p["assets"]["subtitles"][a["rgba_sha256"]]["present_at_build"])

    def test_unknown_asset_reference_rejected(self):
        self.o["frames"][0]["overlays"]["subtitles"]["asset_id"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "Unknown"):
            self.payload()

    def test_rgba_png_required_and_checksum_option(self):
        a = next(iter(self.o["assets"]["subtitles"].values()))
        source = (self.root / "frames/F000000.png").read_bytes()
        (self.root / a["path"]).write_bytes(source)
        a["bytes"] = len(source)
        with self.assertRaisesRegex(ValueError, "RGBA"):
            self.payload()
        self.o = copy.deepcopy(self.inputs[0])
        shutil.copytree(self.fixture_root / "overlay_assets", self.root / "overlay_assets", dirs_exist_ok=True)
        next(iter(self.o["assets"]["subtitles"].values()))["png_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            self.payload(verify_assets=True)

    def test_exact_original_no_nearest(self):
        self.o["frames"][2]["original_frame"] = "frames/F000003.png"
        with self.assertRaisesRegex(ValueError, "exact frame"):
            self.payload()

    def test_no_reference_pixels_as_source(self):
        self.r["canonical_drawings"][1]["source_images"] = ["reference_frames/F000003.png"]
        with self.assertRaisesRegex(ValueError, "Non-production"):
            self.payload()

    def test_source_directories_cannot_smuggle_reference_or_other_pngs(self):
        for category in ("cels", "drawing_audit", "drawing_candidates"):
            for tail in ("reference.png", "preview.png", "nested/source.png", "source.PNG"):
                path = f"{category}/DEMO/{tail}"
                drawing = {"source_samples": [{"frame": 3, "pts": self.o["frames"][3]["pts"], "image": path}]}
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, "never reference.png"):
                    viewer.validate_drawing_source(self.root, drawing, 3, path, self.o["frames"][3]["pts"])
        self.c = [{"id": "DEMO-B", "source_frame": 3, "source_image": "cels/DEMO-B/reference.png"}]
        with self.assertRaisesRegex(ValueError, "never reference.png"):
            self.payload()

    def test_source_samples_authoritative(self):
        self.r["canonical_drawings"][0]["source_frames"] = [7]
        p = self.payload()
        self.assertIn("cels/DEMO-A/source.png", [x["path"] for x in p["frames"][0]["sources"]])
        self.assertNotIn("cels/DEMO-A/source.png", [x["path"] for x in p["frames"][7]["sources"]])

    def test_drawing_candidates_only_accept_explicit_exact_samples(self):
        drawing = self.r["canonical_drawings"][1]
        path = "drawing_candidates/D001/source.png"
        drawing["source_images"] = [path]
        with self.assertRaisesRegex(ValueError, "exact-frame/PTS"):
            self.payload()
        drawing["source_samples"] = [{"frame": 3, "pts": self.o["frames"][3]["pts"], "image": path}]
        payload = self.payload()
        self.assertIn(path, [s["path"] for s in payload["frames"][3]["sources"]])
        self.assertNotIn(path, [s["path"] for s in payload["frames"][2]["sources"]])
        drawing["source_samples"][0]["pts"] += 1
        with self.assertRaisesRegex(ValueError, "exact-frame/PTS"):
            self.payload()

    def test_drawing_candidate_malicious_paths_and_symlink_rejected(self):
        frame, pts = 3, self.o["frames"][3]["pts"]
        for path in ("drawing_candidates/../cels/DEMO-A/source.png", "drawing_candidates/%2e%2e/source.png", "drawing_candidates/https://evil/source.png", "drawing_candidates//D001/source.png", "drawing_candidates/D001/source.png?frame=3", "drawing_candidates/D001/source.png#x", "drawing_candidates/D001/source.png\x00", "/tmp/source.png", "reference_frames/F000003.png"):
            drawing = {"source_samples": [{"frame": frame, "pts": pts, "image": path}]}
            with self.subTest(path=path), self.assertRaises(ValueError):
                viewer.validate_drawing_source(self.root, drawing, frame, path, pts)
        (self.root / "drawing_candidates").symlink_to(self.root / "cels", target_is_directory=True)
        path = "drawing_candidates/DEMO-A/source.png"
        drawing = {"source_samples": [{"frame": frame, "pts": pts, "image": path}]}
        with self.assertRaisesRegex(ValueError, "Symlink"):
            viewer.validate_drawing_source(self.root, drawing, frame, path, pts)

    def test_catalog_alone_cannot_adopt_drawing_candidate(self):
        self.c = [{"id": "DEMO-B", "source_frame": 3, "source_image": "drawing_candidates/D001/source.png"}]
        with self.assertRaisesRegex(ValueError, "Catalog source"):
            self.payload()

    @unittest.skipUnless((REPO / "magic_maid_20261029/data/reuse_manifest.json").is_file(), "Production reuse manifest not present; real-source regression pending")
    def test_real_d001_d003_source_samples_regression(self):
        project = REPO / "magic_maid_20261029"
        reuse = viewer.read_json(project / "data/reuse_manifest.json")
        timeline = viewer.read_json(project / "data/original_timeline.json")
        audit = viewer.read_json(project / "data/drawing_coverage_audit.json")
        drawings = {d["id"]: d for d in reuse["canonical_drawings"]}
        supplements = {d["id"]: d for d in audit["supplemental_observed_states"]}
        for did, frame in (("D001", 1247), ("D002", 4603), ("D003", 4679)):
            with self.subTest(drawing=did):
                drawing = drawings["ART-" + did]
                path = f"drawing_candidates/{did}/source.png"
                self.assertIn((frame, path), viewer.source_records(drawing))
                sample = next(s for s in drawing["source_samples"] if s["image"] == path)
                self.assertEqual(sample["frame"], frame)
                self.assertEqual(sample["pts"], timeline[frame]["pts"])
                target = viewer.validate_drawing_source(project, drawing, frame, path, timeline[frame]["pts"])
                self.assertEqual(viewer.png_dimensions(target), (1920, 1080))
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), supplements[did]["png_sha256"])
                self.assertEqual(supplements[did]["status"], "confirmed_missing_visible_drawing_state")

    def test_alias_cannot_inflate_count(self):
        self.r["canonical_drawings"][2]["count_in_conservative_plan"] = True
        with self.assertRaisesRegex(ValueError, "Alias cannot"):
            self.payload()

    def test_duplicate_drawing_and_unknown_alias_rejected(self):
        self.r["canonical_drawings"].append(copy.deepcopy(self.r["canonical_drawings"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.payload()
        self.r = copy.deepcopy(self.inputs[1])
        self.r["canonical_drawings"][2]["alias_of"] = "NOPE"
        with self.assertRaisesRegex(ValueError, "Alias target"):
            self.payload()

    def test_reuse_exact_pts_and_occurrence_pts(self):
        self.r["frames"][1]["pts"] += 1
        with self.assertRaisesRegex(ValueError, "Reuse frame"):
            self.payload()
        self.r = copy.deepcopy(self.inputs[1])
        self.r["canonical_drawings"][0]["occurrences"][0]["end_pts_exclusive"] += 1
        with self.assertRaisesRegex(ValueError, "Occurrence PTS"):
            self.payload()

    def test_sections_complete_no_overlap_local_pts(self):
        self.s["frame_sections"][4] = "S02"
        with self.assertRaisesRegex(ValueError, "S-section"):
            self.payload()
        self.s = copy.deepcopy(self.inputs[2])
        self.s["sections"][0]["ranges"][1]["local_start_pts"] = 0
        with self.assertRaisesRegex(ValueError, "local timeline"):
            self.payload()

    def test_no_silent_planning_count_mismatch(self):
        self.r["summary"]["planning_count"] = 331
        with self.assertRaisesRegex(ValueError, "planning count"):
            self.payload()

    def test_planning_budget_and_candidate_totals_are_manifest_driven(self):
        self.r["canonical_drawings"][3]["count_in_conservative_plan"] = True
        self.r["summary"]["planning_count"] = 3
        self.s["sections"][0]["new_drawing_ids"].append("DEMO-C")
        self.s["sections"][0]["new_drawing_count"] = 2
        self.r["conditional_reuse_pairs"] = [{**self.r["conditional_reuse_pairs"][0], "id": f"DEMO-CROSS-{i:02d}"} for i in range(1, 8)]
        p = self.payload()
        self.assertEqual(p["planning_count"], 3)
        self.assertEqual(p["kind_counts"], {"body_pose": 1, "mouth_detail": 1, "head_detail": 1})
        self.assertEqual(len(p["conditional_reuse_pairs"]), 7)
        page = viewer.render_html(p)
        self.assertIn("保守工作预算", page)
        self.assertIn("优先核查全身裁切复用候选，未确认新增", page)
        self.assertIn("这是工作顺序建议，不是教程原文", page)
        self.assertNotIn("本段新绘", page)

    def test_linework_color_budget_and_reviewed_work_scope_are_preserved(self):
        self.r["summary"].update(linework_count=1, color_only_count=1)
        self.s["sections"][0].update(new_linework_count=1, new_color_only_count=0, new_linework_ids=["DEMO-A"], new_color_only_ids=[])
        self.s["sections"][1].update(new_linework_count=0, new_color_only_count=1, new_linework_ids=[], new_color_only_ids=["DEMO-B"])
        fields = {"work_scope": "synthetic_partial_linework", "partial_reuse_scope": {"retained": ["body"]},
                  "redraw_regions": ["eyes"], "color_adjustment_regions": [], "work_operation": "local_line_redraw",
                  "line_drawing_required": True, "crop_review_pair_id": "DEMO-LOCAL-REVIEW", "crop_review_evidence": ["Source-observed fixture only"]}
        self.r["canonical_drawings"][0].update(fields)
        self.r["canonical_drawings"][1].update(work_operation="recolor_only", line_drawing_required=False)
        self.r["reviewed_crop_pairs"] = [{"id": "DEMO-LOCAL-REVIEW", "classification": "local_line_variant", "confirmed": False, "visual_reviewed": True}]
        self.s["sections"][0]["reviewed_crop_pair_ids"] = ["DEMO-LOCAL-REVIEW"]
        p = self.payload()
        self.assertEqual((p["linework_count"], p["color_only_count"]), (1, 1))
        self.assertEqual((p["sections"][1]["linework_count"], p["sections"][1]["color_only_count"]), (0, 1))
        for key, value in fields.items():
            self.assertEqual(p["drawings"][0][key], value)
        if shutil.which("node"):
            html = self.root / "mixed-budget.html"
            html.write_text(viewer.render_html(p))
            checked = subprocess.run(["node", str(REPO / "tests/overlay_viewer_contract.cjs"), str(html)], check=True, capture_output=True, text=True)
            self.assertIn("interaction contracts passed", checked.stdout)

    def test_budget_breakdown_absent_is_unknown_and_mismatch_is_rejected(self):
        p = self.payload()
        self.assertIsNone(p["linework_count"])
        self.assertIsNone(p["color_only_count"])
        self.r["summary"]["linework_count"] = 2
        with self.assertRaisesRegex(ValueError, "both counts"):
            self.payload()
        self.r["summary"]["color_only_count"] = 1
        with self.assertRaisesRegex(ValueError, "work budget"):
            self.payload()
        self.r["summary"]["color_only_count"] = 0
        self.s["sections"][0].update(new_linework_count=0, new_color_only_count=0)
        with self.assertRaisesRegex(ValueError, "S01.*work budget"):
            self.payload()

    def test_confirmed_crop_pairs_count_unique_reviews_not_transitive_aliases(self):
        pair = {"id": "DEMO-REVIEW", "from_id": "DEMO-ALIAS", "to_id": "DEMO-A", "classification": "confirmed_crop_reuse", "confirmed": True, "visual_reviewed": True, "evidence_paths": ["sheets/fixture.jpg"]}
        self.r["reviewed_crop_pairs"] = [pair]
        self.r["summary"]["confirmed_crop_reuse_pairs"] = 1
        alias = self.r["canonical_drawings"][2]
        alias.update(work_operation="crop_reuse_alias", line_drawing_required=False, crop_review_pair_id="DEMO-REVIEW")
        self.r["canonical_drawings"].append({**copy.deepcopy(alias), "id": "DEMO-TRANSITIVE-ALIAS"})
        self.s["sections"][0]["reviewed_crop_pair_ids"] = ["DEMO-REVIEW"]
        p = self.payload()
        self.assertEqual(p["confirmed_crop_reuse_count"], 1)
        self.assertEqual(sum(d["work_operation"] == "crop_reuse_alias" for d in p["drawings"]), 2)
        self.assertEqual(p["planning_count"], 2)
        self.assertEqual(len(p["conditional_reuse_pairs"]), 1)
        if shutil.which("node"):
            html = self.root / "confirmed-crop.html"
            html.write_text(viewer.render_html(p))
            subprocess.run(["node", str(REPO / "tests/overlay_viewer_contract.cjs"), str(html)], check=True, capture_output=True, text=True)
        self.r["summary"]["confirmed_crop_reuse_pairs"] = 2
        with self.assertRaisesRegex(ValueError, "unique reviewed pairs"):
            self.payload()

    def test_reviewed_pairs_cannot_remain_conditional_or_confirm_local_variants(self):
        pair = {"id": "DEMO-CROSS-01", "classification": "local_line_variant", "confirmed": False}
        self.r["reviewed_crop_pairs"] = [pair]
        with self.assertRaisesRegex(ValueError, "conditional candidate"):
            self.payload()
        pair["id"] = "DEMO-REVIEW"
        pair["confirmed"] = True
        with self.assertRaisesRegex(ValueError, "Only pure crop-reuse"):
            self.payload()

    def test_section_linework_color_ids_must_partition_budget(self):
        self.s["sections"][0].update(new_linework_count=0, new_color_only_count=1,
                                     new_linework_ids=[], new_color_only_ids=["DEMO-B"])
        with self.assertRaisesRegex(ValueError, "partition"):
            self.payload()

    def test_crop_alias_cannot_claim_count_or_missing_confirmed_review(self):
        alias = self.r["canonical_drawings"][2]
        alias.update(work_operation="crop_reuse_alias", line_drawing_required=True)
        with self.assertRaisesRegex(ValueError, "no-new-linework alias"):
            self.payload()
        alias["line_drawing_required"] = False
        with self.assertRaisesRegex(ValueError, "must link to a confirmed"):
            self.payload()

    def test_all_conditional_pairs_remain_unconfirmed(self):
        self.r["conditional_reuse_pairs"] = [{**self.r["conditional_reuse_pairs"][0], "id": f"DEMO-CROSS-{i:02d}"} for i in range(1, 50)]
        p = self.payload()
        self.assertEqual(len(p["conditional_reuse_pairs"]), 49)
        self.assertTrue(all(x["confirmed"] is False for x in p["conditional_reuse_pairs"]))
        self.assertEqual(p["planning_count"], 2)

    def test_template_failure_status_is_not_upgraded(self):
        item = self.o["frames"][0]["overlays"]["subtitles"]
        item["status"] = "missing_required_template"
        item["metadata"] = {"template_status": "missing_required_source_observed_template"}
        p = self.payload()
        self.assertEqual(p["frames"][0]["overlays"]["subtitles"]["status"], "missing_required_template")
        self.assertTrue(p["frames"][0]["overlays"]["subtitles"]["requires_review"])

    def test_new_drawing_ownership_cannot_double_count(self):
        self.s["sections"][1]["new_drawing_ids"].append("DEMO-A")
        self.s["sections"][1]["new_drawing_count"] += 1
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.payload()

    def test_safe_json_and_metadata_bounds(self):
        text = viewer.render_html(self.payload())
        self.assertNotIn("</script><script>alert", text)
        self.assertIn("\\u003c/script\\u003e", text)
        self.assertEqual(viewer.bounded_metadata("data:image/png;base64,xxx"), "[内嵌数据未复制到工作台]")
        self.assertLess(len(viewer.bounded_metadata(list(range(1000)))), 40)
        with self.assertRaises(ValueError):
            viewer.safe_json({"nan": float("nan")})

    def test_no_symlink_assets_or_output(self):
        a = next(iter(self.o["assets"]["subtitles"].values()))
        path = self.root / a["path"]
        backup = self.root / "outside.png"
        path.rename(backup)
        path.symlink_to(backup)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            self.payload()
        target = self.root / "linked.html"
        target.symlink_to(self.root / "nonexistent.html")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            viewer.output_path(self.root, "linked.html")

    def test_output_cannot_touch_protected_paths_or_hardlinks(self):
        for relative in ("source/new.html", "frames/new.html", "data/new.html", "../oops.html", "original.mp4"):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                viewer.output_path(self.root, relative)
        (self.root / "first.html").write_text("do not alter")
        os.link(self.root / "first.html", self.root / "second.html")
        with self.assertRaisesRegex(ValueError, "hard-linked"):
            viewer.output_path(self.root, "second.html")

    def test_foreign_root_html_is_preserved(self):
        for name in ("打开参考库.html", "分层工作台.html", "unowned.html"):
            original = "<!doctype html>\n<html>既有交付：不可覆盖</html>".encode("utf-8")
            path = self.root / name
            path.write_bytes(original)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "not owned"):
                viewer.build(self.root, output=name)
            self.assertEqual(path.read_bytes(), original)

    def test_owned_html_can_be_rebuilt(self):
        result = viewer.build(self.root)
        path = Path(result["output"])
        original = path.read_bytes()
        self.assertTrue(original.startswith(viewer.OWNED_HTML_PREFIX))
        manifest_path = self.root / "data/overlay_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["frames"][0]["overlays"]["effects"]["metadata"]["viewer_test_revision"] = "second build"
        manifest_path.write_text(json.dumps(manifest))
        viewer.build(self.root)
        updated = path.read_bytes()
        self.assertTrue(updated.startswith(viewer.OWNED_HTML_PREFIX))
        self.assertNotEqual(original, updated)
        self.assertIn(b"second build", updated)

    def test_build_atomic_local_and_structural_ids(self):
        result = viewer.build(self.root, verify_assets=True)
        page = Path(result["output"]).read_text()
        self.assertEqual(result["frame_count"], 8)
        self.assertEqual(result["section_count"], 2)
        self.assertEqual(result["browser_qa"], "not_run_by_builder")
        self.assertIn("合成测试夹具", page)
        ids = re.findall(r'\bid="([^"]+)"', page)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn("fetch(", page)
        self.assertNotRegex(page, r'<script[^>]+src=|<link[^>]+href="https?://')
        self.assertTrue(all(x in ids for x in ["frameSlider", "sourceStatus", "drawingGrid", "sectionRows", "sectionRelation", "overlayOrder", "overlayOrderStatus"]))
        before = (self.root / "frames/F000000.png").read_bytes()
        viewer.build(self.root)
        self.assertEqual(before, (self.root / "frames/F000000.png").read_bytes())

    @unittest.skipUnless(shutil.which("node"), "Node unavailable: JS contract tests not run")
    def test_javascript_syntax_and_interaction_contract(self):
        page = viewer.render_html(self.payload())
        scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', page, re.S)
        code = scripts[-1]
        js = self.root / "viewer.js"
        js.write_text(code)
        subprocess.run(["node", "--check", str(js)], check=True, capture_output=True, text=True)
        html = self.root / "fixture.html"
        html.write_text(page)
        checked = subprocess.run(["node", str(REPO / "tests/overlay_viewer_contract.cjs"), str(html)], check=True, capture_output=True, text=True)
        self.assertIn("interaction contracts passed", checked.stdout)


if __name__ == "__main__":
    unittest.main()
