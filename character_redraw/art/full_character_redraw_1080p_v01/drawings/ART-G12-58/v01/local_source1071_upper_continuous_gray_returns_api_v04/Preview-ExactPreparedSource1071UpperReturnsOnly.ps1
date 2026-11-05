#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='fe534ef50fcec97afcdaf3f5d407c3319ab504bad399ae72a4b72366c38f779e'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.provenance,$l.scope,$l.auth,$l.provider,$l.config,$l.observations,$l.local_status,$l.future_whole)+@($l.refs)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared evidence changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
$fields=@('InputImages','PromptFile','MaskFile','OutputDirectory','OutputFileName','Size','Quality','Background')
if($q.Count -ne 8 -or @($q.Keys | Where-Object {$_ -notin $fields}).Count -ne 0 -or $q.InputImages.Count -ne 4 -or $q.MaskFile -ne $l.mask.path -or $q.PromptFile -ne $l.prompt.path -or $q.Size -ne '1104x1440' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot -or $q.OutputFileName -ne 'character_api_original.png'){throw 'Exact eight-field request mismatch.'}
for($i=0;$i -lt 4;$i++){if($q.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8 | ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$d=Get-Content -LiteralPath 'D:\CODEX\魔术之心\image_defaults.json' -Raw -Encoding UTF8 | ConvertFrom-Json
if(-not $d.generation_prompt_prefix.enabled -or $d.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory fullLEFT prefix changed.'}
if(-not $l.PREPONLY -or $l.execution_released -or -not $l.wait_for_fresh55_pass -or $l.API_calls_authorized_by_this_lock -ne 0){throw 'PREPONLY boundary changed.'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Preserve dispatch/result: '+$n)}
}
# Only local Preview: provider returns before key access, HTTP, attempts or output writes. No Execute branch.
$v=& $l.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.input_count -ne 4 -or -not $v.mask_provided -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits' -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.quality -ne 'high' -or $v.size -ne '1104x1440' -or $v.background -ne 'transparent'){throw 'Unexpected Preview.'}
$p=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $p){throw 'Preserve prior Preview proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$v;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;wait_for_fresh55_pass=$true;execution_released=$false;key_accessed=$false;network_requests=0;API_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($p,($proof | ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$v
