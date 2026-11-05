#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$root=Split-Path -Parent $PSScriptRoot
$prior=Join-Path $root 'art\20261030_pv_F002306_v01\inputs'
$run=Join-Path $root 'art\20261030_pv_F002306_v02'
$inputs=Join-Path $run 'inputs'
[void][IO.Directory]::CreateDirectory($inputs)
foreach($name in @('source_F002306.png','source_F002306_detail.png','maid_turnaround_v01.png')) {
    $target=Join-Path $inputs $name
    if(-not(Test-Path -LiteralPath $target)){Copy-Item -LiteralPath (Join-Path $prior $name) -Destination $target}
}
$sheet=[Drawing.Bitmap]::new((Join-Path $inputs 'maid_turnaround_v01.png'))
$head=$null
try {
    $head=$sheet.Clone([Drawing.Rectangle]::new(230,0,200,310),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $head.Save((Join-Path $inputs 'maid_identity_head_front.png'),[Drawing.Imaging.ImageFormat]::Png)
} finally {if($head){$head.Dispose()};$sheet.Dispose()}
@{
    source_frame=2306;source_time_s=76.944;source='attachment 1 original PV';
    original_fullframe='source_F002306.png';
    original_pose_crop=@{file='source_F002306_detail.png';source_rectangle_xyxy=@(760,55,1120,1055);resampled=$false};
    identity_crop=@{file='maid_identity_head_front.png';source_file='maid_turnaround_v01.png';source_rectangle_xyxy=@(230,0,430,310);resampled=$false;role='head and hair identity only; not rendering style'};
    previous_failed_candidate_used_as_reference=$false;
    intent='A new API generation with more pixels allocated to the character, preserving the same source pose. Original frame compositing follows separately.';
    user_accepted=$false
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $run 'INPUT_PROVENANCE.json') -Encoding utf8
Write-Output 'Prepared v02 source references and native-resolution identity head crop.'
