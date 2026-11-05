from pathlib import Path
import json,hashlib,datetime
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/whole_imggen_lower_root_own_shoulder_front_v01");V=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01");O=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16");D=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_WHOLE_G33_48_LOW_ROOT_SHOULDER_FRONT_20261104_v01")
sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest();ev=lambda z:{"path":str(Path(z)),"sha256":sha(z)}
raw=R/"character_imggen_original.png";assert sha(raw)=="556550bc741a8d09d013bc12a2d63b93c465ca7a510b5ae8c0d69ea31ae92679"
job=json.loads((V/"JOB.json").read_text("utf8"));source=Path(job["source_image"]);guide=V/"inputs/source_pose_guide.png"
assert sha(source)==job["source_image_sha256"]
paths=[source,guide,raw,R/"qa_white.png",R/"qa_black.png",O/"character_api_original.png",O/"qa_white.png",O/"qa_black.png",D/"root_shoulder_occlusion_white_3x.png",D/"root_shoulder_occlusion_black_3x.png",D/"eyes_actual_closed_white_5x.png",D/"SOURCE_FIRST_CURRENT_UNIFORM_READONLY.png"]
req=B/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v10.json";ep=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json"
obj={"id":"ART-G33-48","reviewer":"Sol xhigh fresh independent current whole review; did not produce this whole return","reviewed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"run":str(R),"image":str(raw),"image_sha256":sha(raw),"image_dimensions":[957,1644],"source_frame":2513,"source_pts":1341616,"time_base":"1/16000","source":ev(source),"guide":ev(guide),"review_status":"retained_static_candidate","status":"retained_static_candidate","independent_static_pass":True,"repair_required":False,"P1":[],"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04","requirements":ev(req),"eye_color_policy":ev(ep),
"retained_static_findings":[
{"region":"lowLEFT root and two beads","raw_roi_xyxy":[566,354,648,410],"observation":"本近正面俯头的解剖LEFT在画右。两颗红珠约(599,379)/(626,380)已落在该侧bob末缘/下颌后的低nape，灰发边进入珠组，珠组下接唯一灰卷；不像FIRST把珠组抬在帽后上方/卷悬在肩外。可见根与首转为同一侧连续路径，未见另一独立卷根或多珠。"},
{"region":"own shoulder/front layering","raw_roi_xyxy":[443,389,648,606],"observation":"上两大灰转已靠本颈胸身体一侧并覆盖白肩frill/黑胸衣的前面；白frill位于卷后。原横掌及白cuff在卷前方遮住中下连接。下方在该同一cuff内侧重现小段灰前/返回和C，未在遮挡后新增一串大卷；不是把返回灰面挖空凑孔。"},
{"region":"twoLarge plus trueSmall then C visible budget","observation":"可见两宽大前转和连续不透明灰返回，小末转部分被横掌/袖口遮住，末段在袖内侧以较小灰转/C重现。当前可见投影与同一整束总2L+trueSmall+C相容，没有从臂下重新计数加圈。隐藏完整末转/空气轴和3D路径不能由这张单图认证，也不把任意深黑衣面误记为空洞。"},
{"region":"own expression and hands","observation":"源F2513双闭睫、小闭笑和俯斜头保持；画左竖食指/其它折指收在胸前，另一手横搭红结前、长指朝画左下与拇指外分，两手不合并。两不同白cuff/弯腕/黑袖叠压仍属本态，未改成47的头旁高掌或开眼点口。"},
{"region":"body costume extent","observation":"黑立领/长黑袖裙、红胸结金扣、白肩frill/长围裙腰和画右后结/尾带保持。两腿靠拢交错及两只完整黑鞋/实际可见踝带和小跟都在，不按ending绿色服替换。统一缩到624x1072复看后没有发现新的非一致小腿长/鞋侧移P1；摄影尚未注册。"},
{"region":"head cap material and actual alpha","observation":"帽贴头、两主要黑叶、头颈衣领接合成立。bob及卷未新增明显银白亮带；内返略深/轻柔色阶不单独退修。原raw边缘彩色点在正常全白黑与该局部放大未成明显彩色实体碎屑/halo，不因隐藏RGB直接判alpha污染，也不宣称像素已清零。"}
],
"P2":[{"code":"occluded_small_turn_unobservable","observation":"小末转有被掌/cuff遮挡部分；只保当前可见相容性，不认证隐藏整圈、固定长度/孔数或通用curl master。"},{"code":"redraw_local_shapes_and_registration_pending","observation":"头肩/腰裙/掌指线条仍为重绘，和source有小形体/线条差；whole统一缩放仅只读诊断，非已批准生产变换。实际1080曝光定位和连播仍待。"},{"code":"soft_gray_surface_and_ink_variation","observation":"卷灰前/返回有轻软面差，衣裙较整齐，未作为严格单RGB平涂或原线逐笔复刻认证；无明显新增银白高光P1。"}],
"eye_applicability":{"viewer_left":"closed_no_visible_iris","viewer_right":"closed_no_visible_iris","actual_native_enlarged_eye_roi_xyxy":[422,263,630,329],"observation":"源和新whole两眼均为闭合黑睫/眼线，没有可见虹膜或glint；5x实际查看，无须也不得新增虹膜做配色。","normal_open_eyes_present":False,"visible_iris_count":0,"secondary_eye_local_not_applicable":True,"Py_color_edit_applied":False},
"secondary_eye_local_status":"not_applicable_closed_no_visible_iris_actual_viewed","no_visible_iris":True,"eye_color_edit_pass_claimed":False,
"current_vs_FIRST":"FIRST的高耳上珠与外悬卷为失败历史，未继承通过；本新whole低根与本肩前重叠已实际改动且重新独审。",
"diagnostic_scope":{"path":str(D/"DIAGNOSTIC.json"),"sha256":sha(D/"DIAGNOSTIC.json"),"uniform_source_scale":624/957,"translation":[0,0],"no_localwarp":True,"production_placement_approved":False},
"actual_viewed_paths":[str(p) for p in paths],"actual_input_artifact_sha256":[ev(p) for p in paths],"read_evidence":[ev(p) for p in [V/"JOB.json",R/"REQUEST.json",req,ep]],
"hidden_geometry_certified":False,"full_curl_master_certified":False,"photography_approved":False,"dynamic_validated":False,"actual_playback":False,"user_accepted":False,"production_selected":False,"central_registry_changed":False,"exposure_bindings_changed":False,"art_pixels_changed":False,"API_calls":0,"imagegen_calls":0,"Python_recolor_calls":0}
out=B/"review/SOL_WHOLE_G33_48_LOW_ROOT_SHOULDER_FRONT_20261104_v01.json";assert not out.exists(),"Preserve existing report"
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
md=out.with_suffix(".md");md.write_text("""G33-48 新whole：retained_static_candidate。

已实际看F2513 canonical/guide、新raw/全白黑、原FIRST及只读统一624×1072对照。画右低bob/nape下的两珠已接同一束唯一灰卷；两大转压到自己的白frill和颈胸前。原横掌/白cuff在前遮中下段，袖内侧仅重现较小转/C，没有遮挡后另起一套大圈。隐藏小转的完整几何不认证。

原俯斜头、双closed睫/小闭笑、两不同胸前手及腕袖、黑长袖红结白裙/后带和两完整鞋保留；没有因闭眼而跳过人体。正常白黑未见可见彩色实体杂片或新增银白亮带。轻柔灰面、局部重画/衣线和隐藏拓扑为P2，非生产摄影/动态通过。

secondary_eye_local_status = not_applicable_closed_no_visible_iris_actual_viewed。两眼5×实际无iris，不执行Py、不增虹膜。

原图SHA256：556550bc741a8d09d013bc12a2d63b93c465ca7a510b5ae8c0d69ea31ae92679。
0生成/Py/中央/曝光/艺术像素修改；用户验收、摄影、动态均false。
""",encoding="utf8")
print(json.dumps({"report":str(out),"sha256":sha(out),"md_sha256":sha(md),"review_status":obj["review_status"],"secondary_eye_local_status":obj["secondary_eye_local_status"]},ensure_ascii=False))

