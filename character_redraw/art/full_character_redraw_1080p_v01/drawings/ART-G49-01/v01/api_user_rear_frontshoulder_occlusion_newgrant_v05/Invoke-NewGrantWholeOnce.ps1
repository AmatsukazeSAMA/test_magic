#Requires -Version 7.0
$ErrorActionPreference='Stop'
$recordPath=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $recordPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'd155edcfbecc0ff6478738d035b22232dc88ac78b568702f8643865c85213593'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $recordPath -Raw|ConvertFrom-Json -AsHashtable
if($d.id -ne 'ART-G49-01' -or $d.first_drawing -or -not $d.new_live_single_grant -or $d.planned_logical_requests -ne 1){throw 'Wrong new single-grant scope'}
$q=$d.parameters
if($q.Count -ne 8 -or $q.Size -ne '1024x1072' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong parameters'}
foreach($x in @($d.provider,$d.source,$d.same_project_official_upload_confirmation,$d.requirements)+@($d.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}
}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
# Older G49-01 grant is consumed and remains untouched. This is the NEW live once-grant, not a restart.
foreach($name in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','NEW_GRANT_DISPATCH_ONCE.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'Existing NEW run attempt/return/claim: recover only'}
}
if(Get-ChildItem -LiteralPath $PSScriptRoot -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing new-run UNKNOWN: no restart'}
$preview=& $d.provider.path @q -Preview
if($preview.submitted -or $preview.n -ne 1 -or $preview.retry -ne 1 -or $preview.input_count -ne 3 -or $preview.model -ne 'gpt-image-2.5-sunburst' -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($preview|ConvertTo-Json -Depth 8),$utf8)
$lockPath=Join-Path $PSScriptRoot 'NEW_GRANT_DISPATCH_ONCE.json'
$lockStream=[IO.File]::Open($lockPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G49-01 NEW live single grant ONE logical whole edit only; old grant not reused');$lockStream.Write($bytes,0,$bytes.Length)}finally{$lockStream.Dispose()}
$started=[DateTime]::UtcNow
$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G49-01';status='official_NEW_GRANT_whole_started';operation_kind='whole_character_redraw';new_live_single_grant=$true;logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');old_consumed_grant_reused=$false;direct_request_sha256='d155edcfbecc0ff6478738d035b22232dc88ac78b568702f8643865c85213593'}
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 10),$utf8)}
Save-Receipt
try{
 & $d.provider.path @q
 $receipt.status='known_saved_return'
 $result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json
 $receipt.image_sha256=$result.output_sha256;$receipt.actual_retries=$result.automatic_retries;$receipt.provider_elapsed_seconds=$result.elapsed_seconds
}catch{
 $receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw
}finally{
 $receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt
}
