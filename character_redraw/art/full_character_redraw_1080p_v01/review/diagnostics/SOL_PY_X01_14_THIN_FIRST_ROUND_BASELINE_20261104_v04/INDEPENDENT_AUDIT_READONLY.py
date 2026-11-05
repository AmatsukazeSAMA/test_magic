import json, hashlib, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
R=B/"drawings/ART-X01-14/v01/py_post_pass_thin_first_round_baseline_eyes_v04"
D=B/"review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04"
D.mkdir(parents=True,exist_ok=True)
ver=json.loads((R/"VERIFICATION.json").read_text(encoding="utf-8-sig"))
sp=Path(ver["spec"]["path"]); spec=json.loads(sp.read_text(encoding="utf-8-sig"))
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert h(sp)=="50ddaba05f5411c3958effb6c597882ab55e2639aa9f9a265df9ce2bc9f0634e"
ip=Path(spec["input"]["path"]); op=R/"character_eye_gray_local.png"
assert h(ip)=="8181037962aaa0624155fc5ac1af924536be55f5b4b35311f4cf78d748de29ae"
assert h(op)=="ca8c7fe058a6578b3562975387651052f73c87dc086f393d56f3f2663be5d5a7"
a=np.array(Image.open(ip).convert("RGBA")); o=np.array(Image.open(op).convert("RGBA"))
assert a.shape==o.shape and list(Image.open(ip).size)==spec["input_dimensions"]
H,W=a.shape[:2]; Y,X=np.indices((H,W)); exp=a.copy()
union=np.zeros((H,W),bool); guards=union.copy(); per=[]; diag=[]
def save(im,name):
 p=D/name; im.save(p); diag.append({"path":str(p),"sha256":h(p)});return p
def white(arr):
 im=Image.fromarray(arr); bg=Image.new("RGBA",im.size,"white");bg.alpha_composite(im);return bg.convert("RGB")
for e in spec["eyes"]:
 mrec=e["interior_mask"]; grec=e["protected_glint_mask"]
 assert h(mrec["path"])==mrec["sha256"] and h(grec["path"])==grec["sha256"]
 mm=Image.open(mrec["path"]); gg=Image.open(grec["path"])
 assert mm.mode==gg.mode=="L" and mm.size==gg.size==(W,H)
 mn=np.array(mm); gn=np.array(gg)
 assert set(np.unique(mn))<={0,255} and set(np.unique(gn))<={0,255}
 m=mn==255;g=gn==255
 assert not np.any(m&union) and not np.any(m&g)
 union|=m;guards|=g
 cx,cy=e["center_xy"];dx,dy=e["down_unit_xy"]
 assert abs(math.hypot(dx,dy)-1)<1e-9
 u=(X-cx)*dy-(Y-cy)*dx;v=(X-cx)*dx+(Y-cy)*dy
 lx,ly=e["light_cap"]["center_local_xy"];rx,ry=e["light_cap"]["radii_xy"]
 q=np.sqrt(((u-lx)/rx)**2+((v-ly)/ry)**2)
 weights=np.clip(((1-q)*min(rx,ry))/e["light_transition_width_px"]+.5,0,1)
 dc=np.array(spec["dark_rgb"],float);lc=np.array(spec["light_rgb"],float)
 rgb=np.rint(dc+weights[...,None]*(lc-dc)).astype(np.uint8)
 exp[m,:3]=rgb[m]
 yy,xx=np.where(m)
 parent_values=a[m,:3].astype(float)
 oldlight=np.linalg.norm(parent_values-lc,axis=1)<=np.linalg.norm(parent_values-dc,axis=1)
 count=int(m.sum())
 per.append({"name":e["name"],"mask":mrec,"glint":grec,"allowed_pixels":count,"protected_glint_pixels":int(g.sum()),"mask_bbox_xyxy_exclusive":[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],"changed_pixels":int(np.any(a[m]!=o[m],axis=1).sum()),"expected_RGB_mismatch_pixels":int(np.any(rgb[m]!=o[m,:3],axis=1).sum()),"light_core_pixels":int(np.count_nonzero(weights[m]==1)),"dark_core_pixels":int(np.count_nonzero(weights[m]==0)),"AA_pixels":int(np.count_nonzero((weights[m]>0)&(weights[m]<1))),"weighted_light_fraction":float(weights[m].mean()),"half_coverage_light_fraction":float(np.mean(weights[m]>=.5)),"original_nearest_palette_light_fraction":float(oldlight.mean()),"note":"Independent current native-mask AA weight measurement adapted to the approved round-cap baseline; not a fixed user area rule."})
 box=tuple(e["context_roi_xyxy_exclusive"]); orig=white(a).crop(box);final=white(o).crop(box)
 save(orig,e["name"]+"_ORIGINAL_1x.png");save(final,e["name"]+"_FINAL_1x.png")
 overlay=white(a).copy();z=np.array(overlay);z[m]=[0,210,230];z[g]=[255,0,200]
 overlay=Image.fromarray(z).crop(box)
 panels=[orig,overlay,final];pw,ph=orig.size; panel=Image.new("RGB",(pw*3,ph),"white")
 for i,p in enumerate(panels):panel.paste(p,(i*pw,0))
 save(panel.resize((pw*3*8,ph*8),Image.Resampling.NEAREST),e["name"]+"_ORIGINAL_MASK_FINAL_8x.png")
changed=np.any(a!=o,axis=2)
assert all(e["expected_RGB_mismatch_pixels"]==0 for e in per)
qa=[]
for color,name in [((255,255,255),"qa_white.png"),((0,0,0),"qa_black.png")]:
 bg=Image.new("RGBA",(W,H),color+(255,));bg.alpha_composite(Image.fromarray(o));calc=np.array(bg.convert("RGB"))
 actual=np.array(Image.open(R/name).convert("RGB"))
 qa.append({"path":str(R/name),"sha256":h(R/name),"independent_composite_RGB_mismatch_pixels":int(np.any(calc!=actual,axis=2).sum())})
parents=[]
for x in spec["whole_art_pass_evidence"]:
 p=Path(x["path"]);v=json.loads(p.read_text(encoding="utf-8-sig"))
 assert h(p)==x["sha256"] and v["image_sha256"]==h(ip)
 passed=v.get("primary_static_pass") is True or v.get("review_status")=="retained_static_candidate"
 assert passed
 parents.append({"path":str(p),"sha256":h(p),"image_sha256":h(ip),"exact_parent_static_pass_read":True})
cm=np.array(Image.open(R/"changed_pixels_mask.png").convert("L"))>0
aud={"reviewer":"Sol xhigh independent NumPy audit; not preparer/apply operator","source":{"path":str(ip),"sha256":h(ip)},"output":{"path":str(op),"sha256":h(op)},"approved_spec":{"path":str(sp),"sha256":h(sp)},"dimensions":[W,H],"method":"Direct independent full native-grid local-axis ellipse and signed-distance1.5px AA, rounded RGB; no official apply/validator import or execution.","per_eye":per,"pixel_summary":{"changed_pixels":int(changed.sum()),"allowed_pixels":int(union.sum()),"protected_glint_pixels":int(guards.sum()),"outside_mask_RGBA_changed_pixels":int(np.count_nonzero(changed&~union)),"alpha_changed_pixels":int(np.count_nonzero(a[...,3]!=o[...,3])),"protected_glint_RGBA_changed_pixels":int(np.count_nonzero(changed&guards)),"expected_full_RGBA_mismatch_pixels":int(np.any(exp!=o,axis=2).sum()),"saved_changed_mask_mismatch_pixels":int(np.count_nonzero(cm!=changed))},"QA_composites":qa,"parent_static_evidence":parents,"diagnostics":diag,"recolor_apply_calls":0,"API_calls":0,"imagegen_calls":0,"central_writes":False}
(D/"INDEPENDENT_PIXEL_AUDIT.json").write_text(json.dumps(aud,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"audit":str(D/"INDEPENDENT_PIXEL_AUDIT.json"),"audit_sha256":h(D/"INDEPENDENT_PIXEL_AUDIT.json"),"per_eye":per,"pixels":aud["pixel_summary"],"QA":qa},ensure_ascii=False))

