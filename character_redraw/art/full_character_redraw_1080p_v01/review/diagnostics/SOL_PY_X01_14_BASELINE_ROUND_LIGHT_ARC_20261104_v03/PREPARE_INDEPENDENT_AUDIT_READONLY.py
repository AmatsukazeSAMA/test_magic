from pathlib import Path
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
old=B/"review/diagnostics/SOL_PY_X01_14_ROUNDED_RIBBON_SMALLER_LIGHT_CAP_20261104_v02/INDEPENDENT_AUDIT_READONLY.py"
D=B/"review/diagnostics/SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03"
D.mkdir(parents=True,exist_ok=True)
s=old.read_text(encoding="utf-8")
s=s.replace("py_post_pass_user_round_ribbon_smaller_light_cap_v02","py_post_pass_user_baseline_round_light_arc_v03")
s=s.replace("SOL_PY_X01_14_ROUNDED_RIBBON_SMALLER_LIGHT_CAP_20261104_v02","SOL_PY_X01_14_BASELINE_ROUND_LIGHT_ARC_20261104_v03")
s=s.replace("37ef8d2d63e3380c20b16854b59eeadcd758c78d89015941494455d9da567f81","4dce2ab7c83945afececf90f4c13b4993dd4e939e124c45495d350a7ff5ec918")
s=s.replace("fdaf20a7430d5e2255ae338c088c3becb786ac85b215185f2f2cb066c9dde7f8","4e32cd0574f18b5c5d8738df29ec8dfcb8b6444e76400ddeedd483a208429ad1")
s=s.replace("Light fraction is a recomputed ROOT trial measurement, not a user-specified mandatory ratio.","This is antialiased weight over current permission mask, not the baseline threshold-classified region fraction or a user-fixed target.")
insert=r'''
# Independently compare revisions: same source and same mask bytes, only internal cap changes.
prior=B/"drawings/ART-X01-14/v01/py_post_pass_user_round_ribbon_smaller_light_cap_v02/character_eye_gray_local.png"
pp=np.array(Image.open(prior).convert("RGBA")); revision=np.any(pp!=o,axis=2)
prevspec=json.loads(Path(spec["previous_spec"]["path"]).read_text(encoding="utf-8-sig"))
assert h(spec["previous_spec"]["path"])==spec["previous_spec"]["sha256"]
for curr,prev in zip(spec["eyes"],prevspec["eyes"]):
 assert curr["interior_mask"]==prev["interior_mask"] and curr["protected_glint_mask"]==prev["protected_glint_mask"]
revcheck={"prior_image":str(prior),"prior_image_sha256":h(prior),"changed_pixels":int(revision.sum()),"outside_same_permission_RGBA_changed_pixels":int(np.count_nonzero(revision&~union)),"alpha_changed_pixels":int(np.count_nonzero(pp[...,3]!=o[...,3])),"protected_glint_RGBA_changed_pixels":int(np.count_nonzero(revision&guards)),"mask_and_glint_SHA_identical_to_previous_revision":True,"previous_arc_approval_inherited":False}
baseline_record_path=B/"review/USER_X01_14_LIGHT_ARC_BASELINE_CHECK_20261104_v01/BASELINE_COMPARISON_AND_USER_FEEDBACK.json"
baseline_record=json.loads(baseline_record_path.read_text(encoding="utf-8-sig"))
for rec in [baseline_record["baseline_master"],baseline_record["baseline_crop"]]:
 assert h(rec["path"])==rec["sha256"]
audit_baseline={"record":{"path":str(baseline_record_path),"sha256":h(baseline_record_path)},"master":baseline_record["baseline_master"],"crop":baseline_record["baseline_crop"],"source_threshold_estimated_light_fractions":[x["threshold_estimated_light_fraction"] for x in baseline_record["baseline_measurements"]],"measurement_scope":"Baseline threshold figures are documented ROOT observations, not independently reconstructed masks. Current fractions were independently recomputed from actual target spec and pixel audit. Threshold classification vs AA weighted coverage and different iris masks are different estimators; neither is a fixed user ratio."}
'''
s=s.replace('(D/"INDEPENDENT_PIXEL_AUDIT.json").write_text',insert+'\naud["revision_comparison"]=revcheck\naud["baseline_comparison"]=audit_baseline\n(D/"INDEPENDENT_PIXEL_AUDIT.json").write_text')
s=s.replace('"QA":qa}', '"QA":qa,"revision_comparison":revcheck}')
(D/"INDEPENDENT_AUDIT_READONLY.py").write_text(s,encoding="utf-8")

