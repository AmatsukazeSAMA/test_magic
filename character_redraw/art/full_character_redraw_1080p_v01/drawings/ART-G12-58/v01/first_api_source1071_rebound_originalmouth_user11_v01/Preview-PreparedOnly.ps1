#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$runDir = $PSScriptRoot
$locked = Get-Content -LiteralPath (Join-Path $runDir 'REQUEST_LOCK.json') -Raw | ConvertFrom-Json
function Assert-Exact([string]$File, [string]$Hash) {
    if ((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Hash) {
        throw "Immutable preparation mismatch: $File"
    }
}
foreach ($item in @($locked.prepared_request, $locked.draft, $locked.prompt, $locked.wrapper, $locked.authorization, $locked.scope_check, $locked.JOB, $locked.REGISTRATION_PLAN, $locked.source_full, $locked.source_guide, $locked.input_provenance)) {
    Assert-Exact $item.path $item.sha256
}
foreach ($ref in $locked.references) { Assert-Exact $ref.path $ref.sha256 }
$prepared = Get-Content -LiteralPath $locked.prepared_request.path -Raw | ConvertFrom-Json -AsHashtable
if ($prepared.Count -ne 8 -or $prepared.Size -ne '816x1072' -or $prepared.Quality -ne 'high' -or $prepared.Background -ne 'transparent' -or $prepared.InputImages.Count -ne 6) {
    throw 'Unexpected prepared arguments'
}
Assert-Exact $prepared.PromptFile $locked.prompt_sha256
$defaults = Get-Content -LiteralPath $locked.project_defaults_path -Raw | ConvertFrom-Json
if ([string]$defaults.generation_prompt_prefix.text -cne [string]$locked.mandatory_prefix) { throw 'Mandatory LEFT prefix changed' }
$config = Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if ($config.model -ne $locked.model) { throw 'Configured model changed' }
if ((Test-Path -LiteralPath (Join-Path $runDir 'attempt.json')) -or (Test-Path -LiteralPath (Join-Path $runDir 'character_api_original.png'))) {
    throw 'Existing attempt or raw; recover only, never resubmit'
}
$previewPath = Join-Path $runDir 'API_PREVIEW_PROOF_v01.json'
if (Test-Path -LiteralPath $previewPath) { throw 'Preserve existing Preview evidence' }
# This helper has no send branch. Preview returns before credential or network code.
$report = & $locked.wrapper.path @prepared -Preview
if ($report.submitted -ne $false -or $report.endpoint -ne $locked.endpoint -or $report.model -ne $locked.model -or $report.quality -ne 'high' -or $report.size -ne '816x1072' -or $report.background -ne 'transparent' -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided) {
    throw 'Unexpected no-send Preview result'
}
[IO.File]::WriteAllText($previewPath, ($report | ConvertTo-Json -Depth 10), [Text.UTF8Encoding]::new($false))
$report
