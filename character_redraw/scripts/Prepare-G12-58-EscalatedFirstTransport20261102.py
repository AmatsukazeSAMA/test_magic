"""Preserve the sandbox proxy failure and prepare the same payload with network approval."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
old = base / 'drawings/ART-G12-58/v01/first_api_source1071_rebound_originalmouth_user11_v01'
run = base / 'drawings/ART-G12-58/v01/first_api_source1071_samepayload_escalated_transport_v02'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
if (run / 'API_PREPARED_REQUEST.json').exists():
    raise SystemExit('Existing transport request preserved; no repeat.')
assert sha(old / 'API_PREPARED_REQUEST.json') == '0db988c81284a973af36993d826fbcf38fb27f372f8b554e04d4cc0c41d2a90e'
attempt = read(old / 'attempt.json')
assert attempt['curl_exit_code'] == 7 and attempt['http_status'] == '000'
assert 'over proxy 127.0.0.1 after 0 ms: Could not connect to server' in attempt['error']
for name in ['result.json', 'character_api_original.png', 'api_response.json']:
    assert not (old / name).exists(), 'Recover a saved remote result, never repeat it.'
audit = old / 'TRANSPORT_SUBMISSION_EVIDENCE_AUDIT_v01.json'
assert sha(audit) == '9b9b8c5dcb5feb0fa3d7883991346439286728a1fc505485d9159e0b94f9621c'
run.mkdir(exist_ok=True)
q = read(old / 'API_PREPARED_REQUEST.json')
q['OutputDirectory'] = str(run)
q['Stage'] = 'ART-G12-58 source1071 FIRST remote transport under escalation after saved local sandbox proxy connect failure; same six images/prompt/parameters'
assert len(q) == 8 and len(q['InputImages']) == 6
formal = run / 'API_PREPARED_REQUEST.json'
save(formal, q)
auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
evidence = lambda p: {'path': str(p), 'sha256': sha(p)}
release = run / 'ROOT_TRANSPORT_CLASSIFICATION_AND_RELEASE.json'
save(release, {'id': 'ART-G12-58', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'previous_attempt_preserved': evidence(old / 'attempt.json'), 'readonly_recovery_audit': evidence(audit),
    'previous_execution_permissions': 'use_default; no network escalation was requested',
    'failure_classification': 'Local execution-environment proxy TCP connection failure, curl7 at0ms before any API response, not an API authentication/quota/model response. Wrapper api_calls1 was written before process start and does not prove remote submission.',
    'root_recovery_checks': 'No response body, remote receipt, result or raw exists; headers empty/http000; error specifically local proxy connection could not be established. No unknown returned remote artwork is being discarded.',
    'not_claimed': 'No upload/TCP trace was collected; do not invent a measured byte count or verified billing charge.',
    'manual_next_action': 'One reviewed same-payload request with sandbox_permissions=require_escalated under the existing actual explicit future-project API consent, following API transport troubleshooting; no automatic retry or alternate provider/channel.',
    'authority': evidence(auth), 'actual_user_answer': read(auth)['user_reply_verbatim'],
    'actual_user_question': read(auth)['question_text'],
    'exact_six_images_actually_viewed_by_root': [evidence(Path(p)) for p in q['InputImages']],
    'root_payload_observation': 'Only original1071 complete anime action guide, R191v02 gray-hair-only crop, user-approved complete11 gray head/curl context, user gray-return detail crop, own source1071 eyes/open-smile crop and unlit pigment key. Same project drawing material and same official destination; no unrelated data.',
    'n': 1, 'quality': 'high', 'size': '816x1072', 'background': 'transparent',
    'endpoint': 'https://api.openai.com/v1/images/edits', 'automatic_retry': 0,
    'fresh_root_Sol_required': True, 'art_accepted': False})
lock = {'id': 'ART-G12-58', 'formal': evidence(formal), 'prompt': evidence(Path(q['PromptFile'])),
        'release': evidence(release), 'auth': evidence(auth),
        'provider': evidence(root / 'scripts/Invoke-ReferenceImage.ps1'),
        'refs': [evidence(Path(p)) for p in q['InputImages']]}
lock_path = run / 'AUTHORIZED_CALL_LOCK.json'
save(lock_path, lock)
script = r'''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCK_SHA__'){throw 'Immutable request lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.release,$l.auth,$l.provider)+@($l.refs)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Exact authorized inputs changed'}}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 6 -or $f.Size -ne '816x1072' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected request'}
for($i=0;$i -lt 6;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed'}}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt; recovery only'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Model changed'}
$start=[DateTime]::UtcNow;$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json'
$r=@{id=$l.id;status='one_escalated_transport_started';started_utc=$start.ToString('o');n=1;automatic_retry=0;endpoint='https://api.openai.com/v1/images/edits';formal_sha256=$l.formal.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($r|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$r.status='provider_script_returned';$r.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$r.status='failed_or_unknown_no_retry';$r.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$r.finished_utc=[DateTime]::UtcNow.ToString('o');$r.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
'''
(run / 'Invoke-AuthorizedFirstEscalatedTransportOnce.ps1').write_text(script.replace('__LOCK_SHA__', sha(lock_path)), encoding='utf-8')
print(json.dumps({'formal': evidence(formal), 'lock': evidence(lock_path), 'release': evidence(release),
                  'calls': 0}, ensure_ascii=False))
