#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$expectedLockSHA='6e962f5f99852aa64c0c764cb54f88ebcec9c41e6d2b652db24bdac439e9645b'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedLockSHA){throw 'Immutable lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
foreach($entry in @($locked.formal,$locked.prompt,$locked.mask,$locked.mask_provenance,$locked.provenance,$locked.review,$locked.actual_view_list,$locked.history,$locked.scope,$locked.auth,$locked.provider,$locked.provider_configuration,$locked.Sol170,$locked.local_repair_status,$locked.future_whole_draft)+@($locked.refs)){
 if((Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256){throw ('Prepared input changed: '+$entry.path)}
}
$request=Get-Content -LiteralPath $locked.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($request.Count -ne 8 -or $request.InputImages.Count -ne 2 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '1120x1392' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact request.'}
for($i=0;$i -lt 2;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $locked.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $locked.prefix_text){throw 'LEFT prefix changed.'}
if(-not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Prompt prefix mismatch.'}
foreach($n in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Existing attempt/result must recover: '+$n)}}
# Preview-only: no Execute branch, no key decryption, no HTTP or generation.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.n -ne 1 -or -not $preview.mask_provided -or $preview.input_count -ne 2 -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected preview boundary.'}
$p=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $p){throw 'Preserve existing preview.'}
$r=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;request_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;lock_sha256=$expectedLockSHA;execution_released=$false;no_key_or_network_in_preview=$true;api_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($p,($r|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
