from pathlib import Path
from PIL import Image
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01"
D=B/"review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence"
D.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_imggen_original.png";a=Image.open(raw).convert("RGBA")
assert h(raw)=="f55ac32a894b384697e37f677f3580219b6282d91fcbb42abfceb49a78fc0392"
outs=[]
for label,roi,f in [("CURRENT_ROOT_COMPLETE_COIL",[590,278,772,580],3),("CURRENT_LOWER_PATH",[618,468,738,577],5),("CURRENT_EYES",[468,188,645,284],3)]:
 for color in ["white","black"]:
  im=Image.new("RGBA",a.size,color);im.alpha_composite(a);q=im.convert("RGB").crop(roi)
  p=D/(label+"_"+color+"_"+str(f)+"x.png");q.resize((q.width*f,q.height*f),Image.Resampling.NEAREST).save(p)
  outs.append({"path":str(p),"sha256":h(p),"raw_roi_xyxy_exclusive":roi,"scale":f})
# Uniform whole-image normalization for own guide comparison, never part-warp or actual registration.
q=Image.open(R/"qa_white.png").convert("RGB");f=720/q.width
p=D/"CURRENT_UNIFORM_WIDTH720_DIAGNOSTIC.png";q.resize((720,round(q.height*f)),Image.Resampling.LANCZOS).save(p)
outs.append({"path":str(p),"sha256":h(p),"uniform_scale":f,"production_registration":False})
rec={"image":{"path":str(raw),"sha256":h(raw),"dimensions":list(a.size)},"diagnostics":outs,"source_comparison_scope":"Whole layer uniformly resized/cropped/composited for readonly visual review; no art edits or production placement.","generation_calls":0}
(D/"DIAGNOSTIC_PROVENANCE.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,ensure_ascii=False))

