#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
if(-not $Preview){throw 'PREPONLY: Preview is required. This script has no dispatch branch and cannot submit.'}
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '18e8f3c88e7852679fe6cf90e601e3805e8b444d85c4eb56e7fc917d42f3d664'){throw 'PREP lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.source_audit,$l.input_review,$l.requirements,$l.configured_connection_public)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw "Changed PREP evidence: $($x.path)"}
}
if($l.generation_calls_authorized_by_this_PREP -ne 0 -or $l.submitted){throw 'PREP scope changed'}
$q=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne $l.input_count -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.Size -ne $l.size -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Prepared parameters changed'}
for($i=0;$i -lt $l.input_count;$i++){if($q.InputImages[$i] -ne $l.references[$i].path){throw 'Reference order changed'}}
$defs=Get-Content -LiteralPath $l.project_defaults_path -Raw|ConvertFrom-Json
if([string]$defs.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'Configured LEFT prefix changed'}
$pt=[IO.File]::ReadAllText($l.prompt.path)
if(-not $pt.StartsWith([string]$l.mandatory_prefix,[StringComparison]::Ordinal)){throw 'Prompt lacks exact full configured prefix'}
foreach($name in @('attempt.json','result.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'A prior attempt/return exists; preserve and recover. Never dispatch or retry here.'}
}
# Only Preview is passed, unconditionally. Wrapper returns before credentials/network/attempt writes.
& $l.wrapper.path @q -Preview
return
