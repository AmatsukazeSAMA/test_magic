#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw|ConvertFrom-Json
$specs=@(
 @{id='ART-G17-01';crop=@(265,32,355,252);view='front three-quarter, looking back toward the viewer; original open round eyes and tiny neutral mouth, not a smile';side='The TWO red bead roots and ONE long mint-striped corkscrew are on IMAGE RIGHT beside the visible ear, hanging naturally down beside the neck.'},
 @{id='ART-G21-01';crop=@(930,45,765,670);view='rear three-quarter, BACK OF HEAD with only a tiny face sliver visible on IMAGE LEFT; do not rotate to face us';side='The TWO red bead roots and the ONE long mint-striped corkscrew are on IMAGE LEFT beside the small visible face sliver. The right half of the bob has NO beads or spiral. The left drill drapes naturally beside the nape/back.'},
 @{id='ART-G22-01';crop=@(296,90,300,260);view='strict RIGHT-facing profile, keep the source wide open eye and tiny neutral mouth; no sleepy eyelid';side='The TWO red bead roots and ONE complete long mint-striped corkscrew are behind the jaw on IMAGE LEFT, naturally hanging alongside the nape. Keep its full middle turns and curled tip, not a tiny two-turn tassel.'}
)
Add-Type -AssemblyName System.Drawing
foreach($spec in $specs){
 $job=$plan.jobs|Where-Object id -eq $spec.id
 $run=Join-Path (Join-Path $base $job.run_relative) 'head_only_v01'
 if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')){throw 'Existing head-only attempt; never automatically resubmit.'}
 [void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
 $im=[Drawing.Bitmap]::new($job.source_image);$c=$spec.crop
 $crop=$im.Clone([Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]$c[2],[int]$c[3]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 $guide=[Drawing.Bitmap]::new(816,816);$g=[Drawing.Graphics]::FromImage($guide)
 try {
  $g.Clear([Drawing.Color]::FromArgb(213,167,169));$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $s=[Math]::Min(620/[double]$crop.Width,430/[double]$crop.Height)
  $g.DrawImage($crop,[Drawing.RectangleF]::new([single]((816-$crop.Width*$s)/2),30,[single]($crop.Width*$s),[single]($crop.Height*$s)))
  $guide.Save((Join-Path $run 'inputs\current_source_head.png'),[Drawing.Imaging.ImageFormat]::Png)
 }finally{$g.Dispose();$guide.Dispose();$crop.Dispose();$im.Dispose()}
 Copy-Item -LiteralPath (Join-Path (Join-Path $base $job.run_relative) 'inputs\view_matched_identity.png') -Destination (Join-Path $run 'inputs\view_matched_identity.png')
 $prompt=@"
Draw ONE isolated head-and-bare-neck animation asset with the COMPLETE attached corkscrew hair, on real transparent alpha. Draw NO hat, NO white maid cap, NO headband, NO black ribbon or bow, NO collar, NO shoulders and NO clothes. The original costume, cap and ribbon are preserved separately for post-compositing; this API asset must contain only head, face, bare neck, gray bob, two red beads and one complete spiral lock. Keep the whole crown and the curled tip inside the canvas with transparent margin.

Image 1 gives the CURRENT source head angle, eye opening, mouth expression and the original PV's simple line drawing. This exact view is: $($spec.view). Its red twin-drill hair is replaced entirely. Ignore and omit the original white cap, black ribbon, clothes and letters in reference 1.
Image 2 gives ONLY the new identity: rounded short ash-gray bob, bangs, subtle mint stripe, two red beads and one long tapering corkscrew. $($spec.side)

The full connected spiral has about five broad turns, including the complete middle and a small tapering curled tip, and extends approximately ONE BOB-HEAD HEIGHT below the bead root. Do not attach it across the opposite side or force it in front of a shoulder. Keep the head in the upper half of the canvas and reserve lower room for the whole spiral. Original sparse black PV contours, simple source-like eyes, a tiny source-like mouth, a few grouped hair sections. All interiors are perfectly FLAT single-color fills: warm skin #FCE8DC, hair #B8B7B4, subtle mint #B1CFBB, red beads #B51C24, dark ink. No gradients, blush, lighting, shine, glints, texture, hair highlight bands or detailed strands. Source expression stays unchanged. One transparent head only, zero lettering or scenery.
"@
 [IO.File]::WriteAllText((Join-Path $run 'prompt.txt'),$prompt,[Text.UTF8Encoding]::new($false))
 [IO.File]::WriteAllText((Join-Path $run 'HEAD_ASSET_ROLE.json'),(@{id=$job.id;source_frame=$job.source_frame;source=$job.source_image;crop_xywh=$spec.crop;method='API draws complete head and connected spiral in one pass; original body and original cap retained separately for compositing';user_basis='Earlier user allowed face-only replacement with original PV body design; current task requests character-only API redraw and later compositing';user_accepted=$false}|ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
 Write-Output $run
}
