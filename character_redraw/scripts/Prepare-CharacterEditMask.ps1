#Requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Id)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$base=Join-Path $root 'art\full_character_redraw_1080p_v01'
$plan=Get-Content -LiteralPath (Join-Path $base 'REDRAW_PLAN.json') -Raw | ConvertFrom-Json
$job=$plan.jobs | Where-Object id -eq $Id
if($job.kind -ne 'body_pose' -or $job.group -in @('G01','G02','G06','G07') -or -not $job.source_panel_id){return}
$run=Join-Path $base $job.run_relative
$mattePath=Join-Path $plan.source_project ('layers\'+$job.source_panel_id+'\subject_visible.png')
if(-not(Test-Path -LiteralPath $mattePath)){return}
Add-Type -AssemblyName System.Drawing
if(-not('CelBodyProtection' -as [type])){
 Add-Type -ReferencedAssemblies @('System.Drawing.Common','System.Drawing.Primitives','System.Runtime','System.Runtime.InteropServices') -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public static class CelBodyProtection {
 public static void Save(Bitmap source, string target) {
  Rectangle rect=new Rectangle(0,0,source.Width,source.Height);
  BitmapData bits=source.LockBits(rect,ImageLockMode.ReadWrite,PixelFormat.Format32bppArgb);
  byte[] b=new byte[bits.Stride*source.Height];
  Marshal.Copy(bits.Scan0,b,0,b.Length);
  for(int y=0;y<source.Height;y++) for(int x=0;x<source.Width;x++) {
   int i=y*bits.Stride+x*4;
   bool retain=y>=source.Height*.40 && b[i+3]>32 && Math.Max(b[i],Math.Max(b[i+1],b[i+2]))<100;
   b[i]=b[i+1]=b[i+2]=255;b[i+3]=(byte)(retain?255:0);
  }
  Marshal.Copy(b,0,bits.Scan0,b.Length);source.UnlockBits(bits);
  source.Save(target,ImageFormat.Png);
 }
}
'@
}
$original=[Drawing.Bitmap]::new($mattePath)
$c=$job.crop_xyxy
$crop=$original.Clone([Drawing.Rectangle]::new([int]$c[0],[int]$c[1],[int]($c[2]-$c[0]),[int]($c[3]-$c[1])),[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$guide=[Drawing.Bitmap]::new([int]$job.output_size[0],[int]$job.output_size[1],[Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g=[Drawing.Graphics]::FromImage($guide)
$target=Join-Path $run 'inputs\body_ink_protection_mask.png'
try{
 $g.Clear([Drawing.Color]::Transparent)
 $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
 $s=[Math]::Min(($guide.Width-24)/[double]$crop.Width,($guide.Height-24)/[double]$crop.Height)
 $dx=($guide.Width-$crop.Width*$s)/2;$dy=($guide.Height-$crop.Height*$s)/2
 $g.DrawImage($crop,[Drawing.RectangleF]::new([single]$dx,[single]$dy,[single]($crop.Width*$s),[single]($crop.Height*$s)))
 $g.Dispose();$g=$null
 [CelBodyProtection]::Save($guide,$target)
}finally{if($g){$g.Dispose()};$guide.Dispose();$crop.Dispose();$original.Dispose()}
[IO.File]::WriteAllText((Join-Path $run 'MASK_INTENT.json'),(@{source=$mattePath;purpose='Guide API to preserve observed lower-body dark ink, garment silhouette and shoe/leg placement. Head, fill colors and background remain editable.';mask_is_advisory=$true;source_semantics_needs_review=$true;no_final_art_painted_locally=$true} | ConvertTo-Json),[Text.UTF8Encoding]::new($false))
Write-Output $target

