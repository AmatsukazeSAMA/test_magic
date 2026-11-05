from pathlib import Path
from PIL import Image,ImageFilter
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];OLD=CEL/'draft_first_api_rear_commonlayout_userapproved11_geometry_v01'
INP=RUN/'inputs';INP.mkdir(exist_ok=True);QA=RUN/'diagnostics';QA.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def copy(src,name,expected):
    assert sha(src)==expected;dest=INP/name;assert not dest.exists();shutil.copyfile(src,dest)
    return {'source':str(src),'source_sha256':expected,'path':str(dest),'sha256':sha(dest),'operation':'exact bytecopy'}
oldprov=json.loads((OLD/'SOURCE_SIX_REFERENCE_PROVENANCE.json').read_text(encoding='utf-8'))
original=Image.open(CEL/'inputs/source_pose_guide.png').convert('RGBA');selected=Image.open(oldprov['references'][0]['path']).convert('RGBA')
mask=Image.open(OLD/'inputs/SOURCE13_PIXEL_SELECTION_MASK.png').convert('L')
capbox=[228,36,350,117];whiteseed=Image.new('L',original.size,0)
for y in range(capbox[1],capbox[3]):
    for x in range(capbox[0],capbox[2]):
        r,g,b,a=original.getpixel((x,y))
        if r>225 and g>225 and b>225:whiteseed.putpixel((x,y),255)
capcontext=whiteseed.filter(ImageFilter.MaxFilter(5))
leafbox=[266,36,317,115];cap_restored=0
for y in range(capbox[1],capbox[3]):
    for x in range(capbox[0],capbox[2]):
        r,g,b,a=original.getpixel((x,y));oldred=r>70 and g<90 and b<90 and r>1.6*g and r>1.6*b
        leaf=leafbox[0]<=x<leafbox[2] and leafbox[1]<=y<leafbox[3] and max(r,g,b)<100
        if (capcontext.getpixel((x,y)) or leaf) and not oldred:
            selected.putpixel((x,y),original.getpixel((x,y)));mask.putpixel((x,y),255);cap_restored+=1
sp=INP/'ref1_ORIGINAL2355_COMMON_REAR_CLOSED_LASH_SOURCE_CAP_FULL_BODY_HANDS_LEGS_SHOES.png';assert not sp.exists();selected.save(sp)
mp=INP/'SOURCE13_BACKBOB_VERSION_PIXEL_SELECTION_MASK.png';mask.save(mp)
assert all(not mask.getpixel((x,y)) or selected.getpixel((x,y))==original.getpixel((x,y)) for y in range(original.height) for x in range(original.width))
refs=[{'source':str(CEL/'inputs/source_pose_guide.png'),'source_sha256':sha(CEL/'inputs/source_pose_guide.png'),'path':str(sp),'sha256':sha(sp),'operation':'previousreadonly originalcommonlayout plus exactoriginalcap/2leaf pixelrestoration atoriginalcoordinates, no newpainting','previous_source_selection_provenance':evidence(OLD/'SOURCE_SIX_REFERENCE_PROVENANCE.json'),'cap_roi_xyxy':capbox,'cap_white_selection':'RGB>225 in capROI,MaxFilter5=2pxoutlinecontext; excludeoldredfill','black_two_leaves_roi_xyxy':leafbox,'leaf_selection':'RGBmax<100 in tightleafROI, oldredfill excluded','restored_cap_context_pixels':cap_restored,'mask':evidence(mp),'selected_visible_pixels_equal_original':True,'source_canvas':[624,1072],'trim_transform':{'scale':1,'translation':[0,0],'per_part_transform':False}}]
refs.append(copy(Path(oldprov['references'][1]['path']),'ref2_R040_COIL_ONLY_COMPRESSION_NO_BEADS_EAR_HEAD.png','930e4e61ab265191dc5d66f35671f99a24b6756c1b2d73e605d9c871eb8192a7'))
backsrc=BASE/'inputs/user_hair_side_back.png';assert sha(backsrc)=='09b06d5a4fbd42c7de48f2dc0fa3f2d82c94707bc7f3c71eb73088b7d974a675'
back=Image.open(backsrc).convert('RGBA');box=[222,10,356,134];crop=back.crop(box);backmask=Image.new('L',crop.size,255)
redseed=Image.new('L',back.size,0)
for y in range(112,134):
    for x in range(232,273):
        r,g,b,a=back.getpixel((x,y))
        if r>65 and r>1.3*g and r>1.3*b:redseed.putpixel((x,y),255)
beads=redseed.filter(ImageFilter.MaxFilter(3));coilhide=[228,127,274,134]
for y in range(coilhide[1],coilhide[3]):
    for x in range(coilhide[0],coilhide[2]):
        if not beads.getpixel((x,y)):
            crop.putpixel((x-box[0],y-box[1]),(0,0,0,0));backmask.putpixel((x-box[0],y-box[1]),0)
bp=INP/'ref3_USER_BACK_BOB_LOW_LEFT_BEADS_OUTLINE_ONLY_NO_COIL_UNIFORM_EYES.png';crop.save(bp)
bmp=INP/'BACK_BOB_COIL_EXCLUSION_MASK.png';backmask.save(bmp)
refs.append({'source':str(backsrc),'source_sha256':sha(backsrc),'path':str(bp),'sha256':sha(bp),'crop_xyxy':box,'coil_hide_source_xyxy':coilhide,'bead_keep_rule':'originalredpixels R>65,R>1.3G/B within[232,112,273,134], plus1pxoutlinecontext onlywherecoilhideintersects','mask':evidence(bmp),'operation':'readonly crop/coil exclusion only; retainedsourcepixels unchanged; no recolor','role':'backbob haircut/backhead-low-nape silhouette and anatomicalLEFT lowbeads only; no polishedlighting/mint/coil/clothes/pose ownership'})
refs.append(copy(BASE/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref4_USER_APPROVED11_CONTINUOUS_SPIRAL_TAPER_TERMINAL_CURL_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'))
refs.append(copy(BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref5_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
diags=[]
for i in [0,2]:
    rgba=Image.open(refs[i]['path']).convert('RGBA')
    for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
        bg=Image.new('RGBA',rgba.size,(*rgb,255));bg.alpha_composite(rgba);out=QA/f'REF{i+1}_{label}_1x.png';bg.convert('RGB').save(out);diags.append(evidence(out))
        if i==2:
            out=QA/f'REF3_{label}_4x.png';bg.convert('RGB').resize((rgba.width*4,rgba.height*4),Image.Resampling.NEAREST).save(out);diags.append(evidence(out))
record={'id':'ART-G33-13','created_at_utc':datetime.now(timezone.utc).isoformat(),'state':'FIVE_REFERENCE_BACK_BOB_PREPARATION_ONLY_NOT_SUBMITTED','references':refs,'diagnostics':diags,'G02_omitted_source_iris_unobservable':True,'oldfront_G02_preparation_preserved':str(OLD),'oldsource_diagnostics_and_scope':evidence(OLD/'SOURCE_SIX_REFERENCE_PROVENANCE.json'),'API_calls':0,'native_calls':0,'central_write':False}
p=RUN/'FIVE_REFERENCE_PROVENANCE.json';assert not p.exists();p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':evidence(p),'reference_sha256':[v['sha256'] for v in refs],'calls':0},ensure_ascii=False))
