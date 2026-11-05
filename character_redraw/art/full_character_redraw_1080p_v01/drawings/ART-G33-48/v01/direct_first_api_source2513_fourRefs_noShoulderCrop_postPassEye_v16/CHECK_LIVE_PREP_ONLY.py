from pathlib import Path
from PIL import Image
import hashlib,json,datetime
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");V=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16");R.mkdir(parents=True,exist_ok=True)
sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest()
defaults=json.loads(Path(r"D:/CODEX/魔术之心/image_defaults.json").read_text("utf8"))
print(json.dumps({"selected_defaults":{k:val for k,val in defaults.items() if any(w in k.lower() for w in ["eye","source_hairstyle","prefix","curl","model","quality","retry"])}},ensure_ascii=False))
records=json.loads((B/"PROGRESS.json").read_text("utf8"));reg=json.loads((B/"ASSET_REGISTRY.json").read_text("utf8"));plan=json.loads((B/"REDRAW_PLAN.json").read_text("utf8"))
id="ART-G33-48";rows=[x for x in records["records"] if x.get("id")==id]
assert len(rows)==1 and rows[0]["status"]=="pending" and not rows[0].get("image")
assert not reg.get(id,{}).get("image")
matches=[]
def walk(z,path=""):
 if isinstance(z,dict):
  for k,val in z.items():
   if val==id and not k in ["id","previous_in_family","drawing_id"]:matches.append([path+"/"+k,val])
   walk(val,path+"/"+k)
 elif isinstance(z,list):
  for i,val in enumerate(z):walk(val,path+"/"+str(i))
walk(reg,"registry");walk(plan,"plan")
initial=[{"path":str(q),"sha256":sha(q)} for q in V.rglob("*") if q.is_file() and R not in q.parents]
face=Image.open(V/"inputs/source_pose_guide.png");part=face.crop((175,126,425,377));part.resize((750,753),Image.Resampling.NEAREST).save(R/"OWN_SOURCE_FACE_HANDS_OBSERVATION_ONLY_3x.png")
obj={"id":id,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"progress_record":rows[0],"registry_entry":reg.get(id),"other_alias_references":matches,"initial_own_nested_files":initial,"nested_execution_or_art_files":[],"no_prior_execution":True,"generation_submitted":False,"API_calls":0,"central_writes":False}
(R/"LIVE_INVENTORY_PREP_ONLY.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(obj,ensure_ascii=False))

