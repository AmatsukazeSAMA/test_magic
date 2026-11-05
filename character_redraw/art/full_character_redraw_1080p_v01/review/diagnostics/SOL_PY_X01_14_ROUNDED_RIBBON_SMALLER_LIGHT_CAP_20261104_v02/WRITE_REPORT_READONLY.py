import json,hashlib
from pathlib import Path
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/diagnostics/SOL_PY_X01_14_ROUNDED_RIBBON_SMALLER_LIGHT_CAP_20261104_v02"
R=B/"drawings/ART-X01-14/v01/py_post_pass_user_round_ribbon_smaller_light_cap_v02"
stem=B/"review/SOL_PY_X01_14_ROUNDED_RIBBON_SMALLER_LIGHT_CAP_20261104_v02"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((D/"INDEPENDENT_PIXEL_AUDIT.json").read_text(encoding="utf-8"))
viewed=[R/"qa_white.png",R/"qa_black.png",R/"USER_EYE_SMALLER_LIGHT_CAP_BEFORE_AFTER_3x.png"]
for eye in ["viewer_left","viewer_right"]:
 viewed += [D/(eye+"_ORIGINAL_MASK_FINAL_8x.png"),D/(eye+"_ORIGINAL_1x.png"),D/(eye+"_FINAL_1x.png")]
assert a["pixel_summary"]["changed_pixels"]==2601
assert all(a["pixel_summary"][k]==0 for k in ["outside_mask_RGBA_changed_pixels","alpha_changed_pixels","protected_glint_RGBA_changed_pixels","expected_full_RGBA_mismatch_pixels","saved_changed_mask_mismatch_pixels"])
obj={
"id":"ART-X01-14","reviewer":"Sol xhigh independent scoped eye actual-view and NumPy audit; not mask preparer/apply operator",
"image":a["output"]["path"],"image_sha256":a["output"]["sha256"],
"parent_image":a["source"]["path"],"parent_image_sha256":a["source"]["sha256"],
"review_status":"retained_scoped_eye_candidate","secondary_eye_local_passed":True,"scoped_edit_review_passed":True,
"secondary_eye_local_status":"passed_scoped_smaller_light_cap_independent_pixel_and_visual_review",
"eye_color_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"scope":"Only the two current139526 normal-open iris interiors and reduced lower convex light-gray cap. No outline/upperliner or whole-art revision.",
"user_feedback_quote":"浅灰色占比太大，像白内障",
"observations":[
"实际看最终完整白黑QA、同域修改前后3x、两眼原/掩膜/最终8x及原/最终native1x；浅灰从覆盖大半虹膜收成底部较小、横向宽而上凸的弧，深灰成为主体，正常尺度读感明确改善。",
"每眼沿自身倾斜轴处理；原瞳形外轮廓、眼白、真实上眼线、睫毛、小白glint及AA保持，无新增中央黑瞳点或虹膜内部侧/下黑圈。深灰上沿保持原有与lid的接合，没有另改眼皮外形。",
"独立NumPy在完整native网格重建spec局部轴椭圆、1.5px signed-distance AA及舍入RGB，未导入或执行正式apply/validator。精确expectedRGBA与输出无差，白黑QA独立重合成无差。"
],
"P1":[],
"P2":["约22.5%为ROOT本次cap试验的许可域加权占比，并非用户指定硬比例、全片统一比例或已获用户认可。正常native画幅仍保原始AA边缘；未将8x像素台阶误称改形缺陷。"],
"issues":[],
"palette":{"dark_rgb":[72,69,67],"light_rgb":[129,128,128],"native_transition_px":1.5},
"independent_pixel_summary":a["pixel_summary"],
"per_eye":a["per_eye"],
"QA_composite_recheck":a["QA_composites"],
"approved_spec":a["approved_spec"],
"independent_audit":{"path":str(D/"INDEPENDENT_PIXEL_AUDIT.json"),"sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json")},
"independent_audit_script":{"path":str(D/"INDEPENDENT_AUDIT_READONLY.py"),"sha256":h(D/"INDEPENDENT_AUDIT_READONLY.py")},
"actual_viewed_paths":[str(p) for p in viewed],
"actual_viewed_evidence":[{"path":str(p),"sha256":h(p)} for p in viewed],
"exact_parent_static_evidence_inherited":a["parent_static_evidence"],
"inheritance_boundary":"Only current139526 parent primary72701450 and independentaca21a evidence for byte-identical eye-exterior is inherited. Old3fb40 parent /2f374 output history is not inherited. This scoped report is not a new whole-cel review or user approval.",
"artwork_full_static_approved_by_this_report":False,"production_approved":False,
"photography_verified":False,"dynamic_verified":False,"hidden_geometry_certified":False,"user_accepted":False,
"API_calls":0,"imagegen_calls":0,"recolor_apply_calls":0,"central_writes":False
}
stem.with_suffix(".json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md="""X01-14 新圆弧卷母稿139526的缩小浅灰cap局改可保留：retained_scoped_eye_candidate；secondary_eye_local_passed / scoped_edit_review_passed = true。

实际查看最终白黑全图、前后3x、逐眼原/掩膜/最终8x与native1x。浅灰已明显收低为较小的宽上凸下弧，深灰成为主体；无新中央黑点或内部侧下黑圈，原眼形、上眼线、睫毛、白高光与AA保持。

独立NumPy重算：许可域2613像素（1278+1335），实际变化2601；眼外RGBA、alpha、169个保护高光像素变化均0。根据批准spec独立重建轴向椭圆与1.5nativepx AA，expected全RGBA和白黑QA重合成差异均0。两灰RGB为72/69/67与129/128/128；每眼加权浅灰约22.5%只是ROOT此次试验值，不是用户硬比例或艺术接受。

输出SHA：fdaf20a7430d5e2255ae338c088c3becb786ac85b215185f2f2cb066c9dde7f8  
母稿SHA：139526ab4dbd67d6a8b220231794c4e8d62fc4feeec997b55c510c9fc9fbfda0

眼外RGBA逐像素不变，整稿静态仅继承新139526母稿PRIMARY72701450和独审aca21a证据，不沿用旧3fb/2f374。此报告只通过眼部限定编辑；摄影、连续播放、隐藏几何、交付和用户验收均未认证。0正式apply、0生成、0中央修改。精确路径/证据SHA见JSON。
"""
stem.with_suffix(".md").write_text(md,encoding="utf-8")
r=json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
assert r["image_sha256"]==h(r["image"])
print(json.dumps({"json":str(stem.with_suffix(".json")),"json_sha256":h(stem.with_suffix(".json")),"md":str(stem.with_suffix(".md")),"md_sha256":h(stem.with_suffix(".md")),"review_status":r["review_status"]},ensure_ascii=False))

