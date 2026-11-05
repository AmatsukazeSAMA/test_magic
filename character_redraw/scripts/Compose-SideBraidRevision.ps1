#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_braid_side_v02'
$old=[Drawing.Bitmap]::new((Join-Path $run 'inputs\previous_head.png'))
$edit=[Drawing.Bitmap]::new((Join-Path $run 'head_api_original.png'))
$base=$curl=$merged=$null
$erase=[Drawing.Drawing2D.GraphicsPath]::new()
$keep=[Drawing.Drawing2D.GraphicsPath]::new()
try {
 if($old.Width -ne 1024 -or $old.Height -ne 1024 -or $edit.Width -ne 1024 -or $edit.Height -ne 1536){throw 'Unexpected head/curl edit dimensions.'}
 $base=[Drawing.Bitmap]::new(1024,1536,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($base)
 try {$g.Clear([Drawing.Color]::Transparent);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$g.DrawImageUnscaled($old,0,0)} finally {$g.Dispose()}
 $oldPoly=@(@(641,689),@(673,716),@(686,751),@(686,802),@(690,850),@(682,890),@(667,930),@(661,958),@(646,983),@(612,1004),@(567,1004),@(563,978),@(577,958),@(566,936),@(547,909),@(535,879),@(530,850),@(534,818),@(538,798),@(527,773),@(527,744),@(539,726),@(560,710),@(587,700))
 $erase.AddPolygon([Drawing.PointF[]]@($oldPoly | ForEach-Object {[Drawing.PointF]::new($_[0],$_[1])}))
 $g=[Drawing.Graphics]::FromImage($base)
 $eraseRegion=[Drawing.Region]::new($erase)
 $eraseRegion.Intersect([Drawing.Rectangle]::new(0,722,1024,814))
 try {
  $g.SetClip($eraseRegion,[Drawing.Drawing2D.CombineMode]::Replace);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
  $b=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent)
  try {$g.FillRectangle($b,0,0,1024,1536)} finally {$b.Dispose()}
 } finally {$g.Dispose();$eraseRegion.Dispose()}
 # Hide only the original head's closed neck base before the new front curl is placed.
 # The PV's existing neck/collar will show through, while the curl remains unclipped.
 $g=[Drawing.Graphics]::FromImage($base)
 $b=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent)
 try {$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$g.FillRectangle($b,366,796,165,62)} finally {$g.Dispose();$b.Dispose()}
 $newPoly=@(@(512,754),@(700,754),@(700,1404),@(480,1404),@(480,850),@(490,850),@(512,825))
 $keep.AddPolygon([Drawing.PointF[]]@($newPoly | ForEach-Object {[Drawing.PointF]::new($_[0],$_[1])}))
 $curl=[Drawing.Bitmap]::new(1024,1536,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($curl)
 try {$g.Clear([Drawing.Color]::Transparent);$g.SetClip($keep);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$g.DrawImageUnscaled($edit,0,0)} finally {$g.Dispose()}
 $curl.Save((Join-Path $run 'isolated_new_curl_native.png'),[Drawing.Imaging.ImageFormat]::Png)
 $scale=0.70;$tx=198.0;$ty=186.2
 $angle=16.0;$rad=$angle*[Math]::PI/180.0;$cos=[Math]::Cos($rad);$sin=[Math]::Sin($rad)
 $pivotX=639.0;$pivotY=714.0
 $dx=$pivotX+$cos*($tx-$pivotX)-$sin*($ty-$pivotY)
 $dy=$pivotY+$sin*($tx-$pivotX)+$cos*($ty-$pivotY)
 $transform=[Drawing.Drawing2D.Matrix]::new([single]($scale*$cos),[single]($scale*$sin),[single](-$scale*$sin),[single]($scale*$cos),[single]$dx,[single]$dy)
 $merged=[Drawing.Bitmap]::new(1024,1536,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($merged)
 try {
  $g.Clear([Drawing.Color]::Transparent)
  $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.Transform=$transform
  $g.DrawImageUnscaled($curl,0,0)
  $g.ResetTransform()
  $g.DrawImageUnscaled($base,0,0)
 } finally {$g.Dispose();$transform.Dispose()}
 $merged.Save((Join-Path $run 'head_composite_before_palette.png'),[Drawing.Imaging.ImageFormat]::Png)
 @{method='local layer composition; previous face/eye/expression/head retained; only newly API-drawn long curl selected, uniformly scaled and inclined toward the FRONT chest';base='inputs/previous_head.png';edit_api_original='head_api_original.png';source_curl_polygon_xy=$newPoly;removed_previous_curl_polygon_xy=$oldPoly;old_curl_removal_min_y=722;base_neck_alpha_exclusion_xywh=@(366,796,165,62);curl_uniform_scale=$scale;curl_translation_before_rotation_xy=@($tx,$ty);frontward_rotation_degrees=$angle;rotation_pivot_xy=@($pivotX,$pivotY);final_affine_elements=@(($scale*$cos),($scale*$sin),(-$scale*$sin),($scale*$cos),$dx,$dy);source_edit_attachment_xy=@(630,754);registered_attachment_xy=@(639,714);output='head_composite_before_palette.png';new_face_adopted=$false;drawn_by_api=$true;software_brush_drawing=$false;user_accepted=$false} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $run 'BRAID_COMPOSITION.json') -Encoding utf8
 Write-Output 'Selected new API curl and composed it under previous head/root beads.'
} finally {$erase.Dispose();$keep.Dispose();foreach($im in @($old,$edit,$base,$curl,$merged)){if($im){$im.Dispose()}}}
