from pathlib import Path
from PIL import Image
import json,hashlib,shutil
from datetime import datetime,timezone

RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3]
INP=RUN/'inputs';INP.mkdir(exist_ok=True);QA=RUN/'diagnostics';QA.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def copy(src,name,expected):
    assert sha(src)==expected,(src,sha(src));dst=INP/name
    if dst.exists():raise FileExistsError(dst)
    shutil.copyfile(src,dst)
    return {'source':str(src),'source_sha256':sha(src),'path':str(dst),'sha256':sha(dst),'operation':'exact byte copy'}
guide=CEL/'inputs/source_pose_guide.png'
assert sha(guide)=='59128fe827964b3cfa77a73e8afc77f32fa7b693b07c9a4a2d4c02a73b2243e9'
source=Image.open(guide).convert('RGBA'); assert source.size==(800,1040)
mask=Image.new('L',source.size,255)
hide=[220,40,780,425];mask.paste(0,hide)
restores={
 'face_openeyes_tinyO':[280,184,535,405],
 'left_white_shoulderfrill_outline':[200,360,316,447],
 'neck_warmshadow_standingcollar':[334,388,423,445],
 'right_shoulder_frill_top':[412,416,494,567]}
for box in restores.values():mask.paste(255,box)
removed_redfill=0
for y in range(40,425):
    for x in range(220,780):
        r,g,b,a=source.getpixel((x,y))
        if r>70 and g<90 and b<90 and r>1.6*g and r>1.6*b and mask.getpixel((x,y)):
            mask.putpixel((x,y),0);removed_redfill+=1
selected=Image.new('RGBA',source.size,(0,0,0,0));selected.paste(source,(0,0),mask)
trim=[16,0,672,1040];common=selected.crop(trim);commonmask=mask.crop(trim)
target=INP/'ref1_ORIGINAL49_COMPACT_COMMON_OPEN_EYES_TINY_O_DISTINCT_LOW_LEFT_HANDS_BODY_APRON.png'
assert not target.exists();common.save(target)
maskpath=INP/'SOURCE49_COMMON_LAYOUT_PIXEL_SELECTION_MASK.png';commonmask.save(maskpath)
visible_equal=True
cropped_source=source.crop(trim)
for y in range(common.height):
    for x in range(common.width):
        if commonmask.getpixel((x,y)) and common.getpixel((x,y))!=cropped_source.getpixel((x,y)):visible_equal=False
assert visible_equal
refs=[{'source':str(guide),'source_sha256':sha(guide),'path':str(target),'sha256':sha(target),'operation':'sourcepixel selection at unchanged guidecoordinates, then wholecanvas16px-left compactcrop only','source_size':[800,1040],'source_head_hide_roi_xyxy':hide,'restore_rois_xyxy':restores,'oldred_fill_exclusion':'Only within hideROI y<425: R>70,G<90,B<90,R>1.6G,R>1.6B; warmneckshadow remains, redbow below425 untouched. No recolor/new drawing.','oldred_selected_fill_pixels_removed':removed_redfill,'compact_crop_xyxy':trim,'output_size':list(common.size),'trim_transform':{'scale':1,'translation':[-16,0],'per_part_transform':False},'selected_pixels_equal_original':visible_equal,'mask':evidence(maskpath)}]
motion=BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000152.png'
assert sha(motion)=='65e502166fbe2a222ae698bd7e82b335cad508a47faf832acfaa72dd3905fe2a'
roi=[438,207,53,82];im=Image.open(motion);hair=im.crop((roi[0],roi[1],roi[0]+roi[2],roi[1]+roi[3]))
hp=INP/'ref2_R152_HAIR_ONLY_SWAY_COMPRESSION_NOT_GEOMETRY.png';hair.save(hp)
refs.append({'source':str(motion),'source_sha256':sha(motion),'path':str(hp),'sha256':sha(hp),'operation':'read-only haircrop','roi_xywh':roi,'no_eyes_or_hands':True,'motion_only_not_geometry':True})
prior=BASE/'drawings/ART-G12-48/v01/draft_first_api_userapproved11_geometry_source_commonlayout_v02/inputs'
refs.append(copy(prior/'ref3_USER_APPROVED_OLD11_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_COIL_EXCLUDED.png','ref3_OLD11_GRAY_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_NO_COIL.png','053477b15810b54c1458a56d912c137a6ee1bdbd8a3904044eb0f95ac1e620a3'))
refs.append(copy(BASE/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref4_USER_APPROVED_OLD11_LINKED_SPIRAL_TAPER_TERMINAL_CURL_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'))
refs.append(copy(BASE/'inputs/eye_G02-01_F100.png','ref5_G02_SINGLE_CHARCOAL_IRIS_METHOD_ONLY.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'))
refs.append(copy(BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
diagnostics=[]
for i in [0,2,3]:
    rgba=Image.open(refs[i]['path']).convert('RGBA')
    for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
        bg=Image.new('RGBA',rgba.size,(*rgb,255));bg.alpha_composite(rgba);out=QA/f'REF{i+1}_{label}_1x.png';bg.convert('RGB').save(out);diagnostics.append(evidence(out))
for name,src,box,factor in [
 ('SOURCE49_FACE_HANDS',guide,[30,180,560,610],2),
 ('SELECTED49_FACE_HANDS_WHITE',QA/'REF1_white_1x.png',[14,180,544,610],2),
 ('R152_HAIR_ONLY',hp,[0,0,hair.width,hair.height],4),
 ('OLD11_NO_COIL_IDENTITY_WHITE',QA/'REF3_white_1x.png',[0,0,255,210],3),
 ('USER_APPROVED11_COIL_WHITE',QA/'REF4_white_1x.png',[0,0,77,154],3)]:
    cr=Image.open(src).crop(box);out=QA/f'{name}_{factor}x.png';cr.resize((cr.width*factor,cr.height*factor),Image.Resampling.NEAREST).save(out)
    diagnostics.append({'path':str(out),'sha256':sha(out),'source':str(src),'source_sha256':sha(src),'crop_xyxy':box,'scale':factor})
scope=json.loads((BASE/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
entries=[]
def walk(v):
    if isinstance(v,dict):
        if v.get('id')=='ART-G12-49':entries.append(v)
        for z in v.values():walk(z)
    elif isinstance(v,list):
        for z in v:walk(z)
walk(scope);assert len(entries)==1
record={'id':'ART-G12-49','created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_SIX_REFERENCE_PREP_ONLY_NOT_SUBMITTED','references':refs,'diagnostics':diagnostics,'priority_scope49':entries[0],'job':evidence(CEL/'JOB.json'),'source_canonical_image':evidence(Path(json.loads((CEL/'JOB.json').read_text(encoding='utf-8'))['source_image'])),'identity_selection_provenance':evidence(prior.parent/'SIX_REFERENCE_PROVENANCE.json'),'api_calls':0,'native_calls':0,'formal_attempt_written':False,'central_write':False}
dest=RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json';assert not dest.exists();dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':evidence(dest),'source_size':list(common.size),'reference_sha256':[v['sha256'] for v in refs]},ensure_ascii=False))
