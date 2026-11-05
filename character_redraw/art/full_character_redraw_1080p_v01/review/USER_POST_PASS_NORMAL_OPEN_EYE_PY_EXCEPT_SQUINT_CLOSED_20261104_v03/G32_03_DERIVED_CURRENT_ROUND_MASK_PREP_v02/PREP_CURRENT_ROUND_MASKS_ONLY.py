from pathlib import Path
import copy
import hashlib
import json
import shutil
from datetime import datetime, timezone

import numpy as np
from PIL import Image

B = Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
P = B / 'review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03'
O = P / 'G32_03_DERIVED_CURRENT_ROUND_MASK_PREP_v02'
OLD = P / 'G32_03_DERIVED_FRAME_CROP_MASK_PREP_v01/G32_03_FOUR_VISIBLE_IRIS_SPEC_PREPONLY_v01.json'
SPEC = O / 'G32_03_FOUR_VISIBLE_IRIS_CURRENT_ROUND_SPEC_PREPONLY_v02.json'
SOURCE = B / 'drawings/ART-G32-03/v01/whole_imggen_user_extend_canvas_normal_coil_then_crop_v04/derived_original_viewport_candidate_v01/character_frame_crop.png'
WHITE = SOURCE.with_name('qa_white.png')
BLACK = SOURCE.with_name('qa_black.png')
CANON = Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G32-03/source.png')
GUIDE = B / 'drawings/ART-G32-03/v01/inputs/source_pose_guide.png'
BASELINE = B / 'review/USER_EYE_GRAY_PATCH_SHAPE_PY_20261104_v02/USER_APPROVED_EYE_REFERENCE_ORIGINAL.png'
BASELINE_CROP = BASELINE.with_name('EYE_COLORS_AND_LIGHT_CAP_REFERENCE.png')
BASELINE_MEAS = B / 'review/USER_X01_14_LIGHT_ARC_BASELINE_CHECK_20261104_v01/BASELINE_COMPARISON_AND_USER_FEEDBACK.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def artifact(path):
    return {'path': Path(path).as_posix(), 'sha256': sha(path)}


def dump(path, value):
    assert not path.exists(), f'Preserve existing artifact: {path}'
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


assert not SPEC.exists(), 'PREP is immutable after finalization; use another version.'
assert sha(SOURCE) == '418d24aa65aef62223aea0ffa25ad2381a42a533aa4353b638d8eff85e371f2d'
assert sha(BASELINE) == 'cdf0a445d2aa9398e5ce3ab8714c563ebc6c735f9fdc98b71d245dc17edb2d66'
old = json.loads(OLD.read_text(encoding='utf-8-sig'))
assert old['input']['sha256'] == sha(SOURCE)
rgb = np.array(Image.open(WHITE).convert('RGB'))
raw = np.array(Image.open(SOURCE).convert('RGBA'))
measure = json.loads(BASELINE_MEAS.read_text(encoding='utf-8-sig'))
normalized = np.mean([e['normalized_center_x_y_radius_x_y'] for e in measure['baseline_measurements']], axis=0)
assert np.allclose(normalized, [.49611775768816646, .902652586879648, .3862977646048331, .35274188480332563])
spec = copy.deepcopy(old)
spec['prep_status'] = 'PREP_ONLY_FRESH_CURRENT_CROP_MASKS_AND_ROUND_BASELINE_ROOT_REVIEW_REQUIRED'
spec['input'] = artifact(SOURCE)
spec['input_dimensions'] = [1404, 785]
spec['root_mask_reviewed'] = False
spec['root_release_granted'] = False
spec['approved'] = False
spec['color_edit_applied'] = False
spec['root_art_selection_required'] = True
spec['dark_rgb'] = [72, 69, 67]
spec['light_rgb'] = [129, 128, 128]
spec['palette_scope'] = 'Existing global v03 palette. G32-03 three-head insert is outside the later dance B-palette selection; no B colors used.'
spec['baseline_master'] = artifact(BASELINE)
spec['baseline_crop'] = artifact(BASELINE_CROP)
spec['baseline_comparison_and_user_feedback'] = artifact(BASELINE_MEAS)
spec['previous_PREP_preserved'] = artifact(OLD)
spec['current_art_independent_report'] = artifact(B / 'review/SOL_G32_03_DERIVED_VIEWPORT_CURRENT_ACTUAL_REVIEW_20261104_v01.json')
spec['scope'] = 'PREP only. Four actually visible normal-open iris interiors and adapted internal round lower cap. No hidden iris reconstruction. Existing permission/glint masks reused only for exact418d crop after actual boundary review. No production image recolor or approval of old flat caps.'
spec['prepared_utc'] = datetime.now(timezone.utc).isoformat()
spec['root_actual_mask_review_required'] = True
spec['formal_eye_apply_calls'] = 0
spec['generation_calls'] = 0
spec['central_writes'] = False
spec['art_pixels_modified'] = False
all_perm = np.zeros(raw.shape[:2], bool)
all_glint = np.zeros(raw.shape[:2], bool)
diagnostics = []
numeric = []

for eye, prior in zip(spec['eyes'], old['eyes']):
    name = eye['name']
    perm_path = O / f'{name}_FULL_IRIS_PERMISSION_exact418d_REUSED_v02.png'
    glint_path = O / f'{name}_ORIGINAL_GLINT_AA_PROTECTION_exact418d_REUSED_v02.png'
    for key, destination in [('interior_mask', perm_path), ('protected_glint_mask', glint_path)]:
        origin = Path(prior[key]['path'])
        assert sha(origin) == prior[key]['sha256']
        assert not destination.exists()
        shutil.copyfile(origin, destination)
        assert sha(origin) == sha(destination)
        eye[key] = artifact(destination)
    m = np.array(Image.open(perm_path).convert('L'))
    g = np.array(Image.open(glint_path).convert('L'))
    assert m.shape == raw.shape[:2] and g.shape == m.shape
    assert set(np.unique(m)).issubset({0, 255}) and set(np.unique(g)).issubset({0, 255})
    m, g = m == 255, g == 255
    assert not np.any(m & g) and not np.any(m & all_perm) and not np.any(g & all_glint)
    all_perm |= m
    all_glint |= g
    y, x = np.where(m | g)
    xy = np.column_stack([x, y]) - np.array(eye['center_xy'])
    dx, dy = eye['down_unit_xy']
    assert abs(np.hypot(dx, dy) - 1) < 1e-12
    local = np.column_stack([xy[:, 0] * dy - xy[:, 1] * dx, xy[:, 0] * dx + xy[:, 1] * dy])
    lo, hi = local.min(axis=0), local.max(axis=0)
    width, height = hi - lo
    center = lo + normalized[:2] * [width, height]
    radii = normalized[2:] * [width, height]
    eye['light_cap'] = {'center_local_xy': center.tolist(), 'radii_xy': radii.tolist()}
    eye['light_transition_width_px'] = 1.5
    eye['root_mask_reviewed'] = False
    eye['mask_reviewed'] = False
    eye['expression_reviewed'] = True
    eye['expression_classification'] = 'normal_open'
    eye['expression_reviewed_by'] = 'Sol xhigh fresh actual current418d crop/native+8x and own2295. Partly hidden iris remains normal-open only in its actually visible region.'
    eye['mask_reuse'] = {'source_PREP': artifact(OLD), 'permission_RGBA_domain_unchanged': True, 'original_glint_AA_unchanged': True, 'original_cap_not_reused': True}
    eye['mask_reviewed_by'] = 'Pending new diagnostics actual review; ROOT approval remains false.'
    ay, ax = np.where(m)
    own = np.column_stack([ax, ay]) - np.array(eye['center_xy'])
    uv = np.column_stack([own[:, 0] * dy - own[:, 1] * dx, own[:, 0] * dx + own[:, 1] * dy])
    rho = np.linalg.norm((uv - center) / radii, axis=1)
    coverage = np.clip(.5 + (1 - rho) * min(radii) / 1.5, 0, 1)
    prevcenter = np.array(prior['light_cap']['center_local_xy'])
    prevradius = np.array(prior['light_cap']['radii_xy'])
    oldcoverage = np.clip(.5 + (1 - np.linalg.norm((uv - prevcenter) / prevradius, axis=1)) * min(prevradius) / 1.5, 0, 1)
    eye['baseline_adaptation'] = {
        'reference_normalized_center_x_y_radius_x_y': normalized.tolist(),
        'own_visible_iris_local_bounds_uv': [*lo.tolist(), *hi.tolist()],
        'own_local_width_height': [float(width), float(height)],
        'original_eye_axis_preserved': True,
        'visible_domain_only_no_hidden_iris_inferred': True,
        'weighted_light_fraction': float(coverage.mean()),
        'half_coverage_light_fraction': float((coverage >= .5).mean()),
        'old_PREP_weighted_light_fraction': float(oldcoverage.mean()),
        'measurement_not_fixed_user_percentage': True,
    }
    roi = eye['context_roi_xyxy_exclusive']
    x0, y0, x1, y1 = roi
    native = Image.fromarray(rgb[y0:y1, x0:x1])
    src_path = O / f'{name}_SOURCE_native.png'
    src8_path = O / f'{name}_SOURCE_8x.png'
    native.save(src_path)
    native.resize((native.width * 8, native.height * 8), Image.Resampling.NEAREST).save(src8_path)
    overlay = rgb.copy().astype(float)
    overlay[m] = .45 * overlay[m] + .55 * np.array([0, 225, 255])
    overlay[g] = [255, 0, 220]
    contour = m.copy()
    contour[m] = np.abs((1 - rho) * min(radii)) <= .8
    overlay[contour] = [255, 230, 0]
    overlay = np.rint(overlay).astype(np.uint8)
    onative = Image.fromarray(overlay[y0:y1, x0:x1])
    op = O / f'{name}_PERMISSION_CYAN_GLINT_MAGENTA_ROUND_ARC_YELLOW_native.png'
    op8 = O / f'{name}_PERMISSION_CYAN_GLINT_MAGENTA_ROUND_ARC_YELLOW_8x.png'
    onative.save(op)
    onative.resize((onative.width * 8, onative.height * 8), Image.Resampling.NEAREST).save(op8)
    cap = np.zeros(m.shape, np.uint8)
    cap[m] = np.rint(coverage * 255).astype(np.uint8)
    cp = O / f'{name}_ROUND_LOWER_CAP_COVERAGE_DIAGNOSTIC_NOT_APPLIED.png'
    Image.fromarray(cap).save(cp)
    eye['diagnostic_paths'] = [artifact(p) for p in [src_path, src8_path, op, op8, cp]]
    diagnostics.extend([src_path, src8_path, op, op8])
    numeric.append({'name': name, 'permission': int(m.sum()), 'glint_AA': int(g.sum()), 'old_cap_fraction': float(oldcoverage.mean()), 'round_cap_fraction': float(coverage.mean()), 'source_roi': roi})

assert int(all_perm.sum()) == 14955 and int(all_glint.sum()) == 815
assert not np.any(all_perm & all_glint)
spec['allowed_pixels_union'] = int(all_perm.sum())
spec['protected_glint_pixels_union'] = int(all_glint.sum())
spec['old_PREP_cap_approval_inherited'] = False
spec['risk_notes'] = [
    'The two partly bob-occluded eyes retain only currently visible iris permission. Their foreground black hair contours must never be included as iris rim; absent glint is not invented.',
    'Reference supplies internal round cap/gray colors only; eye outline, own vertical aspect and head tilt remain original. Measured light fractions are not a fixed global percentage.',
    'This preparer cannot independently approve a future applied output based on these own masks. ROOT must actually inspect mask/spec before applying, then another reviewer examines final scoped output.',
]
exempt_roi = [846, 297, 1294, 469]
x0, y0, x1, y1 = exempt_roi
exempt = Image.fromarray(rgb[y0:y1, x0:x1])
exempt.save(O / 'right_front_TWO_CLOSED_EYES_EXEMPT_native.png')
exempt.resize((exempt.width * 2, exempt.height * 2), Image.Resampling.NEAREST).save(O / 'right_front_TWO_CLOSED_EYES_EXEMPT_2x.png')
dump(O / 'DRAFT_NUMERIC_PREP_NOT_RELEASED.json', {'eyes': numeric, 'permission_union': int(all_perm.sum()), 'glint_union': int(all_glint.sum()), 'input_unchanged_sha256': sha(SOURCE), 'art_pixels_modified': False})
dump(O / 'G32_03_FOUR_VISIBLE_IRIS_CURRENT_ROUND_SPEC_DRAFT_PENDING_ACTUAL.json', spec)
print(json.dumps({'folder': O.as_posix(), 'eyes': numeric, 'diagnostics_to_actual_view': [p.as_posix() for p in diagnostics], 'no_formal_apply': True}, ensure_ascii=False))
