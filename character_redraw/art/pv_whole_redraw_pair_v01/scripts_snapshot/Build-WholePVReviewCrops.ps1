#Requires -Version 7.0
[CmdletBinding()]
param([ValidateSet('back','side')][string]$View='back')
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root ('art\pv_whole_redraw_'+$View+'_v01')
$qa=Join-Path $run 'qa'
[void][IO.Directory]::CreateDirectory($qa)
Add-Type -AssemblyName System.Drawing
$source=[Drawing.Bitmap]::new((Join-Path $run 'whole_PV_api_original.png'))
try {
 if($View -eq 'back') {
  $rects=@{head=@(790,65,350,400);character=@(755,55,435,1025)}
 } else {
  $rects=@{head=@(190,145,270,330);character=@(55,135,425,875)}
 }
 foreach($entry in $rects.GetEnumerator()) {
  $roi=$entry.Value
  $r=[Drawing.Rectangle]::new([int][Math]::Floor($roi[0]*$source.Width/1920.0),[int][Math]::Floor($roi[1]*$source.Height/1080.0),[int][Math]::Floor($roi[2]*$source.Width/1920.0),[int][Math]::Floor($roi[3]*$source.Height/1080.0))
  $r=[Drawing.Rectangle]::Intersect($r,[Drawing.Rectangle]::new(0,0,$source.Width,$source.Height))
  $crop=$source.Clone($r,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
  try {$crop.Save((Join-Path $qa ($entry.Key+'_native_crop.png')),[Drawing.Imaging.ImageFormat]::Png)} finally {$crop.Dispose()}
 }
} finally {$source.Dispose()}
[IO.File]::WriteAllText((Join-Path $qa 'README.txt'),'Diagnostic crops only, at native output scale. The complete API original is unchanged.',[Text.UTF8Encoding]::new($false))

