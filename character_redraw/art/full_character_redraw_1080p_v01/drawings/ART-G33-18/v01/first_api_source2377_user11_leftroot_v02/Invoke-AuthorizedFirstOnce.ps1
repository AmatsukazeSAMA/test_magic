#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b535504e29b10b7cd638314532eb3045c1cd5cfe5f60142e4ff373b8b7305ec5'){throw 'Immutable 18 lock changed.'}
$lock=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($lock.formal,$lock.draft,$lock.prompt,$lock.release,$lock.project_release,$lock.auth,$lock.provider)+@($lock.refs)+@($lock.preserved_originals)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Released 18 bytes changed.'}}
$formal=Get-Content -LiteralPath $lock.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.InputImages.Count -ne 6 -or $formal.Size -ne '608x1136' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact8field 18 request.'}
for($i=0;$i -lt 6;$i++){if($formal.InputImages[$i] -ne $lock.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $lock.prefix_text){throw 'Released LEFT prefix changed.'}
if(@(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'attempt.json').Count -gt 0 -or @(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'character_api_original.png').Count -gt 0){throw 'Existing18 attempt/raw; no duplicate or unknown retry.'}
$reg=Get-Content -LiteralPath 'D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/ASSET_REGISTRY.json' -Raw|ConvertFrom-Json
if($null -ne $reg.($lock.id)){throw '18 already centrally registered; stop duplicate.'}
$provider=$lock.provider.path
if($Preview){& $provider @formal -Preview;return}
$rp=Join-Path $PSScriptRoot 'ARTIST_API_EXECUTION_RECEIPT.json'
if(Test-Path -LiteralPath $rp){throw '18 invocation already recorded; no second call.'}
$start=[DateTime]::UtcNow
$receipt=@{id=$lock.id;status='authorized_FIRST_API_started';started_utc=$start.ToString('o');formal_sha256=$lock.formal.sha256;root_release_sha256=$lock.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @formal;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
