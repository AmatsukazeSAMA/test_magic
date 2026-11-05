#Requires -Version 7.0
[CmdletBinding()]
param([ValidateSet('side','back')][string]$View='side',[switch]$Preview)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root ('art\20261030_braid_'+$View+'_v02')
if($View -eq 'side'){
 $names=@('edit_base_portrait.png','user_side_back_hair.png','front_braid_shape_reference.png','source_PV_head_style.png')
 $size='1024x1536'
} else {
 $names=@('previous_head.png','user_back_bob_detail.png','user_side_back_hair.png','source_PV_head_style.png')
 $size='1024x1024'
}
$images=@($names | ForEach-Object {Join-Path $run ('inputs\'+$_)})
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile (Join-Path $run 'prompt.txt') -InputImages $images -OutputDirectory $run -Quality high -Size $size -Background transparent -OutputFileName 'head_api_original.png' -Stage ($View+' local correction: braid orientation/length and latest back-bob reference; original PV body retained') -Preview:$Preview
