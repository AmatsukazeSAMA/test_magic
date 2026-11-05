#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$refs='D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\references\maid_outfit'
$sheet=[Drawing.Bitmap]::new((Join-Path $root 'art\20261030_maid_turnaround_v01\maid_turnaround_v01.png'))
$specs=@(
 @{view='front';run='20261030_head_style_front_v03';source='FR01_F002306.png';frame=2306;time=76.944;crop=@(790,75,290,220);identity=@(230,0,200,280)},
 @{view='side';run='20261030_head_style_side_v01';source='SD01_F002751.png';frame=2751;time=91.792;crop=@(205,160,230,200);identity=@(640,0,250,290)},
 @{view='back';run='20261030_head_style_back_v01';source='BK01_F002362.png';frame=2362;time=78.812;crop=@(825,75,270,210);identity=@(1100,0,240,290)}
)
try {
 foreach($s in $specs){
  $run=Join-Path $root ('art\'+$s.run);$inputs=Join-Path $run 'inputs'
  [void][IO.Directory]::CreateDirectory($inputs)
  $target=Join-Path $inputs 'source_frame.png'
  if(-not(Test-Path -LiteralPath $target)){Copy-Item -LiteralPath (Join-Path $refs $s.source) -Destination $target}
  $original=[Drawing.Bitmap]::new($target)
  $style=$identity=$null
  try {
   $c=$s.crop;$style=$original.Clone([Drawing.Rectangle]::new($c[0],$c[1],$c[2],$c[3]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
   $style.Save((Join-Path $inputs 'source_head_style.png'),[Drawing.Imaging.ImageFormat]::Png)
   $c=$s.identity;$identity=$sheet.Clone([Drawing.Rectangle]::new($c[0],$c[1],$c[2],$c[3]),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
   $identity.Save((Join-Path $inputs 'identity_head.png'),[Drawing.Imaging.ImageFormat]::Png)
  } finally {foreach($im in @($original,$style,$identity)){if($im){$im.Dispose()}}}
  @{view=$s.view;frame=$s.frame;time_s=$s.time;source_attachment=1;source_png=$s.source;source_crop_xywh=$s.crop;identity_sheet_crop_xywh=$s.identity;crop_resampled=$false;new_hypothesis='head-only enlarged native drawing with a fixed, small flat-color palette; original PV is sole rendering reference';user_accepted=$false} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $run 'INPUT_PROVENANCE.json') -Encoding utf8
 }
} finally {$sheet.Dispose()}
Write-Output 'Prepared independent source-pose and identity head references for front, side and back.'
