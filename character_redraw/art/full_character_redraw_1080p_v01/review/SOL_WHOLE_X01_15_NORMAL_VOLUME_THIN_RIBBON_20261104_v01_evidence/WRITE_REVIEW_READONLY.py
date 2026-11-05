from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-15/v01/whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01"
D=B/"review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence"
O=B/"review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=R/"character_imggen_original.png"
assert h(raw)=="f55ac32a894b384697e37f677f3580219b6282d91fcbb42abfceb49a78fc0392"
viewed=json.loads("[\"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/X01-15/source.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/inputs/source_pose_guide.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01/character_imggen_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-15/v01/direct_first_api_source4082_ownPose_junctionOnly_thinFirstBand_roundArc_v18/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_thin_first_round_baseline_eyes_v04/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/CURRENT_ROOT_COMPLETE_COIL_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/CURRENT_ROOT_COMPLETE_COIL_black_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/CURRENT_LOWER_PATH_white_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/CURRENT_LOWER_PATH_black_5x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/CURRENT_EYES_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/CURRENT_UNIFORM_WIDTH720_DIAGNOSTIC.png\"]")
jpath=B/"drawings/ART-X01-15/v01/JOB.json";j=json.loads(jpath.read_text(encoding="utf-8-sig"))
req=R/"REQUEST.json"
obj={
"id":"ART-X01-15","reviewer":"Sol xhigh fresh independent actual whole-art/source review; not maker",
"image":str(raw),"image_sha256":h(raw),"raw_dimensions":[1052,1495],
"review_status":"repair_required","repair_required":True,
"source":j["source_image"],"source_frame":4082,"source_pts":2179776,"time_base":"1/16000",
"guide":str(B/"drawings/ART-X01-15/v01/inputs/source_pose_guide.png"),
"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04",
"requirements_revision":"goal_curl_assessment_20261104_v10",
"eye_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"P1":[
{"area":"真Small→C结构缺失","raw_roi_xyxy_exclusive":[625,483,744,574],
"finding":"当前两个主转的灰前/返回带加宽后，第二大转下沿直接缩成底部C钩；未见独立较小转自身灰正面→opaque灰返回→再收C的链条。下段5x双底看，窄带一路连续绕入同一个钩，并没有钩之前额外的小正返回折。",
"visibility_boundary":"该段位于本领胸/白frill前且无遮挡手腕；不能把缺失的独立Small假称藏在肩/臂后。C内部部分后景随底色变化，只证明局部透底，不证明真Small存在，未按窗口数量计圈。",
"repair_direction":"保留已恢复的主转卷径、薄首带、低两珠与本肩前单束路线，在第二大转后补足真正较小的灰正面和实体返回，再自然收细为C；同时控制下段pitch，不靠拉长大C或增加额外大圈。"}
],
"retained_visible_findings":[
"新稿已消除FIRST细条吊饰式体量：主转宽度和灰返回明显恢复，相对自身头肩可读正常大束。旧FIRST20120450的缩水P1不直接沿用到本图。",
"首正面带仍是较薄的圆弧宽发带，未回到厚方筒；gray正/返回实体连续，mint材质边保留，无须为更多透孔挖灰。新较大的间隙能看到后方frill/胸bow/竖白带，属于本衣物深度，不能一律称alpha空窗。",
"固定解剖LEFT落在画右低bob/nape，恰好两珠先接唯一灰束再过本肩前；未见高后脑另一根或第二条coil。",
"Fresh own4082/guide、旧FIRST与全层等比720宽诊断对看：自己的斜头/颈、画左较圆眼与画右低上睑窄眼、小闭弧笑、两只不同平托glove/裸前臂屈肘和灰green短袖短裙/黑bow金扣/白frillapron后bow基本保持，未套14的竖侧掌。",
"源画左外伸腿与完整左鞋、画右近直腿和源底裁关系大体保留；原花瓣/字幕未画入人物层。正常完整白黑QA未见raw外缘彩RGB显成实体大halo，未把隐藏RGB当alpha污染。"
],
"P2":[
{"area":"纵向pitch/整体投影","raw_roi_xyxy_exclusive":[599,291,758,574],"finding":"新主圈较松、两大转纵距偏开，尾到腰带附近，较相邻14正常束显长；当前列P2投影/体量关注，不以输出分辨率、固定根尾比或请求1.5x作否决。修Small时需避免再加长总束，不能把此关注转成复制14方向/动作。"},
{"area":"材料","finding":"内返面仍有轻微gray深浅/软调和少量规整细线，无新增明显银白打光；容许的内返灰差不豁免真Small几何P1，也不表示严格纯色认证。"},
{"area":"摄影/原鞋裁","finding":"只读1052→720全层等比图排除canvas大小差，非摄影注册。原F4082仅左鞋完整、右鞋被1080底切，当前返图右底平截及画布空边必须按正式viewport另定位；不认证原画外完整右鞋底。"}
],
"eye_classification":{
"viewer_left":{"actual_classification":"normal_open_visible_iris","next_step":"Art repair first; after a new final art pass separately recolor the exact final native iris interior by Py, protecting original outline/glint/AA/liner."},
"viewer_right":{"actual_classification":"narrowed_squint_visible_iris_current_return","next_step":"Current low upperlid aperture retained and exempt under v03; do not force round/open. Fresh classify again after next whole."}
},
"secondary_eye_local_status":"art_repair_required_before_per_eye_secondary_local_fix",
"secondary_eye_local_passed":False,
"actual_viewed_paths":viewed,
"actual_input_artifact_sha256":[{"path":p,"sha256":h(p),"actual_viewed_image":True} for p in viewed],
"metadata_evidence":[{"path":str(req),"sha256":h(req)},{"path":str(jpath),"sha256":h(jpath)}],
"diagnostic_provenance":{"path":str(D/"DIAGNOSTIC_PROVENANCE.json"),"sha256":h(D/"DIAGNOSTIC_PROVENANCE.json")},
"reference_roles":"Own4082 alone controls pose/expression/hands/costume/extent. Previous14 is adjacent normal-mass diagnostic, not action/camera. Approved8e0 is complete band/return/trueSmall/C construction, not fixed hole count/axis/ratio.",
"old_art_or_eye_pass_inherited":False,"artwork_static_passed":False,
"hidden_geometry_certified":False,"photography_passed":False,"dynamic_playback_verified":False,"user_accepted":False,"production_ready":False,
"generation_calls_by_reviewer":0,"API_calls_by_reviewer":0,"recolor_apply_calls":0,"art_pixels_modified_by_reviewer":False,"central_metadata_modified":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
z=json.loads(O.read_text(encoding="utf-8"));assert z["image_sha256"]==h(z["image"])
print(json.dumps({"report":str(O),"sha256":h(O),"review_status":z["review_status"]},ensure_ascii=False))

