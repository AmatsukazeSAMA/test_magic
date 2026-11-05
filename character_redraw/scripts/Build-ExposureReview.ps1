#Requires -Version 7.0
[CmdletBinding()]
param(
 [Parameter(Mandatory)][string]$Chapter,
 [ValidateSet('all','unresolved','task_samples')][string]$Scope='all',
 [ValidateRange(1,64)][int]$PerPage=16
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$coverage=Join-Path $base 'coverage'
$ledger=Get-Content -LiteralPath (Join-Path $coverage 'EXPOSURE_LEDGER.json') -Raw | ConvertFrom-Json
$rows=@($ledger.frames | Where-Object chapter_id -eq $Chapter)
if(-not $rows.Count){throw 'No such source chapter.'}
if($Scope -eq 'unresolved'){$rows=@($rows | Where-Object source_status -eq 'unresolved_candidate')}
if($Scope -eq 'task_samples'){
 $tasks=Get-Content -LiteralPath (Join-Path $coverage 'UNRESOLVED_REVIEW_TASKS.json') -Raw | ConvertFrom-Json
 $samples=@($tasks.tasks | Where-Object {$_.key[0] -eq $Chapter} | ForEach-Object {
  $f=$_.frames
  $f[0];$f[[int][Math]::Floor(($f.Count-1)/2)];$f[-1]
 } | Sort-Object -Unique)
 $rows=@($rows | Where-Object frame -in $samples)
}
if(-not $rows.Count){throw 'No source frames selected.'}
$out=Join-Path $coverage ('review\'+$Chapter+'_'+$Scope)
[void][IO.Directory]::CreateDirectory($out)
$utf8=[Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Drawing
$font=[Drawing.Font]::new('Arial',11)
$small=[Drawing.Font]::new('Arial',9)
$tileW=480;$tileH=310;$cols=4
$pages=@()
try{
 for($offset=0;$offset -lt $rows.Count;$offset+=$PerPage){
  $selected=@($rows | Select-Object -Skip $offset -First $PerPage)
  $nrows=[int][Math]::Ceiling($selected.Count/[double]$cols)
  $sheet=[Drawing.Bitmap]::new($cols*$tileW,$nrows*$tileH)
  $g=[Drawing.Graphics]::FromImage($sheet)
  $paths=@()
  try{
   $g.Clear([Drawing.Color]::FromArgb(244,244,244))
   $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
   for($i=0;$i -lt $selected.Count;$i++){
    $row=$selected[$i]
    $path=Join-Path $coverage $row.source_frame
    $paths+=$path
    $im=[Drawing.Bitmap]::new($path)
    $x=($i%$cols)*$tileW;$y=[int][Math]::Floor($i/[double]$cols)*$tileH
    try{$g.DrawImage($im,[Drawing.Rectangle]::new($x,$y+40,480,270))}finally{$im.Dispose()}
    $g.DrawString(('F'+$row.frame+' / '+$row.chapter_id+' / '+$row.source_status),$font,[Drawing.Brushes]::Black,$x+3,$y+2)
    $ids=if($row.proposed_canonical_ids.Count){$row.proposed_canonical_ids -join ','}else{$row.candidate_ids -join ','}
    $g.DrawString(('Candidate: '+$ids),$small,[Drawing.Brushes]::DarkSlateGray,$x+3,$y+22)
   }
   $file=Join-Path $out ('page_'+([int]($offset/$PerPage)+1).ToString('00')+'.png')
   $sheet.Save($file,[Drawing.Imaging.ImageFormat]::Png)
   $pages+=@{image=$file;frames=@($selected.frame);source_paths=$paths;scope='Visual review evidence only; no automatic binding or acceptance'}
  }finally{$g.Dispose();$sheet.Dispose()}
 }
}finally{$font.Dispose();$small.Dispose()}
$manifest=@{chapter=$Chapter;scope=$Scope;selected_frame_count=$rows.Count;page_count=$pages.Count;pages=$pages;actual_reviewed=$false}
[IO.File]::WriteAllText((Join-Path $out 'INDEX.json'),($manifest | ConvertTo-Json -Depth 15),$utf8)
[PSCustomObject]@{chapter=$Chapter;scope=$Scope;frames=$rows.Count;pages=$pages.Count;directory=$out;binding_decisions=0}
