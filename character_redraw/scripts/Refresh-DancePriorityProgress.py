"""Record explicitly reviewed current-policy cels and refresh first-clip progress.

Use --record-ids only after actual root and Sol review under the latest rules.
Legacy static approvals do not automatically satisfy this policy index.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from EyeLocalPolicy import current_eye_style_pass, dance_b_state_ids, inherited_curl_review_passed


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--record-ids', nargs='*', default=[])
    a = p.parse_args()
    base = Path(__file__).resolve().parents[1] / 'art/full_character_redraw_1080p_v01'
    folder = base / 'dance_first10_reference_redraw_v01'
    load = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
    sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
    def review_entry(path, work_id):
        review = load(Path(path))
        entries = review.get('entries', review.get('records'))
        return next(r for r in entries if r['id'] == work_id) if entries is not None else review

    scope = load(folder / 'PRIORITY_SCOPE.json')
    defaults = load(base.parents[1] / 'image_defaults.json')
    curl_policy_id = defaults.get('drill_structure_rule', {}).get('policy_id')
    registry = load(base / 'ASSET_REGISTRY.json')
    index_path = folder / 'CURRENT_POLICY_STATIC_REVIEW_INDEX.json'
    index = load(index_path) if index_path.exists() else {'records': {}, 'history': []}
    ids = {s['id'] for s in scope['states']}
    for work_id in a.record_ids:
        if work_id not in ids:
            raise RuntimeError('Current priority index accepts only first-clip state IDs.')
        art = registry[work_id]
        if not art['primary_static_pass'] or not art['independent_static_pass']:
            raise RuntimeError('Both actual static reviews are required before policy recording.')
        parent = art.get('inherited_parent_art_review')
        if art.get('locally_repaired') and not art.get('whole_imggen_completed') and not parent:
            raise RuntimeError('Intermediate local repair cannot enter the current-policy index.')
        if sha(art['image']) != art['sha256']:
            raise RuntimeError('Reviewed original bytes changed.')
        primary = review_entry(art['primary_review'], work_id)
        independent = review_entry(art['independent_review'], work_id)
        if parent:
            if primary.get('inherited_parent_art_review') != parent:
                raise RuntimeError('Selected art and root review disagree on the inherited evidence.')
            valid_eye = inherited_curl_review_passed(base.parents[1], art, curl_policy_id)
            if not current_eye_style_pass(art, valid_eye, dance_b_state_ids(base.parents[1])):
                raise RuntimeError('The eye post-pass needs verified eye pixels and both current parent curl reviews.')
        if curl_policy_id and (primary.get('curl_structure_policy_id') != curl_policy_id
                               or independent.get('curl_structure_policy_id') != curl_policy_id):
            raise RuntimeError('Both actual reviews must explicitly inspect the current curl construction; old approvals cannot be inherited.')
        value = {key: art[key] for key in ['id', 'image', 'sha256', 'selected_run', 'primary_review', 'independent_review']}
        value.update({'recorded_utc': datetime.now(timezone.utc).isoformat(),
                      'policy': 'Original-only action; AI hair motion only; unlit gray/mint hair; fixed anatomical LEFT root with view-appropriate occlusion; current monochrome eye method.',
                      'basis': 'Explicit root recording after actual root and Sol current-policy visual review, never inherited from a legacy approval.'})
        if curl_policy_id:
            value['curl_structure_policy_id'] = curl_policy_id
        if parent:
            value['inherited_parent_art_review'] = parent
        for key in ['primary_review', 'independent_review']:
            value[key + '_sha256'] = sha(value[key])
        if work_id in index['records'] and index['records'][work_id] != value:
            index['history'].append(index['records'][work_id])
        index['records'][work_id] = value
    valid = {}
    prior_valid = {}
    for work_id, record in index['records'].items():
        art = registry.get(work_id, {})
        if (art.get('primary_static_pass') and art.get('independent_static_pass')
                and art.get('sha256') == record['sha256']
                and sha(record['image']) == record['sha256']
                and all(sha(art[key]) == record[key + '_sha256']
                        for key in ['primary_review', 'independent_review'])
                and all(sha(ref['path']) == ref['sha256'] for ref in
                        record.get('inherited_parent_art_review', {}).get('art_reviews', {}).values())):
            if not curl_policy_id or record.get('curl_structure_policy_id') == curl_policy_id:
                valid[work_id] = record
            else:
                prior_valid[work_id] = record
    ledger = load(folder / 'EXPOSURE_BINDINGS.json')
    rows = ledger['frames']
    selected = sum(bool(r.get('actual_selected_asset_binding')) for r in rows)
    selected_current = sum(bool(r.get('actual_selected_asset_binding'))
                           and r['actual_selected_asset_binding']['id'] in valid
                           and r['actual_selected_asset_binding']['master_sha256'] == valid[r['actual_selected_asset_binding']['id']]['sha256']
                           for r in rows)
    states = []
    for state in scope['states']:
        art = registry.get(state['id'], {})
        states.append({'id': state['id'], 'first_frame': state['first_frame'], 'last_frame': state['last_frame'],
                       'current_policy_static_review_passed': state['id'] in valid,
                       'retained_prior_policy_static_evidence': prior_valid.get(state['id']),
                       'curl_construction_recheck_required': bool(curl_policy_id and state['id'] not in valid),
                       'current_registry_status': art.get('status', 'pending'),
                       'current_image': art.get('image'), 'current_image_sha256': art.get('sha256'),
                       'current_policy_review_evidence': valid.get(state['id']),
                       'dynamic_validated': False, 'user_accepted': False})
    progress = {'updated_utc': datetime.now(timezone.utc).isoformat(),
                'source_frame_range': [834, 1133], 'source_time_base': scope['original_time_base'],
                'clip_start_pts': scope['clip_start_pts'], 'clip_end_pts_exclusive': scope['clip_end_pts_exclusive'],
                'total_visible_states': len(states), 'current_policy_static_reviewed_states': len(valid),
                'curl_structure_policy_id': curl_policy_id,
                'retained_prior_policy_static_evidence_states': len(prior_valid),
                'review_revision_note': 'Latest construction is hollow two large turns plus one small terminal turn. The current user-approved X01 reference is curl drawing method only; it does not approve the whole character or any old dance state. Historical G33-11 and earlier static reports remain preserved, with no automatic acceptance under the latest rule. Actual opaque gray returns must not be removed merely to force alpha holes.',
                'remaining_current_policy_static_states': len(states) - len(valid),
                'total_original_exposures': len(rows), 'selected_asset_bound_exposures': selected,
                'current_policy_asset_bound_exposures': selected_current,
                'actual_render_binding_verified_exposures': sum(bool(r.get('actual_render_binding_verified')) for r in rows),
                'actual_continuous_playback_validated': False, 'complete': False, 'user_accepted': False,
                'states': states}
    index['current_curl_structure_policy_id'] = curl_policy_id
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / 'PROGRESS.json').write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in progress.items() if key != 'states'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
