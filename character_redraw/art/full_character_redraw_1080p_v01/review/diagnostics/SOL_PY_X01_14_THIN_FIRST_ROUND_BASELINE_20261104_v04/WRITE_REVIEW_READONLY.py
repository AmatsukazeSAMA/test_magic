from pathlib import Path
import json,hashlib
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04"
O=B/"review/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04.json"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((D/"INDEPENDENT_PIXEL_AUDIT.json").read_text(encoding="utf-8"))
viewed=json.loads("[\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_thin_first_round_baseline_eyes_v04/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_thin_first_round_baseline_eyes_v04/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_EYE_GRAY_PATCH_SHAPE_PY_20261104_v02/EYE_COLORS_AND_LIGHT_CAP_REFERENCE.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04/viewer_left_ORIGINAL_MASK_FINAL_8x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04/viewer_right_ORIGINAL_MASK_FINAL_8x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04/viewer_left_FINAL_1x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04/viewer_right_FINAL_1x.png\"]")
spec=json.loads(Path(a["approved_spec"]["path"]).read_text(encoding="utf-8-sig"))
assert a["pixel_summary"]["changed_pixels"]==2686 and a["pixel_summary"]["allowed_pixels"]==2687
assert all(a["pixel_summary"][k]==0 for k in ["outside_mask_RGBA_changed_pixels","alpha_changed_pixels","protected_glint_RGBA_changed_pixels","expected_full_RGBA_mismatch_pixels","saved_changed_mask_mismatch_pixels"])
assert a["output"]["sha256"]=="ca8c7fe058a6578b3562975387651052f73c87dc086f393d56f3f2663be5d5a7"
obj={
"id":"ART-X01-14","reviewer":"Sol xhigh fresh independent scoped eye actual-view/NumPy audit; not mask preparer or apply operator",
"image":a["output"]["path"],"image_sha256":a["output"]["sha256"],
"parent_image":a["source"]["path"],"parent_image_sha256":a["source"]["sha256"],
"review_status":"retained_scoped_eye_candidate","secondary_eye_local_passed":True,"scoped_edit_review_passed":True,
"secondary_eye_local_status":"passed_current_818103_native_two_gray_round_baseline_arc_independent_review",
"eye_color_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"scope":"Only exact818103 current two normal-open iris-interior RGB and lower upward-convex round-cap boundary; no outer geometry, upperliner or whole-character revision.",
"eye_classification":{"viewer_left":"normal_open_visible_iris_actual_viewed","viewer_right":"normal_open_visible_iris_actual_viewed"},
"observations":[
"实际看最终完整白黑QA、认可cdf0内部cap基线crop、两眼原-mask-final8x和最终native1x。两灰分区为深灰主体加饱满的底部上凸浅灰圆弧，保当前不同倾斜开度；未回到过小扁条或把基线眼外形搬过来。",
"原小白glints及AA、眼白/外虹膜轮廓、真实上眼线和睫毛保持；未见新增中央黑瞳点或内部侧/下黑圈。上接触处保守保留原有AA/liner，当前正常尺寸无明显新矩形角或眼皮改形。",
"新818103眼内许可mask逐眼重新核验为满画布binaryL和当前SHA，左1307/右1380，保护glint左72/右81；本次计算和视觉核验未用旧139526/4e32掩膜或眼部通过。",
"独立NumPy重建当前spec各眼自身轴、内部椭圆、1.5nativepx signed-distance AA与精确舍入RGB；expected fullRGBA与输出差0，白黑QA独立重合成差0。未导入、执行正式Recolor或其validator。",
"当前818103眼外字节完全一致，因此首圈变薄/灰返回/原人物的整稿证据只沿exact818103主评a119和独审6d1aa9继承；本局改报告不重复授权整稿，也不沿旧139526艺术或4e32眼色结论。"
],
"P1":[],
"P2":["虹膜原生像素小，8x可见原始边缘与AA步进；没有把真实上眼线或外轮廓AA当成应擦除的iris黑环。新圆弧权重约34.78%/32.67%仅是当前许可域和轴向椭圆的测量，不是用户固定比例。"],
"issues":[],
"palette":{"dark_rgb":[72,69,67],"light_rgb":[129,128,128],"native_transition_px":1.5},
"independent_pixel_summary":a["pixel_summary"],"per_eye":a["per_eye"],
"approved_spec":a["approved_spec"],
"baseline_crop":spec["baseline_crop"],
"baseline_geometry_role":"Only internal round-cap curvature and color. No reference eye-outline/gaze/glint or global percentage is transferred.",
"QA_composite_recheck":a["QA_composites"],
"independent_audit":{"path":str(D/"INDEPENDENT_PIXEL_AUDIT.json"),"sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json")},
"independent_audit_script":{"path":str(D/"INDEPENDENT_AUDIT_READONLY.py"),"sha256":h(D/"INDEPENDENT_AUDIT_READONLY.py")},
"actual_viewed_paths":viewed,"actual_viewed_evidence":[{"path":p,"sha256":h(p)} for p in viewed],
"exact_parent_static_evidence_inherited":a["parent_static_evidence"],
"inherited_whole_limitations":"Current818103 parent soft inner-gray/material P2, diagnostic-only normalization and original4078 bottom-shoe viewport limitation remain. No hidden shoe/whole curl/photography/dynamic certification added by eye edit.",
"previous_eye_mask_or_pass_inherited":False,
"artwork_full_static_approved_by_this_report":False,"production_approved":False,
"photography_verified":False,"dynamic_verified":False,"hidden_geometry_certified":False,"user_accepted":False,
"API_calls":0,"imagegen_calls":0,"recolor_apply_calls":0,"central_writes":False
}
assert not O.exists()
O.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
r=json.loads(O.read_text(encoding="utf-8"));assert r["image_sha256"]==h(r["image"])
print(json.dumps({"report":str(O),"sha256":h(O),"review_status":r["review_status"],"audit_sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json")},ensure_ascii=False))

