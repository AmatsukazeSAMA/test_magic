#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '1006afcd101d80cddcbc2066107e91ec82b1203686b1704c5b340eaac8d36051'){throw 'Extra whole PREP lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.extra_authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.provenance,$l.initial_provenance,$l.actual_reference_review,$l.requirements,$l.user_approved_curl_baseline,$l.api_request_policy,$l.defaults,$l.release_helper)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Exact payload/provider/authority changed'}
}
if($l.operation_kind -ne 'whole_character_redraw' -or $l.first_drawing -ne $false -or $l.planned_logical_requests -ne 1){throw 'Wrong operation metadata'}
$grant=Get-Content -LiteralPath $l.extra_authorization.path -Raw|ConvertFrom-Json
if($grant.id -ne $l.id -or $grant.operation_kind -ne $l.operation_kind -or $grant.first_drawing -ne $false -or $grant.maximum_new_logical_requests -ne 1 -or $grant.quality -ne 'high' -or $grant.n -ne 1 -or $grant.retry -ne 1){throw 'Extra authorization mismatch'}
if(Test-Path -LiteralPath $l.extra_operation_claim_path){throw 'Extra logical operation already claimed'}
$f=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.ContainsKey('Retry') -or $f.InputImages.Count -ne 3 -or $f.Size -ne '1024x1072' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot -or $f.OutputFileName -ne 'character_api_original.png' -or $f.Stage -notlike '*EXTRA_WHOLE_HAIR_REDRAW*' -or $f.Stage -like '*FIRST*'){throw 'Unexpected extra whole formal parameters'}
for($i=0;$i -lt 3;$i++){if($f.InputImages[$i] -ne $l.references[$i].path){throw 'Reference order changed'}}
$d=Get-Content -LiteralPath $l.defaults.path -Raw|ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix -or $d.api_request_policy.retry -ne 1 -or $d.api_request_policy.n -ne 1){throw 'Prefix or retry policy changed'}
if(-not ([IO.File]::ReadAllText($f.PromptFile)).StartsWith([string]$l.mandatory_prefix,[StringComparison]::Ordinal)){throw 'Exact multiline LEFT prefix missing'}
foreach($n in @('attempt.json','request_manifest.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt/release: preserve recovery only'}}
# PREVIEW ONLY: no execute/claim branch; helper returns before key and HTTP.
$v=& $l.wrapper.path @f -Preview
if($v.submitted -ne $false -or $v.n -ne 1 -or $v.retry -ne 1 -or $v.maximum_transport_attempts -ne 2 -or $v.input_count -ne 3 -or $v.mask_provided -ne $false -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected Preview route'}
if(Test-Path -LiteralPath $l.extra_operation_claim_path){throw 'Preview consumed authorization unexpectedly'}
$v
