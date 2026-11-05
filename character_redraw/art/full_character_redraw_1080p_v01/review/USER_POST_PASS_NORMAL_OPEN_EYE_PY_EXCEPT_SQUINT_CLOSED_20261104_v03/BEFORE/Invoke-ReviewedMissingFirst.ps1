#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Run, [switch]$Preview)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runPath = (Resolve-Path -LiteralPath $Run).Path
if (Test-Path -LiteralPath (Join-Path $runPath 'HOLD_NO_GENERATION.json')) { throw 'This preparation is held after a failed input hypothesis; preserve it and prepare a changed request before generation.' }
$requestPath = Join-Path $runPath 'DIRECT_REQUEST.json'
$releasePath = Join-Path $runPath 'ROOT_DIRECT_EXECUTION_RELEASE.json'
$request = Get-Content -LiteralPath $requestPath -Raw | ConvertFrom-Json -AsHashtable
$release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
if ($release.id -ne $request.id -or $release.maximum_new_logical_requests -ne 1) { throw 'Invalid root release.' }
if ((Get-FileHash -LiteralPath $requestPath -Algorithm SHA256).Hash -ine $release.request_sha256) { throw 'Released request changed.' }
$provider = Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1'
if ((Get-FileHash -LiteralPath $provider -Algorithm SHA256).Hash -ine $release.wrapper_sha256) { throw 'Released provider changed.' }
foreach ($reference in $request.refs) {
    if ((Get-FileHash -LiteralPath $reference.path -Algorithm SHA256).Hash -ine $reference.sha256) { throw 'Released reference changed.' }
    if (@($release.actual_root_viewed_inputs | Where-Object { $_.path -eq $reference.path -and $_.sha256 -eq $reference.sha256 }).Count -ne 1) { throw 'Reference lacks actual root input review.' }
}
if ((Get-FileHash -LiteralPath $request.prompt.path -Algorithm SHA256).Hash -ine $request.prompt.sha256) { throw 'Released prompt changed.' }
if ($request.parameters.OperationKind -ne 'first_missing' -or $request.parameters.DrawingId -ne $request.id) { throw 'Not an explicit missing FIRST.' }
$drawingFolder = Join-Path $projectRoot ('art\full_character_redraw_1080p_v01\drawings\' + $request.id)
$priorExecution = @(Get-ChildItem -LiteralPath $drawingFolder -Recurse -File | Where-Object { $_.Name -in @('attempt.json','BUILTIN_GENERATION.json','result.json') })
if ($priorExecution.Count -gt 0) { throw 'Prior execution exists; classify its result before any FIRST submission.' }
if ($request.model -ne 'gpt-image-2.5-sunburst' -or $request.n -ne 1 -or $request.retry -ne 1 -or $request.parameters.Quality -ne 'high') { throw 'Unexpected provider/count/quality/retry.' }
$invokeArgs = $request.parameters
if ($Preview) { $invokeArgs.Preview = $true }
& $provider @invokeArgs
