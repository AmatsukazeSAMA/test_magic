#Requires -Version 7.0
$ErrorActionPreference='Stop'
$r=$PSScriptRoot
$l=Get-Content -LiteralPath (Join-Path $r 'REQUEST_LOCK.json') -Raw | ConvertFrom-Json
function Assert-Exact([string]$p,[string]$h){if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $h){throw "Payload mismatch: $p"}}
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN)){Assert-Exact $x.path $x.sha256}
foreach($x in $l.references){Assert-Exact $x.path $x.sha256}
$d=Get-Content -LiteralPath $l.project_defaults_path -Raw | ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'LEFT prefix changed'}
if(Test-Path -LiteralPath (Join-Path $r 'attempt.json')){throw 'Attempt exists, recovery only'}
$p=Get-Content -LiteralPath $l.prepared_request.path -Raw | ConvertFrom-Json -AsHashtable
if($p.Count -ne 8 -or $p.Size -ne '1424x1040' -or $p.Quality -ne 'high' -or $p.Background -ne 'transparent' -or $p.InputImages.Count -ne 6){throw 'Payload arguments mismatch'}
$report=& $l.wrapper.path @p -Preview
if($report.submitted -ne $false -or $report.endpoint -ne $l.endpoint -or $report.model -ne $l.model -or $report.size -ne $l.size -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected preview'}
$dest=Join-Path $r 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $dest){throw 'Preserve existing preview'}
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$report
