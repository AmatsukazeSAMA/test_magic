from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/direct_first_api_canonical1324_wider3766_fourRefs_noShoulderCrop_postPassEye_v16");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G13_29_MASK_PREP_v01");src=R/"character_api_original.png";sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest()
assert sha(src)=="af86db358694df0cc43dcea5a0f9ab9c99ec387040f54227cf8d37814586c927"
im=Image.open(src);assert im.mode=="RGBA" and im.size==(976,976);a=np.array(im);H,W=a.shape[:2];Y,X=np.indices((H,W));out=a.copy();allow=np.zeros((H,W),bool);protect=allow.copy()
settings=[
dict(name="viewer_left",roi=[287,279,345,335],first=280,last=333,
clip={280:(309,334),281:(308,334),282:(306,334),283:(302,335),284:(301,335),285:(299,336),286:(298,337),287:(297,338),288:(296,338),289:(295,339),290:(294,339),291:(293,340),292:(292,340),293:(292,341),294:(291,341),330:(298,330),331:(299,329),332:(302,328),333:(304,326)},
glintbox=[306,282,323,297],center=[315.0,306.5],down=[-.28,.96],capcenter=[0,27.5],radii=[24.5,25.5]),
dict(name="viewer_right",roi=[427,334,484,389],first=335,last=387,
clip={335:(446,466),336:(441,471),337:(438,473),338:(435,474),339:(434,475),340:(433,476),341:(433,477),342:(434,478),343:(433,478),344:(432,479),345:(431,479),346:(431,480)},
glintbox=[448,335,464,353],center=[454.5,360.8],down=[-.36,math.sqrt(1-.36**2)],capcenter=[0,26.5],radii=[23.3,24.2])
]
eyes=[]
for e in settings:
 m=np.zeros((H,W),bool);env=m.copy();x0,y0,x1,y1=e["roi"]
 for y in range(e["first"],e["last"]+1):
  if y in e["clip"]:lo,hi=e["clip"][y]
  else:
   c=a[y,x0:x1,:3].astype(int);idx=np.where((c.max(1)-c.min(1)<30)&(c.mean(1)<165))[0]+x0
   if not len(idx):continue
   # The original glint splits a row into two gray runs: both are the SAME
   # iris envelope. Preserve the full manually isolated row, then subtract
   # the exact glint support; choosing only the longest run leaves stripes.
   lo,hi=int(idx[0]),int(idx[-1])+1
  env[y,lo:hi]=True;m[y,lo:hi]=True
 gx0,gy0,gx1,gy1=e["glintbox"];g=np.zeros((H,W),bool);c=a[gy0:gy1,gx0:gx1,:3].astype(int)
 g[gy0:gy1,gx0:gx1]=(c.mean(2)>100)&(c.max(2)-c.min(2)<40);g&=env;m[g]=False
 assert not np.any(m&allow);allow|=m;protect|=g
 mp=P/(e["name"]+"_FULL_IRIS_MASK.png");gp=P/(e["name"]+"_GLINT_PROTECTION.png");Image.fromarray(m.astype("uint8")*255).save(mp);Image.fromarray(g.astype("uint8")*255).save(gp)
 cx,cy=e["center"];dx,dy=e["down"];u=(X-cx)*dy-(Y-cy)*dx;v=(X-cx)*dx+(Y-cy)*dy;lx,ly=e["capcenter"];rx,ry=e["radii"]
 q=np.hypot((u-lx)/rx,(v-ly)/ry);t=np.clip((1-q)*min(rx,ry)/1.5+.5,0,1);dark=np.array([72,69,67]);light=np.array([129,128,128]);rgb=np.rint(dark+t[:,:,None]*(light-dark)).astype("uint8");out[m,:3]=rgb[m]
 yy,xx=np.where(m);gy,gx=np.where(g)
 eyes.append({"name":e["name"],"interior_mask":{"path":str(mp),"sha256":sha(mp)},"protected_glint_mask":{"path":str(gp),"sha256":sha(gp)},"center_xy":e["center"],"down_unit_xy":e["down"],"light_cap":{"center_local_xy":e["capcenter"],"radii_xy":e["radii"]},"light_transition_width_px":1.5,"expression_reviewed":True,"expression_classification":"normal_open","expression_reviewed_by":"Sol xhigh actual current raw/full whiteblack, native/8x and per-native-pixel upper boundary grid; each eye freshly traced, original unequal aperture/head tilt not borrowed from reference","mask_reviewed":False,"root_mask_reviewed":False,"allowed_pixels":int(m.sum()),"protected_glint_pixels":int(g.sum()),"iris_bbox_xyxy":[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],"glint_bbox_xyxy":[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)],"upper_dark_coverage_added":False,"upper_connection_scope":"Actual native upper iris cap lies below true upper liner; no separate upper dark-coverage/outline-shape revision. Preserve original liner/lash and outer AA."})
Image.fromarray(allow.astype("uint8")*255).save(P/"BOTH_FULL_IRIS_PERMISSION.png");Image.fromarray(protect.astype("uint8")*255).save(P/"BOTH_GLINT_PROTECTION.png")
preview=P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png";Image.fromarray(out).save(preview);w=Image.open(R/"qa_white.png").convert("RGB")
nw=Image.new("RGBA",im.size,"white");nw.alpha_composite(Image.fromarray(out));nw=nw.convert("RGB");nw.save(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_WHITE.png")
ov=np.array(w);ov[allow]=np.rint(ov[allow]*.35+np.array([0,200,240])*.65).astype("uint8");ov[protect]=[255,0,220];ov=Image.fromarray(ov);ov.save(P/"FULL_MASK_OVERLAY_NATIVE.png")
diags=[]
for n,box in [("viewer_left",[271,266,369,343]),("viewer_right",[416,320,509,398])]:
 cw,ch=box[2]-box[0],box[3]-box[1]
 for sc in [1,8]:
  panel=Image.new("RGB",(cw*sc*3,ch*sc+24),"#ddd");d=ImageDraw.Draw(panel)
  for j,(pic,label) in enumerate([(w,"ORIGINAL"),(ov,"CYAN permission / PINK glint"),(nw,"PREVIEW ONLY")]):
   panel.paste(pic.crop(box).resize((cw*sc,ch*sc),Image.Resampling.NEAREST),(j*cw*sc,24));d.text((j*cw*sc+2,5),label,fill="black")
  dp=P/(n+f"_ORIGINAL_MASK_PREVIEW_{sc}x.png");panel.save(dp);diags.append({"path":str(dp),"sha256":sha(dp),"crop_xyxy":box,"scale":sc})
policy=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json";primary=R/"PRIMARY_GOAL_REVIEW.json";ind=B/"review/SOL_FIRST_G13_29_MINIMAL_FOUR_REFS_20261104_v16.json"
for pp in [primary,ind]:
 o=json.loads(pp.read_text("utf8"));assert o["image_sha256"]==sha(src)
assert json.loads(primary.read_text("utf8"))["primary_static_pass"] and json.loads(ind.read_text("utf8"))["review_status"]=="retained_static_candidate"
spec={"id":"ART-G13-29","prep_status":"PREP_ONLY_PENDING_ROOT_MASK_AND_WIDE_CAP_APPROVAL_DO_NOT_APPLY","input":{"path":str(src),"sha256":sha(src)},"input_dimensions":[976,976],"dark_rgb":[72,69,67],"light_rgb":[129,128,128],"eyes":eyes,"policy":{"path":str(policy),"sha256":sha(policy)},"policy_id":"post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03","whole_art_pass_evidence":[{"path":str(x),"sha256":sha(x)} for x in [primary,ind]],"root_mask_reviewed":False,"root_release_granted":False,"color_edit_applied":False,"upper_dark_coverage_added":False,"scope":"Fresh per-eye native iris-interior RGB and its own-axis broad lower convex cap only; no reference outline/gaze/glint or symmetric-eye template. Upper liner/lashes/sclera/all alpha/outside immutable. Diagnostic preview is not final output or selectable.","generation_calls":0,"API_calls":0,"central_writes":False}
sp=P/"G13_29_FULL_IRIS_SPEC_PREPONLY_v01.json";sp.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
changed=np.any(a!=out,axis=2);assert not np.any(changed&~allow) and np.array_equal(a[...,3],out[...,3]) and np.array_equal(a[protect],out[protect])
receipt={"id":"ART-G13-29","spec":{"path":str(sp),"sha256":sha(sp)},"input":spec["input"],"eyes":eyes,"allowed_pixels":int(allow.sum()),"protected_glint_pixels":int(protect.sum()),"diagnostic_only_preview":{"path":str(preview),"sha256":sha(preview),"production_selectable":False},"diagnostics":diags,"pixel_check":{"changed_pixels":int(changed.sum()),"outside_mask_RGBA_changes":int((changed&~allow).sum()),"alpha_changes":int((a[...,3]!=out[...,3]).sum()),"protected_glint_RGBA_changes":int(np.any(a[protect]!=out[protect],axis=1).sum())},"final_apply_executed":False,"root_release_granted":False,"generation_calls":0}
(P/"PREP_ONLY_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({"spec":receipt["spec"],"eyes":[{"name":x["name"],"count":x["allowed_pixels"],"glint":x["protected_glint_pixels"],"bbox":x["iris_bbox_xyxy"]} for x in eyes],"pixel_check":receipt["pixel_check"]},ensure_ascii=False))

