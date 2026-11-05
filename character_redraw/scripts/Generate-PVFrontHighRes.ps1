#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_pv_F002306_v02'
$names=@('source_F002306_detail.png','maid_identity_head_front.png','source_F002306.png')
$images=@($names | ForEach-Object { Join-Path $run ('inputs\'+$_) })
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Quality high -Size 1536x2304 -Background transparent -OutputFileName 'pv_character_highres_api_raw.png' -Stage 'F2306 front full body v02: new high-resolution portrait generation with PV style simplification; not an upscale or animation' -Preview:$Preview
