using System;
public static class PVPaletteV2 {
 static byte Clamp(double x) { return (byte)Math.Max(0,Math.Min(255,Math.Round(x))); }
 static void BlendInk(byte[] p,int i,int r,int g,int b,double t) {
  t=Math.Max(0,Math.Min(1,t));if(t>0.97)t=1;
  p[i+2]=Clamp(23+t*(r-23));p[i+1]=Clamp(21+t*(g-21));p[i]=Clamp(20+t*(b-20));
 }
 public static int[] GradeHead(byte[] p,int w,int h,int stride) {
  int changed=0,skin=0,hair=0,white=0,mint=0,red=0,alpha=0,ink=0;
  for(int y=0;y<h;y++)for(int x=0;x<w;x++){
   int i=y*stride+x*4,b=p[i],g=p[i+1],r=p[i+2],a=p[i+3];
   if(a==0)continue;
   bool core=Math.Max(r,Math.Max(g,b))<35;
   if(r>65&&r>g+4&&g>b+2&&g>r*0.6&&b>r*0.5){BlendInk(p,i,252,232,220,(r-23)/231.0);skin++;}
   else if(r>90&&r>g*1.8&&r>b*1.8&&g<100){BlendInk(p,i,181,28,36,(r-23)/158.0);red++;}
   else if(r>70&&g>r+6&&g>b+4){BlendInk(p,i,177,207,187,(g-21)/186.0);mint++;}
   else if(r>218&&g>218&&b>210&&Math.Abs(r-g)<12){p[i+2]=238;p[i+1]=238;p[i]=235;white++;}
   else if(r>155&&r<215&&Math.Abs(r-g)<12&&Math.Abs(g-b)<15){p[i+2]=184;p[i+1]=183;p[i]=180;hair++;}
   bool diff=(p[i]!=b||p[i+1]!=g||p[i+2]!=r);
   if(diff)changed++;
   if(p[i+3]!=a)alpha++;
   if(core&&diff)ink++;
  }
  return new int[]{changed,skin,hair,white,mint,red,alpha,ink};
 }
 public static int GradeSkinRect(byte[] p,int w,int h,int stride,int x0,int y0,int x1,int y1) {
  int n=0;
  for(int y=Math.Max(0,y0);y<Math.Min(h,y1);y++)for(int x=Math.Max(0,x0);x<Math.Min(w,x1);x++){
   int i=y*stride+x*4,b=p[i],g=p[i+1],r=p[i+2];
   bool warm=r>65&&r>g+7&&(g>b+2||(r>225&&Math.Abs(g-b)<14))&&g>r*0.55&&b>r*0.5;
   bool neckShade=r>130&&r>g+75&&Math.Abs(g-b)<20&&g>60&&b>60;
   if(warm||neckShade){BlendInk(p,i,252,232,220,(r-23)/232.0);n++;}
  }
  return n;
 }
 public static int GradeSkinPolygon(byte[] p,int w,int h,int stride,int[] xy) {
  int n=0,x0=w,y0=h,x1=0,y1=0;
  for(int k=0;k<xy.Length;k+=2){x0=Math.Min(x0,xy[k]);x1=Math.Max(x1,xy[k]);y0=Math.Min(y0,xy[k+1]);y1=Math.Max(y1,xy[k+1]);}
  for(int y=Math.Max(0,y0);y<Math.Min(h,y1+1);y++)for(int x=Math.Max(0,x0);x<Math.Min(w,x1+1);x++){
   bool inside=false;double px=x+0.5,py=y+0.5;
   for(int a=0,b=xy.Length-2;a<xy.Length;b=a,a+=2){
    double ax=xy[a],ay=xy[a+1],bx=xy[b],by=xy[b+1];
    if((ay>py)!=(by>py)&&px<(bx-ax)*(py-ay)/(by-ay)+ax)inside=!inside;
   }
   if(inside)n+=GradeSkinRect(p,w,h,stride,x,y,x+1,y+1);
  }
  return n;
 }
}
