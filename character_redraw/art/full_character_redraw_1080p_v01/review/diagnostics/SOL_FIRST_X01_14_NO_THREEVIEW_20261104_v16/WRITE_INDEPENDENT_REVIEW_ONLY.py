from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,datetime
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/direct_first_api_source4078_noThreeView_flatBob_totalTurnBudget_postPassEye_v16");D=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_FIRST_X01_14_NO_THREEVIEW_20261104_v16");sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest()
raw=R/"character_api_original.png";assert sha(raw)=="5a9d538439f233c6804cd689567c3515ec5a1dc9787b886b0272f39ab96c37ee"
job=json.loads((R.parent/"JOB.json").read_text("utf8"));source=Path(job["source_image"]);guide=R.parent/"inputs/source_pose_guide.png"
assert sha(source)==job["source_image_sha256"]
paths=[source,guide,raw,R/"qa_white.png",R/"qa_black.png",D/"CURRENT_full_white.png",D/"CURRENT_full_black.png",D/"head_root_coil_white_3x.png",D/"head_root_coil_black_3x.png",D/"lower_coil_black_5x.png",D/"OWN_GUIDE_HEAD_HANDS_2x.png",Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-13/v01/direct_first_api_source4074_sourceOnly_threeViewAnatomy_postPassEye_v15/qa_white.png"),Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png")]
a=np.array(Image.open(raw));qaudit={}
for label in ["white","black"]:
 ours=np.array(Image.open(D/("CURRENT_full_"+label+".png")).convert("RGB"));theirs=np.array(Image.open(R/("qa_"+label+".png")).convert("RGB"));qaudit[label+"_composite_RGBA_origin_RGB_mismatch_pixels"]=int(np.any(ours!=theirs,axis=2).sum());assert np.array_equal(ours,theirs)
req=B/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v10.json"
eye=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json"
obj={"id":"ART-X01-14","reviewer":"Sol xhigh independent actual source/current-image visual review; did not prepare this request","reviewed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"run":str(R),"image":str(raw),"image_sha256":sha(raw),"image_dimensions":[624,1072],"source_frame":4078,"source_pts":2177648,"time_base":"1/16000","source":{"path":str(source),"sha256":sha(source)},"guide":{"path":str(guide),"sha256":sha(guide)},"review_status":"repair_required","status":"repair_required","independent_static_pass":False,"repair_required":True,"curl_structure_policy_id":"hollow_two_large_one_small_20261102_v04","requirements":{"path":str(req),"sha256":sha(req)},"eye_color_policy":{"path":str(eye),"sha256":sha(eye)},
"P1":[{"code":"two_beads_on_opposite_side_from_only_coil_no_lowLEFT_chain","raw_bead_group_bbox_xyxy":[247,244,281,264],"raw_bead_approx_centers":[[257,254],[270,250]],"raw_coil_upper_origin_bbox_xyxy":[349,205,404,245],"observation":"双珠连在画左低bob/近侧RIGHT耳下缘，唯一灰卷却由画右下颌/肩褶上端直接起。近正面本头的解剖LEFT在画右；当前珠组在相反侧，无法追出同侧bob→两珠→首灰转的连续路线。此为实际跨侧分拆/未连接，不是首圈高于珠或隐藏一部分珠的问题；灰卷本体在画右肩前，但双珠留在另一侧，不能靠眼部改色或统一摄影解决。","repair_direction":"保持本源头身、已分开两手、衣裙和底裁；把同一低解剖LEFT根→恰两珠→唯一卷连接重绘到同一侧，删除画左另一耳旁错误珠组，按自己的颈胸/白frill前后关系接上。不得把整个角色镜像或保留双根。"}],
"P2":[{"code":"soft_tone_and_internal_return_tolerance","observation":"新bob未见旧13的银白高光带，仍有轻柔灰面/衣身色阶；内返回略深不单独升P1。不是严格单RGB材质认证。"},{"code":"local_redraw_proportions_and_placement_not_measured","observation":"头肩/腰、掌指简化和局部裙摆线与source仍有重画余差；本轮未测最终1080统一配准，不把raw相同画布坐标差当新增人体P1。保持两侧不同手势和原鞋裁边，后续摄影另核。"}],
"retained_findings":[
"原右高举窄侧掌/左肩侧横展掌已经分开；没有复制12/13的双手贴合上举模板。裸前臂、不同肘腕方向与黑手套原不规则指形总体保持。",
"保持原不等正常开眼/小白glints与闭口弧笑、头的斜向及躯干倾向。两只可见眼均normal_open，色彩尚未通过v03二次Py。",
"灰绿只用于源主衣布、领部和裙；黑胸bow/手套/长袜鞋、白frill/apron/cuffs/腰/后带及金扣保留，未变成长袖前段黑红服。",
"白maidcap贴头、两片主要黑叶可见。未看到新增第三独立黑叶或头颈拼接。",
"外露卷可读到上两宽灰转、下方收细小转/灰返回和C；不是仅以孔数计圈。可见卷在自己白肩褶和黑胸结前叠压，当前没有横过胸的前臂遮挡；不再把臂下另起一套圈当合理遮挡。该结构优点不能豁免双珠错侧未连根。",
"source画左鞋被底裁，画右鞋尖近底边；当前亦保持相应下沿平裁/近边范围，没有据此证明全鞋或画外鞋底。"
],
"changed_reference_outcome":{"observation":"相对实际打开的X01-13旧polished返图，新X01-14的bob和大面积灰发不再有明显银白条带；主布/手势也正确转到本源。但新的两侧分离珠根P1仍然成立。","no_internal_causal_claim":True,"not_global_reference_adoption":True},
"alpha_display_assessment":{"raw_gray_cloud":"Raw查看器可见灰云，但正常白/黑底复合未显示对应灰云实体背景；不据A0隐藏RGB判污染。","normal_white_black_background_artifact_P1":False,"read_only_diagnostics_generated_in_review_directory_only":True,"qa_readback":qaudit,"not_claiming_all_alpha_is_255_or_edges_zeroed":True},
"eye_applicability":{"viewer_left":"normal_open","viewer_right":"normal_open","post_pass_separate_Python_required":True,"secondary_eye_local_status":"wait_root_and_curl_repair_art_pass_then_fresh_normal_open_local_two_gray","eye_color_approved":False,"original_glints_must_be_preserved":True,"no_Python_applied":True},
"actual_viewed_paths":[str(p) for p in paths],"actual_input_artifact_sha256":[{"path":str(p),"sha256":sha(p)} for p in paths],"read_evidence":[{"path":str(p),"sha256":sha(p)} for p in [R/"DIRECT_REQUEST.json",R.parent/"JOB.json",req,eye,D/"DIAGNOSTIC.json"]],
"hidden_geometry_certified":False,"full_curl_master_certified":False,"photography_approved":False,"dynamic_validated":False,"actual_playback":False,"user_accepted":False,"production_selected":False,"central_registry_changed":False,"exposure_bindings_changed":False,"art_pixels_changed":False,"API_calls":0,"imagegen_calls":0,"Python_recolor_calls":0}
out=B/"review/SOL_FIRST_X01_14_NO_THREEVIEW_20261104_v16.json"
assert not out.exists(),"Preserve existing formal report"
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
md=out.with_suffix(".md");md.write_text("""X01-14：repair_required。

P1 是珠根与卷分到头的两侧。原尺寸双珠约(257,254)/(270,250)，在画左bob/近RIGHT耳；唯一灰卷却从画右颌侧/肩frill上端[349,205,404,245]直接开始，无法形成解剖LEFT低bob→两珠→首转连续路径。卷本体的肩前位置可保，但不能用隐藏或整体镜像解释相反侧珠组。

已实际看F4078 canonical、own guide、raw、正式全白黑和只读头根/卷局部。右高窄掌与左肩侧展掌已分开，源不等开眼/闭笑、灰绿主布/黑bow手套袜鞋和白围裙/原底裁大致保持。可见宽灰转、较小末转/返回与C有改善；相比实看的13旧稿，bob不再有明显银白亮带。内灰柔差P2，不代替连接P1，也不认证隐藏总轴/动态。

raw灰云在实际全白黑不成实体污染；自行只读复合与run正式WB像素一致。两只眼均normal_open，先修人物并fresh过审后再做局部Py；当前无眼色通过。

原图SHA256：5a9d538439f233c6804cd689567c3515ec5a1dc9787b886b0272f39ab96c37ee。
未改原图、中央或曝光，0API/0imggen/0Py改色；摄影、动态、用户验收均false。
""",encoding="utf8")
print(json.dumps({"report":str(out),"sha256":sha(out),"md":str(md),"md_sha256":sha(md),"image_sha256":sha(raw),"review_status":"repair_required"},ensure_ascii=False))

