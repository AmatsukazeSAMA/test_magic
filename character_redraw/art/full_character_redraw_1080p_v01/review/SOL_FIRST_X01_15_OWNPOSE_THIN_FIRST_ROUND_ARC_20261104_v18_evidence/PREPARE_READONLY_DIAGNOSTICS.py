from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/direct_first_api_source4082_ownPose_junctionOnly_thinFirstBand_roundArc_v18"
D=B/"review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence"
D.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_api_original.png";a=Image.open(raw).convert("RGBA")
out=[]
for label,roi,scale in [("CURRENT_ROOT_COIL",[417,187,513,332],4),("CURRENT_EYE",[318,130,443,199],5)]:
 for color in ["white","black"]:
  bg=Image.new("RGBA",a.size,color);bg.alpha_composite(a);q=bg.convert("RGB").crop(roi)
  p=D/(label+"_"+color+"_"+str(scale)+"x.png");q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST).save(p)
  out.append({"path":str(p),"sha256":h(p),"raw_roi_xyxy_exclusive":roi,"scale":scale})
guide=B/"drawings/ART-X01-15/v01/inputs/source_pose_guide.png"
src=Image.open(guide).convert("RGB");box=[316,152,443,218];q=src.crop(box);p=D/"OWN_GUIDE_EYES_5x.png";q.resize((q.width*5,q.height*5),Image.Resampling.NEAREST).save(p)
out.append({"path":str(p),"sha256":h(p),"guide_roi_xyxy_exclusive":box,"scale":5})
# Diagnostic only: uniform scale using manual actual eye-center spans, no rotation/part warp/production registration.
items=[
("X01-14 preceding",B/"drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04/qa_white.png",[(428,304),(526,255)]),
("X01-15 current",R/"qa_white.png",[(350,173),(415,154)])
]
panel=Image.new("RGB",(1000,530),"white");draw=ImageDraw.Draw(panel); transforms=[]
for i,(lab,p,points) in enumerate(items):
 im=Image.open(p).convert("RGB");mid=[(points[0][j]+points[1][j])/2 for j in [0,1]]
 span=math.dist(*points);scale=120/span;tx=230-scale*mid[0];ty=180-scale*mid[1]
 # output coordinates sample input inverse.
 q=im.transform((500,500),Image.Transform.AFFINE,(1/scale,0,-tx/scale,0,1/scale,-ty/scale),resample=Image.Resampling.BICUBIC,fillcolor="white")
 panel.paste(q,(500*i,30));draw.text((i*500+8,8),lab,fill="black")
 transforms.append({"image":str(p),"sha256":h(p),"manual_eye_centers":points,"uniform_scale":scale,"translation":[tx,ty],"purpose":"Illustrative face-scale context only; not an acceptance ratio, pose matching or photography."})
p=D/"HEAD_CONTEXT_UNIFORM_EYE_SPAN_DIAGNOSTIC.png";panel.save(p);out.append({"path":str(p),"sha256":h(p)})
arr=np.array(a)
rec={"raw":{"path":str(raw),"sha256":h(raw),"dimensions":list(a.size)},"diagnostics":out,"context_transforms":transforms,"scope":"Readonly QA/crops and uniformly scaled context. No artwork pixels or central metadata changed.","generation_calls":0}
(D/"DIAGNOSTIC_PROVENANCE.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,ensure_ascii=False))

