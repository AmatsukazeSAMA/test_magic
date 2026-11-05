"""Freeze this progress and user-correction chain without claiming full completion."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
save = lambda p, q: p.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
folder = base / 'review/checkpoints/v20261104_user_three_curl_corrections_and_smaller_light_cap_v27'
assert (folder / 'STATUS.json').exists()
assert not (folder / 'FOLLOWUP_USER_THREE_CURL_AND_SMALLER_CAP.json').exists()
registry = read(base / 'ASSET_REGISTRY.json')
records = []
for ident in ('ART-G33-48', 'ART-X01-14', 'ART-G13-28', 'ART-G13-29'):
    selected = registry[ident]
    assert selected['status'] == 'reviewed_static_candidate'
    assert sha(Path(selected['image'])) == selected['sha256']
    item = {'id': ident, 'selected_image': ev(Path(selected['image'])),
        'primary_review': ev(Path(selected['primary_review'])), 'independent_review': ev(Path(selected['independent_review'])),
        'inherited_parent_art_review': selected.get('inherited_parent_art_review'),
        'user_accepted': False, 'photography_approved': False, 'dynamic_validated': False}
    if ident == 'ART-G33-48':
        assert selected['secondary_eye_local_status'] == 'not_applicable_closed_no_visible_iris_actual_viewed'
        item['eye_exemption'] = selected['secondary_eye_local_status']
    else:
        assert selected['secondary_eye_local_passed']
        vpath = Path(selected['eye_local_verification']['path'])
        verification = read(vpath)
        assert verification['outside_mask_changed_pixels'] == verification['alpha_changed_pixels'] == verification['protected_glint_changed_pixels'] == 0
        item['eye_verification'] = ev(vpath)
        item['eye_changed_pixels'] = verification['changed_pixels']
    records.append(item)

batch = base / 'review/checkpoints/v20261104_three_FIRST_four_whole_user_curl_repairs_before_smaller_cap_v26/BATCH_ARTIFACTS.json'
assert read(batch)['official_API_added'] == 3 and read(batch)['builtin_added'] == 4
delivery = base / 'review/USER_THREE_ROOT_COUNT_SIDE_CORRECTIONS_20261104_v01/DELIVERY/DELIVERY.json'
assert len(read(delivery)['entries']) == 3
snapshots = []
for name in ('PROGRESS.json', 'ASSET_REGISTRY.json', 'API_CALL_STATISTICS.json', 'CURL_REVISION_QUEUE_CURRENT.json', 'EYE_LOCAL_SECONDARY_REVISION_QUEUE_CURRENT.json'):
    target = folder / ('SNAPSHOT_' + name)
    assert not target.exists()
    shutil.copyfile(base / name, target)
    snapshots.append(ev(target))
followup = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'previous_goal_turn_classification': 'no_progress',
    'previous_goal_turn_basis': 'Previous response reverified and redelivered an existing X01-12 correction; no new drawing or selected-state mutation.',
    'this_goal_turn_classification': 'progress',
    'full_scope_preserved': {'planned_states': 307, 'original_PV_exposures': 4763, 'first_dance_states': 66},
    'official_FIRST_batch': ev(batch), 'official_API_added_since_v25': 3, 'builtin_added_since_v25': 4,
    'official_API_after_latest_smaller_light_cap_feedback': 0, 'builtin_after_latest_smaller_light_cap_feedback': 0,
    'entries': records, 'user_delivery': ev(delivery),
    'three_frame_user_feedback': ev(base / 'review/USER_THREE_ROOT_COUNT_SIDE_CORRECTIONS_20261104_v01/USER_INSTRUCTION_AND_EXACT_ARTIFACTS.json'),
    'X01_rectangular_coil_user_rejection': ev(base / 'review/USER_X01_14_RECTANGULAR_COIL_REJECTION_20261104_v01/USER_REJECTION_AND_REQUIRED_ROUNDED_RIBBON.json'),
    'X01_smaller_eye_cap_user_feedback': ev(base / 'review/USER_X01_14_LIGHT_CAP_AREA_TOO_LARGE_20261104_v01/USER_FEEDBACK_AND_LOCAL_CAP_TRIAL.json'),
    'smaller_light_fraction_trial': {'coverage_weighted_fraction_approx': .225, 'is_ROOT_trial_not_user_numerical_specification': True, 'global_user_accepted_baseline': False},
    'G32_03_derived_crop_and_four_eye_PREP_only': ev(base / 'review/G32_03_DERIVED_CROP_AND_EYE_PREP_HANDOFF_20261104_v01.json'),
    'G32_03_PREP_not_counted_as_selected_or_eye_applied': True,
    'snapshots': snapshots, 'generation_inflight': 0, 'user_accepted': False,
    'actual_dynamic_playback_validated': False, 'goal_status': 'active', 'goal_complete': False,
    'next_work': 'Continue55 missingFIRSTs and remaining current-art fixes/normal-eye local edits, then source-PTS registration/1080 layers and actual original/slow shot playback. Keep restricted G49-03..06 and prior rejected/unknown requests unissued; no Git push.'}
followpath = folder / 'FOLLOWUP_USER_THREE_CURL_AND_SMALLER_CAP.json'
save(followpath, followup)
goalpath = base / 'GOAL_EXECUTION.json'
goal = read(goalpath)
save(folder / 'GOAL_EXECUTION_BEFORE_CLOSEOUT_POINTERS.json', goal)
for key in ('latest_missing_FIRST_batch', 'latest_missing_FIRST_batch_artifacts'):
    if goal.get(key):
        goal.setdefault(key + '_pointer_history', []).append(goal[key])
    goal[key] = ev(batch)
goal['latest_user_three_curl_correction_delivery'] = ev(delivery)
goal['latest_user_three_curl_correction_closeout'] = ev(followpath)
goal['latest_smaller_eye_light_cap_trial_result'] = {'image': records[1]['selected_image'], 'eye_verification': records[1]['eye_verification'],
    'scope': 'Current X01-14 trial only; deep gray dominant, smaller lower gray cap, no outline/glint/outside/alpha change; no global artistic acceptance inferred.',
    'user_accepted': False}
goal['updated_utc'] = followup['recorded_utc']
save(goalpath, goal)
print(json.dumps({'followup': ev(followpath), 'delivery': ev(delivery), 'remaining_FIRST': read(batch)['remaining_without_FIRST'], 'goal_complete': False}, ensure_ascii=False))
