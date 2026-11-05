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
$defaults = Get-Content -LiteralPath (Join-Path $projectRoot 'image_defaults.json') -Raw | ConvertFrom-Json -AsHashtable
if ($request.eye_color_policy.path -ne $defaults.eye_color_policy.path -or $request.eye_color_policy.sha256 -ne $defaults.eye_color_policy.sha256) { throw 'Prepared eye policy is superseded; preserve it and prepare the latest post-pass/eye-expression workflow.' }
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
if ($release.authorized_prior_rejected_attempts) {
    $authorization = $release.remaining41_batch_authorization
    $expected = Join-Path $projectRoot 'art/full_character_redraw_1080p_v01/batches/USER_REMAINING41_FIRSTS_SUNBURST26_20261105_v01/USER_REMAINING41_BATCH_SCOPE.json'
    if ($request.id -ne 'ART-G33-16' -or $authorization.path -ne $expected -or (Get-FileHash -LiteralPath $authorization.path -Algorithm SHA256).Hash -ine $authorization.sha256) { throw 'Invalid known-rejected replacement authorization.' }
    foreach ($prior in $release.authorized_prior_rejected_attempts) {
        if ((Get-FileHash -LiteralPath $prior.path -Algorithm SHA256).Hash -ine $prior.sha256) { throw 'Prior rejection evidence changed.' }
        $receipt = Get-Content -LiteralPath $prior.path -Raw | ConvertFrom-Json
        if ($receipt.status -ne 'api_rejected' -or [string]$receipt.http_status -ne '400' -or $receipt.curl_exit_code -ne 0) { throw 'Only a definite HTTP 400 rejection may be replaced under this scope.' }
        $priorExecution = @($priorExecution | Where-Object { $_.FullName -ne $prior.path })
    }
}
if ($priorExecution.Count -gt 0) { throw 'Prior execution exists; classify its result before any FIRST submission.' }
$policy = $defaults.api_request_policy
if ($request.model -ne $policy.model -or $request.n -ne $policy.n -or $request.retry -ne $policy.retry -or $request.parameters.Quality -ne $policy.quality) { throw 'Prepared API request differs from the current model/count/quality/retry policy.' }
$invokeArgs = $request.parameters
if ($Preview) { $invokeArgs.Preview = $true }
& $provider @invokeArgs
