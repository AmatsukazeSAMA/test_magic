from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
RUN=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=json.loads((RUN/'MASK_PROVENANCE_v01.json').read_text(encoding='utf-8'));target=Path(old['source_image']);im=Image.open(target).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(np.int16);alpha=a[:,:,3];H,W=alpha.shape
editable=np.array(Image.open(old['mask']['path']))[:,:,3]==0
points=[(655,551),(662,554),(670,554),(677,551),(680,548),(681,554),(680,561),(675,566),(668,568),(660,565),(654,561)]
p=Image.new('L',(W,H),0);ImageDraw.Draw(p).polygon(points,fill=255);domain=np.array(p)>0
ink=rgb.max(2)<65;inkprotect=np.array(Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
green=(rgb[:,:,1]-rgb[:,:,0]>=5)&(rgb[:,:,1]-rgb[:,:,2]>=3)&(rgb.mean(2)>=100)&(rgb.mean(2)<=230)
seed=domain&green&(alpha>=235)&~inkprotect;tip=np.array(Image.fromarray((seed*255).astype('uint8')).filter(ImageFilter.MinFilter(5)))>0
newcount=int((tip&~editable).sum());editable|=tip;ma=np.full((H,W,4),255,np.uint8);ma[editable,3]=0
mp=RUN/'mask_WRONG_MINT_UPPER_WIDE_AND_FULL_C_INTERIORS_KEEP_THINMINT_RIMS_v02.png';Image.fromarray(ma).save(mp)
base=Image.new('RGBA',im.size,'white');base.alpha_composite(im);ol=np.zeros((H,W,4),np.uint8);ol[editable]=[245,0,170,150];overlay=Image.alpha_composite(base,Image.fromarray(ol));diag=[]
for label,xy,scale in [('FULL',[0,0,W,H],1),('COIL',[534,369,713,626],5)]:
 q=RUN/f'PREP_PRIOR_CANDIDATE_47856091_MATERIAL_MASKv02_OVERLAY_{label}_{scale}x.png';t=overlay.crop(tuple(xy));t.resize((t.width*scale,t.height*scale),Image.Resampling.NEAREST).save(q)
 diag.append({'path':str(q),'sha256':sha(q),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':xy,'scale':scale,'magenta':'editable wrong green wide face togray','not_art_or_generation_ref':True})
q=RUN/'PREP_PRIOR_CANDIDATE_47856091_MATERIAL_MASKv02_ALPHA_COIL_5x.png';t=Image.fromarray(ma[:,:,3]).crop((534,369,713,626));t.resize((t.width*5,t.height*5),Image.Resampling.NEAREST).save(q)
diag.append({'path':str(q),'sha256':sha(q),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':[534,369,713,626],'scale':5,'black':'editable A0','white':'protected A255','not_art_or_generation_ref':True})
record={**old,'mask':{'path':str(mp),'sha256':sha(mp),'size':[W,H],'mode':'RGBA'},'supersedes_for_submission_only':'MASK_PROVENANCE_v01.json','old_v01_preserved':True,
 'refinement_reason':'Actual5x v01 missed separately visible green wide terminal face inside lowerC; added only its traced interior keeping2px mint rim/ink/air. No artwork edit or generation.',
 'terminal_C_face':{'polygon_xy':points,'newly_editable_pixels':newcount,'keeps2pxmint_material_rim':True},'alpha_counts':{'0':int(editable.sum()),'255':int((~editable).sum())},'overlays':diag,
 'verified_protection_intersections':{'original_alpha_below235_editable':int((editable&(alpha<235)).sum()),'ink_and_1px_rim_editable':int((editable&inkprotect).sum()),'neutral_already_gray_editable':int((editable&~green).sum())}}
assert not any(record['verified_protection_intersections'].values())
(RUN/'MASK_PROVENANCE_v02.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask':record['mask'],'editable':int(editable.sum()),'tip_added':newcount,'checks':record['verified_protection_intersections']},ensure_ascii=False,indent=2))
