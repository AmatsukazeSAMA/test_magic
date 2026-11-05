import json,hashlib
from pathlib import Path
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/diagnostics/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03"
stem=B/"review/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((D/"INDEPENDENT_PIXEL_AUDIT.json").read_text(encoding="utf-8"))
viewed=json.loads("[\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G26-04/v01/whole_imggen_eye_graypalette_no_center_pupil_v01/character_imggen_original.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_EYE_GRAY_PATCH_SHAPE_PY_20261104_v02/EYE_COLORS_AND_LIGHT_CAP_REFERENCE.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_user_baseline_round_light_arc_v03/qa_white.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_user_baseline_round_light_arc_v03/qa_black.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_user_baseline_round_light_arc_v03/USER_BASELINE_ROUND_ARC_COMPARISON.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03/viewer_left_ORIGINAL_MASK_FINAL_8x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03/viewer_right_ORIGINAL_MASK_FINAL_8x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03/viewer_left_FINAL_1x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03/viewer_right_FINAL_1x.png\",\"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_user_baseline_round_light_arc_v03/USER_BASELINE_ROUND_ARC_COMPARISON_v02.png\"]")
assert a["pixel_summary"]["changed_pixels"]==2596
assert all(a["pixel_summary"][k]==0 for k in ["outside_mask_RGBA_changed_pixels","alpha_changed_pixels","protected_glint_RGBA_changed_pixels","expected_full_RGBA_mismatch_pixels","saved_changed_mask_mismatch_pixels"])
obj={
"id":"ART-X01-14","reviewer":"Sol xhigh independent scoped eye actual-view and NumPy audit; not mask preparer/apply operator",
"image":a["output"]["path"],"image_sha256":a["output"]["sha256"],
"parent_image":a["source"]["path"],"parent_image_sha256":a["source"]["sha256"],
"review_status":"retained_scoped_eye_candidate","secondary_eye_local_passed":True,"scoped_edit_review_passed":True,
"secondary_eye_local_status":"passed_current_baseline_round_light_arc_independent_review",
"eye_color_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"user_feedback_quote":"检查基线，应该浅灰弧度没有那么小吧",
"scope":"Only current139526 two iris-interior RGB and internal lower light-gray boundary; exact native outline/glint/lid/lashes/sclera/all alpha/exterior immutable.",
"observations":[
"实际看认可master全图、内部cap基线crop、当前完整白黑QA、原/裁边v02基线对比图、两眼原-mask-final8x及最终native1x。新浅灰从上一版低平窄弧恢复成饱满上凸圆顶；其归一化高度/曲率读感更接近认可master，深灰仍为主体。",
"两眼分别沿自身原倾斜轴适配；原虹膜外轮廓、白glint及AA、真实上眼线/睫毛/眼白与开度视线保留，没有新增中央黑瞳点或虹膜内部侧下黑圈。未用master替换当前眼形或高光。",
"独立NumPy从当前批准spec和原139526像素重新计算native局部轴椭圆、1.5px signed-distance AA、精确round RGB及全图许可域差分；未调用正式Recolor脚本或其validator，未继承v02弧形通过。",
"v02→v03只433个内部像素不同，同一permission/glint文件SHA完全相同；对应变化不扩张眼形、不触碰alpha或高光。",
"最终1280×720 USER_BASELINE_ROUND_ARC_COMPARISON_v02为展示裁空白版本，已实际查看；展示图裁边不作为生产图底裁/摄影证据。"
],
"P1":[],
"P2":["小native虹膜有不可避免AA与像素步进；未将8x像素台阶当新外形缺陷。该保留意见仅限当前局改，不声称用户已接受或全片应固定相同浅灰面积。"],
"issues":[],
"baseline_reference":a["baseline_comparison"],
"area_measurements":{
"independently_recomputed_current_AA_weighted_fraction":{"viewer_left":a["per_eye"][0]["weighted_light_fraction"],"viewer_right":a["per_eye"][1]["weighted_light_fraction"]},
"baseline_documented_threshold_fraction":{"viewer_left":0.3477977869385984,"viewer_right":0.33543117943790535},
"interpretation":"当前约34.99%/32.93%为锁定许可域上的AA权重均值；基线约34.78%/33.54%是较大原图灰填充的阈值分类面积。两者分辨率、许可域和估计器不同，仅佐证接近，不能称精确面积相等或用户规定百分比。基线拟合点/阈值比例来自ROOT记录，审者独立实际看其master/crop；当前RGBA与加权数值由审者独立重算。"
},
"palette":{"dark_rgb":[72,69,67],"light_rgb":[129,128,128],"native_transition_px":1.5},
"independent_pixel_summary":a["pixel_summary"],"per_eye":a["per_eye"],
"revision_comparison":a["revision_comparison"],"QA_composite_recheck":a["QA_composites"],
"approved_spec":a["approved_spec"],
"independent_audit":{"path":str(D/"INDEPENDENT_PIXEL_AUDIT.json"),"sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json")},
"independent_audit_script":{"path":str(D/"INDEPENDENT_AUDIT_READONLY.py"),"sha256":h(D/"INDEPENDENT_AUDIT_READONLY.py")},
"actual_viewed_paths":viewed,
"actual_viewed_evidence":[{"path":p,"sha256":h(p)} for p in viewed],
"exact_parent_static_evidence_inherited":a["parent_static_evidence"],
"inheritance_boundary":"Only current139526 exact parent PRIMARY72701450 and independentaca21a static evidence for byte-identical eye-exterior is inherited. No old3fb/2f374 art pass or v02 arc approval inherited. Current whole/user acceptance not re-certified.",
"previous_smaller_cap_status":"Historical22.5% ROOT trial is not current approved-baseline geometry and is not inherited by this review; old report retained unmodified.",
"artwork_full_static_approved_by_this_report":False,"production_approved":False,"photography_verified":False,
"dynamic_verified":False,"hidden_geometry_certified":False,"user_accepted":False,
"API_calls":0,"imagegen_calls":0,"recolor_apply_calls":0,"central_writes":False
}
assert not stem.with_suffix(".json").exists()
stem.with_suffix(".json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
r=json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
assert r["image_sha256"]==h(r["image"])=="4e32cd0574f18b5c5d8738df29ec8dfcb8b6444e76400ddeedd483a208429ad1"
print(json.dumps({"json":str(stem.with_suffix(".json")),"json_sha256":h(stem.with_suffix(".json")),"review_status":r["review_status"],"audit_sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json")},ensure_ascii=False))

