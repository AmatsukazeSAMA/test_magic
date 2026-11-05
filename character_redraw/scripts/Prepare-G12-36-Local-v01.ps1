#Requires -Version 7.0
$ErrorActionPreference='Stop'
$base=Join-Path (Split-Path -Parent $PSScriptRoot) 'art/full_character_redraw_1080p_v01'
$original=Join-Path $base 'drawings/ART-G12-36/v01'
$run=Join-Path $original 'local_restore_current_eye_and_wrist_v01'
$specPath=Join-Path $base 'review/G12-36_current_eye_and_wrist_v01_spec.json'
if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'Existing attempt: no paid retry.'}
$spec=@{
 id='ART-G12-36';input_image=(Join-Path $original 'character_api_original.png');output_directory=$run;
 source_pose_guide=(Join-Path $original 'inputs/source_pose_guide.png');
 edit_regions_xywh=@(@(208,226,236,130),@(478,120,258,450));
 changes=@('Restore the current original source rounder open eyes and horizontal flipped wrists with fingers pointing image-right. Do not copy the previous state half-lids or upward-pointing hands.');
}
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText($specPath,($spec | ConvertTo-Json -Depth 10),$utf8)
& (Join-Path $PSScriptRoot 'Prepare-GoalLocalRepair.ps1') -Specification $specPath
$requestPath=Join-Path $run 'LOCAL_REPAIR_REQUEST.json'
$request=Get-Content -LiteralPath $requestPath -Raw | ConvertFrom-Json
$request.InputImages=@($spec.input_image,$spec.source_pose_guide)
$prompt=@'
Correct the complete transparent character in image 1 using ONLY the CURRENT ORIGINAL action in image 2. Image 1 copied the previous drawing's eye expression and hand gesture; both must be restored to image 2. This is a masked structural repair, not a new pose.

EYES: Image 2 has rounder, more open eyes looking towards the raised hands. Restore its exact eyelid opening and gaze, with one solid dark charcoal iris and one small white glint per eye. Keep the existing character identity, face shape, little curved mouth and warm peach skin. No half-lidded sleepy expression, iris rings or gradients.

HANDS AND WRISTS: Rebuild the two raised hands, wrists, white cuffs and adjoining black forearms to the CURRENT source image 2. Both wrists flip horizontally so the flattened fingers extend to IMAGE RIGHT. The upper hand is roughly horizontal at source-guide x530..678 y193..253, the lower hand bends to the right near x625..696 y248..291. Preserve the two DIFFERENT cuff/forearm angles and the negative gap between the arms. Do NOT repeat image 1's fingers pointing diagonally upwards to image-left. Match image 2's actual hand heights, elbow angles and silhouette; economical mitten-like PV fingers are appropriate.

All other current image-1 gray bob, two red beads, the full continuous substantial mint-striped corkscrew, the two-leaf maid headband, body, black dress, white ruffles, apron and red neck bow remain close to image 1. Do not recolor hair red, copy the original twin tails, add hands or costume parts, or invent hidden anatomy. Preserve the existing canvas and bottom crop. Genuine transparent alpha around the visible character. No text, background, props or effects. Flat economical hand-drawn PV ink; no polish, soft gradients, fabric texture or glossy hair bands.

This is an intermediate repair. A separate built-in imagegen redraw of the WHOLE currently visible character must follow to unify joins before final review.
'@
[IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,$utf8)
[IO.File]::WriteAllText($requestPath,($request | ConvertTo-Json -Depth 15),$utf8)
[PSCustomObject]@{id=$spec.id;request=$requestPath;api_calls=0}
