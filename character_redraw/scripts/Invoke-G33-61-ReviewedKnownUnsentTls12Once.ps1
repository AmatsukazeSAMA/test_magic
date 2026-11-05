#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Run, [switch]$Preview)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$base = Join-Path $projectRoot 'art/full_character_redraw_1080p_v01'
$drawing = Join-Path $base 'drawings/ART-G33-61'
$runPath = (Resolve-Path -LiteralPath $Run).Path
$expectedRun = Join-Path $drawing 'v01/direct_first_api_source2582_ownPose_danceB_tls12_knownUnsent_v21'
if ($runPath -ine (Resolve-Path -LiteralPath $expectedRun).Path) { throw 'Not the exact G33-61 recovery v21 run.' }
$old = Join-Path $drawing 'v01/direct_first_api_source2582_ownPose_danceB_tls12_v20'
function Read-Json([string]$File) { Get-Content -LiteralPath $File -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable }
function Test-Hash([string]$File, [string]$Expected) {
    if (-not $Expected -or (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash -ine $Expected) { throw "Locked file mismatch: $File" }
}
function Test-Ref($Ref, [string]$File) {
    if (-not $Ref -or $Ref.path -ine (Resolve-Path -LiteralPath $File).Path) { throw "Locked file path mismatch: $File" }
    Test-Hash $File $Ref.sha256
}
$requestPath = Join-Path $runPath 'DIRECT_REQUEST.json'
$release = Read-Json (Join-Path $runPath 'ROOT_DIRECT_EXECUTION_RELEASE.json')
$r = Read-Json $requestPath
Test-Hash $requestPath $release.request_sha256
if ($r.id -ne 'ART-G33-61' -or $release.id -ne $r.id -or $release.maximum_new_logical_requests -ne 1 -or $release.official_calls_before_this_release -ne 0) { throw 'Unexpected release scope.' }
if (Test-Path -LiteralPath (Join-Path $runPath 'HOLD_NO_GENERATION.json')) { throw 'Recovery is held.' }
$p = $r.parameters
if ($p.OperationKind -ne 'first_missing' -or $p.DrawingId -ne $r.id -or $p.OutputDirectory -ine $runPath -or $p.OutputFileName -ne 'character_api_original.png' -or $p.Size -ne '816x1072' -or $p.Background -ne 'transparent' -or $p.Quality -ne 'high' -or $r.model -ne 'gpt-image-2.5-sunburst' -or $r.n -ne 1 -or $r.retry -ne 1) { throw 'Unexpected provider/count/quality/retry/output.' }
$defaults = Read-Json (Join-Path $projectRoot 'image_defaults.json')
if ($r.eye_color_policy.path -ne $defaults.eye_color_policy.path -or $r.eye_color_policy.sha256 -ne $defaults.eye_color_policy.sha256 -or $defaults.api_request_policy.retry -ne 1) { throw 'Current eye or retry policy changed.' }
Test-Hash $r.eye_color_policy.path $r.eye_color_policy.sha256
Test-Hash (Join-Path $projectRoot 'image_defaults.json') $r.recovery_of.defaults_sha256

$provider = Join-Path $PSScriptRoot 'Invoke-ReferenceImage-Tls12Recovery20261104.ps1'
Test-Ref $r.provider $provider
Test-Hash $provider $release.wrapper_sha256
Test-Ref $release.runner $PSCommandPath
$proofPath = Join-Path $old 'KNOWN_UNSENT_BEFORE_HTTP_CLASSIFICATION.json'
Test-Ref $r.recovery_of.proof $proofPath
Test-Ref $release.known_unsent_evidence $proofPath
$proof = Read-Json $proofPath
$attemptPath = Join-Path $old 'attempt.json'
$metricsPath = Join-Path $old 'curl_transport_metrics.json'
$headersPath = Join-Path $old 'response_headers.txt'
if ($proof.id -ne $r.id -or $proof.classification -cne 'known_unsent_before_http' -or $proof.original_attempt_record_preserved -ine $attemptPath -or $proof.facts.http_status -ne '000' -or $proof.facts.curl_exit_code -ne 35 -or $proof.facts.size_request -ne 0 -or $proof.facts.size_upload -ne 0 -or $proof.facts.response_file_exists -ne $false -or $proof.facts.server_image_exists -ne $false -or $proof.facts.server_result_record_exists -ne $false) { throw 'Prior execution is not verified unsent.' }
Test-Hash $attemptPath $proof.original_attempt_record_sha256
Test-Ref $proof.transport_metrics $metricsPath
Test-Ref $proof.proxy_connect_headers $headersPath
$attempt = Read-Json $attemptPath
$metrics = Read-Json $metricsPath
if ($attempt.curl_exit_code -ne 35 -or $attempt.http_status -ne '000' -or $attempt.transport_attempt_count -ne 1 -or $metrics.exitcode -ne 35 -or $metrics.http_code -ne 0 -or $metrics.http_connect -ne 200 -or $metrics.time_appconnect -ne 0 -or $metrics.size_request -ne 0 -or $metrics.size_upload -ne 0 -or $metrics.size_download -ne 0 -or $metrics.num_retries -ne 0 -or $metrics.proxy_used -ne 1 -or (Get-Content -LiteralPath $headersPath -Raw).Trim() -ne 'HTTP/1.1 200 Connection established') { throw 'Prior HTTP transport evidence no longer matches.' }
$priorExecutions = @(Get-ChildItem -LiteralPath $drawing -Recurse -File | Where-Object { $_.Name -in @('attempt.json','BUILTIN_GENERATION.json','result.json','character_api_original.png','character_imggen_original.png','api_response.raw.json') })
if ($priorExecutions.Count -ne 1 -or $priorExecutions[0].FullName -ine $attemptPath) { throw 'Another execution or result exists; do not submit.' }
$registry = Read-Json (Join-Path $base 'ASSET_REGISTRY.json')
if (($registry | ConvertTo-Json -Depth 50 -Compress).Contains('ART-G33-61')) { throw 'G33-61 already has a registry or alias record.' }

$oldQpath = Join-Path $old 'DIRECT_REQUEST.json'
$oldReleasePath = Join-Path $old 'ROOT_DIRECT_EXECUTION_RELEASE.json'
Test-Ref $r.recovery_of.original_request $oldQpath
Test-Ref $release.prior_actual_review_release $oldReleasePath
$oldQ = Read-Json $oldQpath
$oldRelease = Read-Json $oldReleasePath
Test-Hash $oldQpath $oldRelease.request_sha256
Test-Hash $oldQ.prompt.path $oldQ.prompt.sha256
Test-Ref $r.prompt $p.PromptFile
if ($r.prompt.sha256 -ne $oldQ.prompt.sha256 -or $r.model -ne $oldQ.model -or $r.n -ne $oldQ.n -or $r.retry -ne $oldQ.retry -or $r.provider.sha256 -ne $oldQ.provider.sha256) { throw 'Recovery prompt/provider payload differs from the unsent request.' }
if ($r.refs.Count -ne 5 -or $r.refs.Count -ne $oldQ.refs.Count -or $p.InputImages.Count -ne $r.refs.Count -or $p.Count -ne $oldQ.parameters.Count) { throw 'Unexpected reference or parameter count.' }
foreach ($key in $oldQ.parameters.Keys) {
    if ($key -in @('OutputDirectory','PromptFile')) { continue }
    if (($p[$key] | ConvertTo-Json -Depth 10 -Compress) -cne ($oldQ.parameters[$key] | ConvertTo-Json -Depth 10 -Compress)) { throw "Recovery parameter changed: $key" }
}
for ($i = 0; $i -lt $r.refs.Count; $i++) {
    $ref = $r.refs[$i]; $prior = $oldQ.refs[$i]
    if ($ref.path -cne $prior.path -or $ref.sha256 -cne $prior.sha256 -or $p.InputImages[$i] -cne $ref.path) { throw 'Recovery reference changed.' }
    Test-Hash $ref.path $ref.sha256
    foreach ($proofRelease in @($oldRelease,$release)) {
        if (@($proofRelease.actual_root_viewed_inputs | Where-Object { $_.path -eq $ref.path -and $_.sha256 -eq $ref.sha256 }).Count -ne 1) { throw 'Reference lacks exact recorded root review.' }
    }
}
if ($Preview) { $p.Preview = $true }
& $provider @p
