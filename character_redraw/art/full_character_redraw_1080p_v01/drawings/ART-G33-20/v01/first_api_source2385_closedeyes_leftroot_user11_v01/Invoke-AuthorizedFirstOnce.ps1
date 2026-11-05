#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$runDir=$PSScriptRoot
$locked=Get-Content -LiteralPath (Join-Path $runDir 'REQUEST_LOCK.json') -Raw | ConvertFrom-Json
function Assert-ExactFile([string]$File,[string]$Expected){
    if((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Expected){throw "Input/request lock mismatch: $File"}
}
Assert-ExactFile $locked.prepared_request.path $locked.prepared_request.sha256
Assert-ExactFile $locked.authorization.path $locked.authorization.sha256
Assert-ExactFile $locked.root_release.path $locked.root_release.sha256
Assert-ExactFile $locked.wrapper.path $locked.wrapper.sha256
Assert-ExactFile $locked.JOB.path $locked.JOB.sha256
Assert-ExactFile $locked.REGISTRATION_PLAN.path $locked.REGISTRATION_PLAN.sha256
foreach($ref in $locked.references){Assert-ExactFile $ref.path $ref.sha256}
$prepared=Get-Content -LiteralPath $locked.prepared_request.path -Raw | ConvertFrom-Json -AsHashtable
Assert-ExactFile $prepared.PromptFile $locked.prompt_sha256
if($prepared.Count -ne 8 -or $prepared.Size -ne '624x1072' -or $prepared.Quality -ne 'high' -or $prepared.Background -ne 'transparent' -or $prepared.InputImages.Count -ne 6){throw 'Unexpected request shape or payload'}
if(Test-Path -LiteralPath (Join-Path $runDir 'attempt.json')){throw 'Existing attempt: recover; never retry automatically'}
if(Test-Path -LiteralPath (Join-Path $runDir 'character_api_original.png')){throw 'Existing raw image: do not resubmit'}
& $locked.wrapper.path @prepared
