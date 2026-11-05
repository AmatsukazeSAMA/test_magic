#Requires -Version 7.0
[CmdletBinding()]
param([ValidateSet('front','side','back')][string]$View='front')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -Path (Join-Path $PSScriptRoot 'PVPaletteV2.cs')
Add-Type -TypeDefinition @'
using System;
public static class PVAngleScanV2 {
 static bool InRect(int x,int y,int[] r){for(int k=0;k<r.Length;k+=4)if(x>=r[k]&&y>=r[k+1]&&x<r[k]+r[k+2]&&y<r[k+1]+r[k+3])return true;return false;}
 static bool Skin(int r,int g,int b){return (r>65&&r>g+7&&(g>b+2||(r>225&&Math.Abs(g-b)<14))&&g>r*0.55&&b>r*0.5)||(r>130&&r>g+75&&Math.Abs(g-b)<20&&g>60&&b>60);}
 public static int[] Compare(byte[] a,byte[] b,int w,int h,int stride,int[] head,int[] skin){
  int headN=0,skinN=0,bad=0,ink=0;
  for(int y=0;y<h;y++)for(int x=0;x<w;x++){
   int i=y*stride+x*4;if(a[i]==b[i]&&a[i+1]==b[i+1]&&a[i+2]==b[i+2])continue;
   if(InRect(x,y,head)){headN++;continue;}
   if(InRect(x,y,skin)&&Skin(a[i+2],a[i+1],a[i]))skinN++;else bad++;
   if(Math.Max(a[i],Math.Max(a[i+1],a[i+2]))<35)ink++;
  }
  return new int[]{headN,skinN,bad,ink};
 }
}
'@
$root=Split-Path -Parent $PSScriptRoot
$delivery=Join-Path $root 'art\20261030_pv_three_angles_v02'
$layoutPath=Join-Path $delivery ($View+'_layout.json')
$cfg=Get-Content -LiteralPath $layoutPath -Raw | ConvertFrom-Json
$run=Join-Path $delivery $View
[void][IO.Directory]::CreateDirectory($run)
$sourcePath=Join-Path $root $cfg.source
$headPath=Join-Path $root $cfg.head
function Pixels([Drawing.Bitmap]$im,[switch]$Writable) {
 $mode=if($Writable){[Drawing.Imaging.ImageLockMode]::ReadWrite}else{[Drawing.Imaging.ImageLockMode]::ReadOnly}
 $bits=$im.LockBits([Drawing.Rectangle]::new(0,0,$im.Width,$im.Height),$mode,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 if($bits.Stride -lt 0){$im.UnlockBits($bits);throw 'Negative PNG stride.'}
 $bytes=[byte[]]::new($bits.Stride*$im.Height)
 [Runtime.InteropServices.Marshal]::Copy($bits.Scan0,$bytes,0,$bytes.Length)
 if(-not $Writable){$im.UnlockBits($bits)}
 return @{bytes=$bytes;stride=$bits.Stride;bits=$bits}
}
function Save([Drawing.Bitmap]$im,[string]$name){$im.Save((Join-Path $run $name),[Drawing.Imaging.ImageFormat]::Png)}
function Quality([Drawing.Graphics]$g){$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality}
function New-HeadRegion([double]$factor=1){
 $region=[Drawing.Region]::new();$region.MakeEmpty()
 foreach($r in $cfg.head_clip_xywh){$region.Union([Drawing.RectangleF]::new($r[0]*$factor,$r[1]*$factor,$r[2]*$factor,$r[3]*$factor))}
 foreach($r in $cfg.head_clip_exclude_xywh){$region.Exclude([Drawing.RectangleF]::new($r[0]*$factor,$r[1]*$factor,$r[2]*$factor,$r[3]*$factor))}
 return $region
}
$source=[Drawing.Bitmap]::new($sourcePath)
$head=[Drawing.Bitmap]::new($headPath)
$plate=$layer=$composite=$fourK=$detail=$originalDetail=$comparison=$bg=$null
try {
 if($source.Width -ne 1920 -or $source.Height -ne 1080){throw 'Source is not a native 1920x1080 frame.'}
 $plate=$source.Clone([Drawing.Rectangle]::new(0,0,1920,1080),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $p=Pixels $plate -Writable
 $gradedSkin=0
 try {
  foreach($r in $cfg.body_skin_roi_xywh){$gradedSkin += [PVPaletteV2]::GradeSkinRect($p.bytes,1920,1080,$p.stride,$r[0],$r[1],$r[0]+$r[2],$r[1]+$r[3])}
  foreach($poly in $cfg.body_skin_polygon_xy){$xy=[int[]]@($poly | ForEach-Object {foreach($v in $_){[int]$v}});$gradedSkin += [PVPaletteV2]::GradeSkinPolygon($p.bytes,1920,1080,$p.stride,$xy)}
  [Runtime.InteropServices.Marshal]::Copy($p.bytes,0,$p.bits.Scan0,$p.bytes.Length)
 } finally {$plate.UnlockBits($p.bits)}
 $g=[Drawing.Graphics]::FromImage($plate)
 try {
  $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
  if($cfg.background_observed){
   $bg=[Drawing.Bitmap]::new((Join-Path $root $cfg.background_observed))
   foreach($r in $cfg.old_head_cleanup_xywh){$rect=[Drawing.Rectangle]::new($r[0],$r[1],$r[2],$r[3]);$g.DrawImage($bg,$rect,$rect,[Drawing.GraphicsUnit]::Pixel)}
  } else {
   $q=$cfg.flat_background_sample_xy;$pink=$source.GetPixel($q[0],$q[1])
   $brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(255,$pink.R,$pink.G,$pink.B))
   try {foreach($r in $cfg.old_head_cleanup_xywh){$g.FillRectangle($brush,[Drawing.Rectangle]::new($r[0],$r[1],$r[2],$r[3]))}} finally {$brush.Dispose()}
  }
 } finally {$g.Dispose()}
 Save $plate 'body_and_background_plate.png'
 $s=[double]$cfg.scale;$tx=[double]$cfg.translation_xy[0];$ty=[double]$cfg.translation_xy[1]
 $layer=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($layer);$clip=New-HeadRegion
 try {
  $g.Clear([Drawing.Color]::Transparent);Quality $g;$g.SetClip($clip,[Drawing.Drawing2D.CombineMode]::Replace)
  $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
  $g.DrawImage($head,[Drawing.RectangleF]::new($tx,$ty,$head.Width*$s,$head.Height*$s),[Drawing.RectangleF]::new(0,0,$head.Width,$head.Height),[Drawing.GraphicsUnit]::Pixel)
 } finally {$g.Dispose();$clip.Dispose()}
 Save $layer 'head_layer_1920x1080.png'
 $composite=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($composite)
 try {$g.DrawImageUnscaled($plate,0,0);$g.DrawImageUnscaled($layer,0,0)} finally {$g.Dispose()}
 Save $composite 'composite_1920x1080.png'
 $a=Pixels $source;$b=Pixels $composite
 $headRects=[int[]]@($cfg.head_clip_xywh | ForEach-Object {foreach($v in $_){[int]$v}})
 $skinRects=[int[]]@($cfg.body_skin_roi_xywh | ForEach-Object {foreach($v in $_){[int]$v}})
 if($cfg.body_skin_validation_extra_xywh){$skinRects += [int[]]@($cfg.body_skin_validation_extra_xywh | ForEach-Object {foreach($v in $_){[int]$v}})}
 $check=[PVAngleScanV2]::Compare($a.bytes,$b.bytes,1920,1080,$a.stride,$headRects,$skinRects)
 if($check[2] -ne 0 -or $check[3] -ne 0){throw ('Protected body/lyrics check failed: '+($check -join ','))}
 $fourK=[Drawing.Bitmap]::new(3840,2160,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($fourK);$clip=New-HeadRegion 2
 try {
  Quality $g;$g.DrawImage($plate,[Drawing.Rectangle]::new(0,0,3840,2160),0,0,1920,1080,[Drawing.GraphicsUnit]::Pixel)
  $g.SetClip($clip,[Drawing.Drawing2D.CombineMode]::Replace)
  $g.DrawImage($head,[Drawing.RectangleF]::new($tx*2,$ty*2,$head.Width*$s*2,$head.Height*$s*2),[Drawing.RectangleF]::new(0,0,$head.Width,$head.Height),[Drawing.GraphicsUnit]::Pixel)
 } finally {$g.Dispose();$clip.Dispose()}
 Save $fourK 'composite_3840x2160_view.png'
 $z=$cfg.detail_roi_xywh
 $detail=$fourK.Clone([Drawing.Rectangle]::new($z[0]*2,$z[1]*2,$z[2]*2,$z[3]*2),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 Save $detail 'head_detail.png'
 $originalDetail=[Drawing.Bitmap]::new($z[2]*2,$z[3]*2,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($originalDetail)
 try {Quality $g;$g.DrawImage($source,[Drawing.Rectangle]::new(0,0,$originalDetail.Width,$originalDetail.Height),$z[0],$z[1],$z[2],$z[3],[Drawing.GraphicsUnit]::Pixel)} finally {$g.Dispose()}
 $comparison=[Drawing.Bitmap]::new($detail.Width*2+60,$detail.Height+80,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($comparison)
 $font=[Drawing.Font]::new('Microsoft YaHei',22,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
 $ink=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(50,45,47))
 try {
  $g.Clear([Drawing.Color]::FromArgb(247,243,240));$g.DrawString(('原 PV · F'+$cfg.frame),$font,$ink,15,12);$g.DrawString(($cfg.label_zh+' · 头部合成 / 肤色统一'),$font,$ink,$detail.Width+45,12)
  $g.DrawImageUnscaled($originalDetail,15,55);$g.DrawImageUnscaled($detail,$detail.Width+45,55)
 } finally {$g.Dispose();$font.Dispose();$ink.Dispose()}
 Save $comparison 'source_comparison.png'
 $report=@{
  view=$View;frame=$cfg.frame;source_time_s=$cfg.time_s;source_attachment=1;
  source=$sourcePath;source_sha256=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant();head=$headPath;
  drawing_provider='OpenAI API';quality='high';postprocessing='explicit non-generative palette correction; user-requested warmer skin RGB 252,232,220; no new body drawing';
  head_dimensions=@($head.Width,$head.Height);source_dimensions=@(1920,1080);view_dimensions=@(3840,2160);
  head_transform=@{uniform_scale=$s;translation_xy=@($tx,$ty);mirror=$false;warp=$false};
  changed_head_region_rgb_pixels=$check[0];changed_original_body_skin_rgb_pixels=$check[1];
  unexpected_changed_pixels_outside_head_and_body_skin=$check[2];changed_original_dark_ink_pixels_outside_head=$check[3];
  original_body_structure_preserved=$true;original_uniform_preserved=$true;original_subtitles_preserved=$true;
  background_cleanup=$cfg.background_note;high_resolution_view_note='Original body, background and lyrics resampled 2x from 1080p; new head drawn directly from its 1024px API original';
  technical_pass=$true;agent_artistic_review_pending=$true;user_accepted=$false;dynamic_consistency_tested=$false
 }
 $report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $run 'COMPOSITING_CHECK.json') -Encoding utf8
 $report | ConvertTo-Json -Depth 10
} finally {foreach($im in @($source,$head,$plate,$layer,$composite,$fourK,$detail,$originalDetail,$comparison,$bg)){if($im){$im.Dispose()}}}
