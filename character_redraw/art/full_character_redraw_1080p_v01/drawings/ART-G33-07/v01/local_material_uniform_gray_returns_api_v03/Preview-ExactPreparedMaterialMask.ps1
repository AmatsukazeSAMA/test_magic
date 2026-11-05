#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expectedLockSHA='5ac9e23a2297b9bf79f52a6873c50468392295a15e3a804faca79282dda0faa8'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedLockSHA){throw 'Immutable prepared lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
foreach($entry in @($locked.formal,$locked.prompt,$locked.mask,$locked.mask_provenance,$locked.provenance,$locked.review,$locked.actual_view_list,$locked.history,$locked.scope,$locked.auth,$locked.provider,$locked.provider_configuration,$locked.Sol162,$locked.local_repair_status)+@($locked.refs)){
 if((Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256){throw ('Prepared input/evidence changed: '+$entry.path)}
}
$request=Get-Content -LiteralPath $locked.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($request.Count -ne 8 -or $request.InputImages.Count -ne 2 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '960x1648' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact two-ref eight-field masked request.'}
for($i=0;$i -lt 2;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $locked.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $locked.prefix_text){throw 'Current mandatory LEFT prefix changed.'}
if(-not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Prompt prefix mismatch.'}
foreach($n in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Existing attempt/result must recover, not resubmit: '+$n)}
}
# PREVIEW ONLY. No Execute branch, credential access, HTTP, or generation.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.n -ne 1 -or -not $preview.mask_provided -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected preview boundary.'}
$previewPath=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $previewPath){throw 'Existing preview preserved; inspect instead of overwrite.'}
$record=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;request_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;lock_sha256=$expectedLockSHA;execution_released=$false;no_key_or_network_in_preview=$true;api_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($previewPath,($record|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
