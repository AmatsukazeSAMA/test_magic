#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$utf8=[Text.UTF8Encoding]::new($false)
$views=@{
 back=@{frame=2362;time_s=78.812;study='20261030_head_style_back_v01'}
 side=@{frame=2751;time_s=91.792;study='20261030_head_style_side_v01'}
}
foreach($view in @('back','side')) {
 $spec=$views[$view]
 $run=Join-Path $root ('art\pv_whole_redraw_'+$view+'_v01')
 if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')) {throw "An attempt already exists for $view; preserve the run."}
 $inputs=Join-Path $run 'inputs'
 [void][IO.Directory]::CreateDirectory($inputs)
 $sources=[ordered]@{
  '01_original_PV_frame.png'=('art\'+$spec.study+'\inputs\source_frame.png')
  '02_original_identity_turnaround.png'='art\20261030_maid_turnaround_v01\inputs\identity_turnaround.png'
  '03_user_hair_side_and_back.png'='art\20261030_braid_revision_refs\user_side_back_hair.png'
  '04_user_back_bob_detail.png'='art\20261030_braid_revision_refs\user_back_bob_detail.png'
  '05_original_PV_head_line_style.png'=('art\'+$spec.study+'\inputs\source_head_style.png')
 }
 $inputRecords=@()
 foreach($entry in $sources.GetEnumerator()) {
  $source=Join-Path $root $entry.Value
  if(-not(Test-Path -LiteralPath $source)) {throw "Missing input: $source"}
  $dest=Join-Path $inputs $entry.Key
  Copy-Item -LiteralPath $source -Destination $dest
  $inputRecords+=@{file=('inputs/'+$entry.Key);source=$source;sha256=(Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()}
 }
 $record=[ordered]@{
  user_request='Use the configured API to redraw the entire image. Restore the complete spiral lock, not deletion of its broken part.'
  view=$view;source_attachment=1;source_frame=$spec.frame;source_time_s=$spec.time_s
  method='One unmasked whole-frame image-edit request. Deliver decoded API output unchanged.'
  body_and_background='Redrawn by API with the original PV composition, pose, maid costume and lettering as reference.'
  braid='One continuous silver-gray and mint spiral on anatomical left, two red beads at its root, complete tapered tip. Sweep toward front; keep visible rear curl beside outer left shoulder.'
  target_skin_rgb=@(252,232,220);quality='high';requested_size='2560x1440';n=1
  post_generation_painting=$false;local_cut_and_paste=$false;user_accepted=$false
  inputs=$inputRecords
 }
 [IO.File]::WriteAllText((Join-Path $run 'INTENT.json'),($record | ConvertTo-Json -Depth 15),$utf8)
}

