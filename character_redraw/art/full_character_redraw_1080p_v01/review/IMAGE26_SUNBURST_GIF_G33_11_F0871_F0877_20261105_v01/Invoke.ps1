$ErrorActionPreference = 'Stop'
$endpoint = 'https://api.openai.com/v1/images/generations'
$requestPath = Join-Path $PSScriptRoot 'REQUEST.json'
$key = & 'C:/Users/11515/.agents/skills/openai-api/api/Get-OpenAIKey.ps1'
try {
    $attemptPath = Join-Path $PSScriptRoot 'GIF_ATTEMPT.json'
    $attempt = [ordered]@{ endpoint = $endpoint; model = 'gpt-image-2.6-sunburst'; request_sha256 = (Get-FileHash -LiteralPath $requestPath -Algorithm SHA256).Hash.ToLowerInvariant(); started_utc = [DateTime]::UtcNow.ToString('o') }
    $lock = [IO.File]::Open($attemptPath, [IO.FileMode]::CreateNew)
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes(($attempt | ConvertTo-Json))
        $lock.Write($bytes, 0, $bytes.Length)
    } finally { $lock.Dispose() }
    $timer = [Diagnostics.Stopwatch]::StartNew()
    try {
        $response = Invoke-WebRequest -Uri $endpoint -Method Post -Authentication Bearer -Token $key -ContentType 'application/json' -InFile $requestPath -TimeoutSec 600 -SkipHttpErrorCheck
    } catch {
        $attempt['state'] = 'transport_error_or_unknown_delivery'
        $attempt['elapsed_seconds'] = $timer.Elapsed.TotalSeconds
        $attempt['error'] = $_.Exception.Message
        $attempt | ConvertTo-Json | Set-Content -LiteralPath $attemptPath -Encoding utf8NoBOM
        throw
    }
    $attempt['elapsed_seconds'] = $timer.Elapsed.TotalSeconds
    $attempt['http_status'] = [int]$response.StatusCode
    $attempt['request_id'] = ($response.Headers['x-request-id'] -join ',')
    [IO.File]::WriteAllText((Join-Path $PSScriptRoot 'response.raw.json'), [string]$response.Content, [Text.UTF8Encoding]::new($false))
    $attempt['state'] = 'response_saved'
    $attempt | ConvertTo-Json | Set-Content -LiteralPath $attemptPath -Encoding utf8NoBOM
    $body = $response.Content | ConvertFrom-Json
    if ($response.StatusCode -lt 200 -or $response.StatusCode -ge 300) {
        throw ('HTTP {0} {1}: {2}' -f $response.StatusCode, $body.error.code, $body.error.message)
    }
    $gif = [Convert]::FromBase64String($body.data[0].b64_json)
    if ($gif.Length -lt 6 -or [Text.Encoding]::ASCII.GetString($gif, 0, 6) -notin 'GIF87a','GIF89a') {
        throw 'The response did not contain GIF bytes.'
    }
    $out = Join-Path $PSScriptRoot 'sunburst26_dance_probe.gif'
    [IO.File]::WriteAllBytes($out, $gif)
    $attempt['state'] = 'gif_saved'
    $attempt['gif_sha256'] = (Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash.ToLowerInvariant()
    $attempt | ConvertTo-Json | Set-Content -LiteralPath $attemptPath -Encoding utf8NoBOM
    $attempt | ConvertTo-Json
} finally { if ($null -ne $key) { $key.Dispose() } }
