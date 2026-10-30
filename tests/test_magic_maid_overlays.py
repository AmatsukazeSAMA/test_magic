"""Portable overlay-contract tests; no extractor/source-video download required."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import magic_maid_overlays as overlays


class AlphaContractTests(unittest.TestCase):
    def test_template_dependencies_use_selected_project_and_exact_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "data").mkdir()
            (project / "data/template.png").write_bytes(b"source-observed template")
            configure = mock.Mock()
            module = SimpleNamespace(configure_project=configure, DATA_DEPENDENCIES=["data/template.png"])
            with mock.patch.object(overlays.importlib, "import_module", return_value=module):
                result = overlays.extractor_dependencies(project)
            self.assertEqual(result, {"data/template.png": hashlib.sha256(b"source-observed template").hexdigest()})
            self.assertEqual(configure.call_count, 2)
            module.DATA_DEPENDENCIES = ["../outside"]
            with mock.patch.object(overlays.importlib, "import_module", return_value=module), self.assertRaises(ValueError):
                overlays.extractor_dependencies(project)

    def test_straight_alpha_composition_is_not_premultiplied_twice(self):
        rgba = np.array([[[240, 20, 60, 128], [0, 0, 0, 0], [240, 20, 60, 255]]], dtype=np.uint8)
        background = np.full((1, 3, 3), 40, dtype=np.uint8)
        result = overlays.composite_straight(rgba, background)
        np.testing.assert_array_equal(result, [[[140, 30, 50], [40, 40, 40], [240, 20, 60]]])
        self.assertEqual(overlays.rgba_stats(rgba), {
            "nonzero_alpha_pixels": 2, "partial_alpha_pixels": 1, "opaque_pixels": 1, "bbox": [0, 0, 3, 1]})

    def test_transparent_rgb_and_dtype_contract(self):
        transparent = np.zeros((2, 3, 4), dtype=np.uint8)
        self.assertIsNone(overlays.rgba_stats(transparent)["bbox"])
        for invalid in (transparent.astype(float), transparent[:, :, :3], [[0, 0, 0, 0]]):
            with self.assertRaises(ValueError):
                overlays.rgba_stats(invalid)
        transparent[0, 0, 0] = 1
        with self.assertRaisesRegex(ValueError, "zero RGB"):
            overlays.rgba_stats(transparent)

    def test_cropped_canvas_rejected(self):
        with self.assertRaisesRegex(ValueError, "full canvas"):
            overlays.rgba_stats(np.zeros((2, 3, 4), dtype=np.uint8), [30, 20])

    def test_explicit_status_and_serializable_metadata_required(self):
        for value in ({}, {"status": ""}, {"status": "x", "error": float("nan")},
                      {"status": "x", "count": np.int64(3)}):
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                overlays.normalize_metadata(value)
        self.assertEqual(overlays.normalize_metadata({"status": "unsupported", "limitations": ["occluded"]})["status"], "unsupported")


class AssetAndManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name)
        (self.project / "data").mkdir()
        self.rows = [
            {"frame": 0, "pts": 0, "duration_ticks": 528},
            {"frame": 1, "pts": 528, "duration_ticks": 544},
            {"frame": 2, "pts": 1072, "duration_ticks": 533},
        ]
        (self.project / "data/original_timeline.json").write_text(json.dumps(self.rows))
        (self.project / "data/chapters.json").write_text(json.dumps([
            {"id": "M00", "start_frame": 0, "end_frame_exclusive": 3}]))
        (self.project / "data/original_ffprobe.json").write_text(json.dumps({"streams": [{
            "codec_type": "video", "time_base": "1/16000", "duration_ts": 1605, "width": 4, "height": 2}]}))
        self.assets = {name: {} for name in overlays.CATEGORIES}
        self.ids = {}
        for category in overlays.CATEGORIES:
            (self.project / "overlays" / category).mkdir(parents=True)
            self.ids[category] = []
            for alpha in (0, 128):
                rgba = np.zeros((2, 4, 4), dtype=np.uint8)
                if alpha:
                    rgba[0, 1] = (237, 237, 237, alpha)
                identity, asset = overlays.store_rgba(self.project, "overlays", category, rgba)
                self.assets[category][identity] = asset
                self.ids[category].append(identity)
        self.frames = []
        for row in self.rows:
            self.frames.append({**row, "chapter_id": "M00", "group": "", "original_frame": f"frames/F{row['frame']:06d}.png",
                                "source_png_sha256": "0" * 64, "source_rgb_sha256": "0" * 64,
                                "source_rgb_md5": "0" * 32,
                                "overlays": {category: {
                                    "asset_id": self.ids[category][0 if row["frame"] == 0 else 1],
                                    "status": "needs_review", "requires_review": True,
                                    "metadata": {"status": "needs_review", "limitations": ["estimated alpha"]},
                                } for category in overlays.CATEGORIES}})
        self.manifest = {
            "schema": overlays.SCHEMA, "build_complete": True, "source": "source/original.mp4",
            "source_sha256": overlays.SOURCE_HASHES["original"], "asset_root": "overlays",
            "alpha_mode": "straight", "transparent_rgb": [0, 0, 0], "dimensions": [4, 2],
            "frame_count": 3, "completed_frames": 3, "time_base": "1/16000", "video_duration_ticks": 1605,
            "assets": self.assets, "frames": self.frames,
            "source_cache_verification": {"all_cached_rgb_equal_source_decode": True, "frame_count": 3,
                "rgb_frame_checksum_chain_sha256": hashlib.sha256("\n".join(["0" * 32] * 3).encode()).hexdigest()},
            "summary": overlays.summarize(self.frames, self.assets),
            "exposures": overlays.make_exposures(self.frames),
        }
        self.manifest_path = self.project / "data/overlay_manifest.json"
        self.save()

    def tearDown(self):
        self.temporary.cleanup()

    def save(self):
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def verify(self):
        return overlays.verify_manifest(self.project, self.manifest_path, check_source=False)

    def test_independent_saved_assets_and_exact_timing(self):
        report = self.verify()
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["final_frame_duration_ticks"], 533)
        self.assertFalse(report["semantic_quality_verified"])
        self.assertEqual(report["summary"]["categories"]["subtitles"]["empty_frames"], 1)
        self.assertEqual(report["summary"]["categories"]["effects"]["frames_with_partial_alpha"], 2)

    def test_content_dedup_does_not_duplicate_still_frames(self):
        rgba = np.zeros((2, 4, 4), dtype=np.uint8)
        identity, asset = overlays.store_rgba(self.project, "overlays", "subtitles", rgba)
        self.assertEqual(identity, self.ids["subtitles"][0])
        self.assertEqual(len(list((self.project / "overlays/subtitles").glob("*.png"))), 2)
        self.assertEqual(asset, self.assets["subtitles"][identity])

    def test_exposures_use_exact_pts_not_frame_over_thirty(self):
        exposure = self.manifest["exposures"]["subtitles"][1]
        self.assertEqual(exposure, {
            "start_frame": 1, "end_frame_exclusive": 3, "start_pts": 528,
            "end_pts_exclusive": 1605, "asset_id": self.ids["subtitles"][1]})
        concat = self.project / "subtitles.ffconcat"
        overlays.write_portable_concat(concat, [f"subtitles/F{i:06d}.png" for i in range(3)], self.rows, "1/16000")
        text = concat.read_text()
        self.assertIn("duration 0.033000", text)
        self.assertIn("duration 0.034000", text)
        self.assertIn("duration 0.033312", text)
        self.assertNotIn(str(self.project), text)
        self.assertEqual(text.count("file '"), 4)  # final duplicate is timing sentinel

    def test_modified_asset_is_rejected(self):
        asset = next(iter(self.assets["subtitles"].values()))
        (self.project / asset["path"]).write_bytes(b"altered")
        with self.assertRaises(ValueError):
            self.verify()

    def test_unindexed_asset_is_not_silently_delivered(self):
        Image.new("RGBA", (4, 2)).save(self.project / "overlays/effects/unindexed.png")
        with self.assertRaisesRegex(ValueError, "unindexed PNG"):
            self.verify()

    def test_invalid_pts_missing_category_and_false_summary_rejected(self):
        mutations = [lambda d: d["frames"][1].update(pts=533),
                     lambda d: d["frames"][2].update(duration_ticks=528),
                     lambda d: d["frames"][0]["overlays"].pop("effects"),
                     lambda d: d["summary"]["categories"]["subtitles"].update(nonempty_frames=3),
                     lambda d: d.update(alpha_mode="premultiplied"),
                     lambda d: d["exposures"]["subtitles"][1].update(end_pts_exclusive=1600)]
        initial = copy.deepcopy(self.manifest)
        for mutation in mutations:
            self.manifest = copy.deepcopy(initial)
            mutation(self.manifest)
            self.save()
            with self.assertRaises(ValueError):
                self.verify()

    def test_source_or_unknown_output_never_overwritten(self):
        source = self.project / "source"
        source.mkdir()
        (source / "original.mp4").write_bytes(b"original")
        for output, manifest in [("source/new", "data/new.json"), ("new", "source/new.json"),
                                 ("new", "source/original.mp4"), ("overlays", "data/new.json")]:
            with self.subTest(output=output, manifest=manifest), self.assertRaises(ValueError):
                overlays.prepare_build_paths(self.project, output, manifest)
        self.assertEqual((source / "original.mp4").read_bytes(), b"original")

    def test_symlink_asset_and_output_parent_rejected(self):
        (self.project / "linked").symlink_to(self.project / "overlays", target_is_directory=True)
        with self.assertRaises(ValueError):
            overlays.prepare_build_paths(self.project, "linked/new", "data/new.json")
        asset = next(iter(self.assets["effects"].values()))
        path = self.project / asset["path"]
        moved = self.project / "moved.png"
        path.replace(moved)
        path.symlink_to(moved)
        with self.assertRaises(ValueError):
            self.verify()

    def test_export_has_both_complete_transparent_png_sequences(self):
        output = self.project / "exported"
        with mock.patch.object(overlays, "validate_source", return_value={"status": "pass"}):
            result = overlays.export_sequence(self.project, self.manifest_path, output)
        self.assertEqual(result["frame_count_per_category"], 3)
        for category in overlays.CATEGORIES:
            self.assertEqual(len(list((output / category).glob("*.png"))), 3)
            with Image.open(output / category / "F000000.png") as image:
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.getpixel((0, 0)), (0, 0, 0, 0))
            self.assertEqual((output / category / "F000001.png").read_bytes(), (output / category / "F000002.png").read_bytes())
        sequence = json.loads((output / "sequence.json").read_text())
        self.assertEqual(sequence["frames"][-1]["duration_ticks"], 533)
        with self.assertRaises(ValueError):
            overlays.export_sequence(self.project, self.manifest_path, output)

    def test_checker_preview_never_uses_original_background(self):
        output = self.project / "preview.png"
        subtitle = self.assets["subtitles"][self.ids["subtitles"][0]]["path"]
        effects = self.assets["effects"][self.ids["effects"][0]]["path"]
        overlays._preview_frame((str(self.project), subtitle, effects, str(output), [4, 2]))
        with Image.open(output) as image:
            self.assertEqual(image.size, (4, 37))
            self.assertEqual(image.getpixel((0, 36)), (46, 46, 46))

    def test_preview_decode_checked_against_actual_overlay_composite(self):
        frame = self.project / "composite.png"
        Image.new("RGB", (4, 2), (46, 46, 46)).save(frame)
        rows = self.rows[:1]
        with mock.patch.object(overlays, "decode_frame_at_pts", return_value=bytes([47] * 24)):
            result = overlays.verify_preview_samples(Path("movie.mp4"), [frame], rows, "1/16000", [4, 2])
        self.assertEqual(result["status"], "pass")
        with mock.patch.object(overlays, "decode_frame_at_pts", return_value=bytes([80] * 24)):
            with self.assertRaisesRegex(ValueError, "differs from saved RGBA"):
                overlays.verify_preview_samples(Path("movie.mp4"), [frame], rows, "1/16000", [4, 2])


if __name__ == "__main__":
    unittest.main()
