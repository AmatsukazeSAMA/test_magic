from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");O=Path(__file__).resolve().parent
S=B/"drawings/ART-X01-12/v01/whole_imggen_user_wrongside_sourceOnly_farLEFT_v01/character_imggen_original.png"
N=B/"drawings/ART-X01-12/v01/py_post_pass_two_gray_wide_lower_arc_v01/character_eye_gray_local.png"
SP=B/"review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_12_MASK_PREP_v01/X01_12_FULL_IRIS_SPEC_ROOT_APPROVED_v01.json"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(S)=="0ce8713d7b22594ec12c3998bc15d89b03462ecd5b2585bd5df6d7d6c163c9b5" and sha(N)=="ca5fc6bd168207c87ef292e2c9ba46eb63efbc245b4b63f245b337386e179b43"
assert sha(SP)=="6b2564aa7aaff44bc0afea8cf9a17dad0634a1d2d1208ef1b98f8e6e7a38575c"
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
 round_low=np.maximum(0,np.max((actual.astype(float)-.5-dark)/(light-dark),axis=1));round_high=np.minimum(1,np.min((actual.astype(float)+.5-dark)/(light-dark),axis=1));bad_common_rounding=round_low>round_high+1e-12
 delta=np.abs(actual.astype(int)-expected.astype(int));colors,counts=np.unique(actual,axis=0,return_counts=True)
 core_dark=int(np.all(actual==dark,axis=1).sum());core_light=int(np.all(actual==light,axis=1).sum())
 bbox=(int(xx.min())-10,int(yy.min())-10,int(xx.max())+11,int(yy.max())+11);x0,y0,x1,y1=bbox
 overlay=wa.copy();overlay[m]=(255,0,255);overlay[g]=(0,230,255)
 strips=[wa[y0:y1,x0:x1],wn[y0:y1,x0:x1],overlay[y0:y1,x0:x1]];pair=np.concatenate(strips,axis=1)
 Image.fromarray(pair).save(O/f'{eye["name"]}_ORIGINAL_CURRENT_MASK_native_1x.png')
 Image.fromarray(pair).resize((pair.shape[1]*8,pair.shape[0]*8),Image.Resampling.NEAREST).save(O/f'{eye["name"]}_ORIGINAL_CURRENT_MASK_8x.png')
 item={"name":eye["name"],"allowed_pixels":int(m.sum()),"protected_glint_pixels":int(g.sum()),"changed_pixels_inside":int(np.any(n[m]!=a[m],axis=1).sum()),"inside_alpha_changed":int((n[m,3]!=a[m,3]).sum()),"outside_gray_interval_pixels":int(outside_interval.sum()),"near_black_RGB_max_le5_pixels":int((actual.max(axis=1)<=5).sum()),"inconsistent_common_rounding_coverage_pixels":int(bad_common_rounding.sum()),"legal_115_113_112_pixels":int(np.all(actual==[115,113,112],axis=1).sum()),"core_dark":core_dark,"core_light":core_light,"transition_pixels":int(m.sum())-core_dark-core_light,"independent_cap_formula_mismatched_pixels":int(np.any(delta,axis=1).sum()),"independent_cap_formula_max_channel_difference":int(delta.max()),"geometry":{"center_xy":eye["center_xy"],"down_unit_xy":eye["down_unit_xy"],"light_cap":eye["light_cap"],"transition_width":eye["light_transition_width_px"]},"unique_RGB_values_with_counts":[{"rgb":[int(x) for x in c],"count":int(k)} for c,k in zip(colors,counts)],"diagnostic_roi_xyxy":bbox}
 items.append(item)
changed=np.any(a!=n,axis=2);audit={"method":"Independent NumPy decoded full RGBA comparison and manual reconstruction from declarative per-eye ellipse/axis/1.5px specification. Each AA color independently checked for one shared coverage interval whose three rounded channels equal its RGB, without red-only projection. No project apply/validator imported; VERIFICATION counts not reused.","source":{"path":str(S),"sha256":sha(S)},"output":{"path":str(N),"sha256":sha(N)},"spec":{"path":str(SP),"sha256":sha(SP)},"dimensions":[957,1644],"allowed_total":int(allowed.sum()),"protected_glints_total":int(glints.sum()),"changed_total":int(changed.sum()),"outside_allowed_RGBA_changed_pixels":int((changed&~allowed).sum()),"whole_alpha_changed_pixels":int((a[:,:,3]!=n[:,:,3]).sum()),"protected_glint_RGBA_changed_pixels":int((changed&glints).sum()),"eyes":items,"art_pixels_written":False,"generation_calls":0,"central_writes":False}
(O/"INDEPENDENT_PIXEL_AUDIT.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in audit.items() if k!="eyes"},ensure_ascii=False));print(json.dumps([{k:v for k,v in x.items() if k not in ["unique_RGB_values_with_counts","geometry"]} for x in items],ensure_ascii=False))
