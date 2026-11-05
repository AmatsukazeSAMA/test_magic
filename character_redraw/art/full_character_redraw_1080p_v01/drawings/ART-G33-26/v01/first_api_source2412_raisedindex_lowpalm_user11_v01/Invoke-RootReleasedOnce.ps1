#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$runDir=$PSScriptRoot
$locked=Get-Content -LiteralPath (Join-Path $runDir 'EXECUTION_LOCK_v01.json') -Raw | ConvertFrom-Json
function Assert-Exact([string]$File,[string]$Hash){
 if((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Hash){throw "Immutable payload mismatch: $File"}
}
foreach($item in @($locked.immutable_prep_lock,$locked.formal_request,$locked.authorization,$locked.root_release,$locked.scope_check,$locked.wrapper,$locked.JOB,$locked.REGISTRATION_PLAN)){
 Assert-Exact $item.path $item.sha256
}
foreach($ref in $locked.references){Assert-Exact $ref.path $ref.sha256}
$prepared=Get-Content -LiteralPath $locked.formal_request.path -Raw | ConvertFrom-Json -AsHashtable
Assert-Exact $prepared.PromptFile $locked.prompt_sha256
if($prepared.Count -ne 8 -or $prepared.Size -ne '640x1040' -or $prepared.Quality -ne 'high' -or $prepared.Background -ne 'transparent' -or $prepared.InputImages.Count -ne 6){throw 'Prepared argument mismatch'}
$defaults=Get-Content -LiteralPath $locked.project_defaults_path -Raw | ConvertFrom-Json
if([string]$defaults.generation_prompt_prefix.text -cne [string]$locked.mandatory_prefix){throw 'Mandatory LEFT prefix changed; stop before sending'}
$config=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed'}
if((Test-Path -LiteralPath (Join-Path $runDir 'attempt.json')) -or (Test-Path -LiteralPath (Join-Path $runDir 'character_api_original.png'))){throw 'Existing attempt/raw: recover only, never resubmit'}
$previewPath=Join-Path $runDir 'API_PREVIEW_PROOF_v01.json'
if($Preview){
 if(Test-Path -LiteralPath $previewPath){throw 'Existing Preview evidence preserved'}
 $report=& $locked.wrapper.path @prepared -Preview
 if($report.submitted -ne $false -or $report.endpoint -ne $locked.endpoint -or $report.model -ne $locked.model -or $report.quality -ne 'high' -or $report.size -ne '640x1040' -or $report.background -ne 'transparent' -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected no-send Preview'}
 [IO.File]::WriteAllText($previewPath,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
 $report
 return
}
if(-not (Test-Path -LiteralPath $previewPath)){throw 'Successful no-send Preview required'}
$pre=Get-Content -LiteralPath $previewPath -Raw | ConvertFrom-Json
if($pre.submitted -ne $false -or $pre.endpoint -ne $locked.endpoint -or $pre.model -ne $locked.model -or $pre.size -ne '640x1040' -or $pre.quality -ne 'high' -or $pre.input_count -ne 6 -or $pre.n -ne 1){throw 'Preview evidence mismatch'}
& $locked.wrapper.path @prepared
