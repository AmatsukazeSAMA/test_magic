#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string[]]$Ids,[string]$Round='pilot',[switch]$SourceOnly)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$review=Join-Path $base 'review'
[void][IO.Directory]::CreateDirectory($review)
Add-Type -AssemblyName System.Drawing
$tileW=460;$tileH=500;$columns=3
$rows=[int][Math]::Ceiling($Ids.Count/[double]$columns)
$sheet=[Drawing.Bitmap]::new($tileW*$columns,$tileH*$rows)
$g=[Drawing.Graphics]::FromImage($sheet)
$font=[Drawing.Font]::new('Arial',12)
try{
 $g.Clear([Drawing.Color]::FromArgb(235,235,235))
 $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
 for($i=0;$i -lt $Ids.Count;$i++){
  $job=$plan.jobs | Where-Object id -eq $Ids[$i]
  $run=Join-Path $base $job.run_relative
  $px=($i%$columns)*$tileW;$py=[int][Math]::Floor($i/[double]$columns)*$tileH
  $g.DrawString(($job.id+' / F'+$job.source_frame),$font,[Drawing.Brushes]::Black,$px+6,$py+4)
  $guidePath=Join-Path $run 'inputs\source_pose_guide.png'
  if(-not(Test-Path -LiteralPath $guidePath)){$guidePath=Join-Path $run 'inputs\source_character_crop.png'}
  $paths=@($guidePath)
  $original=Join-Path $run 'character_api_original.png'
  if(-not(Test-Path -LiteralPath $original)){$original=Join-Path $run 'character_api_cel.png'}
  if(-not $SourceOnly -and (Test-Path -LiteralPath $original)){
   $raw=[Drawing.Bitmap]::new($original)
   $white=[Drawing.Bitmap]::new($raw.Width,$raw.Height)
   $wg=[Drawing.Graphics]::FromImage($white)
   try{$wg.Clear([Drawing.Color]::White);$wg.DrawImageUnscaled($raw,0,0);$white.Save((Join-Path $run 'qa_white.png'),[Drawing.Imaging.ImageFormat]::Png)}finally{$wg.Dispose();$white.Dispose();$raw.Dispose()}
   $paths+=(Join-Path $run 'qa_white.png')
  }
  for($j=0;$j -lt $paths.Count;$j++){
   $im=[Drawing.Bitmap]::new($paths[$j])
   try{
    $paneW=($tileW-18)/$paths.Count
    $s=[Math]::Min(($paneW-8)/[double]$im.Width,($tileH-40)/[double]$im.Height)
    $x=$px+6+$paneW*$j+($paneW-$im.Width*$s)/2;$y=$py+28+($tileH-40-$im.Height*$s)/2
    $g.DrawImage($im,[Drawing.RectangleF]::new([single]$x,[single]$y,[single]($im.Width*$s),[single]($im.Height*$s)))
   }finally{$im.Dispose()}
  }
 }
 $suffix=if($SourceOnly){'_sources.png'}else{'_comparison.png'}
 $sheet.Save((Join-Path $review ($Round+$suffix)),[Drawing.Imaging.ImageFormat]::Png)
}finally{$font.Dispose();$g.Dispose();$sheet.Dispose()}
Write-Output (Join-Path $review ($Round+$suffix))

