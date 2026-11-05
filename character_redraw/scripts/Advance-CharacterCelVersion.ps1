#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string[]]$Ids,[Parameter(Mandatory)][string]$Reason,[string]$UnknownRetryApproval)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$path=Join-Path $base 'REDRAW_PLAN.json'
$plan=Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
$history=@()
foreach($id in $Ids){
 $job=$plan.jobs | Where-Object id -eq $id
 $old=Join-Path $base $job.run_relative
 $number=[int]($job.run_relative.Split('/')[-1].Substring(1))+1
 $new=('drawings/'+$id+'/v'+$number.ToString('00'))
 $approvalRecord=$null
 if(Test-Path -LiteralPath (Join-Path $old 'attempt.json')){
  $a=Get-Content -LiteralPath (Join-Path $old 'attempt.json') -Raw | ConvertFrom-Json
  if($a.api_calls -eq 1 -and $a.status -ne 'api_rejected' -and -not(Test-Path -LiteralPath (Join-Path $old 'result.json'))){
   if(-not $UnknownRetryApproval){throw 'A submitted call has no known result. Do not paid-retry it without resolving the existing result or explicit user authorization.'}
   $approval=Get-Content -LiteralPath $UnknownRetryApproval -Raw | ConvertFrom-Json
   $attemptHash=(Get-FileHash -LiteralPath (Join-Path $old 'attempt.json')).Hash.ToLowerInvariant()
   $approvalRecord=@($approval.records | Where-Object { $_.id -eq $id -and [IO.Path]::GetFullPath($_.previous_run) -eq [IO.Path]::GetFullPath($old) -and $_.previous_attempt_sha256 -eq $attemptHash -and $_.next_run_relative -eq $new -and $_.api_calls_authorized -eq 1 -and $_.status -eq 'explicitly_approved_by_user' })
   if($approvalRecord.Count -ne 1 -or -not(Test-Path -LiteralPath $approvalRecord[0].recovery_audit)){throw 'Explicit approval must bind this exact unknown attempt, its recovery audit, and the single next version.'}
  }
 }
 if(Test-Path -LiteralPath (Join-Path $base $new)){throw 'New version already exists; do not overwrite.'}
 $history+=@{id=$id;previous=$job.run_relative;new=$new;reason=$Reason;utc=[DateTime]::UtcNow.ToString('o');explicit_unknown_retry_approval=if($approvalRecord){[IO.Path]::GetFullPath($UnknownRetryApproval)}else{$null}}
 $job.run_relative=$new
}
[IO.File]::WriteAllText($path,($plan | ConvertTo-Json -Depth 35),[Text.UTF8Encoding]::new($false))
foreach($record in $history){[IO.File]::AppendAllText((Join-Path $base 'VERSION_HISTORY.jsonl'),($record | ConvertTo-Json -Compress)+"`n",[Text.UTF8Encoding]::new($false))}
& (Join-Path $PSScriptRoot 'Materialize-CharacterRedraw.ps1') -Ids $Ids

