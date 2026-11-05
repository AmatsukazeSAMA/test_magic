#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Specification)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=[IO.Path]::GetFullPath((Join-Path $root 'art\full_character_redraw_1080p_v01'))
$spec=Get-Content -LiteralPath $Specification -Raw | ConvertFrom-Json
$run=[IO.Path]::GetFullPath($spec.output_directory)
if(-not $run.StartsWith($base+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Repair output must stay in the current project.'}
if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'Repair attempt already exists; no automatic paid retry.'}
[void][IO.Directory]::CreateDirectory($run)
Add-Type -AssemblyName System.Drawing
$original=[Drawing.Bitmap]::new($spec.input_image)
$mask=[Drawing.Bitmap]::new($original.Width,$original.Height,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g=[Drawing.Graphics]::FromImage($mask)
try{
 $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
 $g.Clear([Drawing.Color]::White)
 foreach($r in $spec.edit_regions_xywh){
  if($r[0] -lt 0 -or $r[1] -lt 0 -or $r[0]+$r[2] -gt $original.Width -or $r[1]+$r[3] -gt $original.Height){throw 'Edit region outside original image.'}
  $g.FillRectangle([Drawing.Brushes]::Transparent,[int]$r[0],[int]$r[1],[int]$r[2],[int]$r[3])
 }
 $mask.Save((Join-Path $run 'edit_mask.png'),[Drawing.Imaging.ImageFormat]::Png)
 # API output sizes require multiples of 16. Native built-in outputs need not.
 # Preserve the input and matching mask at native size; request a valid output.
 $outputWidth=[int]([Math]::Ceiling($original.Width/16.0)*16)
 $outputHeight=[int]([Math]::Ceiling($original.Height/16.0)*16)
 $size=($outputWidth.ToString()+'x'+$outputHeight.ToString())
}finally{$g.Dispose();$mask.Dispose();$original.Dispose()}
$changes=@($spec.changes | ForEach-Object {'- '+$_}) -join "`n"
$eyeReference=if($spec.eye_reference){$spec.eye_reference}else{Join-Path $base 'inputs\eye_G02-01_F100.png'}
$hairReference=if($spec.hair_reference){$spec.hair_reference}else{Join-Path $base 'inputs\identity_full_drill_three_views.png'}
$eyeRole=if($spec.eye_reference_role){$spec.eye_reference_role}else{"the user-preferred G02 EYES ONLY; preserve its upper-lash construction with a solid dark-charcoal iris and small white glint, while the current source controls eye opening"}
$prompt=@"
Make the following LOCAL STRUCTURAL CORRECTIONS to reference 1, the current transparent complete visible character for $($spec.id). The provided alpha mask identifies editable regions; keep all other areas as close as possible to reference 1. Output the complete transparent character, not the mask and not a separate hair patch. Keep current face, eye opening, gaze, mouth, hand contact, original source clothing and framing unless a listed correction explicitly restores a missing source element. No background, words, effects, independent props or invented costume.

$changes

Reference 2 is the original head construction, including the substantial gray/mint corkscrew, for identity and drill volume only. Reference 3 is $eyeRole. Reference 4 is the ORIGINAL PV action and costume guide: preserve that exact visible pose and garment. Do not add a maid uniform, headband, cuffs or neck bow to casual clothing. Reference 2's polished shading and green reflective bob bands are not a style reference.

Use economical dark PV ink, flat ash-gray bob, muted mint stripe on the single drill, two red beads, healthy light warm peach skin. Do not add bob highlight bands, airbrush, hair strand detailing, fabric texture or glossy shading. Preserve a genuinely long tapering continuous drill; allow lower turns to continue beyond the existing close-up crop or disappear naturally behind the shoulder rather than miniaturizing the whole lock to keep its tip visible. Keep natural shoulder overlap and anatomical attachment. Genuine transparent alpha outside the visible character.

This result is an intermediate local repair. A subsequent built-in imagegen whole-character redraw is required by the user's workflow before final review; do not try to deliver a detached patch or collage here.
"@
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,$utf8)
$request=@{
 PromptFile=(Join-Path $run 'prompt.txt');
 InputImages=@($spec.input_image,$hairReference,$eyeReference,$spec.source_pose_guide);
 OutputDirectory=$run;Size=$size;Quality='high';Background='transparent';OutputFileName='character_api_original.png';
 Stage=('GOAL intermediate local repair: '+$spec.id+'; mandatory whole-character imggen follows');
 MaskFile=(Join-Path $run 'edit_mask.png')
}
if($spec.continuity_reference){
 $request.InputImages+=@($spec.continuity_reference)
 $prompt+="`nREFERENCE 5 is the preceding reviewed character for HAIR CONSTRUCTION AND SHOULDER OCCLUSION ONLY. Match its bead-root scale, full coil volume, length and behind-shoulder overlap. Preserve reference 1's CURRENT eye opening and source 4 pose. Do not shorten the coil to fit its tip on canvas."
 [IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,$utf8)
}
[IO.File]::WriteAllText((Join-Path $run 'LOCAL_REPAIR_REQUEST.json'),($request | ConvertTo-Json -Depth 15),$utf8)
[IO.File]::WriteAllText((Join-Path $run 'LOCAL_REPAIR_STATUS.json'),(@{id=$spec.id;intermediate_only=$true;must_follow_with_whole_character_imggen=$true;whole_character_imggen_completed=$false;user_accepted=$false} | ConvertTo-Json),$utf8)
[PSCustomObject]@{prepared=$true;id=$spec.id;size=$size;mask=$request.MaskFile;run=$run;api_calls=0}
