"""Transfer only the two supplied iris color fields onto exact X01-14 masks.

Preview candidates only. The existing selected image and global policy stay put.
Reference lids, outlines, glints and face pixels are never pasted into the target.
"""
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from EyeLocalPolicy import check_post_pass_eye_edit

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
REVIEW = BASE / 'review/USER_X01_14_EYE_STYLE_TWO_REFERENCES_20261104_v01'
SPEC_PATH = BASE / 'review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_14_THIN_FIRST_WHOLE_MASK_PREP_v01/X01_14_THIN_FIRST_WHOLE_TWO_NORMAL_IRIS_SPEC_ROOT_APPROVED_v01.json'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
evidence = lambda p: {'path': str(Path(p).resolve()), 'sha256': sha(p)}
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))


def largest_component(mask):
    seen = np.zeros_like(mask)
    groups = []
    for y, x in zip(*np.where(mask)):
        if seen[y, x]:
            continue
        queue = deque([(y, x)])
        seen[y, x] = True
        points = []
        while queue:
            py, px = queue.popleft()
            points.append((py, px))
            for ny, nx in ((py-1, px), (py+1, px), (py, px-1), (py, px+1)):
                if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    queue.append((ny, nx))
        groups.append(points)
    result = np.zeros_like(mask)
    for y, x in max(groups, key=len):
        result[y, x] = True
    return result


def axes_xy(x, y, center, down):
    dx, dy = down
    return (x-center[0])*dy-(y-center[1])*dx, (x-center[0])*dx+(y-center[1])*dy


def style_field(reference, roi, down):
    x0, y0, x1, y1 = roi
    rgb = reference[y0:y1, x0:x1, :3].astype(float)
    gray = rgb.mean(axis=2)
    material = largest_component((gray > 35) & (gray < 145) & (np.ptp(rgb, axis=2) < 20))
    # One native-pixel inset excludes white/black outer-edge antialiasing and
    # the source glint's antialias fringe. No source glint is transferred.
    core = material.copy()
    core[0] = core[-1] = False
    core[:, 0] = core[:, -1] = False
    core[1:-1, 1:-1] &= (material[:-2, 1:-1] & material[2:, 1:-1]
                           & material[1:-1, :-2] & material[1:-1, 2:])
    assert core.sum() > 300
    filled = rgb.copy()
    valid_yx = np.column_stack(np.where(core))
    invalid_yx = np.column_stack(np.where(~core))
    for start in range(0, len(invalid_yx), 128):
        points = invalid_yx[start:start+128]
        distances = ((points[:, None, :] - valid_yx[None, :, :]) ** 2).sum(axis=2)
        nearest = valid_yx[distances.argmin(axis=1)]
        filled[points[:, 0], points[:, 1]] = rgb[nearest[:, 0], nearest[:, 1]]
    ys, xs = np.where(material)
    center = [(xs.min()+xs.max())/2+x0, (ys.min()+ys.max())/2+y0]
    u, v = axes_xy(xs+x0, ys+y0, center, down)
    bounds = [float(u.min()), float(v.min()), float(u.max()), float(v.max())]
    return filled, center, bounds, {
        'roi_xyxy': roi, 'down_unit_xy': down, 'center_xy': center,
        'material_local_bounds_uv': bounds, 'material_pixels': int(material.sum()),
        'interior_sample_pixels': int(core.sum()),
        'sample_color_p10_p50_p90': np.percentile(rgb[core], [10, 50, 90], axis=0).round(2).tolist(),
        'source_glint_outline_and_eyelid_excluded': True,
    }


def sample_bilinear(field, x, y):
    x = np.clip(x, 0, field.shape[1]-1)
    y = np.clip(y, 0, field.shape[0]-1)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    x1, y1 = np.minimum(x0+1, field.shape[1]-1), np.minimum(y0+1, field.shape[0]-1)
    fx, fy = (x-x0)[:, None], (y-y0)[:, None]
    return ((1-fx)*(1-fy)*field[y0, x0] + fx*(1-fy)*field[y0, x1]
            + (1-fx)*fy*field[y1, x0] + fx*fy*field[y1, x1])


def main():
    REVIEW.mkdir(exist_ok=True)
    spec = read(SPEC_PATH)
    source = Path(spec['input']['path'])
    assert sha(source) == spec['input']['sha256'] == '8181037962aaa0624155fc5ac1af924536be55f5b4b35311f4cf78d748de29ae'
    check_post_pass_eye_edit(ROOT, source, spec)
    registry = BASE / 'ASSET_REGISTRY.json'
    defaults = ROOT / 'image_defaults.json'
    untouched = {str(p): sha(p) for p in (registry, defaults, source)}
    before = np.asarray(Image.open(source)).copy()
    assert before.shape == (1645, 956, 4)
    masks, glints = [], []
    for eye in spec['eyes']:
        for key in ('interior_mask', 'protected_glint_mask'):
            assert sha(eye[key]['path']) == eye[key]['sha256']
        masks.append(np.asarray(Image.open(eye['interior_mask']['path'])) == 255)
        glints.append(np.asarray(Image.open(eye['protected_glint_mask']['path'])) == 255)
    allowed, protected = np.logical_or.reduce(masks), np.logical_or.reduce(glints)
    assert not (allowed & protected).any()
    variants = [
        ('A', Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-2462cf88-c2ae-464a-ae5f-180296f9363b.png'),
         '34e582536a73ee2afa113bbf57152a660f22dc515069cc81054426bb229d9ee1',
         [(420, 207, 469, 255), (515, 190, 555, 241)],
         [(0.15, float(np.sqrt(1-.15**2))), (.12, float(np.sqrt(1-.12**2)))]),
        ('B', Path('C:/Users/11515/.codex/generated_images/01a18c9e-c795-7c41-9eed-612ceab2f81f/exec-632d860c-8676-4b62-8d59-14f508a361ab.png'),
         '80e10642029b2259a139268484becf8cd78f40716f8f4d91366da202e1fc8cac',
         [(370, 347, 455, 426), (553, 409, 635, 492)],
         [(-.32, float(np.sqrt(1-.32**2))), (-.32, float(np.sqrt(1-.32**2)))]),
    ]
    outputs = []
    for label, ref, expected, rois, directions in variants:
        assert sha(ref) == expected
        saved_ref = REVIEW / f'USER_REFERENCE_{label}.png'
        assert not saved_ref.exists()
        shutil.copyfile(ref, saved_ref)
        reference = np.asarray(Image.open(saved_ref).convert('RGBA'))
        after = before.copy()
        eye_details = []
        for eye, mask, roi, down_ref in zip(spec['eyes'], masks, rois, directions):
            field, center_ref, bounds_ref, detail = style_field(reference, roi, down_ref)
            ys, xs = np.where(mask)
            u, v = axes_xy(xs, ys, eye['center_xy'], eye['down_unit_xy'])
            u0, v0, u1, v1 = eye['baseline_adaptation']['own_actual_filled_iris_local_bounds_uv']
            ru0, rv0, ru1, rv1 = bounds_ref
            ru, rv = ru0+(u-u0)/(u1-u0)*(ru1-ru0), rv0+(v-v0)/(v1-v0)*(rv1-rv0)
            dx, dy = down_ref
            rx = center_ref[0] + ru*dy + rv*dx - roi[0]
            ry = center_ref[1] - ru*dx + rv*dy - roi[1]
            after[ys, xs, :3] = np.rint(sample_bilinear(field, rx, ry)).astype(np.uint8)
            detail.update({'name': eye['name'], 'target_mask': eye['interior_mask'],
                           'target_glint': eye['protected_glint_mask'],
                           'target_local_bounds_uv': [u0, v0, u1, v1],
                           'target_down_unit_xy': eye['down_unit_xy']})
            eye_details.append(detail)
        changed = np.any(before != after, axis=2)
        assert np.array_equal(before[~allowed], after[~allowed])
        assert np.array_equal(before[protected], after[protected])
        assert np.array_equal(before[..., 3], after[..., 3])
        out = BASE / f'drawings/ART-X01-14/v01/py_user_reference_{label}_eye_style_trial_v01'
        out.mkdir(exist_ok=False)
        image = out / 'character_eye_style_trial.png'
        Image.fromarray(after).save(image)
        assert np.array_equal(np.asarray(Image.open(image)), after)
        for name, color in [('white', 'white'), ('black', 'black')]:
            bg = Image.new('RGBA', (956, 1645), color)
            bg.alpha_composite(Image.fromarray(after))
            bg.convert('RGB').save(out / f'qa_{name}.png')
        Image.fromarray(changed.astype(np.uint8)*255).save(out / 'changed_pixels_mask.png')
        report = {
            'source': evidence(source), 'user_reference': evidence(saved_ref),
            'output': evidence(image), 'original_target_mask_spec': evidence(SPEC_PATH),
            'script': evidence(__file__), 'method': 'Bilinear transfer of reference iris RGB field in each eye local coordinates, with reference outlines/glints excluded. Target raster is never warped.',
            'eyes': eye_details, 'allowed_pixels': int(allowed.sum()),
            'changed_pixels': int(changed.sum()), 'outside_iris_RGBA_changes': 0,
            'alpha_changes': 0, 'original_glint_and_glint_AA_changes': 0,
            'eye_outline_shape_position_and_gaze_changed': False,
            'API_calls': 0, 'imagegen_calls': 0, 'trial_only': True,
            'global_eye_policy_changed': False, 'asset_registry_changed': False,
            'user_accepted': False, 'production_bound': False,
        }
        (out/'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        outputs.append({'variant': label, 'output': evidence(image), 'white_preview': evidence(out/'qa_white.png'),
                        'verification': evidence(out/'VERIFICATION.json')})
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 24)
    small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 19)
    panel = Image.new('RGB', (1180, 460), (245, 245, 245))
    draw = ImageDraw.Draw(panel)
    draw.text((18, 10), '同一张图，仅比较眼内画法', font=font, fill=(30, 30, 30))
    roi = (390, 215, 560, 335)
    for x, p, title in [(12, source, '图1原眼睛'), (404, Path(outputs[0]['output']['path']), 'A：参考图2'), (796, Path(outputs[1]['output']['path']), 'B：参考补充图')]:
        draw.text((x, 55), title, font=font, fill=(25, 25, 25))
        crop = Image.open(p).crop(roi)
        bg = Image.new('RGBA', crop.size, 'white'); bg.alpha_composite(crop)
        panel.paste(bg.convert('RGB').resize((374, 264), Image.Resampling.NEAREST), (x, 100))
    draw.text((18, 395), '眼形、眼白、眼线和原高光保留；人物其余像素逐像素一致。', font=small, fill=(45, 45, 45))
    comparison = REVIEW/'EYE_STYLE_COMPARISON.png'
    panel.save(comparison)
    for p, digest in untouched.items():
        assert sha(p) == digest, 'Existing selected state or original changed.'
    delivery = {'recorded_utc': datetime.now(timezone.utc).isoformat(), 'source': evidence(source),
                'user_requests': ['应用图2的眼睛画法至1试试', '这张也行'],
                'outputs': outputs, 'comparison': evidence(comparison),
                'existing_selection_and_global_policy_unchanged': True,
                'scope': 'Two reversible local iris-style trials. No automatic global adoption.'}
    (REVIEW/'USER_TRIAL_DELIVERY.json').write_text(json.dumps(delivery, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(delivery, ensure_ascii=False))


if __name__ == '__main__':
    main()
