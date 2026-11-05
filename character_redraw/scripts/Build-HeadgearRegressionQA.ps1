#Requires -Version 7.0
[CmdletBinding()]
param([string]$Version='v01')
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$out=Join-Path $base ('review\headgear_audit_'+$Version)
if(Test-Path -LiteralPath $out){throw 'Keep the existing diagnostic catalog; choose a new version.'}
[void][IO.Directory]::CreateDirectory($out)
$registry=Get-Content -LiteralPath (Join-Path $base 'ASSET_REGISTRY.json') -Raw | ConvertFrom-Json -AsHashtable
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$groups=@('G12','G13','G15','G17','G18','G19','G21','G22','G23','G24','G25','G33','G34','G36','G51')
$rows=@()
foreach($id in @($registry.Keys | Sort-Object)){
 $asset=$registry[$id]
 $job=$plan.jobs | Where-Object id -eq $id
 if($asset.primary_static_pass -and $asset.independent_static_pass -and $job.group -in $groups){
  $rows+=@{id=$id;job=$job;asset=$asset;source=(Join-Path (Join-Path $base $job.run_relative) 'inputs\source_pose_guide.png');qa=(Join-Path $asset.selected_run 'qa_white.png')}
 }
}
Add-Type -AssemblyName System.Drawing
function Draw-HeadDiagnostic($graphics,[string]$path,[int]$x,[int]$y,[double]$portion,[bool]$rotate){
 $bitmap=[Drawing.Bitmap]::new($path)
 try{
  if($rotate){$bitmap.RotateFlip([Drawing.RotateFlipType]::Rotate180FlipNone)}
  $height=[int][Math]::Ceiling($bitmap.Height*$portion)
  $scale=[Math]::Min(345.0/$bitmap.Width,288.0/$height)
  $width=$bitmap.Width*$scale
  $drawHeight=$height*$scale
  $graphics.DrawImage($bitmap,[Drawing.RectangleF]::new([single]($x+(345-$width)/2),[single]$y,[single]$width,[single]$drawHeight),[Drawing.RectangleF]::new(0,0,$bitmap.Width,$height),[Drawing.GraphicsUnit]::Pixel)
  return @{native_dimensions=@($bitmap.Width,$bitmap.Height);diagnostic_crop_xywh=@(0,0,$bitmap.Width,$height);diagnostic_rotation_degrees=if($rotate){180}else{0}}
 }finally{$bitmap.Dispose()}
}
$pages=@()
$font=[Drawing.Font]::new('Arial',12)
try{
 for($offset=0;$offset -lt $rows.Count;$offset+=8){
  $selected=@($rows[$offset..([Math]::Min($rows.Count-1,$offset+7))])
  $height=[int]([Math]::Ceiling($selected.Count/2.0)*335)
  $canvas=[Drawing.Bitmap]::new(1440,$height,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g=[Drawing.Graphics]::FromImage($canvas)
  $entries=@()
  try{
   $g.Clear([Drawing.Color]::White)
   $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
   for($i=0;$i -lt $selected.Count;$i++){
    $row=$selected[$i]
    if((Get-FileHash -LiteralPath $row.asset.image).Hash.ToLowerInvariant() -ne $row.asset.sha256){throw 'Reviewed art changed before catalog build.'}
    $x=($i%2)*720
    $y=[int][Math]::Floor($i/2.0)*335
    $portion=if($row.job.kind -eq 'body_pose'){.45}elseif($row.job.kind -eq 'half_body'){.62}else{.85}
    $rotate=$row.job.group -eq 'G19'
    if($rotate){$portion=.7}
    $g.DrawString(($row.id+' / F'+$row.job.source_frame+' / SOURCE | CURRENT '+$row.asset.sha256.Substring(0,10)),$font,[Drawing.Brushes]::Black,[single]($x+4),[single]($y+3))
    $sourceCrop=Draw-HeadDiagnostic $g $row.source ($x+5) ($y+30) $portion $rotate
    $artCrop=Draw-HeadDiagnostic $g $row.qa ($x+365) ($y+30) $portion $rotate
    $entries+=@{id=$row.id;source=$row.source;current_qa=$row.qa;current_image=$row.asset.image;image_sha256=$row.asset.sha256;source_diagnostic=$sourceCrop;current_diagnostic=$artCrop}
   }
   $page=Join-Path $out ('page_'+([int]($offset/8)+1).ToString('00')+'.png')
   $canvas.Save($page,[Drawing.Imaging.ImageFormat]::Png)
   $pages+=@{image=$page;entries=$entries;actual_reviewed=$false}
  }finally{$g.Dispose();$canvas.Dispose()}
 }
}finally{$font.Dispose()}
@{scope='Diagnostic source/selected-QA head crops only; no art pixels changed and no automatic review or acceptance.';items=$rows.Count;pages=$pages;actual_reviewed=$false;user_accepted=$false} | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $out 'INDEX.json') -Encoding utf8
[PSCustomObject]@{items=$rows.Count;pages=$pages.Count;directory=$out;art_pixels_changed=$false;visual_review='pending actual inspection'}
