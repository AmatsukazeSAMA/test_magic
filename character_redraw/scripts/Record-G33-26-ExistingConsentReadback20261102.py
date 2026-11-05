"""Record new scope checks before re-presenting the same known-unsent command."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G33-26/v01/first_api_source2412_raisedindex_lowpalm_user11_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
a = read(auth)
assert a['user_reply_verbatim'] == '允许本次44及GOAL后续同类素材'
assert '此GOAL后续同类人物稿、参考图及必要蒙版发送至同一官方API' in a['question_text']
formal = run / 'API_PREPARED_REQUEST.json'
assert sha(formal) == 'a9948fa789eb4af7b901783c2eb3bc2a99a2d44af9f3952c599d9b6c88a6162f'
q = read(formal)
scope = read(run / 'AUTHORIZATION_SCOPE_CHECK_v01.json')
assert q['InputImages'] == [x['path'] for x in scope['refs']]
for item in scope['refs']:
    p = Path(item['path'])
    p.relative_to(run / 'inputs')
    assert sha(p) == item['sha256']
for name in ['attempt.json', 'result.json', 'character_api_original.png']:
    assert not (run / name).exists(), 'A sent/returned attempt must be recovered, not repeated.'
out = run / 'ROOT_EXISTING_USER_CONSENT_READBACK_AFTER_REJECTION_v01.json'
assert not out.exists(), 'Preserve the prior check.'
v = {'id': 'ART-G33-26', 'checked_utc': datetime.now(timezone.utc).isoformat(),
     'actual_user_authority_in_current_thread': {'path': str(auth), 'sha256': sha(auth),
          'question_text': a['question_text'], 'answer_verbatim': a['user_reply_verbatim']},
     'exact_future_scope_reconfirmed': 'The actual user answer explicitly includes subsequent same-category full-PV GOAL drawing art/references and necessary masks to the same official API, not merely44 or repairs.',
     'root_actually_viewed_each_six_payload_images': scope['refs'],
     'root_observation': 'All six are this project anime PV/current pose, tiny AI hair-only crop, user-approved complete gray head/curl scale context, user-provided gray return detail crop, source2412 own eyes/neutral closed mouth crop, and unlit pigment key. No personal document, credential, unrelated file or endpoint was added.',
     'formal_request': {'path': str(formal), 'sha256': sha(formal)},
     'new_scope_checks_after_rejection': True,
     'same_command_payload_endpoint_and_runner_preserved': True,
     'API_requests_already_sent': 0, 'known_unsent_verified': True,
     'endpoint': 'https://api.openai.com/v1/images/edits', 'model': 'gpt-image-2.5-sunburst',
     'quality': 'high', 'size': '640x1040', 'background': 'transparent', 'n': 1,
     'automatic_retries': 0, 'not_unknown_paid_request_retry': True,
     'action': 'Present the unchanged one-first-image command to approval review with the actual explicit future-project consent; do not use any alternate channel or bypass.',
     'user_artistic_acceptance': False}
out.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'scope_readback': str(out), 'sha256': sha(out), 'API_calls': 0}, ensure_ascii=False))
