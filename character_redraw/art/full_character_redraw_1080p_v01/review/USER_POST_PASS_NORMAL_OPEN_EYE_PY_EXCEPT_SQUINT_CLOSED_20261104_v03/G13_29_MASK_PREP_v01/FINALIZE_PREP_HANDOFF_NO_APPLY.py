from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/direct_first_api_canonical1324_wider3766_fourRefs_noShoulderCrop_postPassEye_v16");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G13_29_MASK_PREP_v01");sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest()
sp=P/"G13_29_FULL_IRIS_SPEC_PREPONLY_v01.json";spec=json.loads(sp.read_text("utf8"));src=Path(spec["input"]["path"])
assert sha(src)==spec["input"]["sha256"]=="af86db358694df0cc43dcea5a0f9ab9c99ec387040f54227cf8d37814586c927"
a=np.array(Image.open(src));preview=P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png";out=np.array(Image.open(preview));allow=np.zeros(a.shape[:2],bool);protect=allow.copy();items=[]
for e in spec["eyes"]:
 masks=[]
 for key in ["interior_mask","protected_glint_mask"]:
  pth=Path(e[key]["path"]);im=Image.open(pth);arr=np.array(im);assert im.mode=="L" and im.size==(976,976) and set(np.unique(arr)).issubset({0,255});assert sha(pth)==e[key]["sha256"];masks.append(arr==255)
 m,g=masks;assert not np.any(m&g) and not np.any(m&allow);allow|=m;protect|=g
 items.append({"eye":e["name"],"allowed_pixels":int(m.sum()),"iris_bbox_xyxy":e["iris_bbox_xyxy"],"protected_glint_pixels":int(g.sum()),"mask":e["interior_mask"],"glint":e["protected_glint_mask"],"center_xy":e["center_xy"],"down_unit_xy":e["down_unit_xy"],"light_cap":e["light_cap"]})
changed=np.any(a!=out,axis=2)
assert not np.any(changed&~allow) and np.array_equal(a[...,3],out[...,3]) and np.array_equal(a[protect],out[protect])
assert np.all(out[allow,:3]>=np.array([72,69,67]))
actual=[R/"character_api_original.png",R/"qa_white.png",R/"qa_black.png"]
for n in ["viewer_left","viewer_right"]:actual+=[P/(n+"_ORIGINAL_8x.png"),P/(n+"_upper_PIXEL_GRID.png"),P/(n+"_ORIGINAL_MASK_PREVIEW_8x.png")]
actual+=[P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_WHITE.png"]
obj={"id":"ART-G13-29","status":"PREP_ONLY_PENDING_ROOT_MASK_AND_WIDE_CAP_APPROVAL_DO_NOT_APPLY","input":spec["input"],"spec":{"path":str(sp),"sha256":sha(sp)},"eyes":items,"allowed_pixels_total":int(allow.sum()),"protected_glint_pixels_total":int(protect.sum()),"diagnostic_only_preview":{"path":str(preview),"sha256":sha(preview),"production_selectable":False},"preview_pixel_audit":{"changed_pixels":int(changed.sum()),"outside_mask_RGBA_changes":int((changed&~allow).sum()),"alpha_changes":int((a[...,3]!=out[...,3]).sum()),"protected_glint_RGBA_changes":int(np.any(a[protect]!=out[protect],axis=1).sum()),"zero_black_center_pixels_in_authorized_interior":True},"actual_observation":"Each normal-open current iris freshly traced. Own unequal aperture/gaze and true upper liner/sclera/lashes/outer AA stay intact. Both original small glints and surrounding native AA remain protected. Source upper boundary grids inspected; no copied opposite-eye mask, no extra upper outline or shape-rounding operation.","whole_art_pass_evidence":spec["whole_art_pass_evidence"],"actual_viewed_paths":[{"path":str(z),"sha256":sha(z)} for z in actual],"mask_reviewed":False,"root_release_granted":False,"color_edit_applied":False,"final_Recolor_EyeGrayLocal_executed":False,"secondary_eye_local_passed":False,"API_calls":0,"imagegen_calls":0,"central_writes":False,"photography_verified":False,"dynamic_verified":False,"user_accepted":False}
hp=P/"PREP_ONLY_HANDOFF.json";hp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
(P/"README.md").write_text("""仅PREP，未执行 Recolor-EyeGrayLocal.py。所有 mask_reviewed/root_release 均 false。

绑定 ART-G13-29 当前FIRST af86db35…86c927（976×976），静态候选证据已读。两normal眼各自原生二值L许可/高光AA保护蒙版，自己的倾斜down轴与宽上凸下浅灰cap，1.5px内弧过渡。只改虹膜内RGB；原眼型/视线/白glint/睫毛/眼白/所有alpha与眼外像素不动，不把眼内颜色PREP当整稿或眼色通过。

ROOT请实际看 viewer_left/right_ORIGINAL_MASK_PREVIEW_8x.png（原图／青许可+洋红高光保护／诊断预览）及各upper_PIXEL_GRID。批准须另存ROOT spec；最终输出仍需fresh scoped独审。诊断preview绝不可直接选为生产稿。
""",encoding="utf8")
print(json.dumps({"spec":str(sp),"spec_sha256":sha(sp),"handoff":str(hp),"handoff_sha256":sha(hp),"allowed_pixels":int(allow.sum()),"protected_glint_pixels":int(protect.sum()),"pixel_check":obj["preview_pixel_audit"]},ensure_ascii=False))

