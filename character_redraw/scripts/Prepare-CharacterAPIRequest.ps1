#Requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Id,
    [ValidateSet('auto_source','open','half_open','closed','profile','not_visible')][string]$SourceEyeState='auto_source',
    [int[]]$PreviousHeadCrop,
    [string]$SourceObservation
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
# Prepare sequentially: style-reference materialization uses shared GDI files.
# The resulting independent network-only requests can then run concurrently.
$buildArgs=@{Id=$Id;SourceEyeState=$SourceEyeState;BuildOnly=$true}
if($PreviousHeadCrop){$buildArgs.PreviousHeadCrop=$PreviousHeadCrop}
$prepared=& (Join-Path $PSScriptRoot 'Invoke-CharacterRedraw.ps1') @buildArgs
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$job=$plan.jobs | Where-Object id -eq $Id
$run=Join-Path $base $job.run_relative
if(-not $prepared.images -or -not $prepared.size){throw 'No prepared image request was returned.'}
if($SourceObservation){
    $note=@{id=$Id;observation=$SourceObservation;basis='Declared by the primary agent after actual current-source inspection; not artistic approval.'}
    [IO.File]::WriteAllText((Join-Path $run 'ACTUAL_SOURCE_OBSERVATION.json'),($note | ConvertTo-Json -Depth 5),[Text.UTF8Encoding]::new($false))
    [IO.File]::AppendAllText((Join-Path $run 'prompt.txt'),("`nCURRENT ACTUALLY VIEWED SOURCE OBSERVATION: "+$SourceObservation+"`n"),[Text.UTF8Encoding]::new($false))
}
$request=@{
    PromptFile=(Join-Path $run 'prompt.txt');InputImages=@($prepared.images)
    OutputDirectory=$run;Size=$prepared.size;Quality='high';Background='transparent'
    OutputFileName='character_api_original.png'
    Stage=('Full-film GOAL: '+$Id+'; G02 solid iris and continuous complete drill')
}
$target=Join-Path $run 'API_PREPARED_REQUEST.json'
[IO.File]::WriteAllText($target,($request | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
[PSCustomObject]@{id=$Id;request=$target;size=$request.Size;quality='high';api_calls=0}
