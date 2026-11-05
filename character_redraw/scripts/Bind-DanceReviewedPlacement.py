"""Bind one actually reviewed placement to its exact original exposure range.

This records image selection only; a renderer still has to read and verify it,
and actual continuous art playback remains a separate gate.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from PIL import Image


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('proposal', type=Path)
    p.add_argument('--independent', type=Path, required=True)
    a = p.parse_args()
    base = Path(__file__).resolve().parents[1] / 'art/full_character_redraw_1080p_v01'
    dest = base / 'dance_first10_reference_redraw_v01'
    load = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
    sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
    proposal_path = a.proposal.resolve()
    proposal_path.relative_to(dest)
    proposal = load(proposal_path)
    primary_path = proposal_path.parent / 'PRIMARY_REGISTRATION_REVIEW.json'
    primary = load(primary_path)
    independent = load(a.independent)
    layer = Path(proposal['rendered_character_layer'])
    layer_hash = sha(layer)
    asset = load(base / 'ASSET_REGISTRY.json')[proposal['id']]
    if not asset['primary_static_pass'] or not asset['independent_static_pass']:
        raise RuntimeError('Current master artwork must have both static reviews.')
    if asset['sha256'] != proposal['current_art_sha256'] or sha(asset['image']) != asset['sha256']:
        raise RuntimeError('Proposal is no longer the current reviewed artwork.')
    if not primary.get('primary_static_registration_pass'):
        raise RuntimeError('Root actual placement review is missing.')
    for path, expected in primary['viewed_sha256'].items():
        if sha(path) != expected:
            raise RuntimeError('Root-reviewed placement evidence changed.')
    if (not independent.get('static_registration_review_passed') or
            independent.get('review_status') != 'retained_static_registration_candidate' or
            independent.get('id') != proposal['id'] or
            independent.get('current_registered_candidate_sha256') != layer_hash or
            independent.get('proposal_sha256') != sha(proposal_path)):
        raise RuntimeError('Independent actual review does not approve this exact placement.')
    if proposal['rendered_character_layer_sha256'] != layer_hash:
        raise RuntimeError('Rendered layer changed after proposal.')
    with Image.open(layer) as im:
        if im.size != (1920, 1080) or im.mode != 'RGBA' or im.getchannel('A').getextrema()[0] != 0:
            raise RuntimeError('Expected transparent 1080P layer.')
    scope = load(dest / 'PRIORITY_SCOPE.json')
    ledger_path = dest / 'EXPOSURE_BINDINGS.json'
    if ledger_path.exists():
        ledger = load(ledger_path)
    else:
        ledger = {'schema': 'magic-maid.dance-first10-actual-selected-assets/1',
                  'source_time_base': scope['original_time_base'],
                  'clip_start_pts': scope['clip_start_pts'], 'clip_end_pts_exclusive': scope['clip_end_pts_exclusive'],
                  'frames': scope['exposure_proposals']}
    first, last = independent['scene_start_frame'], independent['scene_end_frame']
    evidence_frames = {int(Path(item['path']).stem[1:]) for item in proposal['original_source_frames']}
    if evidence_frames != set(range(first, last + 1)):
        raise RuntimeError('Per-exposure placement review evidence is incomplete.')
    previous = []
    for row in ledger['frames']:
        if not first <= row['source_frame'] <= last:
            continue
        if row['source_ids'] != [proposal['id']]:
            raise RuntimeError('Placement ID conflicts with reviewed original source attribution.')
        previous.append(dict(row))
        row['actual_selected_asset_binding'] = {
            'id': proposal['id'], 'master_image': asset['image'], 'master_sha256': asset['sha256'],
            'layer_1080': str(layer), 'layer_sha256': layer_hash,
            'scale': proposal['current_asset_to_first_scene_scale'],
            'translation': proposal['current_asset_to_first_scene_translation'],
            'registration_proposal': str(proposal_path),
            'root_placement_review': str(primary_path),
            'independent_placement_review': str(a.independent.resolve()),
            'independent_placement_review_sha256': sha(a.independent),
            'static_registration_review_passed': True, 'dynamic_validated': False, 'user_accepted': False,
        }
        row['actual_render_binding_verified'] = False
    bound = sum(row['actual_selected_asset_binding'] is not None for row in ledger['frames'])
    ledger.update({'updated_utc': datetime.now(timezone.utc).isoformat(), 'bound_exposures': bound,
                   'total_exposures': len(ledger['frames']), 'unbound_exposures': len(ledger['frames']) - bound,
                   'complete': False, 'actual_continuous_playback_validated': False, 'user_accepted': False})
    if ledger_path.exists():
        with (dest / 'EXPOSURE_BINDING_HISTORY.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'utc': ledger['updated_utc'], 'previous_ledger_sha256': sha(ledger_path),
                                     'replaced_rows': previous}, ensure_ascii=False) + '\n')
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'id': proposal['id'], 'bound_exposures': bound, 'total_exposures': len(ledger['frames']),
                      'new_range': [first, last], 'dynamic_validated': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
