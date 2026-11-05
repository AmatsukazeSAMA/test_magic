#Requires -Version 7.0
[CmdletBinding()]
param([ValidateSet('back','side')][string]$View='back',[switch]$Preview)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root ('art\pv_whole_redraw_'+$View+'_v01')
$images=@(Get-ChildItem -LiteralPath (Join-Path $run 'inputs') -File -Filter '*.png' | Sort-Object Name | ForEach-Object FullName)
if($images.Count -ne 5){throw 'The five ordered references must all be present.'}
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Quality high -Size '2560x1440' -Background opaque -OutputFileName 'whole_PV_api_original.png' -Stage ($View+' entire original-PV frame redrawn by API; complete spiral lock, warmer skin') -Preview:$Preview

