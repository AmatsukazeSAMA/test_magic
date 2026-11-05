#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_pv_F002306_v01'
$names=@('source_F002306.png','maid_turnaround_v01.png','source_F002306_detail.png')
$images=@($names | ForEach-Object { Join-Path $run ('inputs\'+$_) })
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Quality high -Size 2048x1152 -Background transparent -OutputFileName 'pv_character_api_raw.png' -Stage 'one original-PV frame redraw trial; F2306 front full body; not a sequence' -Preview:$Preview
