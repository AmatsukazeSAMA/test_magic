#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$utf8=[Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Drawing
if(-not ('PriorityMatte' -as [type])) {
 Add-Type -ReferencedAssemblies @('System.Drawing.Common','System.Drawing.Primitives','System.Runtime','System.Runtime.InteropServices') -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public static class PriorityMatte {
 public static void Key(Bitmap image) {
  var d=image.LockBits(new Rectangle(0,0,image.Width,image.Height),ImageLockMode.ReadWrite,PixelFormat.Format32bppArgb);
  byte[] b=new byte[d.Stride*image.Height];Marshal.Copy(d.Scan0,b,0,b.Length);
  for(int y=0;y<image.Height;y++) for(int x=0;x<image.Width;x++) {
   int i=y*d.Stride+x*4;
   double distance=Math.Sqrt(Math.Pow(b[i+2]-213,2)+Math.Pow(b[i+1]-167,2)+Math.Pow(b[i]-169,2));
   b[i+3]=(byte)(distance<15?0:distance<52?Math.Round(255*(distance-15)/37):255);
  }
  Marshal.Copy(b,0,d.Scan0,b.Length);image.UnlockBits(d);
 }
}
'@
}
$specs=@(
 @{id='ART-G17-01';frame=1501;head=@(240,25,635,450);view='front_three_quarter';ref=@(365,0,290,440);refPath=(Join-Path $base 'inputs\original_identity_turnaround.png');text='Keep the ORIGINAL extended arm reaching to IMAGE LEFT, the hand gesture, large WHITE apron ties across the back, two differently bent bare legs and original shoe positions. Keep the original shoulders and maid cap. The head looks back toward the viewer while the torso faces away. Replace the red twin-drill hairstyle with the gray bob and ONE long mint-striped corkscrew, two red beads at the visible ear on IMAGE RIGHT. Its connected coil reaches down beside the collar toward the shoulder blade, about one bob-head height below its root. The bucket is a separate compositing prop; leave the hand in its original grasp with transparent space below it.'},
 @{id='ART-G21-01';frame=1647;head=@(914,22,1728,837);view='rear_three_quarter_looking_left';ref=@(205,2,161,224);refPath=(Join-Path $root 'art\20261030_braid_revision_refs\user_side_back_hair.png');text='This is the BACK of the head, slightly turned to IMAGE LEFT. Keep the original tiny visible face sliver on IMAGE LEFT, original dark high collar and white shoulder frills. KEEP the original white ruffled MAID CAP and black ribbon on top. The new rounded gray bob must have TWO red beads and the ONE mint-striped corkscrew ROOT on IMAGE LEFT, next to that visible face/left nape; the RIGHT half of the bob and right nape have NO beads and NO drill. The spiral must be complete from those left beads through its wide upper turn, connected middle turns and tapering curled tip. Let it drape naturally down the left side of the neck/back to the shoulder. Do not turn the face toward us. Omit ALL white lettering at the left edge, including Music and MIMI.'},
 @{id='ART-G22-01';frame=1666;head=@(275,75,640,495);view='right_profile_seated';ref=@(205,2,161,224);refPath=(Join-Path $root 'art\20261030_braid_revision_refs\user_side_back_hair.png');text='Keep this exact RIGHT-facing seated profile, chin, nose and eye direction; the back remains upright, one original hand rests by the knees and the ORIGINAL crossed dangling bare legs keep both knee/ankle/shoe locations. Keep the original small white maid cap and black ribbon. The gray bob and TWO red beads sit behind the jaw on IMAGE LEFT. From those beads draw ONE COMPLETE long silver-gray/mint corkscrew hanging naturally behind the neck, visible along the back shoulder. It must NOT be a short dangling fragment: include a broad upper coil, connected middle section and tapered curled tip, totaling about one bob-head height below the bead root, around five broad turns. Keep all of it connected to its two red beads.'}
)
foreach($spec in $specs){
 $job=$plan.jobs | Where-Object id -eq $spec.id
 $run=Join-Path $base $job.run_relative
 if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'Advance to a NEW version before preparing a paid redraw.'}
 $inputs=Join-Path $run 'inputs'
 [void][IO.Directory]::CreateDirectory($inputs)
 $src=[Drawing.Bitmap]::new($job.source_image)
 $c=$job.crop_xyxy
 $crop=$src.Clone([Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]($c[2]-$c[0]),[int]($c[3]-$c[1])),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try{
  [PriorityMatte]::Key($crop)
  if($spec.frame -eq 1501){
   # Independent bucket and handle lie below the visible gripping fingers. This is alpha matting of the reference, not painting.
   $cg=[Drawing.Graphics]::FromImage($crop)
   try {
    $cg.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
    $points=@(@(620,606),@(647,605),@(669,615),@(681,631),@(690,638),@(694,656),@(713,683),@(732,712),@(744,738),@(738,763),@(708,783),@(673,796),@(639,796),@(615,785),@(594,766),@(576,744),@(562,721),@(553,699),@(556,678),@(572,663),@(589,655),@(602,649),@(612,647),@(622,646),@(633,638),@(647,632),@(661,629),@(652,618),@(639,615),@(626,616))
    $polygon=[Drawing.PointF[]]@($points | ForEach-Object {[Drawing.PointF]::new([single]($_[0]-$c[0]),[single]($_[1]-$c[1]))})
    $brush=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent)
    try{$cg.FillPolygon($brush,$polygon);$cg.FillRectangle($brush,[Drawing.Rectangle]::new([int](625-$c[0]),[int](600-$c[1]),125,195))}finally{$brush.Dispose()}
   } finally {$cg.Dispose()}
  }
  $guide=[Drawing.Bitmap]::new([int]$job.output_size[0],[int]$job.output_size[1],[Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $gg=[Drawing.Graphics]::FromImage($guide)
  try{
   $gg.Clear([Drawing.Color]::Transparent)
   $gg.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
   $reg=Get-Content -LiteralPath (Join-Path $run 'REGISTRATION_PLAN.json') -Raw|ConvertFrom-Json
   $s=$reg.source_to_guide_scale;$t=$reg.source_to_guide_translation
   $gg.DrawImage($crop,[Drawing.RectangleF]::new([single]($c[0]*$s+$t[0]),[single]($c[1]*$s+$t[1]),[single]($crop.Width*$s),[single]($crop.Height*$s)))
   $guide.Save((Join-Path $inputs 'isolated_source_character.png'),[Drawing.Imaging.ImageFormat]::Png)
   $mask=[Drawing.Bitmap]::new($guide.Width,$guide.Height,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
   $mg=[Drawing.Graphics]::FromImage($mask)
   try{
    $mg.Clear([Drawing.Color]::White)
    $mg.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
    $h=$spec.head;$clear=[Drawing.SolidBrush]::new([Drawing.Color]::Transparent)
    try {$mg.FillRectangle($clear,[Drawing.RectangleF]::new([single]($h[0]*$s+$t[0]),[single]($h[1]*$s+$t[1]),[single](($h[2]-$h[0])*$s),[single](($h[3]-$h[1])*$s)))}finally{$clear.Dispose()}
    $mask.Save((Join-Path $inputs 'head_edit_mask.png'),[Drawing.Imaging.ImageFormat]::Png)
   }finally{$mg.Dispose();$mask.Dispose()}
  }finally{$gg.Dispose();$guide.Dispose()}
 }finally{$crop.Dispose();$src.Dispose()}
 $identity=[Drawing.Bitmap]::new($spec.refPath);$r=$spec.ref
 $ref=$identity.Clone([Drawing.Rectangle]::new([int]$r[0],[int]$r[1],[int]$r[2],[int]$r[3]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try{$ref.Save((Join-Path $inputs 'view_matched_identity.png'),[Drawing.Imaging.ImageFormat]::Png)}finally{$ref.Dispose();$identity.Dispose()}
 $prompt=@"
Edit image 1, the isolated ORIGINAL PV character. Keep its body, clothes, hands, legs, proportions, pose, canvas placement and crop exactly. Only replace the red hair and face with the identity in image 2. Preserve the original white maid cap and its black ribbon. Return ONE complete transparent character cel on this same canvas, retaining all visible original limbs. The opaque mask protects the original body and transparent background; the clear region allows the complete head, hair and drill to be redrawn coherently.

$($spec.text)

Image 1 controls all pose, expression, cropping, original maid uniform, ink and flat fill style. Image 2 supplies ONLY rounded ash-gray bob construction, two red beads, complete muted-mint-striped spiral and healthy light warm peach skin. Translate its detailed design into the ORIGINAL simple PV drawing: sparse continuous dark outlines, flat solid fills, simple source-like eyes and mouth. Skin #FCE8DC, hair a flat muted ash gray, mint stripe subtle. No gradients, glossy beads, hair shine, fabric shading, detailed strands or cast shadows. Copy the ORIGINAL economical uniform folds and source eye expression. Independent props, captions and background belong to post-production and must remain transparent. Do not copy school uniform details from image 2. Maintain the same anatomical attachment, coil length and shading in adjacent cels.
"@
 [IO.File]::WriteAllText((Join-Path $run 'prompt_priority_repair.txt'),$prompt,$utf8)
 [IO.File]::WriteAllText((Join-Path $run 'PRIORITY_REPAIR.json'),(@{user_flagged_frame=$spec.frame;view=$spec.view;method='Whole transparent character API edit; isolated source reference and complete body protection mask; view-specific head identity';head_edit_source_xyxy=$spec.head;source_reference_matte='Observed uniform pink background color key; bucket alpha exclusion for F1501; source image and raw API return preserved';mask_is_advisory=$true;artistic_acceptance=$false} | ConvertTo-Json -Depth 8),$utf8)
}
Write-Output 'Prepared 3 new priority redraws; API calls 0.'
