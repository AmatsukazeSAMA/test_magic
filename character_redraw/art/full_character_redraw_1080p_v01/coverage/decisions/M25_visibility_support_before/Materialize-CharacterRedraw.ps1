#Requires -Version 7.0
[CmdletBinding()]
param([string[]]$Ids)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$jobs=@($plan.jobs | Where-Object {-not $Ids -or $_.id -in $Ids})
$utf8=[Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Drawing
foreach($job in $jobs){
 $run=Join-Path $base $job.run_relative
 if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){continue}
 $inputs=Join-Path $run 'inputs'
 [void][IO.Directory]::CreateDirectory($inputs)
 if((Get-FileHash -LiteralPath $job.source_image -Algorithm SHA256).Hash.ToLowerInvariant() -ne $job.source_image_sha256){throw "Source changed: $($job.id)"}
 $source=[Drawing.Bitmap]::new($job.source_image)
 try{
  $c=$job.crop_xyxy
  $rect=[Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]($c[2]-$c[0]),[int]($c[3]-$c[1]))
  $crop=$source.Clone($rect,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
  try{
   $crop.Save((Join-Path $inputs 'source_character_crop.png'),[Drawing.Imaging.ImageFormat]::Png)
   $w=[int]$job.output_size[0];$h=[int]$job.output_size[1]
   $guide=[Drawing.Bitmap]::new($w,$h,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
   $g=[Drawing.Graphics]::FromImage($guide)
   try{
    $g.Clear([Drawing.Color]::FromArgb(255,213,167,169))
    $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $s=[Math]::Min(($w-24)/[double]$crop.Width,($h-24)/[double]$crop.Height)
    $dx=($w-$crop.Width*$s)/2;$dy=($h-$crop.Height*$s)/2
    $g.DrawImage($crop,[Drawing.RectangleF]::new([single]$dx,[single]$dy,[single]($crop.Width*$s),[single]($crop.Height*$s)))
    $guide.Save((Join-Path $inputs 'source_pose_guide.png'),[Drawing.Imaging.ImageFormat]::Png)
    $registration=@{source_to_guide_scale=$s;source_to_guide_translation=@(($dx-$c[0]*$s),($dy-$c[1]*$s));guide_dimensions=@($w,$h);note='Reference preparation only. Actual API output alignment requires review; these are not measured output anchors.'}
    [IO.File]::WriteAllText((Join-Path $run 'REGISTRATION_PLAN.json'),($registration | ConvertTo-Json -Depth 10),$utf8)
   }finally{$g.Dispose();$guide.Dispose()}
  }finally{$crop.Dispose()}
 }finally{$source.Dispose()}
 [IO.File]::WriteAllText((Join-Path $run 'JOB.json'),($job | ConvertTo-Json -Depth 15),$utf8)
}
[PSCustomObject]@{planned=$jobs.Count;prepared_references=$true;api_calls=0}

