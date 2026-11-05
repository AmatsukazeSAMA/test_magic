#Requires -Version 7.0
$ErrorActionPreference='Stop'
$record=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $record -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'a8355ea2095fb866feae9b3f5c997924fc7eead298cb986d54d940c0d16a18d4'){throw 'Direct request changed'}
$d=Get-Content -LiteralPath $record -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if($d.id -ne 'ART-G48-06' -or $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne '1680x576' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong correction parameters'}
foreach($x in @($d.provider,$d.source,$d.live_user_official_upload_confirmation,$d.requirements)+@($d.references)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
foreach($n in @('attempt.json','result.json','character_api_original.png','request_manifest.json','prompt_effective.txt','CORRECTION_DISPATCH_ONCE.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing correction attempt/return: recover only'}}
if(Get-ChildItem -LiteralPath $PSScriptRoot -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing UNKNOWN: no restart'}
$p=& $d.provider.path @q -Preview
if($p.submitted -or $p.n -ne 1 -or $p.retry -ne 1 -or $p.input_count -ne 4 -or $p.quality -ne 'high' -or $p.background -ne 'transparent' -or $p.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider route'}
$utf8=[Text.UTF8Encoding]::new($false);[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json'),($p|ConvertTo-Json -Depth 8),$utf8)
$once=[IO.File]::Open((Join-Path $PSScriptRoot 'CORRECTION_DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=$utf8.GetBytes('ART-G48-06 ONE logical source coherent FRONT shoulder correction only');$once.Write($bytes,0,$bytes.Length)}finally{$once.Dispose()}
$started=[DateTime]::UtcNow;$receiptPath=Join-Path $PSScriptRoot 'EXECUTION_RECEIPT_SOL.json'
$receipt=@{id='ART-G48-06';status='official_frontshoulder_correction_started';operation_kind='whole_character_redraw';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');direct_request_sha256='a8355ea2095fb866feae9b3f5c997924fc7eead298cb986d54d940c0d16a18d4'}
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 10),$utf8)}
Save-Receipt
try{& $d.provider.path @q;$receipt.status='known_saved_return';$r=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json;$receipt.image_sha256=$r.output_sha256;$receipt.actual_retries=$r.automatic_retries;$receipt.provider_elapsed_seconds=$r.elapsed_seconds}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
