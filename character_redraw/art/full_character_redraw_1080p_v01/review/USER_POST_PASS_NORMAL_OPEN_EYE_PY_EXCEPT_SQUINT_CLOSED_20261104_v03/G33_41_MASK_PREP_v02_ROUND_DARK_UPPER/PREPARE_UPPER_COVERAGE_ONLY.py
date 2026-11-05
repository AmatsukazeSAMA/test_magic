from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, hashlib, json, copy, datetime
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
O=Path(__file__).resolve().parent
V1=O.parent/"G33_41_MASK_PREP_v01"
S=B/"drawings/ART-G33-41/v01/direct_first_api_source2480_approvedCoil_innerGray_eyeArcNoOutline_v11/character_api_original.png"
P=B/"drawings/ART-G33-41/v01/py_post_pass_native_two_gray_no_center_v01/character_eye_gray_local.png"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(S)=="636b913a402e8619cc352c0af830862a4aca5b5b1aece3a4b923158a201d4aaa"
assert sha(P)=="2f66e00906f7a4db9edbf35ca1f7308443dd788cda63e7924a2467bdbc1e7695"
a=np.array(Image.open(S).convert("RGBA")); spec=json.loads((V1/"G33_41_FULL_IRIS_SPEC.json").read_text(encoding="utf-8-sig")); oldspecsha=sha(V1/"G33_41_FULL_IRIS_SPEC.json")
# Local ellipse crowns derived against own original top/native pixels. Strict intersection with v01 iris; not a new eye silhouette.
geo={"viewer_left":{"center_xy":[382.2,149.8],"radii_xy":[8.7,11.2],"top_rows_inclusive":[139,141]},"viewer_right":{"center_xy":[444.0,158.8],"radii_xy":[10.8,12.0],"top_rows_inclusive":[147,149]}}
allallowed=np.zeros(a.shape[:2],bool); allprotected=np.zeros(a.shape[:2],bool); allchange=np.zeros(a.shape[:2],bool); newcoverage=np.full(a.shape[:2],255,np.uint8); updates=[]; ss=32
for eye in spec["eyes"]:
 name=eye["name"]; m=np.array(Image.open(eye["interior_mask"]["path"]))==255;g=np.array(Image.open(eye["protected_glint_mask"]["path"]))==255
 assert sha(eye["interior_mask"]["path"])==eye["interior_mask"]["sha256"] and sha(eye["protected_glint_mask"]["path"])==eye["protected_glint_mask"]["sha256"]
 allallowed|=m;allprotected|=g;c=np.full(m.shape,255,np.uint8);cfg=geo[name];cx,cy=cfg["center_xy"];rx,ry=cfg["radii_xy"];y0,y1=cfg["top_rows_inclusive"]
 for y,x in np.argwhere(m):
  if y0<=y<=y1:
   # Area coverage of the ellipse at native pixel cell; center samples on a 32x32 grid.
   xx=x-.5+(np.arange(ss)+.5)/ss; yy=y-.5+(np.arange(ss)+.5)/ss
   inside=((xx[None,:]-cx)/rx)**2+((yy[:,None]-cy)/ry)**2<=1
   c[y,x]=round(float(inside.mean())*255)
 changed=(c<255)&m;assert not np.any(changed&g);assert not np.any(changed&~m)
 rows={str(int(y)):[{"x":int(x),"coverage":int(c[y,x])} for x in np.where(changed[y])[0]] for y in np.where(changed.any(axis=1))[0]}
 out=O/f"{name}_UPPER_DARK_COVERAGE_SSAA32.png";Image.fromarray(c).save(out)
 allowance=O/f"{name}_TOP_WEIGHT_CHANGE_ALLOWANCE.png";Image.fromarray(changed.astype(np.uint8)*255).save(allowance)
 eye["upper_dark_coverage"]={"path":str(out),"sha256":sha(out),"bounds_xyxy":[int(np.where(changed)[1].min()),int(np.where(changed)[0].min()),int(np.where(changed)[1].max())+1,int(np.where(changed)[0].max())+1],"mask_reviewed":True,"meaning":"255=existing two-gray result; 0..254=original source RGB to dark RGB area blend, ONLY exact listed top rows/pixels; no lower-cap operation"}
 eye["upper_dark_geometry"]=cfg;eye["upper_dark_coverage_ssaa"]=ss;eye["upper_dark_changed_pixels"]=int(changed.sum());eye["upper_dark_exact_changes"]=rows
 eye["root_mask_reviewed"]=False;eye["allowed_pixels"]=int(m.sum());eye["expression_reviewed"]=True;eye["expression_classification"]="normal_open";eye["mask_reviewed"]=True;eye["mask_reviewed_by"]="Sol actual original/current/proposed native and 10x overlays; ROOT actual approval pending"
 updates.append({"name":name,"old_flat_top_row":y0,"old_top_span":([378,382] if name=="viewer_left" else [438,449]),"coverage_only_changes":rows,"changed_coverage_pixels":int(changed.sum()),"iris_allowed_pixels_unchanged":int(m.sum()),"light_cap_unchanged":True,"upper_liner_glint_sclera_alpha_protected":True})
 newcoverage[changed]=c[changed];allchange|=changed
assert int(allallowed.sum())==661 and not np.any(allchange&allprotected)
# These are mask-only diagnostics. No candidate art RGB, recolor, composite or cleanup is emitted.
def white(p):
 im=Image.open(p).convert("RGBA");w=Image.new("RGBA",im.size,"white");w.alpha_composite(im);return np.array(w.convert("RGB"))
w=white(S);old=white(P);ov=w.copy();ov[allallowed]=(255,0,255);ov[allprotected]=(0,230,255)
newov=ov.copy();weight=newcoverage.astype(float)/255
for y,x in np.argwhere(allchange):newov[y,x]=np.rint(np.array([255,0,255])*weight[y,x]+w[y,x]*(1-weight[y,x])).astype(np.uint8)
roi=(365,128,465,175);x0,y0,x1,y1=roi
panels=[w[y0:y1,x0:x1],old[y0:y1,x0:x1],newov[y0:y1,x0:x1]];pair=np.concatenate(panels,axis=1)
Image.fromarray(pair).save(O/"ORIGINAL_CURRENT_PROPOSED_MASK_native_1x.png")
Image.fromarray(pair).resize((3000,470),Image.Resampling.NEAREST).save(O/"ORIGINAL_CURRENT_PROPOSED_MASK_10x.png")
maskpair=np.concatenate([ov[y0:y1,x0:x1],newov[y0:y1,x0:x1]],axis=1)
Image.fromarray(maskpair).resize((2000,470),Image.Resampling.NEAREST).save(O/"V01_V02_MASK_OVERLAY_10x.png")
Image.fromarray(newcoverage).save(O/"ALL_UPPER_DARK_COVERAGE_SSAA32.png")
Image.fromarray(allchange.astype(np.uint8)*255).save(O/"ALL_TOP_WEIGHT_CHANGE_ALLOWANCE.png")
spec.update({"prep_status":"PREP_ONLY_upper_dark_rounding_root_actual_review_required_no_apply","input":{"path":str(S),"sha256":sha(S)},"current_selected_py_context":{"path":str(P),"sha256":sha(P),"role":"actual current result diagnosis only; original RGB remains blend authority"},"parent_spec":{"path":str(V1/"G33_41_FULL_IRIS_SPEC.json"),"sha256":oldspecsha},"root_mask_reviewed":False,"root_release_granted":False,"color_edit_applied":False,"upper_dark_coverage_must_be_honored":True,"do_not_apply_with_legacy_binary_mask_only_renderer":True,"scope":"Only native upper-dark attachment coverage weights in 3 top rows per eye; full iris permission 661 unchanged. Lower light-cap parameters and all other allowed colors remain identical to v01. Original upper-liner/lashes/glints/sclera/skin/all alpha are protected.","boundary":"Not an applied art result or pass. The original upper-liner is irregular; this conservatively softens tiny row-mask corner steps and cannot promise a new perfect round arc without altering the protected upper liner.","generation_calls":0,"art_pixels_modified":False,"central_writes":False})
specpath=O/"G33_41_UPPER_DARK_ROUNDING_SPEC_PREPONLY_v02.json";specpath.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
receipt={"id":"ART-G33-41","status":"PREP_ONLY_root_actual_view_before_apply","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"original":{"path":str(S),"sha256":sha(S)},"selected_py_context":{"path":str(P),"sha256":sha(P)},"spec":{"path":str(specpath),"sha256":sha(specpath)},"updates":updates,"total_coverage_only_changed_pixels":int(allchange.sum()),"original_iris_permission_pixels":661,"full_iris_masks_glint_masks_and_light_cap_geometry_unchanged":True,"production_rgb_written":False,"generation_calls":0,"central_writes":False,"root_reviewed":False,"limitations":["Only weights of already-authorized top iris pixels are suggested. No expansion into original upper liner, no iris resizing or transferred eye outline.","Fractional coverage uses original source RGB to dark blend; exact weighted validator must restrict this exception to listed pixels/weights. It must not exempt a center pupil or a side/bottom dark rim.","If source upper-liner geometry itself is judged too angular, achieving a perfectly round new joint would require altering protected liner; this PREP deliberately does not do that."]}
(O/"PREP_ONLY_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"updates":updates,"total_changed_coverage":int(allchange.sum()),"spec":str(specpath),"spec_sha256":sha(specpath)},ensure_ascii=False))
