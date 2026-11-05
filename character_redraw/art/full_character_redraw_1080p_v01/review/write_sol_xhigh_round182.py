from pathlib import Path
from PIL import Image
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"review";run=B/"drawings/ART-G33-17/v01/whole_imggen_after_continuous_ribbon_local_v07"
read=lambda p:json.loads(p.read_text("utf-8-sig"))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{"path":p.as_posix(),"sha256":sha(p)}
raw=run/"character_imggen_original.png"
assert sha(raw)=="e2f92af8e6f84dad11615ef84fe72b3daa8d89f3f6e343ffb89d4f587462962b"
builtin=read(run/"BUILTIN_GENERATION.json")
q=read(run/"request_imggen_ROOT_AUTHORIZED.json")
primary=run/"PRIMARY_GOAL_REVIEW.json";pr=read(primary)
assert pr["image_sha256"]==sha(raw)
for x in builtin["reference_inputs"]:
 assert sha(Path(x["image"]))==x["sha256"]
policy=B/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"
assert sha(policy)=="b06daa9a9a043cbd26d3af8bab5125969faf05154a93bf2f9249defc69d06e4a"
src=Path("D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-17/source.png")
views=read(R/"sol_xhigh_round182_actual_views.json")["actual_viewed_paths"]
actual=[{**ev(Path(p)),"dimensions":list(Image.open(p).size)} for p in views]
viewhash=hashlib.sha256(json.dumps(actual,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
ledger=read(B/"coverage/EXPOSURE_LEDGER.json")
timing=[{k:f[k] for k in ["frame","pts","end_pts","duration_ticks"]} for f in ledger["frames"] if f["frame"] in [895,896,897,898]]
criteria=[
 {"criterion":"卷形与连续性","status":"retained_visible_static_candidate",
  "observation":"完整头身先看，再核当张WB4x/alpha：上段宽gray面经可见窄灰回边/内返接下一宽面；中下段已经改为连贯转折并渐细接末C。实际与旧v06白底对照，旧中段2–3个分叉毛尖与下方独立灰囊均不再可见。可见段没有清楚分离封口盖片/直发束终止后另包灰囊P1；不是仅凭末C存在或alpha连通判通过。",
  "treatment":"保当前宽GRAY与不透明返回；较圆/压紧的窄返和机械边界留P2，不以固定孔数/圈数或挖opaquegray修读法。",
  "not_observable":"被bob/红bow/frill遮住的背返和轴心不认证，完整hidden3D与全卷master不认证。"},
 {"criterion":"发量与投影","status":"retained_medium_head_chest_volume_P2_projection_pending",
  "observation":"完整当前bob/颈肩/红结/胸身中，卷体位于画右前胸外沿，长度至胸侧C，体量中等；没有tiny附件、腰长粗尾或超头巨大卷。新轮廓比旧v06发团式鼓起收整。",
  "treatment":"不为追求更大空窗再膨胀，亦不缩成小挂件；相邻转身段固有发量与投影变化另核，不套固定ratio。",
  "not_observable":"15→20→17时序/原速慢速连续性未播放，不能由本静态候选认证。"},
 {"criterion":"发根与连接","status":"visible_far_LEFT_front_route_compatible_hidden_root_not_certified",
  "observation":"本向画右front3/4中，画左近耳/后脑未新增红珠根；露卷从画右低bob/颏颈附近进入同侧前胸。双珠及实际低root被farbob/颈肩遮住，未见可见高根或错侧接合，但隐藏低位不能靠prompt或遮挡自行认证。",
  "treatment":"保固定解剖LEFT远侧、当前bob遮挡及自然接缝，不强掀bob露珠、不镜像或换到近侧。",
  "not_observable":"精确隐藏红珠/低nape/root3D路线不可观察，不宣称已经证实隐藏根位置。"},
 {"criterion":"材质与画风","status":"retained_with_P2_softgray_narrowmint",
  "observation":"宽面及末C主要为与bob相近的GRAY，mint是较窄边条；没有整片mint主面、银白高光或独立深暗返回底块P1。softgray轻差、少量浅边和压紧窄返仍有P2；眼各一块深charcoal加普通小白点，无黑中央芯+浅灰环/下月牙。",
  "treatment":"P2具体保留，不称严格每pixel同色平填。不得用深暗/银亮面增强体积，也不为抹轻差破坏已可读灰带。",
  "not_observable":"所有隐面材质与严格平涂不认证。"},
 {"criterion":"空间遮挡","status":"retained_visible_front_shoulder_T",
  "observation":"颏、黑领/redbow与白frill形成可见前景T；gray卷位于画右肩前胸外缘，没有回到近侧后脑/背肩。部分白窗口在黑底仍白，是原白frill实体，不当作空气；C内开口随底变色。不能用白窗去认证完整轴心或把frill抹成洞。",
  "treatment":"保原衣肩与当前前胸路线，不扩大衣服遮错发、不强拉隐藏段到前景。",
  "not_observable":"隐藏路线/准确绕肩3D及连续遮挡动态未认证。"},
 {"criterion":"整个人物及透明边缘","status":"retained_source_action_full_canonical_body_first_crop_pending",
  "observation":"新raw完整WB、原2374全身/guide和895..898四native均actual：原圆睁眼开度/视线与小闭弧笑、画右front3/4头身、近侧屈肘/袖口回腰后且手原遮挡、远手隐藏、两主要黑帽叶在viewerRIGHT、黑领红bow金扣/白肩袖frill/腰后结带/长apron黑裙、交叉腿和两不同角度踝带鞋均保。没有借first半身裁切删母稿腿鞋，WB无实体背景/明显halo或新拼缝P1。",
  "treatment":"局部帽/bob/衣袖/frill/腰裙鞋廓差P2。canonical两全鞋与first895..898半身分开，后续新uniform摄影按实际半身源定位裁切，不在首段露隐藏腿鞋。",
  "not_observable":"未做新摄影，源1080定位/extent、全片复用、renderer/原速慢速/用户验收均未过。"}
]
docs=[run/"BUILTIN_GENERATION.json",run/"NATIVE_CALL_RECEIPT.json",run/"request_imggen_ROOT_AUTHORIZED.json",run/"prompt_imggen.txt",primary,R/"sol_xhigh_round182_diagnostics/PROVENANCE.json",policy,run.parent/"JOB.json"]
e={
 "id":"ART-G33-17","reviewer":"Sol xhigh independent actual-image review",
 "run":run.as_posix(),"image":raw.as_posix(),"image_sha256":sha(raw),"dimensions":list(Image.open(raw).size),
 "artifact":{"path":raw.as_posix(),"raw_sha256":sha(raw)},"actual_viewed":True,
 "curl_structure_policy_id":"open_hollow_ribbon_20261101_v01",
 "requirements_revision":"goal_curl_assessment_20261102_v03","requirements_path":policy.as_posix(),"requirements_sha256":sha(policy),
 "source_frame":2374,"source_pts":1267408,"source_time_base":"1/16000",
 "canonical_source":src.as_posix(),"canonical_source_sha256":sha(src),
 "source_pose_guide":(run/"inputs/ref2_ORIGINAL2374_COMPLETE_UNMASKED_ACTION_GUIDE.png").as_posix(),
 "first_case_frame":895,"first_case_scene_start_frame":895,"first_case_scene_end_frame":898,
 "first_case_pts_range":[477808,479952],"source_native_frame_timing":timing,
 "primary_review_available_at_review":True,"primary_static_pass_recorded":bool(pr["primary_static_pass"]),
 "primary_review_path":primary.as_posix(),"primary_review_sha256_before_attachment":sha(primary),
 "exact_reference_paths":[Path(p).as_posix() for p in q["refs"]],
 "full_prompt_actually_read":True,"full_prompt_path":(run/"prompt_imggen.txt").as_posix(),"full_prompt_sha256":sha(run/"prompt_imggen.txt"),
 "operation_kind":"whole_character_redraw","whole_character_completed_recorded":True,
 "mandatory_whole_after_local_repair_completed_recorded":True,
 "local_repair_parent":builtin["local_repair_parent"],"local_parent_SHA":"7ac2b5ab14558eaa8714e8890b80a43129e175d358fcde1fc3fd48b3018748c1",
 "generation_receipt_is_not_art_pass":True,"old179_and_local_art_status_not_inherited":True,
 "actual_viewed_paths":[x["path"] for x in actual],"actual_viewed_evidence":actual,"evidence_sha256":viewhash,
 "evidence_document_paths":[p.as_posix() for p in docs],"evidence_documents":[ev(p) for p in docs],
 "review_status":"retained_static_candidate","repair_required":False,"independent_static_pass":True,
 "recommendation":"Retain current visible static candidate only. Fresh uniform photography for895..898 and continuous source-timed playback remain required; do not certify hidden root or full coil master.",
 "root_laterality_repair_required":False,"root_height_repair_required":False,"eye_mono_material_repair_required":False,
 "headwear_extra_leaf_repair_required":False,"visible_curl_geometry_repair_required":False,
 "visible_curl_size_repair_required":False,"visible_curl_occlusion_repair_required":False,"visible_curl_material_repair_required":False,
 "material_concern_open":True,"strict_flat_material_certified":False,
 "source_visible_body_actually_reviewed":True,"source_full_legs_and_two_shoes_actually_reviewed":True,
 "all_four_first_native_frames_actually_viewed":True,"canonical_and_first_crop_distinguished":True,
 "canonical_two_complete_shoes_visible":True,"first_case_legs_and_shoes_visible":False,
 "per_criterion_assessments":criteria,
 "issues":[
  {"severity":"P2","issue":"上/中转较圆、窄返回边及少量mint线较机械；软灰轻差/浅边","repair_required":False,"open":True,"not_downgraded_P1":"当前未见旧fork/graypouch或明显独立打光；不因不透明而判实心。"},
  {"severity":"P2","issue":"帽bob/袖肩frill/腰裙鞋等局部源轮廓差；与前邻转身的体量和投影衔接仍待真实时序核对","repair_required":False,"open":True},
  {"severity":"P2","issue":"当前稿尚未做895..898新uniform摄影；应维持原半身范围，不露母稿画外腿鞋","repair_required":False,"photographic_condition_pending":True}],
 "diagnostic_provenance":ev(R/"sol_xhigh_round182_diagnostics/PROVENANCE.json"),
 "old_PREP_prior_local_diagnostics_not_current_whole_evidence":True,
 "alpha_support":read(R/"sol_xhigh_round182_diagnostics/PROVENANCE.json")["alpha_point_support_only"],
 "alpha_boundary":"Full actual WB/current4x first, alpha samples support only. Whole gray faces remain nearopaque; white frill is not automatically air. Raw hiddenRGB dots are not claimed visible halo.",
 "comparison_evidence_roles":{"old_v06_white":"Actually viewed rejected fork/blob comparison only, no verdict inheritance.","local7ac2_full":"Actual input intermediate only; mandatorywhole newbytes independently viewed.","correct11":"Connected gray ribbon/taperC and fullhead relative volume only, no fixed turns/axis or costume/eyes transfer.","latest_gray_detail":"Grayface and grayreturn structure only, no gloss transfer.","G02":"Single charcoal/plain small glint method; own2374 aperture/expression remains exclusive."},
 "hidden_geometry_certified":False,"hidden_root_position_certified":False,"complete_curl_master_certified":False,
 "source_visible_extent_coverage_verified":False,"photographic_registration_validated":False,
 "continuous_playback_validated":False,"dynamic_validated":False,"renderer_verified":False,
 "user_accepted":False,"art_accepted":False,"user_explicitly_rejected_this_raw":False,
 "public_registry_selection_binding_modified":False,"reviewer_API_calls":0,"reviewer_native_calls":0,"reviewer_network_calls":0
}
report={"report":"sol_xhigh_round182","date":"2026-11-02","reviewer":"Sol xhigh independent actual-image review",
 "requirements_revision":"goal_curl_assessment_20261102_v03","requirements_path":policy.as_posix(),"requirements_sha256":sha(policy),
 "review_scope":"Fresh wholev07 current exactraw/fullWB/4exactrefs/fullprompt/source2374full+895..898all4native/current4xWB-alpha-eyes/oldv06actualcontrast/G02/approved11graydetail. No local or179 pass inheritance.",
 "entries":[e],"reviewer_generation_calls":0,"reviewer_network_calls":0}
p=R/"sol_xhigh_round182.json";assert not p.exists();p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md=f"""# Sol xhigh Round182 — ART-G33-17 whole v07

**retained_static_candidate**。新整张实际未见明确P1；仅保留当前可见静态候选，不是用户验收、摄影或动态通过。

原图：{raw.as_posix()}  
SHA256：{sha(raw)}  
957×1643；母2374/PTS1267408。first895..898 / PTS477808..479952，time_base1/16000。

实际查看完整raw/白黑、四张exact输入/完整prompt、原2374完整人物和895–898全部四native、旧v06白底、当张精确来源的卷WB4x/alpha/眼4x，以及G02/用户正确11头肩体量和灰带细图；共{len(actual)}个图像文件，路径/SHA均在JSON。run内PREP_PRIOR_LOCAL7ac2诊断不是当前whole证据，未拿它冒充新图。

"""
for c in criteria:md+=f"- **{c['criterion']}**：{c['observation']} {c['treatment']} 不认证：{c['not_observable']}\n"
md+="""
P2 OPEN：圆/压紧窄返回与机械边线、softgray/少量浅边、局部帽脸袖肩腰裙鞋轮廓差；前邻转身的发量/投影衔接仍待时序。

旧v06分叉毛尖和下方独立灰囊已不见；该结论来自新全图和当张4x，而非局修回执或alpha连通。根珠被farbob/颈肩遮，只能说可见路线未见错侧/高根，不能认证隐藏低root精确位置。canonical完整双鞋保留，first半身另做新uniform摄影。

本轮API/native/network均0，只写自己报告和只读诊断；未改中央或绑定。隐藏3D、全卷master、摄影、renderer、原速/慢速连续播放与用户验收均false。
"""
mp=R/"sol_xhigh_round182.md";assert not mp.exists();mp.write_text(md,encoding="utf-8")
print(json.dumps({"id":"ART-G33-17","decision":"retained_static_candidate","raw_sha256":sha(raw),"json":ev(p),"md":ev(mp),"actual_image_count":len(actual)},ensure_ascii=False))

