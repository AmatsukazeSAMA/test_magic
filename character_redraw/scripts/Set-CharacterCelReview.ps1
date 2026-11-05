#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string[]]$Ids,[Parameter(Mandatory)][string]$Observation,[switch]$Hold)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
foreach($id in $Ids){
 $job=$plan.jobs | Where-Object id -eq $id
 $run=Join-Path $base $job.run_relative
 if(-not(Test-Path -LiteralPath (Join-Path $run 'character_api_original.png')) -and -not(Test-Path -LiteralPath (Join-Path $run 'character_api_cel.png'))){throw 'Cannot review an image that has not returned.'}
 $record=@{scope='Actual agent visual inspection of source and correctly alpha-composited API return';observation=$Observation;continue_family=(-not $Hold);status=$(if($Hold){'HOLD'}else{'candidate_for_continued_trial'});strict_PV_style_pass=$false;user_accepted=$false;dynamic_consistency_tested=$false;reviewed_utc=[DateTime]::UtcNow.ToString('o')}
 [IO.File]::WriteAllText((Join-Path $run 'VISUAL_REVIEW.json'),($record | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
}

