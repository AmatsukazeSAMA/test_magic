#Requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$PromptFile,
    [Parameter(Mandatory)][string[]]$InputImages,
    [Parameter(Mandatory)][string]$OutputDirectory,
    [string]$Size = '1536x1024',
    [ValidateSet('low','medium','high','xhigh','max','auto')][string]$Quality,
    [ValidateSet('opaque','transparent','auto')][string]$Background = 'opaque',
    [string]$OutputFileName = 'maid_turnaround_v01.png',
    [string]$Stage = 'reference image candidate',
    [string]$MaskFile,
    [switch]$Preview,
    [string]$DrawingId,
    [ValidateSet('auto','drill','loose_recolor')][string]$HairstyleMode = 'auto'
)
$ErrorActionPreference = 'Stop'
$apiRoot = 'C:\Users\11515\.agents\skills\openai-api\api'
$config = Get-Content -LiteralPath (Join-Path $apiRoot 'connection.json') -Raw | ConvertFrom-Json
if (-not $Quality) { $Quality = $config.defaults.quality }
$model = $config.model
$endpoint = 'https://api.openai.com/v1/images/edits'
$inputPromptPath = (Resolve-Path -LiteralPath $PromptFile).Path
$prompt = [IO.File]::ReadAllText($inputPromptPath)
$spatialPrefix = ''
$loosePrefix = ''
$hairstylePolicyId = $null
$hairstylePolicy = $null
$retryCount = 0
$projectRoot = Split-Path $PSScriptRoot -Parent
$projectDefaultsPath = Join-Path $projectRoot 'image_defaults.json'
if (Test-Path -LiteralPath $projectDefaultsPath) {
    $projectDefaults = Get-Content -LiteralPath $projectDefaultsPath -Raw | ConvertFrom-Json
    if ($projectDefaults.api_request_policy) {
        $retryCount = [int]$projectDefaults.api_request_policy.retry
        if ($retryCount -notin @(0,1)) { throw 'Project retry must be 0 or 1.' }
    }
    if ($null -ne $projectDefaults.source_hairstyle_policy) {
        $pointer = $projectDefaults.source_hairstyle_policy
        if (-not $pointer.path -or [string]$pointer.sha256 -notmatch '^[a-fA-F0-9]{64}$') {
            throw 'source_hairstyle_policy requires path and SHA-256.'
        }
        $policyPath = if ([IO.Path]::IsPathRooted([string]$pointer.path)) {
            [IO.Path]::GetFullPath([string]$pointer.path)
        } else {
            [IO.Path]::GetFullPath((Join-Path $projectRoot ([string]$pointer.path)))
        }
        $relativePolicyPath = [IO.Path]::GetRelativePath($projectRoot, $policyPath)
        if ([IO.Path]::IsPathRooted($relativePolicyPath) -or $relativePolicyPath -eq '..' -or $relativePolicyPath.StartsWith('..' + [IO.Path]::DirectorySeparatorChar)) {
            throw 'Source hairstyle policy must stay inside the project root.'
        }
        if ((Get-FileHash -LiteralPath $policyPath -Algorithm SHA256).Hash -ine [string]$pointer.sha256) {
            throw 'Source hairstyle policy bytes changed.'
        }
        $hairstylePolicy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json -AsHashtable
        if ($hairstylePolicy -isnot [System.Collections.IDictionary] -or $hairstylePolicy.states -isnot [System.Collections.IDictionary] -or
            $hairstylePolicy.policy_id -isnot [string] -or -not $hairstylePolicy.policy_id.Trim() -or
            $hairstylePolicy.prompt_prefix -isnot [string] -or -not $hairstylePolicy.prompt_prefix.Trim()) {
            throw 'Source hairstyle policy requires policy_id, prompt_prefix and a states object.'
        }
        foreach ($id in $hairstylePolicy.states.Keys) {
            $entry = $hairstylePolicy.states[$id]
            if (-not $id -or $entry -isnot [System.Collections.IDictionary] -or $entry.mode -cnotin @('drill','loose_recolor')) {
                throw "Invalid source hairstyle state: $id."
            }
        }
        $hairstylePolicyId = $hairstylePolicy.policy_id
    }
}
# Only complete output-directory segments identify a configured state. Stage and
# arbitrary prompt text never select a hairstyle or rewrite prepared wording.
$pathSegments = [IO.Path]::GetFullPath($OutputDirectory) -split '[\\/]'
$matchedIds = @($hairstylePolicy.states.Keys | Where-Object { $_ -in $pathSegments })
if ($matchedIds.Count -gt 1) { throw 'OutputDirectory matches multiple source hairstyle states.' }
if ($matchedIds.Count -eq 1) {
    if ($DrawingId -and $DrawingId -ine $matchedIds[0]) { throw 'DrawingId conflicts with the source hairstyle state in OutputDirectory.' }
    $DrawingId = $matchedIds[0]
}
$knownMode = 'drill'
if ($DrawingId -and $hairstylePolicy) {
    $knownId = @($hairstylePolicy.states.Keys | Where-Object { $_ -ieq $DrawingId })
    if ($knownId.Count -eq 1) { $DrawingId = $knownId[0]; $knownMode = $hairstylePolicy.states[$DrawingId].mode }
}
if ($knownMode -eq 'loose_recolor' -and $HairstyleMode -eq 'drill') {
    throw 'A known source-loose drawing cannot use the drill hairstyle override.'
}
if ($HairstyleMode -eq 'auto') { $HairstyleMode = $knownMode }
$HairstyleMode = $HairstyleMode.ToLowerInvariant()
# Compare logical newlines without rewriting an already prepared prompt.
$comparablePrompt = $prompt.Replace("`r`n", "`n").Replace("`r", "`n")
if ($HairstyleMode -eq 'loose_recolor') {
    if (-not $hairstylePolicy) { throw 'loose_recolor requires a verified source hairstyle policy.' }
    $drillPrefix = [string]$projectDefaults.generation_prompt_prefix.text
    $comparableDrillPrefix = $drillPrefix.Replace("`r`n", "`n").Replace("`r", "`n")
    if ($comparableDrillPrefix -and $comparablePrompt.Contains($comparableDrillPrefix, [StringComparison]::Ordinal)) {
        throw 'Prepared source-loose prompt contains the old drill prefix; prepare a new prompt without contradictory instructions.'
    }
    $loosePrefix = $hairstylePolicy.prompt_prefix
    $comparablePrefix = $loosePrefix.Replace("`r`n", "`n").Replace("`r", "`n")
    if (-not $comparablePrompt.StartsWith($comparablePrefix, [StringComparison]::Ordinal)) {
        $prompt = $loosePrefix + [Environment]::NewLine + [Environment]::NewLine + $prompt
    }
} elseif ($projectDefaults.generation_prompt_prefix -and $projectDefaults.generation_prompt_prefix.enabled) {
    $spatialPrefix = [string]$projectDefaults.generation_prompt_prefix.text
    $comparablePrefix = $spatialPrefix.Replace("`r`n", "`n").Replace("`r", "`n")
    if ($spatialPrefix -and -not $comparablePrompt.StartsWith($comparablePrefix, [StringComparison]::Ordinal)) {
        $prompt = $spatialPrefix + [Environment]::NewLine + [Environment]::NewLine + $prompt
    }
}
if ($prompt.Length -gt 32000) { throw 'Prompt exceeds 32000 characters.' }
$records = @($InputImages | ForEach-Object {
    $p = (Resolve-Path -LiteralPath $_).Path
    [PSCustomObject]@{path=$p;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant();bytes=(Get-Item -LiteralPath $p).Length}
})
$maskRecord=$null
if($MaskFile){$maskPath=(Resolve-Path -LiteralPath $MaskFile).Path;$maskRecord=@{path=$maskPath;sha256=(Get-FileHash -LiteralPath $maskPath -Algorithm SHA256).Hash.ToLowerInvariant();bytes=(Get-Item -LiteralPath $maskPath).Length}}
if ($Preview) {
    [PSCustomObject]@{endpoint=$endpoint;model=$model;quality=$Quality;size=$Size;background=$Background;n=1;retry=$retryCount;retry_engine='curl standard transient errors';maximum_transport_attempts=(1+$retryCount);input_count=$records.Count;mask_provided=($null -ne $maskRecord);spatial_prefix_applied=([bool]$spatialPrefix);hairstyle_prefix_applied=([bool]$loosePrefix);drawing_id=$DrawingId;hairstyle_mode=$HairstyleMode;hairstyle_policy_id=$hairstylePolicyId;effective_prompt_characters=$prompt.Length;submitted=$false}
    return
}
[void][IO.Directory]::CreateDirectory($OutputDirectory)
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
$attemptPath = Join-Path $OutputDirectory 'attempt.json'
if (Test-Path -LiteralPath $attemptPath) { throw 'This run already has an attempt record. Use a new output directory; no automatic paid retry.' }
if ([IO.Path]::GetFileName($OutputFileName) -ne $OutputFileName -or [IO.Path]::GetExtension($OutputFileName) -ne '.png') { throw 'OutputFileName must be a PNG basename.' }
$imagePath = Join-Path $OutputDirectory $OutputFileName
$responsePath = Join-Path $OutputDirectory 'api_response.raw.json'
$requestPath = Join-Path $OutputDirectory 'request_body.tmp'
$headersPath = Join-Path $OutputDirectory 'response_headers.txt'
$utf8 = [Text.UTF8Encoding]::new($false)
function Save-Json($p,$v) { [IO.File]::WriteAllText($p,($v | ConvertTo-Json -Depth 30),$utf8) }
$effectivePromptPath = Join-Path $OutputDirectory 'prompt_effective.txt'
if (Test-Path -LiteralPath $effectivePromptPath) { throw 'Existing effective prompt preserved; inspect this run before submission.' }
[IO.File]::WriteAllText($effectivePromptPath, $prompt, $utf8)
$body = @{model=$model;prompt=$prompt;n=1;size=$Size;quality=$Quality;output_format='png';background=$Background;images=@($records | ForEach-Object { @{image_url=('data:image/png;base64,'+[Convert]::ToBase64String([IO.File]::ReadAllBytes($_.path)))} })}
if($maskRecord){$body.mask=@{image_url=('data:image/png;base64,'+[Convert]::ToBase64String([IO.File]::ReadAllBytes($maskRecord.path)))}}
$manifest = @{provider='OpenAI API';endpoint=$endpoint;model=$model;quality=$Quality;size=$Size;background=$Background;n=1;output_format='png';inputs=$records;prompt_file=$effectivePromptPath;input_prompt_file=$inputPromptPath;prompt_sha256=(Get-FileHash -LiteralPath $effectivePromptPath -Algorithm SHA256).Hash.ToLowerInvariant();spatial_prefix_applied=([bool]$spatialPrefix);spatial_prefix=$spatialPrefix;input_fidelity='omitted for this model';user_accepted=$false;stage=$Stage;documentation='https://developers.openai.com/api/reference/resources/images/methods/edit'}
$manifest.retry=$retryCount
$manifest.drawing_id=$DrawingId
$manifest.hairstyle_mode=$HairstyleMode
$manifest.hairstyle_policy_id=$hairstylePolicyId
$manifest.hairstyle_prefix_applied=[bool]$loosePrefix
$manifest.hairstyle_prefix=$loosePrefix
$manifest.retry_engine='curl standard transient errors; no retry-all-errors'
$manifest.maximum_transport_attempts=1+$retryCount
if($maskRecord){$manifest.mask=$maskRecord}
Save-Json (Join-Path $OutputDirectory 'request_manifest.json') $manifest
[IO.File]::WriteAllText($requestPath,($body | ConvertTo-Json -Depth 10 -Compress),$utf8)
$started = [DateTime]::UtcNow
$attempt = @{status='prepared';started_utc=$started.ToString('o');api_calls=0;automatic_retries=0;maximum_automatic_retries=$retryCount;maximum_transport_attempts=(1+$retryCount);logical_request_count=1}
Save-Json $attemptPath $attempt
$secureKey = $null
$curlProcess = $null
try {
    $secureKey = & (Join-Path $apiRoot 'Get-OpenAIKey.ps1')
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = (Get-Command curl.exe -ErrorAction Stop).Source
    $psi.UseShellExecute=$false
    $psi.CreateNoWindow=$true
    $psi.RedirectStandardInput=$true
    $psi.RedirectStandardOutput=$true
    $psi.RedirectStandardError=$true
    foreach($a in @('--silent','--show-error','--retry',([string]$retryCount),'--connect-timeout','30','--max-time','900','--http1.1','--request','POST','--url',$endpoint,'--config','-','--header','Content-Type: application/json','--data-binary',('@'+$requestPath),'--output',$responsePath,'--dump-header',$headersPath,'--write-out','%{json}')) { $psi.ArgumentList.Add($a) }
    $curlProcess = [Diagnostics.Process]::new()
    $curlProcess.StartInfo = $psi
    $attempt.status='submitted_result_pending'
    $attempt.api_calls=1
    Save-Json $attemptPath $attempt
    [void]$curlProcess.Start()
    $bstr=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
    try {
        $curlProcess.StandardInput.WriteLine('header = "Authorization: Bearer '+[Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)+'"')
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
        $curlProcess.StandardInput.Close()
    }
    $stdoutTask=$curlProcess.StandardOutput.ReadToEndAsync()
    $stderrTask=$curlProcess.StandardError.ReadToEndAsync()
    $curlProcess.WaitForExit()
    $transportText=$stdoutTask.GetAwaiter().GetResult().Trim()
    $errorText=$stderrTask.GetAwaiter().GetResult() -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]'
    [IO.File]::WriteAllText((Join-Path $OutputDirectory 'curl_transport_metrics.json'),$transportText,$utf8)
    [IO.File]::WriteAllText((Join-Path $OutputDirectory 'curl_stderr.txt'),$errorText,$utf8)
    $transport=$transportText | ConvertFrom-Json
    $status='{0:D3}' -f [int]$transport.http_code
    $attempt.automatic_retries=[int]$transport.num_retries
    $attempt.transport_attempt_count=1+[int]$transport.num_retries
    $attempt.retry_metrics_file=Join-Path $OutputDirectory 'curl_transport_metrics.json'
    $attempt.http_response_codes=@(if(Test-Path -LiteralPath $headersPath){[regex]::Matches([IO.File]::ReadAllText($headersPath),'(?m)^HTTP/\S+\s+(\d{3})')|ForEach-Object{[int]$_.Groups[1].Value}})
    if($attempt.automatic_retries -gt $retryCount){throw 'Transport exceeded authorized retry budget.'}
    $attempt.http_status=$status
    $attempt.curl_exit_code=$curlProcess.ExitCode
    if($curlProcess.ExitCode -ne 0) { throw "Transport failed after the configured retry budget: $errorText. Preserve this result for recovery." }
    $response=[IO.File]::ReadAllText($responsePath) | ConvertFrom-Json
    if([int]$status -lt 200 -or [int]$status -ge 300) {
        $attempt.status='api_rejected'
        throw ('HTTP '+$status+': '+($response.error.message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]'))
    }
    if(@($response.data).Count -ne 1 -or -not $response.data[0].b64_json) { throw 'No expected single image in response; retain raw response and do not retry.' }
    [IO.File]::WriteAllBytes($imagePath,[Convert]::FromBase64String($response.data[0].b64_json))
    $manifest.response_quality=$response.quality
    $manifest.response_size=$response.size
    $manifest.response_background=$response.background
    $manifest.usage=$response.usage
    $manifest.created=$response.created
    $manifest.automatic_retries=$attempt.automatic_retries
    $manifest.transport_attempt_count=$attempt.transport_attempt_count
    $manifest.transport_metrics_file=$attempt.retry_metrics_file
    $manifest.output_path=$imagePath
    $manifest.output_sha256=(Get-FileHash -LiteralPath $imagePath -Algorithm SHA256).Hash.ToLowerInvariant()
    $manifest.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3)
    Save-Json (Join-Path $OutputDirectory 'result.json') $manifest
    $attempt.status='completed'
    $attempt.image=$imagePath
    Write-Output ([PSCustomObject]@{provider='OpenAI API';model=$model;quality=$Quality;image=$imagePath;elapsed_seconds=$manifest.elapsed_seconds})
} catch {
    if($attempt.status -ne 'api_rejected') { $attempt.status='failed_or_result_unknown' }
    $attempt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]'
    throw $attempt.error
} finally {
    $attempt.finished_utc=[DateTime]::UtcNow.ToString('o')
    Save-Json $attemptPath $attempt
    if($curlProcess) { $curlProcess.Dispose() }
    if($secureKey) { $secureKey.Dispose() }
    if(Test-Path -LiteralPath $requestPath) { Remove-Item -LiteralPath $requestPath -Force }
}
