from pathlib import Path
from PIL import Image, ImageFilter
from datetime import datetime, timezone
import hashlib, json, shutil

BASE = Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
FRONT = BASE / 'drawings/ART-G12-48/v01/draft_first_api_userapproved11_geometry_source_commonlayout_v02/inputs/ref3_USER_APPROVED_OLD11_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_COIL_EXCLUDED.png'
BACK = BASE / 'drawings/ART-G33-13/v01/draft_first_api_rear_source_backbob_userapproved11_geometry_v02/inputs/ref3_USER_BACK_BOB_LOW_LEFT_BEADS_OUTLINE_ONLY_NO_COIL_UNIFORM_EYES.png'
GEOMETRY = BASE / 'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png'
KEY = BASE / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
EYE = BASE / 'inputs/eye_G02-01_F100.png'
EXPECTED = {FRONT:'053477b15810b54c1458a56d912c137a6ee1bdbd8a3904044eb0f95ac1e620a3', BACK:'75ded1be4fda0d60e06416874ccafe72cdefb65c7f3e9bdf38cbf23468178561', GEOMETRY:'13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959', KEY:'d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0', EYE:'6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
    p=Path(p); v={'path':str(p),'sha256':sha(p)}
    if p.suffix.lower()=='.png':
        im=Image.open(p);v.update(size=list(im.size),mode=im.mode)
    return v
def write_json(p,v):
    assert not p.exists(),p
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def copyref(src,dst):
    assert sha(src)==EXPECTED[src],src
    assert not dst.exists(),dst
    shutil.copyfile(src,dst)
    return {**ev(dst),'source':ev(src),'operation':'exact byte copy; no art pixel changes'}
def composite(im,rgb):
    out=Image.new('RGBA',im.size,(*rgb,255));out.alpha_composite(im);return out.convert('RGB')
def is_red(rgb):
    r,g,b=rgb[:3];return r>70 and g<90 and b<90 and r>1.6*g and r>1.6*b

for src,wanted in EXPECTED.items(): assert sha(src)==wanted,src
scope=json.loads((BASE/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'))
frame_pts=json.loads((BASE/'inputs/motion_reference_upright_first10_20261031_v01/FRAME_PTS.json').read_text(encoding='utf-8-sig'))['frames']

specs=[dict(id='ART-G12-51',run='draft_first_api_source_commonlayout_locked11_v01',size=(768,992),trim=[16,0,736,992],hide=[210,28,740,420],restores={'face_eyes_neutral_mouth_ear':[330,179,569,418],'neck_collar':[365,399,487,476],'left_shoulder_frill':[257,394,363,476]},cap=[339,66,605,198],leaves=[593,138,680,232],motion=163,roi=[394,239,51,57],identity=FRONT),
       dict(id='ART-G33-14',run='draft_first_api_rear_commonlayout_locked11_v01',size=(624,1072),trim=[64,0,544,1072],hide=[160,37,424,225],restores={'nape_original_neck':[260,192,315,244],'right_shoulder_frill':[326,199,398,274],'left_shoulder_frill':[173,224,249,278]},cap=[216,39,344,104],leaves=[162,42,233,111],motion=43,roi=[341,205,68,40],identity=BACK)]

for s in specs:
    cel=BASE/'drawings'/s['id']/'v01';run=cel/s['run'];inp=run/'inputs';qa=run/'diagnostics'
    inp.mkdir(exist_ok=True);qa.mkdir(exist_ok=True)
    guide=cel/'inputs/source_pose_guide.png';original=Image.open(guide).convert('RGBA');assert original.size==s['size']
    mask=Image.new('L',original.size,255);mask.paste(0,s['hide'])
    for box in s['restores'].values():mask.paste(255,box)
    # Restore original white cap and its existing ink context, not original red hair.
    seed=Image.new('L',original.size,0)
    for y in range(s['cap'][1],s['cap'][3]):
        for x in range(s['cap'][0],s['cap'][2]):
            r,g,b,a=original.getpixel((x,y))
            if min(r,g,b)>225:seed.putpixel((x,y),255)
    cap_context=seed.filter(ImageFilter.MaxFilter(5))
    for y in range(s['hide'][1],s['hide'][3]):
        for x in range(s['hide'][0],s['hide'][2]):
            rgb=original.getpixel((x,y));r,g,b=rgb[:3]
            leaf=s['leaves'][0]<=x<s['leaves'][2] and s['leaves'][1]<=y<s['leaves'][3] and max(r,g,b)<100
            cap=s['cap'][0]<=x<s['cap'][2] and s['cap'][1]<=y<s['cap'][3] and cap_context.getpixel((x,y))
            if cap or leaf:mask.putpixel((x,y),255)
            if is_red(rgb):mask.putpixel((x,y),0)
    # Head removal overlaps a few high thumb/finger pixels in 51: preserve original skin/ink only.
    hand_restore=None
    if s['id']=='ART-G12-51':
        hand_restore=[88,161,240,339];skin=Image.new('L',original.size,0)
        for y in range(hand_restore[1],hand_restore[3]):
            for x in range(hand_restore[0],hand_restore[2]):
                r,g,b,a=original.getpixel((x,y))
                if r>225 and g>170 and b>160:skin.putpixel((x,y),255)
        hand_context=skin.filter(ImageFilter.MaxFilter(5))
        for y in range(hand_restore[1],hand_restore[3]):
            for x in range(hand_restore[0],hand_restore[2]):
                if hand_context.getpixel((x,y)) and not is_red(original.getpixel((x,y))):mask.putpixel((x,y),255)
    selected=Image.new('RGBA',original.size,(0,0,0,0));selected.paste(original,(0,0),mask)
    selected=selected.crop(s['trim']);mask=mask.crop(s['trim']);cropped=original.crop(s['trim'])
    assert all(not mask.getpixel((x,y)) or selected.getpixel((x,y))==cropped.getpixel((x,y)) for y in range(mask.height) for x in range(mask.width))
    sp=inp/('ref1_ORIGINAL1033_COMMON_OPEN_EYES_NEUTRAL_MOUTH_FULL_HANDS_WAIST_APRON.png' if s['id']=='ART-G12-51' else 'ref1_ORIGINAL2362_COMMON_REAR_NO_FACE_FULL_HANDS_SKIRT_LEGS_SOURCE_SHOE_CROP.png')
    assert not sp.exists();selected.save(sp);mp=inp/'ORIGINAL_PIXEL_SELECTION_MASK.png';mask.save(mp)
    motion=BASE/f'inputs/motion_reference_upright_first10_20261031_v01/frames/R{s["motion"]:06d}.png'
    x,y,w,h=s['roi'];hair=Image.open(motion).crop((x,y,x+w,y+h));hp=inp/f'ref2_R{s["motion"]:03d}_COIL_ONLY_MOTION_NO_FACE_ROOT_ACTION.png';hair.save(hp)
    refs=[{**ev(sp),'source':ev(guide),'operation':'source pixels selected at original coordinates; hide old red hair/high roots, retain source cap/2 leaves, restore exact face/neck/hands/body; global trim only','mask':ev(mp)}, {**ev(hp),'source':ev(motion),'crop_xywh':s['roi'],'operation':'readonly hair-motion crop; no face, action or root-position authority'}]
    refs.append(copyref(s['identity'],inp/('ref3_OLD11_BOB_CAP_LOW_BEADS_NO_COIL_IDENTITY_ONLY.png' if s['id']=='ART-G12-51' else 'ref3_BACK_BOB_LOW_LEFT_NAPE_BEADS_NO_COIL_NO_EYES_IDENTITY_ONLY.png')))
    refs.append(copyref(GEOMETRY,inp/'ref4_USER_APPROVED11_CONTINUOUS_SPIRAL_TAPER_TERMINAL_C_ONLY.png'))
    if s['id']=='ART-G12-51':refs.append(copyref(EYE,inp/'ref5_G02_SINGLE_CHARCOAL_EYE_METHOD_ONLY.png'))
    refs.append(copyref(KEY,inp/f'ref{len(refs)+1}_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png'))
    diagnostics=[]
    for i in [0,2,3]:
        im=Image.open(refs[i]['path']).convert('RGBA')
        for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
            out=qa/f'REF{i+1}_{label}_1x.png';composite(im,rgb).save(out);diagnostics.append(ev(out))
            if i in [2,3]:
                out=qa/f'REF{i+1}_{label}_4x.png';composite(im,rgb).resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(out);diagnostics.append(ev(out))
    hpout=qa/f'REF2_R{s["motion"]:03d}_HAIR_ONLY_5x.png';hair.resize((hair.width*5,hair.height*5),Image.Resampling.NEAREST).save(hpout);diagnostics.append(ev(hpout))
    job=json.loads((cel/'JOB.json').read_text(encoding='utf-8-sig'));state=next(v for v in scope['states'] if v['id']==s['id'])
    record={'id':s['id'],'created_utc':datetime.now(timezone.utc).isoformat(),'state':'READONLY_REFERENCE_PREPARATION_NOT_SUBMITTED','references':refs,'guide_size':list(original.size),'compact_canvas':list(selected.size),'guide_crop_xyxy':s['trim'],'transform':{'uniform_scale':1,'translation':[-s['trim'][0],-s['trim'][1]],'per_part_transform':False},'head_hide_xyxy':s['hide'],'original_restore_rois':s['restores'],'source_cap_roi':s['cap'],'source_two_leaves_roi':s['leaves'],'high_hand_restore_roi':hand_restore,'retained_pixels_exact_source_pixels':True,'selection_edges_not_output_cuts':True,'red_fill_exclusion':'only inside original head ROI; R>70,G/B<90,R>1.6G/B; no recoloring. All source body/redbow untouched.','motion_frame_index':s['motion'],'motion_pts':frame_pts[s['motion']]['pts'],'motion_seconds':frame_pts[s['motion']]['pts_time'],'motion_roi_xywh':s['roi'],'scope':state,'JOB':ev(cel/'JOB.json'),'original_full':ev(Path(job['source_image'])),'diagnostics':diagnostics,'correct11_geometry_sha256':EXPECTED[GEOMETRY],'G33_13_49a3_user_rejected_not_used':True,'API_calls':0,'native_calls':0,'formal_API_PREPARED_REQUEST_written':False,'attempt_written':False,'central_write':False}
    out=run/'READONLY_REFERENCE_PROVENANCE.json';write_json(out,record)
    print(json.dumps({'id':s['id'],'provenance':ev(out),'size':list(selected.size),'ref_sha256':[r['sha256'] for r in refs],'calls':0},ensure_ascii=False))
