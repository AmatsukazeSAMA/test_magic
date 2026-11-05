#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\full_character_redraw_1080p_v01\repairs\F1647_shoulder_v01'
if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'No automatic paid retry.'}
[void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
Add-Type -AssemblyName System.Drawing
$src=[Drawing.Bitmap]::new('D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G21-01\source.png')
$c=$src.Clone([Drawing.Rectangle]::new(930,720,240,360),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$im=[Drawing.Bitmap]::new(688,1024);$g=[Drawing.Graphics]::FromImage($im)
try{$g.Clear([Drawing.Color]::FromArgb(213,167,169));$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic;$g.DrawImage($c,[Drawing.Rectangle]::new(8,8,672,1008));$im.Save((Join-Path $run 'inputs\source_shoulder.png'))}finally{$g.Dispose();$im.Dispose();$c.Dispose();$src.Dispose()}
$prompt=@'
Edit this small ORIGINAL PV shoulder-frill detail. Remove the WHITE LETTERS M and I at the left edge and reconstruct the very short black outer frill contour hidden underneath the letter I. Keep the actual white maid shoulder frill, its outer curve, angular top, black fold lines, cropped black clothing and exact canvas placement. Do not redesign or move the shoulder. This is only a tiny shoulder-detail restoration for later character-layer compositing, not a full figure.
Use original sparse irregular solid black PV contours and flat #EEEEEE white frill / #303030 clothing. No gray shading, fabric texture, gradients or glow. Pink is only the reference scene background: replace that pink with genuine transparent alpha. White letters belong to a separate post-production subtitle layer and must be ABSENT from this character detail, including letter portions overlapping the frill edge. Infer the short obscured contour smoothly between the directly visible source stroke ends. Keep all other directly observed folds and source crop boundaries. No face, head, hair, bow, cap, hand, new clothing parts, lettering or scenery. Output exactly the isolated original shoulder detail, completing only the small glyph-obscured edge.
'@
[IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $run 'ROLE.json'),(@{source_frame=1647;crop_xywh=@(930,720,240,360);guide_scale=2.8;guide_translation=@(-2596,-2008);output='shoulder_api_original.png';role='API reconstructs only a source-obscured short shoulder outline. Raw whole-detail return retained; target character patch is small and independently recorded.';new_API_head_required=$false;author_hidden_pixels_recovered=$false}|ConvertTo-Json),[Text.UTF8Encoding]::new($false))
Write-Output $run
