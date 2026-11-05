from pathlib import Path
import json,hashlib
from PIL import Image
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03"
D=B/"review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=Image.open(R/"character_imggen_original.png").convert("RGBA")
outs=[]
for roi,label,f in [([560,225,770,520],"CURRENT_LOWROOT_SHOULDER_CONTEXT",3),([650,417,768,505],"CURRENT_SMALL_TAIL_CONTEXT",5)]:
 for color in ["white","black"]:
  im=Image.new("RGBA",a.size,color);im.alpha_composite(a);q=im.convert("RGB").crop(roi);p=D/(label+"_"+color+"_"+str(f)+"x.png");q.resize((q.width*f,q.height*f),Image.Resampling.NEAREST).save(p)
  outs.append({"path":str(p),"sha256":h(p),"raw_roi_xyxy":roi,"scale":f})
(D/"CURRENT_ART_DETAIL_PROVENANCE.json").write_text(json.dumps({"raw":str(R/"character_imggen_original.png"),"sha256":h(R/"character_imggen_original.png"),"dimensions":list(a.size),"diagnostics":outs,"generation_calls":0,"art_unchanged":True},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
ledger=json.loads((B/"coverage/EXPOSURE_LEDGER.json").read_text(encoding="utf-8-sig"))
print(json.dumps({"source_video_declared":ledger["source_video"],"source_video_sha256_declared_not_recomputed":ledger["source_sha256"],"time_base":ledger["time_base"],"frames":[{k:f[k] for k in ["frame","pts","end_pts","duration_ticks","source_frame"]} for f in ledger["frames"] if 834<=f["frame"]<=840],"current_image_sha256":h(R/"character_imggen_original.png"),"dimensions":list(a.size)},ensure_ascii=False))

