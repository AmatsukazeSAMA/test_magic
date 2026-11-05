from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
RUN=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
prior=json.loads((RUN/'MASK_PROVENANCE_v01.json').read_text(encoding='utf-8'))
target=Path(prior['source_image']);im=Image.open(target).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(np.int16);alpha=a[:,:,3]
oldmask=np.array(Image.open(prior['mask']['path']).convert('RGBA'))
editable=oldmask[:,:,3]==0;H,W=alpha.shape
gridy=np.arange(H)[:,None];iris=editable&(gridy<300);gray=editable&~iris
cp=[(790,455),(798,450),(806,450),(814,454),(819,460),(821,464),(817,462),(809,458),(800,457),(794,460),(788,464)]
poly=Image.new('L',(W,H),0);ImageDraw.Draw(poly).polygon(cp,fill=255);domain=np.array(poly)>0
neutral=(rgb.max(2)-rgb.min(2)<=13)&(np.abs(rgb[:,:,1]-rgb[:,:,0])<=7)&(np.abs(rgb[:,:,1]-rgb[:,:,2])<=10)
mint=(rgb[:,:,1]-rgb[:,:,0]>7)|(rgb[:,:,1]-rgb[:,:,2]>10)
mintprotect=np.array(Image.fromarray((mint*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
deepink=(rgb.max(2)<55);inkprotect=np.array(Image.fromarray((deepink*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
addition=domain&neutral&(rgb.mean(2)>=75)&(rgb.mean(2)<=215)&(alpha>=235)&~mintprotect&~inkprotect
gray|=addition;editable=gray|iris
ma=np.full((H,W,4),255,dtype=np.uint8);ma[editable,3]=0
mp=RUN/'mask_V16_GRAY_MATERIAL_INTERIORS_AND_WHOLE_IRIS_INTERIORS_v02.png';Image.fromarray(ma).save(mp)
base=Image.new('RGBA',im.size,'white');base.alpha_composite(im)
ol=np.zeros((H,W,4),dtype=np.uint8);ol[gray]=[245,0,170,150];ol[iris]=[0,155,255,160]
overlay=Image.alpha_composite(base,Image.fromarray(ol));records=[]
for label,xy,scale in [('FULL',[0,0,W,H],1),('COIL',[595,290,870,525],5),('EYES',[390,205,620,295],5)]:
 out=RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_MASKv02_OVERLAY_{label}_{scale}x.png';tile=overlay.crop(tuple(xy));tile.resize((tile.width*scale,tile.height*scale),Image.Resampling.NEAREST).save(out)
 records.append({'path':str(out),'sha256':sha(out),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':xy,'scale':scale,'colors':{'magenta':'editable gray pigment','cyan':'editable entire iris'},'not_art_or_generation_ref':True})
for label,xy in [('COIL',[595,290,870,525]),('EYES',[390,205,620,295])]:
 out=RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_MASKv02_ALPHA_{label}_5x.png';tile=Image.fromarray(ma[:,:,3]).crop(tuple(xy));tile.resize((tile.width*5,tile.height*5),Image.Resampling.NEAREST).save(out)
 records.append({'path':str(out),'sha256':sha(out),'source_image':str(target),'source_sha256':sha(target),'prepared_before_future_return':True,'crop_xyxy':xy,'scale':5,'black':'editable A0','white':'protected A255','not_art_or_generation_ref':True})
checks={'transparent_or_alpha_below235_editable':int((editable&(alpha<235)).sum()),'coil_thinmint_plus_rim_editable':int((gray&mintprotect).sum()),'new_C_patch_deepink_plus_rim_editable':int((addition&inkprotect).sum())}
assert not any(checks.values())
record={**prior,'mask':{'path':str(mp),'sha256':sha(mp),'mode':'RGBA','size':[W,H]},'supersedes_for_submission_only':'MASK_PROVENANCE_v01.json',
 'prior_v01_preserved':True,'refinement_reason':'Actualv01 coil5x showed only small central C gray triangle open: allow actual 75..215 neutral gray C interior inside explicit hand-traced gray-only polygon without blanket erosion; still protect mint and deep ink1px. This is input mask refinement, not an artwork edit or generation.',
 'C_gray_interior_refinement':{'polygon_xy':cp,'newly_editable_count':int((addition&~(oldmask[:,:,3]==0)).sum()),'source_gray_RGB_example':[109,106,107],'ink_exclusion':'maxRGB<55 plus1px dilation','mint_exclusion':'same mint classifier plus1px dilation','source_alpha_minimum':235},
 'gray_material':{**prior['gray_material'],'editable_count':int(gray.sum())},'total_editable_count':int(editable.sum()),'protected_count':int((~editable).sum()),'alpha_counts':{'0':int(editable.sum()),'255':int((~editable).sum())},'overlays':records,'verified_protection_intersection_counts_v02':checks,'manual_visual_review_required':True}
(RUN/'MASK_PROVENANCE_v02.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask':record['mask'],'gray_count':int(gray.sum()),'iris_count':int(iris.sum()),'new_C_count':record['C_gray_interior_refinement']['newly_editable_count'],'total':int(editable.sum()),'checks':checks},ensure_ascii=False,indent=2))
