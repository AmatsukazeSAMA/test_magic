#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b0a844070172073305b811444c41256078c34b0e938ab2eb662124aeb05b2827'){throw 'Immutable lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
$entries=@($locked.formal,$locked.request,$locked.prompt,$locked.mask,$locked.mask_provenance,$locked.provenance,$locked.artist_actual_view,$locked.history,$locked.scope,$locked.auth,$locked.provider,$locked.provider_configuration,$locked.local_status,$locked.future_whole,$locked.future_prompt,$locked.fresh179)+@($locked.refs)
foreach($item in $entries){if((Get-FileHash -LiteralPath $item.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256){throw ('Prepared item changed: '+$item.path)}}
$request=Get-Content -LiteralPath $locked.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($request.Count -ne 8 -or $request.InputImages.Count -ne 4 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '960x1648' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Exact8-field parameters changed.'}
for($i=0;$i -lt 4;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $locked.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured provider model changed.'}
$defs=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defs.generation_prompt_prefix.enabled -or $defs.generation_prompt_prefix.text -ne $locked.prefix_text -or -not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix changed.'}
foreach($name in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png','api_response.raw.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw ('Existing execution artifact; recover, never resubmit: '+$name)}}
# PREVIEW ONLY. Wrapper returns before key decryption, attempt creation and HTTP.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.n -ne 1 -or -not $preview.mask_provided -or $preview.input_count -ne 4 -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Preview boundary changed.'}
$output=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $output){throw 'Existing Preview evidence preserved.'}
$proof=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;exact_lock_sha256='b0a844070172073305b811444c41256078c34b0e938ab2eb662124aeb05b2827';formal_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;execution_released=$false;root_release_received=$false;api_calls=0;native_calls=0;HTTP_calls=0;automatic_retries=0;no_key_decryption_or_network=$true;technical_preview_not_art_acceptance=$true}
[IO.File]::WriteAllText($output,($proof|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
