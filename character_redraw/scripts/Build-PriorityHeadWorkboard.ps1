#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw|ConvertFrom-Json
$specs=@(@('ART-G17-01',0,0,500,420),@('ART-G21-01',0,0,848,950),@('ART-G22-01',190,80,340,400))
$font=[Drawing.Font]::new('Arial',11)
$pen=[Drawing.Pen]::new([Drawing.Color]::FromArgb(100,10,80,200),1)
try{
 foreach($spec in $specs){
  $job=$plan.jobs|Where-Object id -eq $spec[0];$run=Join-Path $base $job.run_relative
  $im=[Drawing.Bitmap]::new((Join-Path $run 'qa_white.png'))
  $crop=$im.Clone([Drawing.Rectangle]::new([int]$spec[1],[int]$spec[2],[int]$spec[3],[int]$spec[4]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g=[Drawing.Graphics]::FromImage($crop)
  try{
   for($x=50;$x -lt $im.Width;$x+=50){$px=$x-$spec[1];if($px -ge 0 -and $px -lt $crop.Width){$g.DrawLine($pen,$px,0,$px,$crop.Height);$g.DrawString([string]$x,$font,[Drawing.Brushes]::Blue,$px+2,2)}}
   for($y=50;$y -lt $im.Height;$y+=50){$py=$y-$spec[2];if($py -ge 0 -and $py -lt $crop.Height){$g.DrawLine($pen,0,$py,$crop.Width,$py);$g.DrawString([string]$y,$font,[Drawing.Brushes]::Blue,2,$py+2)}}
   $crop.Save((Join-Path $base ('review\'+$job.id+'_head_coordinates.png')),[Drawing.Imaging.ImageFormat]::Png)
  }finally{$g.Dispose();$crop.Dispose();$im.Dispose()}
 }
}finally{$pen.Dispose();$font.Dispose()}
