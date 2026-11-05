from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/api_user_parallel_redraw_latest_coil_tls12_v02"
D=B/"review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence";D.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_api_original.png";a=Image.open(raw).convert("RGBA")
assert h(raw)=="897eef064e9ba25ad4d409771acc29fd3ee45c1d9c17a0da353ff2aed2aa2e37"
outs=[]
def crop_save(im,roi,scale,name):
 q=im.crop(roi);p=D/name;q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST).save(p)
 outs.append({"path":str(p),"sha256":h(p),"roi_xyxy":roi,"scale":scale})
for bg in ["white","black"]:
 im=Image.new("RGBA",a.size,bg);im.alpha_composite(a);im=im.convert("RGB")
 crop_save(im,[603,280,754,505],4,"ROOT_COIL_"+bg+"_4x.png")
 crop_save(im,[643,391,737,490],6,"LOWER_PATH_"+bg+"_6x.png")
 if bg=="white":crop_save(im,[470,185,650,288],3,"CURRENT_EYES_WHITE_3x.png")
p=B/"drawings/ART-X01-15/v01/whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02/qa_white.png"
roi=[579,271,787,598];l=Image.open(p).convert("RGB").crop(roi);r=Image.open(R/"qa_white.png").convert("RGB").crop(roi)
pa=Image.new("RGB",(l.width*2,l.height+20),"white");pa.paste(l,(0,20));pa.paste(r,(l.width,20));dr=ImageDraw.Draw(pa);dr.text((3,2),"Rejected fa114",fill="black");dr.text((l.width+3,2),"Current 897eef",fill="black")
p2=D/"SAME_NATIVE_SCALE_COMPACT_COIL_COMPARISON_2x.png";pa.resize((pa.width*2,pa.height*2),Image.Resampling.NEAREST).save(p2)
outs.append({"path":str(p2),"sha256":h(p2),"roi_xyxy":roi,"scale":2,"note":"Same native coordinates, almost identical output canvas size. Visual context only, not a fixed acceptance ratio."})
res={"image":{"path":str(raw),"sha256":h(raw),"dimensions":list(a.size)},"diagnostics":outs,"original_art_unchanged":True,"generation_calls":0}
(D/"DIAGNOSTIC_PROVENANCE.json").write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(res,ensure_ascii=False))

