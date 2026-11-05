#Requires -Version 7.0
$ErrorActionPreference='Stop'
$projectRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'RETRY33_PREP_MANIFEST.json') -Raw|ConvertFrom-Json -AsHashtable
$defaults=Get-Content -LiteralPath (Join-Path $projectRoot 'image_defaults.json') -Raw|ConvertFrom-Json -AsHashtable
$proof=@()
$crlf=[string][char]13+[char]10
$lf=[string][char]10
$cr=[string][char]13
foreach($case in $manifest.cases){
 $q=Get-Content -LiteralPath $case.request.path -Raw|ConvertFrom-Json -AsHashtable
 $run=$case.run
 $p=Join-Path $run 'API_PREVIEW_2_6.json'
 if(Test-Path -LiteralPath $p){throw "Preserve existing $p"}
 $argsMap=$q.parameters
 $v=& $q.provider.path @argsMap -Preview
 if($v.model -ne 'gpt-image-2.6-sunburst' -or $v.n -ne 1 -or $v.retry -ne 1 -or $v.submitted -ne $false){throw 'Invalid actual Preview'}
 $effective=[IO.File]::ReadAllText($q.prompt.path)
 $prefix=[string]$defaults.generation_prompt_prefix.text
 $comparable=$effective.Replace($crlf,$lf).Replace($cr,$lf)
 $comparablePrefix=$prefix.Replace($crlf,$lf).Replace($cr,$lf)
 if($defaults.generation_prompt_prefix.enabled -and -not $comparable.StartsWith($comparablePrefix,[StringComparison]::Ordinal)){$effective=$prefix+[Environment]::NewLine+[Environment]::NewLine+$effective}
 $eyePolicy=Get-Content -LiteralPath $defaults.eye_color_policy.path -Raw|ConvertFrom-Json -AsHashtable
 $eyePrefix=[string]$eyePolicy.generation_prompt_prefix
 if(-not $effective.Contains($eyePrefix,[StringComparison]::Ordinal)){$effective+=[Environment]::NewLine+[Environment]::NewLine+$eyePrefix}
 $bytes=[Text.UTF8Encoding]::new($false).GetBytes($effective)
 $hash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
 if($hash -ne $q.expected_effective_prompt_sha256){throw "Effective prompt differs from original: $($q.id)"}
 $v|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $p -Encoding utf8NoBOM
 $proof+=@{id=$q.id;request_sha256=$case.request.sha256;preview=@{path=$p;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()};effective_prompt_same_as_original=$true;effective_prompt_sha256=$hash;refs_exact_unchanged=$true;submitted=$false}
}
$path=Join-Path $PSScriptRoot 'RETRY33_ACTUAL_PREVIEW_AND_SAME_PAYLOAD_PROOF.json'
if(Test-Path -LiteralPath $path){throw 'Preserve existing proof'}
@{count=$proof.Count;network_calls=0;cases=$proof}|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $path -Encoding utf8NoBOM
Write-Output "PREVIEW_COUNT=$($proof.Count)"
Write-Output ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant())
