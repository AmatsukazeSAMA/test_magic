#Requires -Version 7.0
$ErrorActionPreference='Stop'
$projectRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
$base=Join-Path $projectRoot 'art/full_character_redraw_1080p_v01'
$facts=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'SOURCE_FACTS.json') -Raw|ConvertFrom-Json -AsHashtable
$cases=@()
foreach($id in ($facts.Keys|Sort-Object)){
 $run=@(Get-ChildItem -LiteralPath (Join-Path $base "drawings/$id/v01") -Directory -Filter '*minimal_v21')
 if($run.Count -ne 1){continue}
 $r=$run[0].FullName
 $qPath=Join-Path $r 'DIRECT_REQUEST.json'
 $q=Get-Content -LiteralPath $qPath -Raw|ConvertFrom-Json -AsHashtable
 $p=Join-Path $r 'API_PREVIEW_2_6.json'
 if(-not(Test-Path -LiteralPath $p)){
  $argsMap=$q.parameters
  $preview=& $q.provider.path @argsMap -Preview
  if($preview.model -ne 'gpt-image-2.6-sunburst' -or $preview.retry -ne 1){throw 'Preview model/retry mismatch'}
  $preview|ConvertTo-Json -Depth 30|Set-Content -LiteralPath $p -Encoding utf8NoBOM
 }
 $cases+=@{id=$id;source_frame=$q.source_frame;source_pts=$q.source_pts;run=$r;request=@{path=$qPath;sha256=(Get-FileHash -LiteralPath $qPath -Algorithm SHA256).Hash.ToLower()};prompt=$q.prompt;preview=@{path=$p;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower()};lock=@{path=(Join-Path $r 'PREPARATION_LOCK.json');sha256=(Get-FileHash -LiteralPath (Join-Path $r 'PREPARATION_LOCK.json') -Algorithm SHA256).Hash.ToLower()};refs=$q.refs}
}
$manifest=@{prepared_utc=[datetime]::UtcNow.ToString('o');count=$cases.Count;scope='FIRST preparation only, no submissions or central changes';logical_submissions=0;root_actual_refs_review_and_release_required=$true;cases=$cases}
$manifest|ConvertTo-Json -Depth 30|Set-Content -LiteralPath (Join-Path $PSScriptRoot 'PREP_MANIFEST_CURRENT.json') -Encoding utf8NoBOM
Write-Output "PREP_COUNT=$($cases.Count)"
