#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$taskRun=$PSScriptRoot
$taskLockPath=Join-Path $taskRun 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $taskLockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'e96ade722bb6e46f28bf0b7dec5601668201783fc29d464b27d593338e6af3c3'){throw 'Exact lock changed'}
$taskLock=Get-Content -LiteralPath $taskLockPath -Raw | ConvertFrom-Json
foreach($taskEntry in @($taskLock.formal,$taskLock.draft,$taskLock.prompt,$taskLock.wrapper,$taskLock.auth)+@($taskLock.refs)){
    if((Get-FileHash -LiteralPath $taskEntry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskEntry.sha256){throw ('Exact input changed: '+$taskEntry.path)}
}
foreach($taskName in @('attempt.json','result.json','character_api_original.png','api_response.raw.json')){
    if(Test-Path -LiteralPath (Join-Path $taskRun $taskName)){throw ('Existing execution evidence: '+$taskName)}
}
$taskFormal=Get-Content -LiteralPath $taskLock.formal.path -Raw | ConvertFrom-Json -AsHashtable
if($taskFormal.Count -ne 8 -or $taskFormal.Size -ne '1312x784' -or $taskFormal.Quality -ne 'high' -or $taskFormal.Background -ne 'transparent' -or $taskFormal.InputImages.Count -ne 6){throw 'Formal scope mismatch'}
$taskPreview=& $taskLock.wrapper.path @taskFormal -Preview
if($taskPreview.submitted -ne $false -or $taskPreview.n -ne 1 -or $taskPreview.endpoint -ne 'https://api.openai.com/v1/images/edits' -or $taskPreview.model -ne 'gpt-image-2.5-sunburst'){throw 'Preview mismatch'}
$taskRecord=[ordered]@{id='ART-G12-71';PREPONLY=$true;submitted=$false;API_calls=0;HTTP_calls=0;native_calls=0;automatic_retries=0;root_release_received=$false;formal_sha256=$taskLock.formal.sha256;lock_sha256='e96ade722bb6e46f28bf0b7dec5601668201783fc29d464b27d593338e6af3c3';actual_preview=$taskPreview;technical_preview_not_art_pass=$true}
$taskPreviewPath=Join-Path $taskRun 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $taskPreviewPath){throw 'Preserve existing preview evidence'}
[IO.File]::WriteAllText($taskPreviewPath,($taskRecord|ConvertTo-Json -Depth 12),[Text.UTF8Encoding]::new($false))
$taskRecord|ConvertTo-Json -Depth 12
