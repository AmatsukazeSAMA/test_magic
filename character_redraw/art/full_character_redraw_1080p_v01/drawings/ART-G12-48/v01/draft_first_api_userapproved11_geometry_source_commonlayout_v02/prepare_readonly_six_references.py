from pathlib import Path
from PIL import Image
import json, hashlib, shutil
from datetime import datetime, timezone

BASE=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
RUN=Path(__file__).parent
INP=RUN/'inputs'; INP.mkdir(exist_ok=True)
QA=RUN/'diagnostics'; QA.mkdir(exist_ok=True)
PREF=BASE/'drawings/ART-G12-48/v01/preflight_source_layout_hair_only_HOLD_v01'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def copy(src,name,expected):
    assert sha(src)==expected,(src,sha(src))
    dst=INP/name
    if dst.exists(): raise FileExistsError(dst)
    shutil.copyfile(src,dst)
    assert sha(dst)==expected
    return {'source':str(src),'source_sha256':expected,'path':str(dst),'sha256':sha(dst),'operation':'exact byte copy'}
refs=[]
refs.append(copy(PREF/'inputs/ORIGINAL48_COMMON_LAYOUT_FACE_BODY_COMPLETE_DISTINCT_HANDS_READONLY.png','ref1_ORIGINAL48_COMMON_LAYOUT_DISTINCT_MOUTH_COVERING_HANDS_BODY_WAIST_APRON.png','d3ebdf0e0893b87867a12d1eca8cf50d5f5cde466f978ef7bd606428a8a5f847'))
refs.append(copy(PREF/'inputs/R146_HAIR_ONLY_READONLY.png','ref2_R146_HAIR_ONLY_MOTION_NOT_GEOMETRY.png','8c3da41df2bf9930304e9a3a609e6c7121d5caed2f7517fd78a36cf686da6987'))
old=BASE/'drawings/ART-G33-11/v01/character_api_original.png'
assert sha(old)=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'
im=Image.open(old).convert('RGBA')
box=[120,65,375,275]
crop=im.crop(box)
hide=[280,255,351,275]
relative=[hide[0]-box[0],hide[1]-box[1],hide[2]-box[0],hide[3]-box[1]]
crop.paste((0,0,0,0),relative)
px=crop.load(); zeroed_hidden=0
for y in range(crop.height):
    for x in range(crop.width):
        if px[x,y][3]==0 and px[x,y][:3]!=(0,0,0):
            px[x,y]=(0,0,0,0);zeroed_hidden+=1
identity=INP/'ref3_USER_APPROVED_OLD11_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_COIL_EXCLUDED.png'
if identity.exists():raise FileExistsError(identity)
crop.save(identity)
src=im.crop(box); mask=Image.new('L',crop.size,255); mask.paste(0,relative)
mask.save(INP/'IDENTITY_COIL_EXCLUSION_MASK.png')
unchanged=True
for y in range(crop.height):
    for x in range(crop.width):
        if mask.getpixel((x,y)) and src.getpixel((x,y))[3]>0 and crop.getpixel((x,y))!=src.getpixel((x,y)):unchanged=False
assert unchanged
refs.append({'source':str(old),'source_sha256':sha(old),'path':str(identity),'sha256':sha(identity),'operation':'readonly identity crop; rectangular coil exclusion; alpha0 RGB zeroed; no paint/transform','crop_xyxy':box,'coil_hide_source_xyxy':hide,'coil_hide_crop_xyxy':relative,'alpha0_hidden_rgb_cleaned_pixel_count':zeroed_hidden,'all_retained_visible_pixels_equal_source':unchanged,'mask':str(INP/'IDENTITY_COIL_EXCLUSION_MASK.png'),'mask_sha256':sha(INP/'IDENTITY_COIL_EXCLUSION_MASK.png')})
refs.append(copy(BASE/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref4_USER_SELECTED_OLD11_CONTINUOUS_SPIRAL_TAPER_TERMINAL_CURL_GEOMETRY_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'))
refs.append(copy(BASE/'inputs/eye_G02-01_F100.png','ref5_G02_SINGLE_CHARCOAL_IRIS_METHOD_NO_HEART_APERTURE_COPY.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'))
refs.append(copy(BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_UNLIT_GRAY_MINT_PIGMENT_KEY_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'))
diagnostics=[]
for i in [0,2,3]:
    rgba=Image.open(refs[i]['path']).convert('RGBA')
    for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
        bg=Image.new('RGBA',rgba.size,(*rgb,255));bg.alpha_composite(rgba)
        dest=QA/f'REF{i+1}_{label}_1x.png';bg.convert('RGB').save(dest)
        diagnostics.append({'path':str(dest),'sha256':sha(dest),'source_reference':i+1,'background':label,'scale':1})
        if i in [2,3]:
            zoom=QA/f'REF{i+1}_{label}_3x.png';bg.convert('RGB').resize((rgba.width*3,rgba.height*3),Image.Resampling.NEAREST).save(zoom)
            diagnostics.append({'path':str(zoom),'sha256':sha(zoom),'source_reference':i+1,'background':label,'scale':3})
record={'id':'ART-G12-48','created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PRIVATE_REFERENCE_PREPARATION_NO_API_OR_NATIVE','references':refs,'diagnostics':diagnostics,'original_source_layout_provenance':{'path':str(PREF/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json'),'sha256':sha(PREF/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json')},'api_calls':0,'native_calls':0,'formal_prepare_or_attempt_written':False,'central_write':False}
dest=RUN/'SIX_REFERENCE_PROVENANCE.json'
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':str(dest),'sha256':sha(dest),'identity_sha256':sha(identity),'reference_sha256':[v['sha256'] for v in refs]},ensure_ascii=False))
