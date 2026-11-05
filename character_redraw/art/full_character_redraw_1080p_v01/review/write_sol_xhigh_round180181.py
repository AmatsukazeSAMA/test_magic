from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib,sys
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"review"
read=lambda p:json.loads(p.read_text("utf-8-sig"))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{"path":p.as_posix(),"sha256":sha(p)}
def save(p,d):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
views=read(R/"sol_xhigh_round180181_actual_views_v02.json")
policy=B/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"
assert sha(policy)=="b06daa9a9a043cbd26d3af8bab5125969faf05154a93bf2f9249defc69d06e4a"
ledger=read(B/"coverage/EXPOSURE_LEDGER.json")
data={
180:{"id":"ART-G06-01","run":"prep_first_api_source476_inverted_visibleonly_grayLEFT_v01","frame":476,"pts":254128,"first":425,
 "rawsha":"78b8374d8323ed5acb6ac5a3c331be9f00936b47643b39566d0d5079e137f52e",
 "summary":"repair_required：卷的宽前面到整片末C偏mint-green，非灰主面+薄mint材料条。盘区确透明且盘前手保留；当前不是实心/封盘结构否决。",
 "repair":"只按实际问题修回与bob一致的无打光GRAY宽前/返回及末C，保连续卷、当前合理发量、低LEFT倒悬根、原动作/裸足与现有盘区透明；若局修必须随后mandatory whole并fresh双审。",
 "p1":[{"severity":"P1","issue":"主卷材料薄荷化","location":"raw约[170,866,249,1018]，珠下各宽前面以及整个末C","evidence":"全白/全黑1x均见卷为大片mint-green，bob仍gray；当前来源3x也见mint占宽面与C，非仅窄边。","repair_required":True}],
 "criteria":[
  ("卷形与连续性","visible_connection_readable_material_repair_required","珠下各宽面经窄内返回连接下转与末C，WB3x可追；部分窗随底变色，不见明确全断、分离封口盖盘或实心锥P1。宽面不透明本身不是错误。","保这份可见连贯路径，不为去绿删除gray返回或强挖规定孔。","隐藏轴心/所有背返、真实3D不认证。"),
  ("发量与投影","no_visible_size_P1_static_only","完整倒悬头身中卷位于bob旁，宽度和可见长度属中等发量，没有tiny挂件或巨大粗卷；整体向屏幕下方落，符合倒悬静态方向。","不固定长度/圈数或复制正立11轴角，不为材料修复放大缩小卷。","没有原速/慢速或全组重力运动认证。"),
  ("发根与连接","visible_low_anatomical_LEFT_projection_retained","倒悬偏正面，唯一珠组在viewerLEFT可见耳/nape低根附近，珠下自然接单卷；其屏幕高度不能按正立耳高口诀判断。另一侧没有珠卷，无镜像身体迹象。","保同一解剖LEFT，低根相对头颌/耳颈而非屏幕y。","bob后根完整路线不可观察。"),
  ("材质与画风","repair_required_P1","bob灰、卷的主宽前面和整C则大片偏mint-green；全WB1x已有明显材料差，3x进一步确认，并非一条窄材料边。无须依赖量色阈值才能判错。","宽面/返回/末C归同bob的无光GRAY，mint只作细材料条；保卷形与体量。","softgray与肤色柔差另外P2；不称严格平涂通过。"),
  ("空间遮挡","visible_character_only_hole_retained_registration_pending","大盘主体位置随WB底色改变；横跨盘区的张掌/前臂、另一侧抓沿手/灰袖仍保，源盘挡胸腹未被补成新身体。源/返图下颌口部均紧邻盘边，未凭参考补出完整新嘴。","盘/独立rim仍由后期；source接触和人物切口需另行真实摄影，不因盘洞已透明自动签边界注册。","被原盘/幽灵挡住的手/躯干细节不认证。"),
  ("整个人物及透明边缘","source_visible_pose_retained_with_material_repair","完整raw/WB/母476native及ownsource：倒悬头身、闭睫无iris、灰松袖和深衣边、横臂张掌及另一抓沿手、两条不同角裸足均保；没有误添maidcap/黑叶/普通女仆鞋装。主盘空区真透明。","脚趾/袖幅/脸廓局部差P2，后续uniform摄影必须联合原脚/手/头及盘接触；不可用补hiddenbody解决空区。","未做1920注册、全曝光复用、动态图/用户验收。")
 ]},
181:{"id":"ART-G07-03","run":"prep_first_api_source507_inverted_visibleonly_grayLEFT_v01","frame":507,"pts":270672,"first":507,
 "rawsha":"86add1bff80fe09bdeb5102e352cfe33e88bba1f3ed441ee94cdc76d01763de3",
 "summary":"repair_required：画面上方大块白盘及黑rim被实画进人物PNG；黑底仍不消失。完整耳廓3x还显示珠根接在朝bob冠顶一端，不能把LEFT投影侧对等同低nape正确；需核正低根高度。眼/灰卷连续性当前未见另项P1。",
 "repair":"先移除不属于人物层的opaque白盘/独立黑rim及必要alpha残边，保灰袖/盘前或盘旁手/皮肤/bob/原眼与可读gray返回；原盘挡颏嘴胸处仍透明、不补hiddenbody。当前珠根相对倒悬耳颌轴的高度另外需核正，不可称盘-only修复足够；任何后续根修复须独立锁作用域，不能擅自扩大盘mask。若局修后须mandatory whole并fresh双审。",
 "p1":[{"severity":"P1","issue":"独立道具白盘/黑rim残留于人物层","location":"raw上方约x[435,1215],y[0,300]的盘面及沿其下缘弧形黑rim；不要把左灰袖/右手当作盘删掉","evidence":"全黑QA仍见巨大白盘和弧rim；当前raw alpha支持盘面[750,80]/[900,180]均A254。该不透明道具违反only人物/盘留后期，不能靠摄影移位解释。","repair_required":True}],
 "criteria":[
  ("卷形与连续性","visible_connection_readable_no_solid_P1_found","当前宽gray前面经可见窄斜gray返回连到下一收细转折和末C，WB3x可追；内窗口部分随底变色，返回中仍有不透明灰段。未见明确互不连接的封口片堆或全断。","保宽gray和实体gray返回，不把opaque或压扁椭圆直接判实心，不为去盘重造卷。","所有隐藏内轴、背返及空气拓扑不认证。"),
  ("发量与投影","no_visible_size_P1_static_only","完整大头上下文中coil沿bob旁下落，宽度/体量合理，非tiny挂件或巨大粗卷；末C不延伸成腰尾。","保当前合理体量，不套11正立比例/固定圈数。","独立镜头倒悬摆动及相邻实际播放未审。"),
  ("发根与连接","repair_required_visible_attachment_height","唯一双珠在倒悬viewerLEFT，侧别投影本身未见换侧。但完整耳廓3x可见耳约raw y421..516，两珠接合约y536..543，朝bob冠顶/头顶一端，而颏颈在盘沿的屏幕上方；这是沿当前头颌轴的相对位置，不是把屏幕y套正立规则。可见接合点有解剖耳上侧安装问题，低nape不应据侧对直接放行。","重新核同一LEFT低耳后/颈侧接合，不镜像身体或换RIGHT；盘-only mask不得自动扩到root。隐藏根可遮，但不能凭隐藏为当前可见高接合自证正确。","完整bob后root/3D不认证；初全图侧对判断不足，完整耳廓观察优先。"),
  ("材质与画风","P2_soft_gray_mechanical_return_edges","宽前和末C目前主要是gray，mint色差窄/轻，未见180那种整片mint主面；窄规则返回/略soft灰面和几何分段线感P2 OPEN。无明确独立银白高光/深暗返回块P1。","去盘时保当前gray主面/不透明返回；不得因机械线感挖掉灰带。","严格平涂/所有隐藏面不认证。"),
  ("空间遮挡","repair_required_P1_prop_layer_contamination","原盘本来遮住颏/嘴/胸；新图把大白盘和独立黑rim保留成实体，当前人物层不再是only可见人物。盘旁手/上方松灰袖仍是源真实人物，不能扩大去盘区域误删它们。","独立道具移交后期；原盘挡住区域透明，不补嘴/胸/新身体。精细人物-盘接触按原507边界处理。","源盘后颏嘴胸的隐藏像素不恢复、不认证。"),
  ("整个人物及透明边缘","repair_required_P1_plate_other_visible_pose_retained","实际raw/fullWB/源507native：倒悬裸头、大头裁切、顶部灰袖和抓沿部分手保；双眼仍为源不等睁开/斜眼轴、单深色平填和普通小白点，无旧灰月牙或黑中心灰环P1；没有新O口/笑嘴、帽叶、画外腿鞋。人物外空区换底，但大盘主体不换底。","只修盘与必要边缘并保source可见人物；局部肤/袖/发线软差P2，摄影pending。","没有全重复曝光复用、注册/动态/用户通过。")
 ]}
}
for n in ([int(x) for x in sys.argv[1:]] or [180,181]):
 d=data[n];aid=d["id"];run=B/"drawings"/aid/"v01"/d["run"]
 raw=run/"character_api_original.png";assert sha(raw)==d["rawsha"]
 src=Path("D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels")/aid.removeprefix("ART-")/"source.png"
 result=read(run/"result.json");assert result["output_sha256"]==sha(raw)
 q=read(run/"API_PREPARED_REQUEST.json")
 for x in result["inputs"]:assert sha(Path(x["path"]))==x["sha256"]
 actual=[]
 for p in views[f"round{n}"]:
  p=Path(p);actual.append({**ev(p),"dimensions":list(Image.open(p).size)})
 actualhash=hashlib.sha256(json.dumps(actual,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
 primary=run/"PRIMARY_GOAL_REVIEW.json";pr=read(primary) if primary.exists() else {}
 docs=[run/"result.json",run/"ROOT_API_EXECUTION_RECEIPT.json",run/"request_manifest.json",run/"API_PREPARED_REQUEST.json",run/"prompt_effective.txt",run/"SOURCE_VISIBLE_SCOPE_AUDIT_PREPONLY.json",run/"ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json",R/f"sol_xhigh_round{n}_diagnostics/PROVENANCE.json",policy]
 if n==181:
  docs.append(R/"sol_xhigh_round181_diagnostics/EAR_BEAD_DIAGNOSTIC_PROVENANCE.json")
  d["p1"].append({"severity":"P1","issue":"可见珠根朝头顶一侧安装，不能认证低耳后nape","location":"完整耳廓ROI[250,330,495,610]；耳约y421..516，珠接合约y536..543，须沿倒悬头颌轴理解","evidence":"完整耳/root3x中接合处在冠顶一端，原盘沿处才是颏颈方向；初步只确认LEFT侧对不足。","repair_required":True,"hidden_root_geometry_not_claimed":True})
 if primary.exists():docs.append(primary)
 criteria=[{"criterion":a,"status":b,"observation":c,"treatment":e,"not_observable":f} for a,b,c,e,f in d["criteria"]]
 entry={
 "id":aid,"reviewer":"Sol xhigh independent actual-image review","run":run.as_posix(),
 "image":raw.as_posix(),"image_sha256":sha(raw),"dimensions":list(Image.open(raw).size),
 "artifact":{"path":raw.as_posix(),"raw_sha256":sha(raw)},"actual_viewed":True,
 "curl_structure_policy_id":"open_hollow_ribbon_20261101_v01",
 "requirements_revision":"goal_curl_assessment_20261102_v03","requirements_path":policy.as_posix(),"requirements_sha256":sha(policy),
 "source_frame":d["frame"],"source_pts":d["pts"],"source_time_base":"1/16000",
 "canonical_source":src.as_posix(),"canonical_source_sha256":sha(src),
 "source_pose_guide":str(Path(q["InputImages"][0])).replace("\\","/"),
 "first_case_frame":d["first"],"first_source_nomination_frame":d["first"],
 "first_case_scene_start_frame":None,"first_case_scene_end_frame":None,
 "source_nomination_timing":read(run/"SOURCE_VISIBLE_SCOPE_AUDIT_PREPONLY.json")["source_visible_exposure_nominations"],
 "all_nominated_exposures_actually_viewed":False,"exposure_reuse_certified":False,
 "primary_review_available_at_review":primary.exists(),"primary_static_pass_recorded":bool(pr.get("primary_static_pass",False)),
 "primary_review_path":primary.as_posix() if primary.exists() else None,
 "primary_review_sha256_before_attachment":sha(primary) if primary.exists() else None,
 "operation_kind":"FIRST_official_API_reference_image","provider":"OpenAI API","model":result["model"],
 "known_generation_count_recorded":1,"provider_elapsed_seconds_recorded":result["elapsed_seconds"],
 "current_review_API_calls":0,"current_review_native_calls":0,"current_review_network_calls":0,
 "receipt_not_art_pass":True,"PREP_history_not_current_return_status":True,
 "whole_character_completed_recorded":False,"local_repair_parent":None,
 "exact_reference_paths":[str(Path(x)).replace("\\","/") for x in q["InputImages"]],
 "full_prompt_actually_read":True,"full_prompt_path":(run/"prompt_effective.txt").as_posix(),"full_prompt_sha256":sha(run/"prompt_effective.txt"),
 "actual_viewed_paths":[x["path"] for x in actual],"actual_viewed_evidence":actual,"evidence_sha256":actualhash,
 "evidence_document_paths":[x.as_posix() for x in docs],"evidence_documents":[ev(x) for x in docs],
 "review_status":"repair_required","repair_required":True,"recommendation":d["repair"],"summary":d["summary"],
 "independent_static_pass":False,"source_visible_body_actually_reviewed":True,
 "root_laterality_repair_required":False,"root_height_repair_required":n==181,"eye_mono_material_repair_required":False,
 "headwear_extra_leaf_repair_required":False,"visible_curl_geometry_repair_required":False,
 "visible_curl_size_repair_required":False,"visible_curl_material_repair_required":n==180,
 "visible_curl_occlusion_repair_required":False,"independent_prop_alpha_repair_required":n==181,
 "material_concern_open":True,"strict_flat_material_certified":False,
 "spatial_identity_rule":"Fixed anatomical LEFT low ear/nape; current original frontal inversion projects toward viewerLEFT. Assess relative to rolled head/ear/chin, not upright screen-y or mirrored body.",
 "per_criterion_assessments":criteria,"issues":d["p1"]+[{"severity":"P2","issue":"softgray/肤色柔差、窄机械返回线和局部脸/手/袖/发轮廓差；真实摄影联合定位及人物-盘边界待核。","open":True,"repair_required":False}],
 "alpha_support":read(R/f"sol_xhigh_round{n}_diagnostics/PROVENANCE.json")["RGBA_point_support_only"],
 "alpha_evidence_boundary":"WB实际观感优先；点alpha和诊断只是支持，不替代美术判断，不从raw隐藏RGB误判背景。",
 "comparison_evidence_roles":{"own_source":"Action/expression/costume/crop/disc contact exclusive authority.","correct11_fullhead":"Relative volume/connected ribbon context only; no maidcap/costume/pose transfer.","latest_gray_detail":"Broad gray material surfaces and narrow mint edge/continuous return only, no glossy light transfer.","G02":"Single charcoal pigment/plain small glint method, not its half-lid aperture or heart-shaped detail.","preceding_bob_crop":"Bare short-bob identity context only; current source expression and gray material override old shading."},
 "hidden_geometry_certified":False,"complete_curl_master_certified":False,"source_visible_extent_coverage_verified":False,
 "photographic_registration_validated":False,"continuous_playback_validated":False,"dynamic_validated":False,
 "renderer_verified":False,"user_accepted":False,"art_accepted":False,"user_explicitly_rejected_this_raw":False,
 "technical_pixel_splice_asserted":False,"transparent_complete_disconnect_asserted":False,
 "public_registry_selection_binding_modified":False
 }
 report={"report":f"sol_xhigh_round{n}","date":"2026-11-02","reviewer":"Sol xhigh independent actual-image review",
 "requirements_revision":"goal_curl_assessment_20261102_v03","requirements_path":policy.as_posix(),"requirements_sha256":sha(policy),
 "review_scope":"Fresh actual current FIRST raw/full white-black/own canonical+native+guide/all five exact inputs/full effective prompt/current source-hashed WB3x/eye3x/alpha; no reuse from PREP or HTTP success.",
 "entries":[entry],"generation_calls_by_reviewer":0,"network_calls_by_reviewer":0}
 save(R/f"sol_xhigh_round{n}.json",report)
 md=f"""# Sol xhigh Round {n} — {aid}

**repair_required**。{d['summary']}

原图：{raw.as_posix()}  
SHA256：{sha(raw)}  
母帧 F{d['frame']} / PTS {d['pts']} / time_base 1/16000。最早源提名 F{d['first']}；本轮仅审母帧当前图，不确认全部提名复用或绑定。

实际查看 raw、完整白/黑底、原PV母帧native/完整source/guide、五张正式输入、当前来源的根卷WB3x/眼3x/盘alpha，以及correct11头肩体量/G02/最新宽灰细图；共{len(actual)}个图像文件。全部路径及SHA在JSON；完整effective prompt与一次known回执已核。HTTP/回执不是美术通过。

"""
 for c in criteria:md+=f"- **{c['criterion']}**：{c['observation']} {c['treatment']} 不认证：{c['not_observable']}\n"
 md+=f"""
修复建议：{d['repair']}

P2 OPEN：软灰/肤色柔差、窄机械返回及局部脸手袖发轮廓。摄影和人物-盘接触仍待；不可用摄影消除当前明确P1。原被盘挡的躯干/口颌不是可补齐的人体证据。

本轮reviewer API/native/network均0，只写自己报告/只读诊断，未改中央或绑定。隐藏3D、摄影、全曝光复用、原速/慢速播放与用户验收均未通过。
"""
 mp=R/f"sol_xhigh_round{n}.md";assert not mp.exists();mp.write_text(md,encoding="utf-8")
 print(json.dumps({"round":n,"id":aid,"decision":"repair_required","raw_sha256":sha(raw),"json":ev(R/f"sol_xhigh_round{n}.json"),"md":ev(mp),"actual_image_count":len(actual)},ensure_ascii=False))

