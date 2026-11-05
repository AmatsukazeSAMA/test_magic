from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence"
D.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
proof=[]
for p in [B/"coverage/EXPOSURE_LEDGER.json",B/"dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json"]:
 a=json.loads(p.read_text(encoding="utf-8-sig"));print("FILE",str(p),"KEYS",list(a) if isinstance(a,dict) else "list")
 def walk(v,loc=""):
  if isinstance(v,dict):
   f=v.get("frame",v.get("source_frame",v.get("frame_number")))
   if isinstance(f,int) and 834<=f<=840:
    print("FRAME",loc,json.dumps(v,ensure_ascii=False));proof.append({"metadata_path":str(p),"record_path":loc,"record":v});return
   if v.get("id")=="ART-G33-01" or v.get("drawing_id")=="ART-G33-01":
    print("ID",loc,json.dumps(v,ensure_ascii=False));proof.append({"metadata_path":str(p),"record_path":loc,"record":v});return
   for k,x in v.items():walk(x,loc+"/"+str(k))
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,loc+"/"+str(i))
 walk(a)
sources=[B/"coverage/source_frames"/("F"+str(f).zfill(6)+".png") for f in range(834,841)]
outs=[]
for k,frames in enumerate([range(834,838),range(838,841)]):
 page=Image.new("RGB",(1040,1960),"white");draw=ImageDraw.Draw(page)
 for n,f in enumerate(frames):
  p=B/"coverage/source_frames"/("F"+str(f).zfill(6)+".png")
  im=Image.open(p).convert("RGB").crop((640,120,1160,1080))
  x=(n%2)*520;y=(n//2)*980;page.paste(im,(x,y+20));draw.text((x+3,y+3),"Native F"+str(f)+" crop640,120,1160,1080",fill="black")
 op=D/("ALL_NATIVE_SOURCES_PAGE_"+str(k+1)+".png");page.save(op);outs.append({"path":str(op),"sha256":h(op),"frames":list(frames),"source_crop_xyxy":[640,120,1160,1080],"resized":False})
# Source-source diagnostic uniform proposal; old geometry is a starting estimate, visually rechecked now.
canon=Path("D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-01/source.png")
c=Image.open(canon).convert("RGB")
sc=1.809475806451613;tx=-788.7883064516129;ty=-13.465221774193594
aligned=c.transform((1920,1080),Image.Transform.AFFINE,(1/sc,0,-tx/sc,0,1/sc,-ty/sc),resample=Image.Resampling.BICUBIC,fillcolor="white")
a=Image.open(sources[0]).convert("RGB")
roi=(640,120,1160,1080);left=aligned.crop(roi);right=a.crop(roi)
pair=Image.new("RGB",(1040,980),"white");pair.paste(left,(0,20));pair.paste(right,(520,20));ImageDraw.Draw(pair).text((4,4),"F2306 uniform diagnostic | Actual F834",fill="black")
op=D/"ORIGINAL_CANONICAL2306_UNIFORM_VS_ACTUAL834.png";pair.save(op);outs.append({"path":str(op),"sha256":h(op),"source_uniform_transform":{"scale":sc,"translation":[tx,ty]},"source_crop_xyxy":roi,"not_production_registration":True})
summary={"source_frames":[{"frame":f,"path":str(p),"sha256":h(p),"exists":p.exists()} for f,p in zip(range(834,841),sources)],"source_source_uniform_diagnostic":{"canonical":str(canon),"canonical_sha256":h(canon),"scale":sc,"translation":[tx,ty],"based_on":"Historical ORIGINAL-only face-bbox estimate, not accepted automatically; actual stroke/neck/bow/sleeve correspondence inspected fresh."},"metadata_snapshots":proof,"diagnostics":outs,"central_writes":False,"generation_calls":0}
(D/"ACTUAL_SOURCE_AND_BINDING_EVIDENCE.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("EVIDENCE",str(D/"ACTUAL_SOURCE_AND_BINDING_EVIDENCE.json"),h(D/"ACTUAL_SOURCE_AND_BINDING_EVIDENCE.json"))

