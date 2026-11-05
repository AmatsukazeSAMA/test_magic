from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/diagnostics/G13_29_CANONICAL1324_VS_WIDER3766_20261104_v01"
D.mkdir(parents=True,exist_ok=True)
p=Path(r"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G13-29/source.png")
q=B/"coverage/source_frames/F003766.png"
A=Image.open(p).convert("RGB"); C=Image.open(q).convert("RGB")
a=np.asarray(A,dtype=np.float32); c=np.asarray(C,dtype=np.float32)
# Only character pixels in canonical common region, no caption/background.
yy,xx=np.mgrid[80:1060:4,0:1120:4]
v=a[yy,xx]
bg=np.array([212,169,171],dtype=np.float32)
use=(np.max(v,axis=2)-np.min(v,axis=2)>25)|(np.max(v,axis=2)<110)|(np.min(v,axis=2)>220)
x=xx[use].astype(float);y=yy[use].astype(float);v=v[use]
def err(s,tx,ty):
 X=x*s+tx;Y=y*s+ty
 valid=(X>=0)&(X<1919)&(Y>=0)&(Y<1079)
 X=X[valid];Y=Y[valid]; V=v[valid]
 i=X.astype(int);j=Y.astype(int);fx=(X-i)[:,None];fy=(Y-j)[:,None]
 got=c[j,i]*(1-fx)*(1-fy)+c[j,i+1]*fx*(1-fy)+c[j+1,i]*(1-fx)*fy+c[j+1,i+1]*fx*fy
 # Outliers capped: diagnostic similarity, no identity claim from score.
 return float(np.minimum(np.abs(got-V).mean(axis=1),60).mean())
s,tx,ty=.82,107.,82.
best=err(s,tx,ty)
for ds,dt in [(0.002,2),(0.001,1),(.0005,.5),(.0002,.2),(.0001,.1)]:
 for _ in range(5):
  improved=False
  for axis,delta in [(0,ds),(1,dt),(2,dt)]:
   opts=[]
   for sign in [-1,0,1]:
    k=[s,tx,ty];k[axis]+=sign*delta
    opts.append((err(*k),k))
   e,k=min(opts,key=lambda z:z[0])
   if e<best-1e-8:best=e;s,tx,ty=k;improved=True
  if not improved:break
mapped=A.transform(C.size,Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.BICUBIC,fillcolor=(235,235,235))
mapped.save(D/"canonical1324_uniform_in_3766_coordinates.png")
panels=[("eyes mouth head",[275,320,635,610]),("fingers cuff lines",[665,480,1040,900]),("collar bow shoulder crossarm",[155,540,760,1040])]
rows=[]
for name,roi in panels:
 l=mapped.crop(roi);r=C.crop(roi)
 # Same native current scale, no per-region adjustments.
 w=max(l.width,r.width);h=l.height
 row=Image.new("RGB",(w*2+20,h+32),(245,245,245));dr=ImageDraw.Draw(row)
 dr.text((5,5),"canonical1324 uniform: "+name,fill="black");dr.text((w+25,5),"original3766 same ROI",fill="black")
 row.paste(l,(0,32));row.paste(r,(w+20,32));rows.append(row)
out=Image.new("RGB",(max(k.width for k in rows),sum(k.height for k in rows)+20*(len(rows)-1)),(230,230,230))
dy=0
for k in rows:out.paste(k,(0,dy));dy+=k.height+20
out.save(D/"COMMON_VISIBLE_STROKES_UNIFORM_COMPARISON.png")
# Whole-side comparison at native current coords, top common extent marked only in metadata.
L=mapped.crop((80,100,1080,1080));R=C.crop((80,100,1080,1080))
whole=Image.new("RGB",(2020,1012),(245,245,245));dr=ImageDraw.Draw(whole)
dr.text((5,5),"Canonical1324 uniform ONLY - below original extent is diagnostic filler",fill="black")
dr.text((1025,5),"Original3766 wider true PV extent",fill="black");whole.paste(L,(0,32));whole.paste(R,(1020,32));whole.save(D/"FULL_SOURCE_UNIFORM_COMPARISON.png")
def sha(z):return hashlib.sha256(Path(z).read_bytes()).hexdigest()
obj={"diagnostic_only":True,"production_registration_approved":False,"source":str(p),"source_sha256":sha(p),"wider_source":str(q),"wider_source_sha256":sha(q),"transform":{"kind":"one uniform scale and XY translation, no rotation/shear/local warp","canonical1324_to_wider3766":{"scale":s,"translation":[tx,ty]},"estimated_by":"robust RGB fit on common original character pixels, excluding captions; actual visual stroke review required","fit_score_not_identity_proof":best,"transformed_canonical_bottom_y":1080*s+ty},"comparison_rois_in_3766":panels,"images":[{"path":str(z),"sha256":sha(z)} for z in [D/"canonical1324_uniform_in_3766_coordinates.png",D/"COMMON_VISIBLE_STROKES_UNIFORM_COMPARISON.png",D/"FULL_SOURCE_UNIFORM_COMPARISON.png"]]}
(D/"DIAGNOSTIC.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(obj,ensure_ascii=False))

