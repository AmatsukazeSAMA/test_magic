from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import json,hashlib
B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':sha(p)}
specs=[('ART-G12-51',[
 ('RETURN_EAR_LOW_ROOT_FULL_COIL',[463,302,646,596],[1,3]),
 ('RETURN_FULL_CONTINUOUS_SPIRAL',[493,360,618,585],[1,3]),
 ('RETURN_EYES_NEUTRAL_DOT_MOUTH',[310,230,546,376],[2]),
 ('RETURN_HIGH_OK_LOOP_THREE_FINGERS',[67,168,220,342],[3]),
 ('RETURN_LOW_CROSSBOW_DROOP_HAND',[208,512,417,619],[3]),
 ('RETURN_CAP_TWO_BLACK_LEAVES',[294,52,655,205],[2])]),
 ('ART-G33-14',[
 ('RETURN_BACK_HEAD_LOW_LEFT_ROOT_FULL_COIL',[131,68,359,349],[1,3]),
 ('RETURN_FULL_CONTINUOUS_SPIRAL',[158,192,244,345],[1,3]),
 ('RETURN_CAP_TWO_LEAVES_WRONG_SCREEN_RIGHT',[140,31,365,142],[2]),
 ('RETURN_WAIST_BACK_HAND_CONTACT',[274,411,432,511],[3]),
 ('RETURN_LOWER_FOLDED_HAND',[56,521,134,632],[3]),
 ('RETURN_COMPLETE_VISIBLE_LEGS_SOURCE_TOE_CROP',[144,904,424,1216],[2])])]
for ident,spec in specs:
 cel=B/'drawings'/ident/'v01';out=cel/'artist_return_diagnostics_v01';out.mkdir(exist_ok=True);rows=[]
 for label,box,scales in spec:
  for color in ['white','black']:
   src=cel/f'qa_{color}.png';im=Image.open(src).crop(box)
   for scale in scales:
    p=out/f'{label}_{color}_{scale}x.png';assert not p.exists();im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).save(p)
    rows.append({**ev(p),'source':ev(src),'crop_xyxy':box,'uniform_diagnostic_scale':scale,'art_pixels_not_modified':True})
 proof={'id':ident,'created_utc':datetime.now(timezone.utc).isoformat(),'raw':ev(cel/'character_api_original.png'),'diagnostics':rows,'purpose':'readonly visual QA crops and nearest neighbor enlargement; no finalart changes','API_calls_this_script':0,'native_calls_this_script':0,'central_write':False}
 p=out/'DIAGNOSTIC_PROVENANCE.json';assert not p.exists();p.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'id':ident,'diagnostic_provenance':ev(p),'count':len(rows)},ensure_ascii=False))
