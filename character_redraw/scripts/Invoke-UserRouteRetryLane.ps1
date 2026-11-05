#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$LaneFile)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$lane = Get-Content -LiteralPath $LaneFile -Raw | ConvertFrom-Json
$utf8 = [Text.UTF8Encoding]::new($false)
$errorsInSequence = 0
$stopFile = Join-Path (Split-Path $LaneFile -Parent) 'STOP_ROUTE_RETRY_TRANSPORT.json'
foreach ($item in $lane.cases) {
    if (Test-Path -LiteralPath $stopFile) { throw 'Retry transport circuit breaker is open.' }
    $run = (Resolve-Path -LiteralPath $item.run).Path
    $releasePath = Join-Path $run 'ROOT_ROUTE_RETRY_RELEASE.json'
    if ((Get-FileHash -LiteralPath $releasePath -Algorithm SHA256).Hash -ine $item.root_release_sha256) { throw 'Retry release changed.' }
    $release = Get-Content -LiteralPath $releasePath -Raw | ConvertFrom-Json
    if ($release.id -ne $item.id -or $release.maximum_new_logical_requests -ne 1 -or $release.user_reply_verbatim -ne '已更换网络线路，重试') { throw 'Exact user retry authorization missing.' }
    foreach ($ref in @($release.request, $release.upload_authorization, $release.parent_attempt, $release.parent_metrics, $release.parent_root_release)) {
        if ((Get-FileHash -LiteralPath $ref.path -Algorithm SHA256).Hash -ine $ref.sha256) { throw 'Released retry evidence changed.' }
    }
    $request = Get-Content -LiteralPath $release.request.path -Raw | ConvertFrom-Json -AsHashtable
    if ($request.id -ne $item.id -or $request.model -ne 'gpt-image-2.6-sunburst' -or $request.n -ne 1 -or $request.retry -ne 1 -or $request.parameters.Quality -ne 'high') { throw 'Unexpected retry parameters.' }
    foreach ($ref in @($request.provider, $request.prompt) + @($request.refs)) {
        if ((Get-FileHash -LiteralPath $ref.path -Algorithm SHA256).Hash -ine $ref.sha256) { throw 'Retry payload changed.' }
    }
    $provider = (Resolve-Path -LiteralPath $request.provider.path).Path
    if ($provider -ne (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1')) { throw 'Only the project official image provider may execute.' }
    $drawingRoot = Join-Path $projectRoot ('art/full_character_redraw_1080p_v01/drawings/' + $item.id)
    if (@(Get-ChildItem -LiteralPath $drawingRoot -Recurse -Filter 'character_api_original.png' -File).Count -gt 0) {
        Write-Output ('PRESERVED ' + $item.id + ' already has a return')
        continue
    }
    foreach ($name in @('attempt.json', 'result.json', 'ROUTE_RETRY_OPERATOR.json')) {
        if (Test-Path -LiteralPath (Join-Path $run $name)) { throw 'This authorized retry already has execution evidence.' }
    }
    $receipt = [ordered]@{id=$item.id; status='user_authorized_route_retry_started'; started_utc=[DateTime]::UtcNow.ToString('o'); parent_transport_class=$release.parent_transport_class}
    $receiptPath = Join-Path $run 'ROUTE_RETRY_OPERATOR.json'
    [IO.File]::WriteAllText($receiptPath, ($receipt | ConvertTo-Json -Depth 5), $utf8)
    Write-Output ('START ' + $item.id)
    try {
        $invokeArgs = $request.parameters
        & $provider @invokeArgs | Out-Null
        if (-not (Test-Path -LiteralPath (Join-Path $run 'result.json'))) { throw 'No saved result.' }
        $receipt.status = 'saved_return_pending_actual_reviews'
        $errorsInSequence = 0
    } catch {
        $receipt.status = 'retry_terminal_error_preserved'
        $receipt.error = $_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+', '[REDACTED]'
        $errorsInSequence += 1
    } finally {
        $receipt.finished_utc = [DateTime]::UtcNow.ToString('o')
        [IO.File]::WriteAllText($receiptPath, ($receipt | ConvertTo-Json -Depth 5), $utf8)
        Write-Output ($receipt.status + ' ' + $item.id)
    }
    if ($errorsInSequence -ge 2) {
        [IO.File]::WriteAllText($stopFile, ($receipt | ConvertTo-Json -Depth 5), $utf8)
        throw 'Two consecutive retry failures. All retry lanes stopped.'
    }
}
Write-Output 'LANE_FINISHED'
