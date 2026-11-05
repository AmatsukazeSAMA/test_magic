"""Lock one prepared FIRST request after the root has actually viewed every input.

Preparation only. The generated PowerShell runner separately requires network
approval, refuses existing runs, and locks the user's per-request retry budget.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p = argparse.ArgumentParser(__doc__)
p.add_argument('run', type=Path)
p.add_argument('--observation', required=True)
a = p.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
run = a.run.resolve()
run.relative_to(base)
read = lambda f: json.loads(f.read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
evidence = lambda f: {'path': str(f), 'sha256': sha(f)}
def save(f, value):
    if f.exists():
        raise SystemExit(f'Existing evidence preserved: {f}')
    f.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

formal = run / 'API_PREPARED_REQUEST.json'
prep_path = run / 'REQUEST_LOCK.json'
prep = read(prep_path)
q = read(formal)
defaults_path = root / 'image_defaults.json'
defaults = read(defaults_path)
retry = defaults.get('api_request_policy', {}).get('retry', 0)
assert retry in (0, 1)
operation = prep.get('operation_kind', 'first_drawing')
assert operation in ('first_drawing', 'whole_character_redraw')
extra = None
claim_path = None
if operation == 'whole_character_redraw':
    extra = prep['extra_authorization']
    extra_path = Path(extra['path']).resolve()
    extra_path.relative_to(base)
    assert sha(extra_path) == extra['sha256']
    grant = read(extra_path)
    assert grant['id'] == prep['id'] and grant['operation_kind'] == operation
    assert grant['maximum_new_logical_requests'] == 1 and grant['quality'] == 'high'
    assert grant['n'] == 1 and grant['retry'] == retry
    claim_path = extra_path.with_suffix('.consumed.json')
    assert not claim_path.exists(), 'This extra operation has already been claimed.'
assert set(q) == {'PromptFile', 'InputImages', 'OutputDirectory', 'Size', 'Quality', 'Background', 'OutputFileName', 'Stage'}
assert q['Quality'] == 'high' and q['Background'] == 'transparent' and 1 <= len(q['InputImages']) <= 6
assert len(q['Size'].split('x')) == 2 and all(int(v) > 0 and int(v) % 16 == 0 for v in q['Size'].split('x')), 'API output dimensions must be positive multiples of 16.'
assert Path(q['OutputDirectory']).resolve() == run and q['OutputFileName'] == 'character_api_original.png'
for name in ('attempt.json', 'character_api_original.png', 'ROOT_API_EXECUTION_RECEIPT.json'):
    assert not (run / name).exists(), 'Existing attempt: recover, never submit again.'
for item in [prep['prepared_request'], prep['draft'], prep['prompt'], prep['wrapper'], prep['authorization'], prep['JOB'], prep['REGISTRATION_PLAN'], *prep['references']]:
    assert sha(Path(item['path'])) == item['sha256'], f'Prepared input changed: {item["path"]}'
assert [str(Path(x).resolve()) for x in q['InputImages']] == [str(Path(x['path']).resolve()) for x in prep['references']]
auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
consent = read(auth)
preview = run / 'API_PREVIEW_PROOF_PREPONLY.json'
v = read(preview)
assert v['submitted'] is False and v['n'] == 1 and v['quality'] == 'high'
assert prep.get('retry', 0) == retry and v.get('retry', 0) == retry
assert prep['mandatory_prefix'] == defaults['generation_prompt_prefix']['text']
assert Path(q['PromptFile']).read_text(encoding='utf-8-sig').startswith(prep['mandatory_prefix'])
assert v['size'] == q['Size'] and v['background'] == 'transparent' and v['input_count'] == len(q['InputImages'])
assert v['endpoint'] == 'https://api.openai.com/v1/images/edits' and v['model'] == 'gpt-image-2.5-sunburst'
release = run / 'ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json'
save(release, {'id': prep['id'], 'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'actual_root_viewed_all_images': [evidence(Path(x)) for x in q['InputImages']],
    'reference_count': len(q['InputImages']),
    'prompt_actually_read': evidence(Path(q['PromptFile'])),
    'root_observation': a.observation, 'authorization': evidence(auth),
    'actual_user_question': consent['question_text'], 'actual_user_answer': consent['user_reply_verbatim'],
    'scope': f'Only this GOAL project anime character/reference drawings, same official endpoint, high n1 transparent, retry={retry}. No unrelated data.',
    'first_drawing': operation == 'first_drawing', 'operation_kind': operation,
    'extra_authorization': extra, 'maximum_new_logical_requests': 1,
    'maximum_automatic_retries': retry, 'network_calls_before_this_release': 0,
    'api_request_policy': defaults.get('api_request_policy'),
    'manual_execution_requires_escalated_network_permission': True,
    'fresh_root_and_Sol_actual_review_required': True, 'user_accepted': False, 'dynamic_validated': False})
lock = {'id': prep['id'], 'formal': evidence(formal), 'prep_lock': evidence(prep_path),
    'prompt': evidence(Path(q['PromptFile'])), 'release': evidence(release),
    'auth': evidence(auth), 'provider': evidence(root / 'scripts/Invoke-ReferenceImage.ps1'),
    'preview': evidence(preview), 'JOB': prep['JOB'], 'REGISTRATION_PLAN': prep['REGISTRATION_PLAN'],
    'refs': [evidence(Path(x)) for x in q['InputImages']], 'input_count': len(q['InputImages']), 'size': q['Size'],
    'mandatory_prefix': prep['mandatory_prefix'], 'retry': retry, 'project_defaults_path': str(defaults_path),
    'operation_kind': operation, 'extra_authorization': extra,
    'extra_operation_claim_path': str(claim_path) if claim_path else None}
lock_path = run / 'ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json'
save(lock_path, lock)
script = r'''#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCK_SHA__'){throw 'Immutable call lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prep_lock,$l.prompt,$l.release,$l.auth,$l.provider,$l.preview,$l.JOB,$l.REGISTRATION_PLAN)+@($l.refs)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Exact authorized payload changed'}
}
if($l.extra_authorization -and (Get-FileHash -LiteralPath $l.extra_authorization.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.extra_authorization.sha256){throw 'Extra-operation authorization changed'}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $l.input_count -lt 1 -or $l.input_count -gt 6 -or $f.InputImages.Count -ne $l.input_count -or $l.refs.Count -ne $l.input_count -or $f.Size -ne $l.size -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected prepared parameters'}
for($i=0;$i -lt $l.input_count;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Input order changed'}}
$defaults=Get-Content -LiteralPath $l.project_defaults_path -Raw|ConvertFrom-Json
if([string]$defaults.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'LEFT prefix changed'}
if([int]$defaults.api_request_policy.retry -ne [int]$l.retry){throw 'Authorized retry policy changed'}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed'}
if($Preview){& $l.provider.path @f -Preview;return}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt: recover only'}}
if($l.extra_operation_claim_path){
 $claim=@{id=$l.id;reserved_run=$PSScriptRoot;operation_kind=$l.operation_kind;maximum_new_logical_requests=1;claimed_utc=[DateTime]::UtcNow.ToString('o');authorization_sha256=$l.extra_authorization.sha256}
 $claimBytes=[Text.UTF8Encoding]::new($false).GetBytes(($claim|ConvertTo-Json -Depth 10))
 $claimStream=[IO.File]::Open($l.extra_operation_claim_path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
 try{$claimStream.Write($claimBytes,0,$claimBytes.Length)}finally{$claimStream.Dispose()}
}
$start=[DateTime]::UtcNow;$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json'
$r=@{id=$l.id;status='one_root_reviewed_operation_started';operation_kind=$l.operation_kind;extra_authorization=$l.extra_authorization;started_utc=$start.ToString('o');n=1;maximum_automatic_retries=$l.retry;endpoint='https://api.openai.com/v1/images/edits';formal_sha256=$l.formal.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($r|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$r.status='provider_script_returned';$r.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$r.status='failed_or_unknown_retry_budget_finished';$r.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$r.finished_utc=[DateTime]::UtcNow.ToString('o');$r.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
'''
runner = run / 'Invoke-RootReviewedFirstOnce.ps1'
if runner.exists():
    raise SystemExit('Existing runner preserved.')
runner.write_text(script.replace('__LOCK_SHA__', sha(lock_path)), encoding='utf-8')
print(json.dumps({'id': prep['id'], 'release': evidence(release), 'lock': evidence(lock_path), 'runner': evidence(runner), 'network_calls': 0}, ensure_ascii=False))
