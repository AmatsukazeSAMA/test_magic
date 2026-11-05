"""Propose a uniform whole-cel placement from ORIGINAL PV face geometry.

Color components are diagnostic anchors only. Both reviewers must view the
resulting art/source before any placement can enter the exposure bindings.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image


def face_box(path, region):
    with Image.open(path) as im:
        x, y, w, h = region
        pix = np.array(im.convert('RGB').crop((x, y, x + w, y + h))).astype(int)
    r, g, b = pix[..., 0], pix[..., 1], pix[..., 2]
    mask = (r > 190) & (g > 130) & (b > 100) & (r > g + 8) & (g > b + 4)
    visited = np.zeros(mask.shape, dtype=bool)
    best = []
    for iy, ix in zip(*np.nonzero(mask)):
        if visited[iy, ix]:
            continue
        q = deque([(iy, ix)])
        visited[iy, ix] = True
        points = []
        while q:
            py, px = q.popleft()
            points.append((py, px))
            for ny, nx in ((py - 1, px), (py + 1, px), (py, px - 1), (py, px + 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
        if len(points) > len(best):
            best = points
    if len(best) < 100:
        raise RuntimeError('No reliable source-face component; inspect and use another geometric basis.')
    yy, xx = zip(*best)
    return [int(x + min(xx)), int(y + min(yy)), int(x + max(xx) + 1), int(y + max(yy) + 1)]


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--id', required=True)
    p.add_argument('--first-frame', type=int, required=True)
    p.add_argument('--source-head-region', nargs=4, type=int, required=True)
    p.add_argument('--scene-head-region', nargs=4, type=int, required=True)
    p.add_argument('--version', default='v01')
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / 'art/full_character_redraw_1080p_v01'
    load = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
    scope = load(base / 'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')
    state = next(s for s in scope['states'] if s['id'] == a.id and s['first_frame'] == a.first_frame)
    asset = load(base / 'ASSET_REGISTRY.json')[a.id]
    if not asset['primary_static_pass'] or not asset['independent_static_pass']:
        raise RuntimeError('Only current both-reviewed master art may be placed.')
    sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if sha(asset['image']) != asset['sha256']:
        raise RuntimeError('Reviewed image bytes changed.')
    reg_dir = Path(asset['selected_run'])
    while not (reg_dir / 'REGISTRATION_PLAN.json').exists():
        if reg_dir == base or reg_dir.parent == reg_dir:
            raise RuntimeError('Missing source-to-guide registration.')
        reg_dir = reg_dir.parent
    reg = load(reg_dir / 'REGISTRATION_PLAN.json')
    job = load(reg_dir / 'JOB.json')
    source = Path(reg.get('source_image', job['source_image']))
    scene = base / f'coverage/source_frames/F{a.first_frame:06d}.png'
    sb = face_box(source, a.source_head_region)
    tb = face_box(scene, a.scene_head_region)
    sx, sy = (tb[2] - tb[0]) / (sb[2] - sb[0]), (tb[3] - tb[1]) / (sb[3] - sb[1])
    if abs(sx / sy - 1) > .15:
        raise RuntimeError('Diagnostic anchors disagree; inspect source instead of distorting the cel.')
    source_scale = (sx + sy) / 2
    source_tx = (tb[0] + tb[2]) / 2 - source_scale * (sb[0] + sb[2]) / 2
    source_ty = (tb[1] + tb[3]) / 2 - source_scale * (sb[1] + sb[3]) / 2
    with Image.open(asset['image']) as im:
        fit = min(reg['guide_dimensions'][0] / im.width, reg['guide_dimensions'][1] / im.height)
        ox = (reg['guide_dimensions'][0] - im.width * fit) / 2
        oy = (reg['guide_dimensions'][1] - im.height * fit) / 2
    scale = fit / reg['source_to_guide_scale'] * source_scale
    tx = (ox - reg['source_to_guide_translation'][0]) / reg['source_to_guide_scale'] * source_scale + source_tx
    ty = (oy - reg['source_to_guide_translation'][1]) / reg['source_to_guide_scale'] * source_scale + source_ty
    folder = base / 'dance_first10_reference_redraw_v01/registration_proposals'
    folder.mkdir(parents=True, exist_ok=True)
    stem = f'{a.id}_F{a.first_frame:04d}_{a.version}'
    calc = folder / f'{stem}_geometry.json'
    if calc.exists():
        raise RuntimeError('Preserve previous geometry calculations; select a new version.')
    obj = {'id': a.id, 'scene_frame': a.first_frame, 'canonical_source_frame': job['source_frame'],
           'canonical_source_face_bbox': sb, 'first_scene_source_face_bbox': tb,
           'source_face_width_ratio': sx, 'source_face_height_ratio': sy,
           'original_source_master_to_first_scene_uniform_scale': source_scale,
           'original_source_master_translation': [source_tx, source_ty],
           'current_asset_to_first_scene_scale': scale,
           'current_asset_to_first_scene_translation': [tx, ty], 'source_to_guide_registration': reg,
           'source_head_region_xywh': a.source_head_region, 'scene_head_region_xywh': a.scene_head_region,
           'basis': 'Largest warm-skin connected component inside declared ORIGINAL head regions only; diagnostic uniform placement proposal, never artistic acceptance or AI-video tracking.',
           'original_source_skin_detection_is_diagnostic_only': True,
           'actual_visual_registration_pass': False, 'dynamic_validated': False, 'user_accepted': False}
    calc.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    subprocess.run([sys.executable, '-X', 'utf8', str(root / 'scripts/Revise-DanceRegistrationCandidate.py'),
                    str(calc), '--output', str(folder / stem), '--dy', '0', '--end-frame', str(state['last_frame'])], check=True)


if __name__ == '__main__':
    main()
