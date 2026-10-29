"""Run with python -m unittest discover -s tests -p 'test_magic_maid_timeline.py'."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from PIL import Image


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("timeline", REPO / "scripts/magic_maid_timeline.py")
timeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(timeline)


class TimingUnitTests(unittest.TestCase):
    def test_integer_pts_and_final_duration(self):
        rows = timeline.validated_timeline([
            {"frame": 0, "pts": 0, "duration_s": 999},
            {"frame": 1, "pts": 528},
            {"frame": 2, "pts": 1072},
        ], "1/16000", 1605)
        self.assertEqual([r["duration_ticks"] for r in rows], [528, 544, 533])

    def test_invalid_timelines_rejected(self):
        bad = [[], [{"frame": 1, "pts": 0}], [{"frame": 0, "pts": 1}],
               [{"frame": 0, "pts": 0.0}],
               [{"frame": 0, "pts": 0}, {"frame": 1, "pts": 0}]]
        for rows in bad:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                timeline.validated_timeline(rows, "1/16000", 100)
        with self.assertRaises(ValueError):
            timeline.validated_timeline([{"frame": 0, "pts": 0}], "1/16000", 0)

    def test_chapter_gaps_and_overlap_rejected(self):
        for chapters in [[], [{"id": "x", "start_frame": 1, "end_frame_exclusive": 2}],
                         [{"id": "x", "start_frame": 0, "end_frame_exclusive": 1},
                          {"id": "y", "start_frame": 0, "end_frame_exclusive": 2}]]:
            with self.subTest(chapters=chapters), self.assertRaises(ValueError):
                timeline.chapter_index(chapters, 2)

    def test_source_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for value in ["../secret", "/tmp/secret", "", None]:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    timeline.inside(root, value)
            self.assertEqual(timeline.inside(root, "frames/F000000.png"), root / "frames/F000000.png")

    def test_json_output_protects_sources_unknown_files_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "original.mp4"
            source.write_bytes(b"immutable video")
            with self.assertRaises(ValueError):
                timeline.write_json(source, {"schema": timeline.SCHEMA}, overwrite=True, expected_schema=timeline.SCHEMA)
            self.assertEqual(source.read_bytes(), b"immutable video")
            unknown = root / "catalog.json"
            unknown.write_text('[{"source":"keep"}]')
            with self.assertRaises(ValueError):
                timeline.write_json(unknown, {"schema": timeline.SCHEMA}, overwrite=True, expected_schema=timeline.SCHEMA)
            link = root / "link.json"
            link.symlink_to(unknown)
            with self.assertRaises(ValueError):
                timeline.write_json(link, {})
            parent_link = root / "linked-parent"
            parent_link.symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                timeline.write_json(parent_link / "new.json", {})
            generated = root / "generated.json"
            timeline.write_json(generated, {"schema": timeline.SCHEMA, "value": 1})
            timeline.write_json(generated, {"schema": timeline.SCHEMA, "value": 2}, overwrite=True, expected_schema=timeline.SCHEMA)
            self.assertEqual(json.loads(generated.read_text())["value"], 2)

    def test_cli_bindings_cannot_overwrite_original_video(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "original.mp4"
            output.write_bytes(b"do not replace")
            with self.assertRaises(ValueError):
                timeline.main(["bindings", "--output", str(output)])
            self.assertEqual(output.read_bytes(), b"do not replace")

    def test_render_refuses_existing_verification_sidecar_before_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "movie.verification.json").write_text('{"keep":true}')
            with self.assertRaises(ValueError):
                timeline.render(root, root / "movie.mp4", None)
            self.assertFalse((root / "movie.mp4").exists())

    def test_container_difference_requires_verified_rgb_and_valid_label_hash(self):
        # A re-encoded PNG is portable; a changed label or unverified source is not.
        import numpy as np
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = Image.new("RGB", (64, 64), (10, 120, 240))
            original = root / "original.png"
            image.save(original, compress_level=0)
            original_hash = timeline.sha256(original)
            image.save(original, compress_level=9)
            self.assertNotEqual(timeline.sha256(original), original_hash)
            labels = root / "labels.png"
            Image.fromarray(np.zeros((64, 64), dtype=np.uint8)).save(labels)
            partition = {"frame": 0, "original_frame": "original.png", "label_map": "labels.png",
                         "source_png_sha256": original_hash, "label_png_sha256": timeline.sha256(labels)}
            with self.assertRaises(ValueError):
                timeline.compose_frame_partition(root, partition, [64, 64], {})
            result, changed_container = timeline.compose_frame_partition(root, partition, [64, 64],
                                                                         {"all_cached_rgb_equal_source_decode": True})
            self.assertTrue(changed_container)
            self.assertEqual(result.tobytes(), image.tobytes())
            labels.write_bytes(b"tampered")
            with self.assertRaises(ValueError):
                timeline.compose_frame_partition(root, partition, [64, 64], {"all_cached_rgb_equal_source_decode": True})

    def test_partition_composition_and_incomplete_alpha(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a = Image.new("RGBA", (2, 1), (0, 0, 0, 0))
            a.putpixel((0, 0), (20, 30, 40, 255))
            b = Image.new("RGBA", (2, 1), (0, 0, 0, 0))
            b.putpixel((1, 0), (100, 110, 120, 255))
            a.save(root / "a.png")
            b.save(root / "b.png")
            panel = {"panel_id": "x", "layers": [{"path": "a.png", "z_index": 0}, {"path": "b.png", "z_index": 1}]}
            result = timeline.compose_layers(root, panel, [2, 1])
            self.assertEqual(result.tobytes(), bytes([20, 30, 40, 100, 110, 120]))
            panel["layers"].pop()
            with self.assertRaises(ValueError):
                timeline.compose_layers(root, panel, [2, 1])

    def test_concat_cumulative_rounding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = timeline.validated_timeline([{"frame": i, "pts": i * 533} for i in range(300)], "1/16000", 300 * 533)
            concat = root / "frames.ffconcat"
            timeline.write_concat(concat, [root / "x.png"] * 300, rows, "1/16000")
            from decimal import Decimal
            durations = [Decimal(line.split()[1]) for line in concat.read_text().splitlines() if line.startswith("duration ")]
            self.assertEqual(sum(durations), Decimal("9.993750"))
            self.assertEqual(concat.read_text().count("file "), 301)


class RepositoryBindingsTests(unittest.TestCase):
    def setUp(self):
        self.project = REPO / "magic_maid_20261029"

    def test_full_bindings_do_not_invent_global_cel_ids(self):
        result = timeline.build_bindings(self.project)
        self.assertEqual(result["frame_count"], 4763)
        self.assertEqual(result["time_base"], "1/16000")
        self.assertEqual(result["frames"][-1]["duration_ticks"], 533)
        self.assertEqual(result["summary"]["audited_character_bound_frames"], 161)
        self.assertEqual(result["summary"]["source_fallback"], 4763)
        self.assertLessEqual(result["summary"]["exact_catalog_source_frames"], 411)
        self.assertEqual(result["frames"][9]["character_binding"]["state_id"], "G01-01")
        self.assertEqual(result["frames"][20]["character_binding"]["state_id"], "G01-01")
        self.assertIsNone(result["frames"][170]["character_binding"])
        self.assertIn("X01-01", result["frames"][4021]["exact_source_panel_ids"])
        self.assertNotIn("X01-01", result["frames"][4022]["exact_source_panel_ids"])
        self.assertNotEqual(result["frames"][4021]["pts"], result["frames"][4022]["pts"])

    def test_supplemental_observation_does_not_extrapolate_or_assert_author_identity(self):
        rows = timeline.build_bindings(self.project)["frames"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            audit = {"supplemental_observed_states": [{"id": "D-test", "source_frame": 4021,
                      "source_pts": rows[4021]["pts"], "status": "visible_state_audited",
                      "author_cel_identity": None,
                      "observed_exposures": [{"start_frame": 4021, "end_frame_exclusive": 4022,
                                              "start_pts": rows[4021]["pts"], "end_pts_exclusive": rows[4022]["pts"],
                                              "evidence_level": "native_visible_comparison"}]}]}
            (root / "data/drawing_coverage_audit.json").write_text(json.dumps(audit))
            links, count = timeline.supplemental_observations(root, rows, rows[-1]["pts"] + rows[-1]["duration_ticks"])
            self.assertEqual(count, 1)
            self.assertEqual(set(links), {4021})
            self.assertIsNone(links[4021][0]["author_cel_identity"])
            self.assertFalse(links[4021][0]["automatic_layer_or_transform_reuse"])

    def test_layer_binding_never_extends_to_same_pose_exposure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "layers.json"
            path.write_text(json.dumps({"panels": [{"panel_id": "G01-01", "source_frame": 9, "source_pts": 4800,
                                                   "layers": [{"path": "dummy.png"}], "status": "needs_review"}]}))
            result = timeline.build_bindings(self.project, path)
            self.assertEqual(result["frames"][9]["composition"]["mode"], "exact_source_layers")
            self.assertEqual(result["frames"][10]["composition"]["mode"], "source_fallback")
            self.assertEqual(result["frames"][20]["composition"]["mode"], "source_fallback")
            self.assertEqual(result["summary"]["exact_source_layers"], 1)

    def test_layer_identity_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "layers.json"
            path.write_text(json.dumps({"panels": [{"panel_id": "G01-01", "source_frame": 10, "source_pts": 4800}]}))
            with self.assertRaises(ValueError):
                timeline.build_bindings(self.project, path)

    def test_all_frame_partition_binding_is_coverage_not_semantic_approval(self):
        baseline = timeline.build_bindings(self.project)
        partition = {"schema": "magic-maid.frame-visible-partitions/1", "build_complete": True,
                     "source_sha256": baseline["source_sha256"], "time_base": baseline["time_base"],
                     "video_duration_ticks": baseline["video_duration_ticks"], "dimensions": baseline["dimensions"],
                     "frame_count": 4763, "completed_frames": 4763,
                     "labels": [{"index": i, "name": name} for i, name in enumerate(timeline.FRAME_LABEL_NAMES)],
                     "frames": [{k: row[k] for k in ("frame", "pts", "duration_ticks", "original_frame")} |
                                {"label_map": f"frame_labels/F{row['frame']:06d}.png", "status": "needs_review"}
                                for row in baseline["frames"]]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frames.json"
            path.write_text(json.dumps(partition))
            result = timeline.build_bindings(self.project, frame_layer_manifest=path)
            self.assertEqual(result["summary"]["frame_visible_partition"], 4763)
            self.assertEqual(result["summary"]["source_fallback"], 0)
            self.assertEqual(result["frames"][4021]["composition"]["semantic_status"], "needs_review")
            self.assertTrue(result["frames"][4021]["composition"]["does_not_imply_clean_cel"])
            partition["frames"][4022]["pts"] = partition["frames"][4021]["pts"]
            path.write_text(json.dumps(partition))
            with self.assertRaises(ValueError):
                timeline.build_bindings(self.project, frame_layer_manifest=path)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg integration dependency unavailable")
class ExactVideoIntegrationTests(unittest.TestCase):
    def test_lossless_rgb_exact_variable_pts_tail_and_full_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pts = [0, 528, 1072, 1600, 2128, 2672]
            rows = timeline.validated_timeline([{"frame": i, "pts": p} for i, p in enumerate(pts)], "1/16000", 3205)
            paths = []
            colors = [(173, 0, 3), (213, 167, 169), (255, 226, 211),
                      (0, 0, 0), (238, 238, 238), (185, 150, 30)]
            for i in range(len(rows)):
                path = root / f"{i}.png"
                image = Image.new("RGB", (64, 64), colors[i])
                image.putpixel((i + 1, i + 1), (i, 255 - i, 125))
                image.save(path)
                paths.append(path)
            audio = root / "audio.m4a"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
                            "-t", "0.25", "-c:a", "aac", str(audio)], check=True)
            output = root / "movie.mp4"
            timeline.encode_exact(paths, rows, "1/16000", output, audio)
            report = timeline.verify_movie(output, rows, "1/16000", paths, audio, expected_dimensions=[64, 64])
            self.assertTrue(report["all_frame_rgb_equal"])
            self.assertTrue(report["audio_packet_copy_equal"])
            self.assertEqual(report["final_frame_duration_ticks"], 533)
            self.assertGreater(report["audio"]["duration_ticks"] / 48000, 3205 / 16000)
            for index in (0, 1, 4, 5):
                decoded = timeline.decode_frame_at_pts(output, rows[index]["pts"], "1/16000", [64, 64])
                self.assertEqual(decoded, Image.open(paths[index]).convert("RGB").tobytes())
            preview = root / "preview.mp4"
            timeline.transcode_preview(output, preview)
            preview_report = timeline.verify_movie(preview, rows, "1/16000", source_audio=audio,
                                                   expected_color_metadata=timeline.PREVIEW_COLOR_METADATA)
            self.assertIsNone(preview_report["all_frame_rgb_equal"])
            self.assertTrue(preview_report["audio_packet_copy_equal"])
            self.assertEqual(preview_report["final_frame_duration_ticks"], 533)
            self.assertEqual(preview_report["color_metadata"], timeline.PREVIEW_COLOR_METADATA)
            direct_preview = root / "direct-preview.mp4"
            timeline.encode_exact(paths, rows, "1/16000", direct_preview, audio, preview=True)
            direct_report = timeline.verify_movie(direct_preview, rows, "1/16000", source_audio=audio,
                                                   expected_color_metadata=timeline.PREVIEW_COLOR_METADATA)
            self.assertEqual(direct_report["color_metadata"], timeline.PREVIEW_COLOR_METADATA)
            import numpy as np
            for variant in (preview, direct_preview):
                for index in (0, 1, 2, 5):
                    decoded = timeline.decode_frame_at_pts(variant, rows[index]["pts"], "1/16000", [64, 64])
                    rgb = np.frombuffer(decoded, dtype=np.uint8).reshape(64, 64, 3)
                    median = np.median(rgb[12:52, 12:52], axis=(0, 1))
                    self.assertLessEqual(float(np.max(np.abs(median - colors[index]))), 4.0)
            with self.assertRaises(ValueError):
                timeline.verify_movie(output, rows, "1/16000", expected_color_metadata=timeline.PREVIEW_COLOR_METADATA)
            color_check = timeline.verify_preview_colors(preview, output, rows, "1/16000", [64, 64], sample_frames=[0, 1, 2, 5])
            self.assertEqual(color_check["status"], "pass")
            self.assertEqual(color_check["sample_count"], 4)
            with self.assertRaises(ValueError):
                timeline.encode_exact(paths, rows, "1/16000", output, audio)


if __name__ == "__main__":
    unittest.main()
