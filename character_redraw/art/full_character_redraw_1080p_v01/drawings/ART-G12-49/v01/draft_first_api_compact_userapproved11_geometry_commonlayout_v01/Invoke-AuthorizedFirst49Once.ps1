#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$celDirectory=Split-Path -Parent $PSScriptRoot
$requestPath=Join-Path $celDirectory 'API_PREPARED_REQUEST.json'
$formalSha=(Get-FileHash -LiteralPath $requestPath -Algorithm SHA256).Hash.ToLowerInvariant()
if($formalSha -ne '9c9bda6407119a6d582f39874c8244d90528d724da05bc44303ba7c729e5a3fe'){throw 'Formal request changed.'}
$formal=Get-Content -LiteralPath $requestPath -Raw | ConvertFrom-Json -AsHashtable
$draftPath=Join-Path $PSScriptRoot 'DRAFT_API_REQUEST.json'
if((Get-FileHash -LiteralPath $draftPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b45f7063653b369846a433abf36cfc9d25cff9a2217d78ace3e29123be8bb93e'){throw 'Immutable draft changed.'}
$draft=Get-Content -LiteralPath $draftPath -Raw | ConvertFrom-Json
if($formal.Count -ne 8 -or $formal.Size -ne '656x1040' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.InputImages.Count -ne 6){throw 'Unexpected exact request.'}
if((Get-FileHash -LiteralPath $formal.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne '22059861ce6647dca384943080506bddd8ae1fce6c8a0c61134ca8f44277738c'){throw 'Prompt changed.'}
for($i=0;$i -lt 6;$i++){
    if($formal.InputImages[$i] -ne $draft.InputImages[$i]){throw 'Reference path changed.'}
    if((Get-FileHash -LiteralPath $formal.InputImages[$i] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $draft.reference_sha256[$i]){throw 'Reference bytes changed.'}
}
$projectRoot='D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01'
$authPath=Join-Path $projectRoot 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
if((Get-FileHash -LiteralPath $authPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'){throw 'Project authorization changed.'}
$registry=Get-Content -LiteralPath (Join-Path $projectRoot 'ASSET_REGISTRY.json') -Raw | ConvertFrom-Json
$previous=$registry.'ART-G12-48'
if(-not $previous.primary_static_pass -or -not $previous.independent_static_pass -or $previous.sha256 -ne 'e69349aa27decf395526a8a33a7c63f3a1b850a791736d2659fcb4d18bb7daa7'){throw 'Previous48 reviewed state changed.'}
$config=Get-Content -LiteralPath 'C:\Users\11515\.agents\skills\openai-api\api\connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured image model changed.'}
$scriptPath='D:\CODEX\魔术之心\scripts\Invoke-ReferenceImage.ps1'
$scope=Get-Content -LiteralPath (Join-Path $celDirectory 'PROJECT_SCOPE_REFERENCE_RELEASE.json') -Raw | ConvertFrom-Json
if((Get-FileHash -LiteralPath $scriptPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $scope.provider_script.sha256){throw 'Provider script changed.'}
if($Preview){& $scriptPath @formal -Preview;return}
if(Test-Path -LiteralPath (Join-Path $celDirectory 'attempt.json')){throw 'Existing attempt; no retry permitted.'}
$receiptPath=Join-Path $celDirectory 'ARTIST_API_EXECUTION_RECEIPT.json'
if(Test-Path -LiteralPath $receiptPath){throw 'Artist invocation already recorded; no second call.'}
$started=[DateTime]::UtcNow
$receipt=@{id='ART-G12-49';status='approved_invocation_started';started_utc=$started.ToString('o');formal_request_sha256=$formalSha;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;root_release_sha256='4f4a5781eb6ae66e1ebb5ef68546899cf38af1eac134d51cff50a2cde164c70f';project_authorization_sha256='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt | ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{
    & $scriptPath @formal
    $receipt.status='provider_script_returned'
    $receipt.provider_result=Get-Content -LiteralPath (Join-Path $celDirectory 'result.json') -Raw | ConvertFrom-Json
}catch{
    $receipt.status='failed_or_unknown_no_retry'
    $receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]'
    throw
}finally{
    $receipt.finished_utc=[DateTime]::UtcNow.ToString('o')
    $receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3)
    Save-Receipt
}
