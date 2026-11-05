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
 try {
  $g.SetClip($erase);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
  $b=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent)
  try {$g.FillRectangle($b,0,0,1024,1536)} finally {$b.Dispose()}
 } finally {$g.Dispose()}
 $newPoly=@(@(566,726),@(646,715),@(678,741),@(690,785),@(695,830),@(688,867),@(659,906),@(635,930),@(668,956),@(685,990),@(688,1035),@(672,1085),@(637,1125),@(656,1159),@(671,1192),@(668,1239),@(645,1277),@(614,1316),@(599,1342),@(575,1366),@(529,1385),@(523,1370),@(543,1352),@(549,1328),@(535,1307),@(509,1283),@(500,1251),@(504,1215),@(516,1182),@(547,1148),@(564,1127),@(529,1109),@(507,1081),@(501,1045),@(505,1009),@(517,980),@(546,957),@(514,934),@(495,902),@(493,870),@(498,835),@(513,798),@(535,766))
 $keep.AddPolygon([Drawing.PointF[]]@($newPoly | ForEach-Object {[Drawing.PointF]::new($_[0],$_[1])}))
 $curl=[Drawing.Bitmap]::new(1024,1536,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($curl)
 try {$g.Clear([Drawing.Color]::Transparent);$g.SetClip($keep);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$g.DrawImageUnscaled($edit,0,0)} finally {$g.Dispose()}
 $curl.Save((Join-Path $run 'isolated_new_curl_native.png'),[Drawing.Imaging.ImageFormat]::Png)
 $scale=0.70;$tx=186.5;$ty=197.3
 $merged=[Drawing.Bitmap]::new(1024,1536,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($merged)
 try {
  $g.Clear([Drawing.Color]::Transparent)
  $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.DrawImage($curl,[Drawing.RectangleF]::new($tx,$ty,1024*$scale,1536*$scale),[Drawing.RectangleF]::new(0,0,1024,1536),[Drawing.GraphicsUnit]::Pixel)
  $g.DrawImageUnscaled($base,0,0)
 } finally {$g.Dispose()}
 $merged.Save((Join-Path $run 'head_composite_before_palette.png'),[Drawing.Imaging.ImageFormat]::Png)
 @{method='local layer composition; previous face/eye/expression/head retained; only newly API-drawn long curl selected and uniformly scaled';base='inputs/previous_head.png';edit_api_original='head_api_original.png';source_curl_polygon_xy=$newPoly;removed_previous_curl_polygon_xy=$oldPoly;curl_uniform_scale=$scale;curl_translation_xy=@($tx,$ty);source_edit_root_anchor_xy=@(625,721);target_old_root_anchor_xy=@(624,702);output='head_composite_before_palette.png';new_face_adopted=$false;drawn_by_api=$true;software_brush_drawing=$false;user_accepted=$false} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $run 'BRAID_COMPOSITION.json') -Encoding utf8
 Write-Output 'Selected new API curl and composed it under previous head/root beads.'
} finally {$erase.Dispose();$keep.Dispose();foreach($im in @($old,$edit,$base,$curl,$merged)){if($im){$im.Dispose()}}}
