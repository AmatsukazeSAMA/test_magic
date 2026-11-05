#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$RunDirectory)
$ErrorActionPreference='Stop'
$run=[IO.Path]::GetFullPath($RunDirectory)
$utf8=[Text.UTF8Encoding]::new($false)
$attemptPath=Join-Path $run 'attempt.json'
$attempt=Get-Content -LiteralPath $attemptPath -Raw | ConvertFrom-Json
if(Test-Path -LiteralPath (Join-Path $run 'result.json')){throw 'Completed receipt already exists; do not overwrite.'}
if($attempt.http_status -ne '200' -or $attempt.curl_exit_code -ne 0){throw 'Only a known completed HTTP-200 transfer may be recovered locally.'}
$response=Get-Content -LiteralPath (Join-Path $run 'api_response.raw.json') -Raw | ConvertFrom-Json
if(@($response.data).Count -ne 1 -or -not $response.data[0].b64_json){throw 'Complete expected image response unavailable; no API retry.'}
$manifest=Get-Content -LiteralPath (Join-Path $run 'request_manifest.json') -Raw | ConvertFrom-Json -AsHashtable
$imagePath=Join-Path $run 'character_api_original.png'
if(Test-Path -LiteralPath $imagePath){throw 'Image already exists; do not overwrite.'}
[IO.File]::WriteAllBytes($imagePath,[Convert]::FromBase64String($response.data[0].b64_json))
foreach($pair in @(@('response_quality',$response.quality),@('response_size',$response.size),@('response_background',$response.background),@('usage',$response.usage),@('created',$response.created),@('output_path',$imagePath),@('output_sha256',(Get-FileHash -LiteralPath $imagePath -Algorithm SHA256).Hash.ToLowerInvariant()))){$manifest[$pair[0]]=$pair[1]}
$manifest.elapsed_seconds=[Math]::Round(([DateTime]::Parse($attempt.finished_utc)-[DateTime]::Parse($attempt.started_utc)).TotalSeconds,3)
$manifest.local_receipt_recovery=@{reason='Parent review runner stopped while complete HTTP response was already saved; decode stored response without any new API call.';additional_api_calls=0;recovered_utc=[DateTime]::UtcNow.ToString('o')}
[IO.File]::WriteAllText((Join-Path $run 'result.json'),($manifest | ConvertTo-Json -Depth 30),$utf8)
Copy-Item -LiteralPath $attemptPath -Destination (Join-Path $run 'attempt_before_local_recovery.json')
$attempt.status='completed'
$attempt | Add-Member -NotePropertyName image -NotePropertyValue $imagePath -Force
$attempt | Add-Member -NotePropertyName local_receipt_recovery -NotePropertyValue $true -Force
[IO.File]::WriteAllText($attemptPath,($attempt | ConvertTo-Json -Depth 15),$utf8)
[PSCustomObject]@{local_response_decoded=$true;additional_api_calls=0;image=$imagePath}

