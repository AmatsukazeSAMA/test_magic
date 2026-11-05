#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$RunDirectory,[string]$InputFile='head_api_original.png')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -Path (Join-Path $PSScriptRoot 'PVPaletteV2.cs')
$path=Join-Path $RunDirectory $InputFile
$im=[Drawing.Bitmap]::new($path)
try {
 $r=[Drawing.Rectangle]::new(0,0,$im.Width,$im.Height)
 $bits=$im.LockBits($r,[Drawing.Imaging.ImageLockMode]::ReadWrite,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try {
  if($bits.Stride -lt 0){throw 'Unexpected PNG stride.'}
  $buffer=[byte[]]::new($bits.Stride*$im.Height)
  [Runtime.InteropServices.Marshal]::Copy($bits.Scan0,$buffer,0,$buffer.Length)
  $counts=[PVPaletteV2]::GradeHead($buffer,$im.Width,$im.Height,$bits.Stride)
  if($counts[6] -ne 0 -or $counts[7] -ne 0){throw 'Palette correction changed alpha or dark ink cores.'}
  [Runtime.InteropServices.Marshal]::Copy($buffer,0,$bits.Scan0,$buffer.Length)
 } finally {$im.UnlockBits($bits)}
 $im.Save((Join-Path $RunDirectory 'head_palette_matched.png'),[Drawing.Imaging.ImageFormat]::Png)
 @{method='user-requested warmer skin and limited-palette correction of the API drawing; no line or geometry reconstruction';drawing_provider='OpenAI API';original=$InputFile;output='head_palette_matched.png';palette_input_sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant();output_sha256=(Get-FileHash -LiteralPath (Join-Path $RunDirectory 'head_palette_matched.png') -Algorithm SHA256).Hash.ToLowerInvariant();palette_script_sha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'PVPaletteV2.cs') -Algorithm SHA256).Hash.ToLowerInvariant();wrapper_script_sha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();source_skin_reference='20261030_maid_turnaround_v01/inputs/identity_turnaround.png';source_skin_patch_xyxy=@(474,224,513,236);source_skin_patch_median_rgb=@(254,244,238);target_skin_rgb=@(252,232,220);target_hair_rgb=@(184,183,180);target_headband_rgb=@(238,238,235);target_mint_rgb=@(177,207,187);target_beads_rgb=@(181,28,36);changed_color_pixels=$counts[0];classified_skin_pixels=$counts[1];classified_hair_pixels=$counts[2];classified_white_pixels=$counts[3];classified_mint_pixels=$counts[4];classified_red_pixels=$counts[5];changed_alpha_pixels=$counts[6];changed_dark_ink_core_pixels=$counts[7];user_accepted=$false} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $RunDirectory 'PALETTE_MATCH.json') -Encoding utf8
 Write-Output 'Applied warmer revised skin; alpha and dark ink cores unchanged.'
} finally {$im.Dispose()}
