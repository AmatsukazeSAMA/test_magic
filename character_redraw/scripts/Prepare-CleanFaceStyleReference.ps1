#Requires -Version 7.0
$ErrorActionPreference='Stop'
$base=Join-Path (Split-Path -Parent $PSScriptRoot) 'art/full_character_redraw_1080p_v01/inputs'
Add-Type -AssemblyName System.Drawing
$source=Join-Path $base 'PV_identity_face_only.png'
$target=Join-Path $base 'PV_face_style_no_headgear.png'
$image=[Drawing.Bitmap]::new($source)
try{
 $crop=$image.Clone([Drawing.Rectangle]::new(40,50,140,110),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try{$crop.Save($target,[Drawing.Imaging.ImageFormat]::Png)}finally{$crop.Dispose()}
}finally{$image.Dispose()}
$meta=@{source=$source;target=$target;crop_xywh=@(40,50,140,110);operation='Native-pixel reference crop only; no painting';reason='The previous misleadingly named face-only image still contained a maid cap and black leaf. Remove those non-source costume cues from the style reference.';scope='Economical facial ink and flat gray/peach palette only; current source controls eye opening and all costume.'}
[IO.File]::WriteAllText((Join-Path $base 'CLEAN_FACE_STYLE_REFERENCE.json'),($meta|ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
$target
