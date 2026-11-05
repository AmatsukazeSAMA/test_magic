from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=B/"drawings/ART-X01-12/v01/whole_imggen_user_wrongside_sourceOnly_farLEFT_v01";P=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_12_MASK_PREP_v01"
src=R/"character_imggen_original.png";sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)=="0ce8713d7b22594ec12c3998bc15d89b03462ecd5b2585bd5df6d7d6c163c9b5"
im=Image.open(src);a=np.array(im);H,W=a.shape[:2];Y,X=np.indices((H,W));out=a.copy();allow=np.zeros((H,W),bool);protect=allow.copy();dark=np.array([72,69,67],float);light=np.array([129,128,128],float)
settings=[
dict(name="viewer_left",roi=[356,260,394,299],first=265,last=297,toprows=[265,266,267],
clip={265:(364,379),266:(362,379),267:(361,380),268:(360,383),269:(359,384),270:(359,386),271:(359,387),272:(358,387),273:(358,388),274:(358,388),287:(361,391),288:(361,391),289:(362,391)},
glintbox=[361,267,370,276],center=[374.6,281],down=[.28,math.sqrt(1-.28**2)],capcenter=[0,17.2],radii=[14,15]),
dict(name="viewer_right",roi=[440,237,474,272],first=239,last=269,toprows=[239,240,241],
clip={239:(451,460),240:(449,462),241:(447,463),242:(445,464),243:(443,465),244:(443,467),245:(442,468),246:(442,468),247:(442,469),261:(444,472),262:(444,472),263:(445,471)},
glintbox=[448,237,461,249],center=[455.7,254.1],down=[.34,math.sqrt(1-.34**2)],capcenter=[0,15.9],radii=[12.5,14])
]
eyes=[]
for e in settings:
    m=np.zeros((H,W),bool);env=m.copy();x0,y0,x1,y1=e["roi"]
    for y in range(e["first"],e["last"]+1):
        rgb=a[y,x0:x1,:3].astype(int);idx=np.where((rgb.max(1)-rgb.min(1)<28)&(rgb.mean(1)<165))[0]+x0
        if not len(idx):continue
        runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1);r=max(runs,key=len);lo,hi=int(r[0]),int(r[-1])+1
        if y in e["clip"]:lo,hi=e["clip"][y]
        env[y,lo:hi]=True;m[y,lo:hi]=True
        if y in e["toprows"]:m[y,a[y,:,:3].astype(int).mean(1)<34]=False
    x0,y0,x1,y1=e["glintbox"];g=np.zeros((H,W),bool);c=a[y0:y1,x0:x1,:3].astype(int)
    g[y0:y1,x0:x1]=(c.mean(2)>80)&(c.max(2)-c.min(2)<40)
    # Include only the original highlight support within the actual iris envelope, never neighboring sclera.
    g&=env;m[g]=False;allow|=m;protect|=g
    mp=P/(e["name"]+"_FULL_IRIS_MASK.png");gp=P/(e["name"]+"_GLINT_PROTECTION.png")
    Image.fromarray(m.astype("uint8")*255).save(mp);Image.fromarray(g.astype("uint8")*255).save(gp)
    cx,cy=e["center"];dx,dy=e["down"];u=(X-cx)*dy-(Y-cy)*dx;v=(X-cx)*dx+(Y-cy)*dy;lx,ly=e["capcenter"];rx,ry=e["radii"]
    q=np.hypot((u-lx)/rx,(v-ly)/ry);t=np.clip((1-q)*min(rx,ry)/1.5+.5,0,1)
    rgb=np.rint(dark+t[:,:,None]*(light-dark)).astype("uint8");out[m,:3]=rgb[m]
    yy,xx=np.where(m);gy,gx=np.where(g)
    eyes.append(dict(name=e["name"],interior_mask=dict(path=str(mp),sha256=sha(mp)),protected_glint_mask=dict(path=str(gp),sha256=sha(gp)),center_xy=e["center"],down_unit_xy=e["down"],
      light_cap=dict(center_local_xy=e["capcenter"],radii_xy=e["radii"]),light_transition_width_px=1.5,
      expression_reviewed=True,expression_classification="normal_open",expression_reviewed_by="Sol xhigh actual selected whole/fullWB/own4070guide and native/12x; each eye visibly open despite original petal occlusion",
      mask_reviewed=False,root_mask_reviewed=False,allowed_pixels=int(m.sum()),protected_glint_pixels=int(g.sum()),
      iris_bbox_xyxy=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],glint_bbox_xyxy=[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)],
      upper_dark_coverage_added=False,upper_connection_scope="Respect actual curved original join and upper liner; no generic rectangular top patch or new upper-AA coverage."))
Image.fromarray(allow.astype("uint8")*255).save(P/"BOTH_FULL_IRIS_PERMISSION.png");Image.fromarray(protect.astype("uint8")*255).save(P/"BOTH_GLINT_PROTECTION.png")
preview=P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png";Image.fromarray(out).save(preview)
sw=Image.new("RGBA",im.size,"white");sw.alpha_composite(im);nw=Image.new("RGBA",im.size,"white");nw.alpha_composite(Image.fromarray(out));nw.convert("RGB").save(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_WHITE.png")
ov=np.array(sw.convert("RGB"));ov[allow]=np.rint(ov[allow]*.35+np.array([0,200,240])*.65).astype("uint8");ov[protect]=[255,0,220];ov=Image.fromarray(ov)
diags=[]
for name,box in [("viewer_left",(342,254,400,306)),("viewer_right",(435,228,477,277))]:
    cw,ch=box[2]-box[0],box[3]-box[1]
    for sc in [1,8]:
        canvas=Image.new("RGB",(cw*sc*3,ch*sc+24),"#dddddd");d=ImageDraw.Draw(canvas)
        for j,(panel,label) in enumerate([(sw.convert("RGB"),"ORIGINAL"),(ov,"CYAN permit/MAGENTA glint"),(nw.convert("RGB"),"DIAGNOSTIC ONLY")]):
            part=panel.crop(box).resize((cw*sc,ch*sc),Image.Resampling.NEAREST);canvas.paste(part,(j*cw*sc,24));d.text((j*cw*sc+2,5),label,fill="black")
        p=P/f"{name}_ORIGINAL_MASK_PREVIEW_{sc}x.png";canvas.save(p);diags.append(dict(path=str(p),sha256=sha(p),crop_xyxy=list(box),scale=sc))
spec=dict(id="ART-X01-12",prep_status="PREP_ONLY_PENDING_ROOT_MASK_AND_CAP_APPROVAL_DO_NOT_APPLY",input=dict(path=str(src),sha256=sha(src)),input_dimensions=list(im.size),dark_rgb=[72,69,67],light_rgb=[129,128,128],eyes=eyes,
policy=dict(path=str(B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json"),sha256=sha(B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json")),
policy_id="post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",root_mask_reviewed=False,root_release_granted=False,color_edit_applied=False,upper_dark_coverage_added=False,
scope="Only selected current iris-interior RGB plus local broad lower convex cap; original eye silhouette, upper liner/lashes/sclera/glints/AA/all alpha/outside locked. Original petal does not make both returned visible eyes exempt. PREP only; no final apply.",
generation_calls=0,API_calls=0,central_writes=False)
sp=P/"X01_12_FULL_IRIS_SPEC_PREPONLY_v01.json";sp.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
changed=np.any(a!=out,axis=2)
receipt=dict(id="ART-X01-12",spec=dict(path=str(sp),sha256=sha(sp)),input=spec["input"],eyes=eyes,allowed_pixels=int(allow.sum()),protected_glint_pixels=int(protect.sum()),
diagnostic_only_preview=dict(path=str(preview),sha256=sha(preview)),diagnostics=diags,
pixel_check=dict(outside_mask_RGBA_changes=int((changed&~allow).sum()),alpha_changes=int((a[:,:,3]!=out[:,:,3]).sum()),glint_RGBA_changes=int(np.any(a[protect]!=out[protect],axis=1).sum()),changed_pixels=int(changed.sum())),
final_apply_executed=False,root_release_granted=False,generation_calls=0)
(P/"PREP_ONLY_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,ensure_ascii=False))

