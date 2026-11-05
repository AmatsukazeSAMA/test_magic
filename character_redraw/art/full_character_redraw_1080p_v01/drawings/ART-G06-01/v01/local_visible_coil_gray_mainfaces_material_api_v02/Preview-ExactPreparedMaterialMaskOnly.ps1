#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expected='a51158ec5bf2b4120b41d9d78895b75c48c6f4773de8a4dad7d829f9bb53e9a5'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'Prepared lock changed.'}
$l=Get-Content -LiteralPath $lockPath -Raw -Encoding UTF8|ConvertFrom-Json
foreach($e in @($l.formal,$l.prompt,$l.mask,$l.mask_provenance,$l.provenance,$l.observations,$l.scope,$l.auth,$l.provider,$l.config,$l.local_status,$l.future_whole_template)+@($l.refs)){
 if((Get-FileHash -LiteralPath $e.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $e.sha256){throw ('Prepared input changed: '+$e.path)}
}
$q=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne 2 -or $q.Size -ne '640x1040' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.MaskFile -ne $l.mask.path -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact eight-field request.'}
for($i=0;$i -lt 2;$i++){if($q.InputImages[$i] -ne $l.refs[$i].path){throw 'First target/reference order changed.'}}
$cfg=Get-Content -LiteralPath $l.config.path -Raw -Encoding UTF8|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:\CODEX\魔术之心\image_defaults.json' -Raw -Encoding UTF8|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($q.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix mismatch.'}
foreach($n in @('attempt.json','character_api_original.png','result.json','request_manifest.json','prompt_effective.txt','ROOT_MASKED_CALL_LOCK.json','ROOT_ACTUAL_MASKED_REPAIR_RELEASE.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Existing dispatch/release preserved: '+$n)}}
# ONLY Preview. No Execute branch, key access or network.
$actual=& $l.provider.path @q -Preview
if($actual.submitted -or $actual.n -ne 1 -or $actual.input_count -ne 2 -or -not $actual.mask_provided -or $actual.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected preview response.'}
$out=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $out){throw 'Preserve previous preview proof.'}
$proof=@{id=$l.id;PREPONLY=$true;actual_preview=$actual;formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;lock_sha256=$expected;api_calls=0;native_calls=0;network_requests=0;automatic_retries=0;execution_released=$false;key_accessed=$false;preview_is_not_artistic_pass=$true}
[IO.File]::WriteAllText($out,($proof|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$actual
