#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$delivery=Join-Path $root 'art\20261030_pv_three_angles_v01'
$views=@(
 @{id='front';label='正面 F2306 · 01:16.944';crop=@(760,55,360,1000)},
 @{id='side';label='侧面 F2751 · 01:31.792';crop=@(55,135,425,875)},
 @{id='back';label='背面 F2362 · 01:18.812';crop=@(755,55,435,1025)}
)
$title=[Drawing.Font]::new('Microsoft YaHei',28,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
$font=[Drawing.Font]::new('Microsoft YaHei',22,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
$small=[Drawing.Font]::new('Microsoft YaHei',18,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
$ink=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(50,45,47))
$figures=[Drawing.Bitmap]::new(1520,1160,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$heads=[Drawing.Bitmap]::new(1880,790,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$frames=[Drawing.Bitmap]::new(1200,2195,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$gf=[Drawing.Graphics]::FromImage($figures);$gh=[Drawing.Graphics]::FromImage($heads);$gp=[Drawing.Graphics]::FromImage($frames)
try {
 foreach($g in @($gf,$gh,$gp)){$g.Clear([Drawing.Color]::FromArgb(247,243,240));$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality}
 $gf.DrawString('原 PV 头部替换 · 正 / 侧 / 背',$title,$ink,20,12)
 $gh.DrawString('头部近景 · 肤色按最初人设统一',$title,$ink,20,12)
 for($i=0;$i -lt $views.Count;$i++){
  $v=$views[$i];$run=Join-Path $delivery $v.id
  $im=[Drawing.Bitmap]::new((Join-Path $run 'composite_1920x1080.png'))
  $detail=[Drawing.Bitmap]::new((Join-Path $run 'head_detail.png'))
  try {
   $col=20+$i*500;$gf.DrawString($v.label,$font,$ink,$col,58)
   $c=$v.crop;$factor=[Math]::Min(480.0/$c[2],1000.0/$c[3]);$dw=[int][Math]::Round($c[2]*$factor);$dh=[int][Math]::Round($c[3]*$factor)
   $gf.DrawImage($im,[Drawing.Rectangle]::new($col+[int]((480-$dw)/2),100,$dw,$dh),$c[0],$c[1],$c[2],$c[3],[Drawing.GraphicsUnit]::Pixel)
   $col=20+$i*620;$gh.DrawString($v.label,$font,$ink,$col,58)
   $gh.DrawImageUnscaled($detail,$col+[int]((600-$detail.Width)/2),100)
   $py=$i*730;$gp.DrawString($v.label,$font,$ink,15,$py+8)
   $gp.DrawImage($im,[Drawing.Rectangle]::new(0,$py+45,1200,675),0,0,1920,1080,[Drawing.GraphicsUnit]::Pixel)
  } finally {$im.Dispose();$detail.Dispose()}
 }
 $gf.DrawString('原身体、制服和动作保留；仅头部重绘并统一肤色。背面原帧一只鞋末端出画。',$small,$ink,20,1120)
 $figures.Save((Join-Path $delivery 'three_angles_character_overview.png'),[Drawing.Imaging.ImageFormat]::Png)
 $heads.Save((Join-Path $delivery 'three_angles_heads_overview.png'),[Drawing.Imaging.ImageFormat]::Png)
 $frames.Save((Join-Path $delivery 'three_pv_frames_overview.png'),[Drawing.Imaging.ImageFormat]::Png)
 Write-Output 'Built full-body, head-detail and complete-PV review sheets.'
} finally {foreach($o in @($gf,$gh,$gp,$figures,$heads,$frames,$title,$font,$small,$ink)){if($o){$o.Dispose()}}}
