from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

SPEC = importlib.util.spec_from_file_location("verify_layers", Path(__file__).resolve().parents[1] / "scripts/verify_layers.py")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class LayerIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "data").mkdir()
        (self.root / "cels/A").mkdir(parents=True)
        (self.root / "layers/A").mkdir(parents=True)
        self.rgb = np.array([[[10, 20, 30], [40, 50, 60]],
                             [[70, 80, 90], [100, 110, 120]]], dtype=np.uint8)
        Image.fromarray(self.rgb).save(self.root / "cels/A/source.png")
        self.catalog = {"id": "A", "source_frame": 3, "source_pts": 1600,
                        "source_image": "cels/A/source.png", "dimensions": [2, 2],
                        "source_png_sha256": VERIFY.digest(self.root / "cels/A/source.png")}
        self.panel = {"panel_id": "A", "source_frame": 3, "source_pts": 1600,
                      "layers": [{"name": "a", "path": "layers/A/a.png"},
                                 {"name": "b", "path": "layers/A/b.png"}]}
        self.write_layer("a", np.array([[True, False], [True, False]]))
        self.write_layer("b", np.array([[False, True], [False, True]]))
        (self.root / "data/panel_catalog.json").write_text(json.dumps([self.catalog]))
        (self.root / "data/layer_manifest.json").write_text(json.dumps({"panels": [self.panel]}))

    def tearDown(self):
        self.directory.cleanup()

    def write_layer(self, name, mask, altered=False):
        rgba = np.zeros((2, 2, 4), dtype=np.uint8)
        rgba[mask, :3] = self.rgb[mask]
        rgba[mask, 3] = 255
        if altered:
            rgba[0, 0, 0] += 1
        Image.fromarray(rgba).save(self.root / f"layers/A/{name}.png")

    def test_exact_partition_does_not_claim_semantic_pass(self):
        report = VERIFY.verify(self.root, expected_panels=1)
        self.assertEqual(report["status"], "pass")
        self.assertFalse(report["semantic_acceptance"])
        self.assertFalse(report["hidden_pixels_recovered"])

    def test_overlap_rejected(self):
        self.write_layer("b", np.ones((2, 2), dtype=bool))
        with self.assertRaisesRegex(ValueError, "multiply assigned"):
            VERIFY.verify_panel(self.root, self.panel, self.catalog)

    def test_gap_rejected(self):
        self.write_layer("b", np.zeros((2, 2), dtype=bool))
        with self.assertRaisesRegex(ValueError, "unassigned"):
            VERIFY.verify_panel(self.root, self.panel, self.catalog)

    def test_stale_unlisted_png_rejected(self):
        self.write_layer("obsolete_subtitle", np.ones((2, 2), dtype=bool))
        with self.assertRaisesRegex(ValueError, "unlisted/missing PNG"):
            VERIFY.verify_panel(self.root, self.panel, self.catalog)

    def test_hidden_rgb_outside_binary_alpha_rejected(self):
        path = self.root / "layers/A/a.png"
        rgba = np.array(Image.open(path))
        rgba[0, 1, :3] = [1, 2, 3]
        Image.fromarray(rgba).save(path)
        with self.assertRaisesRegex(ValueError, "RGB must be zero"):
            VERIFY.verify_panel(self.root, self.panel, self.catalog)

    def test_changed_visible_rgb_rejected(self):
        self.write_layer("a", np.array([[True, False], [True, False]]), altered=True)
        with self.assertRaisesRegex(ValueError, "unchanged source RGB"):
            VERIFY.verify_panel(self.root, self.panel, self.catalog)

    def test_original_mutation_rejected(self):
        Image.fromarray(self.rgb + 1).save(self.root / "cels/A/source.png")
        with self.assertRaisesRegex(ValueError, "source PNG was modified"):
            VERIFY.verify_panel(self.root, self.panel, self.catalog)

    def test_source_frame_or_pts_mismatch_rejected(self):
        for field in ("source_frame", "source_pts"):
            panel = copy.deepcopy(self.panel)
            panel[field] += 1
            with self.assertRaisesRegex(ValueError, "mismatch"):
                VERIFY.verify_panel(self.root, panel, self.catalog)

    def test_paths_do_not_escape(self):
        for path in ("../source.png", "/tmp/source.png", "https://example.com/a.png", "..\\a"):
            with self.assertRaises(ValueError):
                VERIFY.local_path(self.root, path)

    def test_duplicate_panels_rejected(self):
        (self.root / "data/layer_manifest.json").write_text(json.dumps({"panels": [self.panel, self.panel]}))
        with self.assertRaisesRegex(ValueError, "exactly once"):
            VERIFY.verify(self.root, expected_panels=2)

    def test_report_cannot_overwrite_original_or_catalog(self):
        report = {"schema": VERIFY.REPORT_SCHEMA, "status": "pass"}
        for path in (self.root / "cels/A/source.png", self.root / "data/panel_catalog.json"):
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                VERIFY.save_report(path, report)
            self.assertEqual(path.read_bytes(), before)
        output = self.root / "data/verified.json"
        VERIFY.save_report(output, report)
        VERIFY.save_report(output, report)
        self.assertEqual(json.loads(output.read_text()), report)

    def test_report_symlink_rejected_without_mutating_target(self):
        report = {"schema": VERIFY.REPORT_SCHEMA, "status": "pass"}
        target = self.root / "data/actual.json"
        VERIFY.save_report(target, report)
        link = self.root / "data/link.json"
        link.symlink_to(target)
        before = target.read_bytes()
        with self.assertRaisesRegex(ValueError, "symlink"):
            VERIFY.save_report(link, report)
        self.assertEqual(before, target.read_bytes())


if __name__ == "__main__":
    unittest.main()
