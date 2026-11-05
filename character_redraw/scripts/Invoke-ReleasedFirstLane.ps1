#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$LaneFile)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$batchRoot = (Resolve-Path -LiteralPath (Join-Path $projectRoot 'art/full_character_redraw_1080p_v01/batches/USER_REMAINING41_FIRSTS_SUNBURST26_20261105_v01')).Path
$scope = Get-Content -LiteralPath (Join-Path $batchRoot 'USER_REMAINING41_BATCH_SCOPE.json') -Raw | ConvertFrom-Json
$upload = Get-Content -LiteralPath (Join-Path $batchRoot 'USER_PROJECT_LOCAL_IMAGE_UPLOAD_AUTHORIZATION.json') -Raw | ConvertFrom-Json
if ($upload.user_reply_verbatim -ne '允许本项目上传本地图片至openai api') { throw 'Project upload authorization missing.' }
$lanePath = (Resolve-Path -LiteralPath $LaneFile).Path
if (-not $lanePath.StartsWith($batchRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Lane must belong to the authorized batch.' }
$lane = Get-Content -LiteralPath $lanePath -Raw | ConvertFrom-Json
$allowedIds = @($scope.states.id)
$runner = Join-Path $PSScriptRoot 'Invoke-ReviewedMissingFirst.ps1'
$utf8 = [Text.UTF8Encoding]::new($false)
$consecutiveErrors = 0

foreach ($item in $lane.cases) {
    if ($item.id -notin $allowedIds) { throw 'Drawing outside the remaining41 scope.' }
    $run = (Resolve-Path -LiteralPath $item.run).Path
    $request = Get-Content -LiteralPath (Join-Path $run 'DIRECT_REQUEST.json') -Raw | ConvertFrom-Json
    $release = Join-Path $run 'ROOT_DIRECT_EXECUTION_RELEASE.json'
    if ($request.id -ne $item.id -or $request.model -ne 'gpt-image-2.6-sunburst' -or $request.n -ne 1 -or $request.retry -ne 1 -or $request.parameters.Quality -ne 'high') { throw 'Unexpected request scope or parameters.' }
    if ((Get-FileHash -LiteralPath $release -Algorithm SHA256).Hash -ine $item.release_sha256) { throw 'Released input evidence changed.' }
    $drawingRoot = Join-Path $projectRoot ('art/full_character_redraw_1080p_v01/drawings/' + $item.id)
    $existing = @(Get-ChildItem -LiteralPath $drawingRoot -Recurse -File | Where-Object { $_.Name -in @('attempt.json', 'result.json', 'BUILTIN_GENERATION.json') })
    if ($existing.Count -gt 0) {
        Write-Output ("PRESERVED " + $item.id + ' existing execution evidence')
        continue
    }
    $receiptPath = Join-Path $run 'BATCH_OPERATOR_RECEIPT.json'
    if (Test-Path -LiteralPath $receiptPath) { throw 'Existing operator receipt preserved.' }
    $receipt = [ordered]@{id=$item.id; started_utc=[DateTime]::UtcNow.ToString('o'); status='operator_started'; lane_file=$lanePath; logical_requests_authorized=1; retries_authorized=1}
    [IO.File]::WriteAllText($receiptPath, ($receipt | ConvertTo-Json -Depth 5), $utf8)
    Write-Output ("START " + $item.id)
    try {
        & $runner -Run $run | Out-Null
        $result = Join-Path $run 'result.json'
        $image = Join-Path $run 'character_api_original.png'
        if (-not (Test-Path -LiteralPath $result) -or -not (Test-Path -LiteralPath $image)) { throw 'Provider returned without saved image and receipt.' }
        $receipt.status = 'saved_return_pending_actual_reviews'
        $receipt.image = $image
        $receipt.image_sha256 = (Get-FileHash -LiteralPath $image -Algorithm SHA256).Hash.ToLowerInvariant()
        $consecutiveErrors = 0
    } catch {
        $receipt.status = 'terminal_error_preserved_no_resubmission'
        $receipt.error = $_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+', '[REDACTED]'
        $consecutiveErrors += 1
    } finally {
        $receipt.finished_utc = [DateTime]::UtcNow.ToString('o')
        [IO.File]::WriteAllText($receiptPath, ($receipt | ConvertTo-Json -Depth 5), $utf8)
        Write-Output ($receipt.status + ' ' + $item.id)
    }
    if ($consecutiveErrors -ge 2) {
        throw 'Two consecutive request errors. Lane stopped for transport diagnosis.'
    }
}
Write-Output 'LANE_FINISHED'
