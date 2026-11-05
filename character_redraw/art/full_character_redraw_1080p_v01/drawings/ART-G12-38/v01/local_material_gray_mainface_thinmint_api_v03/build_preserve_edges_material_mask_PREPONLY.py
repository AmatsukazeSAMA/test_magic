from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
RUN=Path(__file__).parent;target=RUN/'inputs/ref1_CURRENT38_V02_47856091_COMPLETE_RGBA_TARGET.png'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
im=Image.open(target).convert('RGBA');a=np.array(im);H,W=a.shape[:2];rgb=a[:,:,:3].astype(np.int16);alpha=a[:,:,3]
assert sha(target)=='4785609114b9b57113db98decde0f12909d077b79faf09799221db6ad61c7aa5'
planes={
 'upper_first_wide_front':[(557,472),(562,464),(571,455),(588,442),(608,429),(622,420),(628,416),(633,419),(636,426),(638,431),(636,436),(627,443),(610,456),(593,470),(578,483),(570,489),(565,485),(560,478)],
 'lower_C_wide_front':[(650,507),(658,509),(664,516),(665,521),(659,531),(650,542),(644,552),(642,562),(645,570),(652,574),(662,574),(671,570),(677,564),(680,557),(680,551),(683,553),(684,563),(680,575),(672,583),(661,587),(647,587),(635,582),(626,574),(620,564),(620,552),(624,541),(632,530),(641,519)]
}
ink=rgb.max(2)<65;inkprotect=np.array(Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
green=(rgb[:,:,1]-rgb[:,:,0]>=5)&(rgb[:,:,1]-rgb[:,:,2]>=3)&(rgb.mean(2)>=100)&(rgb.mean(2)<=230)
editable=np.zeros((H,W),bool);records=[]
for name,points in planes.items():
 p=Image.new('L',(W,H),0);ImageDraw.Draw(p).polygon(points,fill=255);domain=np.array(p)>0
 seed=domain&green&(alpha>=235)&~inkprotect
 sel=np.array(Image.fromarray((seed*255).astype('uint8')).filter(ImageFilter.MinFilter(5)))>0
 editable|=sel;y,x=np.where(sel)
 records.append({'name':name,'manual_visible_material_polygon_xy':points,'seed_pixels':int(seed.sum()),'editable_pixels':int(sel.sum()),'editable_bbox_xyxy':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'protected_thinmint_rim':'2px erosion inside actual erroneous green wide surface; existing narrow interturn mint outside these surfaces entirely protected'})
ma=np.full((H,W,4),255,np.uint8);ma[editable,3]=0
mp=RUN/'mask_WRONG_MINT_UPPER_WIDE_AND_C_INTERIORS_KEEP_THINMINT_RIMS_v01.png';Image.fromarray(ma).save(mp)
base=Image.new('RGBA',im.size,'white');base.alpha_composite(im);color=np.zeros((H,W,4),np.uint8);color[editable]=[245,0,170,150]
overlay=Image.alpha_composite(base,Image.fromarray(color));diag=[]
for label,xy,scale in [('FULL',[0,0,W,H],1),('COIL',[534,369,713,626],5)]:
 q=RUN/f'PREP_PRIOR_CANDIDATE_47856091_MATERIAL_MASK_OVERLAY_{label}_{scale}x.png';tile=overlay.crop(tuple(xy));tile.resize((tile.width*scale,tile.height*scale),Image.Resampling.NEAREST).save(q)
 diag.append({'path':str(q),'sha256':sha(q),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':xy,'scale':scale,'magenta':'editable wrong-mint wide-material interior to gray','not_art_or_generation_ref':True})
q=RUN/'PREP_PRIOR_CANDIDATE_47856091_MATERIAL_MASK_ALPHA_COIL_5x.png';tile=Image.fromarray(ma[:,:,3]).crop((534,369,713,626));tile.resize((tile.width*5,tile.height*5),Image.Resampling.NEAREST).save(q)
diag.append({'path':str(q),'sha256':sha(q),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':[534,369,713,626],'scale':5,'black':'editable A0','white':'protected A255','not_art_or_generation_ref':True})
checks={'original_alpha_below235_editable':int((editable&(alpha<235)).sum()),'ink_and_1px_rim_editable':int((editable&inkprotect).sum()),'neutral_already_gray_pixels_editable':int((editable&~green).sum()),'outside_coil_material_ROI_editable':int(editable[:369].sum()+editable[626:].sum()+editable[:, :534].sum()+editable[:,713:].sum())}
assert not any(checks.values())
r={'id':'ART-G12-38','source_image':str(target),'source_sha256':sha(target),'mask':{'path':str(mp),'sha256':sha(mp),'mode':'RGBA','size':[W,H]},
 'semantics':'A0 only pigment interior of wrong broad mint upperface/lowerC; A255 protected. Target art never painted.',
 'material_planes':records,'alpha_counts':{'0':int(editable.sum()),'255':int((~editable).sum())},'verified_protection_intersections':checks,
 'gray_correct_central_wide_face_protected':True,'thinmint_route_remains_protected_rim_not_rebuilt_geometry':True,
 'protected_regions':['central correct gray face/returns','existing narrow mint band and2px wideface/C material rim','ink/outline','air and alpha boundary','bob/beads/root','eyes/mouth/face/cap','hands/cuffs/frill/costume and source bottom cutoff'],
 'overlays':diag,'manual_final_5x_review_required':True,'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'mandatory_future_builtin_whole':True,'pixel_statistics_not_art_PASS':True}
(RUN/'MASK_PROVENANCE_v01.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask':r['mask'],'regions':records,'counts':r['alpha_counts'],'checks':checks},ensure_ascii=False,indent=2))
