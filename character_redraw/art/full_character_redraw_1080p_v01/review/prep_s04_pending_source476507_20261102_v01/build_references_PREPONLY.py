"""Read-only-derived FIRST-input preparation. No network, credentials, selection or generation."""
from pathlib import Path
from PIL import Image
import json, hashlib, shutil
BASE=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
TASK=BASE/"review/prep_s04_pending_source476507_20261102_v01"
TASK.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
    if p.exists(): raise RuntimeError("Preserve existing PREP: "+str(p))
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
jobs=[
 {"id":"ART-G06-01","source_frame":476,"run_name":"prep_first_api_source476_inverted_visibleonly_grayLEFT_v01","prev":"drawings/ART-G06-02/v01/whole_imggen_v02/character_imggen_original.png","prevsha":"e3e1b45d677196fe6cdd99f2802d77f8bb08a34ca6a2995674f9db4551a1f7d9","prevroi":[385,1135,725,1485],"source_roi":[790,630,1005,765],"expected_source_sha":"3ab6bfb9148ca10aea60725a3450fbb020bf892ffc8b5f8384864a69be1bb0a0"},
 {"id":"ART-G07-03","source_frame":507,"run_name":"prep_first_api_source507_inverted_visibleonly_grayLEFT_v01","prev":"drawings/ART-G07-02/v03/whole_imggen_v01/character_imggen_original.png","prevsha":"7b68bfaf3f6cc39f8075fad614d90b9c7af45a84baee30ad7b3a1898df104f07","prevroi":[500,260,1085,890],"source_roi":[390,180,1010,545],"expected_source_sha":"a81c533ab1073bad1478bf33bcb958a8b397fda74c6b404fb420a407da868e37"}
]
plan=json.loads((BASE/"REDRAW_PLAN.json").read_text("utf-8-sig"))
progress=json.loads((BASE/"PROGRESS.json").read_text("utf-8-sig"))
ledger=json.loads((BASE/"coverage/EXPOSURE_LEDGER.json").read_text("utf-8-sig"))
registry=json.loads((BASE/"ASSET_REGISTRY.json").read_text("utf-8-sig"))
output=[]
for item in jobs:
    aid=item["id"];parent=BASE/"drawings"/aid/"v01"
    job=next(j for j in plan["jobs"] if j["id"]==aid)
    row=next(j for j in progress["records"] if j["id"]==aid)
    assert row["status"]=="pending" and row.get("image") is None and aid not in registry
    source=Path(job["source_image"]);assert sha(source)==item["expected_source_sha"]
    # Only registered-source candidate files count, never previous group's art or derived refs.
    known=list((BASE/"drawings"/aid).rglob("character*original*.png"))
    assert not known, "Existing return discovered; do not prepare duplicate FIRST"
    assert not [c for c in progress["calls"] if ("/"+aid+"/") in ("/"+c["run"].replace("\\","/")+"/")]
    run=parent/item["run_name"]
    if run.exists(): raise RuntimeError("Choose new PREP version: "+str(run))
    (run/"inputs").mkdir(parents=True)
    records=[]
    def copied(name,src,role):
        dest=run/"inputs"/name;shutil.copy2(src,dest)
        records.append({"path":dest.as_posix(),"sha256":sha(dest),"dimensions":list(Image.open(dest).size),"source":str(src).replace("\\","/"),"source_sha256":sha(src),"derivation":"exact_byte_copy","role":role})
    copied("ref1_ORIGINAL_COMPLETE_UNMASKED_ACTION_GUIDE.png",parent/"inputs/source_pose_guide.png","Own original source only: orientation/expression/visible limbs/costume/crop and disc-occlusion boundary. Original red identity/independent disc/ghosts are not rendered.")
    prev=BASE/item["prev"];assert sha(prev)==item["prevsha"]
    roi=item["prevroi"];im=Image.open(prev).convert("RGBA").crop(roi)
    white=Image.new("RGBA",im.size,"white");white.alpha_composite(im)
    dest=run/"inputs/ref2_PRECEDING_INVERTED_BAREBOB_PARTIAL_HEAD_CONTEXT_NO_COIL.png";white.convert("RGB").save(dest)
    records.append({"path":dest.as_posix(),"sha256":sha(dest),"dimensions":list(white.size),"source":prev.as_posix(),"source_sha256":sha(prev),"source_roi_xyxy":roi,"derivation":"unchanged_rectangle_crop_then_white_alpha_composite_no_retouch_no_resize","role":"Preceding actual drawing identity/bare inverted bob context only, deliberately excludes old bead/coil/body; old material/expression/art pass not inherited."})
    copied("ref3_USER_CORRECT11_COIL_GEOMETRY_ONLY_NO_MAIDCAP.png",BASE/"inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png","User-approved broad gray winding/returns/taper/C only; no cap, fixed axis/length/turn count, lighting or source-action authority; tiny adjacent cloth is context only.")
    copied("ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY.png",BASE/"drawings/ART-G12-39/v01/whole_imggen_source966_reviewed37_plaincrop_grayonly_context_v04/inputs/ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY.png","Unlit gray pigment only, all broad faces and returns gray, mint thin muted material band.")
    roi=item["source_roi"];dest=run/"inputs/ref5_OWN_SOURCE_EXPRESSION_DISC_OCCLUSION_ONLY.png";Image.open(source).crop(roi).save(dest)
    records.append({"path":dest.as_posix(),"sha256":sha(dest),"dimensions":list(Image.open(dest).size),"source":source.as_posix(),"source_sha256":sha(source),"source_roi_xyxy":roi,"derivation":"unchanged_source_rectangle_crop_no_rotation_no_resize_no_retouch","role":"Own current inverted eye aperture/lashes and disc-hidden jaw/mouth boundary only; no invented mouth/body behind disc, no red identity copying."})
    resolved=[]
    for f in ledger["frames"]:
        ids=f.get("resolved_canonical_ids") or f.get("proposed_canonical_ids") or []
        if aid in ids:resolved.append({k:f[k] for k in ["frame","pts","end_pts","duration_ticks"]})
    obj={"id":aid,"run":run.as_posix(),"source_frame":item["source_frame"],"source_pts":job["source_pts"],"source_image":source.as_posix(),"source_image_sha256":sha(source),"source_canvas":list(Image.open(source).size),"guide_dimensions":list(Image.open(parent/"inputs/source_pose_guide.png").size),"proposed_request_size":job["output_size_string"],"reference_count":len(records),"references":records,"job_before_sha256":sha(parent/"JOB.json"),"registration_plan_before_sha256":sha(parent/"REGISTRATION_PLAN.json"),"source_visible_exposure_nominations":resolved,"exposure_evidence_only_not_binding":True,"progress_snapshot":{"updated_utc":progress["updated_utc"],"status":"pending","image":None},"existing_actual_return_files":[],"existing_own_API_calls":[],"selected_asset_existed":False,"PREPONLY":True,"submitted":False,"generation_calls_made":0,"network_calls":0}
    write(run/"INPUT_PROVENANCE_PREPONLY.json",obj);output.append(obj)
write(TASK/"REFERENCE_PREPARATION_INDEX.json",output)
print(json.dumps([{"id":x["id"],"run":x["run"],"references":x["references"],"source_visible_exposure_nominations":x["source_visible_exposure_nominations"]} for x in output],ensure_ascii=False))

