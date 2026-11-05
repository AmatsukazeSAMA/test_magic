"""Record root's already-performed actual placement inspection, never inspect art."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p = argparse.ArgumentParser(__doc__)
p.add_argument('folder', type=Path)
p.add_argument('--note', required=True)
p.add_argument('--extra-viewed', nargs='*', type=Path, default=[])
a = p.parse_args()
base = Path(__file__).resolve().parents[1] / 'art/full_character_redraw_1080p_v01'
folder = a.folder.resolve()
allowed_roots = (base / 'dance_first10_reference_redraw_v01/registration_proposals',
                 base / 'coverage/review')
if not any(folder.is_relative_to(root) for root in allowed_roots):
    raise SystemExit('Expected a versioned placement in the dance or source-review workspace.')
read = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
out = folder / 'PRIMARY_REGISTRATION_REVIEW.json'
if out.exists():
    raise SystemExit('Existing root photographic review preserved.')
proposal_path = folder / 'REGISTRATION_PROPOSAL.json'
q = read(proposal_path)
asset = read(base / 'ASSET_REGISTRY.json')[q['id']]
if not asset['primary_static_pass'] or not asset['independent_static_pass']:
    raise SystemExit('Current master is not both visually reviewed.')
if sha(Path(asset['image'])) != asset['sha256'] or asset['sha256'] != q['current_art_sha256']:
    raise SystemExit('Proposal/current master bytes changed.')
surfaces = [folder / n for n in ['character_1920x1080_proposed.png',
            'pink_position_proposed.png', 'source_comparison.png',
            'all_first_hold_source_frames.png']]
frames = sorted(int(Path(r['path']).stem[1:]) for r in q['original_source_frames'])
assert frames == list(range(frames[0], frames[-1] + 1))
assert sha(surfaces[0]) == q['rendered_character_layer_sha256']
viewed = [*surfaces, proposal_path, *[p.resolve() for p in a.extra_viewed]]
v = {'id': q['id'], 'reviewer': 'root actual full-frame and original-exposure visual inspection',
     'reviewed_utc': datetime.now(timezone.utc).isoformat(),
     'scene_frame_range': [frames[0], frames[-1]], 'source_frame_range': [frames[0], frames[-1]],
     'primary_static_registration_pass': True, 'current_master_sha256': asset['sha256'],
     'current_registered_candidate_sha256': sha(surfaces[0]),
     'actual_viewed_paths': [str(p) for p in viewed],
     'viewed_sha256': {str(p): sha(p) for p in viewed},
     'all_original_hold_rows_actually_viewed': True, 'observation': a.note,
     'uniform_scale': q['current_asset_to_first_scene_scale'],
     'uniform_translation': q['current_asset_to_first_scene_translation'],
     'current_master_unchanged_by_uniform_registration': True,
     'no_partwise_warp': True, 'no_reference_pixel_paste': True,
     'independent_static_registration_pass': False,
     'dynamic_validated': False, 'continuous_playback_validated': False, 'user_accepted': False}
out.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'root_placement_review': str(out), 'sha256': sha(out),
                  'binding_changed': False}, ensure_ascii=False))
