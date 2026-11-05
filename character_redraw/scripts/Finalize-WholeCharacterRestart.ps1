#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01\whole_character_restart_v01'
$delivery=Join-Path $base 'delivery'
$index=Get-Content -LiteralPath (Join-Path $delivery 'INDEX.json') -Raw|ConvertFrom-Json
Add-Type -AssemblyName System.Drawing
$atlas=[Drawing.Bitmap]::new(1380,850);$ag=[Drawing.Graphics]::FromImage($atlas);$ag.Clear([Drawing.Color]::FromArgb(245,243,241));$font=[Drawing.Font]::new('Arial',14)
try{
 for($i=0;$i -lt $index.records.Count;$i++){
  $r=$index.records[$i]
  $copy=Join-Path $delivery $r.delivery_original
  Copy-Item -LiteralPath $r.original_image -Destination $copy
  if((Get-FileHash -LiteralPath $copy).Hash.ToLowerInvariant() -ne $r.original_sha256){throw 'Raw delivery bytes changed.'}
  $raw=[Drawing.Bitmap]::new($copy)
  $frame=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb);$g=[Drawing.Graphics]::FromImage($frame)
  try{
   $g.Clear([Drawing.Color]::Transparent);$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
   $s=$r.whole_sprite_uniform_scale;$t=$r.whole_sprite_translation
   $g.DrawImage($raw,[Drawing.RectangleF]::new([single]$t[0],[single]$t[1],[single]($raw.Width*$s),[single]($raw.Height*$s)))
   $frame.Save((Join-Path $delivery $r.delivery_rgba_1080),[Drawing.Imaging.ImageFormat]::Png)
  }finally{$g.Dispose()}
  $preview=[Drawing.Bitmap]::new(1920,1080);$g=[Drawing.Graphics]::FromImage($preview)
  try{$g.Clear([Drawing.Color]::FromArgb(213,167,169));$g.DrawImageUnscaled($frame,0,0);$preview.Save((Join-Path $delivery $r.delivery_pink_preview),[Drawing.Imaging.ImageFormat]::Png)}finally{$g.Dispose()}
  $x=$i*460;$ag.DrawString(('F'+$r.frame+' / '+$r.provider),$font,[Drawing.Brushes]::Black,$x+12,12)
  $displayScale=[Math]::Min(430/[double]$raw.Width,790/[double]$raw.Height)
  $ag.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $ag.DrawImage($raw,[Drawing.RectangleF]::new([single]($x+(460-$raw.Width*$displayScale)/2),[single](46+(790-$raw.Height*$displayScale)/2),[single]($raw.Width*$displayScale),[single]($raw.Height*$displayScale)))
  $raw.Dispose();$frame.Dispose();$preview.Dispose()
 }
 $atlas.Save((Join-Path $delivery 'whole_character_review.png'),[Drawing.Imaging.ImageFormat]::Png)
}finally{$ag.Dispose();$atlas.Dispose();$font.Dispose()}
Write-Output $delivery
