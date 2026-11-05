#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw|ConvertFrom-Json
$specs=@(
 @{id='ART-G06-03';crop=@(740,620,300,235);rotation=180;size='816x816'},
 @{id='ART-G07-02';crop=@(100,270,1060,700);rotation=180;size='1536x1536'},
 @{id='ART-G18-01';crop=@(1318,130,535,390);rotation=0;size='816x816'},
 @{id='ART-G33-03';crop=@(790,78,290,250);rotation=0;size='816x816'},
 @{id='ART-G33-04';crop=@(770,52,300,275);rotation=0;size='816x816'},
 @{id='ART-G33-05';crop=@(780,0,305,302);rotation=0;size='816x816'}
)
Add-Type -AssemblyName System.Drawing
foreach($sp in $specs){
 $j=$plan.jobs|Where-Object id -eq $sp.id;$run=Join-Path (Join-Path $base $j.run_relative) 'head_only_v01'
 if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'Head-only attempt exists; never resubmit.'}
 [void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
 $im=[Drawing.Bitmap]::new($j.source_image);$c=$sp.crop
 $crop=$im.Clone([Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]$c[2],[int]$c[3]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 if($sp.rotation -eq 180){$crop.RotateFlip([Drawing.RotateFlipType]::Rotate180FlipNone)}
 $guide=[Drawing.Bitmap]::new(816,816);$g=[Drawing.Graphics]::FromImage($guide)
 try{$g.Clear([Drawing.Color]::FromArgb(213,167,169));$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$s=[Math]::Min(620/[double]$crop.Width,430/[double]$crop.Height);$g.DrawImage($crop,[Drawing.RectangleF]::new([single]((816-$crop.Width*$s)/2),30,[single]($crop.Width*$s),[single]($crop.Height*$s)));$guide.Save((Join-Path $run 'inputs\current_source_head.png'))}finally{$g.Dispose();$guide.Dispose();$crop.Dispose();$im.Dispose()}
 $identity=[Drawing.Bitmap]::new((Join-Path $base 'inputs\original_identity_turnaround.png'))
 $ref=$identity.Clone([Drawing.Rectangle]::new(365,0,290,440),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try{$ref.Save((Join-Path $run 'inputs\view_matched_identity.png'))}finally{$ref.Dispose();$identity.Dispose()}
 $rotText=if($sp.rotation -eq 180){'The current SOURCE HEAD crop has deliberately been rotated upright for accurate identity construction. Draw it in THIS upright reference orientation. We will rotate the WHOLE API head back 180 degrees during post-compositing, so keep the bead root on IMAGE RIGHT of this upright head; do not pre-invert or mirror it yourself.'}else{'Keep exactly the current source head tilt and face direction; do not normalize a tilted dance head into a straight pose.'}
 $prompt=@"
Draw ONE isolated head-and-bare-neck animation asset on transparent alpha, with a complete gray bob and ONE complete attached long spiral lock. No maid cap, headband, ribbon, bow, collar, shoulder, arm, hands, body, clothes, plate, disc, captions, effects or background. We retain all ORIGINAL body, outfit, hands, legs and headwear separately in source-preserving post-compositing.

Reference 1 is the CURRENT original PV head for $($j.id), frame $($j.source_frame). Copy its exact head tilt, viewing direction, eye opening, pupil direction, and mouth shape. Open eyes must remain open, closed eyes remain closed, an open mouth remains that size, and neutral is not replaced by a smile. $rotText
Reference 2 gives only the identity: rounded short ash-gray bob and bangs, two red beads and one muted-mint-striped gray corkscrew on the character's anatomical LEFT, which is IMAGE RIGHT for this upright front-facing head. No second lock or bead pair. Do not copy reference 2's detailed eye rendering, smile, skin shading, collar or school outfit.

Keep the complete crown and curled drill tip inside the canvas with transparent margins. Head in the upper half, enough space below for the whole spiral. Connected spiral from the bead root, through about five broad tapering turns and the full middle, to a small curled tip, about one bob-head height below the root. Natural side/nape drape; do not force it over a shoulder. Match the ORIGINAL simple hand-drawn PV: a few grouped hair contours, continuous dark ink with modest natural width variation, simple solid dark eyes and a tiny source-like mouth. Flat skin #FCE8DC, hair #B8B7B4, mint #B1CFBB, beads #B51C24. Perfectly flat single-color interiors: no gradients, lighting, blush, highlights, glints, texture or fine detailed strands. One head plus bare neck and complete connected lock ONLY, zero costume or props.
"@
 [IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,[Text.UTF8Encoding]::new($false))
 [IO.File]::WriteAllText((Join-Path $run 'HEAD_ASSET_ROLE.json'),(@{id=$j.id;source_frame=$j.source_frame;crop_xywh=$sp.crop;reference_rotation_degrees=$sp.rotation;post_head_rotation_degrees=$sp.rotation;size=$sp.size;reason='Sol xhigh flagged an obvious defect in existing candidate: amputated body, inverted root, or mismatched head style. Redraw whole head and full connected lock with original body retained.';user_accepted=$false}|ConvertTo-Json),[Text.UTF8Encoding]::new($false))
 Write-Output ([PSCustomObject]@{id=$j.id;run=$run;size=$sp.size})
}
