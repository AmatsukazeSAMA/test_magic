#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string[]]$Ids,[string]$Round='round01',[ValidateRange(1,6)][int]$Workers=4)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$chosen=@($plan.jobs | Where-Object id -in $Ids)
if($chosen.Count -ne $Ids.Count){throw 'Invalid or repeated drawing IDs.'}
if(@($chosen | Group-Object group | Where-Object Count -gt 1).Count){throw 'Do not run two dependent cels from the same group in one round.'}
$jobs=@();$records=@()
foreach($id in $Ids){
 while(@($jobs | Where-Object State -eq Running).Count -ge $Workers){
  $finished=Wait-Job -Job @($jobs | Where-Object State -eq Running) -Any -Timeout 1
  if($finished){Receive-Job -Job $finished -ErrorAction Continue | Write-Output}
 }
 $jobs+=Start-ThreadJob -ThrottleLimit $Workers -ArgumentList $root,$id -ScriptBlock {
  param($taskRoot,$drawingId)
  $ErrorActionPreference='Stop'
  try{
   & (Join-Path $taskRoot 'scripts\Invoke-CharacterRedraw.ps1') -Id $drawingId | Out-Null
   $taskBase=Join-Path $taskRoot 'art\full_character_redraw_1080p_v01'
   $taskPlan=Get-Content -LiteralPath (Join-Path $taskBase 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
   $taskSpec=$taskPlan.jobs | Where-Object id -eq $drawingId
   $celRun=Join-Path $taskBase $taskSpec.run_relative
   $py='C:\Users\11515\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
   $PSNativeCommandUseErrorActionPreference=$false
   $auditOutput=& $py (Join-Path $taskRoot 'scripts\Audit-CharacterCel.py') $celRun 2>&1
   if($LASTEXITCODE -ne 0){throw 'Integrity/alpha diagnostic failed; preserve result and hold.'}
   [PSCustomObject]@{id=$drawingId;status='returned_needs_visual_review'}
  }catch{[PSCustomObject]@{id=$drawingId;status='failed_or_hold';error=($_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]')}}
 }
}
Wait-Job -Job $jobs | Out-Null
foreach($job in $jobs){Receive-Job -Job $job -ErrorAction Continue | Write-Output;Remove-Job -Job $job}
& (Join-Path $PSScriptRoot 'Build-CharacterReview.ps1') -Ids $Ids -Round $Round

