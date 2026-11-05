#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6fb25b504f95cb7983aed79fd7e69bbb6b3e69c5992cbcca4de345c513e167af'){throw 'FIRST PREP lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.provenance,$l.initial_provenance,$l.actual_reference_review,$l.requirements,$l.curl_baseline,$l.api_request_policy,$l.defaults,$l.release_helper)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Exact prepared input/provider/policy changed'}
}
if($l.operation_kind -ne 'first_drawing' -or $l.first_drawing -ne $true -or $l.planned_logical_requests -ne 1){throw 'Unexpected FIRST metadata'}
$f=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.ContainsKey('Retry') -or $f.InputImages.Count -ne 5 -or $f.Size -ne '832x1008' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot -or $f.OutputFileName -ne 'character_api_original.png' -or $f.Stage -notlike '*FIRST*'){throw 'Unexpected FIRST parameters'}
for($i=0;$i -lt 5;$i++){if($f.InputImages[$i] -ne $l.references[$i].path){throw 'Reference order changed'}}
$d=Get-Content -LiteralPath $l.defaults.path -Raw|ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix -or $d.api_request_policy.retry -ne 1 -or $d.api_request_policy.n -ne 1){throw 'Prefix or transport policy changed'}
$logicalPrompt=([IO.File]::ReadAllText($f.PromptFile)).Replace("`r`n","`n").Replace("`r","`n")
$logicalPrefix=([string]$l.mandatory_prefix).Replace("`r`n","`n").Replace("`r","`n")
if(-not $logicalPrompt.StartsWith($logicalPrefix,[StringComparison]::Ordinal)){throw 'Full multiline LEFT prefix missing'}
$asset=Split-Path -Parent $PSScriptRoot
foreach($n in @('attempt.json','result.json','request_manifest.json','character_api_original.png','character_imggen_original.png','ROOT_API_EXECUTION_RECEIPT.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json')){
 if(Get-ChildItem -LiteralPath $asset -Recurse -File -Filter $n){throw 'Existing attempt/return/release: preserve recovery only'}
}
if(Get-ChildItem -LiteralPath $asset -Recurse -File|Where-Object Name -Match 'UNKNOWN'){throw 'Unknown artifact: recover before new FIRST'}
# No execute branch. Explicit Preview returns before credentials/attempt/HTTP.
$v=& $l.wrapper.path @f -Preview
if($v.submitted -ne $false -or $v.n -ne 1 -or $v.retry -ne 1 -or $v.maximum_transport_attempts -ne 2 -or $v.input_count -ne 5 -or $v.mask_provided -ne $false -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected Preview route'}
$v | ConvertTo-Json -Depth 10
