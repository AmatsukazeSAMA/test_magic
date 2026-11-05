#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$delivery=Join-Path $root 'art\20261030_pv_three_angles_v01'
$specs=@(
 @{view='front';frame=2306;time=76.944;study='20261030_head_style_front_v03';review='Front closed eyes and pose retained; flat gray bob and warm-ivory skin; neck bottom outline excluded to retain source collar attachment.'},
 @{view='side';frame=2751;time=91.792;study='20261030_head_style_side_v01';review='Independent left-facing profile, one open eye and small open mouth; original picture border restored from source F2686; neck polygon and front foot skin correction visually inspected.'},
 @{view='back';frame=2362;time=78.812;study='20261030_head_style_back_v01';review='Independent rear head, short bob nape and own-left accessory root only; long curl remains occluded toward front; original pose and source foot crop retained.'}
)
$selected=@()
foreach($s in $specs){
 $run=Join-Path $delivery $s.view
 $checkPath=Join-Path $run 'COMPOSITING_CHECK.json'
 $check=Get-Content -LiteralPath $checkPath -Raw | ConvertFrom-Json -AsHashtable
 if(-not $check.technical_pass -or $check.unexpected_changed_pixels_outside_head_and_body_skin -ne 0 -or $check.changed_original_dark_ink_pixels_outside_head -ne 0){throw ('Failed protection check: '+$s.view)}
 $check.agent_artistic_review_pending=$false;$check.agent_artistic_satisfied=$true
 $check | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $checkPath -Encoding utf8
 $art=@{view=$s.view;frame=$s.frame;agent_satisfied=$true;user_accepted=$false;scope='static original-PV head replacement preview';review=$s.review;reviewed_files=@('composite_1920x1080.png','head_detail.png','source_comparison.png');identity_skin_reference='original supplied character; median RGB 254,244,238';postprocessing='API actual drawing plus explicit non-generative palette correction, original-body skin color correction and layered compositing';limits=@('head line edges cleaner than compressed source video','not a claim of original author stroke recovery','no adjacent-frame or dynamic test','4K body/background are resampled from 1080p source')}
 $art | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $run 'ART_REVIEW.json') -Encoding utf8
 $selected+=@{view=$s.view;source_frame=$s.frame;source_time_s=$s.time;source_attachment=1;head_study=('art/'+$s.study);composite=('art/20261030_pv_three_angles_v01/'+$s.view+'/composite_1920x1080.png');view_4k=('art/20261030_pv_three_angles_v01/'+$s.view+'/composite_3840x2160_view.png');head_alpha=('art/20261030_pv_three_angles_v01/'+$s.view+'/head_layer_1920x1080.png');agent_satisfied=$true;user_accepted=$false}
}
$allRuns=@('20261030_maid_turnaround_v01','20261030_pv_F002306_v01','20261030_pv_F002306_v02','20261030_head_style_front_v03','20261030_head_style_side_v01','20261030_head_style_back_v01')
$calls=@()
foreach($name in $allRuns){
 $run=Join-Path $root ('art\'+$name)
 $r=Get-Content -LiteralPath (Join-Path $run 'result.json') -Raw | ConvertFrom-Json
 $a=Get-Content -LiteralPath (Join-Path $run 'attempt.json') -Raw | ConvertFrom-Json
 if($a.status -ne 'completed' -or $a.api_calls -ne 1 -or $r.quality -ne 'high'){throw ('Unexpected request status or quality: '+$name)}
 $inputs=@()
 foreach($input in $r.inputs){
  $actual=(Get-FileHash -LiteralPath $input.path -Algorithm SHA256).Hash.ToLowerInvariant()
  if($actual -ne $input.sha256){throw ('Generation input changed after submission: '+$input.path)}
  $inputs+=@{path=$input.path;sha256=$actual;matches_request=$true}
 }
 $actual=(Get-FileHash -LiteralPath $r.output_path -Algorithm SHA256).Hash.ToLowerInvariant()
 if($actual -ne $r.output_sha256){throw ('API original changed: '+$name)}
 $im=[Drawing.Bitmap]::new($r.output_path)
 try {$dimensions=@($im.Width,$im.Height)} finally {$im.Dispose()}
 $calls+=@{run=$name;api_calls=1;provider=$r.provider;requested_model=$r.model;quality=$r.quality;response_quality=$r.response_quality;requested_size=$r.size;response_size=$r.response_size;actual_dimensions=$dimensions;elapsed_seconds=$r.elapsed_seconds;status=$a.status;inputs=$inputs;original_output=$r.output_path;original_output_sha256=$actual;original_unchanged=$true}
}
@{project_api_calls=$calls.Count;api_calls_since_resolution_request=4;calls=$calls;automatic_paid_retries=0;default_quality='high'} | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath (Join-Path $delivery 'GENERATION_LOG.json') -Encoding utf8
@{current_selection='three static original-PV head-replacement previews';date='2026-10-30';review='art/20261030_pv_three_angles_v01/REVIEW.md';overview='art/20261030_pv_three_angles_v01/three_angles_character_overview.png';head_overview='art/20261030_pv_three_angles_v01/three_angles_heads_overview.png';drawing_provider='configured OpenAI API';quality='high';body_source='attachment 1 original PV; original shoulder and uniform structure';skin_reference='initial supplied school-uniform character';skin_base_rgb=@(254,244,238);agent_satisfied=$true;user_accepted=$false;dynamic_consistency_tested=$false;full_film_started=$false;selected=$selected} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $root 'CURRENT_SELECTION.json') -Encoding utf8
$snapshot=Join-Path $delivery 'scripts_snapshot'
[void][IO.Directory]::CreateDirectory($snapshot)
foreach($name in @('PVPalette.cs','Match-PVHeadPalette.ps1','Compose-PVAngle.ps1','Build-ThreeAngleReview.ps1','Prepare-PVHeadStudies.ps1','Generate-PVHeadStudy.ps1','Invoke-ReferenceImage.ps1','Finalize-ThreeAngleReview.ps1')){Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination (Join-Path $snapshot $name)}
$sumPath=Join-Path $delivery 'SHA256SUMS.txt'
$lines=@(Get-ChildItem -LiteralPath $delivery -Recurse -File | Where-Object {$_.FullName -ne $sumPath} | Sort-Object FullName | ForEach-Object {
 (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()+' *'+[IO.Path]::GetRelativePath($delivery,$_.FullName).Replace('\','/')
})
$lines | Set-Content -LiteralPath $sumPath -Encoding utf8
[pscustomobject]@{angles=3;agent_review='satisfied for static previews';protected_pixel_checks='3/3 passed';generation_input_hashes='all preserved';api_original_hashes='all preserved';project_calls=$calls.Count;calls_since_resolution_request=4;delivery=$delivery;user_accepted=$false}
