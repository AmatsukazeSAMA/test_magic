#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Image,[string]$OutputDirectory)
$ErrorActionPreference='Stop'
if(-not $OutputDirectory){$OutputDirectory=Split-Path -Parent ([IO.Path]::GetFullPath($Image))}
[void][IO.Directory]::CreateDirectory($OutputDirectory)
Add-Type -AssemblyName System.Drawing
$raw=[Drawing.Bitmap]::new($Image)
try{
 foreach($name in @('white','black')){
  $qa=[Drawing.Bitmap]::new($raw.Width,$raw.Height)
  $g=[Drawing.Graphics]::FromImage($qa)
  try{
   $g.Clear($(if($name -eq 'white'){[Drawing.Color]::White}else{[Drawing.Color]::Black}))
   $g.DrawImageUnscaled($raw,0,0)
   $qa.Save((Join-Path $OutputDirectory ('qa_'+$name+'.png')),[Drawing.Imaging.ImageFormat]::Png)
  }finally{$g.Dispose();$qa.Dispose()}
 }
}finally{$raw.Dispose()}
Write-Output $OutputDirectory
