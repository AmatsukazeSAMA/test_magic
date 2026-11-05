#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$pair=Join-Path $root 'art\pv_whole_redraw_pair_v01'
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Json([string]$path,$value){[IO.File]::WriteAllText($path,($value | ConvertTo-Json -Depth 20),$utf8)}
foreach($name in @('README.md','CURRENT_SELECTION.json','image_defaults.json')) {
 $backup=Join-Path $pair ('previous_root_'+$name)
 if(-not(Test-Path -LiteralPath $backup)){Copy-Item -LiteralPath (Join-Path $root $name) -Destination $backup}
}
$selected=@()
$log=@()
foreach($view in @('back','side')) {
 $relative='art/pv_whole_redraw_'+$view+'_v01'
 $run=Join-Path $root $relative
 $check=Get-Content -LiteralPath (Join-Path $run 'TECHNICAL_CHECK.json') -Raw | ConvertFrom-Json
 if(-not $check.technical_integrity_pass){throw "$view failed technical integrity."}
 $intent=Get-Content -LiteralPath (Join-Path $run 'INTENT.json') -Raw | ConvertFrom-Json
 $result=Get-Content -LiteralPath (Join-Path $run 'result.json') -Raw | ConvertFrom-Json
 $selected+=@{view=$view;source_attachment=1;source_frame=$intent.source_frame;source_time_s=$intent.source_time_s;image=($relative+'/whole_PV_api_original.png');actual_dimensions=$check.actual_dimensions;sha256=$check.sha256;method='API unmasked whole-frame redraw; unmodified return';user_accepted=$false;strict_PV_style_pass=$false}
 $log+=@{view=$view;api_calls=1;provider='OpenAI API';requested_model=$result.model;quality=$result.quality;response_quality=$result.response_quality;dimensions=$check.actual_dimensions;elapsed_seconds=$result.elapsed_seconds;output=$result.output_path;output_sha256=$result.output_sha256;post_generation_painting=$false;user_accepted=$false}
}
$selection=[ordered]@{
 current_selection='Latest whole-frame API redraw trials: back and side, complete spiral lock'
 selected=$selected
 drawing_provider='configured OpenAI API';requested_model='gpt-image-2.5-sunburst';quality='high'
 user_accepted=$false;strict_PV_style_pass=$false;agent_review='Complete-coil correction visible; additional shading, glints and background texture remain.'
 technical_integrity_pass=$true;api_calls_this_revision=2;dynamic_consistency_tested=$false;full_film_started=$false
 front_previous_candidate='art/20261030_pv_three_angles_v01/front/composite_1920x1080.png'
 previous_layer_composites='art/20261030_pv_three_angles_v02'
 review='art/pv_whole_redraw_pair_v01/ART_REVIEW.md'
}
Save-Json (Join-Path $root 'CURRENT_SELECTION.json') $selection
Save-Json (Join-Path $pair 'GENERATION_LOG.json') $log
$defaults=Get-Content -LiteralPath (Join-Path $root 'image_defaults.json') -Raw | ConvertFrom-Json
$defaults.quality='high'
$defaults.approval_sequence='User authorized whole-frame API redraw trials of side and back; artistic acceptance remains pending.'
Save-Json (Join-Path $root 'image_defaults.json') $defaults
$readme=@'
# 魔术之心 · PV 人物重绘

当前为**背面 F2362、侧面 F2751 的整帧 API 重绘试稿**。本轮使用已配置 OpenAI API，请求模型 `gpt-image-2.5-sunburst`、质量 `high`，各生成一次，实际均为 2560×1440。交付原图保持 API 返回字节，没有局部拼接或后续调色。

卷发按最新要求补出完整下段与收尖，侧面向胸前垂落；肤色改为较有血色的浅暖桃色。严格原 PV 的平涂一致性仍未通过：返图还有少量柔化、珠子高光和背景纹理。两张均待用户审阅，未获制作采用或动态验收。

- [背面整帧原图](art/pv_whole_redraw_back_v01/whole_PV_api_original.png)
- [侧面整帧原图](art/pv_whole_redraw_side_v01/whole_PV_api_original.png)
- [造型及画风评估](art/pv_whole_redraw_pair_v01/ART_REVIEW.md)
- [本轮调用记录](art/pv_whole_redraw_pair_v01/GENERATION_LOG.json)

![背面整帧试稿](art/pv_whole_redraw_back_v01/whole_PV_api_original.png)

![侧面整帧试稿](art/pv_whole_redraw_side_v01/whole_PV_api_original.png)

每个绘图目录保留输入、提示词、输入哈希、外发授权、请求清单、响应、原图与技术检查。`qa/` 为原尺寸局部查看图。当前选择见 `CURRENT_SELECTION.json`。

本轮字幕、背景与身体也参与了重绘，不能视为原片像素保护合成。旧三向合成、局部换头和卷发试验均保留在各自目录；前一版根目录说明与选择已备份到 `art/pv_whole_redraw_pair_v01/`。正面旧预览仍保留，未在本轮重新绘制。

原 PV 参考及分段工程位于 `D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029`，属于附件1。附件2仅用于拆解参考。当前未开始全片制作。
'@
[IO.File]::WriteAllText((Join-Path $root 'README.md'),$readme,$utf8)
$snapshot=Join-Path $pair 'scripts_snapshot'
[void][IO.Directory]::CreateDirectory($snapshot)
foreach($name in @('Invoke-ReferenceImage.ps1','Prepare-WholePVRedraw.ps1','Generate-WholePVRedraw.ps1','Audit-WholePVRedraw.py','Build-WholePVReviewCrops.ps1','Finalize-WholePVRedraw.ps1')) {
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination (Join-Path $snapshot $name)
}
$hashLines=@()
foreach($view in @('back','side')){
 $run=Join-Path $root ('art\pv_whole_redraw_'+$view+'_v01')
 foreach($file in Get-ChildItem -LiteralPath $run -File -Recurse | Sort-Object FullName){
  $hashLines+=((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()+'  '+[IO.Path]::GetRelativePath($root,$file.FullName).Replace('\','/'))
 }
}
[IO.File]::WriteAllText((Join-Path $pair 'SHA256SUMS.txt'),($hashLines -join "`n")+"`n",$utf8)
[PSCustomObject]@{api_calls=2;dimensions='2560x1440';quality='high';original_returns_unmodified=$true;strict_PV_style_pass=$false;user_accepted=$false;selection=(Join-Path $root 'CURRENT_SELECTION.json')}

