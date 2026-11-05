from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");O=Path(__file__).resolve().parent
S=B/"drawings/ART-G33-43/v01/whole_imggen_sourceOnlyBody_frontRootContext_v02/character_imggen_original.png"
N=B/"drawings/ART-G33-43/v01/py_post_pass_two_gray_wide_lower_arc_v01/character_eye_gray_local.png"
SP=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G33_43_MASK_PREP_v02_WIDE_LOWER_CAP/G33_43_FULL_IRIS_SPEC_ROOT_APPROVED_v02.json"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(S)=="1af19847862106bec2ae8aeb75fd2fc1b0baeeadb163b34066fd9f391a9323e4" and sha(N)=="2bd7bf7a500ce786f96d5650189daa8db415c2a6aae4b95a1ab4f08ac95fcafd"
assert sha(SP)=="ef64741788240dd7ebf23cfa6cb9633cb7ad4faff6bee876d0169455b9b14b14"
spec=json.loads(SP.read_text(encoding="utf-8-sig"));a=np.array(Image.open(S).convert("RGBA"));n=np.array(Image.open(N).convert("RGBA"));assert a.shape==n.shape==(1644,957,4)
allowed=np.zeros(a.shape[:2],bool);glints=allowed.copy();items=[];dark=np.array(spec["dark_rgb"],float);light=np.array(spec["light_rgb"],float)
def white(p):
 im=Image.open(p).convert("RGBA");out=Image.new("RGBA",im.size,"white");out.alpha_composite(im);return np.array(out.convert("RGB"))
wa=white(S);wn=white(N)
for eye in spec["eyes"]:
 for key in ["interior_mask","protected_glint_mask"]:assert sha(eye[key]["path"])==eye[key]["sha256"]
 m=np.array(Image.open(eye["interior_mask"]["path"]))==255;g=np.array(Image.open(eye["protected_glint_mask"]["path"]))==255
 assert not (m&g).any() and not (m&allowed).any();allowed|=m;glints|=g
 yy,xx=np.where(m);dx=xx-eye["center_xy"][0];dy=yy-eye["center_xy"][1];ux,uy=eye["down_unit_xy"];across=dx*uy-dy*ux;down=dx*ux+dy*uy
 cx,cy=eye["light_cap"]["center_local_xy"];rx,ry=eye["light_cap"]["radii_xy"];norm=np.sqrt(((across-cx)/rx)**2+((down-cy)/ry)**2);signed=(1-norm)*min(rx,ry);mix=np.clip(.5+signed/eye["light_transition_width_px"],0,1)
 expected=np.rint(dark[None,:]*(1-mix[:,None])+light[None,:]*mix[:,None]).astype(np.uint8);actual=n[m,:3]
 lo=np.minimum(dark,light);hi=np.maximum(dark,light);outside_interval=np.any((actual<lo)|(actual>hi),axis=1)
 delta=np.abs(actual.astype(int)-expected.astype(int));colors,counts=np.unique(actual,axis=0,return_counts=True)
 core_dark=int(np.all(actual==dark,axis=1).sum());core_light=int(np.all(actual==light,axis=1).sum())
 bbox=(int(xx.min())-10,int(yy.min())-10,int(xx.max())+11,int(yy.max())+11);x0,y0,x1,y1=bbox
 overlay=wa.copy();overlay[m]=(255,0,255);overlay[g]=(0,230,255)
 strips=[wa[y0:y1,x0:x1],wn[y0:y1,x0:x1],overlay[y0:y1,x0:x1]];pair=np.concatenate(strips,axis=1)
 Image.fromarray(pair).save(O/f'{eye["name"]}_ORIGINAL_CURRENT_MASK_native_1x.png')
 Image.fromarray(pair).resize((pair.shape[1]*8,pair.shape[0]*8),Image.Resampling.NEAREST).save(O/f'{eye["name"]}_ORIGINAL_CURRENT_MASK_8x.png')
 item={"name":eye["name"],"allowed_pixels":int(m.sum()),"protected_glint_pixels":int(g.sum()),"changed_pixels_inside":int(np.any(n[m]!=a[m],axis=1).sum()),"inside_alpha_changed":int((n[m,3]!=a[m,3]).sum()),"outside_gray_interval_pixels":int(outside_interval.sum()),"near_black_RGB_max_le5_pixels":int((actual.max(axis=1)<=5).sum()),"core_dark":core_dark,"core_light":core_light,"transition_pixels":int(m.sum())-core_dark-core_light,"independent_cap_formula_mismatched_pixels":int(np.any(delta,axis=1).sum()),"independent_cap_formula_max_channel_difference":int(delta.max()),"geometry":{"center_xy":eye["center_xy"],"down_unit_xy":eye["down_unit_xy"],"light_cap":eye["light_cap"],"transition_width":eye["light_transition_width_px"]},"unique_RGB_values_with_counts":[{"rgb":[int(x) for x in c],"count":int(k)} for c,k in zip(colors,counts)],"diagnostic_roi_xyxy":bbox}
 items.append(item)
changed=np.any(a!=n,axis=2);audit={"method":"Independent NumPy decoded full RGBA comparison and manual reconstruction from declarative per-eye ellipse/axis/1.5px specification. No project apply/validator imported; VERIFICATION counts not reused.","source":{"path":str(S),"sha256":sha(S)},"output":{"path":str(N),"sha256":sha(N)},"spec":{"path":str(SP),"sha256":sha(SP)},"dimensions":[957,1644],"allowed_total":int(allowed.sum()),"protected_glints_total":int(glints.sum()),"changed_total":int(changed.sum()),"outside_allowed_RGBA_changed_pixels":int((changed&~allowed).sum()),"whole_alpha_changed_pixels":int((a[:,:,3]!=n[:,:,3]).sum()),"protected_glint_RGBA_changed_pixels":int((changed&glints).sum()),"eyes":items,"art_pixels_written":False,"generation_calls":0,"central_writes":False}
(O/"INDEPENDENT_PIXEL_AUDIT.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in audit.items() if k!="eyes"},ensure_ascii=False));print(json.dumps([{k:v for k,v in x.items() if k not in ["unique_RGB_values_with_counts","geometry"]} for x in items],ensure_ascii=False))
