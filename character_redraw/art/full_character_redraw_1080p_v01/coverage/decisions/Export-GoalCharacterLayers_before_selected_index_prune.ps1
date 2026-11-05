#Requires -Version 7.0
[CmdletBinding()]
param([string[]]$Ids)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$registry=Get-Content -LiteralPath (Join-Path $base 'ASSET_REGISTRY.json') -Raw|ConvertFrom-Json -AsHashtable
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw|ConvertFrom-Json
$priority=Get-Content -LiteralPath (Join-Path $base 'whole_character_restart_v01\delivery\INDEX.json') -Raw|ConvertFrom-Json
$out=Join-Path $base 'delivery_1080p_v01'
$adjustmentFile=Join-Path $base 'review/WHOLE_SPRITE_PLACEMENT_ADJUSTMENTS.json'
$adjustments=if(Test-Path -LiteralPath $adjustmentFile){Get-Content -LiteralPath $adjustmentFile -Raw|ConvertFrom-Json -AsHashtable}else{@{}}
[void][IO.Directory]::CreateDirectory($out)
$utf8=[Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Drawing
$records=@()
foreach($id in @($registry.Keys|Sort-Object)){
 if($Ids -and $id -notin $Ids){continue}
 $asset=$registry[$id]
 if(-not $asset.primary_static_pass -or -not $asset.independent_static_pass){continue}
 if($asset.requires_whole_imggen -and -not $asset.whole_imggen_completed){throw 'Patched candidate cannot be exported.'}
 $job=$plan.jobs|Where-Object id -eq $id
 $sourceReference=if($job.production_reference){$job.production_reference}else{$job}
 $image=$asset.image
 $hash=(Get-FileHash -LiteralPath $image).Hash.ToLowerInvariant()
 if($hash -ne $asset.sha256){throw 'Selected image changed after review.'}
 $folder=Join-Path $out ($id+'\'+$hash.Substring(0,12))
 [void][IO.Directory]::CreateDirectory($folder)
 $raw=[Drawing.Bitmap]::new($image)
 $frame=[Drawing.Bitmap]::new(1920,1080,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($frame)
 try{
  $g.Clear([Drawing.Color]::Transparent)
  $run=[IO.DirectoryInfo]::new($asset.selected_run)
  while($run -and -not(Test-Path -LiteralPath (Join-Path $run.FullName 'REGISTRATION_PLAN.json'))){$run=$run.Parent}
  if($run){
   $reg=Get-Content -LiteralPath (Join-Path $run.FullName 'REGISTRATION_PLAN.json') -Raw|ConvertFrom-Json
   # A selected older version can still use its own recorded source; never
   # describe its placement using a newer plan reference it did not consume.
   if($reg.source_image){$sourceReference=$reg}
   elseif(Test-Path -LiteralPath (Join-Path $run.FullName 'JOB.json')){
    $registeredJob=Get-Content -LiteralPath (Join-Path $run.FullName 'JOB.json') -Raw|ConvertFrom-Json
    $sourceReference=if($registeredJob.production_reference){$registeredJob.production_reference}else{$registeredJob}
   }
   $fit=[Math]::Min($reg.guide_dimensions[0]/[double]$raw.Width,$reg.guide_dimensions[1]/[double]$raw.Height)
   $ox=($reg.guide_dimensions[0]-$raw.Width*$fit)/2
   $oy=($reg.guide_dimensions[1]-$raw.Height*$fit)/2
   $scale=$fit/$reg.source_to_guide_scale
   $tx=($ox-$reg.source_to_guide_translation[0])/$reg.source_to_guide_scale
   $ty=($oy-$reg.source_to_guide_translation[1])/$reg.source_to_guide_scale
   $method='Uniform whole-sprite fit through original source-to-guide transform; provisional until actual placement review.'
  }elseif($id -eq 'ART-G33-01'){
   # The first pilot predates REGISTRATION_PLAN. Its source crop is documented
   # in Prepare-CharacterPilot.ps1 and PROJECT_SCOPE.json, not the later plan.
   $scale=1000.0/$raw.Height
   $tx=942.5-$raw.Width*$scale/2;$ty=48.0
   $method='Documented legacy pilot source crop (750,48,385,1000), whole sprite height fit and center; provisional placement.'
  }else{
   $pre=$priority.records|Where-Object id -eq $id
   if(-not $pre){throw ('No source registration or reviewed priority placement found for '+$id)}
   $scale=$pre.whole_sprite_uniform_scale;$tx=$pre.whole_sprite_translation[0];$ty=$pre.whole_sprite_translation[1]
   $method=$pre.layout_method
  }
  $appliedAdjustment=$null
  if($adjustments.ContainsKey($id)){
   $appliedAdjustment=$adjustments[$id]
   if($appliedAdjustment.image_sha256 -ne $hash){throw ('Placement adjustment belongs to another artwork: '+$id)}
   $factor=[double]$appliedAdjustment.scale_multiplier
   $pivot=$appliedAdjustment.pivot_canvas
   $tx=$pivot[0]+($tx-$pivot[0])*$factor+$appliedAdjustment.translation_after[0]
   $ty=$pivot[1]+($ty-$pivot[1])*$factor+$appliedAdjustment.translation_after[1]
   $scale*=$factor
   $folder=Join-Path $folder $appliedAdjustment.version
   [void][IO.Directory]::CreateDirectory($folder)
   $method+=' Actual source comparison prompted a documented uniform whole-sprite scale/translation; no partwise changes.'
  }
  $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.DrawImage($raw,[Drawing.RectangleF]::new([single]$tx,[single]$ty,[single]($raw.Width*$scale),[single]($raw.Height*$scale)))
  $target=Join-Path $folder 'character_1920x1080.png'
  $frame.Save($target,[Drawing.Imaging.ImageFormat]::Png)
 }finally{$g.Dispose();$raw.Dispose()}
 $pink=[Drawing.Bitmap]::new(1920,1080);$pg=[Drawing.Graphics]::FromImage($pink)
 try{
  $pg.Clear([Drawing.Color]::FromArgb(213,167,169));$pg.DrawImageUnscaled($frame,0,0)
  $preview=Join-Path $folder 'position_preview.png';$pink.Save($preview,[Drawing.Imaging.ImageFormat]::Png)
  $source=[Drawing.Bitmap]::new($sourceReference.source_image)
  $comparison=[Drawing.Bitmap]::new(1920,580);$cg=[Drawing.Graphics]::FromImage($comparison);$font=[Drawing.Font]::new('Arial',14)
  try{
   $cg.Clear([Drawing.Color]::White)
   $cg.DrawString(($id+' / F'+$sourceReference.source_frame+' SOURCE'),$font,[Drawing.Brushes]::Black,8,5)
   $cg.DrawString('CHARACTER ONLY / PROVISIONAL PLACEMENT',$font,[Drawing.Brushes]::Black,968,5)
   $cg.DrawImage($source,[Drawing.Rectangle]::new(0,40,960,540))
   $cg.DrawImage($pink,[Drawing.Rectangle]::new(960,40,960,540))
   $comparison.Save((Join-Path $folder 'source_comparison.png'),[Drawing.Imaging.ImageFormat]::Png)
  }finally{$source.Dispose();$cg.Dispose();$comparison.Dispose();$font.Dispose()}
 }finally{$pg.Dispose();$pink.Dispose();$frame.Dispose()}
 $record=@{id=$id;source_frame=$sourceReference.source_frame;source_pts=$sourceReference.source_pts;source_image=$sourceReference.source_image;canonical_source_frame=$job.source_frame;canonical_source_image=$job.source_image;image=$image;image_sha256=$hash;layer_1080=$target;layer_sha256=(Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant();preview=$preview;source_comparison=(Join-Path $folder 'source_comparison.png');whole_sprite_scale=$scale;whole_sprite_translation=@($tx,$ty);placement_method=$method;placement_adjustment=$appliedAdjustment;placement_visual_review='pending';dimensions=@(1920,1080);whole_character_pixels_only=$true;partwise_warp_or_separate_head_fusion=$false;source_scene_composited=$false;dynamic_review=$false;user_accepted=$false}
 [IO.File]::WriteAllText((Join-Path $folder 'PLACEMENT.json'),($record|ConvertTo-Json -Depth 10),$utf8)
 $records+=$record
}
$indexPath=Join-Path $out 'INDEX.json'
if($Ids -and (Test-Path -LiteralPath $indexPath)){
 $existing=Get-Content -LiteralPath $indexPath -Raw|ConvertFrom-Json
 $records=@($existing.records|Where-Object {$_.id -notin $Ids})+@($records)
}
[IO.File]::WriteAllText($indexPath,(@{records=$records;scope='Staging export of independently reviewed static candidates, not complete film delivery';whole_film_complete=$false;user_accepted=$false}|ConvertTo-Json -Depth 15),$utf8)
[PSCustomObject]@{exported=$records.Count;directory=$out;placement_reviews='pending';whole_film_complete=$false}
