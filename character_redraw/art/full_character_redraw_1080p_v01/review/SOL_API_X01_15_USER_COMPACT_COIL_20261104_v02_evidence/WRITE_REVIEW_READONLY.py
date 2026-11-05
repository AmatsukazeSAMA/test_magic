from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/api_user_parallel_redraw_latest_coil_tls12_v02"
D=B/"review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence"
O=B/"review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_api_original.png"
assert h(raw)=="897eef064e9ba25ad4d409771acc29fd3ee45c1d9c17a0da353ff2aed2aa2e37"
v=json.loads("[\"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/X01-15/source.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/inputs/source_pose_guide.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/api_user_parallel_redraw_latest_coil_tls12_v02/character_api_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/api_user_parallel_redraw_latest_coil_tls12_v02/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/api_user_parallel_redraw_latest_coil_tls12_v02/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence/ROOT_COIL_white_4x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence/ROOT_COIL_black_4x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence/LOWER_PATH_white_6x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence/LOWER_PATH_black_6x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence/CURRENT_EYES_WHITE_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_API_X01_15_USER_COMPACT_COIL_20261104_v02_evidence/SAME_NATIVE_SCALE_COMPACT_COIL_COMPARISON_2x.png\"]")
rp=R/"API_REDRAW_REQUEST.json";r=json.loads(rp.read_text(encoding="utf-8-sig"))
jp=B/"drawings/ART-X01-15/v01/JOB.json";j=json.loads(jp.read_text(encoding="utf-8-sig"))
up=Path(r["user_feedback"]["path"]);u=json.loads(up.read_text(encoding="utf-8-sig"))
assert h(up)==r["user_feedback"]["sha256"] and h(r["eye_policy"]["path"])==r["eye_policy"]["sha256"]
obj={
"id":"ART-X01-15","reviewer":"Sol xhigh fresh independent actual API redraw art/source review; not maker",
"image":str(raw),"image_sha256":h(raw),"raw_dimensions":[1056,1504],
"review_status":"repair_required","repair_required":True,
"source":j["source_image"],"source_frame":4082,"source_pts":2179776,"time_base":"1/16000",
"guide":str(B/"drawings/ART-X01-15/v01/inputs/source_pose_guide.png"),
"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04",
"requirements_revision":"goal_curl_assessment_20261104_v10",
"eye_policy_id":"post_pass_normal_open_eye_dance_B_override_20261104_v04",
"user_rejected_predecessor":{"statement":u["statement"],"image":u["rejected_image"],"feedback_record":{"path":str(up),"sha256":h(up)},"predecessor_pass_inherited":False},
"P1":[
{"area":"第二大转→独立真Small→C连续结构","raw_roi_xyxy_exclusive":[644,396,728,486],
"finding":"新两大转下方仍看不到独立小转的灰正面与自身opaque返回。第二大转的末端宽灰带直接弯成一个C，中心只是该钩内缘/小mint尖与后方白frill；C内部开口不是另一个Small。",
"visible_evidence":"4x全卷、6x下段白黑双底均实际看。末段在肩frill前，没有前景手/袖遮挡可以解释独立Small缺失；白色空处两底基本不换，读作后方衣料，不据孔数判圈。对照被否fa114时，小转额外的独立灰front/返回可明确分开，本次紧缩时该段消失。",
"repair_direction":"保当前压小后的主径和长度、低两珠同束肩前、原表演服装，只在下段给真Small独立较小灰front与实体返回再收C。压缩局部pitch来容纳它，勿恢复fa114膨大垂到腰的体量、只加洞或多添一大圈。"}
],
"retained_visible_findings":[
"fa114与897eef全白QA及同原像素尺度2x并排实际看，头颈/珠和肩参考基本一致而新卷整体更窄、垂落更短；旧尾触腰线，新尾在胸前白肩带/黑bow旁结束，已响应过蓬松过大问题。无硬性缩放百分比或旧艺术通过继承。",
"低画右bob/nape→解剖LEFT两红珠→唯一灰mint束→本肩/领胸前深度仍连贯；未见第二发根、第三珠、镜像或肩外悬吊。主灰正面和实体灰返回尚可保。",
"own4082原片/guide对应斜头、小闭弧笑、画左较圆与画右较窄开眼、两只高低黑glove平托掌/前臂、灰green主体短maid衣/黑bow金扣/白frillapron后带、帽两叶、左外伸腿全鞋与右近直腿；未明显套相邻不同姿势。",
"真实整白黑QA未见raw大灰云形成实体背景灰雾，也未画入原花瓣/歌词；技术API返回不代美术通过。"
],
"P2":[
{"area":"材质/卷面","finding":"首两大转保持宽灰面与薄荷边；灰返回及窄边少量软色/规整线，不称纯同RGB，无新增明显银白亮带。内部灰容差并不能补足缺少Small的几何。"},
{"area":"摄影与源鞋裁","finding":"原4082左鞋完整、右鞋在1080底切。当前raw右鞋平截与画布边仍需正式摄影恢复原viewport，不认可画外鞋底、注册或连续播放。"}
],
"eye_classification":{
"viewer_left":{"actual_classification":"normal_open_visible_iris","observation":"实际较圆开眼/小glint，人物修过后按当前B低饱和另局部Py；保护原眼形、眼线、glint/AA和alpha。"},
"viewer_right":{"actual_classification":"narrowed_squint_visible_iris_current_return","observation":"实际较低上睑剪裁，保源较窄开度，不为配色强睁；当前窄眼可豁免，修后按新exactraw再分类。"}
},
"secondary_eye_local_status":"art_repair_required_before_per_eye_B_low_saturation_local_fix",
"secondary_eye_local_passed":False,
"actual_viewed_paths":v,
"actual_input_artifact_sha256":[{"path":p,"sha256":h(p),"actual_viewed_image":True} for p in v],
"metadata_evidence":[{"path":str(rp),"sha256":h(rp)},{"path":str(jp),"sha256":h(jp)},r["eye_policy"]],
"diagnostic_provenance":{"path":str(D/"DIAGNOSTIC_PROVENANCE.json"),"sha256":h(D/"DIAGNOSTIC_PROVENANCE.json")},
"reference_roles":"Own4082 source owns action/eyes/body/costume/extent; rejectedfa114 for size/path comparison only;8e0 complete band topology only. No fixed hole count, root size ratio, hidden geometry, animation or final adoption inferred.",
"artwork_static_passed":False,"hidden_geometry_certified":False,"photography_passed":False,
"dynamic_playback_verified":False,"user_accepted":False,"production_ready":False,
"generation_calls_by_reviewer":0,"API_calls_by_reviewer":0,"recolor_apply_calls":0,"art_pixels_modified_by_reviewer":False,"central_metadata_modified":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
z=json.loads(O.read_text(encoding="utf-8"));assert h(z["image"])==z["image_sha256"]
print(json.dumps({"report":str(O),"sha256":h(O),"status":z["review_status"]},ensure_ascii=False))

