from pathlib import Path
import json,hashlib
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G13_29_CANONICAL1324_VS_WIDER3766_20261104_v01")
images=json.loads(r'''["D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G13-29/source.png","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F003766.png","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M25_source_comparison_v01/page_12.png","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/inputs/source_pose_guide.png","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G13_29_CANONICAL1324_VS_WIDER3766_20261104_v01/COMMON_VISIBLE_STROKES_UNIFORM_COMPARISON.png","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G13_29_CANONICAL1324_VS_WIDER3766_20261104_v01/FULL_SOURCE_UNIFORM_COMPARISON.png"]''')
docs=json.loads(r'''["D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/JOB.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/REGISTRATION_PLAN.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/FRAME_DECODE.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M25_wider_source_proposal_v01/PROPOSAL.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M25_source_comparison_v01/INDEX.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M25_SOURCE_REUSE_NOMINATIONS_v01.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/sol_xhigh_source_M10_v01.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/sol_xhigh_source_M25_v01.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G13_29_CANONICAL1324_VS_WIDER3766_20261104_v01/DIAGNOSTIC.json","D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/direct_first_api_source1324_G3343ShoulderFrontContext_postPassEye_v14/DIRECT_REQUEST.json"]''')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
diag=json.loads((D/"DIAGNOSTIC.json").read_text("utf8"))
report={
"id":"ART-G13-29","review_scope":"original-source visible-state reuse and production-reference provenance only",
"reviewer":"Sol xhigh","canonical_source_frame":1324,"canonical_image":images[0],"canonical_image_sha256":sha(images[0]),
"production_reference_frame":3766,"production_reference_image":images[1],"production_reference_image_sha256":sha(images[1]),
"source_state_reuse_confirmed":True,
"review_status":"confirmed_visible_state_photographic_reuse",
"wider_production_reference_justified":True,
"provenance":{
"original_video_sha256_recorded_in_FRAME_DECODE":"ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1",
"frame_numbering":"zero-based decoded original PV order; source timing uses original_timeline per FRAME_DECODE",
"canonical_source_matches_decoded_F001324_exact_sha":sha(B/"coverage/source_frames/F001324.png")==sha(images[0]),
"original_comparison_entry":"M25_source_comparison_v01/INDEX.json pages[11].entries[2], shown page_12.png lower-left",
"wider_proposal_record":"M25_wider_source_proposal_v01/PROPOSAL.json records[29]",
"earlier_source_reviews":"sol_xhigh_source_M10_v01 segment1316..1327; sol_xhigh_source_M25_v01 segment3766..3777; supporting provenance, conclusions freshly checked here",
"production_crop_xyxy":[79,118,1043,1080],"production_guide_size":[976,976],
"canonical_JOB_and_sampling_preserved":True,
"guide_is_coarse_source_reference_not_alpha":True
},
"fresh_visual_findings":[
{"region":"eyes, mouth, head/neck","observation":"同一统一缩放平移后，两眼开合轮廓/小白点、眉线与刘海交叉、粉色开笑口右端小折、鼻点、下颌/颈边及帽折同时吻合；未见新的表情或头倾重描。"},
{"region":"hands and cuffs","observation":"后方竖指组的指尖小缺口/弯指三角交叠、前方横掌两层指尖/掌内短线/拇指，及两袖口V折与狭短折线同步吻合，未见指形更换。"},
{"region":"costume and body strokes","observation":"领口矩形折角、红结内钩线与窄尾、金饰、画左泡袖小闭环、白肩褶、交叉黑前臂内部折线同步吻合，支持共同可见原绘制态复用。"},
{"region":"photographic difference / wider extent","observation":"F3766人物约为F1324的0.8168倍并平移；字幕独立未跟随人物缩放。F3766实际多露下方腰带/围裙上缘及更低前臂，F1324裁掉的这些范围不能由F1324本身核同笔，但它们确实来自F3766原PV像素，不是凭空补体。"}
],
"diagnostic_uniform_transform":diag["transform"],
"diagnostic_limit":"单一uniform变换仅帮助看共同笔道，不是生产注册/作者cel编号证明；下界约y964以下的3766新增可见内容不以canonical隐藏信息认证。",
"unknowns":[
"不追认原作者真实cel编号或源工程层级。",
"不证明两段逐曝光所有帧完全相同；本轮精确核F1324与F3766及materialized guide。",
"不认证F1324画外范围的隐藏原画、生成alpha覆盖、画稿质量、最终摄影或连续播放。",
"较宽腰带/围裙来自3766可用作production visible reference，最终新返图仍须逐项审动作/可见范围。"
],
"minimal_prep_recommendation":{
"current_action":"保留现有3766 production guide/REG与canonical1324证据；已具备共同可见态复用依据，无须仅因frame编号不同改成canonical-only。",
"hold":"G13-29保持0call，ROOT按优先级独立release；本审查不提交。",
"fallback_if_ROOT_requires_canonical_only":"另存canonical-only guide/REG和新PREP sibling，不覆盖现文件：用JOB crop[0,51,1143,1080]，单一等比fit到1152x1040并仅padding；own F1324控制可见截边，不补其裁外腰裙。"
},
"actual_viewed_paths":[{"path":p,"sha256":sha(p)} for p in images],
"read_evidence":[{"path":p,"sha256":sha(p)} for p in docs],
"API_calls":0,"generation_submitted":False,"central_files_modified":False,
"artwork_approved":False,"photography_verified":False,"dynamic_verified":False,"user_accepted":False
}
out=B/"review/SOL_G13_29_CANONICAL1324_WIDER3766_SOURCE_EQUIVALENCE_20261104_v01.json"
if out.exists():raise RuntimeError("report already exists; do not overwrite")
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
md=out.with_suffix(".md")
md.write_text("""F1324 与 F3766 的共同可见人物可确认是同一绘制态的摄影复用；G13-29 仍保持 0call，未改现有 guide、REG 或请求。

实际看两张原图、page_12 原源对照、当前 976×976 guide，以及新只读统一对齐图。仅用约 0.8168 倍缩放、平移 [104.5,81.9] 后，眼白点/开笑口与头颈、后手弯指缺口、前掌内短线、两袖口折线、红结钩线及泡袖小闭环同时吻合。没有只凭姿势相近确认。

合法来源为原 PV 解码 F003766；已存在 M25 wider PROPOSAL records[29]、源对源 INDEX page_12 及 M10/M25 原审记录。JOB canonical1324/原采样 SHA 保留；解码 F001324 与 canonical 同 SHA。

可见差异是摄影缩小/平移，以及 F3766 多露腰带、围裙上缘和更低的前臂。F1324 底裁在变换后约为3766坐标 y964，其下内容仅能认定为3766真实可见，不能反推1324隐藏原画。字幕为独立层。

因此现有较宽 production reference 有依据；若 ROOT 仍要 canonical-only，另存新 guide/REG/PREP，用原 JOB crop [0,51,1143,1080] 等比 fit/pad 到 1152×1040，保留当前文件即可。未执行该替代准备。

这不是作者 cel 编号证明、画稿通过、生产摄影或动态/用户验收。
""",encoding="utf8")
print(json.dumps({"json":str(out),"json_sha256":sha(out),"md":str(md),"md_sha256":sha(md),"source_hashes_verified":True},ensure_ascii=False))

