from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
R=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-03/v01/local_api_plate_and_lowroot_SCOPE_DRAFTONLY_v03")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):p=Path(p);return {"path":p.as_posix(),"sha256":sha(p),"bytes":p.stat().st_size}
def save(n,v):
 p=R/n
 if p.exists():raise RuntimeError("Preserve "+n)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return p
p=json.loads((R/"API_PREVIEW_PROOF_PREPONLY.json").read_text(encoding="utf-8"))
assert p["wrapper_preview"]["submitted"] is False
assert p["wrapper_preview"]["mask_provided"] is True
assert not any((R/n).exists() for n in ("attempt.json","api_response.raw.json","result.json","character_api_original.png","request_manifest.json","prompt_effective.txt"))
scope=json.loads((R/"MASK_SCOPE_GEOMETRY_PREPONLY_v03.json").read_text(encoding="utf-8"))
mainfiles=["prompt_api.txt","API_PREPARED_REQUEST.json","REQUEST_LOCK_PREPONLY.json","Preview-PreparedMaskedOnly.ps1","API_PREVIEW_PROOF_PREPONLY.json","PREVIEW_GUARD_REFUSAL_PROOF.json","ARTIST_ACTUAL_MASK_REVIEW_PREPONLY.json","REFERENCE_SCOPE_DRAFT_PROVENANCE.json","MASKED_LOCAL_PREP_DRAFT.json","MASK_SCOPE_GEOMETRY_PREPONLY_v03.json","MANDATORY_WHOLE_TEMPLATE_NOT_DISPATCH.json","ACTUAL_PREP_VIEW_PATHS.json"]
paths=[R/n for n in mainfiles]+list((R/"inputs").glob("*.png"))+list((R/"diagnostics_v03").glob("*.png"))+[R/x["path"].split("/")[-1] for x in scope["records"]]
manifest=save("PAYLOAD_MANIFEST_PREPONLY.json",{
"id":"ART-G07-03","status":"PREPONLY_PAYLOADS_NO_DISPATCH","created_utc":datetime.now(timezone.utc).isoformat(),
"records":[rec(x) for x in paths],"no_api_calls":True,"no_release":True,
"historical_drafts_retained":["mask*_v01.png","mask*_v02.png","diagnostics","diagnostics_v02","MASK_SCOPE_GEOMETRY_PREPONLY.json","MASK_SCOPE_GEOMETRY_PREPONLY_v02.json","PREP_SUSPENDED_PRIORITY182.json"],
"manifest_excludes_handoff_to_avoid_recursive_hash":True})
handoff=save("ARTIST_HANDOFF_PREPONLY.json",{
"schema_version":"masked_local_prep_handoff_v1",
"id":"ART-G07-03","reviewer":"Sol xhigh independent",
"status":"PREPONLY_COMPLETE_HOLD_FOR_ROOT_ACTUAL_SCOPE_REVIEW",
"root_actual_scope_review_and_separate_release_required":True,
"no_artistic_pass":True,
"target_raw_sha256":"86add1bff80fe09bdeb5102e352cfe33e88bba1f3ed441ee94cdc76d01763de3",
"source_frame":507,"source_pts":270672,"time_base":"1/16000",
"purpose":"One proposed masked API local for plate removal plus same-ear lowroot/wholecoil reconnect; not plate-only and not a new FIRST.",
"formal8fields":rec(R/"API_PREPARED_REQUEST.json"),
"prompt":rec(R/"prompt_api.txt"),
"immutable_request_lock":rec(R/"REQUEST_LOCK_PREPONLY.json"),
"preview_only_guard":rec(R/"Preview-PreparedMaskedOnly.ps1"),
"preview_proof":rec(R/"API_PREVIEW_PROOF_PREPONLY.json"),
"guard_refusal_without_preview":rec(R/"PREVIEW_GUARD_REFUSAL_PROOF.json"),
"preview_result":p["wrapper_preview"],
"selected_mask":scope["records"][2],"separate_scope_masks":scope["records"][:2],
"actual_mask_review":rec(R/"ARTIST_ACTUAL_MASK_REVIEW_PREPONLY.json"),
"input_provenance":rec(R/"REFERENCE_SCOPE_DRAFT_PROVENANCE.json"),
"payload_manifest":rec(manifest),
"future_mandatory_whole_template":rec(R/"MANDATORY_WHOLE_TEMPLATE_NOT_DISPATCH.json"),
"parent_must_actual_view_first":[rec(R/"diagnostics_v03"/x) for x in ["COMBINED_OVERLAY_white_FULL_1x.png","COMBINED_OVERLAY_black_FULL_1x.png","PLATE_FACE_CONTACT_OVERLAY_4x.png","PLATE_RIGHT_HAND_OVERLAY_4x.png","LOWROOT_EAR_OVERLAY_4x.png","LOWROOT_C_OVERLAY_4x.png"]],
"observations":{
"plate_scope":"Disc face/rim and finger-gap prop editable; original hand/sleeve/visible face protected. Some ambiguous black contours at face/bob/rim contact intentionally remain protected for parent judgment.",
"root_scope":"Visible wrong crownside beads including glints and whole oldcoil editable. Ear skin/eye/face/mainbob protected; same-ear jaw/neck-end seam editable. No forced pixel point or fixed oldC.",
"transparent_hole":"Original prop-hidden jaw/mouth/neck/chest must stay transparent; no completion.",
"remaining_uncertainty":["face/prop mixed black line","bob/prop mixed tangent [775,275,910,345]","right-hand contour versus independent plate rim"],
"scope_fraction_is_not_artistic_or_release_pass":True},
"preserved_history":"Earlier plate-only v02, v01/v02 mask QA and reports180/181 all retained. No original/candidate art bytes changed.",
"boundaries":{"api_calls":0,"builtin_calls":0,"credentials_loaded":False,"network_access":False,"submitted":False,"root_release":False,"central_tables_modified":False,"root_primary_modified":False,"binding":False,"static_art_pass":False,"hidden_geometry_certified":False,"photography_pass":False,"dynamic_playback_pass":False,"user_accepted":False}
})
md="""G07-03 双 scope 局修准备已完成；仍为 HOLD，等待主代理实际查看并另行 release。没有 API/内置调用、联网、中央表或绑定修改。

- 当前 target 是已知首稿 86add1bf…763de3，原507 / PTS270672 / 1:16000。完整1344×1024，4个合适参考，high / n1 / transparent。
- 盘 scope 移除不透明盘面与独立盘沿，并保原盘前手、灰袖和真实可见脸；原被盘挡住的颌/嘴/胸保持透明，不补身体。
- root scope 去冠顶端旧珠根及整束旧卷，允许同可见耳靠实际颌颈端的低耳后窄缝重新接卷，部分珠可被 bob 挡；不从新根拉长S去追固定旧C。
- 最新两个 scope 的白黑全图、alpha、接触4x及 combined 全图均已实际看。盘/脸、盘/bob和右手描线接触仍有少量歧义保护边，见 ARTIST_ACTUAL_MASK_REVIEW_PREPONLY.json；需要主代理实际决定，未自行扩大权限。
- selected combined mask alpha0 editable / alpha255 protected；219177像素（15.9256%），这是技术范围记录，不是额度/艺术/release通过。
- Preview-PreparedMaskedOnly.ps1 只有 Preview 分支；不带 Preview 已实测拒绝。Preview 返回 submitted=false / input_count4 / mask=true，未读密钥、未建 attempt。
- 局修未来即使已知返图，也必须再完整内置重绘并全新双审与摄影；MANDATORY_WHOLE_TEMPLATE_NOT_DISPATCH.json 仅模板，不能 dispatch。

关键文件与精确SHA均在 ARTIST_HANDOFF_PREPONLY.json / PAYLOAD_MANIFEST_PREPONLY.json。旧盘-only草案、所有旧mask、失败证据保持。
"""
mp=R/"ARTIST_HANDOFF_PREPONLY.md"
if mp.exists():raise RuntimeError("Preserve handoff md")
mp.write_text(md,encoding="utf-8")
save("PREP_RESUMED_AND_COMPLETED_AFTER182_PHOTO.json",{
"status":"PREPONLY_COMPLETE","created_utc":datetime.now(timezone.utc).isoformat(),
"historical_suspension_preserved":"PREP_SUSPENDED_PRIORITY182.json",
"handoff":rec(handoff),"markdown":rec(mp),"api_calls":0,"network_access":False,"root_release":False})
print(json.dumps({"handoff":rec(handoff),"markdown":rec(mp),"manifest":rec(manifest),
"formal":rec(R/"API_PREPARED_REQUEST.json"),"prompt":rec(R/"prompt_api.txt"),
"mask":rec(R/"mask_COMBINED_RGBA_EDIT0_PROTECT255_v03.png"),
"lock":rec(R/"REQUEST_LOCK_PREPONLY.json"),"preview":rec(R/"API_PREVIEW_PROOF_PREPONLY.json"),
"no_attempt_files":True,"api_calls":0},ensure_ascii=False,indent=2))

