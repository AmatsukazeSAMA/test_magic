from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
RUN=Path(__file__).parent
target=RUN/'inputs/ref1_CURRENT_V16_194d01e1_COMPLETE_RGBA_TARGET.png'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(target)=='194d01e113fb275957c254789857abaf5e8bf25afe2313f900a32f7ce10cac92'
im=Image.open(target).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(np.int16);alpha=a[:,:,3]
H,W=alpha.shape
def polygon(points):
 p=Image.new('L',(W,H),0);ImageDraw.Draw(p).polygon(points,fill=255);return np.array(p)>0
coil_polygon=[(658,315),(706,319),(721,330),(728,350),(742,350),(751,365),(768,372),(785,388),(795,411),(793,434),(820,436),(840,447),(848,467),(847,484),(834,497),(815,500),(797,494),(785,480),(774,473),(752,473),(735,470),(719,464),(708,451),(699,439),(690,434),(676,435),(664,429),(654,411),(644,403),(631,399),(620,389),(611,372),(612,363),(631,358),(648,347),(659,334)]
coil_domain=polygon(coil_polygon)
neutral=(rgb.max(2)-rgb.min(2)<=13)&(np.abs(rgb[:,:,1]-rgb[:,:,0])<=7)&(np.abs(rgb[:,:,1]-rgb[:,:,2])<=10)
mean=rgb.mean(2)
mint=(rgb[:,:,1]-rgb[:,:,0]>7)|(rgb[:,:,1]-rgb[:,:,2]>10)
ink=(rgb.max(2)<75)
protected_mint=np.array(Image.fromarray((mint*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
protected_ink=np.array(Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
gray_seed=coil_domain&neutral&(mean>=80)&(mean<=215)&(alpha>=235)&~protected_mint&~protected_ink
gray=np.array(Image.fromarray((gray_seed*255).astype('uint8')).filter(ImageFilter.MinFilter(3)))>0
iris_polygons={
 'viewer_left':[(451,242),(461,242),(468,247),(472,255),(473,263),(472,271),(468,278),(460,282),(452,282),(445,279),(440,273),(437,264),(439,254),(443,247)],
 'viewer_right':[(555,233),(562,233),(569,238),(573,245),(575,253),(574,260),(571,267),(565,272),(557,274),(549,271),(543,266),(539,258),(540,248),(543,240),(548,235)]
}
iris=np.zeros((H,W),dtype=bool);iris_records=[]
for name,points in iris_polygons.items():
 domain=polygon(points)
 # Protect all white-glint and sclera pixels, including a 1px antialias safety rim.
 light=domain&(rgb.max(2)>=115)
 light_protected=np.array(Image.fromarray((light*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
 selected=domain&(rgb.max(2)<115)&(alpha>=235)&~light_protected
 iris|=selected
 yy,xx=np.where(selected)
 iris_records.append({'name':name,'polygon_xy':points,'editable_count':int(selected.sum()),'editable_bbox_xyxy':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'glint_sclera_and_AA_protection':'maxRGB>=115 inside manual iris polygon dilated 1px; outside polygon protected','includes_black_center_and_entire_lower_gray_ring':True})
editable=gray|iris
mask=Image.new('RGBA',(W,H),(255,255,255,255));ma=np.array(mask);ma[editable,3]=0
mp=RUN/'mask_V16_GRAY_MATERIAL_INTERIORS_AND_WHOLE_IRIS_INTERIORS_v01.png'
if mp.exists():raise RuntimeError('preserve existing mask')
Image.fromarray(ma).save(mp)
def bbox(binary):
 y,x=np.where(binary)
 return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)] if len(x) else None
overlay_records=[]
base=Image.new('RGBA',im.size,'white');base.alpha_composite(im)
ol=np.zeros((H,W,4),dtype=np.uint8);ol[gray]=[245,0,170,150];ol[iris]=[0,155,255,160]
overlay=Image.alpha_composite(base,Image.fromarray(ol))
for label,xy,scale in [('FULL',[0,0,W,H],1),('COIL',[595,290,870,525],5),('EYES',[390,205,620,295],5)]:
 p=RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_MASK_OVERLAY_{label}_{scale}x.png'
 tile=overlay.crop(tuple(xy));tile.resize((tile.width*scale,tile.height*scale),Image.Resampling.NEAREST).save(p)
 overlay_records.append({'path':str(p),'sha256':sha(p),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':xy,'scale':scale,'colors':{'magenta':'editable gray pigment only','cyan':'editable entire iris fill only'},'not_art_or_reference':True})
for label,xy,scale in [('COIL',[595,290,870,525],5),('EYES',[390,205,620,295],5)]:
 p=RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_MASK_ALPHA_{label}_{scale}x.png'
 tile=Image.fromarray(ma[:,:,3]).crop(tuple(xy));tile.resize((tile.width*scale,tile.height*scale),Image.Resampling.NEAREST).save(p)
 overlay_records.append({'path':str(p),'sha256':sha(p),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':xy,'scale':scale,'black':'editable A0','white':'protected A255','not_art_or_reference':True})
protection={'original_alpha_below_235_editable':int((editable&(alpha<235)).sum()),'coil_mint_editable':int((gray&protected_mint).sum()),'coil_ink_safety_editable':int((gray&protected_ink).sum()),'outside_manual_semantic_domains_editable':int((editable&~(coil_domain|polygon(iris_polygons['viewer_left'])|polygon(iris_polygons['viewer_right']))).sum())}
assert not any(protection.values())
record={'id':'ART-G33-07','source_image':str(target),'source_sha256':sha(target),'mask':{'path':str(mp),'sha256':sha(mp),'mode':'RGBA','size':[W,H]},
 'semantics':'mask A0 editable material interiors; A255 protected; target artwork bytes untouched',
 'gray_material':{'manual_semantic_envelope_xy':coil_polygon,'editable_count':int(gray.sum()),'editable_bbox_xyxy':bbox(gray),'alpha_minimum':235,'neutral_RGB_rule':'max-min<=13; abs(G-R)<=7; abs(G-B)<=10; mean80..215; mint/ink1px safety; candidate eroded1px','covers':'visible wide gray fronts/inner-back returns/C inner gray pigment, not geometry or opacity'},
 'iris_material':iris_records,'total_editable_count':int(editable.sum()),'protected_count':int((~editable).sum()),'total_bbox_xyxy':bbox(editable),'alpha_counts':{'0':int((ma[:,:,3]==0).sum()),'255':int((ma[:,:,3]==255).sum())},
 'verified_protection_intersection_counts':protection,'protected_semantic_regions':['thin mint including 1px rim','black hair outline including 1px rim','true air and original alpha<235','bob/root/two red beads outside coil material domains','iris white glints and sclera plus 1px rim','eye lids/lashes/eyebrows and aperture boundary outside manual iris interiors','face/body/cap/hands/costume/shoes and all other pixels'],
 'overlays':overlay_records,'manual_visual_review_required':True,'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'final_art_pixel_changed':False,'mandatory_future_builtin_whole':True,'technical_mask_counts_not_art_acceptance':True}
(RUN/'MASK_PROVENANCE_v01.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask':record['mask'],'gray_count':int(gray.sum()),'iris_records':iris_records,'total':int(editable.sum()),'protection':protection,'overlays':overlay_records},ensure_ascii=False,indent=2))
