#Requires -Version 7.0
[CmdletBinding()]
param([string]$Version='composite_v01')
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw|ConvertFrom-Json
$utf8=[Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Drawing
if(-not('PrioritySourceComposite' -as [type])){
 Add-Type -ReferencedAssemblies @('System.Drawing.Common','System.Drawing.Primitives','System.Runtime','System.Runtime.InteropServices','System.Collections') -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public static class PrioritySourceComposite {
 public static byte[] Read(Bitmap im,out int stride) {
  var d=im.LockBits(new Rectangle(0,0,im.Width,im.Height),ImageLockMode.ReadOnly,PixelFormat.Format32bppArgb);
  stride=d.Stride;byte[] b=new byte[stride*im.Height];Marshal.Copy(d.Scan0,b,0,b.Length);im.UnlockBits(d);return b;
 }
 public static void Write(Bitmap im,byte[] b){var d=im.LockBits(new Rectangle(0,0,im.Width,im.Height),ImageLockMode.WriteOnly,PixelFormat.Format32bppArgb);Marshal.Copy(b,0,d.Scan0,b.Length);im.UnlockBits(d);}
 public static int Palette(Bitmap im,bool head){
  int stride;var b=Read(im,out stride);int n=0;
  for(int y=0;y<im.Height;y++)for(int x=0;x<im.Width;x++){
   int i=y*stride+x*4,r=b[i+2],g=b[i+1],bl=b[i];if(b[i+3]<245)continue;
   if(head)b[i+3]=255;
   int nr=r,ng=g,nb=bl;
   if(r>220 && r>g+7 && g>bl+2 && g>160 && bl>150){nr=252;ng=232;nb=220;}
   else if(head && r>130 && ((r>g*1.7 && r>bl*1.6 && g<130)||(r-g>30 && Math.Abs(g-bl)<10 && g<220))){nr=181;ng=28;nb=36;}
   else if(head && g>140 && g>r+5 && g>bl+4){nr=177;ng=207;nb=187;}
   else if(head && r>145 && r<245 && Math.Abs(r-g)<30 && Math.Abs(g-bl)<30){nr=184;ng=183;nb=180;}
   if(nr!=r||ng!=g||nb!=bl){b[i+2]=(byte)nr;b[i+1]=(byte)ng;b[i]=(byte)nb;n++;}
  }Write(im,b);return n;
 }
 public static void Key(Bitmap im,int x0,int y0,int x1,int y1){
  int stride;var b=Read(im,out stride);
  for(int y=0;y<im.Height;y++)for(int x=0;x<im.Width;x++){
   int i=y*stride+x*4;if(b[i+3]==0)continue;
   if(x<x0||x>=x1||y<y0||y>=y1){b[i+3]=0;continue;}
   double distance=Math.Sqrt(Math.Pow(b[i+2]-213,2)+Math.Pow(b[i+1]-167,2)+Math.Pow(b[i]-169,2));
   b[i+3]=(byte)(distance<15?0:distance<52?Math.Round(b[i+3]*(distance-15)/37):b[i+3]);
  }Write(im,b);
 }
 public static Bitmap WhiteCap(Bitmap source,int x0,int y0,int x1,int y1){
  int stride;var b=Read(source,out stride);var o=new byte[b.Length];bool[] white=new bool[source.Width*source.Height];
  for(int y=y0;y<y1;y++)for(int x=x0;x<x1;x++){int i=y*stride+x*4;white[y*source.Width+x]=Math.Min(b[i],Math.Min(b[i+1],b[i+2]))>210 && Math.Abs(b[i+2]-b[i+1])<12;}
  // Retain white components connected to the upper cap. Unrelated eye whites in the ROI are excluded.
  bool[] connected=new bool[white.Length];var queue=new System.Collections.Generic.Queue<int>();
  for(int y=y0;y<y0+(y1-y0)*.65;y++)for(int x=x0;x<x1;x++){int k=y*source.Width+x;if(white[k]){connected[k]=true;queue.Enqueue(k);}}
  while(queue.Count>0){int k=queue.Dequeue(),xx=k%source.Width,yy=k/source.Width;for(int dy=-1;dy<=1;dy++)for(int dx=-1;dx<=1;dx++){int nx=xx+dx,ny=yy+dy,nk=ny*source.Width+nx;if(nx>=x0&&nx<x1&&ny>=y0&&ny<y1&&white[nk]&&!connected[nk]){connected[nk]=true;queue.Enqueue(nk);}}}white=connected;
  for(int y=y0;y<y1;y++)for(int x=x0;x<x1;x++){
   int i=y*stride+x*4;if(b[i+2]>b[i+1]+12 && Math.Max(b[i],Math.Max(b[i+1],b[i+2]))-Math.Min(b[i],Math.Min(b[i+1],b[i+2]))>20)continue;
   bool include=false;for(int dy=-3;dy<=3&&!include;dy++)for(int dx=-3;dx<=3;dx++){int xx=x+dx,yy=y+dy;if(xx>=x0&&xx<x1&&yy>=y0&&yy<y1&&white[yy*source.Width+xx]){include=true;break;}}
   if(include){o[i]=b[i];o[i+1]=b[i+1];o[i+2]=b[i+2];o[i+3]=255;}
  }var result=new Bitmap(source.Width,source.Height,PixelFormat.Format32bppArgb);Write(result,o);return result;
 }
 public static void DarkOnly(Bitmap im){int stride;var b=Read(im,out stride);for(int y=0;y<im.Height;y++)for(int x=0;x<im.Width;x++){int i=y*stride+x*4;if(Math.Max(b[i],Math.Max(b[i+1],b[i+2]))>140)b[i+3]=0;}Write(im,b);}
 public static void FrillPalette(Bitmap im){int s;var b=Read(im,out s);for(int y=0;y<im.Height;y++)for(int x=0;x<im.Width;x++){int i=y*s+x*4;if(b[i+3]<245)continue;b[i+3]=255;if(Math.Min(b[i],Math.Min(b[i+1],b[i+2]))>150){b[i]=b[i+1]=b[i+2]=238;}}Write(im,b);}
 public static void RemoveRedRemnant(Bitmap im,bool preview){int s;var b=Read(im,out s);var original=(byte[])b.Clone();for(int y=310;y<342;y++)for(int x=384;x<412;x++){bool remnant=false;for(int yy=Math.Max(310,y-2);yy<Math.Min(342,y+3);yy++)for(int xx=Math.Max(384,x-2);xx<Math.Min(412,x+3);xx++){int j=yy*s+xx*4;if(original[j+2]>120&&original[j+1]<65&&original[j]<65)remnant=true;}if(remnant){int i=y*s+x*4;if(preview){b[i]=169;b[i+1]=167;b[i+2]=213;b[i+3]=255;}else{b[i+3]=0;}}}Write(im,b);}
 public static void RestoreCredits(Bitmap target,Bitmap source,int[] r){int s,t;var b=Read(source,out s);var o=Read(target,out t);for(int y=r[1];y<r[3];y++)for(int x=r[0];x<r[2];x++){int i=y*s+x*4;if(Math.Min(b[i],Math.Min(b[i+1],b[i+2]))>210&&Math.Max(b[i],Math.Max(b[i+1],b[i+2]))-Math.Min(b[i],Math.Min(b[i+1],b[i+2]))<18){int j=y*t+x*4;Array.Copy(b,i,o,j,4);}}Write(target,o);}
 public static int[] Bounds(Bitmap im){int s;var b=Read(im,out s);int x0=im.Width,y0=im.Height,x1=0,y1=0;for(int y=0;y<im.Height;y++)for(int x=0;x<im.Width;x++)if(b[y*s+x*4+3]>8){x0=Math.Min(x0,x);y0=Math.Min(y0,y);x1=Math.Max(x1,x+1);y1=Math.Max(y1,y+1);}return new int[]{x0,y0,x1,y1};}
}
'@
}
function Path-Of($xy){$p=[Drawing.Drawing2D.GraphicsPath]::new();$points=[Drawing.PointF[]]@($xy|ForEach-Object {[Drawing.PointF]::new([single]$_[0],[single]$_[1])});$p.AddPolygon($points);return ,$p}
function Clear-Polygon($im,$xy){$p=Path-Of $xy;$g=[Drawing.Graphics]::FromImage($im);try{$g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$brush=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent);try{$g.FillPath($brush,$p)}finally{$brush.Dispose()}}finally{$g.Dispose();$p.Dispose()}}
function Clip-Source($im,$xy){$p=Path-Of $xy;$copy=[Drawing.Bitmap]::new($im.Width,$im.Height,[Drawing.Imaging.PixelFormat]::Format32bppArgb);$g=[Drawing.Graphics]::FromImage($copy);try{$g.SetClip($p);$g.DrawImageUnscaled($im,0,0)}finally{$g.Dispose();$p.Dispose()};return ,$copy}
function Save-Image($im,$dir,$name){$im.Save((Join-Path $dir $name),[Drawing.Imaging.ImageFormat]::Png)}
$specs=@(
 @{id='ART-G17-01';scale=.40;anchor=@(416,551);target=@(421,276);headErase=@(@(240,0),@(650,0),@(650,272),@(240,272));cap=@(340,25,521,142);ears=@(@(515,57),@(535,59),@(535,95),@(550,70),@(562,72),@(564,92),@(549,117),@(526,135),@(515,120));capOffset=@(0,0);collar=@(@(400,264),@(437,262),@(441,291),@(417,302),@(393,283))},
 @{id='ART-G21-01';scale=1.18;anchor=@(459,552);target=@(1306,710);headErase=@(@(914,0),@(1735,0),@(1735,700),@(1370,700),@(1257,714),@(1230,687),@(1160,690),@(1110,676),@(1070,716),@(914,716));cap=@(1090,28,1435,252);ears=@(@(1230,87),@(1246,84),@(1292,169),@(1303,126),@(1326,67),@(1344,68),@(1350,127),@(1345,190),@(1326,235),@(1310,254),@(1277,246),@(1241,189));capOffset=@(0,0);collar=@(@(1186,699),@(1362,692),@(1380,766),@(1455,799),@(1421,868),@(1230,838),@(1176,788))},
 @{id='ART-G22-01';scale=.45;anchor=@(435,536);target=@(483,330);headErase=@(@(285,70),@(640,70),@(640,325),@(390,325),@(390,365),@(290,365));cap=@(388,89,452,177);ears=@(@(328,129),@(342,132),@(369,176),@(381,129),@(397,125),@(401,151),@(392,186),@(372,211),@(351,201),@(335,173));capOffset=@(45,0);collar=@(@(428,321),@(478,317),@(497,343),@(493,368),@(451,359),@(424,337))}
)
foreach($spec in $specs){
 $job=$plan.jobs|Where-Object id -eq $spec.id;$parent=Join-Path $base $job.run_relative;$run=Join-Path $parent $Version
 [void][IO.Directory]::CreateDirectory($run)
 $source=[Drawing.Bitmap]::new($job.source_image)
 $body=$source.Clone([Drawing.Rectangle]::new(0,0,1920,1080),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $head=[Drawing.Bitmap]::new((Join-Path $parent 'head_only_v01\head_api_original.png'))
 $c=$job.crop_xyxy;[PrioritySourceComposite]::Key($body,$c[0],$c[1],$c[2],$c[3])
 Clear-Polygon $body $spec.headErase
 if($job.source_frame -eq 1647){Clear-Polygon $body @(@(914,714),@(975,714),@(975,737),@(914,737));Clear-Polygon $body @(@(975,714),@(989,714),@(989,735),@(975,735));Clear-Polygon $body @(@(1045,670),@(1160,670),@(1160,724),@(1045,724))}
 if($job.source_frame -eq 1666){[PrioritySourceComposite]::RemoveRedRemnant($body,$false)}
 if($job.source_frame -eq 1501){
  Clear-Polygon $body @(@(620,606),@(647,605),@(669,615),@(681,631),@(690,638),@(694,656),@(713,683),@(732,712),@(744,738),@(738,763),@(708,783),@(673,796),@(639,796),@(615,785),@(594,766),@(576,744),@(562,721),@(553,699),@(556,678),@(572,663),@(589,655),@(602,649),@(612,647),@(622,646),@(633,638),@(647,632),@(661,629),@(652,618),@(639,615),@(626,616))
  Clear-Polygon $body @(@(625,600),@(750,600),@(750,795),@(625,795))
 }
 $bodyColors=[PrioritySourceComposite]::Palette($body,$false)
 $headColors=[PrioritySourceComposite]::Palette($head,$true)
 $cap=[PrioritySourceComposite]::WhiteCap($source,$spec.cap[0],$spec.cap[1],$spec.cap[2],$spec.cap[3])
 $ears=Clip-Source $source $spec.ears;[PrioritySourceComposite]::DarkOnly($ears)
 $collar=Clip-Source $source $spec.collar;[PrioritySourceComposite]::Key($collar,0,0,1920,1080);[void][PrioritySourceComposite]::Palette($collar,$false)
 if($job.source_frame -ne 1501){[PrioritySourceComposite]::DarkOnly($collar)}
 if($job.source_frame -eq 1647){
  $frillPath=Join-Path $base 'repairs\F1647_shoulder_v01\shoulder_api_original.png';$frill=[Drawing.Bitmap]::new($frillPath);[PrioritySourceComposite]::FrillPalette($frill)
  $fg=[Drawing.Graphics]::FromImage($body)
  try{$fg.SetClip([Drawing.Rectangle]::new(938,754,65,90));$fg.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy;$fg.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$fg.DrawImage($frill,[Drawing.RectangleF]::new([single]929.64,[single]717.142857,[single]($frill.Width/2.8),[single]($frill.Height/2.8)))}finally{$fg.Dispose();$frill.Dispose()}
 }
 $registered=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($registered)
 $s=$spec.scale;$tx=$spec.target[0]-$spec.anchor[0]*$s;$ty=$spec.target[1]-$spec.anchor[1]*$s
 try{$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality;$g.DrawImage($head,[Drawing.RectangleF]::new([single]$tx,[single]$ty,[single]($head.Width*$s),[single]($head.Height*$s)))}finally{$g.Dispose()}
 $character=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb);$g=[Drawing.Graphics]::FromImage($character)
 try{$g.DrawImageUnscaled($body,0,0);$g.DrawImageUnscaled($registered,0,0);$g.DrawImageUnscaled($collar,0,0);$g.DrawImageUnscaled($cap,[int]$spec.capOffset[0],[int]$spec.capOffset[1]);$g.DrawImageUnscaled($ears,[int]$spec.capOffset[0],[int]$spec.capOffset[1])}finally{$g.Dispose()}
 Save-Image $body $run 'original_body_rgba.png';Save-Image $registered $run 'API_head_registered_rgba.png';Save-Image $cap $run 'original_cap_rgba.png';Save-Image $ears $run 'original_ribbon_rgba.png';Save-Image $head $run 'head_palette_matched.png';Save-Image $character $run 'character_1920x1080.png'
 $bounds=[PrioritySourceComposite]::Bounds($character);$x0=[Math]::Max(0,$bounds[0]-12);$y0=[Math]::Max(0,$bounds[1]-12);$x1=[Math]::Min(1920,$bounds[2]+12);$y1=[Math]::Min(1080,$bounds[3]+12)
 $compact=$character.Clone([Drawing.Rectangle]::new($x0,$y0,$x1-$x0,$y1-$y0),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 Save-Image $compact $run 'character_compact.png';$compact.Dispose()
 $white=[Drawing.Bitmap]::new(1920,1080);$g=[Drawing.Graphics]::FromImage($white);try{$g.Clear([Drawing.Color]::White);$g.DrawImageUnscaled($character,0,0)}finally{$g.Dispose()};Save-Image $white $run 'qa_white.png';$white.Dispose()
 $preview=$source.Clone([Drawing.Rectangle]::new(0,0,1920,1080),[Drawing.Imaging.PixelFormat]::Format32bppArgb);$g=[Drawing.Graphics]::FromImage($preview);$p=Path-Of $spec.headErase
 try{$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(213,167,169));try{$g.FillPath($brush,$p);if($job.source_frame -eq 1647){$g.FillRectangle($brush,1045,670,115,54)}}finally{$brush.Dispose()}}finally{$p.Dispose();$g.Dispose()}
 if($job.source_frame -eq 1666){[PrioritySourceComposite]::RemoveRedRemnant($preview,$true)}
 $g=[Drawing.Graphics]::FromImage($preview);try{$g.DrawImageUnscaled($character,0,0)}finally{$g.Dispose()}
 if($job.source_frame -eq 1647){[PrioritySourceComposite]::RestoreCredits($preview,$source,@(915,160,987,830))}
 Save-Image $preview $run ('PV_F'+$job.source_frame+'_1920x1080.png')
 $record=@{id=$job.id;source_frame=$job.source_frame;source_pts=$job.source_pts;source_image=$job.source_image;source_sha256=$job.source_image_sha256;source_role='Each actual original source body/costume; no common frozen body';api_head_original=(Join-Path $parent 'head_only_v01\head_api_original.png');api_head_sha256=(Get-FileHash -LiteralPath (Join-Path $parent 'head_only_v01\head_api_original.png')).Hash.ToLowerInvariant();api_model='gpt-image-2.5-sunburst';api_quality='high';head_uniform_scale=$s;translation_xy=@($tx,$ty);measured_head_neck_anchor=$spec.anchor;frame_neck_anchor=$spec.target;source_cap_translation=$spec.capOffset;body_skin_color_graded_pixels=$bodyColors;head_flat_palette_color_graded_pixels=$headColors;palette_note='Post-compositing flat color grading and near-opaque matte normalization; raw API output preserved. No head or drill contours painted by code.';character_output='character_1920x1080.png';compact_output='character_compact.png';compact_frame_translation=@($x0,$y0);compact_dimensions=@(($x1-$x0),($y1-$y0));preview=('PV_F'+$job.source_frame+'_1920x1080.png');subtitles_and_props='Original PV observed pixels retained in the preview; not API generated. Character layer excludes lettering and independent bucket.';body_matte='Technical observed-background color key and source-region clipping, not author clean alpha';shoulder_contour_repair=$(if($job.source_frame -eq 1647){@{api='repairs/F1647_shoulder_v01/shoulder_api_original.png';adopted_frame_rectangle=@(938,754,1003,844);role='Small API shoulder-outline inference underneath source subtitle I; not original author hidden pixels'}}else{$null});artistic_review='pending';user_accepted=$false;dynamic_validated=$false}
 [IO.File]::WriteAllText((Join-Path $run 'COMPOSITE.json'),($record|ConvertTo-Json -Depth 12),$utf8)
 foreach($im in @($source,$body,$head,$cap,$ears,$collar,$registered,$character,$preview)){$im.Dispose()}
 Write-Output (Join-Path $run $record.preview)
}
