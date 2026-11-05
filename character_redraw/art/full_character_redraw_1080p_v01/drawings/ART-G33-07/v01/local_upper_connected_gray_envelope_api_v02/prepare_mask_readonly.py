"""Prepare an alpha-only edit mask and display QA; never edit target art or call API."""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RUN = Path(__file__).resolve().parent
BASE = RUN.parents[3]
PARENT = RUN.parent
TARGET = PARENT / 'whole_imggen_user_scale_correction_preserve_spiral_v11/character_imggen_original.png'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(TARGET) == '128d9e7ae103f5904b4a2a13cdbb817661595c93522a3cc12d4a0b482fd4f3b3'
im = Image.open(TARGET).convert('RGBA')
assert im.size == (956, 1645)
references = [
    (TARGET, 'ref1_TARGET_V11_EXACT_RGBA.png'),
    (BASE / 'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png', 'ref2_LATEST_USER_BROAD_GRAY_INNER_RETURN_DETAIL.png'),
    (PARENT / 'whole_imggen_source2333_visible_horizontal_hairphase_v14/inputs/ref5_UNLIT_GRAY_MINT_INK_MATERIAL_KEY.png', 'ref3_UNLIT_GRAY_MINT_INK_MATERIAL_KEY.png'),
    (PARENT / 'whole_imggen_source2333_visible_horizontal_hairphase_v14/inputs/ref1_ORIGINAL2333_COMPLETE_UNMASKED_ACTION.png', 'ref4_ORIGINAL2333_COMPLETE_UNMASKED_ACTION_GUIDE.png'),
]
for source, name in references:
    target = RUN / 'inputs' / name
    assert not target.exists()
    shutil.copy2(source, target)
    assert sha(source) == sha(target)

# This is an editable workspace, not a required replacement silhouette. The
# manually observed upper-turn envelope has only a few pixels of spare air.
upper_polygon = [
    (608, 372), (615, 352), (639, 336), (658, 329), (680, 330),
    (705, 341), (727, 354), (741, 367), (745, 385), (742, 406),
    (730, 426), (710, 441), (690, 443), (670, 433), (653, 420),
    (636, 414), (620, 406), (609, 392),
]
upper = Image.new('L', im.size, 0)
ImageDraw.Draw(upper).polygon(upper_polygon, fill=255)

# Lower return and C retain their exact outer path, ink boundaries, mint band,
# tip and alpha windows. Only neutral interior gray surfaces can change color.
lower_envelope = [(721, 365), (751, 369), (770, 381), (777, 404),
                  (774, 422), (793, 420), (808, 435), (811, 453),
                  (806, 466), (795, 475), (782, 476), (773, 466),
                  (768, 458), (749, 460), (729, 453), (714, 442)]
lower = Image.new('L', im.size, 0)
ImageDraw.Draw(lower).polygon(lower_envelope, fill=255)
ar = np.array(im)
rgb = ar[:, :, :3].astype(int)
alpha = ar[:, :, 3]
neutral = ((np.abs(rgb[:, :, 0] - rgb[:, :, 1]) <= 12)
           & (np.abs(rgb[:, :, 1] - rgb[:, :, 2]) <= 12)
           & (rgb.min(axis=2) > 65) & (rgb.max(axis=2) < 230)
           & (alpha > 128) & (np.array(lower) > 0))
lower_material = Image.fromarray(neutral.astype('uint8') * 255).filter(ImageFilter.MinFilter(5))

# Explicit protection for the complete head/bob, original clothes and both
# red beads. The protection masks are alpha-mask geometry, not new art pixels.
head = Image.new('L', im.size, 0)
ImageDraw.Draw(head).polygon([(0, 0), (956, 0), (956, 312), (701, 312),
                             (682, 329), (665, 340), (649, 340), (628, 330),
                             (600, 340), (600, 1645), (0, 1645)], fill=255)
body = Image.new('L', im.size, 0)
ImageDraw.Draw(body).polygon([(0, 418), (632, 418), (653, 425), (667, 447),
                             (689, 470), (704, 1645), (0, 1645)], fill=255)
red = ((rgb[:, :, 0] > 120) & (rgb[:, :, 0] > rgb[:, :, 1] * 1.6)
       & (rgb[:, :, 0] > rgb[:, :, 2] * 1.6) & (alpha > 16))
beads = Image.fromarray(red.astype('uint8') * 255).filter(ImageFilter.MaxFilter(7))
white = (rgb.min(axis=2) > 223) & (alpha > 128)
white_guard = Image.fromarray(white.astype('uint8') * 255).filter(ImageFilter.MaxFilter(5))
protected = ((np.array(head) > 0) | (np.array(body) > 0)
             | (np.array(beads) > 0) | (np.array(white_guard) > 0))
editable = ((np.array(upper) > 0) | (np.array(lower_material) > 0)) & ~protected
assert not np.any(editable & (np.array(beads) > 0))
assert not np.any(editable & (np.array(head) > 0))
assert not np.any(editable & (np.array(body) > 0))

mask = np.full((im.height, im.width, 4), 255, dtype=np.uint8)
mask[editable, 3] = 0
mask_path = RUN / 'mask_COIL_UPPER_GEOMETRY_LOWER_GRAY_INTERIORS_v01.png'
assert not mask_path.exists()
Image.fromarray(mask).save(mask_path)
Image.fromarray(np.where(editable, 255, 0).astype('uint8')).save(RUN / 'qa_readonly/EDITABLE_WORKSPACE_BINARY_READONLY.png')
for bg, label in [((255, 255, 255), 'white'), ((0, 0, 0), 'black')]:
    display = Image.alpha_composite(Image.new('RGBA', im.size, bg + (255,)), im)
    overlay = np.zeros((im.height, im.width, 4), dtype=np.uint8)
    overlay[editable] = (255, 0, 160, 100)
    display = Image.alpha_composite(display, Image.fromarray(overlay)).convert('RGB')
    display.save(RUN / f'qa_readonly/MASK_OVERLAY_FULL_{label}_READONLY.png')
    display.crop((580, 305, 835, 500)).resize((1020, 780), Image.Resampling.NEAREST).save(
        RUN / f'qa_readonly/MASK_OVERLAY_ROOT_COIL_C_4x_{label}_READONLY.png')
    display.crop((535, 290, 845, 590)).resize((930, 900), Image.Resampling.NEAREST).save(
        RUN / f'qa_readonly/MASK_OVERLAY_HEAD_FRILL_PROTECTION_3x_{label}_READONLY.png')

provenance = {
    'target': {'path': str(TARGET), 'sha256': sha(TARGET), 'size': list(im.size)},
    'input_copies': [{'source': str(s), 'copy': str(RUN / 'inputs' / n), 'sha256': sha(s)} for s, n in references],
    'mask': {'path': str(mask_path), 'sha256': sha(mask_path), 'size': list(im.size), 'mode': 'RGBA',
             'alpha_semantics': '0 editable,255 protected; first InputImages file only',
             'editable_pixel_count': int(editable.sum()),
             'editable_bbox_xyxy': list(Image.fromarray(editable.astype('uint8') * 255).getbbox())},
    'upper_polygon_xy': upper_polygon,
    'lower_material_envelope_xy': lower_envelope,
    'lower_material_rule': 'Neutral opaque-gray interiors only, eroded2pixels; no mint/ink/alpha-outline or Cpath relocation.',
    'protected_head_polygon': [(0, 0), (956, 0), (956, 312), (701, 312), (682, 329), (665, 340), (649, 340), (628, 330), (600, 340), (600, 1645), (0, 1645)],
    'protected_body_polygon': [(0, 418), (632, 418), (653, 425), (667, 447), (689, 470), (704, 1645), (0, 1645)],
    'protection': ['All redbeads and3px dilation', 'head/bob/face', 'whitecap/frill2px safety', 'clothes/body/limbs', 'lowerC outer ink/mint and air windows'],
    'qa_only_crop_xyxy': [580, 305, 835, 500],
    'readonly_art_pixel_operations': 'Exactcopies and RGBA alpha-composites/crops/display-resizes only. No target RGB/alpha repair, rotation, paste, erase or redraw.',
    'generation_calls': 0, 'api_calls': 0, 'network_calls': 0,
    'root_release_recorded': False, 'requires_root_actual_input_and_mask_review': True,
}
(RUN / 'MASK_PROVENANCE_DRAFT_v01.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(provenance['mask'], ensure_ascii=False))
