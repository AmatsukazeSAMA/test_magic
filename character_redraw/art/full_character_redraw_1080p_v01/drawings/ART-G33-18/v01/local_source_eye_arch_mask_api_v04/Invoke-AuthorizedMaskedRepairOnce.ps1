#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '73396b07279a3e36a9e29c304c3a8c599528923f5ceecf9ffbb690e9ed572e9b'){throw 'Immutable mask repair lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.release,$l.auth,$l.provider,$l.mask,$l.mask_provenance,$l.provenance)+@($l.refs)+@($l.preserved)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Authorized mask input/evidence changed.'}}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 9 -or $f.InputImages.Count -ne 3 -or $f.MaskFile -ne $l.mask.path -or $f.Size -ne '608x1136' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact9field masked request.'}
for($i=0;$i -lt 3;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text){throw 'LEFT prefix changed.'}
$provider=$l.provider.path
if($Preview){& $provider @f -Preview;return}
foreach($n in @('attempt.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing local attempt/raw; no second call.'}}
$rp=Join-Path $PSScriptRoot 'ARTIST_API_EXECUTION_RECEIPT.json';$start=[DateTime]::UtcNow
$receipt=@{id=$l.id;operation_kind='local_eye_mask_repair';status='authorized_local_mask_invocation_started';started_utc=$start.ToString('o');formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;release_sha256=$l.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;mandatory_whole_imggen=$true}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @f;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
