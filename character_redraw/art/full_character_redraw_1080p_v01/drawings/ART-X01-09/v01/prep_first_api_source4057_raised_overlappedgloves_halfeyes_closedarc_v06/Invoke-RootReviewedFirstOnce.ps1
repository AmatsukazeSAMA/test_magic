#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'eae831a95741ae87ee431672ade9d5ab58faf992e64ce1b7acaa4d229c76bedb'){throw 'Immutable call lock changed'}
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
