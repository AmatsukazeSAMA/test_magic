#Requires -Version 7.0
$ErrorActionPreference='Stop'
$recordPath=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $recordPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '3a4c92aa95753f6c8809af069000ec9e88a5d3590425eee3df2d1a2e5a879bb4'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $recordPath -Raw|ConvertFrom-Json -AsHashtable
if($d.id -ne 'ART-G49-02' -or $d.planned_logical_requests -ne 1 -or $d.G49_01_extra_grant_used_for_this_request){throw 'Wrong FIRST scope'}
$q=$d.parameters
if($q.Count -ne 8 -or $q.Size -ne '1072x1072' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong parameters'}
foreach($x in @($d.provider,$d.source,$d.same_project_authorization)+@($d.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}
}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'e54dc9a364e1dfb5b7355c65b59a2bd6bf3b59346c3df215826443e753eb1a87'){throw 'Prompt changed'}
$asset=Split-Path -Parent $PSScriptRoot
foreach($name in @('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json')){
 if(Get-ChildItem -LiteralPath $asset -Recurse -File -Filter $name){throw 'Existing target attempt/return: recover only'}
}
if(Get-ChildItem -LiteralPath $asset -Recurse -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing target UNKNOWN: no restart'}
$preview=& $d.provider.path @q -Preview
if($preview.submitted -or $preview.n -ne 1 -or $preview.retry -ne 1 -or $preview.input_count -ne 4 -or $preview.model -ne 'gpt-image-2.5-sunburst'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($preview|ConvertTo-Json -Depth 8),$utf8)
$lockPath=Join-Path $PSScriptRoot 'FIRST_DISPATCH_ONCE.json'
$lockStream=[IO.File]::Open($lockPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G49-02 ONE logical FIRST only');$lockStream.Write($bytes,0,$bytes.Length)}finally{$lockStream.Dispose()}
$started=[DateTime]::UtcNow
$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G49-02';status='official_FIRST_started';operation_kind='first_drawing';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');G49_01_grant_consumed=$false;direct_request_sha256='3a4c92aa95753f6c8809af069000ec9e88a5d3590425eee3df2d1a2e5a879bb4'}
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
