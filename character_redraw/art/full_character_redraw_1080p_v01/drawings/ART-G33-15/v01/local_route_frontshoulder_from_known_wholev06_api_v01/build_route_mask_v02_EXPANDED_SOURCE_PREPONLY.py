from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib,datetime

P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
initial=json.loads((P/'INPUT_PROVENANCE_INITIAL_PREPONLY.json').read_text(encoding='utf-8'))
target=Path(initial['reference_inputs'][0]['path'])
assert sha(target)=='c03c252b16f6454e20246884d1616d312c93e518c81f105de660f52215ebc5f7'
raw=Image.open(target).convert('RGBA');a=np.array(raw);h,w=a.shape[:2]
assert (w,h)==(957,1644)
# Human trace on the fresh known v06 5x coordinate QA. Covers the wrong red
# bead/root and complete diagonal rear coil/C, including its ink footprint.
old_poly=[(425,288),(444,289),(459,296),(478,299),(504,308),(516,321),(519,335),(531,341),(539,356),(551,360),(565,374),(570,382),(580,390),(586,402),(592,415),(596,433),(594,447),(583,457),(567,459),(553,452),(547,442),(548,429),(550,424),(537,430),(523,432),(506,426),(492,416),(479,404),(470,391),(459,381),(449,365),(442,350),(428,345),(419,340),(420,326),(420,319),(418,309),(420,298)]
old=Image.new('L',(w,h));ImageDraw.Draw(old).polygon(old_poly,fill=255)
old=old.filter(ImageFilter.MaxFilter(7)) # 3px margin to reconstruct old line seams.
oldarr=np.array(old)>0
# New shoulder-FRONT window, on the turned figure's screen-right external
# neck/upper-chest contour. This is INPUT edit capacity, not a painted curl.
front_poly=[(561,329),(579,330),(602,340),(628,360),(656,389),(686,419),(715,454),(724,492),(717,530),(695,560),(668,572),(646,557),(629,531),(622,508),(626,481),(626,456),(614,430),(598,406),(582,382),(570,359)]
front=Image.new('L',(w,h));ImageDraw.Draw(front).polygon(front_poly,fill=255)
candidate=np.array(front)>0
yy,xx=np.mgrid[:h,:w]
# Permit existing transparent/antialiased air and at most a 12px outside
# contour overlap on the black sleeve, for natural hair-over-body occlusion.
# All white frill and all head/skin remain protected outside old footprint.
air=a[:,:,3]<64
visible=a[:,:,3]>=64
rightedge=np.full(h,-1)
for y in range(h):
 pts=np.flatnonzero(visible[y])
 if len(pts):rightedge[y]=pts[-1]
shell=(xx>=rightedge[:,None]-11)&(xx<=rightedge[:,None]+2)&(yy>=410)&(yy<=563)
black=(a[:,:,:3].max(2)<110)
newarr=candidate&(air|(shell&black))
# Preserve original visible face/chin and its outline. This is a technical
# mask correction following the v01 rectangular face-protection assertion;
# all v01 mask and QA outputs remain preserved.
faceprotect=Image.new('L',(w,h))
ImageDraw.Draw(faceprotect).polygon([(516,318),(528,324),(556,323),(566,311),(580,280),(600,280),(600,334),(516,334)],fill=255)
protected_face=np.array(faceprotect)>0
oldarr[protected_face]=False
newarr[protected_face]=False
edit=oldarr|newarr

mask=np.full((h,w,4),255,np.uint8);mask[edit,3]=0
maskpath=P/'mask_V06_OLD_REAR_ROUTE_REMOVE_NEW_FRONT_EXPOSURE_v02.png';Image.fromarray(mask).save(maskpath)
oldpath=P/'QA_OLD_ROUTE_EDIT_REGION_ONLY_NOT_ART_v02.png';old.save(oldpath)
newpath=P/'QA_FRONT_CAPACITY_REGION_ONLY_NOT_ART_v02.png';Image.fromarray(np.where(newarr,255,0).astype(np.uint8)).save(newpath)
roi=(390,280,730,580)
qas=[]
for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 comp=Image.alpha_composite(Image.new('RGBA',raw.size,bg),raw)
 tint=np.zeros((h,w,4),np.uint8)
 tint[oldarr]=[255,40,110,115]
 tint[newarr]=[20,190,245,105]
 over=Image.alpha_composite(comp,Image.fromarray(tint)).convert('RGB')
 out=P/f'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_OVERLAY_FULL_{name}_1x.png';over.save(out);qas.append(dict(path=str(out),sha256=sha(out)))
 out=P/f'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_OVERLAY_ROUTE_{name}_5x.png';over.crop(roi).resize(((roi[2]-roi[0])*5,(roi[3]-roi[1])*5),Image.Resampling.NEAREST).save(out);qas.append(dict(path=str(out),sha256=sha(out)))
alph=Image.fromarray(mask[:,:,3]).crop(roi).resize(((roi[2]-roi[0])*5,(roi[3]-roi[1])*5),Image.Resampling.NEAREST)
out=P/'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_ALPHA_ROUTE_5x.png';alph.save(out);qas.append(dict(path=str(out),sha256=sha(out)))
green=np.zeros((h,w,4),np.uint8);green[~edit]=[40,205,70,45]
protect=Image.alpha_composite(Image.alpha_composite(Image.new('RGBA',raw.size,(255,255,255,255)),raw),Image.fromarray(green)).convert('RGB')
out=P/'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_PROTECTED_HEAD_BODY_FULL_QA.png';protect.save(out);qas.append(dict(path=str(out),sha256=sha(out)))
# Technical invariants only; these do not prove correct artistic routing.
assert not edit[:285].any()
assert not edit[580:].any()
assert not edit[:,:410].any()
assert not edit[:,725:].any()
assert not np.any(edit[protected_face]) # actual visible face/chin protection polygon
assert not np.any(newarr & (~air) & (~(shell&black)))
samples=[]
for name,x,y in [('cap',440,70),('face',545,300),('rear_bob',375,285),('collar_away_from_old',405,365),('left_white_fan',320,420),('right_white_fan_tip',580,370),('right_puff_inside',620,485),('X_cross',420,575),('waist_bow',430,690),('hand_cuff_right',555,650),('skirt',530,1000),('shoe',600,1530),('old_upper_redbead',440,305),('old_diagonal_turn',505,370),('old_C',575,440),('new_front_air',644,389),('new_front_sleeve_edge',645,453)]:
 samples.append(dict(label=name,xy=[x,y],target_rgba=a[y,x].tolist(),mask_alpha=int(mask[y,x,3]),editable=bool(edit[y,x])))
dump(P/'MASK_PROVENANCE_PREPONLY_v02.json',dict(id='ART-G33-15',source_image=str(target),source_sha256=sha(target),prepared_before_future_return=True,mask=str(maskpath),mask_sha256=sha(maskpath),dimensions=[w,h],mode='RGBA',alpha0_editable=True,alpha255_protected=True,editable_pixels=int(edit.sum()),protected_pixels=int((~edit).sum()),old_rear_route_edit_pixels=int(oldarr.sum()),new_front_window_edit_pixels=int(newarr.sum()),old_new_overlap_pixels=int((oldarr&newarr).sum()),editable_target_air_pixels=int((edit&air).sum()),editable_target_opaque_pixels=int((edit&~air).sum()),old_route_polygon_xy=old_poly,old_route_margin_pixels=3,new_front_capacity_polygon_xy=front_poly,new_front_rule='Only transparent/antialiased air plus <=12px external BLACK sleeve boundary; no white frill/head/skin outside necessary old-route cleanup.',protected_body_below_y580=True,nonnecessary_head_cap_face_protected=True,white_frill_outside_old_footprint_protected=True,coordinate_qa_roi=roi,point_checks=samples,qa= qas,mask_build_only_no_art_pixels_changed=True,not_evidence_future_route_will_be_correct=True,root_and_fresh_Sol_required=True,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
print(json.dumps(dict(mask=str(maskpath),sha256=sha(maskpath),editable_pixels=int(edit.sum()),old=int(oldarr.sum()),new=int(newarr.sum()),qa=qas,samples=samples),ensure_ascii=False))
