#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$runDirectory=$PSScriptRoot
$lockPath=Join-Path $runDirectory 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'aa2f76f1c0f9926115b19624aba72fbd9521771ec29a6ccb4d9fc80179ff43fc'){throw 'Immutable call lock changed.'}
$lock=Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
foreach($r in @($lock.formal_request,$lock.draft,$lock.prompt,$lock.root_release,$lock.project_release,$lock.project_authorization,$lock.provider_script)+@($lock.references)+@($lock.preserved_originals)){
 if((Get-FileHash -LiteralPath $r.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Released input/evidence bytes changed.'}
}
$formal=Get-Content -LiteralPath $lock.formal_request.path -Raw | ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.Size -ne '560x1216' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.InputImages.Count -ne 6 -or $formal.OutputDirectory -ne $runDirectory){throw 'Unexpected exact8field request.'}
for($i=0;$i -lt 6;$i++){if($formal.InputImages[$i] -ne $lock.references[$i].path){throw 'Reference order changed.'}}
$config=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
if(@(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'attempt.json').Count -gt 0){throw 'Existing attempt under cel; no retry.'}
if(@(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'character_api_original.png').Count -gt 0){throw 'Existing cel raw; no duplicate first API.'}
$registry=Get-Content -LiteralPath 'D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/ASSET_REGISTRY.json' -Raw | ConvertFrom-Json
if($null -ne $registry.($lock.id)){throw 'Cel already centrally registered; stop duplicate.'}
$provider=$lock.provider_script.path
if($Preview){& $provider @formal -Preview;return}
$receiptPath=Join-Path $runDirectory 'ARTIST_API_EXECUTION_RECEIPT.json'
if(Test-Path -LiteralPath $receiptPath){throw 'Invocation already recorded; no second call.'}
$started=[DateTime]::UtcNow
$receipt=@{id=$lock.id;status='authorized_invocation_started';started_utc=$started.ToString('o');formal_request_sha256=$lock.formal_request.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;root_release_sha256=$lock.root_release.sha256;project_authorization_sha256=$lock.project_authorization.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt | ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @formal;$receipt.status='provider_script_returned';$receipt.provider_result=Get-Content -LiteralPath (Join-Path $runDirectory 'result.json') -Raw | ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
