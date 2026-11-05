#Requires -Version 7.0
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '0d394714553be2de8606b93f4ff0a042689c6b1b89203f3333740a014b53224b'){throw 'PREP lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'PREP payload changed'}
}
$q=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne 5 -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected PREP parameters'}
& $l.wrapper.path @q -Preview
