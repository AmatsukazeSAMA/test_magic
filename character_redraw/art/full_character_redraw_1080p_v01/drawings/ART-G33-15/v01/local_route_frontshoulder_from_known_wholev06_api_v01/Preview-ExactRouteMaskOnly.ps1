#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'aaa86ff71acfa4e7abdc24a35cb3be45072dbbcc20b4eab9d5cbe78abf71b583'){throw 'Immutable lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
$entries=@($locked.formal,$locked.request,$locked.prompt,$locked.mask,$locked.mask_provenance,$locked.provenance,$locked.artist_review,$locked.actual_view_list,$locked.history,$locked.user_rejection,$locked.scope,$locked.auth,$locked.front_policy,$locked.provider,$locked.provider_configuration,$locked.local_status,$locked.future_whole)+@($locked.refs)
if($locked.fresh174){$entries+=@($locked.fresh174)}
foreach($item in $entries){if((Get-FileHash -LiteralPath $item.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256){throw ('Changed prepared input: '+$item.path)}}
$request=Get-Content -LiteralPath $locked.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($request.Count -ne 8 -or $request.InputImages.Count -ne 3 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '960x1648' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Exact request parameters changed.'}
for($i=0;$i -lt 3;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $locked.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured provider model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $locked.prefix_text -or -not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix changed.'}
foreach($name in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw ('Existing attempt/result: recover, do not resubmit: '+$name)}}
# Preview ONLY: provider returns before key loading/output attempt/network.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.n -ne 1 -or -not $preview.mask_provided -or $preview.input_count -ne 3 -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Preview boundary changed.'}
$path=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $path){throw 'Preserve existing preview.'}
$data=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;exactlocksha='aaa86ff71acfa4e7abdc24a35cb3be45072dbbcc20b4eab9d5cbe78abf71b583';request_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;execution_released=$false;root_release_received=$false;transparent_background=$true;api_calls=0;native_calls=0;HTTP_calls=0;automatic_retries=0;no_key_decryption_or_network=$true;technical_preview_not_art_acceptance=$true}
[IO.File]::WriteAllText($path,($data|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
