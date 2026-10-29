import sys
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import magic_maid_frame_layers as frames
import magic_maid_timeline as timeline


class FramePartitionTests(unittest.TestCase):
    def test_scene_routes_respect_declared_ranges_and_one_frame_entry(self):
        project = SCRIPTS.parent / "magic_maid_20261029"
        bindings = timeline.build_bindings(project)
        routes = frames.scene_routes(timeline.read_json(project / "data/panel_catalog.json"), bindings)
        expected = {0: "", 9: "G01", 96: "G01", 97: "G02", 1488: "G15", 1489: "G16",
                    818: "G11", 834: "G12", 2801: "G12", 3373: "G12", 3625: "G13",
                    2948: "G12", 2954: "G12", 2958: "G12", 2959: "G37",
                    4021: "X01", 4022: "X01", 4103: "X02", 4261: "X05", 4280: "G47", 4315: "X05",
                    4355: "", 4431: "G03", 4762: "G51"}
        for frame, group in expected.items():
            with self.subTest(frame=frame):
                self.assertEqual(routes[frame]["group"], group)
                self.assertFalse(routes[frame]["character_identity_inferred"])
        self.assertEqual(len(routes), 4763)
        self.assertNotEqual(routes[4021]["pts"], routes[4022]["pts"])

    def test_label_roundtrip_is_exact_not_a_semantic_claim(self):
        rgb = np.arange(2 * 3 * 3, dtype=np.uint8).reshape(2, 3, 3)
        masks = {name: np.zeros((2, 3), dtype=bool) for name in frames.LAYER_ORDER}
        for index, name in enumerate(frames.LAYER_ORDER):
            masks[name].flat[index] = True
        labels = frames.labels_from_masks(masks, (2, 3))
        self.assertTrue(np.array_equal(frames.reconstruct_rgb(rgb, labels), rgb))
        masks[frames.LAYER_ORDER[0]][0, 1] = True
        with self.assertRaises(ValueError):
            frames.labels_from_masks(masks, (2, 3))

    def test_palette_png_keeps_ids_not_luminance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "labels.png"
            labels = np.arange(6, dtype=np.uint8).reshape(2, 3)
            image = Image.fromarray(labels, mode="P")
            image.putpalette(frames.PALETTE)
            image.save(path)
            restored = frames.read_labels(path, [3, 2])
            self.assertTrue(np.array_equal(restored, labels))
            bad = Image.fromarray(np.full((2, 3), 7, dtype=np.uint8))
            bad.save(path)
            with self.assertRaises(ValueError):
                frames.read_labels(path, [3, 2])


if __name__ == "__main__":
    unittest.main()
