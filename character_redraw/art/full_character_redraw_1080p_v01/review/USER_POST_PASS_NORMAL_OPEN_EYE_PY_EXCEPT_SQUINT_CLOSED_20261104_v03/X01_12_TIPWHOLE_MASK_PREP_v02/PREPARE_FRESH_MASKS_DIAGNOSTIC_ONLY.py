from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-12/v01/whole_imggen_user_delete_remaining_lower_turn_only_tip_v03");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_12_TIPWHOLE_MASK_PREP_v02")
src=R/"character_imggen_original.png";sha=lambda z:hashlib.sha256(Path(z).read_bytes()).hexdigest()
assert sha(src)=="b893298201832a346c36fb496714a2a97216f3c1586fa4d094988741c29bc07f"
im=Image.open(src);assert im.mode=="RGBA" and im.size==(956,1645)
a=np.array(im);H,W=a.shape[:2];Y,X=np.indices((H,W));out=a.copy();allow=np.zeros((H,W),bool);protect=allow.copy()
settings=[
dict(name="viewer_left",roi=[357,262,394,299],first=263,last=297,
clip={263:(368,380),264:(365,380),265:(363,380),266:(362,381),267:(361,382),268:(360,383),269:(360,387),270:(360,387),271:(360,388),272:(359,389),273:(359,389),274:(359,390),287:(362,393),288:(362,393),289:(363,393),290:(364,393),291:(364,392),292:(365,392),293:(366,391),294:(367,389),295:(368,386),296:(368,383),297:(369,380)},
glintbox=[361,267,372,277],center=[375.0,280.0],down=[.28,.96],capcenter=[0,17.2],radii=[14.4,15.6],toprows=[263,264,265]),
dict(name="viewer_right",roi=[441,234,474,271],first=236,last=269,
clip={236:(453,460),237:(451,462),238:(450,463),239:(450,465),240:(449,466),241:(448,467),242:(447,467),243:(446,468),244:(445,469),245:(444,469),246:(444,470),247:(443,471),261:(445,473),262:(445,473),263:(445,473),264:(446,473),265:(447,473),266:(448,471),267:(449,469),268:(451,466),269:(454,463)},
glintbox=[446,237,464,250],center=[456.5,253.2],down=[.34,math.sqrt(1-.34**2)],capcenter=[0,16],radii=[13.0,14.5],toprows=[236,237,238])
]
eyes=[]
for e in settings:
 m=np.zeros((H,W),bool);env=m.copy();x0,y0,x1,y1=e["roi"]
 for y in range(e["first"],e["last"]+1):
  if y in e["clip"]:lo,hi=e["clip"][y]
  else:
   c=a[y,x0:x1,:3].astype(int);idx=np.where((c.max(1)-c.min(1)<28)&(c.mean(1)<165))[0]+x0
   if not len(idx):continue
   runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1);z=max(runs,key=len);lo,hi=int(z[0]),int(z[-1])+1
  env[y,lo:hi]=True;m[y,lo:hi]=True
  # Manually clipped top intervals follow the visible IRIS cap, below the
  # true upper liner. Include its residual inner black RGB; never use black
  # threshold to preserve an unwanted pupil-cap inside the authorized iris.
 gx0,gy0,gx1,gy1=e["glintbox"];g=np.zeros((H,W),bool);c=a[gy0:gy1,gx0:gx1,:3].astype(int)
 g[gy0:gy1,gx0:gx1]=(c.mean(2)>90)&(c.max(2)-c.min(2)<40)
 g&=env;m[g]=False
 assert not np.any(m&allow);allow|=m;protect|=g
 mp=P/(e["name"]+"_FULL_IRIS_MASK.png");gp=P/(e["name"]+"_GLINT_PROTECTION.png")
 Image.fromarray(m.astype("uint8")*255).save(mp);Image.fromarray(g.astype("uint8")*255).save(gp)
 cx,cy=e["center"];dx,dy=e["down"];u=(X-cx)*dy-(Y-cy)*dx;v=(X-cx)*dx+(Y-cy)*dy;lx,ly=e["capcenter"];rx,ry=e["radii"]
 q=np.hypot((u-lx)/rx,(v-ly)/ry);t=np.clip((1-q)*min(rx,ry)/1.5+.5,0,1)
 color=np.rint(np.array([72,69,67])+t[:,:,None]*(np.array([129,128,128])-np.array([72,69,67]))).astype("uint8");out[m,:3]=color[m]
 yy,xx=np.where(m);gy,gx=np.where(g)
 eyes.append(dict(name=e["name"],interior_mask=dict(path=str(mp),sha256=sha(mp)),protected_glint_mask=dict(path=str(gp),sha256=sha(gp)),center_xy=e["center"],down_unit_xy=e["down"],light_cap=dict(center_local_xy=e["capcenter"],radii_xy=e["radii"]),light_transition_width_px=1.5,expression_reviewed=True,expression_classification="normal_open",expression_reviewed_by="Sol xhigh actual current full white/black QA, native/12x and per-native-pixel coordinate grid; freshly traced exact new image, not copied old mask",mask_reviewed=False,root_mask_reviewed=False,allowed_pixels=int(m.sum()),protected_glint_pixels=int(g.sum()),iris_bbox_xyxy=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],glint_bbox_xyxy=[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)],upper_dark_coverage_added=False,upper_connection_scope="No separate upper-shape or upper-dark coverage operation. Original upper liner/outer AA retained; internal lower cap only."))
Image.fromarray(allow.astype("uint8")*255).save(P/"BOTH_FULL_IRIS_PERMISSION.png");Image.fromarray(protect.astype("uint8")*255).save(P/"BOTH_GLINT_PROTECTION.png")
preview=P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_MUST_NOT_SELECT.png";Image.fromarray(out).save(preview)
white=Image.new("RGBA",im.size,"white");white.alpha_composite(im)
new=Image.new("RGBA",im.size,"white");new.alpha_composite(Image.fromarray(out));new.convert("RGB").save(P/"DIAGNOSTIC_ONLY_COLOR_PREVIEW_WHITE.png")
overlay=np.array(white.convert("RGB"));overlay[allow]=np.rint(overlay[allow]*.35+np.array([0,200,240])*.65).astype("uint8");overlay[protect]=[255,0,220];overlay=Image.fromarray(overlay)
overlay.save(P/"FULL_MASK_OVERLAY_NATIVE.png")
diags=[]
for n,box in [("viewer_left",[344,252,402,306]),("viewer_right",[434,225,485,278])]:
 cw,ch=box[2]-box[0],box[3]-box[1]
 for sc in [1,8]:
  panel=Image.new("RGB",(cw*sc*3,ch*sc+24),"#dddddd");d=ImageDraw.Draw(panel)
  for j,(pic,label) in enumerate([(white.convert("RGB"),"ORIGINAL"),(overlay,"CYAN allowed / PINK glint"),(new.convert("RGB"),"PREVIEW ONLY")]):
   panel.paste(pic.crop(box).resize((cw*sc,ch*sc),Image.Resampling.NEAREST),(j*cw*sc,24));d.text((j*cw*sc+2,5),label,fill="black")
  z=P/(n+f"_ORIGINAL_MASK_PREVIEW_{sc}x.png");panel.save(z);diags.append(dict(path=str(z),sha256=sha(z),crop_xyxy=box,scale=sc))
policy=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json"
old=B/"drawings/ART-X01-12/v01/py_post_pass_two_gray_wide_lower_arc_v01/VERIFICATION.json"
spec=dict(id="ART-X01-12",prep_status="PREP_ONLY_NEW_TIP_WHOLE_PENDING_ART_PASS_AND_ROOT_MASK_APPROVAL_DO_NOT_APPLY",input=dict(path=str(src),sha256=sha(src)),input_dimensions=list(im.size),dark_rgb=[72,69,67],light_rgb=[129,128,128],eyes=eyes,policy=dict(path=str(policy),sha256=sha(policy)),policy_id="post_pass_normal_open_eye_local_two_gray_except_squint_closed_20261104_v03",root_mask_reviewed=False,root_release_granted=False,color_edit_applied=False,upper_dark_coverage_added=False,whole_art_review_status="await_final_current_whole_independent_report_and_ROOT_selection_before_execution",prior_design_reference_only=dict(path=str(old),sha256=sha(old),scope="Only prior wide-lower-cap design; no mask, permission or previous whole pass inherited"),scope="Fresh exact current visible iris RGB plus broad lower upward-convex light-gray cap. No outline/gaze/glint/liner/lash/sclera/alpha/outside change; no final apply.",generation_calls=0,API_calls=0,central_writes=False)
sp=P/"X01_12_TIPWHOLE_FULL_IRIS_SPEC_PREPONLY_v02.json";sp.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
changed=np.any(a!=out,axis=2)
receipt=dict(id="ART-X01-12",input=spec["input"],spec=dict(path=str(sp),sha256=sha(sp)),eyes=eyes,allowed_pixels=int(allow.sum()),protected_glint_pixels=int(protect.sum()),diagnostic_only_preview=dict(path=str(preview),sha256=sha(preview)),diagnostics=diags,pixel_check=dict(changed_pixels=int(changed.sum()),outside_mask_RGBA_changes=int((changed&~allow).sum()),alpha_changes=int((a[:,:,3]!=out[:,:,3]).sum()),glint_RGBA_changes=int(np.any(a[protect]!=out[protect],axis=1).sum())),final_apply_executed=False,root_release_granted=False,generation_calls=0)
(P/"PREP_ONLY_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(receipt,ensure_ascii=False))

