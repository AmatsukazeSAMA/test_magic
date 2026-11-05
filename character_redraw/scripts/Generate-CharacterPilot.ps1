#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$run=Join-Path $base 'drawings\ART-G33-01\v01'
$images=@((Join-Path $run 'inputs\source_character_crop.png'),(Join-Path $base 'inputs\original_identity_turnaround.png'),(Join-Path $base 'inputs\user_hair_side_back.png'))
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Size '640x1024' -Quality high -Background transparent -OutputFileName 'character_api_original.png' -Stage 'Full-film character-only redraw: first compact transparent source-pose cel; natural continuous drill hair, 1080p compositing target' -Preview:$Preview

