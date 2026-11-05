from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02"
D=B/"review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence"
O=B/"review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_imggen_original.png"
assert h(raw)=="fa114462dad743a35cc4a36a1d3ab980076fd7d199041914beb38fdb98736f9c"
v=json.loads("[\"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/X01-15/source.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/inputs/source_pose_guide.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02/character_imggen_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence/CURRENT_ROOT_COMPLETE_COIL_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence/CURRENT_ROOT_COMPLETE_COIL_black_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence/CURRENT_LOWER_PATH_white_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence/CURRENT_LOWER_PATH_black_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence/CURRENT_EYES_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence/CURRENT_UNIFORM_WIDTH720_DIAGNOSTIC.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png\"]")
jp=B/"drawings/ART-X01-15/v01/JOB.json";j=json.loads(jp.read_text(encoding="utf-8-sig"))
rp=R/"REQUEST.json";rq=json.loads(rp.read_text(encoding="utf-8-sig"))
obj={
"id":"ART-X01-15","reviewer":"Sol xhigh fresh independent actual whole/source review; not maker",
"image":str(raw),"image_sha256":h(raw),"raw_dimensions":[1052,1495],
"review_status":"retained_static_candidate","repair_required":False,
"source":j["source_image"],"source_frame":4082,"source_pts":2179776,"time_base":"1/16000",
"guide":str(B/"drawings/ART-X01-15/v01/inputs/source_pose_guide.png"),
"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04",
"requirements_revision":"goal_curl_assessment_20261104_v10",
"eye_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"P1":[],
"visible_static_findings":[
"与旧f55整白QA实际比较，新图第二Large之后增加了可追踪的独立小灰front/opaque返回，然后再C，不再由第二大转直接变成整只C钩。小转不是把一处空气孔或C内部的后景当作计数。",
"新3x根/全卷双底与5x下段看：约raw[666,518,722,550]为较小正面，左/上后缘有实体灰返回，接至约[682,548,725,576]渐小C；几段属于同一束，不在袖/衣物遮挡后重新开始另一组圈。不是无灰return的细S。",
"首两大转直径/灰main体量保持此前恢复结果，首带仍为较薄的弧面，没有缩回FIRST小条饰品，也没为添加Small再增加第三Large。正常全图和只读720宽整层等比诊断同时看，不以输出像素尺寸或固定比值定义正常mass。",
"解剖LEFT在画右低bob/nape，两颗红珠→唯一灰卷→本肩/领胸前的重叠路径保持；未见高后脑另根、第三珠或第二条coil。",
"Own4082的斜头/颈、画左较圆开眼与画右低上睑窄眼、闭弧小笑、两只各异平托黑glove/两裸前臂/屈肘、灰green主布短maid制服/黑bow金扣/两帽叶/白frillapron后带，以及左外伸腿全鞋与右近直腿基本保留。未照14的竖侧手或改变原腿型。",
"白黑底下后frill/白竖带可透过部分coil间隙，属于原衣物后景；下端极小透底不能认证隐藏全轴。完整WB无新增字幕/花瓣、明显实体彩边或头颈拼接；raw外圈彩色RGB不作为alpha污染判断。"
],
"visible_path_regions_raw_xyxy_exclusive":{
"low_bob_beads_root":[622,279,681,323],
"two_maintained_large_front_return_turns":[602,304,759,526],
"independent_small_front_return":[664,514,727,553],
"following_C_taper":[679,547,727,577],
"scope_note":"Overlapping visible-path regions, not a hole-count algorithm or hidden topology proof."
},
"P2":[
{"area":"总pitch/投影长度","raw_roi_xyxy_exclusive":[602,302,760,578],"finding":"整束仍较松、尾近腰带，较最初参考常态显长；本稿确有自身肩姿/投影差，当前列P2并保留相邻一致性检查，未以固定根尾比、请求倍数或单张静态通过声称动态匹配。不能将此图推广为所有镜头的固定长度/方向master。"},
{"area":"材质/描线","finding":"灰返回有轻微内灰差/软面，mint少量柔色和下段规整线仍在；此内返差不单独升P1，不宣称严格单RGB。整体宽gray前返/薄mint与bob材料仍可成立，无明显新增银白高光。"},
{"area":"摄影与原底裁","finding":"Own4082左鞋完整、右鞋触原1080底切；当前raw右鞋底平截/空边必须实际摄影恢复源viewport，不认证画外右鞋底。720宽全层等比图只是只读体态诊断，不是生产注册或部件warp。"}
],
"eye_classification":{
"viewer_left":{"actual_classification":"normal_open_visible_iris","observation":"保原glint/开度/视线，当前虹膜颜色仍需人物pass之后用新exactraw单独B低饱和Py校准，不因本整稿双色或技术返图豁免。"},
"viewer_right":{"actual_classification":"narrowed_squint_visible_iris_current_return","observation":"实际上睑低切入虹膜、比另一眼窄，保原source窄开度；按v03此返回当前可豁免，不能为配色强开或改圆。执行阶段仍按最终exactraw逐眼确认。"}
},
"secondary_eye_local_status":"pending_post_pass_B_low_saturation_eye_local_fix_for_normal_open_eye",
"secondary_eye_local_passed":False,
"eye_mask_provenance_boundary":"Currentfa114 iris pixels are new; neither818103 masks nor earlierX01-14/15 local eye pass can authorize edits on this output.",
"actual_viewed_paths":v,
"actual_input_artifact_sha256":[{"path":p,"sha256":h(p),"actual_viewed_image":True} for p in v],
"metadata_evidence":[{"path":str(rp),"sha256":h(rp)},{"path":str(jp),"sha256":h(jp)}],
"reference_roles":"Own4082 is sole body/head/eyes/hands/costume/extent authority. Oldf55 is failed geometry comparison only; approved8e0 is complete gray-band/return/twoLarge/trueSmall/C construction, no fixed hole number, copied posture or lighting.",
"diagnostic_provenance":{"path":str(D/"DIAGNOSTIC_PROVENANCE.json"),"sha256":h(D/"DIAGNOSTIC_PROVENANCE.json")},
"previous_failure_or_pass_inherited":False,
"hidden_geometry_certified":False,"photography_passed":False,"dynamic_playback_verified":False,"user_accepted":False,"production_ready":False,
"generation_calls_by_reviewer":0,"API_calls_by_reviewer":0,"recolor_apply_calls":0,
"art_pixels_modified_by_reviewer":False,"central_metadata_modified":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md="""X01-15 当前fa114整稿可保留为静态候选。

实际看 own4082原片/guide、新raw/完整白黑、旧f55白底、认可8e0及新3x整卷/5x下段双底。第二大转后现在可追到独立较小灰front和实体grayreturn，再收成C；旧版由第二Large直接成C的P1已改善。判断依据是同一灰带路径，不是tip空气孔或固定洞数。正常两大卷径、薄首带与低LEFT两珠肩前同束保留，未多加一Large或缩回饰品。

自身不等眼开度/闭弧笑、两只不同托掌/前臂、灰green黑白短制服、帽双叶、左外伸腿全鞋与右腿源裁类型保留。P2仍含整体pitch/尾近腰偏松长、轻微软gray/mint及正式右鞋底viewport；此静态通过不认证隐藏卷master、摄影或动态。

左眼实际normal-open，待人物pass后以当前exactraw新mask单独B低饱和Py。右眼实际低上睑窄眼，不强睁/改圆；按最终稿逐眼确认，旧818眼mask不可复用。本稿不代表眼色、用户整图、摄影或动态通过。

Raw SHA：fa114462dad743a35cc4a36a1d3ab980076fd7d199041914beb38fdb98736f9c。完整实际看图路径、源/guide/raw/WB SHA及可见小转ROI见JSON。0生成、0Py、0中央/像素修改。
"""
O.with_suffix(".md").write_text(md,encoding="utf-8")
z=json.loads(O.read_text(encoding="utf-8"));assert z["image_sha256"]==h(z["image"])
print(json.dumps({"report":str(O),"sha256":h(O),"md_sha256":h(O.with_suffix(".md")),"status":z["review_status"]},ensure_ascii=False))

