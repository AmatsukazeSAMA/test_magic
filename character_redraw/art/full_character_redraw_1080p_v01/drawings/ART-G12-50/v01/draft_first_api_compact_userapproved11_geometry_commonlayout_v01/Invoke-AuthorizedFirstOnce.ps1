#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$celDirectory=Split-Path -Parent $PSScriptRoot
$lockPath=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '28dd9c309241924a5c96b50a8c092e86bd698367a62db762590cbb6d43c61b7d'){throw 'Exact call lock changed.'}
$lock=Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
foreach($record in @($lock.formal_request,$lock.draft,$lock.prompt,$lock.root_release,$lock.project_release,$lock.project_authorization)){
    if((Get-FileHash -LiteralPath $record.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.sha256){throw 'Released evidence bytes changed.'}
}
foreach($record in $lock.references){
    if((Get-FileHash -LiteralPath $record.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.sha256){throw 'Exact reference bytes changed.'}
}
$formal=Get-Content -LiteralPath $lock.formal_request.path -Raw | ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.Size -ne $lock.Size -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.InputImages.Count -ne $lock.reference_count -or $formal.OutputDirectory -ne $celDirectory){throw 'Unexpected exact8field request.'}
for($i=0;$i -lt $lock.reference_count;$i++){if($formal.InputImages[$i] -ne $lock.references[$i].path){throw 'Reference order changed.'}}
$projectRoot='D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01'
$registry=Get-Content -LiteralPath (Join-Path $projectRoot 'ASSET_REGISTRY.json') -Raw | ConvertFrom-Json
$previous=$registry.($lock.previous_id)
if(-not $previous.primary_static_pass -or -not $previous.independent_static_pass -or $previous.sha256 -ne $lock.previous_sha256){throw 'Previous currentbothreviewed state changed.'}
$config=Get-Content -LiteralPath 'C:\Users\11515\.agents\skills\openai-api\api\connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured image model changed.'}
$scope=Get-Content -LiteralPath $lock.project_release.path -Raw | ConvertFrom-Json
$scriptPath='D:\CODEX\魔术之心\scripts\Invoke-ReferenceImage.ps1'
if((Get-FileHash -LiteralPath $scriptPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $scope.provider_script.sha256){throw 'Existing official provider script changed.'}
if($Preview){& $scriptPath @formal -Preview;return}
if(Test-Path -LiteralPath (Join-Path $celDirectory 'attempt.json')){throw 'Existing attempt; no retry permitted.'}
$receiptPath=Join-Path $celDirectory 'ARTIST_API_EXECUTION_RECEIPT.json'
if(Test-Path -LiteralPath $receiptPath){throw 'Artist invocation already recorded; no second call.'}
$started=[DateTime]::UtcNow
$receipt=@{id=$lock.id;status='approved_invocation_started';started_utc=$started.ToString('o');formal_request_sha256=$lock.formal_request.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;root_release_sha256=$lock.root_release.sha256;project_authorization_sha256=$lock.project_authorization.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt | ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{
    & $scriptPath @formal
    $receipt.status='provider_script_returned'
    $receipt.provider_result=Get-Content -LiteralPath (Join-Path $celDirectory 'result.json') -Raw | ConvertFrom-Json
}catch{
    $receipt.status='failed_or_unknown_no_retry'
    $receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]'
    throw
}finally{
    $receipt.finished_utc=[DateTime]::UtcNow.ToString('o')
    $receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3)
    Save-Receipt
}
