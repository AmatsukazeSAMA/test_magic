"""Record the user's high/n1/retry1 change without altering existing art or calls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
proof = base / 'review/api_retry1_update_20261103_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

now = datetime.now(timezone.utc).isoformat()
policy_path = base / 'API_REQUEST_POLICY_20261103_v01.json'
req_path = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v05.json'
queue_path = base / 'CURL_REVISION_QUEUE_20261103_v05.json'
assert proof.is_dir() and not any(p.exists() for p in (policy_path, req_path, queue_path))
policy = {
    'policy_id': 'official_api_high_n1_retry1_20261103_v01',
    'recorded_utc': now, 'user_statement_verbatim': '官方API high，n=1，retry=1',
    'endpoint': 'https://api.openai.com/v1/images/edits',
    'model': 'gpt-image-2.5-sunburst', 'quality': 'high', 'n': 1, 'retry': 1,
    'maximum_transport_attempts_per_new_request': 2,
    'retry_engine': 'curl standard transient errors; no retry-all-errors',
    'actual_retry_count_source': 'curl write-out JSON num_retries, saved with headers and sanitized stderr',
    'existing_attempts_and_unknown_results': 'Preserved for recovery; this future-request policy does not reopen old runs or erase their receipts.',
    'changes_curl_geometry_policy': False, 'generation_calls_by_policy_update': 0,
}
save(policy_path, policy)
defaults = read(root / 'image_defaults.json')
defaults['api_request_policy'] = {**policy, 'policy_record': ev(policy_path)}
save(root / 'image_defaults.json', defaults)

prior_req = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v04.json'
req = read(prior_req)
req['requirements_revision'] = 'goal_curl_assessment_20261103_v05'
req['recorded_utc'] = now
req['user_statements_verbatim'].append(policy['user_statement_verbatim'])
req['production_priority']['primary'] = '先补未出首图，全部新首图使用已配置官方API high、n=1、retry=1并采用最新空心两大卷加一个小卷规则。'
req['api_request_policy'] = {**policy, 'policy_record': ev(policy_path)}
req['supersedes'] = {**ev(prior_req), 'conflicts_superseded': ['Earlier retry=0 for future official API requests'],
                     'curl_geometry_unchanged': 'hollow two large turns plus one small terminal turn'}
save(req_path, req)
prior_queue = base / 'CURL_REVISION_QUEUE_20261102_v04.json'
queue = read(prior_queue)
queue['created_utc'] = now
queue['policy'] = ev(req_path)
queue['prior_queue_preserved'] = ev(prior_queue)
queue['api_request_policy'] = ev(policy_path)
for row in queue['records']:
    row['requirements_revision'] = req['requirements_revision']
save(queue_path, queue)

goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
goal.setdefault('curl_assessment_pointer_history', []).append(goal['review']['mandatory_curl_requirements'])
pointer = {**ev(req_path), 'requirements_revision': req['requirements_revision'],
           'construction_policy_id': req['construction_policy_id'], 'recorded_utc': now,
           'old_reports_preserved': True, 'no_automatic_reacceptance': True}
goal['review']['mandatory_curl_requirements'] = pointer
goal['review']['mandatory_left_side_prompt_prefix'] = defaults['generation_prompt_prefix']
goal['latest_curl_assessment_requirements'] = pointer
goal['latest_hollow_drill_policy']['requirements'] = pointer
goal['existing_curl_revision_queue'] = ev(queue_path)
goal['current_priority'] = str(queue_path.resolve())
goal['latest_user_production_priority'] = req['production_priority']
goal['API'].update({'quality': 'high', 'n': 1, 'retry': 1,
                    'automatic_paid_retries': True, 'maximum_automatic_retries': 1,
                    'retry_policy': ev(policy_path)})
goal['latest_api_request_policy'] = {**policy, 'policy_record': ev(policy_path)}
goal['updated_utc'] = now
goal['complete'] = False
save(goal_path, goal)

selection_path = root / 'CURRENT_SELECTION.json'
selection = read(selection_path)
selection.update({'latest_curl_requirements': pointer, 'existing_curl_revision_queue': ev(queue_path),
                  'current_priority': goal['current_priority'], 'latest_api_request_policy': goal['latest_api_request_policy']})
save(selection_path, selection)
doc = base / 'GOAL_CURRENT_REQUIREMENTS.md'
text = doc.read_text(encoding='utf-8').replace('n=1，retry=0', 'n=1，retry=1')
text += '\n官方API最新参数：**high，n=1，retry=1**；单个新请求最多追加一次临时错误重试，实际次数与响应证据逐次保留。\n'
doc.write_text(text, encoding='utf-8')
save(proof / 'UPDATE_RECEIPT.json', {
    'recorded_utc': now, 'api_policy': ev(policy_path), 'requirements': ev(req_path),
    'queue': ev(queue_path), 'goal': ev(goal_path), 'defaults': ev(root / 'image_defaults.json'),
    'provider': ev(root / 'scripts/Invoke-ReferenceImage.ps1'),
    'first_release_helper': ev(root / 'scripts/Release-RootReviewedFirstApi.py'),
    'masked_release_helper': ev(root / 'scripts/Release-RootReviewedMaskedApi.py'),
    'counts_unchanged': queue['counts'], 'original_images_modified': False, 'generation_calls': 0,
})
print(json.dumps({'updated': True, 'policy': policy['policy_id'], 'counts': queue['counts'],
                  'generation_calls': 0}, ensure_ascii=False))
