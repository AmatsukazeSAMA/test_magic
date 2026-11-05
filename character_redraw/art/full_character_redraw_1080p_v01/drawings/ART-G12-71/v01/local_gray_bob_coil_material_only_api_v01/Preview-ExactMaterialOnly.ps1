#Requires -Version 7.0
param()
$ErrorActionPreference='Stop'
$taskLockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $taskLockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b0de6593f4f9876b5ba699cc16e6b0de404c62f6fb39f762a876179132866001'){throw 'Immutable PREP lock changed'}
$taskLock=Get-Content -LiteralPath $taskLockPath -Raw|ConvertFrom-Json
foreach($taskEntry in @($taskLock.formal,$taskLock.request,$taskLock.prompt,$taskLock.mask,$taskLock.wrapper,$taskLock.authorization)+@($taskLock.refs)){
 if((Get-FileHash -LiteralPath $taskEntry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskEntry.sha256){throw 'Exact PREP payload changed'}
}
foreach($taskName in @('attempt.json','result.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $taskName)){throw 'Existing execution evidence: no retry'}}
$taskFormal=Get-Content -LiteralPath $taskLock.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($taskFormal.Count -ne 8 -or $taskFormal.InputImages.Count -ne 2 -or $taskFormal.Size -ne '1312x784' -or $taskFormal.Quality -ne 'high' -or $taskFormal.Background -ne 'transparent' -or $taskFormal.MaskFile -ne $taskLock.mask.path){throw 'Prepared scope changed'}
$taskPreview=& $taskLock.wrapper.path @taskFormal -Preview
if($taskPreview.submitted -ne $false -or $taskPreview.n -ne 1 -or $taskPreview.mask_provided -ne $true -or $taskPreview.endpoint -ne 'https://api.openai.com/v1/images/edits' -or $taskPreview.model -ne 'gpt-image-2.5-sunburst'){throw 'Unexpected Preview'}
$taskRecord=[ordered]@{id='ART-G12-71';PREPONLY=$true;submitted=$false;API_calls=0;HTTP_calls=0;native_calls=0;automatic_retries=0;root_release_received=$false;formal_sha256=$taskLock.formal.sha256;lock_sha256='b0de6593f4f9876b5ba699cc16e6b0de404c62f6fb39f762a876179132866001';actual_preview=$taskPreview;technical_preview_not_art_pass=$true}
$taskPath=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION_PREPONLY.json'
if(Test-Path -LiteralPath $taskPath){throw 'Preserve existing preview record'}
[IO.File]::WriteAllText($taskPath,($taskRecord|ConvertTo-Json -Depth 12),[Text.UTF8Encoding]::new($false))
$taskRecord|ConvertTo-Json -Depth 12
