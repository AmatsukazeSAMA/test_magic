#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
if(-not $Preview){throw 'PREPONLY: this runner only permits -Preview. Root must inspect inputs and use the separate release helper.'}
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '118f33720bbef21e75caaf67f103df81b6421808cf4b918e809a6455919683f8'){throw 'PREP lock changed'}
$l=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.predecessor_gate)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'PREP payload changed'}
}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt/result: recover only'}}
$f=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 5 -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $l.retry -ne 1){throw 'Unexpected FIRST fields'}
for($i=0;$i -lt 5;$i++){if($f.InputImages[$i] -ne $l.references[$i].path){throw 'Reference order changed'}}
# The provider owns default lookup; validate the exact prompt prefix here without key access.
if(-not ([IO.File]::ReadAllText($l.prompt.path)).StartsWith([string]$l.mandatory_prefix,[StringComparison]::Ordinal)){throw 'Mandatory prefix changed'}
$result=& $l.wrapper.path @f -Preview
$proofPath=Join-Path $PSScriptRoot 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $proofPath){throw 'Preserve existing Preview evidence'}
[IO.File]::WriteAllText($proofPath,($result|ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
$result|ConvertTo-Json -Depth 8
