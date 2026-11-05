"""Index this known-return batch and consumed one-time grant without promoting acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def create(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8') as f:
        f.write(json.dumps(v, ensure_ascii=False, indent=2) + '\n')

folder = base / 'review/checkpoints/v20261103_six_FIRST_user_frontshoulder_corrections_v10'
registry = read(base / 'ASSET_REGISTRY.json')
specs = [
    ('ART-G33-25', 'FIRST', 'direct_first_api_source2408_latest_curl_v01'),
    ('ART-X01-10', 'FIRST', 'direct_first_api_source4063_latest_curl_v01'),
    ('ART-G49-02', 'FIRST', 'direct_first_api_source4406_latest_curl_v01'),
    ('ART-G48-05', 'FIRST', 'direct_first_api_source4348_latest_curl_v01'),
    ('ART-G13-18', 'user_edit', 'api_user_frontal_calm_frontshoulder_once_v01'),
    ('ART-G33-24', 'user_edit', 'api_user_remove_extra_turn_twoLarge_oneSmall_v01'),
    ('ART-G33-24', 'user_edit', 'api_user_hollow_airgaps_twoLarge_oneSmall_v02'),
    ('ART-G49-01', 'new_once_grant_edit', 'api_user_rear_frontshoulder_occlusion_newgrant_v05'),
    ('ART-G48-06', 'FIRST', 'direct_first_api_source4352_latest_curl_v01'),
    ('ART-G33-28', 'FIRST', 'direct_first_api_source2427_latest_curl_v01'),
    ('ART-G48-06', 'user_edit', 'api_user_frontal_frontshoulder_natural_crop_v01'),
]
rows = []
for ident, kind, name in specs:
    run = base / f'drawings/{ident}/v01/{name}'
    result = read(run / 'result.json')
    attempt = read(run / 'attempt.json')
    image = Path(result['output_path'])
    assert result['quality'] == 'high' and result['n'] == 1
    assert attempt['api_calls'] == 1 and attempt['status'] == 'completed'
    assert attempt['maximum_automatic_retries'] == 1 and attempt['automatic_retries'] == 0
    assert sha(image) == result['output_sha256']
    primary = run / 'PRIMARY_GOAL_REVIEW.json'
    assert primary.is_file()
    review = read(primary)
    assert review['image_sha256'] == sha(image)
    selected = registry[ident]
    rows.append({'id': ident, 'operation': kind, 'image': ev(image), 'receipt': ev(run / 'result.json'),
        'attempt': ev(run / 'attempt.json'), 'root_review_for_exact_run': ev(primary),
        'independent_for_exact_run': ev(Path(review['independent_review'])),
        'elapsed_seconds': result['elapsed_seconds'], 'quality': 'high', 'n': 1,
        'configured_retry': 1, 'actual_retry': 0, 'known_terminal': True,
        'current_selected_run': selected['selected_run'], 'current_id_status': selected['status'],
        'this_raw_is_current_selected': selected['sha256'] == sha(image), 'user_accepted': False})
assert len(rows) == 11 and sum(r['operation'] == 'FIRST' for r in rows) == 6
grant_row = next(r for r in rows if r['id'] == 'ART-G49-01')
grant_path = base / 'review/USER_REAR_FRONTSHOULDER_NORMAL_VISIBLE_SIZE_20261103_v01/G49_01_NEW_ONCE_GRANT_EXECUTION.json'
create(grant_path, {'user_grant_verbatim': '可以使用一次api',
    'user_later_size_clarification': '肩膀前，可以被遮住看不见一部分，但露出的部分大小得正常',
    'operations_allowed': 1, 'operations_consumed': 1, 'known_saved': True,
    'new_API_calls_from_size_clarification': 0, 'execution': grant_row,
    'art_result': 'repair_required: remaining back-collar overlap, no automatic further call',
    'previous_extra_grant_separate_and_preserved': True})
progress = read(base / 'PROGRESS.json')
queue = read(base / 'CURL_REVISION_QUEUE_CURRENT.json')
policies = [
    base / 'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json',
    base / 'review/USER_FRONTSHOULDER_AND_SOLID_REJECTIONS_20261103_v01/POLICY.json',
    base / 'review/USER_REAR_FRONTSHOULDER_NORMAL_VISIBLE_SIZE_20261103_v01/POLICY.json',
    base / 'review/USER_G48_FRONTAL_SHOULDER_ROUTE_REJECTION_20261103_v01/POLICY.json',
    base / 'review/USER_G48_FRONTAL_SHOULDER_ROUTE_REJECTION_20261103_v01/REGISTRY_STATUS_OVERRIDE.json',
]
data = {'recorded_utc': datetime.now(timezone.utc).isoformat(), 'goal_status': 'active', 'goal_complete': False,
    'operations': rows, 'new_FIRST_images': 6, 'additional_official_API_edits': 5,
    'new_operation_total': 11, 'all_new_operations_known_terminal': True,
    'new_builtin_calls': 0, 'generation_inflight': 0, 'grant_execution': ev(grant_path),
    'latest_user_policies': [ev(p) for p in policies], 'queue': ev(base / 'CURL_REVISION_QUEUE_CURRENT.json'),
    'queue_counts': queue['counts'], 'global_status_counts': progress['status_counts'],
    'photography_index': ev(base / 'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v04.json'),
    'scope': {'planned': 307, 'source_frames': 4763, 'all_work_complete': False},
    'note': '6 FIRSTs saved; current G33-25 retained, G48-06 corrected projection retained; X01-10 wrong nearRIGHT root, G49-02 backcollar, G33-28 shoulder-outboard and G48-05 scoped frontal route are queued. G33-24 both repairs remain hollow-readability P1. G49-01 new once grant consumed, route still P1. G13-18 once trial retained. G48-02..05 historical candidate flags invalidated under explicit frontal rule; no hidden-shoulder waiver, normal mass and natural strip crop. Original raws, failed candidates, user rejections and receipts retained. 2 more G51 single-source photography candidates indexed, no binding or playback. Earlier automatic approval denials were before HTTP and resolved by direct live user same-GOAL consent; no bypass/restart. Historical UNKNOWN remains preserved.',
    'user_artistic_acceptance': False, 'dynamic_validated': False, 'production_binding_changed': False}
artifact = folder / 'BATCH_ARTIFACTS.json'
create(artifact, data)
markdown = folder / 'BATCH_ARTIFACTS.md'
lines = ['本批6张官方high首图、5次用户修正均已known保存；n=1，retry=1，实际重试均0。', '',
         '| ID | 操作 | 秒 | 当前状态 |', '| --- | --- | ---: | --- |']
lines.extend(f"| {r['id']} | {r['operation']} | {r['elapsed_seconds']} | {r['current_id_status']} |" for r in rows)
lines.extend(['', 'G48-06新版仅保留当前可见肩前投影候选，旧外悬稿的用户否决保留。G48-01..05其余旧稿继续待修。G49-01新一次授权已使用，返图仍待修，不再追加。', '',
              f"当前已出图{queue['counts']['existing_images']}项，未出首图{queue['counts']['pending_first_image']}项；最新卷标准静态候选{queue['counts']['current_policy_static_candidate']}项。", '',
              '307绘制态/4763原PV帧完整范围不变；静态候选、单帧摄影、曝光绑定、实际播放、用户艺术验收分开记录。'])
with markdown.open('x', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
goal['latest_batch_artifacts'] = {'json': ev(artifact), 'markdown': ev(markdown)}
goal['latest_G49_01_new_once_grant_execution'] = ev(grant_path)
goal_path.write_text(json.dumps(goal, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'batch': ev(artifact), 'grant_execution': ev(grant_path), 'queue_counts': queue['counts']}, ensure_ascii=False))
