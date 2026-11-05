from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/direct_first_api_source4082_ownPose_junctionOnly_thinFirstBand_roundArc_v18"
D=B/"review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence"
O=B/"review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
v=json.loads("[\"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/X01-15/source.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/inputs/source_pose_guide.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/direct_first_api_source4082_ownPose_junctionOnly_thinFirstBand_roundArc_v18/character_api_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/direct_first_api_source4082_ownPose_junctionOnly_thinFirstBand_roundArc_v18/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/direct_first_api_source4082_ownPose_junctionOnly_thinFirstBand_roundArc_v18/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence/CURRENT_ROOT_COIL_white_4x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence/CURRENT_ROOT_COIL_black_4x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence/CURRENT_EYE_white_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence/OWN_GUIDE_EYES_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_FIRST_X01_15_OWNPOSE_THIN_FIRST_ROUND_ARC_20261104_v18_evidence/HEAD_CONTEXT_UNIFORM_EYE_SPAN_DIAGNOSTIC.png\"]"); raw=R/"character_api_original.png"
assert h(raw)=="20120450b15b24b1bca43e98bde3dbe6e808a4a1d10d2f524f52a5569679ff0c"
qpath=R/"DIRECT_REQUEST.json";q=json.loads(qpath.read_text(encoding="utf-8-sig"))
jpath=B/"drawings/ART-X01-15/v01/JOB.json";j=json.loads(jpath.read_text(encoding="utf-8-sig"))
obj={
"id":"ART-X01-15","reviewer":"Sol xhigh fresh independent actual FIRST art/source review; not request preparer/maker",
"image":str(raw),"image_sha256":h(raw),"raw_dimensions":[720,1024],
"review_status":"repair_required","repair_required":True,
"source":q["source"]["path"],"source_frame":4082,"source_pts":2179776,"source_time_base":"1/16000",
"guide":q["guide"]["path"],
"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04",
"requirements_revision":"goal_curl_assessment_20261104_v10",
"eye_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"P1":[
{"area":"钻发体量/主转卷径","raw_roi_xyxy_exclusive":[424,209,501,322],
"finding":"首两大转相对本头肩明显窄小，整束沿领边读成细条发饰；首带减薄并未同时保持正常主转卷径。首圈/第二圈主体本身可见，没有前景手臂大幅挡住，也非明显窄侧投影，不能用隐藏、深灰返回容差或原动作解释此缩水。",
"evidence":"正常全WB与初始完整三视几何、8e0 completecoil，以及相邻14当次正常头肩并看均成立。另仅整层按两眼间距统一缩放的诊断去掉两张画布大小差后，当前可见主转仍明显更小；该统一缩放仅帮助观察，不是固定比例阈值、动作模板或摄影。",
"repair_direction":"保留本F4082头身/眼开度/两托掌/衣腿和低耳后两珠唯一肩前路线，恢复首两大转本身的正常宽度与发束体量；首正面带可薄，但不要靠把整卷缩成吊饰、只拉长尾尖、加圈或挖掉opaquegray返回来补偿。"}
],
"retained_visible_findings":[
"Own F4082头/颈/躯干倾向、画左较圆眼与画右较低上睑、原小闭弧笑、画左低外托掌/画右高托掌和两裸前臂的不同屈肘类型保留；未复制14竖侧掌或整体镜像。",
"解剖LEFT仍在画右低bob/nape，两颗红珠接单一灰束，卷在本肩frill/领胸前；未见另起高后脑茎、第三珠或第二独立发束。",
"灰前面、opaque返回带和下端独立较小转接C的路径基本可读，无需按孔数挖灰；当前返面没有重复大块银白亮纹。保这些连接，不把体量P1误当应清空灰返回。",
"两MAIN帽叶贴头、灰green仅MAIN短袖短裙、黑胸bow/手套/长袜鞋、金扣和白frill/apron/腰后bow及后带基本保；左外伸腿全鞋可见，右腿原底裁边界待摄影明确。",
"完整白黑QA没有显示raw里的大块灰云；未将透明RGB展示当alpha灰雾或主体halo。未复制前景花瓣/歌词。"
],
"P2":[
{"area":"材料","finding":"局部灰面轻微软调、mint窄边存在；此项不足以消除正常体量P1，也不宣称严格同一RGB。"},
{"area":"独立小转/收尖","finding":"下小转与C在紧凑投影中相近，虽可追灰返回，修体量时须保两大后真正较小转再C；不凭空窗数量认证全隐藏拓扑或统一圈长。"},
{"area":"摄影与底裁","finding":"720×1024画布与前14尺寸不同，不能直接凭同canvas像素大小判人体。原4082左鞋完整、右鞋被1080底切；当前右鞋平截与raw空边仍需实际摄影恢复源切口，不认证画外右鞋底。原手/肩/裙部局部描线和比例余差未作为已定位或动态通过。"}
],
"eye_classification":{
"viewer_left":{"actual_classification":"normal_open_visible_iris","observation":"可见较圆正常虹膜、小白glint，当前有深黑中心；待人物修过后独立Py校准眼内RGB/浅灰弧，保护原形/眼线/高光。"},
"viewer_right":{"actual_classification":"narrowed_squint_visible_iris_exempt_under_v03_current_return","observation":"实际5x与own源对看，上睑较低切入虹膜，当前为窄眼，保其窄开度与glint，不为配色强行画圆或补睁；后续修whole后按最终逐眼重新分类，不永久豁免新像素。"}
},
"secondary_eye_local_status":"art_repair_required_before_per_eye_secondary_local_fix",
"secondary_eye_local_passed":False,
"actual_viewed_paths":v,
"actual_input_artifact_sha256":[{"path":p,"sha256":h(p),"actual_viewed_image":True} for p in v],
"metadata_evidence":[{"path":str(qpath),"sha256":h(qpath)},{"path":str(jpath),"sha256":h(jpath)},q["eye_color_policy"],q["requirements"]],
"comparison_role_boundary":"14 only adjacent mass/connection diagnosis; initial3views only geometry/mass, not polished lighting;8e0 completecoil only gray ribbon/return/small+C construction. Own4082 remains sole action/eye opening/body/costume/extent authority.",
"diagnostic_provenance":{"path":str(D/"DIAGNOSTIC_PROVENANCE.json"),"sha256":h(D/"DIAGNOSTIC_PROVENANCE.json")},
"generation_technical_success_not_art_pass":True,
"artwork_static_passed":False,"hidden_geometry_certified":False,
"photography_passed":False,"dynamic_playback_verified":False,"user_accepted":False,"production_ready":False,
"generation_calls_by_reviewer":0,"API_calls_by_reviewer":0,"recolor_apply_calls":0,"art_pixels_modified_by_reviewer":False,"central_metadata_modified":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
z=json.loads(O.read_text(encoding="utf-8"));assert z["image_sha256"]==h(z["image"])
print(json.dumps({"report":str(O),"sha256":h(O),"review_status":z["review_status"]},ensure_ascii=False))

