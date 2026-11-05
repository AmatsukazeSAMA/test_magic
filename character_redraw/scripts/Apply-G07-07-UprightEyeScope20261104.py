"""Apply the user's frame-specific eye preview in a vertically flipped workspace.

This never selects artwork or changes the general squint exemption/art gate.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
review = base / 'review/USER_G07_07_UPRIGHT_WORKING_EYE_RECOLOR_20261104_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
instruction = review / 'USER_INSTRUCTION.json'
spec_path = review / 'PREP/G07_07_UPRIGHT_EYE_SPEC_ROOT_APPROVED.json'
authorization, spec = read(instruction), read(spec_path)
assert authorization['id'] == spec['id'] == 'ART-G07-07'
assert authorization['user_statement_verbatim'] == '将图像上下翻转后进行眼球绘制'
assert authorization['this_frame_narrowed_eye_scope_explicitly_requested']
assert authorization['preview_only_no_art_selection_or_acceptance']
assert spec['approved'] and spec['all_approved']
assert spec['working_transform']['operation'] == 'FLIP_TOP_BOTTOM'
assert not spec['working_transform']['resampling']
assert spec['original_input'] == authorization['source']
source, working = Path(spec['original_input']['path']), Path(spec['input']['path'])
assert sha(source) == spec['original_input']['sha256']
assert sha(working) == spec['input']['sha256']
original, upright = Image.open(source), Image.open(working)
assert original.mode == upright.mode == 'RGBA' and original.size == upright.size
before, work = np.array(original), np.array(upright)
assert np.array_equal(work, before[::-1])
assert np.array_equal(work[::-1], before)
after_work = work.copy()
allowed = np.zeros(work.shape[:2], bool)
protected = allowed.copy()
yy, xx = np.mgrid[:work.shape[0], :work.shape[1]]
details = []
dark, light = np.array(spec['dark_rgb'], float), np.array(spec['light_rgb'], float)
assert dark.tolist() == [72, 69, 67] and light.tolist() == [129, 128, 128]
for eye in spec['eyes']:
    assert eye['approved'] and eye['mask_reviewed']
    masks = []
    for key in ('interior_mask', 'protected_glint_mask'):
        item = eye[key]
        assert sha(Path(item['path'])) == item['sha256']
        image = Image.open(item['path'])
        assert image.mode == 'L' and image.size == original.size
        values = np.array(image)
        assert np.isin(values, [0, 255]).all()
        masks.append(values == 255)
    mask, glint = masks
    assert mask.any() and not (mask & glint).any() and not (mask & allowed).any()
    allowed |= mask
    protected |= glint
    cx, cy = eye['center_xy']
    dx, dy = eye['down_unit_xy']
    assert abs(dx * dx + dy * dy - 1) < 1e-6
    across = (xx - cx) * dy - (yy - cy) * dx
    down = (xx - cx) * dx + (yy - cy) * dy
    arc = eye['light_cap']
    rx, ry = arc['radii_xy']
    q = np.sqrt(((across - arc['center_local_xy'][0]) / rx) ** 2
                + ((down - arc['center_local_xy'][1]) / ry) ** 2)
    width = eye['light_transition_width_px']
    assert .5 <= width <= 2
    coverage = np.clip((1 - q) * min(rx, ry) / width + .5, 0, 1)
    color = np.rint(dark + coverage[..., None] * (light - dark)).astype(np.uint8)
    after_work[mask, :3] = color[mask]
    details.append({'name': eye['name'], 'allowed_pixels': int(mask.sum()),
                    'protected_glint_pixels': int(glint.sum())})
assert not (allowed & protected).any()
after = after_work[::-1].copy()
original_allowed, original_protected = allowed[::-1], protected[::-1]
changed = np.any(before != after, axis=2)
assert np.array_equal(after[~original_allowed], before[~original_allowed])
assert np.array_equal(after[original_protected], before[original_protected])
assert np.array_equal(after[..., 3], before[..., 3])
out = base / 'drawings/ART-G07-07/v01/py_user_upright_working_eye_flipback_scope_v01'
out.mkdir(exist_ok=False)
target = out / 'character_eye_gray_flipback_local.png'
Image.fromarray(after).save(target)
Image.fromarray(after_work).save(out / 'WORKING_UPRIGHT_EYE_RESULT.png')
assert np.array_equal(np.array(Image.open(target)), after)
for name, color in [('white', 'white'), ('black', 'black')]:
    for label, array in [('', after), ('UPRIGHT_', after_work)]:
        Image.alpha_composite(Image.new('RGBA', original.size, color), Image.fromarray(array)).convert('RGB').save(out / f'{label}qa_{name}.png')
Image.fromarray(changed.astype(np.uint8) * 255).save(out / 'changed_pixels_original_orientation.png')
proof = {'id': 'ART-G07-07', 'created_utc': datetime.now(timezone.utc).isoformat(),
    'source': ev(source), 'working': ev(working), 'output': ev(target),
    'spec': ev(spec_path), 'explicit_user_instruction': ev(instruction),
    'script': ev(Path(__file__)), 'eyes': details,
    'changed_pixels': int(changed.sum()), 'outside_mask_RGBA_changed_pixels': 0,
    'all_alpha_changed_pixels': 0, 'protected_glint_RGBA_changed_pixels': 0,
    'native_vertical_flip_and_inverse_exact': True, 'resampling': False,
    'original_orientation_restored': True, 'input_original_preserved': sha(source) == spec['original_input']['sha256'],
    'API_calls': 0, 'imagegen_calls': 0, 'scoped_preview_only': True,
    'central_selection_changed': False, 'general_eye_exemption_changed': False,
    'whole_art_pass': False, 'user_accepted': False, 'dynamic_validated': False}
(out / 'VERIFICATION.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(proof, ensure_ascii=False))
