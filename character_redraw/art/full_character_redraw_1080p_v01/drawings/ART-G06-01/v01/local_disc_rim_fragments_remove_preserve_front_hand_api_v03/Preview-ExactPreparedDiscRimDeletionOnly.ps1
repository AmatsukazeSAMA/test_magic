#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='42f6a573e12900d14d6f1211fd65697afb9b9b02d5e221d40714d155169769a8'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw -Encoding UTF8|ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.provenance,$l.scope,$l.auth,$l.provider,$l.config,$l.review,$l.observations,$l.local_status,$l.future_whole)+@($l.refs)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared evidence changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne 1 -or $q.InputImages[0] -ne $l.refs[0].path -or $q.MaskFile -ne $l.mask.path -or $q.Size -ne '984x1600' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Exact request mismatch.'}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$d=Get-Content -LiteralPath 'D:\CODEX\魔术之心\image_defaults.json' -Raw -Encoding UTF8|ConvertFrom-Json
if(-not $d.generation_prompt_prefix.enabled -or $d.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'LEFT prefix changed.'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Preserve dispatch/result: '+$n)}}
# No Execute branch. Local parameter Preview only; helper returns before key/HTTP.
$v=& $l.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.input_count -ne 1 -or -not $v.mask_provided -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected Preview.'}
$p=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $p){throw 'Preserve prior proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$v;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;execution_released=$false;key_accessed=$false;network_requests=0;API_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($p,($proof|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$v
