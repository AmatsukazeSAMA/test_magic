"""Preserve existing failed attempt and classify the observed local proxy failure."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G12-58/v01/first_api_source1071_rebound_originalmouth_user11_v01'
attempt_path = run / 'attempt.json'
a = json.loads(attempt_path.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = run / 'KNOWN_UNSENT_BEFORE_HTTP_CLASSIFICATION.json'
assert not out.exists(), 'Existing classification preserved.'
assert a['curl_exit_code'] == 7 and str(a['http_status']) == '000'
assert 'over proxy 127.0.0.1 after 0 ms: Could not connect to server' in a['error']
assert (run / 'response_headers.txt').stat().st_size == 0
for name in ('api_response.raw.json', 'character_api_original.png', 'result.json'):
    assert not (run / name).exists(), 'Recover existing response instead of claiming unsent.'
audit = run / 'TRANSPORT_SUBMISSION_EVIDENCE_AUDIT_v01.json'
assert sha(audit) == '9b9b8c5dcb5feb0fa3d7883991346439286728a1fc505485d9159e0b94f9621c'
v = {'id': 'ART-G12-58', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
     'classification': 'known_unsent_before_http',
     'original_attempt_record_preserved': str(attempt_path),
     'original_attempt_record_sha256': sha(attempt_path),
     'existing_readonly_recovery_audit': {'path': str(audit), 'sha256': sha(audit)},
     'facts': {'curl_exit_code': 7, 'http_status': '000', 'http_response_headers_bytes': 0,
               'response_file_exists': False, 'server_image_exists': False,
               'server_result_record_exists': False, 'reported_error': a['error']},
     'inference': 'curl reports failure to establish the local proxy connection at0ms. HTTP upload to the official API requires that connection, so this observed local transport invocation is excluded from submitted HTTP requests. No API authentication/quota response occurred. Wrapper api_calls1 was persisted before process start and is not remote submission proof.',
     'not_claimed': 'No TCP trace or uploaded byte measurement was collected; billing is not reported or inferred.',
     'separate_controlled_escalated_result': str(run.parent / 'first_api_source1071_samepayload_escalated_transport_v02/result.json'),
     'automatic_retry_performed': False, 'original_attempt_modified': False}
out.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'path': str(out), 'sha256': sha(out), 'new_network_calls': 0}, ensure_ascii=False))
