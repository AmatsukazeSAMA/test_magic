from pathlib import Path
import json
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
plan=json.loads((B/"REDRAW_PLAN.json").read_text("utf8"))
print(json.dumps({"referencing_job":plan["jobs"][53],"own_jobs":[j for j in plan["jobs"] if j.get("id")=="ART-G33-48"]},ensure_ascii=False))
stats=json.loads((B/"API_CALL_STATISTICS.json").read_text("utf8"))
hit=[]
def walk(z,path=""):
 if isinstance(z,dict):
  if any(v=="ART-G33-48" for v in z.values() if isinstance(v,str)):hit.append({"json_path":path,"record":z})
  for k,v in z.items():walk(v,path+"/"+k)
 elif isinstance(z,list):
  for i,v in enumerate(z):walk(v,path+"/"+str(i))
walk(stats)
print(json.dumps({"API_CALL_STATISTICS_target_matches":hit},ensure_ascii=False))
d=json.loads(Path(r"D:/CODEX/魔术之心/image_defaults.json").read_text("utf8"))
p=json.loads(Path(d["source_hairstyle_policy"]["path"]).read_text("utf8"))
print(json.dumps({"hairstyle_target_state":p["states"].get("ART-G33-48"),"policy_id":p["policy_id"]},ensure_ascii=False))

