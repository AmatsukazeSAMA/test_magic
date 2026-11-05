#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
public static class PVHeadCheck {
 public static int[] Bounds(byte[] b,int w,int h,int stride) {
  int x0=w,y0=h,x1=0,y1=0,n=0;
  for(int y=0;y<h;y++)for(int x=0;x<w;x++)if(b[y*stride+x*4+3]>16){
   if(x<x0)x0=x;if(y<y0)y0=y;if(x+1>x1)x1=x+1;if(y+1>y1)y1=y+1;n++;
  }
  return new int[]{x0,y0,x1,y1,n};
 }
 public static int[] Compare(byte[] a,byte[] b,int w,int h,int stride) {
  int total=0,outside=0,below=0,shoulders=0;
  for(int y=0;y<h;y++)for(int x=0;x<w;x++){
   int i=y*stride+x*4;
   if(a[i]==b[i]&&a[i+1]==b[i+1]&&a[i+2]==b[i+2])continue;
   total++;
   bool head=(x>=792&&x<1072&&y>=78&&y<285);
   bool curl=(x>=966&&x<1018&&y>=245&&y<354);
   if(!head&&!curl)outside++;
   if(y>=354)below++;
   if(y>=285&&y<410&&!curl)shoulders++;
  }
  return new int[]{total,outside,below,shoulders};
 }
}
'@
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_pv_F002306_head_composite_v01'
$inputRun=Join-Path $root 'art\20261030_pv_F002306_v02'
[void][IO.Directory]::CreateDirectory($run)
function Pixels([Drawing.Bitmap]$im) {
 $bits=$im.LockBits([Drawing.Rectangle]::new(0,0,$im.Width,$im.Height),[Drawing.Imaging.ImageLockMode]::ReadOnly,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try {
  if($bits.Stride -lt 0){throw 'Unexpected negative PNG stride.'}
  $bytes=[byte[]]::new($bits.Stride*$im.Height)
  [Runtime.InteropServices.Marshal]::Copy($bits.Scan0,$bytes,0,$bytes.Length)
  return @{bytes=$bytes;stride=$bits.Stride}
 } finally {$im.UnlockBits($bits)}
}
function Save-Png([Drawing.Bitmap]$im,[string]$name) {$im.Save((Join-Path $run $name),[Drawing.Imaging.ImageFormat]::Png)}
function Graphics-Quality([Drawing.Graphics]$g) {
 $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
 $g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
}
$source=[Drawing.Bitmap]::new((Join-Path $inputRun 'inputs\source_F002306.png'))
$raw=[Drawing.Bitmap]::new((Join-Path $inputRun 'pv_character_highres_api_raw.png'))
$head=$plate=$layer=$composite=$fourK=$zoom=$comparison=$null
$mask=[Drawing.Drawing2D.GraphicsPath]::new()
try {
 if($source.Width -ne 1920 -or $source.Height -ne 1080){throw 'Unexpected original dimensions.'}
 if($raw.Width -ne 1536 -or $raw.Height -ne 2304){throw 'Unexpected high-resolution API dimensions.'}
 # The upper rectangle ends above the generated collar and shoulder frills.
 $mask.AddRectangle([Drawing.RectangleF]::new(400,0,700,505))
 # This second contour keeps only the long identity lock below the chin.
 # Points are in the unscaled API image, measured in its native head crop.
 $local=@(@(438,456),@(535,452),@(536,480),@(528,495),@(529,518),@(535,525),@(529,550),@(518,567),@(512,584),@(505,601),@(500,616),@(505,633),@(498,648),@(484,655),@(468,650),@(458,642),@(462,629),@(455,620),@(455,609),@(443,603),@(441,583),@(448,568),@(435,560),@(434,540),@(432,530),@(439,516),@(435,506),@(435,483))
 $points=[Drawing.PointF[]]@($local | ForEach-Object {[Drawing.PointF]::new(400+$_[0],$_[1])})
 $mask.AddPolygon($points)
 $mask.FillMode=[Drawing.Drawing2D.FillMode]::Winding
 $head=[Drawing.Bitmap]::new($raw.Width,$raw.Height,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($head)
 try {$g.Clear([Drawing.Color]::Transparent);$g.SetClip($mask);$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$g.DrawImageUnscaled($raw,0,0)} finally {$g.Dispose()}
 $p=Pixels $head
 $nativeHeadBounds=[PVHeadCheck]::Bounds($p.bytes,$head.Width,$head.Height,$p.stride)
 $headCrop=$head.Clone([Drawing.Rectangle]::new(530,40,500,640),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try {Save-Png $headCrop 'head_highres_rgba.png'} finally {$headCrop.Dispose()}
 $pink=$source.GetPixel(770,70)
 $plate=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($plate)
 try {
  $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
  $g.DrawImageUnscaled($source,0,0)
  $brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(255,$pink.R,$pink.G,$pink.B))
  try {$g.FillRectangle($brush,[Drawing.Rectangle]::new(792,78,280,201))} finally {$brush.Dispose()}
 } finally {$g.Dispose()}
 Save-Png $plate 'original_body_background_lyrics.png'
 # One uniform transform: no body warp, face stretch, or shoulder edits.
 $scale=0.44;$tx=600.4;$ty=61.48
 $layer=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($layer)
 try {
  $g.Clear([Drawing.Color]::Transparent);Graphics-Quality $g
  $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
  $g.DrawImage($head,[Drawing.RectangleF]::new($tx,$ty,$raw.Width*$scale,$raw.Height*$scale),[Drawing.RectangleF]::new(0,0,$raw.Width,$raw.Height),[Drawing.GraphicsUnit]::Pixel)
 } finally {$g.Dispose()}
 Save-Png $layer 'head_registered_1920x1080.png'
 $composite=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($composite)
 try {$g.DrawImageUnscaled($plate,0,0);$g.DrawImageUnscaled($layer,0,0)} finally {$g.Dispose()}
 Save-Png $composite 'pv_F002306_head_composited_1920x1080.png'
 $a=Pixels $source;$b=Pixels $composite
 $checks=[PVHeadCheck]::Compare($a.bytes,$b.bytes,1920,1080,$a.stride)
 if($checks[1] -ne 0 -or $checks[2] -ne 0 -or $checks[3] -ne 0){throw ('Original-body preservation failed: '+($checks -join ','))}
 $fourK=[Drawing.Bitmap]::new(3840,2160,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($fourK)
 try {
  Graphics-Quality $g
  $g.DrawImage($plate,[Drawing.Rectangle]::new(0,0,3840,2160),0,0,1920,1080,[Drawing.GraphicsUnit]::Pixel)
  $g.DrawImage($head,[Drawing.RectangleF]::new($tx*2,$ty*2,$raw.Width*$scale*2,$raw.Height*$scale*2),[Drawing.RectangleF]::new(0,0,$raw.Width,$raw.Height),[Drawing.GraphicsUnit]::Pixel)
 } finally {$g.Dispose()}
 Save-Png $fourK 'pv_F002306_head_composited_3840x2160_view.png'
 $zoom=$fourK.Clone([Drawing.Rectangle]::new(1580,140,580,620),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 Save-Png $zoom 'head_and_shoulders_preview.png'
 $comparison=[Drawing.Bitmap]::new(1240,750,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($comparison)
 $font=[Drawing.Font]::new('Microsoft YaHei',23,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
 $ink=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(50,45,47))
 try {
  $g.Clear([Drawing.Color]::FromArgb(247,243,240));Graphics-Quality $g
  $g.DrawString('原 PV · 身体与制服保留',$font,$ink,25,15)
  $g.DrawString('仅合入头脸与发型',$font,$ink,645,15)
  $g.DrawImage($source,[Drawing.Rectangle]::new(20,65,580,640),790,70,290,320,[Drawing.GraphicsUnit]::Pixel)
  $g.DrawImage($fourK,[Drawing.Rectangle]::new(640,65,580,640),1580,140,580,640,[Drawing.GraphicsUnit]::Pixel)
 } finally {$g.Dispose();$font.Dispose();$ink.Dispose()}
 Save-Png $comparison 'head_comparison.png'
 $result=@{
  status='PASS technical head-only composite; artistic candidate, not accepted';
  source_frame=2306;source_time_s=76.944;source_attachment=1;
  source_dimensions=@(1920,1080);api_dimensions=@(1536,2304);api_quality='high';api_calls_this_generation=1;
  original_source=(Join-Path $inputRun 'inputs\source_F002306.png');
  api_original=(Join-Path $inputRun 'pv_character_highres_api_raw.png');
  api_original_sha256=(Get-FileHash -LiteralPath (Join-Path $inputRun 'pv_character_highres_api_raw.png') -Algorithm SHA256).Hash.ToLowerInvariant();
  adopted_region='new head, hairstyle and one spiral lock only; original body, shoulders and uniform retained';
  old_head_cleanup_rectangle_xyxy=@(792,78,1072,279);old_head_cleanup='sampled original flat pink; not recovery of author layers';
  head_native_alpha_bbox_gt16=@($nativeHeadBounds[0],$nativeHeadBounds[1],$nativeHeadBounds[2],$nativeHeadBounds[3]);
  uniform_scale=$scale;translation_xy=@($tx,$ty);neck_anchor_raw_xy=@(765,508);neck_anchor_frame_xy=@(937,285);
  total_changed_rgb_pixels=$checks[0];changed_pixels_outside_head_and_curl_region=$checks[1];
  changed_pixels_at_or_below_y354=$checks[2];changed_shoulder_region_pixels_excluding_new_curl=$checks[3];
  output_native='pv_F002306_head_composited_1920x1080.png';
  output_view='pv_F002306_head_composited_3840x2160_view.png';
  view_resolution_note='4K viewing composite: original 1080p body, lyrics and background are resampled 2x; new head is composited directly from the new high-resolution API original, not from the 1080p merged image';
  user_accepted=$false;full_animation_validated=$false
 }
 $result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $run 'COMPOSITING_CHECK.json') -Encoding utf8
 $result | ConvertTo-Json -Depth 10
} finally {
 $mask.Dispose()
 foreach($im in @($source,$raw,$head,$plate,$layer,$composite,$fourK,$zoom,$comparison)){if($im){$im.Dispose()}}
}
