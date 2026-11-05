#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$refs=Join-Path $root 'art\20261030_braid_revision_refs'
[void][IO.Directory]::CreateDirectory($refs)
$pairs=@(
 @('C:\Users\11515\AppData\Local\Temp\codex-clipboard-ddddd404-b6f6-4582-a24a-82b11c9c87c6.png','user_side_back_hair.png'),
 @('C:\Users\11515\AppData\Local\Temp\codex-clipboard-12172e1c-7327-48d5-8191-06f67274a77c.png','user_back_bob_detail.png')
)
foreach($pair in $pairs){Copy-Item -LiteralPath $pair[0] -Destination (Join-Path $refs $pair[1])}
foreach($view in @('side','back')){
 $run=Join-Path $root ('art\20261030_braid_'+$view+'_v02');$inputs=Join-Path $run 'inputs'
 [void][IO.Directory]::CreateDirectory($inputs)
 $old=Join-Path $root ('art\20261030_head_style_'+$view+'_v01')
 Copy-Item -LiteralPath (Join-Path $old 'head_palette_matched.png') -Destination (Join-Path $inputs 'previous_head.png')
 Copy-Item -LiteralPath (Join-Path $old 'inputs\source_head_style.png') -Destination (Join-Path $inputs 'source_PV_head_style.png')
 Copy-Item -LiteralPath (Join-Path $refs 'user_side_back_hair.png') -Destination (Join-Path $inputs 'user_side_back_hair.png')
 Copy-Item -LiteralPath (Join-Path $refs 'user_back_bob_detail.png') -Destination (Join-Path $inputs 'user_back_bob_detail.png')
 if($view -eq 'side'){
  $im=[Drawing.Bitmap]::new((Join-Path $inputs 'previous_head.png'))
  $pad=[Drawing.Bitmap]::new(1024,1536,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g=[Drawing.Graphics]::FromImage($pad)
  try {$g.Clear([Drawing.Color]::Transparent);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$g.DrawImageUnscaled($im,0,0);$pad.Save((Join-Path $inputs 'edit_base_portrait.png'),[Drawing.Imaging.ImageFormat]::Png)} finally {$g.Dispose();$pad.Dispose();$im.Dispose()}
  Copy-Item -LiteralPath (Join-Path $root 'art\20261030_head_style_front_v03\head_palette_matched.png') -Destination (Join-Path $inputs 'front_braid_shape_reference.png')
 }
 @{edit_type='local correction of previous candidate, explicitly requested by user';previous_delivery='20261030_pv_three_angles_v01';user_corrections=@('skin too pale: modest warmer peach, RGB 252,232,220','side spiral lock too short: lengthen toward front of chest','back bob follows latest user reference; long spiral lock is in FRONT and must not be drawn as a severed rear stub');view=$view;provider='configured OpenAI API';quality='high';user_accepted=$false} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $run 'REVISION_INTENT.json') -Encoding utf8
}
Write-Output 'Archived both user references and prepared side/back local-edit inputs.'
