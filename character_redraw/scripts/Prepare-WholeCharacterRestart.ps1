#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$restart=Join-Path $base 'whole_character_restart_v01'
[void][IO.Directory]::CreateDirectory((Join-Path $restart 'inputs'))
$utf8=[Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Drawing
$f858=Join-Path $base 'drawings\ART-G12-10\v01\qa_white.png'
$im=[Drawing.Bitmap]::new($f858)
$eyes=$im.Clone([Drawing.Rectangle]::new(245,258,235,135),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
try{$eyes.Save((Join-Path $restart 'inputs\F858_eye_style.png'))}finally{$eyes.Dispose();$im.Dispose()}
$identity=[Drawing.Bitmap]::new((Join-Path $base 'inputs\original_identity_turnaround.png'))
$head=$identity.Clone([Drawing.Rectangle]::new(365,0,290,440),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
try{$head.Save((Join-Path $restart 'inputs\original_front_head_identity.png'))}finally{$head.Dispose();$identity.Dispose()}
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw|ConvertFrom-Json
foreach($id in @('ART-G17-01','ART-G21-01','ART-G22-01')){
 $j=$plan.jobs|Where-Object id -eq $id;$old=Join-Path $base $j.run_relative
 $run=Join-Path $restart ('F'+$j.source_frame)
 [void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
 $targetPath=Join-Path $old ('composite_v02\PV_F'+$j.source_frame+'_1920x1080.png')
 $target=[Drawing.Bitmap]::new($targetPath);$c=$j.crop_xyxy
 $crop=$target.Clone([Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]($c[2]-$c[0]),[int]($c[3]-$c[1])),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $guide=[Drawing.Bitmap]::new([int]$j.output_size[0],[int]$j.output_size[1]);$g=[Drawing.Graphics]::FromImage($guide)
 try{$g.Clear([Drawing.Color]::FromArgb(213,167,169));$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$s=[Math]::Min(($guide.Width-24)/[double]$crop.Width,($guide.Height-24)/[double]$crop.Height);$dx=($guide.Width-$crop.Width*$s)/2;$dy=($guide.Height-$crop.Height*$s)/2;$g.DrawImage($crop,[Drawing.RectangleF]::new([single]$dx,[single]$dy,[single]($crop.Width*$s),[single]($crop.Height*$s)));$guide.Save((Join-Path $run 'inputs\rejected_composite_character_reference.png'))}finally{$g.Dispose();$guide.Dispose();$crop.Dispose();$target.Dispose()}
 Copy-Item -LiteralPath (Join-Path $old 'inputs\source_pose_guide.png') -Destination (Join-Path $run 'inputs\original_PV_pose_costume.png')
 Copy-Item -LiteralPath (Join-Path $restart 'inputs\F858_eye_style.png') -Destination (Join-Path $run 'inputs\F858_eye_style.png')
 $role=@{frame=$j.source_frame;id=$id;provider=$(if($j.source_frame -eq 1647){'configured OpenAI API'}else{'built-in imagegen'});user_request='Overall whole-character redraw; do not repair by recombining separately drawn head, cap and body';eye_baseline_frame=858;eye_baseline_path=$f858;eye_baseline_sha256=(Get-FileHash -LiteralPath $f858).Hash.ToLowerInvariant();head_and_body_separate_compositing_authorized_for_this_restart=$false;character_only=$true;composition_dimensions=@(1920,1080);user_accepted=$false;source_frame=$j.source_frame;source_pts=$j.source_pts;source_image=$j.source_image;target_rejected=$targetPath}
 [IO.File]::WriteAllText((Join-Path $run 'RESTART_SCOPE.json'),($role|ConvertTo-Json -Depth 8),$utf8)
}
$prompt=@'
Redraw the ENTIRE character in image 1 as a NEW cohesive Japanese hand-drawn PV animation cel, not a pasted head on an old torso. This is a BACK three-quarter shoulder portrait, with the face barely peeking toward IMAGE LEFT. Rebuild head, neck, maid cap, black hair ribbon, shoulders and uniform together with natural anatomy and one consistent drawing style. Keep the original camera view and cropped-bust extent from image 2; no complete figure or legs. The neck is short and naturally seated inside the original BLACK high collar, not a long exposed cylinder. Head width and shoulders are balanced. The white ruffled maid cap follows and firmly sits on the crown; the connected black two-leaf/ear ornament is fixed to its band, never floating. White shoulder frills and diagonal apron straps remain the ORIGINAL maid uniform design from image 2.

Image 1 is a REJECTED collage only for rough identity/view; improve the whole construction, do not preserve its oversized head, long neck or detached headwear. Image 2 is the original PV authority for clothing, view, proportions and simple line economy. Image 3 is the USER-SELECTED F858 EYE DRAWING STYLE: curved bold upper lash, dark charcoal iris with a small white highlight and simple lower marks; use this rendering for any tiny visible eye, without adding an eye to the hidden back of the head. Image 4 is the original rear-bob/drill construction reference only, not clothing.

Short rounded ash-gray bob, a few grouped contour lines and clean tapered nape; TWO red beads and only ONE complete gray/muted-mint corkscrew attached on IMAGE LEFT beside the visible left nape. Its complete broad top, connected tapering middle and small curled tip drape naturally to the shoulder/back; no second drill, no missing middle segment, no forced crossing to the front. Warm light peach skin like the original identity, around #FCE8DC. Clean economical source-like black ink and mostly flat color, matching F858's approachable anime PV drawing. Do not fill the back bob with dozens of thin strands or turn the hair into a huge geometric dome. No photoreal textures, glossy rendering, cast shadows or gray airbrush over the costume.

Output ONE integrated character-only transparent PNG on this portrait canvas. Keep all source-visible shoulders and the lower crop, a small clear outer margin. No pink backdrop, captions, letters, credits, borders or effects. The full returned character will be used as ONE drawing; no later local head/body/cap assembly.
'@
[IO.File]::WriteAllText((Join-Path $restart 'F1647\prompt.txt'),$prompt,$utf8)
[IO.File]::WriteAllText((Join-Path $restart 'USER_STEERING.json'),(@{latest_requests=@('这种太丑了，整体重绘','这种存在接缝的，不再修改，使用imggen重绘修改即可','这种头饰飘逸的也是','这张API重绘','F858的眼睛画法为基准');provider_per_frame=@{'1647'='OpenAI API high';'1501'='built-in imagegen';'1666'='built-in imagegen'};superseded='Separate head/body/cap assembly and manual seam-pixel iteration';keep_history=$true;new_eye_style='Use F858 rendering; current frame still controls openness and expression';user_accepted=$false}|ConvertTo-Json -Depth 8),$utf8)
Write-Output $restart
