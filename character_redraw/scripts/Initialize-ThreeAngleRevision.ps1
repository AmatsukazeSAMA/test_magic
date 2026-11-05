#Requires -Version 7.0
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$utf8=[Text.UTF8Encoding]::new($false)
$old=Join-Path $root 'art\20261030_pv_three_angles_v01'
$new=Join-Path $root 'art\20261030_pv_three_angles_v02'
[void][IO.Directory]::CreateDirectory($new)
function Derived-Script([string]$source,[string]$target,[hashtable]$changes){
 $text=[IO.File]::ReadAllText((Join-Path $PSScriptRoot $source))
 foreach($key in $changes.Keys){if(-not $text.Contains($key)){throw ('Missing script substitution: '+$key)};$text=$text.Replace($key,$changes[$key])}
 [IO.File]::WriteAllText((Join-Path $PSScriptRoot $target),$text,$utf8)
}
Derived-Script 'PVPalette.cs' 'PVPaletteV2.cs' @{
 'public static class PVPalette {'='public static class PVPaletteV2 {';
 'BlendInk(p,i,254,244,238,'='BlendInk(p,i,252,232,220,'
}
Derived-Script 'Match-PVHeadPalette.ps1' 'Match-PVHeadPaletteV2.ps1' @{
 'PVPalette'='PVPaletteV2';
 'target_skin_rgb=@(254,244,238)'='target_skin_rgb=@(252,232,220)';
 'Matched flat head colors and original identity skin; alpha and dark ink cores unchanged.'='Applied warmer revised skin; alpha and dark ink cores unchanged.';
 "method='non-generative limited-palette color correction of the API drawing; no line or geometry reconstruction'"="method='user-requested warmer skin and limited-palette correction of the API drawing; no line or geometry reconstruction'"
}
Derived-Script 'Compose-PVAngle.ps1' 'Compose-PVAngleV2.ps1' @{
 'PVPalette'='PVPaletteV2';'PVAngleScan'='PVAngleScanV2';
 '20261030_pv_three_angles_v01'='20261030_pv_three_angles_v02';
 'original identity skin matched at RGB 254,244,238'='user-requested warmer skin RGB 252,232,220'
}
Derived-Script 'Build-ThreeAngleReview.ps1' 'Build-ThreeAngleReviewV2.ps1' @{
 '20261030_pv_three_angles_v01'='20261030_pv_three_angles_v02';
 '原 PV 头部替换 · 正 / 侧 / 背'='原 PV 头部替换 v02 · 肤色 / 发辫修订';
 '头部近景 · 肤色按最初人设统一'='头部近景 v02 · 暖肤色 / 身前发辫'
}
$studies=@{front='20261030_skin_front_v04';side='20261030_braid_side_v02';back='20261030_braid_back_v02'}
foreach($view in @('front','side','back')){
 $cfg=Get-Content -LiteralPath (Join-Path $old ($view+'_layout.json')) -Raw | ConvertFrom-Json -AsHashtable
 $cfg.head='art/'+$studies[$view]+'/head_palette_matched.png'
 if($view -eq 'side'){$cfg.head_clip_xywh=@(@(208,160,222,176),@(270,295,90,150));$cfg.detail_roi_xywh=@(195,145,260,320)}
 $cfg | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $new ($view+'_layout.json')) -Encoding utf8
}
$front=Join-Path $root 'art\20261030_skin_front_v04'
[void][IO.Directory]::CreateDirectory($front)
$original=Join-Path $root 'art\20261030_head_style_front_v03\head_api_original.png'
Copy-Item -LiteralPath $original -Destination (Join-Path $front 'head_api_original.png')
@{method='reuse original front API drawing; non-generative warmer skin correction only';source_api_run='art/20261030_head_style_front_v03';source_api_original=$original;source_api_sha256=(Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash.ToLowerInvariant();new_api_calls=0;target_skin_rgb=@(252,232,220);previous_skin_rgb=@(254,244,238);reason='user judged previous skin too pale';user_accepted=$false} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $front 'DERIVATION.json') -Encoding utf8
Write-Output 'Prepared isolated v02 processing scripts/layouts; v01 delivery preserved.'
