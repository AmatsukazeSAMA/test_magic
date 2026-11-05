#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6f513b498e0a1434e2a2de6c777fce63d7fd418ecfd512fc41d39cd963761844'){throw 'Prepared immutable lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
foreach($entry in @($locked.formal,$locked.prompt,$locked.mask,$locked.provenance,$locked.mask_provenance,$locked.history,$locked.Sol160,$locked.scope,$locked.auth,$locked.provider,$locked.provider_configuration,$locked.local_repair_status,$locked.mask_review)+@($locked.refs)){
 if((Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256){throw ('Prepared payload changed: '+$entry.path)}
}
$request=Get-Content -LiteralPath $locked.formal.path -Raw | ConvertFrom-Json -AsHashtable
if($request.Count -ne 9 -or $request.InputImages.Count -ne 4 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '1584x992' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected base8 plus mask exact request.'}
for($i=0;$i -lt 4;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$config=Get-Content -LiteralPath $locked.provider_configuration.path -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw | ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $locked.prefix_text){throw 'Mandatory LEFT prefix changed.'}
if(-not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Prompt lacks exact current prefix.'}
foreach($name in @('attempt.json','result.json','prompt_effective.txt','request_manifest.json','character_api_original.png')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw ('Existing request/result must be recovered, not sent: '+$name)}
}
# Deliberately preview only. This file has no network/Execute branch and creates no attempt.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits' -or -not $preview.mask_provided -or $preview.n -ne 1){throw 'Preview did not match prepared boundary.'}
$previewPath=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $previewPath){throw 'Existing preview preserved; inspect rather than overwrite.'}
$record=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;request_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;lock_sha256='6f513b498e0a1434e2a2de6c777fce63d7fd418ecfd512fc41d39cd963761844';no_credential_read_or_network_in_preview=$true;execution_released=$false;api_calls=0;native_calls=0;automatic_retries=0;technical_preview_not_artistic_pass=$true}
[IO.File]::WriteAllText($previewPath,($record|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
