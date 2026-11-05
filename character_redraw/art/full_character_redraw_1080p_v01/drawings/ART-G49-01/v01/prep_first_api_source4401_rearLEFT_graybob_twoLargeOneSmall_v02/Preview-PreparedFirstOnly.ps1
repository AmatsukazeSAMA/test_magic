#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'fab6d1709e481148129abd84312e9a6c72a9d882747a3ff5fc47c32c3f226dad'){throw 'Prepared lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.provenance,$l.initial_provenance,$l.actual_reference_review,$l.requirements,$l.api_request_policy,$l.defaults,$l.release_helper)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Prepared input/provider/policy changed'}
}
$f=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.ContainsKey('Retry') -or $f.InputImages.Count -ne 5 -or $f.Size -ne '1024x1072' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot -or $f.OutputFileName -ne 'character_api_original.png'){throw 'Unexpected FIRST parameters'}
for($i=0;$i -lt 5;$i++){if($f.InputImages[$i] -ne $l.references[$i].path){throw 'Input order changed'}}
$d=Get-Content -LiteralPath $l.defaults.path -Raw|ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix -or [int]$d.api_request_policy.retry -ne 1 -or [int]$d.api_request_policy.n -ne 1 -or $d.api_request_policy.quality -ne 'high'){throw 'Defaults prefix/retry policy changed'}
if(-not ([IO.File]::ReadAllText($f.PromptFile)).StartsWith([string]$l.mandatory_prefix,[StringComparison]::Ordinal)){throw 'Exact full LEFT prefix missing'}
foreach($n in @('attempt.json','request_manifest.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing live/release evidence: readonly recovery only'}}
# PREVIEW ONLY: no execute branch. Provider returns before key/attempt/HTTP.
$v=& $l.wrapper.path @f -Preview
if($v.submitted -ne $false -or $v.n -ne 1 -or $v.retry -ne 1 -or $v.maximum_transport_attempts -ne 2 -or $v.input_count -ne 5 -or $v.mask_provided -ne $false -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected Preview route/retry budget'}
$v
