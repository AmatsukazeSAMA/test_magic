#Requires -Version 7.0
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'b9442b63668c1e154a784b31349912488f3adf7dd14aa23ca1cfb98072b147b2'){throw 'Immutable request lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.release,$l.auth,$l.provider)+@($l.refs)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Exact authorized inputs changed'}}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne 6 -or $f.Size -ne '816x1072' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected request'}
for($i=0;$i -lt 6;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed'}}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt; recovery only'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Model changed'}
$start=[DateTime]::UtcNow;$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json'
$r=@{id=$l.id;status='one_escalated_transport_started';started_utc=$start.ToString('o');n=1;automatic_retry=0;endpoint='https://api.openai.com/v1/images/edits';formal_sha256=$l.formal.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($r|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$r.status='provider_script_returned';$r.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$r.status='failed_or_unknown_no_retry';$r.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$r.finished_utc=[DateTime]::UtcNow.ToString('o');$r.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
