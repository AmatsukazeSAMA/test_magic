#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string[]]$Ids,[Parameter(Mandatory)][string]$Batch,[switch]$Preview,[switch]$SplitOnly)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$jobs=@($Ids | ForEach-Object {$id=$_;$plan.jobs | Where-Object id -eq $id})
if($jobs.Count -ne $Ids.Count -or $jobs.Count -lt 2 -or $jobs.Count -gt 3){throw 'Use two or three valid drawing IDs.'}
if(@($jobs.group | Sort-Object -Unique).Count -ne 1){throw 'A sheet must contain consecutive cels from one action group.'}
for($i=1;$i -lt $jobs.Count;$i++){if($jobs[$i].family_order -ne $jobs[$i-1].family_order+1){throw 'Cels must be consecutive in original source order.'}}
$run=Join-Path $base ('batches\'+$Batch)
$utf8=[Text.UTF8Encoding]::new($false)
function SaveJson([string]$p,$v){[IO.File]::WriteAllText($p,($v | ConvertTo-Json -Depth 30),$utf8)}
Add-Type -AssemblyName System.Drawing
if(-not $SplitOnly){
 if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'Batch attempt already recorded. Recover stored response if appropriate; do not resubmit.'}
 foreach($job in $jobs){$celRun=Join-Path $base $job.run_relative;if(Test-Path -LiteralPath (Join-Path $celRun 'attempt.json')){throw 'A selected cel already has an API attempt.'}}
 [void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
 $draft=& (Join-Path $PSScriptRoot 'Invoke-CharacterRedraw.ps1') -Id $Ids[0] -BuildOnly
 $cw=[int](($jobs | ForEach-Object {$_.output_size[0]} | Measure-Object -Maximum).Maximum)
 $ch=[int](($jobs | ForEach-Object {$_.output_size[1]} | Measure-Object -Maximum).Maximum)
 $n=$jobs.Count
 $options=@(@{cols=$n;rows=1;w=$cw*$n;h=$ch},@{cols=1;rows=$n;w=$cw;h=$ch*$n})
 $packing=$options | Where-Object {$_.w -le 3840 -and $_.h -le 3840 -and $_.w*$_.h -le 3686400 -and [Math]::Max($_.w/[double]$_.h,$_.h/[double]$_.w) -le 3} | Select-Object -First 1
 if(-not $packing){throw 'These source-resolution cels do not fit a non-experimental shared canvas. Use fewer cels or individual API calls.'}
 $sheet=[Drawing.Bitmap]::new([int]$packing.w,[int]$packing.h,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $g=[Drawing.Graphics]::FromImage($sheet)
 $cells=@()
 try{
  $g.Clear([Drawing.Color]::FromArgb(255,213,167,169))
  for($i=0;$i -lt $n;$i++){
   $job=$jobs[$i];$celRun=Join-Path $base $job.run_relative
   $x=($i%$packing.cols)*$cw;$y=[int][Math]::Floor($i/[double]$packing.cols)*$ch
   $guide=[Drawing.Bitmap]::new((Join-Path $celRun 'inputs\source_pose_guide.png'))
   $dx=[int][Math]::Floor(($cw-$guide.Width)/2.0);$dy=[int][Math]::Floor(($ch-$guide.Height)/2.0)
   try{$g.DrawImageUnscaled($guide,($x+$dx),($y+$dy))}finally{$guide.Dispose()}
   $cells+=@{id=$job.id;run_relative=$job.run_relative;source_frame=$job.source_frame;rect_xywh=@($x,$y,$cw,$ch);guide_offset_xy=@($dx,$dy);original_guide_size=$job.output_size}
  }
  $sheet.Save((Join-Path $run 'inputs\source_pose_sheet.png'),[Drawing.Imaging.ImageFormat]::Png)
 }finally{$g.Dispose();$sheet.Dispose()}
 $references=@((Join-Path $run 'inputs\source_pose_sheet.png'))+@($draft.images | Select-Object -Skip 1)
 if($jobs[0].group -in @('G06','G07')){
  for($index=1;$index -le 2;$index++){
   $ref=[Drawing.Bitmap]::new($references[$index])
   $target=Join-Path $run ('inputs\rotated_identity_'+$index+'.png')
   try{$ref.RotateFlip([Drawing.RotateFlipType]::Rotate180FlipNone);$ref.Save($target,[Drawing.Imaging.ImageFormat]::Png)}finally{$ref.Dispose()}
   $references[$index]=$target
  }
 }
 $layout=if($packing.cols -gt 1){'LEFT TO RIGHT in separate columns'}else{'TOP TO BOTTOM in separate rows'}
 $cellDescription=($cells | ForEach-Object {$_.id+' F'+$_.source_frame+' at ['+($_.rect_xywh -join ',')+']'}) -join '; '
 $prompt=@"
Create a PRODUCTION CEL SHEET containing exactly $n DIFFERENT ADJACENT ANIMATION DRAWINGS of the same character, $layout. The first reference shows the exact pose and position for each cell. The complete canvas is $($packing.w)x$($packing.h); each independent cell is $($cw)x$($ch). Cell map: $cellDescription. Redraw EACH corresponding character pose. These are successive times, not interacting people. Do not combine poses, omit a cell, repeat the same pose, swap cells, cross cell boundaries or add other figures. Keep every source eye/hand/arm/foot difference that distinguishes these drawings. Maintain the SAME bob shape, two bead attachment, drill length, coil direction, palette and line density across these adjacent cels. Each cell's unused pixels must be genuinely transparent, with no panel border, label, lettering, background, checkerboard or shadow. The shared canvas only packs character pixels; it is not a new scene or illustration.

For each cell apply the following character-only drawing constraints. References 2 onwards keep their stated roles. Here reference 1 means the corresponding cell in the SOURCE POSE SHEET, rather than a single pose.

$($draft.prompt)

FINAL SHEET REQUIREMENT: EXACTLY $n independently posed character cels in the specified cells, all different according to reference 1, on genuine transparent alpha. Draw only characters, without typography, effects or separate props. No new camera framing. Preserve each source cell's pose placement. Do not draw panel dividers.
"@
 if($jobs[0].group -in @('G06','G07')){$prompt+="`nThe two face references are intentionally rotated to the same UPSIDE-DOWN head orientation as these original poses. The bead/drill root belongs on IMAGE LEFT of the upside-down frontal face, matching the rotated anatomical-left identity. Do not place it on fixed image right. Gray casual clothing, no maid uniform/headband. The independent round disc must remain transparent in this layer except for visible overlying fingers.`n"}
 [IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,$utf8)
 SaveJson (Join-Path $run 'SHEET_MANIFEST.json') @{group=$jobs[0].group;cells=$cells;size=@($packing.w,$packing.h);references=$references;quality='high';post_generation_operation='Lossless rectangular pixel extraction only; full API sheet retained';user_accepted=$false}
 if($Preview){[PSCustomObject]@{size=($packing.w.ToString()+'x'+$packing.h);ids=$Ids;source_sheet=(Join-Path $run 'inputs\source_pose_sheet.png');submitted=$false};return}
 foreach($cell in $cells){SaveJson (Join-Path (Join-Path $base $cell.run_relative) 'SHEET_PENDING.json') @{parent_batch=$run;id=$cell.id;note='Do not submit this cel separately while the parent request result is pending.'}}
 & (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $references -OutputDirectory $run -Size ($packing.w.ToString()+'x'+$packing.h) -Quality high -Background transparent -OutputFileName 'api_sheet_original.png' -Stage ('Adjacent character-only cel sheet: '+($Ids -join ', ')) | Out-Null
}
$layoutInfo=Get-Content -LiteralPath (Join-Path $run 'SHEET_MANIFEST.json') -Raw | ConvertFrom-Json
$receipt=Get-Content -LiteralPath (Join-Path $run 'result.json') -Raw | ConvertFrom-Json
$parentImage=Join-Path $run 'api_sheet_original.png'
$raw=[Drawing.Bitmap]::new($parentImage)
try{
 foreach($cell in $layoutInfo.cells){
  $celRun=Join-Path $base $cell.run_relative
  $c=$cell.rect_xywh
  $celFile=Join-Path $celRun 'character_api_cel.png'
  if(-not(Test-Path -LiteralPath $celFile)){
   $crop=$raw.Clone([Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]$c[2],[int]$c[3]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
   try{$crop.Save($celFile,[Drawing.Imaging.ImageFormat]::Png)}finally{$crop.Dispose()}
  }
  SaveJson (Join-Path $celRun 'EXTRACTED_FROM_API_SHEET.json') @{parent_run=$run;parent_image=$parentImage;parent_sha256=$receipt.output_sha256;rect_xywh=$cell.rect_xywh;guide_offset_xy=$cell.guide_offset_xy;operation='Rectangular crop only; no recoloring, painting, warping, masking or layer substitution';api_calls_at_child=0}
  SaveJson (Join-Path $celRun 'result.json') @{provider='OpenAI API';model=$receipt.model;quality=$receipt.quality;response_quality=$receipt.response_quality;size=($c[2].ToString()+'x'+$c[3]);parent_response_size=$receipt.response_size;response_background=$receipt.response_background;output_path=$celFile;output_sha256=(Get-FileHash -LiteralPath $celFile -Algorithm SHA256).Hash.ToLowerInvariant();api_calls=0;parent_api_calls=1;parent_run=$run;user_accepted=$false}
  SaveJson (Join-Path $celRun 'attempt.json') @{status='completed_from_api_sheet';api_calls=0;parent_api_calls=1;parent_run=$run;automatic_retries=0;image=$celFile}
 }
}finally{$raw.Dispose()}
[PSCustomObject]@{batch=$Batch;api_calls=1;characters=$layoutInfo.cells.Count;parent_api_image=$parentImage;status='returned_needs_visual_review'}

