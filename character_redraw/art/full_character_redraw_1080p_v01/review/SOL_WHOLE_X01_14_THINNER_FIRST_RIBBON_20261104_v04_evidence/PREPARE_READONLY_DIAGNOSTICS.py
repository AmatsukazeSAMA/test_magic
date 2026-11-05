from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04"
D=B/"review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence"
D.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/"character_imggen_original.png";assert h(p)=="8181037962aaa0624155fc5ac1af924536be55f5b4b35311f4cf78d748de29ae"
a=Image.open(p).convert("RGBA")
outs=[];spec=[("COIL_ROOT_FIRST_RETURN",tuple([535,320,717,557]),3),("EYES",tuple([375,210,580,342]),3)]
for label,roi,scale in spec:
 for bg,name in [("white","white"),("black","black")]:
  q=Image.new("RGBA",a.size,bg);q.alpha_composite(a);q=q.convert("RGB").crop(roi)
  op=D/(label+"_"+name+"_"+str(scale)+"x.png");q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST).save(op)
  outs.append({"path":str(op),"sha256":h(op),"raw_roi_xyxy_exclusive":roi,"scale":scale})
# Diagnostic uniform normalization only; preserves whole layer geometry, not a production registration.
qa=Image.open(R/"qa_white.png").convert("RGB")
fac=624/qa.width; normalized=qa.resize((624,round(qa.height*fac)),Image.Resampling.LANCZOS)
op=D/"CURRENT_UNIFORM_WIDTH624_DIAGNOSTIC.png";normalized.save(op)
outs.append({"path":str(op),"sha256":h(op),"uniform_scale":fac,"not_production_registration":True})
# Read source bottom exactly; diagnostic only. No source/art pixels edited.
src=Path("D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/X01-14/source.png")
im=Image.open(src).crop((680,900,1300,1080));op=D/"SOURCE4078_NATIVE_BOTTOM_CROP.png";im.save(op)
outs.append({"path":str(op),"sha256":h(op),"source_roi_xyxy_exclusive":[680,900,1300,1080]})
arr=np.array(a)
positions=[(599,398),(606,394),(627,398),(643,385),(618,416),(646,442),(649,491)]
rec={"image":{"path":str(p),"sha256":h(p),"dimensions":list(a.size)},"diagnostics":outs,"RGBA_position_observations":[{"xy":[x,y],"RGBA":arr[y,x].tolist()} for x,y in positions],"scope":"Readonly crop/composite/uniform inspection only, no art modifications or production placement.","API_calls":0,"imagegen_calls":0}
(D/"DIAGNOSTIC_PROVENANCE.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,ensure_ascii=False))

