"""Freeze root-reviewed exact iris masks; no image pixels are changed."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument('--spec', type=Path, required=True)
p.add_argument('--approved', type=Path, required=True)
p.add_argument('--reviewed-surface', type=Path, action='append', required=True)
a = p.parse_args()
read = lambda f: json.loads(f.read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
ev = lambda f: {'path': str(f.resolve()), 'sha256': sha(f)}
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
q = read(a.spec)
assert not a.approved.exists()
selected = read(base / 'ASSET_REGISTRY.json')[q['id']]
assert selected['status'] == 'reviewed_static_candidate'
assert selected['primary_static_pass'] and selected['independent_static_pass']
assert Path(selected['image']).resolve() == Path(q['input']['path']).resolve()
assert selected['sha256'] == q['input']['sha256'] == sha(Path(q['input']['path']))
defaults = read(root / 'image_defaults.json')
assert q['policy']['sha256'] == defaults['eye_color_policy']['sha256']
if 'B_style_acceptance' in q:
    dance_policy = defaults['dance_eye_style_policy']
    assert q['B_style_acceptance'] == dance_policy
    assert sha(Path(dance_policy['path'])) == dance_policy['sha256']
    assert q['id'] in read(Path(dance_policy['path']))['known_dance_state_ids']
else:
    assert q['dark_rgb'] == [72, 69, 67] and q['light_rgb'] == [129, 128, 128]
size = Image.open(q['input']['path']).size
union = np.zeros((size[1], size[0]), dtype=bool)
for eye in q['eyes']:
    assert eye['expression_reviewed'] and eye['expression_classification'] == 'normal_open'
    pair = []
    for field in ('interior_mask', 'protected_glint_mask'):
        item = eye[field]
        f = Path(item['path'])
        assert sha(f) == item['sha256']
        im = Image.open(f)
        assert im.mode == 'L' and im.size == size
        data = np.asarray(im)
        assert np.isin(data, [0, 255]).all()
        pair.append(data == 255)
    assert pair[0].any() and not (pair[0] & pair[1]).any()
    assert not (pair[0] & union).any()
    union |= pair[0]
    eye.update({'mask_reviewed': True, 'root_mask_reviewed': True,
        'mask_reviewed_by': 'ROOT actual source/new whole WB and original/cyan-domain/magenta-glint/diagnostic per-eye surfaces inspected for these exact pixels.'})
q.update({'root_mask_reviewed': True, 'root_release_granted': True,
    'prep_status': 'ROOT_ACTUAL_MASK_APPROVED_READY_FOR_FINAL_PYTHON',
    'root_reviewed_utc': datetime.now(timezone.utc).isoformat(),
    'approved_from_PREP': ev(a.spec), 'root_actually_viewed_surfaces': [ev(f) for f in a.reviewed_surface],
    'whole_art_pass_evidence': [ev(Path(selected[k])) for k in ('primary_review', 'independent_review')],
    'color_edit_applied': False})
a.approved.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'approved_spec': ev(a.approved), 'allowed_pixels': int(union.sum()), 'API_calls': 0, 'imagegen_calls': 0, 'eye_apply': False}, ensure_ascii=False))
