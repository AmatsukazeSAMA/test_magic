#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '3e76258dab32fbf764f7b05fcd8b705cb019f860efdb397073dd2bb220ba8e26'){throw 'Immutable mask repair lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.release,$l.auth,$l.scope,$l.provider,$l.mask,$l.mask_provenance)+@($l.refs)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Authorized input/evidence changed.'}}
$f=Get-Content -LiteralPath $l.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($f.Count -ne 9 -or $f.InputImages.Count -ne 5 -or $f.MaskFile -ne $l.mask.path -or $f.Size -ne '1136x1392' -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact masked request.'}
for($i=0;$i -lt 5;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text){throw 'LEFT prefix changed.'}
if($Preview){& $l.provider.path @f -Preview;return}
foreach($n in @('attempt.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt/raw; no second call.'}}
$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json';$start=[DateTime]::UtcNow
$receipt=@{id=$l.id;operation_kind='local_headpose_aperture_mask_repair';status='authorized_local_mask_invocation_started';started_utc=$start.ToString('o');formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;release_sha256=$l.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;mandatory_whole_imggen=$true}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
