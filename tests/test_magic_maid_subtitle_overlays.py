"""Synthetic contract tests; these do not replace source-image semantic QA."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/magic_maid_subtitle_overlays.py"
SPEC = importlib.util.spec_from_file_location("subtitle_under_test", SCRIPT)
sub = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sub
SPEC.loader.exec_module(sub)


class SubtitleContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        sub.configure_project(self.project)

    def tearDown(self):
        self.temp.cleanup()

    def make_manifest(self, **entry_updates):
        folder = self.project / "data/subtitle_templates"
        folder.mkdir(parents=True, exist_ok=True)
        alpha = np.zeros(sub.CANVAS, np.uint8)
        alpha[50:80, 90:140] = 192
        path = folder / "test_alpha.png"
        Image.fromarray(alpha).save(path)
        entry = {"id": "synthetic_parser_fixture_not_source_evidence", "frame_ranges": [[20, 30]],
                 "source_frames": [20, 23], "source_rgb_sha256": {"20": "1"*64, "23": "2"*64},
                 "ink_rgb": [255, 255, 255], "alpha_path": "data/subtitle_templates/test_alpha.png",
                 "alpha_sha256": sub.sha256(path), "recommended_stack_position": "front_of_subject",
                 "glyph_completeness": "incomplete_observed_glyph"}
        entry.update(entry_updates)
        payload = {"schema": sub.TEMPLATE_SCHEMA, "dimensions": [1920, 1080],
                   "source_video_sha256": sub.SOURCE_VIDEO_SHA256, "templates": [entry]}
        manifest = folder / "manifest.json"
        manifest.write_text(json.dumps(payload))
        return manifest, path, alpha

    def test_no_templates_does_not_create_data(self):
        self.assertEqual(sub.DATA_DEPENDENCIES, ())
        self.assertEqual(list(self.project.iterdir()), [])

    def test_none_is_explicit_empty_and_preserves_readonly_input(self):
        rgb = np.full((*sub.CANVAS, 3), 127, np.uint8)
        rgb.setflags(write=False)
        before = hashlib.sha256(rgb.tobytes()).hexdigest()
        rgba, meta = sub.extract_overlay(rgb, 0, "M00", "")
        self.assertEqual(rgba.shape, (*sub.CANVAS, 4))
        self.assertEqual(rgba.dtype, np.uint8)
        self.assertFalse(np.any(rgba))
        self.assertEqual(meta["status"], "no_text_expected")
        self.assertEqual(hashlib.sha256(rgb.tobytes()).hexdigest(), before)
        json.dumps(meta, allow_nan=False)

    def test_unsupported_never_returns_original_frame(self):
        rgba, meta = sub.extract_overlay(np.full((*sub.CANVAS, 3), 255, np.uint8), 123, "unknown", "")
        self.assertFalse(np.any(rgba))
        self.assertEqual(meta["status"], "unsupported_scene")

    def test_input_contract_rejects_bad_shapes_types_and_frames(self):
        good = np.zeros((*sub.CANVAS, 3), np.uint8)
        for bad in (good.astype(float), good[:, :, :2], good[:2]):
            with self.assertRaises(ValueError):
                sub.extract_overlay(bad, 20, "M01", "G01")
        for bad_frame in (-1, 4763, 2.5, True):
            with self.assertRaises(ValueError):
                sub.extract_overlay(good, bad_frame, "M01", "G01")

    def test_analytic_matte_has_correct_fraction_and_residual(self):
        bg, fg = np.array([200, 100, 150]), np.array([240, 240, 240])
        source = np.stack((bg, (bg+fg)/2, fg))
        alpha, residual = sub._matte(source, bg, fg)
        np.testing.assert_allclose(alpha, [0, .5, 1], atol=1e-6)
        self.assertLess(float(residual.max()), 1e-5)

    def test_identical_background_foreground_is_unobservable(self):
        alpha, _ = sub._matte(np.full((4, 3), 237), [237]*3, [237]*3)
        self.assertFalse(np.any(alpha))

    def test_rgba_zero_rgb_outside_alpha(self):
        alpha = np.array([[0, 1], [127, 255]], np.uint8)
        rgba = sub._rgba(alpha, [237, 238, 239])
        self.assertFalse(rgba[0, 0].any())
        np.testing.assert_array_equal(rgba[alpha>0, :3], np.array([[237,238,239]]*3))

    def test_edge_matte_retains_soft_source_edge_and_rejects_chromatic_noise(self):
        bg = np.array([240, 170, 190], np.uint8)
        rgb = np.broadcast_to(bg, (30, 30, 3)).copy()
        core = np.zeros((30, 30), bool)
        core[10:20, 10:20] = True
        rgb[core] = 250
        rgb[9, 12] = np.rint((bg.astype(float)+250)/2).astype(np.uint8)
        rgb[9, 13] = [30, 200, 30]
        alpha = sub._edge_matte(rgb, core, [250]*3, bg)
        self.assertTrue(np.all(alpha[core] == 255))
        self.assertTrue(100 < alpha[9, 12] < 150)
        self.assertEqual(alpha[9, 13], 0)

    def test_connected_caption_bars_include_backing_and_enclosed_glyph(self):
        rgb = np.full((200, 200, 3), [245, 170, 185], np.uint8)
        backing = np.zeros((200, 200), bool)
        backing[20:160, 20:70] = True
        backing[110:160, 20:170] = True  # One L-shaped caption design.
        rgb[backing] = 46
        rgb[40:60, 35:55] = 237  # An enclosed glyph hole, kept with backing.
        out, metadata = sub._card_overlay(rgb, np.ones((200, 200), bool))
        np.testing.assert_array_equal(out[..., 3]>0, backing)
        np.testing.assert_array_equal(out[40:60,35:55,:3], rgb[40:60,35:55])
        self.assertEqual(metadata["backing_components"], 1)
        self.assertFalse(np.any(out[..., :3][out[..., 3]==0]))

    def test_white_caption_card_supported(self):
        rgb = np.full((150, 200, 3), [245, 170, 185], np.uint8)
        rgb[20:120, 30:170] = 237
        rgb[40:60, 50:70] = 46
        out, metadata = sub._card_overlay(rgb, np.ones((150,200), bool), (237,))
        self.assertEqual(metadata["backing_components"], 1)
        self.assertEqual(int(out[50,60,3]), 255)
        self.assertEqual(int(out[50,60,0]), 46)

    def test_m15_partial_card_keeps_curved_visible_backing_not_exterior_ink(self):
        rgb = np.full((240, 360, 3), [213, 167, 169], np.uint8)
        backing = np.zeros((240, 360), bool)
        backing[20:200, 20:300] = True
        yy, xx = np.indices(backing.shape)
        exterior_ink = backing & (yy >= 60 + (xx-20)**2 / 650)
        visible = backing & ~exterior_ink
        rgb[backing] = 237
        rgb[exterior_ink] = 46
        rgb[30:40, 40:50] = 46  # A fully observed, enclosed glyph hole.
        rgb[220:224, 310:314] = 237  # Tiny isolated noise must stay excluded.
        before, _ = sub._card_overlay(rgb, np.ones(backing.shape, bool), (237,))
        self.assertFalse(before.any())
        after, _ = sub._card_overlay(rgb, np.ones(backing.shape, bool), (237,), visible_partial_card=True)
        np.testing.assert_array_equal(after[..., 3] > 0, visible)
        np.testing.assert_array_equal(after[..., :3][visible], rgb[visible])
        self.assertFalse(after[exterior_ink].any())
        self.assertFalse(after[220:224, 310:314].any())
        self.assertEqual(int(after[35, 45, 0]), 46)
        self.assertEqual(int(after[35, 45, 3]), 255)

    def test_partial_card_mode_is_white_only_and_exact_phase_only(self):
        rgb = np.full((*sub.CANVAS, 3), [213, 167, 169], np.uint8)
        rgb[240:1000, 205:455] = 237
        with self.assertRaisesRegex(ValueError, "restricted"):
            sub._card_overlay(rgb, np.ones(sub.CANVAS, bool), (46,), visible_partial_card=True)
        for frame, chapter in [(1907, "M14"), (1944, "M15"), (1951, "M15"), (1961, "M15"), (1908, "M10")]:
            with self.subTest(frame=frame, chapter=chapter):
                _, metadata = sub.extract_overlay(rgb, frame, chapter, "")
                self.assertNotIn("observed_partial_card", metadata)
        _, metadata = sub.extract_overlay(rgb, 1908, "M15", "X03")
        self.assertTrue(metadata["observed_partial_card"])
        self.assertFalse(metadata["hidden_glyph_completion"])
        self.assertEqual(metadata["glyph_completeness"], "incomplete_observed_glyph")

    def test_ornamental_excludes_frame_and_white_backing(self):
        rgb = np.full((250, 300, 3), [245, 170, 185], np.uint8)
        rgb[20:230, 20:280] = 0
        rgb[30:220, 30:270] = 255
        rgb[70:110, 80:120] = 0
        alpha = sub._ornamental_glyphs(rgb, np.ones((250,300), bool))
        self.assertEqual(int(alpha[90,100]), 255)
        self.assertEqual(int(alpha[25,25]), 0)
        self.assertEqual(int(alpha[150,150]), 0)

    def test_color_level_255_not_costume_237_when_modal(self):
        rgb = np.full((20,20,3), 255, np.uint8)
        rgb[:2] = 237
        self.assertEqual(sub._fg_level(rgb, np.ones((20,20), bool), 237), 255)

    def test_source_phase_boundaries(self):
        self.assertEqual(sub._source_rule(1943,"M15","").kind, "card")
        self.assertEqual(sub._source_rule(1944,"M15","").kind, "none")
        self.assertEqual(sub._source_rule(1950,"M15","").kind, "none")
        self.assertEqual(sub._source_rule(1951,"M15","").kind, "small")
        self.assertEqual(sub._source_rule(1961,"M15","").kind, "none")
        self.assertEqual(sub._source_rule(2058,"M16","").kind, "clear")
        self.assertEqual(sub._source_rule(2059,"M16","").kind, "front")
        self.assertEqual(sub._source_rule(4279,"M30","").kind, "dark")
        self.assertEqual(sub._source_rule(4280,"M30","").kind, "large_front")
        self.assertEqual(sub._source_rule(1158,"M09","").kind, "large")
        self.assertEqual(sub._source_rule(1159,"M09","").kind, "card")

    def test_large_back_caption_stack_not_claimed_foreground(self):
        for chapter in ("M09","M19","M24","M29"):
            self.assertEqual(sub._source_rule(1000, chapter, "").stack, "behind_subject")

    def test_template_registers_exact_dependencies_and_preserves_alpha(self):
        _, _, alpha = self.make_manifest()
        sub.configure_project(self.project)
        self.assertEqual(len(sub.DATA_DEPENDENCIES), 2)
        rgb = np.zeros((*sub.CANVAS,3), np.uint8)
        rgb.setflags(write=False)
        rgba, metadata = sub.extract_overlay(rgb, 20, "M01", "")
        np.testing.assert_array_equal(rgba[...,3], alpha)
        self.assertTrue(metadata["temporal_template_available"])
        self.assertEqual(metadata["glyph_completeness"], "incomplete_observed_glyph")
        self.assertFalse(metadata["production_clean_claimed"])
        self.assertIsNone(sub._template_for(30))
        json.dumps(metadata, allow_nan=False)

    def test_template_requires_source_hash_evidence(self):
        self.make_manifest(source_rgb_sha256={})
        with self.assertRaisesRegex(ValueError, "RGB hash"):
            sub.configure_project(self.project)

    def test_template_rejects_changed_alpha(self):
        _, path, _ = self.make_manifest()
        path.write_bytes(b"not the observed alpha")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            sub.configure_project(self.project)

    def test_lazy_load_rechecks_template_after_configuration(self):
        _, path, _ = self.make_manifest()
        sub.configure_project(self.project)
        path.write_bytes(b"changed after configuration")
        with self.assertRaisesRegex(ValueError, "changed after"):
            sub._template_alpha(sub._template_for(20))

    def test_project_switch_drops_cached_templates(self):
        self.make_manifest()
        sub.configure_project(self.project)
        self.assertIsNotNone(sub._template_for(20))
        other = self.project / "other_project"
        other.mkdir()
        sub.configure_project(other)
        self.assertEqual(sub.DATA_DEPENDENCIES, ())
        self.assertIsNone(sub._template_for(20))

    def test_hash_evidence_must_be_hexadecimal(self):
        self.make_manifest(source_rgb_sha256={"20": "z"*64, "23": "2"*64})
        with self.assertRaisesRegex(ValueError, "RGB hash"):
            sub.configure_project(self.project)

    def test_template_builder_refuses_missing_or_wrong_original(self):
        with self.assertRaises(ValueError):
            sub.build_templates(self.project, [{"id": "not_a_real_observation"}])
        source = self.project / "source"
        source.mkdir()
        (source / "original.mp4").write_bytes(b"wrong video")
        with self.assertRaisesRegex(ValueError, "expected original"):
            sub.build_templates(self.project, [{"id": "not_a_real_observation"}])
        self.assertFalse((self.project / "data").exists())

    def test_template_rejects_unsafe_paths(self):
        self.make_manifest(alpha_path="../outside.png")
        with self.assertRaises(ValueError):
            sub.configure_project(self.project)

    def test_template_rejects_overlap_and_wrong_original(self):
        manifest, _, _ = self.make_manifest()
        data = json.loads(manifest.read_text())
        second = dict(data["templates"][0], id="second")
        data["templates"].append(second)
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            sub.configure_project(self.project)
        data["templates"] = data["templates"][:1]
        data["source_video_sha256"] = "0"*64
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "different original"):
            sub.configure_project(self.project)

    def test_template_rejects_symlinked_asset(self):
        _, path, _ = self.make_manifest()
        other = self.project / "other.png"
        path.rename(other)
        path.symlink_to(other)
        with self.assertRaisesRegex(ValueError, "Symlinked"):
            sub.configure_project(self.project)

    def test_combine_observations_only_keeps_observed_quorum(self):
        a, b = np.zeros(sub.CANVAS,np.uint8), np.zeros(sub.CANVAS,np.uint8)
        a[10:20,10:20], b[10:20,10:20] = 128, 200
        a[30:40,30:40] = 255
        result = sub.combine_observations([a,b], 2)
        self.assertTrue(np.all(result[10:20,10:20] == 200))
        self.assertFalse(np.any(result[30:40,30:40]))
        self.assertFalse(np.any(result[(a==0)&(b==0)]))

    def test_output_cannot_overwrite_sources_or_existing_review(self):
        for relative in ("source/new", "data/new", "layers/new", "frames/new", "../escape"):
            with self.assertRaises(ValueError):
                sub._new_output(self.project, relative)
        target = self.project / "overlays_review/run"
        target.mkdir(parents=True)
        (target / "already.png").write_bytes(b"existing")
        with self.assertRaises(ValueError):
            sub._new_output(self.project, "overlays_review/run")

    def test_missing_required_template_is_not_no_text_expected(self):
        rgb=np.full((*sub.CANVAS,3),(213,167,169),np.uint8)
        _,meta=sub.extract_overlay(rgb,752,"M08","G09")
        self.assertEqual(meta['status'],'missing_required_template')
        self.assertEqual(meta['template_status'],'missing_required_source_observed_template')

    def test_progressive_visibility_and_orange_occlusion(self):
        rgba=np.zeros((*sub.CANVAS,4),np.uint8);rgba[500:510,100:110]=255;rgba[500:510,700:710]=255
        rgb=np.full((*sub.CANVAS,3),(213,167,169),np.uint8)
        entry={'visibility_regions':[{'box':[640,0,1280,1080],'start_frame':4410,'end_frame_exclusive':4431}]}
        out,_=sub._template_visibility(rgba.copy(),rgb,entry,4409)
        self.assertTrue(out[500:510,100:110].any());self.assertFalse(out[500:510,700:710].any())
        rgb[500:510,100:110]=[255,158,22]
        out,notes=sub._template_visibility(rgba.copy(),rgb,{'mask_observed_orange_occlusion':True},2142)
        self.assertFalse(out[500:510,100:110].any());self.assertEqual(notes['source_observed_orange_occluded_pixels'],100)

    def test_styled_flat_source_recovers_white_and_observed_shadow(self):
        sys.path.insert(0,str(SCRIPT.parent))
        import magic_maid_subtitle_templates as recipe
        rgb=np.full((*sub.CANVAS,3),(255,158,22),np.uint8)
        rgb[505:525,505:525]=[102,63,9]
        rgb[500:520,500:520]=255
        rgba,notes=recipe.styled_flat_observation(rgb)
        self.assertEqual(int(rgba[510,510,3]),255)
        self.assertTrue(140<int(rgba[522,522,3])<170)
        self.assertLess(int(rgba[522,522,:3].max()),3)
        self.assertLess(notes['recomposition_mae_rgb'],.1)
        self.assertFalse(np.any(rgba[...,:3][rgba[...,3]==0]))


PROJECT=SCRIPT.parents[1]/'magic_maid_20261029'
@unittest.skipUnless((PROJECT/'frames/F004547.png').is_file() and
                     (PROJECT/'data/subtitle_templates/manifest.json').is_file(),
                     'Real original-frame cache and reviewed template assets are required')
class SourceRegressionTests(unittest.TestCase):
    def setUp(self):
        sub.configure_project(PROJECT)

    def extract(self,frame,chapter,group=''):
        rgb=np.array(Image.open(PROJECT/f'frames/F{frame:06d}.png').convert('RGB'))
        rgb.setflags(write=False)
        return sub.extract_overlay(rgb,frame,chapter,group)

    def test_small_255_glyphs_not_dropped(self):
        for frame,chapter,minimum in [(381,'M04',3000),(463,'M05',7000)]:
            rgba,metadata=self.extract(frame,chapter)
            self.assertGreater(metadata['nonzero_alpha_pixels'],minimum)
            self.assertEqual(metadata['foreground_color'],[255]*3)

    def test_ring_text_is_owned_only_in_its_observed_phase(self):
        for frame in [1951,1960]:
            rgba,meta=self.extract(frame,'M15','X03')
            self.assertGreater(meta['nonzero_alpha_pixels'],1000)
            self.assertFalse(rgba[:350].any())
        self.assertFalse(self.extract(1961,'M15','X03')[0].any())

    def test_m15_ink_cut_white_cards_first_middle_last_and_boundaries(self):
        first, meta = self.extract(1908, 'M15', 'X03')
        self.assertGreater(meta['nonzero_alpha_pixels'], 70000)
        self.assertTrue(meta['observed_partial_card'])
        self.assertFalse(meta['hidden_glyph_completion'])
        self.assertEqual(int(first[250, 220, 3]), 255)
        self.assertEqual(int(first[600, 1480, 3]), 255)
        self.assertEqual(int(first[700, 300, 3]), 0)  # Exterior-connected black ink.
        middle, _ = self.extract(1918, 'M15', 'X03')
        last, last_meta = self.extract(1943, 'M15', 'X03')
        self.assertGreater(np.count_nonzero(middle[..., 3]), 330000)
        self.assertEqual(last_meta['nonzero_alpha_pixels'], 360503)
        self.assertEqual(hashlib.sha256(last.tobytes()).hexdigest(), '45ffe2171b151d557d1178b9c473fade1916bb56afe392819a24e8d296c22b95')
        _, before_meta = self.extract(1907, 'M14', 'G27')
        after, after_meta = self.extract(1944, 'M15', 'X03')
        self.assertNotIn('observed_partial_card', before_meta)
        self.assertFalse(after.any())
        self.assertNotIn('observed_partial_card', after_meta)

    def test_m15_all_36_frames_copy_visible_source_only_and_no_extra_dark_ink(self):
        reference_rgb = np.array(Image.open(PROJECT/'frames/F001930.png').convert('RGB'))
        reference, _ = self.extract(1930, 'M15', 'X03')
        # QA reference only: extraction never loads a different caption frame.
        visible_glyph_positions = sub.ndi.binary_dilation((reference[...,3] > 0) & (reference_rgb.max(axis=-1) < 180), iterations=3)
        for frame in range(1908, 1944):
            with self.subTest(frame=frame):
                rgb = np.array(Image.open(PROJECT/f'frames/F{frame:06d}.png').convert('RGB'))
                rgb.setflags(write=False)
                before = hashlib.sha256(rgb.tobytes()).hexdigest()
                rgba, metadata = sub.extract_overlay(rgb, frame, 'M15', 'X03')
                selected = rgba[...,3] > 0
                self.assertTrue(selected.any())
                np.testing.assert_array_equal(rgba[...,:3][selected], rgb[selected])
                self.assertFalse(np.any(selected & (rgb.max(axis=-1) < 180) & ~visible_glyph_positions))
                self.assertEqual(hashlib.sha256(rgb.tobytes()).hexdigest(), before)
                self.assertFalse(metadata['hidden_glyph_completion'])

    def test_black_vertical_caption_keeps_all_three_characters(self):
        rgba,meta=self.extract(4279,'M30','X05')
        self.assertEqual(meta['foreground_color'],[46]*3)
        self.assertGreater(np.count_nonzero(rgba[:350,:,3]),2000)
        self.assertGreater(np.count_nonzero(rgba[850:,:,3]),2000)

    def test_m08_observed_template_contains_shadow_not_eyes(self):
        rgba,meta=self.extract(792,'M08','G11')
        reference,_=self.extract(820,'M08','G11')
        np.testing.assert_array_equal(rgba,reference)
        self.assertIn('observed_dark_shadow',meta['style_components'])
        self.assertFalse(rgba[:460].any());self.assertFalse(rgba[650:].any())

    def test_orange_transitions_do_not_receive_static_text(self):
        for frame,chapter in [(2147,'M16'),(3372,'M23')]:
            rgba,meta=self.extract(frame,chapter)
            self.assertFalse(rgba.any())
            self.assertEqual(meta['status'],'caption_not_visible_in_current_source_phase')

    def test_progressive_m33_is_not_early_full_sentence(self):
        early,_=self.extract(4409,'M33');middle,_=self.extract(4410,'M33');late,_=self.extract(4418,'M33')
        self.assertFalse(early[:,640:].any());self.assertTrue(middle[:,640:1280].any())
        self.assertFalse(middle[:,1280:].any());self.assertTrue(late[:,1280:].any())

    def test_m30_center_uses_verified_original_same_word(self):
        early,_=self.extract(4285,'M30');middle,meta=self.extract(4286,'M30');late,_=self.extract(4294,'M30')
        self.assertFalse(early[:,640:].any());self.assertTrue(middle[:,640:1280].any())
        self.assertFalse(middle[:,1280:].any());self.assertTrue(late[:,1280:].any())
        self.assertEqual(meta['template_id'],'m30_observed_m33_reuse')

    def test_m35_has_no_headband_or_lower_left_sleeve_blob(self):
        rgba,meta=self.extract(4547,'M35','G50')
        self.assertFalse(rgba[300:800].any())
        self.assertFalse(rgba[850:,:900].any())
        self.assertFalse(rgba[120,480].any())
        self.assertEqual(meta['glyph_completeness'],'incomplete_observed_glyph')

    def test_m23_costume_contacts_are_not_subtitle_pixels(self):
        rgba,meta=self.extract(3330,'M23','G45')
        self.assertFalse(rgba[480,800].any())
        self.assertFalse(rgba[610,1200].any())
        self.assertEqual(meta['glyph_completeness'],'incomplete_observed_glyph')


if __name__ == "__main__":
    unittest.main()
