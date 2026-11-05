#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lockFile=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lockFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne '3317946e4530497e649a4f9158c8375c7f9f2c4c23331af850d74cea56a202c2'){throw 'Immutable repair lock changed.'}
$lock=Get-Content -LiteralPath $lockFile -Raw | ConvertFrom-Json
foreach($r in @($lock.formal,$lock.request,$lock.prompt,$lock.release,$lock.project_authorization,$lock.provider,$lock.parent_attempt)+@($lock.references)+@($lock.preserved_originals)){
 if((Get-FileHash -LiteralPath $r.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Repair input/evidence changed.'}
}
$previous=Get-Content -LiteralPath $lock.parent_attempt_path -Raw | ConvertFrom-Json
if($previous.status -ne 'completed' -or $previous.http_status -ne '200'){throw 'Parent result not known completed.'}
$formal=Get-Content -LiteralPath $lock.formal.path -Raw | ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.InputImages.Count -ne 5 -or $formal.Size -ne '560x1216' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected whole-repair exact request.'}
for($i=0;$i -lt 5;$i++){if($formal.InputImages[$i] -ne $lock.references[$i].path){throw 'Reference order changed.'}}
$config=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$provider=$lock.provider.path
if($Preview){& $provider @formal -Preview;return}
foreach($name in @('attempt.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'This repair already attempted; no retry.'}}
$receiptPath=Join-Path $PSScriptRoot 'ARTIST_API_EXECUTION_RECEIPT.json'
$start=[DateTime]::UtcNow
$receipt=@{id='ART-G33-17';status='authorized_known_parent_whole_repair_invocation_started';started_utc=$start.ToString('o');operation_kind='whole_character_redraw';formal_sha256=$lock.formal.sha256;release_sha256=$lock.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;local_mask_used=$false;parts_spliced=$false}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @formal;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
