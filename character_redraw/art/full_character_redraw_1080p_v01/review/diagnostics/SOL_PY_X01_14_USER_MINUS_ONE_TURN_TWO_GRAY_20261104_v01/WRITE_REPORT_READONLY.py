import json, hashlib
from pathlib import Path
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/diagnostics/SOL_PY_X01_14_USER_MINUS_ONE_TURN_TWO_GRAY_20261104_v01"
audit=json.loads((D/"INDEPENDENT_PIXEL_AUDIT.json").read_text(encoding="utf-8-sig"))
R=B/"drawings/ART-X01-14/v01/py_post_pass_user_minus_one_turn_two_gray_v01"
stem=B/"review/SOL_PY_X01_14_USER_MINUS_ONE_TURN_TWO_GRAY_20261104_v01"
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
viewed=[R/"qa_white.png",R/"qa_black.png"]
for eye in ["viewer_left","viewer_right"]:
    viewed += [D/(eye+"_ORIGINAL_MASK_FINAL_8x.png"),D/(eye+"_ORIGINAL_1x.png"),D/(eye+"_FINAL_1x.png")]
assert h(audit["output"]["path"])=="2f374177261fa89f2ea99175d94d0480dfaed39a2b593ad77f73da85c95c553b"
assert all(audit["pixel_summary"][k]==0 for k in ["outside_mask_RGBA_changed_pixels","alpha_changed_pixels","protected_glint_RGBA_changed_pixels","expected_full_RGBA_mismatch_pixels","saved_changed_mask_mismatch_pixels"])
report={
"schema":"scoped_eye_local_independent_review_v03",
"reviewer":"Sol xhigh",
"id":"ART-X01-14",
"image":audit["output"]["path"],
"image_sha256":audit["output"]["sha256"],
"parent_image":audit["source"]["path"],
"parent_image_sha256":audit["source"]["sha256"],
"review_status":"retained_scoped_eye_candidate",
"secondary_eye_local_passed":True,
"scoped_edit_review_passed":True,
"secondary_eye_local_status":"passed_scoped_native_two_gray_internal_lower_arc_independent_audit",
"eye_color_policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",
"approved_spec":audit["approved_spec"],
"scope":"Only two visible normal-open iris interiors: native RGB recolor and lower upward-convex light-gray cap; no whole-cel re-approval.",
"actual_viewed_paths":[str(p) for p in viewed],
"actual_viewed_evidence":[{"path":str(p),"sha256":h(p)} for p in viewed],
"observations":[
"实际逐眼查看原/最终 native 1x、原/掩膜/最终 8x 以及最终完整白黑 QA。两只虹膜为深灰主体与较宽的下部上凸浅灰弧，各自倾斜和原开合、视线未改。",
"原小白高光及其 AA、真实上眼线、睫毛、眼白和外轮廓保留；未见新增中央黑瞳点或虹膜内部侧/下黑环。深灰上沿沿原眼皮自然衔接，本次没有外形修圆操作。",
"独立使用 NumPy 重建各眼许可行段、减去高光保护，再依据 spec 自身坐标轴、椭圆和 1.5 native px signed-distance AA 重算精确 RGB；未导入或调用官方 apply/validator。"
],
"issues":[],
"P1":[],
"P2":[
"本判断针对原生分辨率的眼内色块及边缘保留；AA 和真实上眼线不能当作应擦除的虹膜黑圈。没有将放大后的像素台阶判为新绘制缺陷。"
],
"palette":{"dark_RGB":[72,69,67],"light_RGB":[129,128,128],"cap_AA_native_px":1.5},
"pixel_audit":audit["pixel_summary"],
"per_eye_pixel_audit":audit["per_eye"],
"QA_composite_recheck":audit["QA_composite_recheck"],
"independent_audit_evidence":{"path":str(D/"INDEPENDENT_PIXEL_AUDIT.json"),"sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json")},
"independent_audit_script":{"path":str(D/"INDEPENDENT_AUDIT_READONLY.py"),"sha256":h(D/"INDEPENDENT_AUDIT_READONLY.py")},
"exact_parent_static_evidence_inherited":audit["parent_static_evidence"],
"inheritance_limit":"Only the exact unchanged eye-exterior RGBA retains its exact parent primary/independent static evidence. This report grants scoped eye approval, not a new full-cel artistic or production approval.",
"artwork_full_static_approved_by_this_report":False,
"hidden_geometry_certified":False,
"production_approved":False,
"photography_verified":False,
"dynamic_verified":False,
"user_accepted":False,
"API_calls":0,"imagegen_calls":0,"recolor_apply_calls":0,"central_writes":False
}
stem.with_suffix(".json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md="""X01-14 本次眼内局改可保留：retained_scoped_eye_candidate。

已实际看最终完整白黑 QA、两眼原/最终 native 1x 和原/掩膜/最终 8x。深灰主体 RGB 72/69/67、下部较宽上凸浅灰弧 RGB 129/128/128 及 1.5 native px 过渡成立；无新增中央黑瞳点或内部侧下黑环，原高光、上眼线、轮廓和视线保持。

独立 NumPy 重算：2409 个许可像素发生变化（左1162、右1247）；眼外 RGBA、全图 alpha、177个保护高光像素变化均为0。按批准 spec 重建行段、轴向椭圆与精确 AA 颜色，最终 RGBA 与独立预期差异为0；白黑 QA 独立重合成差异为0。

原图 SHA：3fb40f36fbb0dfb50b3b973e763d512fcfefb17e1347144c0d3e2d9f6077b154  
输出 SHA：2f374177261fa89f2ea99175d94d0480dfaed39a2b593ad77f73da85c95c553b

仅通过眼内限定编辑；眼外逐像素未变，其整稿静态证据仅继承 exact parent 的主评及独审。本报告未重新认证人物/卷发/隐藏几何、摄影、连续播放、交付或用户接受。0生成、0正式 apply、0中央修改。路径、掩膜/批准 spec/审计 SHA 与实际看图列表见 JSON。
"""
stem.with_suffix(".md").write_text(md,encoding="utf-8")
loaded=json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
assert loaded["scoped_edit_review_passed"] and loaded["image_sha256"]==h(loaded["image"])
print(json.dumps({"json":str(stem.with_suffix(".json")),"json_sha256":h(stem.with_suffix(".json")),"md":str(stem.with_suffix(".md")),"md_sha256":h(stem.with_suffix(".md")),"status":loaded["review_status"]},ensure_ascii=False))

