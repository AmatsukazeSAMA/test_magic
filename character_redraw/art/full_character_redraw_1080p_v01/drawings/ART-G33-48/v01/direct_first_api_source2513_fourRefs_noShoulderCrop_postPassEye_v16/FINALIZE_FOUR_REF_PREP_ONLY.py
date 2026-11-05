from pathlib import Path
import json,hashlib,datetime
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");V=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16");ROOT=B.parent.parent
sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest()
ev=lambda z:{"path":str(Path(z)),"sha256":sha(z)}
q=json.loads((R/"DIRECT_REQUEST.json").read_text("utf8"));lock=json.loads((R/"REQUEST_LOCK.json").read_text("utf8"));preview=json.loads((R/"DIRECT_PREVIEW.json").read_text("utf8"))
for it in [lock["request"],lock["prompt"],lock["JOB"],lock["REGISTRATION_PLAN"],lock["wrapper"],lock["requirements"],lock["eye_color_policy"],lock["source_hairstyle_policy"],lock["project_defaults"],*lock["references"]]:assert sha(it["path"])==it["sha256"]
assert preview["submitted"] is False and preview["input_count"]==4 and preview["quality"]=="high" and preview["n"]==1 and preview["retry"]==1 and preview["drawing_id"]=="ART-G33-48"
execnames={"attempt.json","result.json","BUILTIN_GENERATION.json","api_response.raw.json","ROOT_API_EXECUTION_RECEIPT.json","SUBMISSION_STARTED.json","character_api_original.png","character_imggen_original.png"}
found=[str(z) for z in V.rglob("*") if z.is_file() and z.name in execnames];assert not found
rows=[z for z in json.loads((B/"PROGRESS.json").read_text("utf8"))["records"] if z.get("id")=="ART-G33-48"];reg=json.loads((B/"ASSET_REGISTRY.json").read_text("utf8"))
assert len(rows)==1 and rows[0]["status"]=="pending" and not rows[0].get("image") and not reg.get("ART-G33-48",{}).get("image")
stats=json.loads((B/"API_CALL_STATISTICS.json").read_text("utf8"));hits=[]
def walk(z,path=""):
 if isinstance(z,dict):
  if any(x=="ART-G33-48" for x in z.values() if isinstance(x,str)):hits.append(path)
  for k,val in z.items():walk(val,path+"/"+k)
 elif isinstance(z,list):
  for i,val in enumerate(z):walk(val,path+"/"+str(i))
walk(stats);assert not hits
rec={"id":"ART-G33-48","status":"PREP_ONLY_LOCKED_AWAIT_ROOT_ACTUAL_INPUT_REVIEW_NO_CALL","checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"run":str(R),"request":ev(R/"DIRECT_REQUEST.json"),"prompt":ev(R/"prompt_api.txt"),"prep_lock":ev(R/"REQUEST_LOCK.json"),"Preview":ev(R/"DIRECT_PREVIEW.json"),"preview_summary":preview,"exact_source":q["source"],"exact_guide":q["guide"],"JOB":ev(V/"JOB.json"),"REGISTRATION_PLAN":ev(V/"REGISTRATION_PLAN.json"),"refs":q["refs"],"reference_roles":q["reference_roles"],"own_actual_observation":q["own_action"],"source_change_vs47":"47 open-round tiny-neutral mouth/headside highhand→48 fully CLOSED eyes/short closed smile, viewer-left hand drops to chest with vertical index, other hand horizontally spreads overbow; narrower skirt and closer whole shoes. Failed47 generated root/coil remains shoulder-outboard and is NOT any input.","failure_hypothesis_stop":"No failed43/identity short shoulder/root crop, no full polished3views, no failed47 target included. Only own2513 guide+noeye bob+approvedCOMPLETEcoil+iriscolorinternalcap4refs. Hypothesis only, no internal-tool-cause or success claim.","uniqueness":{"pending_selected_image_absent":True,"prior_nested_execution_or_return_files":found,"API_STATISTICS_target_matches":hits,"source_reuse_scope_for_own":None,"dependent_plan_consumer":"ART-G12-52 future partial head/torso reuse depends on this missing master; explicitly not whole visible-outline alias, does not provide ready G33-48 artwork.","unrelated_unknown_or_HTTP400_state_touched":False},"hash_readback_all_prepared_inputs_match":True,"actual_viewed_paths":[ev(x) for x in q["actual_viewed_paths"]],"requirements":q["requirements"],"eye_color_policy":q["eye_color_policy"],"curl_structure_policy_id":q["curl_structure_policy_id"],"risks":q["risks"],"root_release_granted":False,"submitted":False,"API_calls":0,"imagegen_calls":0,"central_writes":False,"artwork_approved":False,"photography_verified":False,"dynamic_verified":False,"user_accepted":False}
out=R/"PREP_ONLY_HANDOFF.json";out.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(R/"README_PREP_ONLY.md").write_text("""ART-G33-48 F2513 / PTS1341616；仅四参考PREP，0call，root_release=false。

own2513 guide唯一控制动作/头身/双闭眼小闭笑/两不同胸前手/黑长袖红结白裙/完整双鞋。前47仅变化和失败故障对照，未作为生成输入。去掉所有43/identity短肩前/expanded root crop与polished全三视图；低LEFT双珠→同一整束正常体量2大+真小+C的肩前深度由自身颈胸/白frill/黑袖决定。遮挡段计入总圈数，不在臂下重启计数，不为全露缩小或挖灰返回。

当前pending无selected art，完整nested无attempt/result/raw/builtin/UNKNOWN执行产物，API统计无target。G12-52仅未来partial reuse消费者，不是本图已有alias稿。未动其它unknown/HTTP400。

DIRECT_REQUEST / prompt / REQUEST_LOCK 已相互SHA锁定，DIRECT_PREVIEW经真实 -Preview 返回submitted=false、high、624x1072、4refs、n1 retry1。ROOT须实看四refs与ownsource再另释放一次；本目录PREP没有授权或执行生成。闭眼按实际返图判定，不新增iris做配色。真正画稿、摄影、动态、用户验收均待。
""",encoding="utf8")
print(json.dumps({"request":rec["request"],"prompt":rec["prompt"],"lock":rec["prep_lock"],"preview":rec["Preview"],"handoff":ev(out),"zero_call":True},ensure_ascii=False))

