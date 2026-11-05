#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_maid_turnaround_v01'
$names=@('identity_turnaround.png','pv_front_F002306.png','pv_front_detail_F003214.png','pv_side_F002751.png','pv_back_F002362.png')
$images=@($names | ForEach-Object { Join-Path $run ('inputs\'+$_) })
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Quality high -Size 1536x1024 -Stage 'three-view candidate only; PV redraw awaits user acceptance' -Preview:$Preview
