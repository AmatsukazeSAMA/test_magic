"""Compare the approved eye master and prepare an iris-interior arc correction.

No generation, no permission-mask edits and no production color changes here.
The circle fits describe only the internal dark/light boundary in the master.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
OUT = BASE / 'review/USER_X01_14_LIGHT_ARC_BASELINE_CHECK_20261104_v01'
OUT.mkdir(exist_ok=False)
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev = lambda p: {'path': str(Path(p).resolve()), 'sha256': sha(p)}
policy_path = BASE / 'review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json'
policy = read(policy_path)
master = Path(policy['approved_color_master']['path'])
assert sha(master) == policy['approved_color_master']['sha256']
ref = np.asarray(Image.open(master))
records = []
for name, roi in [('viewer_left', (478, 387, 637, 554)),
                  ('viewer_right', (910, 368, 1076, 550))]:
    x0, y0, x1, y1 = roi
    rgb = ref[y0:y1, x0:x1, :3].astype(float)
    neutral = (np.ptp(rgb, axis=2) < 15) & (rgb.mean(2) > 40) & (rgb.mean(2) < 170)
    yy, xx = np.where(neutral)
    bounds = [int(xx.min()+x0), int(yy.min()+y0), int(xx.max()+x0+1), int(yy.max()+y0+1)]
    bx0, by0, bx1, by1 = bounds
    points = []
    for x in range(x0, x1):
        if not bx0 + .2*(bx1-bx0-1) < x < bx1-1-.2*(bx1-bx0-1):
            continue
        column = ref[y0:y1, x, :3].astype(float)
        lum = column.mean(1)
        possible = np.where((lum > 109) & (lum < 160) & (np.ptp(column, axis=1) < 15)
                            & (np.arange(y0, y1) > by0+.4*(by1-by0-1)))[0]
        if len(possible):
            points.append([x, int(y0+possible[0])])
    points = np.asarray(points, float)
    c = np.linalg.lstsq(np.c_[2*points[:, 0], 2*points[:, 1], np.ones(len(points))],
                        np.sum(points**2, axis=1), rcond=None)[0]
    radius = float(np.sqrt(c[2]+c[0]**2+c[1]**2))
    w, h = bx1-bx0, by1-by0
    normalized = [(c[0]-bx0)/w, (c[1]-by0)/h, radius/w, radius/h]
    records.append({'name': name, 'inspected_roi_xyxy': list(roi),
                    'neutral_fill_bbox_xyxy': bounds, 'boundary_points': points.astype(int).tolist(),
                    'fitted_circle_center_xy': c[:2].tolist(), 'fitted_radius_px': radius,
                    'circle_fit_rms_px': float(np.sqrt(np.mean((np.linalg.norm(points-c[:2], axis=1)-radius)**2))),
                    'normalized_center_x_y_radius_x_y': normalized,
                    'threshold_estimated_light_fraction': float(((rgb.mean(2)>109)&neutral).sum()/neutral.sum())})

normalized = np.mean([r['normalized_center_x_y_radius_x_y'] for r in records], axis=0)
old_spec_path = BASE / 'review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_14_ROUNDED_WHOLE_SMALLER_LIGHT_CAP_MASK_PREP_v01/X01_14_TWO_NORMAL_IRIS_SMALLER_LIGHT_CAP_SPEC_ROOT_APPROVED_v01.json'
spec = copy.deepcopy(read(old_spec_path))
src = Image.open(spec['input']['path'])
assert sha(spec['input']['path']) == spec['input']['sha256']
old_py = BASE / 'drawings/ART-X01-14/v01/py_post_pass_user_round_ribbon_smaller_light_cap_v02/character_eye_gray_local.png'
selected = read(BASE / 'ASSET_REGISTRY.json')['ART-X01-14']
assert Path(selected['image']).resolve() == old_py.resolve()
assert selected['secondary_eye_local_passed']
(OUT/'SELECTED_BEFORE_BASELINE_CHECK.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
before = np.asarray(src)
yy, xx = np.mgrid[:src.height, :src.width]
preview = before.copy()
measurements = []
for eye in spec['eyes']:
    mask = np.asarray(Image.open(eye['interior_mask']['path'])) == 255
    glint = np.asarray(Image.open(eye['protected_glint_mask']['path'])) == 255
    assert sha(eye['interior_mask']['path']) == eye['interior_mask']['sha256']
    assert sha(eye['protected_glint_mask']['path']) == eye['protected_glint_mask']['sha256']
    assert not (mask & glint).any()
    cx, cy = eye['center_xy']; dx, dy = eye['down_unit_xy']
    across = (xx-cx)*dy-(yy-cy)*dx
    down = (xx-cx)*dx+(yy-cy)*dy
    u0, u1 = float(across[mask].min()), float(across[mask].max())
    v0, v1 = float(down[mask].min()), float(down[mask].max())
    w, h = u1-u0, v1-v0
    arc = {'center_local_xy': [u0+normalized[0]*w, v0+normalized[1]*h],
           'radii_xy': [normalized[2]*w, normalized[3]*h]}
    old_arc = copy.deepcopy(eye['light_cap'])
    eye['light_cap'] = arc
    eye['mask_reviewed'] = False
    eye['root_mask_reviewed'] = False
    q = np.sqrt(((across-arc['center_local_xy'][0])/arc['radii_xy'][0])**2
                + ((down-arc['center_local_xy'][1])/arc['radii_xy'][1])**2)
    coverage = np.clip((1-q)*min(arc['radii_xy'])/eye['light_transition_width_px']+.5, 0, 1)
    measurements.append({'name': eye['name'], 'own_local_fill_bounds': [u0,v0,u1,v1],
                         'previous_cap': old_arc, 'proposed_cap': arc,
                         'weighted_light_fraction': float(coverage[mask].mean()),
                         'half_coverage_light_fraction': float((coverage[mask]>=.5).mean()),
                         'original_mask_unchanged': True, 'original_glint_unchanged': True})
    # Diagnostic only: show the proposed boundary, never a production color preview.
    diag = before.copy()
    diag[mask, :3] = np.rint(.65*diag[mask, :3]+.35*np.array([0,210,245])).astype(np.uint8)
    diag[glint, :3] = [240,0,180]
    edge = mask & (np.abs(q-1)*min(arc['radii_xy']) < .6)
    diag[edge, :3] = [255,210,0]
    roi = eye['context_roi_xyxy_exclusive']
    cut = Image.fromarray(diag).crop(roi)
    cut.resize((cut.width*8,cut.height*8), Image.Resampling.NEAREST).save(OUT/f"{eye['name']}_BASELINE_ROUND_CAP_MASK_DIAGNOSTIC_8x.png")

for field in ['root_trial_not_user_numeric_rule', 'current_vs_proposed_measurements',
              'root_actually_viewed_surfaces', 'root_reviewed_utc', 'approved_from_PREP',
              'whole_art_pass_evidence']:
    spec.pop(field, None)
spec.update({'prep_status':'BASELINE_ROUND_ARC_PREP_ONLY_NOT_APPROVED',
             'root_mask_reviewed':False, 'root_release_granted':False,
             'user_feedback_quote':'检查基线，应该浅灰弧度没有那么小吧',
             'prepared_utc':datetime.now(timezone.utc).isoformat(),
             'baseline_reference':ev(master), 'previous_spec':ev(old_spec_path),
             'baseline_arc_fit':{'method':'Two inspected master-eye central upper light-boundary circles; mean normalized internal cap only, adapted to this image own mask axes and bounds.',
                                 'normalized_center_x_y_radius_x_y':normalized.tolist(),
                                 'not_global_area_percentage_rule':True},
             'scope':'Only two already-locked normal-open iris interiors; internal light cap returns to the approved round dome. Original outline, glint, eye white, lids/lashes, alpha and every exterior pixel immutable.'})
spec_path = OUT/'X01_14_BASELINE_ROUND_CAP_SPEC_PREPONLY_v01.json'
spec_path.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report = {'recorded_utc':datetime.now(timezone.utc).isoformat(),
          'user_statement_verbatim':'检查基线，应该浅灰弧度没有那么小吧',
          'baseline_master':ev(master),'baseline_crop':policy['light_cap_reference'],
          'baseline_measurements':records,'target_measurements':measurements,
          'finding':'Previous22.5% local trial moved a too-wide ellipse too far down, flattening the visible arc. Approved reference has a rounder dome; preserve that internal curvature while dark stays the larger area.',
          'numeric_status':'Threshold areas and circle fits are measurements, not a user fixed percentage or a replacement eye-outline template.',
          'API_calls':0,'imagegen_calls':0,'formal_eye_apply_calls':0,
          'new_prep_spec':ev(spec_path),'prior_candidate':ev(old_py)}
(OUT/'BASELINE_COMPARISON_AND_USER_FEEDBACK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'directory':str(OUT),'spec':ev(spec_path),'master':records,'target':measurements},ensure_ascii=False))
