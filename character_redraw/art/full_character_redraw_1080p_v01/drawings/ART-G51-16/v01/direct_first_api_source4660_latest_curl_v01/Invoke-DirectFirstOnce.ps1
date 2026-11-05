#Requires -Version 7.0
$ErrorActionPreference='Stop'
$record=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $record -Algorithm SHA256).Hash.ToLowerInvariant() -ne '3d6cc11ca3b2986ead4a68e0d4d62d6376dfc20061b0bf1f4220c195324dcda3'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $record -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if($d.id -ne 'ART-G51-16' -or -not $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne '720x944' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong FIRST parameters'}
foreach($x in @($d.provider,$d.source,$d.live_user_official_upload_confirmation,$d.requirements)+@($d.references)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input or provider changed'}}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
$asset=Split-Path -Parent $PSScriptRoot
foreach($n in @('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json','FIRST_DISPATCH_ONCE.json')){if(Get-ChildItem -LiteralPath $asset -Recurse -File -Filter $n){throw 'Existing target attempt/return: recover only'}}
if(Get-ChildItem -LiteralPath $asset -Recurse -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing UNKNOWN: no restart'}
$p=& $d.provider.path @q -Preview
if($p.submitted -or $p.n -ne 1 -or $p.retry -ne 1 -or $p.input_count -ne 4 -or $p.quality -ne 'high' -or $p.background -ne 'transparent' -or $p.model -ne 'gpt-image-2.5-sunburst' -or $p.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false);[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($p|ConvertTo-Json -Depth 8),$utf8)
$once=[IO.File]::Open((Join-Path $PSScriptRoot 'FIRST_DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G51-16 ONE logical FIRST only');$once.Write($bytes,0,$bytes.Length)}finally{$once.Dispose()}
$started=[DateTime]::UtcNow;$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G51-16';status='official_FIRST_started';operation_kind='first_drawing';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');direct_request_sha256='3d6cc11ca3b2986ead4a68e0d4d62d6376dfc20061b0bf1f4220c195324dcda3'}
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 10),$utf8)}
Save-Receipt
try{& $d.provider.path @q;$receipt.status='known_saved_return';$r=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json;$receipt.image_sha256=$r.output_sha256;$receipt.actual_retries=$r.automatic_retries;$receipt.provider_elapsed_seconds=$r.elapsed_seconds}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
