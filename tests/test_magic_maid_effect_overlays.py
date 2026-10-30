"""Source-free contracts; these do NOT substitute for native source review."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import magic_maid_effect_overlays as fx


class EffectMatteTests(unittest.TestCase):
    def plane(self, h=160, w=240):
        return np.broadcast_to(np.array(fx.PINK,np.uint8),(h,w,3)).copy()

    def test_input_contract(self):
        for rgb in (np.zeros((2,2)),np.zeros((2,2,4),np.uint8),np.zeros((2,2,3))):
            with self.assertRaises(ValueError):
                fx.extract_overlay(rgb,4000,"M27","X05")
        for frame in (-1,4763,True,1.5):
            with self.assertRaises(ValueError):
                fx.extract_overlay(self.plane(),frame,"M27","X05")

    def test_readonly_input_and_json_metadata(self):
        rgb = self.plane()
        rgb[40:80,80:120] = fx.PETAL
        before = rgb.copy()
        rgb.flags.writeable = False
        rgba,meta = fx.extract_overlay(rgb,4000,"M27","X05")
        self.assertTrue(np.array_equal(rgb,before))
        self.assertEqual(rgba.dtype,np.uint8)
        self.assertEqual(rgba.shape,(160,240,4))
        self.assertTrue(np.all(rgba[...,:3][rgba[...,3]==0]==0))
        json.dumps(meta,allow_nan=False)
        self.assertFalse(meta["full_source_fallback"])

    def test_unknown_scene_never_returns_source(self):
        rgb = self.plane()
        rgb[:] = fx.PETAL
        rgba,meta = fx.extract_overlay(rgb,4000,"unknown","X05")
        self.assertFalse(rgba.any())
        self.assertEqual(meta["status"],"unsupported_scene")

    def test_pink_plane_has_no_petals(self):
        rgba,_ = fx.extract_overlay(self.plane(),4000,"M27","X05")
        self.assertFalse(rgba.any())

    def test_fractional_alpha_removes_pink_contamination(self):
        rgb = self.plane()
        rgb[40:90,70:140] = np.rint(.4*np.array(fx.PETAL)+.6*np.array(fx.PINK))
        rgba,meta = fx.extract_overlay(rgb,4000,"M27","X05")
        self.assertLess(abs(float(np.median(rgba[45:85,75:135,3]))/255-.4),.04)
        self.assertTrue(np.all(rgba[45:85,75:135,:3]==fx.PETAL))
        self.assertGreater(meta["categories"][0]["partial_alpha_pixels"],100)

    def test_coherent_faint_petal_is_not_discarded(self):
        rgb = self.plane()
        rgb[40:90,70:140] = np.rint(.05*np.array(fx.PETAL)+.95*np.array(fx.PINK))
        rgba,_ = fx.extract_overlay(rgb,4000,"M27","X05")
        self.assertGreater(float(np.median(rgba[45:85,75:135,3])),7)
        self.assertLess(float(np.median(rgba[45:85,75:135,3])),23)

    def test_opaque_red_costume_not_magenta_petal(self):
        rgb = self.plane()
        rgb[30:140,80:160] = fx.RED
        rgba,_ = fx.extract_overlay(rgb,4200,"M29","X02")
        self.assertEqual(int(rgba[30:140,80:160,3].max()),0)

    def test_gold_after_reveal_not_an_effect(self):
        rgb = self.plane()
        rgb[50:70,100:120] = fx.ORANGE
        rgba,_ = fx.extract_overlay(rgb,847,"M09","G12")
        self.assertFalse(rgba.any())

    def test_isolated_cameo_colour_not_radial_ray(self):
        rgb = self.plane(216,384)
        rgb[85:95,191:201] = fx.RAY
        rgba,_ = fx.extract_overlay(rgb,2221,"M17","G31")
        self.assertFalse(rgba.any())

    def test_bread_protected_without_discarding_small_star(self):
        rgb = self.plane(216,384)
        rgb[80:92,184:196] = fx.ORANGE
        rgb[80:92,40:52] = fx.ORANGE
        rgba,_ = fx.extract_overlay(rgb,3330,"M23","G45")
        self.assertEqual(int(rgba[80:92,184:196,3].max()),0)
        self.assertEqual(int(rgba[85,45,3]),255)

    def test_broad_white_clothing_not_ghost(self):
        rgb = self.plane(216,384)
        rgb[10:180,50:230] = fx.WHITE
        rgba,_ = fx.extract_overlay(rgb,504,"M06","G07")
        self.assertEqual(int(rgba[30:160,80:200,3].max()),0)

    def test_black_fullscreen_requires_observed_black(self):
        rgba,meta = fx.extract_overlay(self.plane(),1821,"M14","G26")
        self.assertFalse(rgba.any())
        self.assertEqual(meta["status"],"unsupported_visible_effect")
        rgba,_ = fx.extract_overlay(np.zeros((30,50,3),np.uint8),1821,"M14","G26")
        self.assertTrue(np.all(rgba[...,3]==255))
        self.assertFalse(rgba[...,:3].any())

    def test_heart_keeps_observed_dark_outline(self):
        rgb = self.plane(216,384)
        rgb[85:110,180:205] = fx.BLACK
        rgb[88:107,183:202] = fx.RED
        rgba,_ = fx.extract_overlay(rgb,4320,"M30","X05")
        self.assertGreater(int(rgba[86,190,3]),245)
        self.assertLess(int(rgba[86,190,:3].max()),10)
        self.assertEqual(int(rgba[95,190,3]),255)

    def test_category_counts_match_actual_matte(self):
        rgb = self.plane()
        rgb[40:80,80:120] = fx.PETAL
        rgba,meta = fx.extract_overlay(rgb,4000,"M27","X05")
        self.assertEqual(meta["visible_pixels"],int((rgba[...,3]>0).sum()))
        self.assertEqual(meta["categories"][0]["partial_alpha_pixels"],
                         int(((rgba[...,3]>0)&(rgba[...,3]<255)).sum()))

    def ghost_strokes(self):
        yy,xx = np.ogrid[:100,:160]
        outer = np.sqrt((xx-80)**2+(yy-50)**2)
        eye = np.sqrt((xx-72)**2+(yy-48)**2)
        alpha = np.zeros((100,160),np.float32)
        alpha[(outer>=33)&(outer<=37)] = 1
        alpha[(eye>=3)&(eye<=5)] = 1
        # A half-covered inner-ink pixel must have opaque pink under it.
        alpha[50,114] = .5
        # A soft exterior skirt must not become opaque.
        alpha[50,118] = .4
        return fx._rgba_colour(fx.GHOST_INK,alpha)

    def test_raw_small_ghost_eye_survives_gap_closing(self):
        rgba,meta = fx._ghost_composite(self.ghost_strokes(),504)
        self.assertEqual(int(rgba[48,72,3]),0)
        self.assertEqual(int(rgba[65,80,3]),255)
        self.assertGreaterEqual(meta["raw_observed_loops_preserved"],2)

    def test_ghost_backing_under_inner_half_stroke(self):
        rgba,_ = fx._ghost_composite(self.ghost_strokes(),504)
        self.assertEqual(int(rgba[50,114,3]),255)
        expected = np.rint(.5*np.array(fx.GHOST_INK)+.5*np.array(fx.PINK))
        self.assertLess(int(np.max(np.abs(rgba[50,114,:3].astype(int)-expected))),3)

    def test_ghost_external_soft_alpha_not_filled(self):
        rgba,_ = fx._ghost_composite(self.ghost_strokes(),504)
        self.assertLess(int(rgba[50,118,3]),180)
        self.assertGreater(int(rgba[50,118,3]),30)

    def test_ghost_does_not_double_fade_opacity(self):
        stroke = self.ghost_strokes()
        stroke[...,3] = np.rint(stroke[...,3].astype(float)*.5).astype(np.uint8)
        rgba,_ = fx._ghost_composite(stroke,504)
        self.assertLessEqual(int(rgba[...,3].max()),129)
        self.assertGreater(int(rgba[65,80,3]),110)
        self.assertEqual(int(rgba[48,72,3]),0)

    def test_ghost_open_garment_crumbs_not_returned(self):
        alpha = np.zeros((100,160),np.float32)
        alpha[35:37,60:75] = .5
        rgba,_ = fx._ghost_composite(fx._rgba_colour(fx.GHOST_INK,alpha),504)
        self.assertFalse(rgba.any())

    def test_canvas_clipped_ghost_records_frame_specific_partial_body(self):
        alpha = np.zeros((100,160),np.float32)
        alpha[0:40,20:23] = 1
        rgba,meta = fx._ghost_composite(fx._rgba_colour(fx.GHOST_INK,alpha),591)
        self.assertGreater(int((rgba[...,3]>0).sum()),0)
        self.assertIn("canvas_clipped_body_not_completed",meta["partial_flags"])
        self.assertEqual(meta["canvas_clipped_contours"][0]["status"],"no_supported_pink_body")

    def test_project_configuration_and_declared_dependencies(self):
        old = fx._PROJECT
        try:
            with tempfile.TemporaryDirectory() as d:
                root = Path(d)
                target = root/fx.DATA_DEPENDENCIES[0]
                target.parent.mkdir(parents=True)
                Image.fromarray(self.plane(10,12)).save(target)
                fx.configure_project(root)
                a = fx._reference(fx.DATA_DEPENDENCIES[0])
                self.assertEqual(a.shape,(10,12,3))
                self.assertFalse(a.flags.writeable)
                fx.configure_project(root)
                self.assertIs(a,fx._reference(fx.DATA_DEPENDENCIES[0]))
                with self.assertRaises(ValueError):
                    fx._reference("../../unexpected.png")
        finally:
            fx.configure_project(old)

    def test_subtitle_relation_is_phase_specific(self):
        for frame,chapter,expected in ((805,"M08","below_subtitles"),
                                      (3368,"M23","above_subtitles"),
                                      (4000,"M27","mixed_or_uncertain")):
            _,meta = fx.extract_overlay(self.plane(),frame,chapter,"")
            self.assertEqual(meta["subtitle_relation"],expected)

    def test_native_f476_pink_body_and_real_eye_voids(self):
        root = Path(__file__).resolve().parents[1]/"magic_maid_20261029"
        path = root/"cels/G06-01/source.png"
        if not path.is_file():
            self.skipTest("native source fixture not restored")
        with Image.open(path) as im:
            source = np.array(im.convert("RGB"))
        rgba,meta = fx.extract_overlay(source,476,"M05","G06")
        self.assertGreater(int(rgba[550,1100,3]),240)  # Plate-contact ghost body.
        self.assertLess(int(rgba[375,585,3]),20)       # Real small source eye.
        self.assertLess(int(rgba[600,1160,3]),20)      # Large right eye.
        self.assertLess(int(rgba[640,1040,3]),20)      # Large left eye.
        self.assertEqual(int(rgba[500,900,3]),0)       # Actual plate, not FX.
        category=meta["categories"][0]
        self.assertEqual(category["source_supported_pink_body_pixels"],66635)
        self.assertEqual(category["protected_source_pink_eye_pixels"],4061)

    def test_native_f1956_ring_excludes_actual_left_of_center_lyric(self):
        root = Path(__file__).resolve().parents[1]/"magic_maid_20261029"
        path = root/"cels/X03-07/source.png"
        if not path.is_file():
            self.skipTest("native source fixture not restored")
        with Image.open(path) as im:
            source = np.array(im.convert("RGB"))
        rgba,meta = fx.extract_overlay(source,1956,"M15","X03")
        self.assertFalse(rgba[378:699,852:926].any())
        self.assertGreater(int((rgba[...,3]>0).sum()),1000)
        self.assertEqual(meta["subtitle_relation"],"below_subtitles")

    def test_horizontal_shutter_protects_isolated_same_colour_prop(self):
        rgb = self.plane()
        rgb[:30] = fx.RAY
        rgb[-30:] = fx.RAY
        rgb[70:80,100:110] = fx.RAY
        rgba,meta = fx.extract_overlay(rgb,2139,"M16","G29")
        self.assertEqual(int(rgba[10,10,3]),255)
        self.assertEqual(int(rgba[150,10,3]),255)
        self.assertFalse(rgba[60:100,90:120].any())
        self.assertEqual(meta["subtitle_relation"],"above_subtitles")
        for frame,chapter in ((2138,"M16"),(2153,"M17")):
            out,_ = fx.extract_overlay(rgb,frame,chapter,"")
            self.assertFalse(out.any())

    def test_native_horizontal_shutter_exact_phase_boundaries(self):
        root = Path(__file__).resolve().parents[1]/"magic_maid_20261029/frames"
        frames = (2138,2139,2152,2153)
        if not all((root/f"F{f:06}.png").is_file() for f in frames):
            self.skipTest("full decoded native source cache not restored")
        for frame in frames:
            with Image.open(root/f"F{frame:06}.png") as im:
                source = np.array(im.convert("RGB"))
            rgba,meta = fx.extract_overlay(source,frame,"M16" if frame<2153 else "M17","")
            if frame in (2138,2153):
                self.assertFalse(rgba.any())
            elif frame==2139:
                self.assertEqual(int(rgba[20,20,3]),255)
                self.assertEqual(int(rgba[1040,20,3]),255)
                self.assertEqual(int(rgba[500,960,3]),0)
                self.assertGreater(meta["visible_pixels"],1200000)
            else:
                self.assertTrue(np.all(rgba[...,3]==255))
                self.assertTrue(np.all(rgba[...,:3]==fx.RAY))


if __name__ == "__main__":
    unittest.main()
