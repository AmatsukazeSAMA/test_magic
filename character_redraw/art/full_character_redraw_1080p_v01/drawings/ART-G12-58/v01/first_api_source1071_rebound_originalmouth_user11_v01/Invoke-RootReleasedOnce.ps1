#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$runDir = $PSScriptRoot
$locked = Get-Content -LiteralPath (Join-Path $runDir 'EXECUTION_LOCK_v01.json') -Raw | ConvertFrom-Json
function Assert-Exact([string]$File, [string]$Hash) {
    if ((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Hash) {
        throw "Released immutable payload mismatch: $File"
    }
}
foreach ($item in @($locked.immutable_prep_lock, $locked.formal_request, $locked.authorization, $locked.root_release, $locked.scope_check, $locked.wrapper, $locked.JOB, $locked.REGISTRATION_PLAN, $locked.preview, $locked.source_full, $locked.source_guide)) {
    Assert-Exact $item.path $item.sha256
}
foreach ($ref in $locked.references) { Assert-Exact $ref.path $ref.sha256 }
$prepared = Get-Content -LiteralPath $locked.formal_request.path -Raw | ConvertFrom-Json -AsHashtable
Assert-Exact $prepared.PromptFile $locked.prompt_sha256
if ($prepared.Count -ne 8 -or $prepared.Size -ne '816x1072' -or $prepared.Quality -ne 'high' -or $prepared.Background -ne 'transparent' -or $prepared.InputImages.Count -ne 6 -or $prepared.OutputDirectory -ne $runDir -or $prepared.OutputFileName -ne 'character_api_original.png') {
    throw 'Released argument mismatch'
}
for ($i = 0; $i -lt 6; $i++) {
    if ($prepared.InputImages[$i] -cne $locked.references[$i].path) { throw 'Released reference order changed' }
}
$defaults = Get-Content -LiteralPath $locked.project_defaults_path -Raw | ConvertFrom-Json
if ([string]$defaults.generation_prompt_prefix.text -cne [string]$locked.mandatory_prefix) { throw 'Mandatory LEFT prefix changed' }
$config = Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if ($config.model -ne 'gpt-image-2.5-sunburst') { throw 'Configured model changed' }
if ((Test-Path -LiteralPath (Join-Path $runDir 'attempt.json')) -or (Test-Path -LiteralPath (Join-Path $runDir 'character_api_original.png'))) {
    throw 'Existing attempt/raw: recover only, never resubmit'
}
$release = Get-Content -LiteralPath $locked.root_release.path -Raw | ConvertFrom-Json
$scope = Get-Content -LiteralPath $locked.scope_check.path -Raw | ConvertFrom-Json
if ($release.id -ne 'ART-G12-58' -or $release.one_first_API_only -ne $true -or $scope.execution_authorized_for_exact_one_call -ne $true) { throw 'Exact root release absent' }
$preview = Get-Content -LiteralPath $locked.preview.path -Raw | ConvertFrom-Json
if ($preview.submitted -ne $false -or $preview.endpoint -ne $locked.endpoint -or $preview.model -ne $locked.model -or $preview.size -ne '816x1072' -or $preview.quality -ne 'high' -or $preview.background -ne 'transparent' -or $preview.input_count -ne 6 -or $preview.n -ne 1 -or $preview.mask_provided) {
    throw 'Successful exact no-send Preview required'
}
# Exact one wrapper invocation. The wrapper records attempt/receipt and has curl retry 0.
& $locked.wrapper.path @prepared
