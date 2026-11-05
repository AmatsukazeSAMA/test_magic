#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'ROOT_MASKED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '0739725c71b8c82dce267468e0b868d7baa7c6a5554c97646e9006bdfc93c4ea'){throw 'Immutable masked call lock changed.'}
$l=Get-Content -LiteralPath $lp -Raw -Encoding UTF8|ConvertFrom-Json
foreach($x in @($l.formal,$l.prompt,$l.mask,$l.release,$l.auth,$l.provider,$l.config)+@($l.refs)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Reviewed input/evidence changed.'}
}
$f=Get-Content -LiteralPath $l.formal.path -Raw -Encoding UTF8|ConvertFrom-Json -AsHashtable
if($f.Count -ne 8 -or $f.InputImages.Count -ne $l.expected_reference_count -or $f.MaskFile -ne $l.mask.path -or $f.Size -ne $l.expected_size -or $f.Quality -ne 'high' -or $f.Background -ne 'transparent' -or $f.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected masked request.'}
for($i=0;$i -lt $l.expected_reference_count;$i++){if($f.InputImages[$i] -ne $l.refs[$i].path){throw 'Reference order changed.'}}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw -Encoding UTF8|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $l.prefix_text){throw 'LEFT prefix changed.'}
$f.Stage='GOAL '+$l.id+' one masked local intermediate; whole imggen and fresh art/photography review mandatory'
if($Preview){& $l.provider.path @f -Preview;return}
foreach($n in @('attempt.json','character_api_original.png','result.json','api_response.raw.json','ROOT_API_EXECUTION_RECEIPT.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $n)){throw 'Existing attempt/result; no second call.'}
}
$rp=Join-Path $PSScriptRoot 'ROOT_API_EXECUTION_RECEIPT.json'
$started=[DateTime]::UtcNow
$receipt=@{id=$l.id;operation_kind='local_mask_repair';status='authorized_local_mask_invocation_started';started_utc=$started.ToString('o');formal_sha256=$l.formal.sha256;mask_sha256=$l.mask.sha256;release_sha256=$l.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;mandatory_whole_imggen=$true;intermediate_only=$true}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $l.provider.path @f;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw -Encoding UTF8|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
