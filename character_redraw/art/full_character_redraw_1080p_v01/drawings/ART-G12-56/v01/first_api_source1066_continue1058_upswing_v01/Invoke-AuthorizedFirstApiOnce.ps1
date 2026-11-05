#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '9ae7c475eae0c1dc75ca07a517ed6fac9d9ba3eb6d273ea22a638986961dcc88'){throw 'Lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
$fp=Join-Path $PSScriptRoot 'API_PREPARED_REQUEST.json'
if((Get-FileHash -LiteralPath $fp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.formal_sha256){throw 'Request changed.'}
$f=Get-Content -LiteralPath $fp -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 6 -or $f.Size -ne '800x976' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected first request.'}
foreach($r in $l.refs){if((Get-FileHash -LiteralPath $r.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Reference changed.'}}
if((Get-FileHash -LiteralPath $f.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.prompt_sha256){throw 'Prompt changed.'}
if((Get-FileHash -LiteralPath $l.auth_path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.auth_sha256){throw 'Authority changed.'}
if((Get-FileHash -LiteralPath $l.provider_path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $l.provider_sha256){throw 'Provider changed.'}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Model changed.'}
if($Preview){& $l.provider_path @f -Preview;return}
if(Test-Path -LiteralPath (Join-Path $PSScriptRoot 'attempt.json')){throw 'Existing attempt; no retry.'}
& $l.provider_path @f
