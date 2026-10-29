import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np


SPEC = importlib.util.spec_from_file_location(
    "drawing_audit", Path(__file__).resolve().parents[1] / "scripts/magic_maid_drawing_audit.py")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class DrawingCoverageTests(unittest.TestCase):
    def test_exact_compositions_do_not_merge_nearby_or_transformed_frames(self):
        self.assertEqual(AUDIT.exact_representatives(["a", "b", "a", "c", "b"]), [0, 1, 0, 3, 1])

    def test_small_eye_change_is_not_exact_identity(self):
        a = np.zeros((135, 240), dtype=np.uint8)
        a[20:100, 60:170] = 1
        b = a.copy()
        b[35, 90] = 3
        self.assertGreater(AUDIT.descriptor_distance(a, b), 0)
        # Even below the triage threshold this is NOT an equality assertion.
        self.assertLess(AUDIT.descriptor_distance(a, b), .025)

    def test_petals_are_not_red_garments(self):
        rgb = np.array([[[140, 32, 105], [180, 10, 10], [252, 218, 199], [30, 30, 30]]], dtype=np.uint8)
        self.assertEqual(AUDIT.color_ink_classes(rgb).tolist(), [[0, 1, 2, 3]])

    def test_exact_pts_and_final_endpoint(self):
        timeline = [{"pts": 0}, {"pts": 528}, {"pts": 1072}]
        row = AUDIT.exposure(timeline, 1, 2, "review")
        self.assertEqual((row["start_pts"], row["end_pts_exclusive"]), (528, 1072))
        last = AUDIT.exposure(timeline, 2, 3, "review")
        self.assertEqual(last["end_pts_exclusive"], AUDIT.VIDEO_END_PTS)
        self.assertIsNone(last["author_cel_identity"])
        self.assertFalse(last["automatic_pixel_reuse_authorized"])

    def test_invalid_exposure_rejected(self):
        timeline = [{"pts": 0}]
        for start, end in [(-1, 1), (0, 0), (0, 2), (1, 0)]:
            with self.assertRaises(ValueError):
                AUDIT.exposure(timeline, start, end, "test")

    def test_three_new_visible_states_not_eight_independent_tail_cels(self):
        confirmed = [x for x in AUDIT.SUPPLEMENTS if x["status"].startswith("confirmed_missing")]
        self.assertEqual(len(confirmed), 3)
        self.assertEqual(sum(e - s for x in confirmed for s, e in x["ranges"]), 55)
        tail = next(x for x in confirmed if x["source_frame"] == 4679)
        self.assertEqual(len(tail["ranges"]), 6)
        self.assertEqual(sum(e - s for s, e in tail["ranges"]), 48)

    def test_catalog_is_not_modified_and_generated_overwrite_requires_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual.json"
            path.write_text('{"manual": true}')
            with self.assertRaises(ValueError):
                AUDIT.write_json(path, {"schema": AUDIT.SCHEMA}, refresh=True)
            self.assertEqual(path.read_text(), '{"manual": true}')

    def test_symlink_output_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "actual").mkdir()
            (root / "link").symlink_to(root / "actual", target_is_directory=True)
            with self.assertRaises(ValueError):
                AUDIT.safe_path(root / "link" / "out.json")

    def test_native_hash_parser_rejects_non_native_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "small.framemd5"
            path.write_text("#format: frame checksums\n0,0,0,1,97200,abc\n")
            with self.assertRaises(ValueError):
                AUDIT.parse_rgb_hashes(path)

    def test_any_native_inventory_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError, "F1"):
            AUDIT.compare_native_hashes(["a", "tampered", "c"], ["a", "b", "c"])
        with self.assertRaises(ValueError):
            AUDIT.compare_native_hashes(["a"], ["a", "b"])

    def test_complete_claim_and_author_count_are_rejected(self):
        valid = {"conclusion": {"all_character_drawing_states_proven_captured": False,
                                "hidden_pixels_recovered": False}, "counts": {"author_cel_count": None}}
        AUDIT.validate_conclusion(valid)
        valid["conclusion"]["all_character_drawing_states_proven_captured"] = True
        with self.assertRaises(ValueError):
            AUDIT.validate_conclusion(valid)
        valid["conclusion"]["all_character_drawing_states_proven_captured"] = False
        valid["counts"]["author_cel_count"] = 411
        with self.assertRaises(ValueError):
            AUDIT.validate_conclusion(valid)

    def test_manifest_asset_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ["/tmp/elsewhere.png", "drawing_candidates/../../outside.png", "source/original.mp4"]:
                with self.assertRaises(ValueError):
                    AUDIT.project_asset(root, name, "drawing_candidates")

    def test_full_cover_is_explicitly_occluded(self):
        status, _, hidden = AUDIT.interval_capture_status({"change_class": "unresolved_under_full_cover",
                                                          "visible_state_label": "fully_occluded", "catalog_panel_id": None})
        self.assertEqual((status, hidden), ("occluded", "full"))

    def test_partial_cover_keeps_known_visible_state_but_not_hidden_identity(self):
        status, _, hidden = AUDIT.interval_capture_status({"change_class": "effects_only_variant_with_occlusion",
                                                          "catalog_panel_id": "G11-07"})
        self.assertEqual((status, hidden), ("known", "partial"))

    def test_uncertain_catalog_link_is_not_identity_proof(self):
        status, _, _ = AUDIT.interval_capture_status({"change_class": "visible_state", "catalog_panel_id": "G12-22",
                                                      "confidence": "medium"})
        self.assertEqual(status, "possible_missing")


if __name__ == "__main__":
    unittest.main()
