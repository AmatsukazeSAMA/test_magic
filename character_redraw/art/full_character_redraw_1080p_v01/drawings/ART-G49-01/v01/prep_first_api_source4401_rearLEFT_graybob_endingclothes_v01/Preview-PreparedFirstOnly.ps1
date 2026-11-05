#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'bd77fa62d98613e283941e82060d5e9db9eaf1d13a00e64e8ed8c20fe7b33285'){throw 'Prepared lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.provenance,$l.defaults)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Prepared evidence changed'}
}
$f=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 5 -or $f.Size -ne '1024x1072' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot -or $f.OutputFileName -ne 'character_api_original.png'){throw 'Unexpected FIRST parameters'}
for($i=0;$i -lt 5;$i++){if($f.InputImages[$i] -ne $l.references[$i].path){throw 'Reference order changed'}}
$d=Get-Content -LiteralPath $l.defaults.path -Raw|ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'LEFT prefix changed'}
if(-not ([IO.File]::ReadAllText($f.PromptFile)).StartsWith([string]$l.mandatory_prefix,[StringComparison]::Ordinal)){throw 'Prompt lacks exact full LEFT prefix'}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json','request_manifest.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing live evidence: readonly recovery only'}}
# There is intentionally no execute branch. Helper -Preview returns before key/attempt/HTTP.
$v=& $l.wrapper.path @f -Preview
if($v.submitted -ne $false -or $v.n -ne 1 -or $v.input_count -ne 5 -or $v.model -ne 'gpt-image-2.5-sunburst' -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected preview route'}
$v
