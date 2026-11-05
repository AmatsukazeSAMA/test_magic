# Offline regression against the actual provider's Preview path; no credential or HTTP operation.
$ErrorActionPreference='Stop'
$projectRoot='D:/CODEX/魔术之心'
$provider=Join-Path $projectRoot 'scripts/Invoke-ReferenceImage.ps1'
$defaults=Get-Content -Raw -LiteralPath (Join-Path $projectRoot 'image_defaults.json') | ConvertFrom-Json
$prefix=[string]$defaults.generation_prompt_prefix.text
$bodyText='本地换行预览核查，不提交。'
$utf8=[Text.UTF8Encoding]::new($false)
$out=Join-Path $PSScriptRoot 'RESULT.json'
if(Test-Path -LiteralPath $out){throw 'Existing test evidence preserved.'}
$inputs=Join-Path $PSScriptRoot 'inputs'
[void][IO.Directory]::CreateDirectory($inputs)
$cases=@(
 @{name='LF_prefix_already_present';text=($prefix+"`n`n"+$bodyText)},
 @{name='CRLF_prefix_already_present';text=($prefix.Replace("`n","`r`n")+"`r`n`r`n"+$bodyText)},
 @{name='prefix_absent';text=$bodyText}
)
$results=@()
foreach($case in $cases){
 $promptPath=Join-Path $inputs ($case.name+'.txt')
 if(Test-Path -LiteralPath $promptPath){throw 'Existing fixture preserved.'}
 [IO.File]::WriteAllText($promptPath,$case.text,$utf8)
 $run=Join-Path $PSScriptRoot $case.name
 $preview=& $provider -PromptFile $promptPath -InputImages @((Join-Path $projectRoot 'art/full_character_redraw_1080p_v01/inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png')) -OutputDirectory $run -OutputFileName 'never_generated.png' -Size '1024x1024' -Quality high -Background transparent -Stage 'OFFLINE_PREFIX_PREVIEW_NO_SUBMISSION' -Preview
 $expected=if($case.name -eq 'prefix_absent'){$prefix.Length+2*[Environment]::NewLine.Length+$bodyText.Length}else{$case.text.Length}
 if($preview.submitted -ne $false -or $preview.effective_prompt_characters -ne $expected){throw ('Prefix regression: '+$case.name)}
 if($preview.n -ne 1 -or $preview.retry -ne 1 -or $preview.maximum_transport_attempts -ne 2){throw 'Request policy changed.'}
 if(Test-Path -LiteralPath $run){throw 'Preview unexpectedly created a request output directory.'}
 $results+=@{case=$case.name;expected_effective_characters=$expected;observed_effective_characters=$preview.effective_prompt_characters;submitted=$preview.submitted;passed=$true}
}
$result=@{cases=$results;all_passed=$true;network_calls=0;generation_calls=0;credential_read=$false;old_request_records_modified=$false;before_wrapper_sha256=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1.before') -Algorithm SHA256).Hash.ToLowerInvariant();after_wrapper_sha256=(Get-FileHash -LiteralPath $provider -Algorithm SHA256).Hash.ToLowerInvariant();recorded_utc=[DateTime]::UtcNow.ToString('o')}
[IO.File]::WriteAllText($out,($result|ConvertTo-Json -Depth 8),$utf8)
$result|ConvertTo-Json -Depth 8
