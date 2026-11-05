import json
from pathlib import Path
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
for p in [B/"dance_first10_reference_redraw_v01/PROGRESS.json",B/"dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json"]:
 a=json.loads(p.read_text(encoding="utf-8-sig"));print("FILE",str(p),"KEYS",list(a) if isinstance(a,dict) else "list")
 if "PROGRESS" in p.name:
  if isinstance(a,dict):
   for k,v in a.items():
    if not isinstance(v,(list,dict)):print(k,repr(v))
 def walk(v,path=""):
  if isinstance(v,dict):
   if (v.get("id")== "ART-G33-01" or v.get("drawing_id")=="ART-G33-01" or v.get("canonical_id")=="ART-G33-01") or (v.get("start_frame")==834):
    print("MATCH",path,json.dumps(v,ensure_ascii=False));return
   for k,w in v.items():walk(w,path+"/"+str(k))
  elif isinstance(v,list):
   for i,w in enumerate(v):walk(w,path+"/"+str(i))
 walk(a)
for p in [B/"coverage/source_frames/F000834.png",B/"coverage/source_frames/F000840.png",B/"drawings/ART-G33-01/v03/JOB.json"]:
 print("EXISTS",str(p),p.exists())
 if p.suffix==".json" and p.exists():print(p.read_text(encoding="utf-8-sig"))

