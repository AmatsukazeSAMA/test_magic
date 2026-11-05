#Requires -Version 7.0
# Preview only. This script has no live-dispatch branch and grants no release.
$ErrorActionPreference = 'Stop'
$lockPath = Join-Path $PSScriptRoot 'PREPARED_PAYLOAD_LOCK.json'
if ((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'c842a26f881fd68862066b2b907b050576f02f8ed93ffe3462fdb6a280b95ccf') {
    throw 'Prepared payload lock changed.'
}
$lock = Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
foreach ($record in @($lock.formal, $lock.prompt, $lock.mask, $lock.mask_provenance, $lock.provider, $lock.connection_config, $lock.project_defaults_at_prepare, $lock.user_scope, $lock.local_repair_status, $lock.prep_scope_gates) + @($lock.refs)) {
    if ((Get-FileHash -LiteralPath $record.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.sha256) { throw 'Prepared evidence changed.' }
}
$formal = Get-Content -LiteralPath $lock.formal.path -Raw | ConvertFrom-Json -AsHashtable
if ($formal.Count -ne 8 -or $formal.InputImages.Count -ne 4 -or $formal.Size -ne '960x1648' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.MaskFile -ne $lock.mask.path -or $formal.OutputDirectory -ne $PSScriptRoot) { throw 'Unexpected exact prepared request.' }
for ($i = 0; $i -lt 4; $i++) { if ($formal.InputImages[$i] -ne $lock.refs[$i].path) { throw 'Input order changed.' } }
if (@('attempt.json', 'api_response.raw.json', 'response_headers.txt', 'character_api_original.png', 'ROOT_API_EXECUTION_RECEIPT.json') | Where-Object { Test-Path -LiteralPath (Join-Path $PSScriptRoot $_) }) { throw 'Attempt or output exists; preserve and inspect.' }
$config = Get-Content -LiteralPath $lock.connection_config.path -Raw | ConvertFrom-Json
if ($config.model -ne 'gpt-image-2.5-sunburst') { throw 'Configured model changed.' }
$result = & $lock.provider.path @formal -Preview
if ($result.submitted -or -not $result.mask_provided -or $result.input_count -ne 4 -or $result.n -ne 1 -or $result.endpoint -ne 'https://api.openai.com/v1/images/edits') { throw 'Unexpected preview result.' }
$result | ConvertTo-Json -Depth 10
