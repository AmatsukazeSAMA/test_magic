#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$dp=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $dp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b18fbbff3ebb1955b4c2c2df143426af50c30c6ba9cdc63b1be9fd4184dff848'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $dp -Raw|ConvertFrom-Json
foreach($x in @($d.authorization,$d.provider,$d.prompt,$d.source)+@($d.refs)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Direct payload changed'}
}
$q=$d.parameters|ConvertTo-Json -Depth 8|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.OutputDirectory -ne $PSScriptRoot -or $q.Size -ne '1136x1040' -or $q.InputImages.Count -ne 3 -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent'){throw 'Unexpected direct parameters'}
if($Preview){& $d.provider.path @q -Preview|ConvertTo-Json -Depth 10;return}
foreach($name in @('attempt.json','result.json','character_api_original.png','DIRECT_API_EXECUTION_RECEIPT.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'Existing execution evidence: recover only; do not submit'}
}
$rp=Join-Path $PSScriptRoot 'DIRECT_API_EXECUTION_RECEIPT.json'
$start=[DateTime]::UtcNow
$r=@{id=$d.id;status='direct_one_logical_first_started';started_utc=$start.ToString('o');n=1;configured_retry=1;request_sha256='b18fbbff3ebb1955b4c2c2df143426af50c30c6ba9cdc63b1be9fd4184dff848';endpoint='https://api.openai.com/v1/images/edits'}
function Save-DirectReceipt{[IO.File]::WriteAllText($rp,($r|ConvertTo-Json -Depth 20),[Text.UTF8Encoding]::new($false))}
Save-DirectReceipt
try{
 & $d.provider.path @q
 $r.status='known_saved'
 $r.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json
}catch{
 $r.status='failed_or_unknown_no_manual_retry'
 $r.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]'
 throw
}finally{
 $r.finished_utc=[DateTime]::UtcNow.ToString('o')
 $r.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3)
 Save-DirectReceipt
}
