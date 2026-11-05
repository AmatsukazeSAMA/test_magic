#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$folder=Join-Path $root 'art\full_character_redraw_1080p_v01\inputs'
Add-Type -AssemblyName System.Drawing
$records=@()
foreach($name in @('identity_full_drill_three_views','PV_identity_face_only','PV_face_style_no_headgear','eye_open_mono_master','eye_G02-01_F100')){
 $source=Join-Path $folder ($name+'.png');$target=Join-Path $folder ($name+'_rot180.png')
 if(-not(Test-Path -LiteralPath $source)){continue}
 if(-not(Test-Path -LiteralPath $target)){
  $im=[Drawing.Bitmap]::new($source)
  try{$im.RotateFlip([Drawing.RotateFlipType]::Rotate180FlipNone);$im.Save($target,[Drawing.Imaging.ImageFormat]::Png)}finally{$im.Dispose()}
 }
 $records+=@{source=$source;target=$target;source_sha256=(Get-FileHash -LiteralPath $source).Hash.ToLowerInvariant();target_sha256=(Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant();rotation_degrees=180;mirror=$false;art_pixels_painted=$false}
}
[IO.File]::WriteAllText((Join-Path $folder 'INVERTED_REFERENCE_PREPARATION.json'),(@{scope='Technical reference camera roll only. Anatomical-left root rotates with head; hair drape must remain natural to current source pose.';records=$records;user_accepted=$false}|ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
