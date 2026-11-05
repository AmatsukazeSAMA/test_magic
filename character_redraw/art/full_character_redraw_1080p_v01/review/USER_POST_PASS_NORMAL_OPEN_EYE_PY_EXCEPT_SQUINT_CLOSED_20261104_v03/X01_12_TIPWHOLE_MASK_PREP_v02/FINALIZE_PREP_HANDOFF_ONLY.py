from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-12/v01/whole_imggen_user_delete_remaining_lower_turn_only_tip_v03");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_12_TIPWHOLE_MASK_PREP_v02");sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest()
sp=P/"X01_12_TIPWHOLE_FULL_IRIS_SPEC_PREPONLY_v02.json";spec=json.loads(sp.read_text("utf8"));raw=Path(spec["input"]["path"])
pri=R/"PRIMARY_GOAL_REVIEW.json";ind=B/"review/SOL_X01_12_USER_LOWER_TURN_REMOVED_TIP_v03.json"
pr=json.loads(pri.read_text("utf8"));ir=json.loads(ind.read_text("utf8"))
assert pr["image_sha256"]==sha(raw)==ir["image_sha256"]==spec["input"]["sha256"]
assert pr["primary_static_pass"] and ir["review_status"]=="retained_static_candidate"
assert sha(ind)=="4f61662f55fd96b5226d6ce4ad0fabb73312e025905a7ccabf688f5bb108c0ce"
spec["whole_art_review_status"]="current_exact_whole_static_pass_evidence_present_waiting_ROOT_eye_mask_approval"
spec["whole_art_pass_evidence"]=[{"path":str(z),"sha256":sha(z)} for z in [pri,ind]]
sp.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
rc=P/"PREP_ONLY_RECEIPT.json";rec=json.loads(rc.read_text("utf8"));rec["spec"]["sha256"]=sha(sp);rc.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
a=np.array(Image.open(raw));out=np.array(Image.open(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png"));allow=np.zeros(a.shape[:2],bool);glint=allow.copy();maskinfo=[]
for e in spec["eyes"]:
 masks=[]
 for key in ["interior_mask","protected_glint_mask"]:
  z=Path(e[key]["path"]);im=Image.open(z);m=np.array(im);assert im.mode=="L" and im.size==(956,1645) and set(np.unique(m)).issubset({0,255}) and sha(z)==e[key]["sha256"];masks.append(m==255)
 m,g=masks;assert not np.any(m&g) and not np.any(m&allow);allow|=m;glint|=g
 maskinfo.append({"eye":e["name"],"allowed_pixels":int(m.sum()),"bbox_xyxy":e["iris_bbox_xyxy"],"protected_glint_pixels":int(g.sum()),"mask_sha256":e["interior_mask"]["sha256"],"glint_mask_sha256":e["protected_glint_mask"]["sha256"]})
changed=np.any(a!=out,axis=2);assert not np.any(changed&~allow) and np.array_equal(a[...,3],out[...,3]) and np.array_equal(a[glint],out[glint]);assert not np.any((out[allow,:3]==0).all(axis=1))
actual=[R/"qa_white.png",R/"qa_black.png"]
for n in ["viewer_left","viewer_right"]:
 actual += [P/(n+"_ORIGINAL_12x.png"),P/(n+"_PIXEL_COORDS.png"),P/(n+"_ORIGINAL_MASK_PREVIEW_1x.png"),P/(n+"_ORIGINAL_MASK_PREVIEW_8x.png")]
actual += [P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_WHITE.png"]
obj={"id":"ART-X01-12","status":"PREP_ONLY_PENDING_ROOT_MASK_APPROVAL_DO_NOT_APPLY","input":spec["input"],"spec":{"path":str(sp),"sha256":sha(sp)},"eyes":maskinfo,
"allowed_pixels_total":int(allow.sum()),"protected_glint_pixels_total":int(glint.sum()),
"diagnostic_preview":{"path":str(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png"),"sha256":sha(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png"),"production_selectable":False},
"geometry":"Each own down axis, broad lower upward-convex ellipse cap; left local center[0,17.2] radii[14.4,15.6], right[0,16] radii[13,14.5]; native1.5px transition. No extra upper-coverage/outside eye-shape operation.",
"actual_observation":"Both eyes normal-open. Current gray body/remaining inner upper black pupil-cap and side/bottom iris RGB included in manually clipped native interior; true upper liner/lashes/sclera and native glint+AA excluded. Eye shapes and glints are not taken from another image. Fresh new full-canvas masks; old masks never resized/copied.",
"preview_pixel_audit":{"changed_pixels":int(changed.sum()),"outside_mask_RGBA_changes":int((changed&~allow).sum()),"alpha_changes":int((a[...,3]!=out[...,3]).sum()),"protected_glint_RGBA_changes":int(np.any(a[glint]!=out[glint],axis=1).sum()),"new_black_center_pixels":0},
"whole_art_pass_evidence":spec["whole_art_pass_evidence"],"actual_viewed_paths":[{"path":str(z),"sha256":sha(z)} for z in actual],
"mask_reviewed":False,"root_release_granted":False,"color_edit_applied":False,"final_recolor_script_executed":False,
"API_calls":0,"imagegen_calls":0,"central_writes":False,"photography_verified":False,"dynamic_verified":False,"user_accepted":False}
hp=P/"PREP_ONLY_HANDOFF.json";hp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(P/"README.md").write_text("""仅PREP；正式 Recolor-EyeGrayLocal.py 未执行，所有 mask_reviewed/root_release 均 false。

绑定新 whole b8932982…bc07f（956×1645）。只两只 normal_open；满画布 binary L 蒙版逐新眼原生像素重做，旧 spec 仅参考 wide cap，未复制/缩放旧 mask。原上眼线/外轮廓、睫毛/眼白、高光及AA、全部alpha和眼外RGBA锁定；源虹膜内部残黑允许改色，未加眼型/上沿外形修圆操作。

请ROOT先实看 viewer_left/right_ORIGINAL_MASK_PREVIEW_8x.png（原图／青色许可+洋红保护／仅诊断预览），再批准另存ROOT spec。最终新输出仍需fresh scoped独审；诊断预览不得选稿。
""",encoding="utf8")
print(json.dumps({"handoff":str(hp),"handoff_sha256":sha(hp),"spec":str(sp),"spec_sha256":sha(sp),"masks":maskinfo,"changed_pixels":int(changed.sum()),"audit_outside_alpha_glint_changes":[0,0,0],"ROOT_approval_pending":True},ensure_ascii=False))

