#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
if(-not $Preview){throw 'PREPONLY: -Preview is mandatory. No dispatch branch exists; ROOT actual scope review and separate release are required.'}
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
$expectedLockSHA='11355881c755e975203e774d2a19d984ee710a5eb2545fad3f9f07deed2642d6'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedLockSHA){throw 'Immutable PREP lock changed.'}
$lock=Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json -AsHashtable
foreach($item in $lock.payloads){
 if(-not(Test-Path -LiteralPath $item.path -PathType Leaf)){throw "Missing locked payload: $($item.path)"}
 if((Get-FileHash -LiteralPath $item.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256){throw "Locked bytes changed: $($item.path)"}
}
$q=Get-Content -LiteralPath $lock.formal_request -Raw | ConvertFrom-Json -AsHashtable
if($q.Count -ne 8){throw 'Formal request must contain exactly eight fields.'}
foreach($key in $lock.request_exact_keys){if(-not $q.ContainsKey($key)){throw "Missing formal field $key"}}
if(($q.InputImages | ConvertTo-Json -Compress) -cne ($lock.input_order | ConvertTo-Json -Compress)){throw 'Input order changed.'}
if($q.Size -cne '1344x1024' -or $q.Quality -cne 'high' -or $q.Background -cne 'transparent'){throw 'Size/quality/background changed.'}
if($q.OutputDirectory -cne $PSScriptRoot.Replace('\','/')){throw 'Output directory changed.'}
if($q.OutputFileName -cne 'character_api_original.png'){throw 'Output basename changed.'}
foreach($name in @('attempt.json','result.json','api_response.raw.json','character_api_original.png','request_manifest.json','prompt_effective.txt')){
 if(Test-Path -LiteralPath (Join-Path $q.OutputDirectory $name)){throw "An actual attempt/output already exists; preserve it and do not reuse this PREP: $name"}
}
$cfg=Get-Content -LiteralPath $lock.public_configuration -Raw | ConvertFrom-Json
if($cfg.model -cne $lock.expected_model -or $cfg.defaults.n -ne 1){throw 'Public model/n mismatch.'}
$prompt=[IO.File]::ReadAllText($q.PromptFile)
if(-not $prompt.StartsWith([string]$lock.spatial_prefix,[StringComparison]::Ordinal)){throw 'Required full spatial prefix missing.'}
$settings=Get-Content -LiteralPath $lock.project_defaults -Raw | ConvertFrom-Json
if(-not $settings.generation_prompt_prefix.enabled -or $settings.generation_prompt_prefix.text -cne $lock.spatial_prefix){throw 'Project spatial prefix mismatch.'}
# The only wrapper call is permanently Preview. Its Preview branch returns before attempt files, credential loader or networking.
& $lock.wrapper @q -Preview
