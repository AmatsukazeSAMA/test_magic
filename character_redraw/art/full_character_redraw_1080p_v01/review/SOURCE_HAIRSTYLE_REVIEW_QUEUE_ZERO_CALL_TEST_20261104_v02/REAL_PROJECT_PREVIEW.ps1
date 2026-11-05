$ErrorActionPreference='Stop'
$q=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'REAL_PREVIEW_CASE.json') -Raw|ConvertFrom-Json -AsHashtable
& 'D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1' @q -Preview | ConvertTo-Json -Depth 10
