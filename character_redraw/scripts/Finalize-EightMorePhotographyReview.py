"""Record root's already actual visual decisions; no art/binding mutations."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
folder = base / 'review/PHOTOGRAPHY_PREP_EIGHT_MORE_STATIC_CANDIDATES_20261103_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def verify(e):
    assert sha(Path(e['path'])) == e['sha256'], e['path']
def create(p, data):
    with p.open('x', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

manifest_path = folder / 'FINAL_PHOTOGRAPHY_PREP_MANIFEST.json'
assert sha(manifest_path) == '29366fe550cd269817c25616c1c0e7da244faa57c3389acac413dbb297129270'
cases = read(manifest_path)['cases']
notes_path = folder / 'ROOT_ACTUAL_VIEW_NOTES.json'
notes = read(notes_path)
sol_path = base / 'review/SOL_PHOTOGRAPHY_EIGHT_MORE_CURRENT_STATIC_20261103_v01.json'
assert sha(sol_path) == '06cc8de9244cd16dfe5ee2028932eec6ab8a59322c14d04cea67afc399f3218b'
sol = read(sol_path)
independent = {r['case_key']: r for r in sol['entries']}
assert set(notes['actual_viewed_case_keys']) == {c['case_key'] for c in cases}
assets = read(base / 'ASSET_REGISTRY.json')
req_path = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
req = read(req_path)
assert sha(req_path) == '93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
entries = []
for c in cases:
    key = c['case_key']
    s = independent[key]
    for e in [c['raw'], c['source'], c['proposed_geometry_not_selected'], c['transparent_unselected_layer'], *c['surfaces'].values(), c['same_native_comparison']]:
        verify(e)
    asset = assets[c['id']]
    assert asset['sha256'] == c['raw']['sha256']
    assert asset['primary_static_pass'] and asset['independent_static_pass']
    assert s['raw']['sha256'] == c['raw']['sha256']
    assert s['proposal']['sha256'] == c['proposed_geometry_not_selected']['sha256']
    assert s['layer']['sha256'] == c['transparent_unselected_layer']['sha256']
    assert s['source_frame'] == c['source_frame'] and s['source_pts'] == c['source_pts']
    conditional = c['id'] == 'ART-X01-07'
    assert s['decision'] == ('conditional' if conditional else 'candidate')
    cut = c.get('entity_cut_projects_y')
    if c.get('entity_cut_raw_y') is not None:
        assert cut is not None and cut > 1080
    actual = [c['surfaces']['white'], c['surfaces']['black'], c['same_native_comparison']]
    primary_art = Path(asset['primary_review'])
    sol_art = Path(asset['independent_review'])
    r = {
        'id': c['id'], 'case_key': key,
        'reviewer': 'root actual full1080 WB and same-native comparison inspection',
        'review_status': 'conditional_static_registration_candidate' if conditional else 'retained_static_registration_candidate',
        'primary_static_registration_pass': not conditional,
        'conditional_registration_candidate': conditional,
        'raw': c['raw'], 'layer': c['transparent_unselected_layer'],
        'proposal': c['proposed_geometry_not_selected'], 'source': c['source'],
        'reviewed_source_frames': [c['source_frame']], 'source_pts': c['source_pts'],
        'scale': c['scale'], 'translation': c['translation'],
        'entity_cut_raw_y': c.get('entity_cut_raw_y'),
        'entity_cut_projects_y': cut,
        'actual_viewed_evidence': actual, 'observation': notes['notes'][key],
        'independent_placement_review': ev(sol_path),
        'independent_static_registration_pass': bool(s['static_registration_review_passed']),
        'static_art_reviews': {'root': ev(primary_art), 'Sol': ev(sol_art)},
        'requirements': {**ev(req_path), 'requirements_revision': req['requirements_revision'], 'construction_policy_id': req['construction_policy_id']},
        'single_source_frame_only': True, 'all_exposure_frames_reviewed': False,
        'front_shoulder_route_certified': False,
        'existing_art_P2_not_cleared': True,
        'production_binding': False, 'production_selected': False,
        'dynamic_validated': False, 'actual_playback': False, 'user_accepted': False,
        'raw_art_pixels_modified': False, 'alpha_cleanup_applied': False, 'partwise_warp': False,
    }
    if conditional:
        r['before_production_binding'] = 'Resolve cap/upper-body versus waist/ankle proportion residual by actual art/photography review. No local warp; existing candidate kept only for comparison.'
    entries.append(r)
now = datetime.now(timezone.utc).isoformat()
primary_path = folder / 'PRIMARY_EIGHT_STATIC_PHOTOGRAPHY_REVIEW.json'
create(primary_path, {
    'reviewer': 'root actual visual inspection', 'recorded_utc': now,
    'manifest': ev(manifest_path), 'actual_notes': ev(notes_path),
    'independent_placement_review': ev(sol_path), 'entries': entries,
    'actual_viewed_image_count': sum(len(r['actual_viewed_evidence']) for r in entries),
    'summary': {'unconditional_single_source_candidates': 8, 'conditional_single_source_candidates': 1, 'distinct_art_states': 8},
    'X01_baseline_scope': 'curl drawing method only; not size/axis/body/camera/user acceptance',
    'no_new_generation': True, 'production_binding': False, 'dynamic_validated': False, 'user_accepted': False,
})
old_path = base / 'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v02.json'
assert sha(old_path) == '4bf2af0e9b78048a78ffb66d6d4f314864b45afffdbdab27165428e078d44cd0'
old = read(old_path)
new = {
    'schema': 'magic-maid.reviewed-single-source-1080-candidates/1',
    'recorded_utc': now, 'previous_index': ev(old_path),
    'primary_placement_review': ev(primary_path), 'independent_placement_review': ev(sol_path),
    'entries': [*old['entries'], *entries],
    'summary': {'total_single_source_review_candidates': len(old['entries']) + len(entries),
                'new_unconditional_candidates': 8, 'new_conditional_candidates': 1,
                'distinct_art_states': len({r['id'] for r in [*old['entries'], *entries]})},
    'production_binding': False, 'all_exposures_reviewed': False,
    'dynamic_validated': False, 'actual_playback': False, 'user_accepted': False,
    'note': 'Only exact raw/proposal/single own source reviewed. Previous entries preserved. X01-07 remains conditional and ineligible for production binding pending proportion disposition. No CURRENT_SELECTION or exposure bindings changed.'
}
new_path = base / 'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v03.json'
create(new_path, new)
assert read(new_path)['entries'][:len(old['entries'])] == old['entries']
print(json.dumps({'primary_review': ev(primary_path), 'index': ev(new_path), 'summary': new['summary']}, ensure_ascii=False))
