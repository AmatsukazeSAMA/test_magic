"""Preserve the one scoped reference-driven return and close its evidence record."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def evidence(p):
    assert p.is_file(), str(p)
    return {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

folder = base / 'review/checkpoints/v20261103_user360_posterior_bob_one_whole_v12'
folder.mkdir(parents=True, exist_ok=True)
batch_path = folder / 'BATCH_ARTIFACTS.json'
assert not batch_path.exists(), 'Preserve existing evidence.'
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(folder / 'GOAL_BEFORE_REFERENCE_CLOSEOUT.json', goal)
prior_pause = {key: goal.pop(key) for key in (
    'pause_status_confirmed_from_goal_service', 'pause_recorded_utc', 'pause_reason'
) if key in goal}
if prior_pause:
    goal.setdefault('pause_history', []).append({
        'historical_pause_fields': prior_pause,
        'resolution': 'Requested side/back reference supplied; actual goal service returned active this turn.'
    })
run = base / 'drawings/ART-G49-01/v01/whole_imggen_user_video_smooth_backbob_v07'
policy = base / 'review/USER_POSTERIOR_BOB_360_REFERENCE_20261103_v01/POLICY.json'
review = base / 'review/SOL_WHOLE_G49_01_VIDEO_POSTERIOR_BOB_V07_20261103_v01.json'
now = datetime.now(timezone.utc).isoformat()
batch = {
    'created_utc': now,
    'user_request': '后发太乱，参考该视频',
    'scope': 'One ART-G49-01 posterior-bob representative using new user video geometry.',
    'posterior_bob_policy': evidence(policy),
    'reference_manifest': evidence(base / 'inputs/user_upper_body_360_hair_structure_20261103_v01/REFERENCE_MANIFEST.json'),
    'builtin_operations_this_turn': 1, 'official_API_calls_this_turn': 0,
    'generation': evidence(run / 'BUILTIN_GENERATION.json'),
    'raw': evidence(run / 'character_imggen_original.png'),
    'white_preview': evidence(run / 'qa_white.png'),
    'prompt': evidence(run / 'prompt_imggen.txt'),
    'independent_review': evidence(review),
    'before_after': evidence(policy.parent / 'BEFORE_AFTER_V06_V07.png'),
    'old_v06': 'Preserved; repair_required for user posterior-bob rejection. Earlier valid shoulder-front observations remain historical.',
    'new_v07': 'Root actual and independent retained_static_candidate; short nape tips, regular arcs and soft tone remain P2 observations.',
    'reference_authority': 'New user360 video supplies posterior-bob geometry only; original PV still owns pose, style, framing and timing.',
    'actual_reference_continuous_playback': False,
    'full_hidden_curl_geometry_certified': False,
    'user_artistic_acceptance': False, 'continuous_PV_playback_validated': False,
    'goal_complete': False, 'generation_inflight': 0,
    'all_inputs_prior_candidates_rejections_and_receipts_preserved': True
}
save(batch_path, batch)
if goal.get('latest_batch_artifacts'):
    goal.setdefault('batch_artifact_history', []).append(goal['latest_batch_artifacts'])
goal['latest_batch_artifacts'] = evidence(batch_path)
goal['latest_posterior_bob_representative'] = {
    'id': 'ART-G49-01', 'status': 'retained_static_candidate',
    'raw': evidence(run / 'character_imggen_original.png'),
    'policy': evidence(policy), 'independent_review': evidence(review),
    'user_accepted': False
}
goal['goal_status'] = 'active'
goal['updated_utc'] = now
save(goal_path, goal)
print(json.dumps({'batch': evidence(batch_path), 'goal_status': goal['goal_status'], 'complete': False}, ensure_ascii=False))
