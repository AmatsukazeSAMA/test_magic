#Requires -Version 7.0
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'd66e87bd7d806992b1bf6d7f2c3456f97c5ddf4f42e76a8b9d47f529d1a15680'){throw 'Immutable call lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prep_lock,$l.prompt,$l.release,$l.auth,$l.provider,$l.preview,$l.JOB,$l.REGISTRATION_PLAN)+@($l.refs)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Exact authorized payload changed'}
}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 6 -or $f.Size -ne $l.size -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected prepared parameters'}
for($i=0;$i -lt 6;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Input order changed'}}
$defaults=Get-Content -LiteralPath $l.project_defaults_path -Raw|ConvertFrom-Json
if([string]$defaults.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'LEFT prefix changed'}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed'}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt: recover only'}}
$start=[DateTime]::UtcNow;$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json'
$r=@{id=$l.id;status='one_root_reviewed_first_started';started_utc=$start.ToString('o');n=1;automatic_retry=0;endpoint='https://api.openai.com/v1/images/edits';formal_sha256=$l.formal.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($r|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$r.status='provider_script_returned';$r.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$r.status='failed_or_unknown_no_retry';$r.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$r.finished_utc=[DateTime]::UtcNow.ToString('o');$r.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
