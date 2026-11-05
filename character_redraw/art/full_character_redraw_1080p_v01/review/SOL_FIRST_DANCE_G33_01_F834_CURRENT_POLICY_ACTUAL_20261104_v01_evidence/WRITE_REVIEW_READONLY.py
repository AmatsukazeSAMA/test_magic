from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03"
D=B/"review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence"
O=B/"review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_imggen_original.png"; assert h(raw)=="72b667deeb5be1f163e29a66700c8ea81f8cb8dc80afe28e0bbac62e6f8a7fec"
v=json.loads("[\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000834.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000840.png\",\"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-01/source.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/inputs/source_pose_guide.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03/character_imggen_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03/qa_white_coil_diagnostic_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/whole_imggen_hollow_flat_motion_v03/qa_black_coil_diagnostic_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/ALL_NATIVE_SOURCES_PAGE_1.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/ALL_NATIVE_SOURCES_PAGE_2.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/ORIGINAL_CANONICAL2306_UNIFORM_VS_ACTUAL834.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/CURRENT_LOWROOT_SHOULDER_CONTEXT_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/CURRENT_LOWROOT_SHOULDER_CONTEXT_black_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/CURRENT_SMALL_TAIL_CONTEXT_white_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_DANCE_G33_01_F834_CURRENT_POLICY_ACTUAL_20261104_v01_evidence/CURRENT_SMALL_TAIL_CONTEXT_black_5x.png\"]");e=json.loads((D/"ACTUAL_SOURCE_AND_BINDING_EVIDENCE.json").read_text(encoding="utf-8"))
ledgerpath=B/"coverage/EXPOSURE_LEDGER.json";ledger=json.loads(ledgerpath.read_text(encoding="utf-8-sig"))
frames=[{k:f[k] for k in ["frame","pts","end_pts","duration_ticks","source_frame"]} for f in ledger["frames"] if 834<=f["frame"]<=840]
progpath=B/"dance_first10_reference_redraw_v01/PROGRESS.json";scopepath=B/"dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json";bindings=B/"dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json"
prog=json.loads(progpath.read_text(encoding="utf-8-sig"))
scope=json.loads(scopepath.read_text(encoding="utf-8-sig"))
state=[x for x in scope["states"] if x["id"]=="ART-G33-01"][0]
canon=Path(state["original_source_master"])
jpath=B/"drawings/ART-G33-01/v03/JOB.json";j=json.loads(jpath.read_text(encoding="utf-8-sig"))
obj={
"id":"ART-G33-01","reviewer":"Sol xhigh fresh independent actual source/exposure and current-policy art review",
"scene_start_frame":834,"scene_end_frame":840,"exposure_count":7,
"image":str(raw),"image_sha256":h(raw),"raw_dimensions":[992,1586],
"review_status":"repair_required","repair_required":True,
"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04",
"requirements_revision":"goal_curl_assessment_20261104_v10",
"review_scope":"One state only: actual F834..840 sources plus current72b667 art, not a batch66 approval or playback validation.",
"source_equivalence":{
"review_status":"confirmed_visible_source_state_reuse",
"canonical_id":"ART-G33-01","canonical_source_frame":2306,"canonical_pts":1231104,"canonical_image":str(canon),"canonical_image_sha256":h(canon),
"actual_first_exposure_frame":834,"actual_first_exposure_pts":445248,"actual_end_pts_exclusive":448976,"time_base":"1/16000",
"actual_source_frames":e["source_frames"],
"actual_view_method":"Native full F834/F840 plus two readonly, unresized 520x960 subject-crop contact pages covering all seven actual source PNGs. Full canonical2306 and its guide opened; ORIGINAL-only uniform side-by-side inspected.",
"source_observations":[
"F834..840可见帽褶/发线、双闭眼多道眼线/小中性闭口、头颈、胸前红bow折边/金扣、左右frill内三角/长竖线、袖缝/右cuff描线保持同一画型。橙底/粉色wipe与歌词变化独立，不构成新人物重描。",
"canonical2306经单一等比放大平移后，上述帽/眼/口/颈/bow/frill/腰与低垂双袖能同时对应actual834，而非只凭脸相似或预存ID。仅原source对原source，无生成身体/AI动作跟踪/局部warp。",
"首段为放大半身viewport，右cuff下手部及全腿鞋被原1080下沿裁外；canonical的裁外部分不能拿来证明first834隐藏细节，也不得在first段显示腿鞋。"
],
"diagnostic_uniform_transform":{"scale":1.809475806451613,"translation":[-788.7883064516129,-13.465221774193594],"scope":"Historical original-source face estimate used only as fresh visually checked diagnostic; not production layer placement."},
"new_visible_drawing_state_required":False,"new_canonical_id_recommendations":[],
"source_author_cel_identity_claimed":False,"hidden_original_geometry_reconstructed":False,
"reuse_boundary":"Reuse current stable source-state ID for the visible upper-body strokes; first-scene photography must be separately reviewed. This does not approve current generated curl or canonical full-body placement."
},
"segments":[{"start_frame":834,"end_frame":840,"status":"confirmed_binding","canonical_id":"ART-G33-01","observation":"Actual seven visible-source exposures match same original drawn state under distinct half-body scale/crop; generated asset remains repair_required under current curl policy."}],
"current_art_assessment":{
"review_status":"repair_required",
"P1":[
{"area":"低根/两珠/肩前路线","raw_roi_xyxy_exclusive":[604,235,760,501],
"finding":"珠约中心(653,260)/(653,280)仍固定在侧脑较高位置，接近当前闭眼层级；可见bob末缘/下颌颈基在更低处约y340..370。该侧耳被bob遮，未虚构可见耳垂；但实际没有低bob/nape先接两珠再绕到颈胸前的连接。",
"route":"主卷从高侧脑沿画右向外下悬，较大部分位于本白肩frill外侧；不是同一低根在本肩/领前自然叠压的当前要求。一个原位整体平移/缩放不能修复人物内部根位与肩前深度。",
"repair_direction":"保留自身闭眼/中性闭口、直立低垂双袖及衣装动作，重建解剖LEFT低耳后bob/nape→两珠→单束本肩前路线。不要只靠把整层向下注册、加孔或挖opaquegray返回来伪修。"}
],
"retained_visible_features":[
"双实际闭眼/小中性闭口和原低垂双臂类型保留，未将AI笑口或睁眼套入。canonical完整衣裙/长袖/白frillapron后带及鞋可见范围基本保留；first段仍须原底裁。",
"三处主要空窗确实白黑切换，宽gray前面与opaque返回连续，不能将原raw透明RGB绿点当填芯，也不应为了更多孔删除grayreturn。",
"第三转相对上两转变小并有下返回/渐尖尾段，可保其连接证据；不因孔数相同就认证完整2Large+trueSmall+C或隐藏拓扑。"
],
"P2":[
{"area":"末端C/卷型读感","raw_roi_xyxy_exclusive":[655,416,758,499],"finding":"末端呈宽叶片式半回弧，细收C不如认可8e0明确，上下开环节距亦较匀；修高根/路线时应逐段保持两大、独立小转再C，不凭三洞等价于三圈。不单凭此局部可读性另新增源画型。"},
{"area":"材料","finding":"mint明显较鲜绿，gray与bob总体同族但有轻微软面和规整内圈线；不称严格低饱和平涂匹配，也不以容许内灰差豁免根位P1。"}
],
"art_static_passed":False,
"prior_round60_or_existing_binding_art_pass_inherited":False
},
"eye_applicability":{
"viewer_left":"closed_no_visible_iris_actual_viewed",
"viewer_right":"closed_no_visible_iris_actual_viewed",
"secondary_eye_local_status":"art_repair_required_current_closed_no_visible_iris_actual_viewed",
"secondary_eye_local_passed":False,
"normal_eye_B_low_saturation_note":"当前两眼确实闭合，无可改虹膜，不因全片后续B配色而补/强睁；新修稿通过后仍逐眼重新分类，正常可见眼另行B低饱和Py。此报告未执行颜色编辑。"
},
"photography_assessment":{
"review_status":"not_revalidated_in_this_current_policy_report",
"existing_binding_is_not_art_proof":True,
"bound_master_sha256":"72b667deeb5be1f163e29a66700c8ea81f8cb8dc80afe28e0bbac62e6f8a7fec",
"existing_layer_sha256_from_metadata":"3488905ebc9c96ed50ab275bdba6fa02098156af4ae5c670b79c4e167637ebf7",
"scope":"Existing binding/technical render receipt recorded for provenance only. Fresh source reuse evidence is not a fresh placement pass; after asset repair re-review uniform first-shot scale/translation and bottom crop. No generated 1080 layer modified or bound."
},
"actual_exposure_pts":frames,
"source_video_provenance":{"path_from_source_ledger":ledger["source_video"],"sha256_declared_in_ledger_not_recomputed":ledger["source_sha256"],"existing_decoded_frames_used":True,"new_video_extract_performed":False},
"priority_metadata_read":{"PROGRESS":{"path":str(progpath),"sha256":h(progpath),"updated_utc":prog["updated_utc"],"current_policy_static_reviewed_states":prog["current_policy_static_reviewed_states"],"retained_prior_policy_static_evidence_states":prog["retained_prior_policy_static_evidence_states"],"meaning":"Recorded file snapshot only, not a claim about all project/global progress."},"PRIORITY_SCOPE":{"path":str(scopepath),"sha256":h(scopepath),"current_state_record":state}},
"metadata_evidence":[{"path":str(p),"sha256":h(p)} for p in [jpath,ledgerpath,bindings,B/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v10.json"]],
"actual_viewed_paths":v,
"actual_viewed_evidence":[{"path":p,"sha256":h(p)} for p in v],
"source_binding_diagnostic_evidence":{"path":str(D/"ACTUAL_SOURCE_AND_BINDING_EVIDENCE.json"),"sha256":h(D/"ACTUAL_SOURCE_AND_BINDING_EVIDENCE.json")},
"current_art_detail_evidence":{"path":str(D/"CURRENT_ART_DETAIL_PROVENANCE.json"),"sha256":h(D/"CURRENT_ART_DETAIL_PROVENANCE.json")},
"photography_passed":False,"actual_continuous_playback_validated":False,"dynamic_validated":False,
"hidden_geometry_certified":False,"user_accepted":False,"whole_film_reviewed":False,
"generation_calls_by_reviewer":0,"API_calls_by_reviewer":0,"recolor_apply_calls":0,"central_metadata_modified":False,"art_pixels_modified":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md="""F834..840 原片可见画型可继续使用 ART-G33-01，当前72b667画稿按新策略需返修。

已实际查看 native F834/F840 全图、全部7张原片的无缩放人物裁片、canonical F2306及guide，并做原图对原图的单一等比放大/平移对照。帽折线、闭眼/小口、红bow折边、肩frill三角与竖线、腰/双低袖及右cuff能同时吻合；7曝光仅背景wipe/歌词变化。此次0新增source drawing state，不考古原作者cel号，不证明裁外手/腿/鞋。

当前画稿P1：画右两珠约(653,260)/(653,280)仍挂在高侧脑，未在实际低bob/nape连接；卷束大部在本肩frill外悬。耳被bob遮，不虚构耳垂位置，但可见下颌/颈基与bob末缘明显更低。这个人物内部路线问题不能靠摄影整体下移解决。灰实体返回与真实透底可保；末端C可读性及较鲜绿mint列P2，不因洞数认结构通过，也不挖灰返回。

两眼实际闭合无虹膜，不强开以套B配色；人物修复后按最终稿重新分类。原动作仍只由PV控制。完整master的腿鞋不能在首段半身viewport中露出，修后摄影须另审；现有binding/技术readback不是本次艺术或摄影通过。

报告JSON包含 exact raw/source/guide/WB/全部实际看图与证据SHA、7曝光PTS及原视频路径。0生成、0Py、0中央/绑定/像素修改；未实际连续播放、未动态或用户验收。仅此1/66，不机械批量通过。
"""
O.with_suffix(".md").write_text(md,encoding="utf-8")
z=json.loads(O.read_text(encoding="utf-8"));assert z["image_sha256"]==h(z["image"])
print(json.dumps({"report":str(O),"sha256":h(O),"md":str(O.with_suffix(".md")),"md_sha256":h(O.with_suffix(".md")),"art_status":z["review_status"],"source_equivalence":z["source_equivalence"]["review_status"],"new_source_state":False},ensure_ascii=False))

