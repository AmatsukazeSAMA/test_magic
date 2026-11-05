#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_pv_F002306_v01'
$source=[Drawing.Bitmap]::new((Join-Path $run 'inputs\source_F002306.png'))
$trial=[Drawing.Bitmap]::new((Join-Path $run 'pv_F002306_composited.png'))
$font=[Drawing.Font]::new('Microsoft YaHei',25,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
$small=[Drawing.Font]::new('Microsoft YaHei',18,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
$ink=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(55,48,50))
$sets=@(
 @{name='style_head_comparison.png';roi=[Drawing.Rectangle]::new(780,65,340,360);w=680;h=720;note='同一原帧位置的头部/领口局部 · 放大仅用于检查，画风以原尺寸为准'},
 @{name='style_cloth_comparison.png';roi=[Drawing.Rectangle]::new(810,420,290,430);w=464;h=688;note='围裙、袖口与衣褶局部 · 两列采用相同裁剪和缩放，不作局部对齐'}
)
try {
 foreach($s in $sets){
   $bw=$s.w*2+80;$bh=$s.h+125
   $im=[Drawing.Bitmap]::new($bw,$bh,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
   $g=[Drawing.Graphics]::FromImage($im)
   try {
     $g.Clear([Drawing.Color]::FromArgb(247,243,240))
     $g.DrawString('原 PV · F2306',$font,$ink,20,12)
     $g.DrawString('描改候选 · v01',$font,$ink,60+$s.w,12)
     $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
     $g.DrawImage($source,[Drawing.Rectangle]::new(20,60,$s.w,$s.h),$s.roi,[Drawing.GraphicsUnit]::Pixel)
     $g.DrawImage($trial,[Drawing.Rectangle]::new(60+$s.w,60,$s.w,$s.h),$s.roi,[Drawing.GraphicsUnit]::Pixel)
     $g.DrawString($s.note,$small,$ink,20,75+$s.h)
     $im.Save((Join-Path $run $s.name),[Drawing.Imaging.ImageFormat]::Png)
   } finally {$g.Dispose();$im.Dispose()}
 }
} finally {$source.Dispose();$trial.Dispose();$font.Dispose();$small.Dispose();$ink.Dispose()}
