#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '0feb6c52cc9d116e21bb1d4e1ef2d7d9010f6a7913a1dcb69365b21ca9146465'){throw 'Immutable lock changed.'}
$l=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
$items=@($l.formal,$l.request,$l.prompt,$l.mask,$l.mask_provenance,$l.provenance,$l.artist_actual_review,$l.history,$l.scope,$l.auth,$l.provider,$l.provider_configuration,$l.local_status,$l.future_whole,$l.future_prompt,$l.fresh185)+@($l.refs)+@($l.future_crops)
foreach($i in $items){if((Get-FileHash -LiteralPath $i.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $i.sha256){throw ('Prepared file changed: '+$i.path)}}
$r=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($r.Count -ne 8 -or $r.InputImages.Count -ne 4 -or $r.Size -ne '1104x1424' -or $r.Quality -ne 'high' -or $r.Background -ne 'transparent' -or $r.MaskFile -ne $l.mask.path -or $r.OutputDirectory -ne $PSScriptRoot){throw 'Exact8-field request changed.'}
for($i=0;$i -lt 4;$i++){if($r.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $l.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text -or -not ([IO.File]::ReadAllText($r.PromptFile)).StartsWith($l.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix changed.'}
foreach($n in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png','api_response.raw.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw ('Existing execution artifact; recover not retry: '+$n)}}
# Preview only; no key decryption, no attempt or HTTP.
$p=& $l.provider.path @r -Preview
if($p.submitted -or $p.n -ne 1 -or -not $p.mask_provided -or $p.input_count -ne 4 -or $p.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Preview boundary changed.'}
$output=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json';if(Test-Path -LiteralPath $output){throw 'Preserve existing preview.'}
$v=@{id=$l.id;PREPONLY=$true;actual_preview=$p;lock_sha256='0feb6c52cc9d116e21bb1d4e1ef2d7d9010f6a7913a1dcb69365b21ca9146465';formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;root_release_received=$false;API_calls=0;native_calls=0;HTTP_calls=0;automatic_retries=0;technical_preview_not_art_pass=$true}
[IO.File]::WriteAllText($output,($v|ConvertTo-Json -Depth 14),[Text.UTF8Encoding]::new($false));$p
