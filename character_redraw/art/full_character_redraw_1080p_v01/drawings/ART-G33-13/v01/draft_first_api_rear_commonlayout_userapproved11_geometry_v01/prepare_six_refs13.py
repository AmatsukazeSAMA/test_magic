from pathlib import Path
from PIL import Image
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];INP=RUN/'inputs';INP.mkdir(exist_ok=True);QA=RUN/'diagnostics';QA.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def copy(src,name,expected):
    assert sha(src)==expected;dest=INP/name;assert not dest.exists();shutil.copyfile(src,dest)
    return {'source':str(src),'source_sha256':expected,'path':str(dest),'sha256':sha(dest),'operation':'exact bytecopy'}
guide=CEL/'inputs/source_pose_guide.png';src=Image.open(guide).convert('RGBA');assert src.size==(624,1072)
mask=Image.new('L',src.size,255);hide=[167,32,445,248];mask.paste(0,hide)
restores={'narrow_left_profile_lash_face':[212,147,299,245],'original_nape_neck_collar':[264,224,342,274],'right_back_frill_tip':[362,237,411,292]}
for box in restores.values():mask.paste(255,box)
for y in range(hide[1],hide[3]):
    for x in range(hide[0],hide[2]):
        r,g,b,a=src.getpixel((x,y))
        if r>70 and g<90 and b<90 and r>1.6*g and r>1.6*b:mask.putpixel((x,y),0)
selected=Image.new('RGBA',src.size,(0,0,0,0));selected.paste(src,(0,0),mask)
assert all(not mask.getpixel((x,y)) or selected.getpixel((x,y))==src.getpixel((x,y)) for y in range(src.height) for x in range(src.width))
target=INP/'ref1_ORIGINAL2355_COMMON_REAR_PROFILE_FOLDED_HAND_WAIST_HAND_FULL_SKIRT_LEGS_SHOES.png';assert not target.exists();selected.save(target)
mp=INP/'SOURCE13_PIXEL_SELECTION_MASK.png';mask.save(mp)
refs=[{'source':str(guide),'source_sha256':sha(guide),'path':str(target),'sha256':sha(target),'head_hide_xyxy':hide,'restore_rois_xyxy':restores,'mask':evidence(mp),'source_canvas':[624,1072],'trim_transform':{'scale':1,'translation':[0,0],'per_part_transform':False},'operation':'originalpixel selection only; oldredhighhead hidden, source narrowprofile/lash/neck/backbody/allhands/completelegs-shoes unchanged','selectedpixels_equal_original':True}]
motion=BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000040.png';roi=[473,212,57,45]
im=Image.open(motion);hair=im.crop((roi[0],roi[1],roi[0]+roi[2],roi[1]+roi[3]));hp=INP/'ref2_R040_COIL_ONLY_COMPRESSION_NO_BEADS_EAR_FACE_BODY_AUTHORITY.png';hair.save(hp)
refs.append({'source':str(motion),'source_sha256':sha(motion),'path':str(hp),'sha256':sha(hp),'roi_xywh':roi,'operation':'readonly lowerhair compressioncrop; excludes redbeads/ear/face/hands, smallfrillcontext remains','root_side_or_axis_authority':False})
prior=BASE/'drawings/ART-G12-50/v01/draft_first_api_compact_userapproved11_geometry_commonlayout_v01/inputs'
refs.append(copy(prior/'ref3_OLD11_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_NO_COIL.png','ref3_OLD11_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_NO_COIL.png','053477b15810b54c1458a56d912c137a6ee1bdbd8a3904044eb0f95ac1e620a3'))
refs.append(copy(BASE/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref4_USER_APPROVED11_CONTINUOUS_SPIRAL_TAPER_TERMINAL_CURL_GEOMETRY_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'))
refs.append(copy(BASE/'inputs/eye_G02-01_F100.png','ref5_G02_METHOD_ONLY_NO_VISIBLE_IRIS_TO_INVENT.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'))
refs.append(copy(BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
diags=[]
for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
    bg=Image.new('RGBA',selected.size,(*rgb,255));bg.alpha_composite(selected);out=QA/f'SOURCE13_COMMON_{label}_1x.png';bg.convert('RGB').save(out);diags.append(evidence(out))
for label,p,box,factor in [
 ('ORIGINAL13_NARROW_PROFILE_LASH_NECK',guide,[204,137,345,280],4),
 ('SELECTED13_NARROW_PROFILE_LASH_NECK_WHITE',QA/'SOURCE13_COMMON_white_1x.png',[204,137,345,280],4),
 ('ORIGINAL13_FOLDED_HAND',guide,[106,299,184,394],3),
 ('ORIGINAL13_WAIST_HAND_CONTACT',guide,[337,389,411,519],3),
 ('ORIGINAL13_COMPLETE_BOTH_LEGS_SHOES',guide,[190,793,488,1043],2),
 ('R040_COIL_ONLY',hp,[0,0,hair.width,hair.height],4)]:
    crop=Image.open(p).crop(box);dest=QA/f'{label}_{factor}x.png';crop.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST).save(dest)
    diags.append({'path':str(dest),'sha256':sha(dest),'source':str(p),'source_sha256':sha(p),'crop_xyxy':box,'scale':factor})
scope=json.loads((BASE/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'));found=[]
def walk(x):
    if isinstance(x,dict):
        if x.get('id')=='ART-G33-13':found.append(x)
        for v in x.values():walk(v)
    elif isinstance(x,list):
        for v in x:walk(v)
walk(scope);assert len(found)==1
reg=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'));assert not reg.get('ART-G33-13');previous=reg['ART-G33-12'];assert previous['primary_static_pass'] and previous['independent_static_pass']
record={'id':'ART-G33-13','created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'SIX_REFERENCE_PREPARATION_ONLY_NO_SUBMISSION','references':refs,'diagnostics':diags,'priority_scope13':found[0],'previous12_current_reviewed':previous,'source_JOB':evidence(CEL/'JOB.json'),'preexisting_prompt_preserved':evidence(CEL/'prompt.txt'),'API_calls':0,'native_calls':0,'formal_request_or_attempt':False,'central_write':False}
p=RUN/'SOURCE_SIX_REFERENCE_PROVENANCE.json';assert not p.exists();p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':evidence(p),'reference_sha256':[v['sha256'] for v in refs],'previous12_sha256':previous['sha256'],'calls':0},ensure_ascii=False))
