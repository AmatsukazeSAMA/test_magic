#Requires -Version 7.0
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
public static class PVAlphaScan {
  public static int[] Bounds(byte[] b,int w,int h,int stride) {
    int minx=w,miny=h,maxx=-1,maxy=-1,clear=0,soft=0,solid=0;
    for(int y=0;y<h;y++)for(int x=0;x<w;x++) {
      int a=b[y*stride+x*4+3];
      if(a==0)clear++;else if(a==255)solid++;else soft++;
      if(a>16){if(x<minx)minx=x;if(y<miny)miny=y;if(x>maxx)maxx=x;if(y>maxy)maxy=y;}
    }
    return new int[]{minx,miny,maxx+1,maxy+1,clear,soft,solid};
  }
  public static int ChangedOutside(byte[] a,byte[] b,int w,int h,int stride,int x0,int y0,int x1,int y1) {
    int n=0;
    for(int y=0;y<h;y++)for(int x=0;x<w;x++) {
      if(x>=x0&&x<x1&&y>=y0&&y<y1)continue;
      int i=y*stride+x*4;
      if(a[i]!=b[i]||a[i+1]!=b[i+1]||a[i+2]!=b[i+2])n++;
    }
    return n;
  }
}
'@
$root=Split-Path -Parent $PSScriptRoot
$run=Join-Path $root 'art\20261030_pv_F002306_v01'
function Pixels([Drawing.Bitmap]$im) {
    $r=[Drawing.Rectangle]::new(0,0,$im.Width,$im.Height)
    $bits=$im.LockBits($r,[Drawing.Imaging.ImageLockMode]::ReadOnly,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        if($bits.Stride -lt 0){throw 'Unexpected bottom-up PNG buffer.'}
        $bytes=[byte[]]::new($bits.Stride*$im.Height)
        [Runtime.InteropServices.Marshal]::Copy($bits.Scan0,$bytes,0,$bytes.Length)
        return @{bytes=$bytes;stride=$bits.Stride}
    } finally {$im.UnlockBits($bits)}
}
function Save-Png([Drawing.Bitmap]$im,[string]$name) {$im.Save((Join-Path $run $name),[Drawing.Imaging.ImageFormat]::Png)}
$source=[Drawing.Bitmap]::new((Join-Path $run 'inputs\source_F002306.png'))
$raw=[Drawing.Bitmap]::new((Join-Path $run 'pv_character_api_raw.png'))
$rgba=$plate=$composite=$checker=$comparison=$null
try {
    $w=1920;$h=1080
    if($source.Width -ne $w -or $source.Height -ne $h){throw 'Unexpected original dimensions.'}
    if($raw.Width -ne 2048 -or $raw.Height -ne 1152){throw 'Unexpected API dimensions.'}
    $rawPixels=Pixels $raw
    $rawInfo=[PVAlphaScan]::Bounds($rawPixels.bytes,$raw.Width,$raw.Height,$rawPixels.stride)
    if($rawInfo[4] -eq 0){throw 'API result has no transparent pixels.'}
    $roi=[Drawing.Rectangle]::new(720,48,470,1012)
    $rgba=[Drawing.Bitmap]::new($w,$h,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g=[Drawing.Graphics]::FromImage($rgba)
    try {
        $g.Clear([Drawing.Color]::Transparent)
        $g.SetClip($roi)
        $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
        $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.PixelOffsetMode=[Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.DrawImage($raw,[Drawing.Rectangle]::new(0,0,$w,$h),0,0,$raw.Width,$raw.Height,[Drawing.GraphicsUnit]::Pixel)
    } finally {$g.Dispose()}
    Save-Png $rgba 'character_F002306_1920x1080.png'
    $px=Pixels $rgba
    $alpha=[PVAlphaScan]::Bounds($px.bytes,$w,$h,$px.stride)
    $pink=$source.GetPixel(770,70)
    $plate=[Drawing.Bitmap]::new($w,$h,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g=[Drawing.Graphics]::FromImage($plate)
    try {
        $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
        $g.DrawImageUnscaled($source,0,0)
        $brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(255,$pink.R,$pink.G,$pink.B))
        try {$g.FillRectangle($brush,$roi)} finally {$brush.Dispose()}
    } finally {$g.Dispose()}
    Save-Png $plate 'background_and_lyrics_F002306.png'
    $composite=[Drawing.Bitmap]::new($w,$h,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g=[Drawing.Graphics]::FromImage($composite)
    try {
        $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceCopy
        $g.DrawImageUnscaled($plate,0,0)
        $g.CompositingMode=[Drawing.Drawing2D.CompositingMode]::SourceOver
        $g.DrawImageUnscaled($rgba,0,0)
    } finally {$g.Dispose()}
    Save-Png $composite 'pv_F002306_composited.png'
    $srcpx=Pixels $source;$outpx=Pixels $composite
    $outsideChanged=[PVAlphaScan]::ChangedOutside($srcpx.bytes,$outpx.bytes,$w,$h,$srcpx.stride,720,48,1190,1060)
    if($outsideChanged -ne 0){throw "Unexpected changed pixels outside replacement ROI: $outsideChanged"}
    $checker=[Drawing.Bitmap]::new($w,$h,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g=[Drawing.Graphics]::FromImage($checker)
    $light=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(225,225,225))
    $dark=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(190,190,190))
    try {
        for($y=0;$y -lt $h;$y+=32){for($x=0;$x -lt $w;$x+=32){$b=if((($x/32)+($y/32))%2 -eq 0){$light}else{$dark};$g.FillRectangle($b,$x,$y,32,32)}}
        $g.DrawImageUnscaled($rgba,0,0)
    } finally {$g.Dispose();$light.Dispose();$dark.Dispose()}
    Save-Png $checker 'character_checker_preview.png'
    $comparison=[Drawing.Bitmap]::new(1080,1200,[Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g=[Drawing.Graphics]::FromImage($comparison)
    $font=[Drawing.Font]::new('Microsoft YaHei',24,[Drawing.FontStyle]::Regular,[Drawing.GraphicsUnit]::Pixel)
    $ink=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(55,48,50))
    try {
        $g.Clear([Drawing.Color]::FromArgb(247,243,240))
        $g.DrawString('原片 F2306',$font,$ink,35,16)
        $g.DrawString('描改试稿 v01 · high',$font,$ink,575,16)
        $g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.DrawImage($source,[Drawing.Rectangle]::new(25,65,490,1095),720,40,470,1050,[Drawing.GraphicsUnit]::Pixel)
        $g.DrawImage($composite,[Drawing.Rectangle]::new(565,65,490,1095),720,40,470,1050,[Drawing.GraphicsUnit]::Pixel)
    } finally {$g.Dispose();$font.Dispose();$ink.Dispose()}
    Save-Png $comparison 'comparison_character.png'
    $result=@{
      status='PASS: technical compositing checks; art remains a candidate';source_frame=2306;source_time_s=76.944;source_pts=1231104;time_base='1/16000';
      source_dimensions=@($w,$h);api_dimensions=@($raw.Width,$raw.Height);resample='2048x1152 to 1920x1080, high-quality bicubic, no pose warping or translation';
      replacement_roi_xyxy=@(720,48,1190,1060);replacement_background_rgb=@($pink.R,$pink.G,$pink.B);background_method='original frame retained outside ROI; former character rectangle filled with sampled original flat pink; no author background recovery claimed';
      raw_alpha_bbox_gt16=@($rawInfo[0],$rawInfo[1],$rawInfo[2],$rawInfo[3]);raw_alpha_zero_pixels=$rawInfo[4];raw_alpha_partial_pixels=$rawInfo[5];raw_alpha_opaque_pixels=$rawInfo[6];
      character_alpha_bbox_gt16=@($alpha[0],$alpha[1],$alpha[2],$alpha[3]);outside_replacement_roi_changed_rgb_pixels=$outsideChanged;
      user_accepted=$false;api_calls=1;output='pv_F002306_composited.png';character='character_F002306_1920x1080.png';comparison='comparison_character.png'
    }
    $result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $run 'COMPOSITING_CHECK.json') -Encoding utf8
    $result | ConvertTo-Json -Depth 10
} finally {
    foreach($im in @($source,$raw,$rgba,$plate,$composite,$checker,$comparison)){if($im){$im.Dispose()}}
}
