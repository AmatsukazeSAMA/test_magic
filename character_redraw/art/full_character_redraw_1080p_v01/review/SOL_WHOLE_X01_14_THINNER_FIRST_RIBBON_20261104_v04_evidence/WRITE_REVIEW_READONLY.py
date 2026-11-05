from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04"
D=B/"review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence"
O=B/"review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
viewed=json.loads("[\"D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/X01-14/source.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/inputs/source_pose_guide.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04/character_imggen_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/whole_imggen_user_thinner_first_ribbon_keep_diameter_v04/FIRST_RIBBON_THICKNESS_BEFORE_AFTER.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence/COIL_ROOT_FIRST_RETURN_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence/COIL_ROOT_FIRST_RETURN_black_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence/EYES_white_3x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence/CURRENT_UNIFORM_WIDTH624_DIAGNOSTIC.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/SOL_WHOLE_X01_14_THINNER_FIRST_RIBBON_20261104_v04_evidence/SOURCE4078_NATIVE_BOTTOM_CROP.png\"]")
raw=R/"character_imggen_original.png"
assert h(raw)=="8181037962aaa0624155fc5ac1af924536be55f5b4b35311f4cf78d748de29ae"
jobpath=B/"drawings/ART-X01-14/v01/JOB.json";j=json.loads(jobpath.read_text(encoding="utf-8-sig"))
diag=json.loads((D/"DIAGNOSTIC_PROVENANCE.json").read_text(encoding="utf-8"))
reqpath=R/"REQUEST.json";req=json.loads(reqpath.read_text(encoding="utf-8-sig"))
obj={
"id":"ART-X01-14",
"reviewer":"Sol xhigh fresh independent actual whole-art review; not maker",
"image":str(raw),"image_sha256":h(raw),"raw_dimensions":[956,1645],
"review_status":"retained_static_candidate",
"source":j["source_image"],"source_frame":j["source_frame"],"source_pts":j["source_pts"],"time_base":"1/16000",
"guide":str(B/"drawings/ART-X01-14/v01/inputs/source_pose_guide.png"),
"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04",
"requirements_revision":"goal_curl_assessment_20261104_v10",
"eye_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"fresh_whole_review":True,"previous_parent_or_eye_pass_inherited":False,
"user_feedback_quote":"第一卷太厚了",
"P1":[],
"visible_static_findings":[
"与同一构图的before/after实际对比，首大圈正面从厚实大片缩为较薄的鼓弧带；外侧卷径和头肩相对体量基本保持，未把整卷缩成小吊坠。首弧上下缘有自然曲率，没有回到方筒直截口。",
"沿低bob/颈后→恰好两颗红珠→首圈→不透明灰返回→下一大圈追踪，仍可读两大转后独立较小灰正面/灰返回，再收C。新首圈上窗是同一转内侧显露，不读作另加完整一圈或三大圈；首圈宽灰返回仍在，没有为露孔削成细S。",
"首圈开口在白黑底均为白色肩frill/衣面，样本(599,398)RGBA239,238,237,253；这是衣物遮挡后景，不冒称真正alpha空气窗或完整隐藏轴认证。内部灰返回和深墨边仍属实体发带。",
"固定解剖LEFT落在画右低耳后bob末缘，两珠低接同一束；灰卷覆盖在该侧肩frill内侧与胸前黑bow之前，未另起高后脑茎或搬到肩外。",
"实际与自身F4078 canonical/guide和等比624宽诊断看：斜头、不等正常睁眼、闭弧笑、画右高举窄glove/画左肩侧展开glove及两侧不同屈肘、躯干腰裙和腿向保留，未镜像或复制别帧手势。",
"两MAIN帽叶、灰绿MAIN布/黑胸bow金扣/黑glove长袜鞋、白frill/apron后带保持。完整WB未见新增字幕/花瓣/脱离主体的高不透明彩片或明显头颈拼接；raw外缘RGB彩点不能当正常合成实体halo。"
],
"P2":[
{"area":"材料","coordinates_raw_xyxy":[553,350,677,546],"observation":"首圈内返靠右有局部略深gray facet（如643,385 RGBA123,119,120,253），其余gray主面略软，mint边也有轻微柔差；当前属于内返/局部软调，无新增银白亮条，未凭该局部灰差单独升P1，不宣称严格单RGB平涂。"},
{"area":"原生裁切/摄影","observation":"F4078两鞋触1080下边，当前back shoe末端比源更闭合；新画外鞋尖/鞋底没有源依据。静态保留不认证其新增画外部分，正式摄影须恢复原source底裁，不能直接将整raw全部鞋底当真实可见范围。"},
{"area":"轮廓/比例","observation":"头帽/手套/裙幅及踝部有重画余差；624宽等比图仅供体态检查，不是生产定位或非一致warp。局部几何、前后帧动势及接触仍须摄影/连续性审核。"}
],
"curl_trace_regions_raw":{
"root_two_beads_xyxy":[569,320,622,356],
"first_thinner_front_and_retained_return_xyxy":[548,348,665,462],
"second_major_turn_xyxy":[596,434,682,503],
"independent_small_then_C_xyxy":[621,488,684,548],
"note":"These regions overlap along one continuous band; no hole-count-based turn counting or hidden-axis reconstruction."
},
"eye_classification":{"viewer_left":"normal_open_visible_iris","viewer_right":"normal_open_visible_iris"},
"eye_observation":"实际3x可见两眼原小白glint/自身开度和视线，内部浅灰仍为饱满圆弧读感，未见新独立中心黑瞳。但这是全新whole返图，不是此前4e32精确像素；当前颜色/AA必须另用本raw新掩膜或审核许可域做Py，旧mask和旧scoped pass不可直接继承。",
"secondary_eye_local_status":"pending_visible_eye_audit_and_secondary_local_fix",
"secondary_eye_local_passed":False,
"actual_viewed_paths":viewed,
"actual_input_artifact_sha256":[{"path":p,"sha256":h(p),"actual_viewed_image":True} for p in viewed],
"request_evidence":[{"path":str(reqpath),"sha256":h(reqpath)},{"path":str(jobpath),"sha256":h(jobpath)}],
"edit_target":{"path":req["references"][0]["path"],"sha256":req["references"][0]["sha256"],"role":"Whole edit target kept latest baseline-round eye context; prior scoped pass not inherited by new pixels."},
"structure_reference":{"path":req["references"][1]["path"],"sha256":req["references"][1]["sha256"],"role":"Complete band/return/small-turn/C structure only; not source action, fixed position or full-picture acceptance."},
"diagnostic_provenance":{"path":str(D/"DIAGNOSTIC_PROVENANCE.json"),"sha256":h(D/"DIAGNOSTIC_PROVENANCE.json")},
"hidden_geometry_certified":False,"photography_passed":False,"dynamic_playback_verified":False,
"user_whole_art_accepted":False,"user_accepted":False,"production_ready":False,
"generation_calls_by_reviewer":0,"API_calls_by_reviewer":0,"recolor_apply_calls":0,
"art_pixels_modified_by_reviewer":False,"central_metadata_modified":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
z=json.loads(O.read_text(encoding="utf-8"));assert z["image_sha256"]==h(z["image"])
print(json.dumps({"report":str(O),"sha256":h(O),"review_status":z["review_status"],"secondary_eye_local_status":z["secondary_eye_local_status"]},ensure_ascii=False))

