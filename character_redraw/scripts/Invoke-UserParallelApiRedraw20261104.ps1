#Requires -Version 7.0
param([Parameter(Mandatory)][string]$Run,[switch]$Preview,[switch]$Tls12Recovery)
$ErrorActionPreference = 'Stop'
$runPath = (Resolve-Path -LiteralPath $Run).Path
$root = Split-Path $PSScriptRoot -Parent
$r = Get-Content -LiteralPath (Join-Path $runPath 'API_REDRAW_REQUEST.json') -Raw | ConvertFrom-Json
if ($r.id -notin @('ART-G33-49','ART-X01-15') -or $r.provider -ne 'configured OpenAI API' -or $r.n -ne 1 -or $r.quality -ne 'high' -or $r.operation -ne 'redraw') { throw 'Unexpected scope.' }
$runName = if ($Tls12Recovery) { 'api_user_parallel_redraw_latest_coil_tls12_v02' } else { 'api_user_parallel_redraw_latest_coil_v01' }
$expected = Join-Path $root "art/full_character_redraw_1080p_v01/drawings/$($r.id)/v01/$runName"
if ($runPath -ine (Resolve-Path -LiteralPath $expected).Path) { throw 'Unexpected output directory.' }
foreach ($f in @($r.prompt, $r.wrapper, $r.eye_policy) + @($r.references)) {
    if ((Get-FileHash -LiteralPath $f.path -Algorithm SHA256).Hash -ine $f.sha256) { throw 'Prepared input changed.' }
}
if ($Tls12Recovery) {
    if (-not $r.recovery_of -or (Get-FileHash -LiteralPath $r.recovery_of.path -Algorithm SHA256).Hash -ine $r.recovery_of.sha256) { throw 'Missing pre-HTTP failure evidence.' }
    $proof = Get-Content -LiteralPath $r.recovery_of.path -Raw | ConvertFrom-Json
    if ($proof.classification -ne 'known_unsent_before_HTTP' -or $proof.facts.curl_exit_code -ne 35 -or $proof.facts.size_request -ne 0 -or $proof.facts.size_upload -ne 0) { throw 'Prior submission is not proven unsent.' }
}
foreach ($name in @('attempt.json','result.json','character_api_original.png')) {
    if (Test-Path -LiteralPath (Join-Path $runPath $name)) { throw 'Existing attempt or result. Do not submit again.' }
}
$argsForProvider = @{
    PromptFile = $r.prompt.path; InputImages = [string[]]@($r.references | ForEach-Object {$_.path})
    OutputDirectory = $runPath; Size = $r.size; Quality = 'high'; Background = 'transparent'
    OutputFileName = 'character_api_original.png'; Stage = "$($r.id)_USER_PARALLEL_COIL_REDRAW"
    DrawingId = $r.id; OperationKind = 'redraw'; Preview = $Preview
}
& $r.wrapper.path @argsForProvider
