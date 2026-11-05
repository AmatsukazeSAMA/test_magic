#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$p=Join-Path $PSScriptRoot 'DIRECT_REQUEST.json'
if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'e2ef0c84e431de45226d8f409f858371592c2eceddf0fa864c5a4f1e3d0765ca'){throw 'DIRECT_REQUEST changed'}
$d=Get-Content -LiteralPath $p -Raw|ConvertFrom-Json -AsHashtable;$q=$d.parameters
if(-not $d.first_drawing -or $d.planned_logical_requests -ne 1 -or $q.Count -ne 8 -or $q.Size -ne '672x976' -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Wrong FIRST scope/parameters'}
foreach($x in @($d.provider,$d.source,$d.live_user_official_upload_confirmation)+@($d.references)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Input/provider changed'}}
if((Get-FileHash -LiteralPath $q.PromptFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $d.prompt_sha256){throw 'Prompt changed'}
$asset=Split-Path -Parent $PSScriptRoot
foreach($n in @('attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json','DISPATCH_ONCE.json')){if(Get-ChildItem -LiteralPath $asset -Recurse -File -Filter $n){throw 'Existing attempt/return: recover only, no second FIRST'}}
if(Get-ChildItem -LiteralPath $asset -Recurse -File|Where-Object Name -Match 'UNKNOWN'){throw 'Existing UNKNOWN: no restart'}
$v=& $d.provider.path @q -Preview
if($v.submitted -or $v.n -ne 1 -or $v.retry -ne 1 -or $v.input_count -ne 3 -or $v.quality -ne 'high' -or $v.background -ne 'transparent' -or $v.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Unexpected provider Preview'}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Json($path,$value){[IO.File]::WriteAllText($path,($value|ConvertTo-Json -Depth 15),$utf8)}
Save-Json (Join-Path $PSScriptRoot 'DIRECT_PREVIEW.json') $v
if($Preview){$v;return}
$f=[IO.File]::Open((Join-Path $PSScriptRoot 'DISPATCH_ONCE.json'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$data=$utf8.GetBytes($d.id+' ONE logical FIRST only; UNKNOWN recover not restart');$f.Write($data,0,$data.Length)}finally{$f.Dispose()}
$started=[DateTime]::UtcNow;$receipt=@{id=$d.id;status='official_FIRST_started';logical_requests=1;configured_retry=1;n=1;quality='high';started_utc=$started.ToString('o');request_sha256='e2ef0c84e431de45226d8f409f858371592c2eceddf0fa864c5a4f1e3d0765ca'}
$receiptPath=Join-Path $PSScriptRoot 'DIRECT_API_EXECUTION_RECEIPT.json';Save-Json $receiptPath $receipt
try{& $d.provider.path @q;$receipt.status='known_saved';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json -AsHashtable}
catch{$receipt.status='failed_or_unknown_NO_RESTART';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.wall_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Json $receiptPath $receipt}
