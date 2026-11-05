from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/py_post_pass_user_minus_one_turn_two_gray_v01");D=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_PY_X01_14_USER_MINUS_ONE_TURN_TWO_GRAY_20261104_v01");D.mkdir(parents=True,exist_ok=True)
sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest();ev=lambda z:{"path":str(Path(z)),"sha256":sha(z)}
vr=json.loads((R/"VERIFICATION.json").read_text("utf8"));sp=Path(vr["spec"]["path"]);spec=json.loads(sp.read_text("utf8"));src=Path(spec["input"]["path"]);dest=R/"character_eye_gray_local.png"
assert sha(src)==spec["input"]["sha256"]=="3fb40f36fbb0dfb50b3b973e763d512fcfefb17e1347144c0d3e2d9f6077b154"
assert sha(dest)=="2f374177261fa89f2ea99175d94d0480dfaed39a2b593ad77f73da85c95c553b"
assert sha(sp)==vr["spec"]["sha256"] and spec["root_release_granted"] and spec["root_mask_reviewed"]
before=np.array(Image.open(src));after=np.array(Image.open(dest));assert before.shape==after.shape and before.shape==(1644,957,4)
H,W=before.shape[:2];Y,X=np.indices((H,W));expected=before.copy();allowed=np.zeros((H,W),bool);glints=allowed.copy();details=[]
original_white=Image.new("RGBA",(W,H),"white");original_white.alpha_composite(Image.fromarray(before));original_white=original_white.convert("RGB")
final_white=Image.new("RGBA",(W,H),"white");final_white.alpha_composite(Image.fromarray(after));final_white=final_white.convert("RGB")
for e in spec["eyes"]:
 assert e["expression_classification"]=="normal_open" and e["mask_reviewed"] and not e.get("upper_dark_coverage_added",False)
 masks=[]
 for key in ["interior_mask","protected_glint_mask"]:
  item=e[key];ip=Path(item["path"]);mim=Image.open(ip);vals=np.array(mim)
  assert sha(ip)==item["sha256"] and mim.mode=="L" and mim.size==(W,H) and set(np.unique(vals)).issubset({0,255})
  masks.append(vals==255)
 m,g=masks;assert not np.any(m&g) and not np.any(m&allowed);allowed|=m;glints|=g
 declared=np.zeros((H,W),bool)
 for yy,lo,hi in e["manual_native_row_spans_xy_inclusive"]:declared[yy,lo:hi+1]=True
 declared[g]=False;declared_diff=int(np.logical_xor(declared,m).sum())
 assert declared_diff==0,"Spec declared native row spans differ from actual mask"
 cx,cy=e["center_xy"];dx,dy=e["down_unit_xy"];assert abs(dx*dx+dy*dy-1)<1e-6
 u=(X-cx)*dy-(Y-cy)*dx;v=(X-cx)*dx+(Y-cy)*dy
 lx,ly=e["light_cap"]["center_local_xy"];rx,ry=e["light_cap"]["radii_xy"];q=np.sqrt(((u-lx)/rx)**2+((v-ly)/ry)**2)
 width=e["light_transition_width_px"];weight=np.clip((1-q)*min(rx,ry)/width+.5,0,1)
 rgb=np.rint(np.array(spec["dark_rgb"],float)+weight[:,:,None]*(np.array(spec["light_rgb"],float)-np.array(spec["dark_rgb"],float))).astype("uint8")
 expected[m,:3]=rgb[m]
 detail={"name":e["name"],"mask":e["interior_mask"],"glint":e["protected_glint_mask"],"allowed_pixels":int(m.sum()),"glint_pixels":int(g.sum()),"declared_row_spans_mask_mismatch_pixels":declared_diff,"exact_expected_RGB_mismatch_pixels":int(np.any(after[m,:3]!=rgb[m],axis=1).sum()),"dark_core_pixels":int((m&(weight==0)).sum()),"light_core_pixels":int((m&(weight==1)).sum()),"transition_pixels":int((m&(weight>0)&(weight<1)).sum()),"iris_bbox_xyxy":e["iris_bbox_xyxy"]}
 details.append(detail)
ov=np.array(original_white);ov[allowed]=np.rint(ov[allowed]*.35+np.array([0,200,240])*.65).astype("uint8");ov[glints]=[255,0,220];ov=Image.fromarray(ov)
diags=[]
for e in spec["eyes"]:
 n=e["name"];bb=e["iris_bbox_xyxy"];box=[bb[0]-10,bb[1]-12,bb[2]+12,bb[3]+10];cw,ch=box[2]-box[0],box[3]-box[1]
 for label,pic in [("ORIGINAL",original_white),("FINAL",final_white)]:
  for sc in [1,8]:
   path=D/(n+"_"+label+f"_{sc}x.png");pic.crop(box).resize((cw*sc,ch*sc),Image.Resampling.NEAREST).save(path);diags.append(ev(path))
 canvas=Image.new("RGB",(cw*8*3,ch*8+24),"#ddd");dr=ImageDraw.Draw(canvas)
 for j,(pic,title) in enumerate([(original_white,"ORIGINAL"),(ov,"CYAN edit/PINK original glint"),(final_white,"FINAL PY OUTPUT")]):
  canvas.paste(pic.crop(box).resize((cw*8,ch*8),Image.Resampling.NEAREST),(j*cw*8,24));dr.text((j*cw*8+3,5),title,fill="black")
 path=D/(n+"_ORIGINAL_MASK_FINAL_8x.png");canvas.save(path);diags.append(ev(path))
changed=np.any(before!=after,axis=2);cm=np.array(Image.open(R/"changed_pixels_mask.png"))==255
summary={"changed_pixels":int(changed.sum()),"allowed_pixels":int(allowed.sum()),"protected_glint_pixels":int(glints.sum()),"outside_mask_RGBA_changed_pixels":int((changed&~allowed).sum()),"alpha_changed_pixels":int((before[:,:,3]!=after[:,:,3]).sum()),"protected_glint_RGBA_changed_pixels":int(np.any(before[glints]!=after[glints],axis=1).sum()),"expected_full_RGBA_mismatch_pixels":int(np.any(expected!=after,axis=2).sum()),"saved_changed_mask_mismatch_pixels":int(np.logical_xor(changed,cm).sum())}
qa={}
for label,bg in [("white","white"),("black","black")]:
 canvas=Image.new("RGBA",(W,H),bg);canvas.alpha_composite(Image.fromarray(after));arr=np.array(canvas.convert("RGB"));provided=np.array(Image.open(R/("qa_"+label+".png")).convert("RGB"));qa[label+"_QA_RGB_mismatch_pixels"]=int(np.any(arr!=provided,axis=2).sum())
assert summary["outside_mask_RGBA_changed_pixels"]==summary["alpha_changed_pixels"]==summary["protected_glint_RGBA_changed_pixels"]==summary["expected_full_RGBA_mismatch_pixels"]==summary["saved_changed_mask_mismatch_pixels"]==0
assert all(v==0 for v in qa.values())
parents=[]
for e in spec["whole_art_pass_evidence"]:
 path=Path(e["path"]);assert sha(path)==e["sha256"];o=json.loads(path.read_text("utf8"));assert o["image_sha256"]==sha(src)
 passed=o.get("primary_static_pass",False) or o.get("review_status")=="retained_static_candidate";assert passed
 parents.append({"path":str(path),"sha256":sha(path),"image_sha256":o["image_sha256"],"exact_parent_static_pass_read":True})
report={"reviewer":"Sol xhigh independent NumPy recomputation; not mask preparer or apply operator","source":ev(src),"output":ev(dest),"approved_spec":ev(sp),"calculation":"Independent direct native-grid local-axis ellipse, clip signed cap distance and np.rint exact RGB; no official recolor/validator functions imported or executed. Declared row-span domains independently rebuilt.","per_eye":details,"pixel_summary":summary,"QA_composite_recheck":qa,"parent_static_evidence":parents,"diagnostics":diags,"API_calls":0,"imagegen_calls":0,"recolor_apply_calls":0,"central_writes":False}
ap=D/"INDEPENDENT_PIXEL_AUDIT.json";ap.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({"audit":ev(ap),"summary":summary,"per_eye":[{"name":e["name"],"allowed":e["allowed_pixels"],"glint":e["glint_pixels"],"RGB_mismatch":e["exact_expected_RGB_mismatch_pixels"]} for e in details],"QA":qa},ensure_ascii=False))

