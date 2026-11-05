$ErrorActionPreference='Stop'
$q=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'case.json') -Raw|ConvertFrom-Json -AsHashtable
& (Join-Path $PSScriptRoot 'scripts/Invoke-ReferenceImage.ps1') @q -Preview | ConvertTo-Json -Depth 10
