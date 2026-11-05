#Requires -Version 7.0
[CmdletBinding()]
param([ValidateSet('front','side','back')][string]$View='front',[switch]$Preview)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$runs=@{front='20261030_head_style_front_v03';side='20261030_head_style_side_v01';back='20261030_head_style_back_v01'}
$run=Join-Path $root ('art\'+$runs[$View])
$images=@((Join-Path $run 'inputs\source_head_style.png'),(Join-Path $run 'inputs\identity_head.png'))
if($View -ne 'front'){$images+=Join-Path $run 'inputs\front_style_master.png'}
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Quality high -Size 1024x1024 -Background transparent -OutputFileName 'head_api_original.png' -Stage ($View+' head-only PV style trial; fixed flat palette; original body to be retained') -Preview:$Preview
