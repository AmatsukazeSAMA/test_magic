"""Save root's completed full WB/native photography review of two G51 states."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
folder = base / 'review/PHOTOGRAPHY_PREP_THREE_NEW_STATIC_CANDIDATES_20261103_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def create(p, v):
    with p.open('x', encoding='utf-8') as f:
        f.write(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
def verify(e):
    assert sha(Path(e['path'])) == e['sha256'], e['path']

manifest_path = folder / 'FINAL_PHOTOGRAPHY_PREP_MANIFEST.json'
assert sha(manifest_path) == 'bb76210f03793a3b19c0c68bededf4a9463db265213ea569f9ac42e8c9b67197'
sol_path = base / 'review/SOL_PHOTOGRAPHY_THREE_NEW_CURRENT_STATIC_20261103_v01.json'
assert sha(sol_path) == 'f42b6b21d8a1389704f9118674d5fef3e083391c6ba601738c91ba786a494413'
sol = {e['case_key']: e for e in read(sol_path)['entries']}
assets = read(base / 'ASSET_REGISTRY.json')
notes = {
    'ART-G51-09': 'Root actually inspected full1080 white/black, same-native source/proposal comparison and own4617 native. Inclined torso/head, single near glove across skirt, hidden far hand, waist/knees/ankles and both complete shoes register plausibly under one whole uniform transform. Cap crown is about10px high with small wrist/skirt/tie residuals; no visible cut inside canvas. Existing art softness and curl-depth caveats remain; single source only.',
    'ART-G51-10': 'Root actually inspected nestedv02 full1080 white/black, same-native comparison and own4625 native. Own round unequal eyes, tiny closed mouth, two unequal low gloves, near straight arm, hips/knees/ankles and both whole shoes broadly retained and placed together. Some cap/eye, shoulder and glove/skirt contour residuals remain; no interior physical cut. User-approved tiny eye-corner marks are allowed. Single source only; curl route not certified by photography.'
}
entries = []
for c in read(manifest_path)['cases']:
    if c['id'] not in notes:
        continue
    s = sol[c['case_key']]
    for e in [c['raw'], c['source'], c['proposed_geometry_not_selected'], c['transparent_unselected_layer'], c['same_native_comparison'], *c['surfaces'].values()]:
        verify(e)
    a = assets[c['id']]
    assert a['sha256'] == c['raw']['sha256'] and a['primary_static_pass'] and a['independent_static_pass']
    assert s['static_registration_review_passed'] and s['raw_sha256'] == a['sha256']
    entries.append({
        'id': c['id'], 'case_key': c['case_key'], 'reviewer': 'root actual full1080 WB and same-native source inspection',
        'review_status': 'retained_static_registration_candidate', 'primary_static_registration_pass': True,
        'independent_static_registration_pass': True, 'raw': c['raw'], 'layer': c['transparent_unselected_layer'],
        'proposal': c['proposed_geometry_not_selected'], 'source': c['source'],
        'reviewed_source_frames': [c['source_frame']], 'source_pts': c['source_pts'],
        'scale': c['scale'], 'translation': c['translation'],
        'actual_viewed_evidence': [c['surfaces']['white'], c['surfaces']['black'], c['same_native_comparison'], c['source']],
        'observation': notes[c['id']], 'independent_placement_review': ev(sol_path),
        'static_art_reviews': {'root': ev(Path(a['primary_review'])), 'Sol': ev(Path(a['independent_review']))},
        'single_source_frame_only': True, 'all_exposure_frames_reviewed': False,
        'front_shoulder_route_certified': False, 'existing_art_P2_not_cleared': True,
        'production_binding': False, 'production_selected': False, 'dynamic_validated': False,
        'actual_playback': False, 'user_accepted': False, 'raw_art_pixels_modified': False,
        'alpha_cleanup_applied': False, 'partwise_warp': False,
    })
assert len(entries) == 2
now = datetime.now(timezone.utc).isoformat()
primary = folder / 'PRIMARY_TWO_G51_STATIC_PHOTOGRAPHY_REVIEW.json'
create(primary, {'recorded_utc': now, 'manifest': ev(manifest_path), 'independent': ev(sol_path), 'entries': entries,
    'G13_18_old_proposals': 'Preserved historical only: newer user-requested shoulder-front API raw requires its own fresh registration.',
    'new_API_calls': 0, 'production_binding': False, 'user_accepted': False})
old = base / 'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v03.json'
assert sha(old) == '962f7553398b5240a38aa58bd873887864217e61de5a0cac6a26c27a7dd40255'
previous = read(old)
all_entries = [*previous['entries'], *entries]
new = base / 'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v04.json'
create(new, {'schema': previous['schema'], 'recorded_utc': now, 'previous_index': ev(old),
    'primary_placement_review': ev(primary), 'independent_placement_review': ev(sol_path), 'entries': all_entries,
    'summary': {'total_single_source_review_candidates': len(all_entries), 'new_unconditional_candidates': 2,
                'new_conditional_candidates': 0, 'distinct_art_states': len({e['id'] for e in all_entries})},
    'production_binding': False, 'all_exposures_reviewed': False, 'dynamic_validated': False,
    'actual_playback': False, 'user_accepted': False,
    'note': 'Only exact source/raw/proposal reviewed. Existing conditional X01-07 remains conditional. G13-18 oldraw proposals not promoted after newer API raw.'})
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
review = goal['review']
review.setdefault('single_source_candidate_index_history', []).append(review['latest_single_source_1080p_candidates'])
review['latest_single_source_1080p_candidates'] = ev(new)
goal['latest_single_source_1080p_candidates'] = ev(new)
goal_path.write_text(json.dumps(goal, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'primary': ev(primary), 'index': ev(new), 'summary': read(new)['summary']}, ensure_ascii=False))
