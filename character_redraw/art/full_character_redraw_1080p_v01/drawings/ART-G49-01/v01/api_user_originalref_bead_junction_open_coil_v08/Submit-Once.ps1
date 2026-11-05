#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
$request = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'DIRECT_REQUEST.json') -Raw | ConvertFrom-Json -AsHashtable
$apiParameters = $request.parameters
& 'D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1' @apiParameters
