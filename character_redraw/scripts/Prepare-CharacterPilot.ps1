#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$project='D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029'
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$shared=Join-Path $base 'inputs'
$run=Join-Path $base 'drawings\ART-G33-01\v01'
[void][IO.Directory]::CreateDirectory($shared)
[void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
$utf8=[Text.UTF8Encoding]::new($false)
Copy-Item -LiteralPath (Join-Path $root 'art\20261030_maid_turnaround_v01\inputs\identity_turnaround.png') -Destination (Join-Path $shared 'original_identity_turnaround.png')
Copy-Item -LiteralPath (Join-Path $root 'art\20261030_braid_revision_refs\user_side_back_hair.png') -Destination (Join-Path $shared 'user_hair_side_back.png')
Add-Type -AssemblyName System.Drawing
$src=[Drawing.Bitmap]::new((Join-Path $project 'cels\G33-01\source.png'))
try {
 $rect=[Drawing.Rectangle]::new(750,48,385,1000)
 $crop=$src.Clone($rect,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
 try {$crop.Save((Join-Path $run 'inputs\source_character_crop.png'),[Drawing.Imaging.ImageFormat]::Png)}finally{$crop.Dispose()}
}finally{$src.Dispose()}
$manifest=[ordered]@{
 scope='All character redraw work items from attachment 1; no generated captions, effects or backgrounds.'
 user_requests=@('1080P即可，后续重绘只需要重绘人物即可，字幕之类的应该由后期合成，节省画布。重绘所有画面，API重绘','钻发不需要刻意往肩膀前，但要注意相邻帧需要一致，不能跳变。')
 provider='configured OpenAI API';endpoint='https://api.openai.com/v1/images/edits';model='gpt-image-2.5-sunburst';quality='high'
 output_composition=@(1920,1080);generation='transparent character-only PNG on compact canvases'
 latest_braid_rule='Natural drape, not forced ahead of shoulder. Keep anatomical-left root, length, coil direction and occlusion consistent across adjacent drawings.'
 authorization='User explicitly requested all-character API redraws in this ongoing configured-API task; prior direct user reply consented to reference transfer to api.openai.com.'
 known_work_item_count=306;unresolved_exposures_kept=$true;all_author_cels_proven_complete=$false
 pilot='ART-G33-01';pilot_size='640x1024';source_frame=2306;source_pts=1231104;time_base='1/16000'
 crop_xywh=@(750,48,385,1000);technical_crop_only=$true;artistic_acceptance='pending'
 api_size_documentation='https://developers.openai.com/api/docs/guides/image-prompting';minimum_API_output_pixels=655360
}
[IO.File]::WriteAllText((Join-Path $base 'PROJECT_SCOPE.json'),($manifest | ConvertTo-Json -Depth 15),$utf8)

