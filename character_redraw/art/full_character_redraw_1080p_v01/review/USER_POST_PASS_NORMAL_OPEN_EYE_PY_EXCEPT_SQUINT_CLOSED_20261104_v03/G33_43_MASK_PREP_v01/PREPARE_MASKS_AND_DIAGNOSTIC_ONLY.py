from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,hashlib,json,math
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=B/"drawings/ART-G33-43/v01/whole_imggen_sourceOnlyBody_frontRootContext_v02";P=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G33_43_MASK_PREP_v01"
src=R/"character_imggen_original.png";im=Image.open(src);assert im.mode=="RGBA" and im.size==(957,1644);a=np.array(im);H,W=a.shape[:2]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
Y,X=np.indices((H,W));dark=np.array([72,69,67],float);light=np.array([129,128,128],float);preview=a.copy()
settings=[
 dict(name="viewer_left",box=[431,237,472,281],first=237,last=280,toprows=[237,238,239],clip={237:(452,461),238:(449,462),239:(447,463),240:(444,464),241:(443,465),242:(442,466),243:(442,467),244:(441,468),245:(440,469),246:(439,469),247:(439,470),248:(438,470),249:(437,471),250:(437,471),251:(437,471),252:(436,471)},glintbox=[453,240,462,249],center=[451.6,258.8],down=[-.18,math.sqrt(1-.18**2)],capcenter=[0,15.5],radii=[10.5,14.7]),
 dict(name="viewer_right",box=[531,266,573,313],first=268,last=310,toprows=[268,269,270],clip={268:(548,561),269:(547,562),270:(544,563),271:(542,564),272:(541,565),273:(540,566),274:(539,567),275:(538,568),276:(537,569),277:(537,570),278:(536,571),279:(535,572),280:(535,572),281:(534,572),282:(534,572),283:(534,572),284:(533,572),285:(533,572),286:(533,572)},glintbox=[553,270,562,278],center=[551.5,288.8],down=[-.20,math.sqrt(1-.20**2)],capcenter=[0,15.7],radii=[11.4,15.0])
]
eyes=[];combined=np.zeros((H,W),bool);protectall=combined.copy()
for e in settings:
    mask=np.zeros((H,W),bool);x0,y0,x1,y1=e["box"]
    for y in range(e["first"],e["last"]+1):
        row=a[y,x0:x1,:3].astype(int);good=(row.max(1)-row.min(1)<28)&(row.mean(1)<165)
        inds=np.where(good)[0]+x0
        if not len(inds):continue
        runs=np.split(inds,np.where(np.diff(inds)>1)[0]+1)
        # Manually reviewed iris crop; use the run crossing the iris body, not the separate lower outer-lash.
        run=max(runs,key=len)
        lo,hi=int(run[0]),int(run[-1])+1
        # Glint can split the gray run in upper rows; manual curve limits supply those full intervals.
        if y in e["clip"]:lo,hi=e["clip"][y]
        mask[y,lo:hi]=True
        # Keep genuine dark upper-liner contact pixels in first three native rows; do not replace the line.
        if y in e["toprows"]:
            line=(a[y,:,:3].astype(int).mean(1)<34)
            mask[y,line]=False
    gx0,gy0,gx1,gy1=e["glintbox"];glint=np.zeros((H,W),bool)
    gr=a[gy0:gy1,gx0:gx1,:3].astype(int)
    glint[gy0:gy1,gx0:gx1]=(gr.mean(2)>80)&(gr.max(2)-gr.min(2)<40)
    mask[glint]=False
    assert not (mask&combined).any();combined|=mask;protectall|=glint
    mp=P/(e["name"]+"_FULL_IRIS_MASK.png");gp=P/(e["name"]+"_GLINT_PROTECTION.png")
    Image.fromarray(mask.astype("uint8")*255).save(mp);Image.fromarray(glint.astype("uint8")*255).save(gp)
    cx,cy=e["center"];dx,dy=e["down"];rx,ry=e["radii"];lx,ly=e["capcenter"]
    u=(X-cx)*dy-(Y-cy)*dx;v=(X-cx)*dx+(Y-cy)*dy
    q=np.hypot((u-lx)/rx,(v-ly)/ry)
    t=np.clip((1-q)*min(rx,ry)/1.5+.5,0,1)
    rgb=np.rint(dark+t[:,:,None]*(light-dark)).astype("uint8")
    preview[mask,:3]=rgb[mask]
    ys,xs=np.where(mask);py,px=np.where(glint)
    eye=dict(name=e["name"],interior_mask=dict(path=str(mp),sha256=sha(mp)),protected_glint_mask=dict(path=str(gp),sha256=sha(gp)),
       center_xy=e["center"],down_unit_xy=e["down"],light_cap=dict(center_local_xy=e["capcenter"],radii_xy=e["radii"]),light_transition_width_px=1.5,
       expression_reviewed=True,expression_classification="normal_open",expression_reviewed_by="Sol xhigh actual current native/12x and own F2488 full/guide; source aperture retained",
       mask_reviewed=False,root_mask_reviewed=False,allowed_pixels=int(mask.sum()),protected_glint_pixels=int(glint.sum()),iris_bbox_xyxy=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
       glint_bbox_xyxy=[int(px.min()),int(py.min()),int(px.max()+1),int(py.max()+1)],upper_dark_coverage_added=False,
       upper_connection_scope="Existing native rounded join used; top-row original true upper-liner pixels excluded, no blind coverage/ellipse applied to upper eye outline.")
    eyes.append(eye)
Image.fromarray(combined.astype("uint8")*255).save(P/"BOTH_FULL_IRIS_PERMISSION.png");Image.fromarray(protectall.astype("uint8")*255).save(P/"BOTH_GLINT_PROTECTION.png")
pp=P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png";Image.fromarray(preview).save(pp)
# Full-size and eye-pair previews are diagnostics, not a production apply/output.
white=Image.new("RGBA",im.size,"white");white.alpha_composite(Image.fromarray(preview));white.convert("RGB").save(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_WHITE.png")
origwhite=Image.new("RGBA",im.size,"white");origwhite.alpha_composite(im);origwhite=origwhite.convert("RGB")
overlay=np.array(origwhite).copy();overlay[combined]=np.rint(overlay[combined]*.35+np.array([0,200,240])*.65).astype("uint8");overlay[protectall]=[255,0,220]
overlay=Image.fromarray(overlay)
pairbox=(410,220,586,322);diag=[]
for sc in [1,8]:
    cw,ch=pairbox[2]-pairbox[0],pairbox[3]-pairbox[1];canvas=Image.new("RGB",(cw*sc*3,ch*sc+24),"#dddddd");d=ImageDraw.Draw(canvas)
    for j,(panel,label) in enumerate([(origwhite,"ORIGINAL"),(overlay,"CYAN allowed / MAGENTA protected"),(white.convert("RGB"),"DIAGNOSTIC COLOR ONLY")]):
        p=panel.crop(pairbox).resize((cw*sc,ch*sc),Image.Resampling.NEAREST);canvas.paste(p,(j*cw*sc,24));d.text((j*cw*sc+2,4),label,fill="black")
    dest=P/f"ORIGINAL_MASK_PREVIEW_{sc}x.png";canvas.save(dest);diag.append(dict(path=str(dest),sha256=sha(dest)))
spec=dict(id="ART-G33-43",prep_status="PREP_ONLY_PENDING_ROOT_ACTUAL_MASK_APPROVAL_DO_NOT_APPLY",input=dict(path=str(src),sha256=sha(src)),input_dimensions=list(im.size),
   dark_rgb=[72,69,67],light_rgb=[129,128,128],eyes=eyes,
   policy=dict(path=str(B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json"),sha256=sha(B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json")),
   policy_id="post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",root_mask_reviewed=False,root_release_granted=False,color_edit_applied=False,
   scope="Iris-interior RGB and lower light-gray internal convex cap only. Actual mask/diagnostic preparation; native upper eye-liner/sclera/lashes/glint/outer AA/all alpha/outside locked. No final apply script executed.",
   upper_dark_coverage_must_be_honored=False,upper_dark_coverage_added=False,
   generation_calls=0,API_calls=0,central_writes=False)
sp=P/"G33_43_FULL_IRIS_SPEC_PREPONLY_v01.json";sp.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
changed=np.any(a!=preview,axis=2)
receipt=dict(spec=dict(path=str(sp),sha256=sha(sp)),input=spec["input"],eyes=eyes,allowed_pixels=int(combined.sum()),glint_pixels=int(protectall.sum()),
   diagnostic_only_preview=dict(path=str(pp),sha256=sha(pp)),diagnostics=diag,
   diagnostic_pixel_check=dict(outside_mask_RGBA_changes=int((changed&~combined).sum()),alpha_changes=int((a[:,:,3]!=preview[:,:,3]).sum()),glint_RGBA_changes=int(np.any(a[protectall]!=preview[protectall],axis=1).sum()),changed_pixels=int(changed.sum())),
   generation_calls=0,final_apply_executed=False,root_approval_pending=True)
(P/"PREP_ONLY_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,ensure_ascii=False))

