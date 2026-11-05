from pathlib import Path
from PIL import Image,ImageDraw
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;D=R/'diagnostics';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
raw=R/'character_api_original.png';assert sha(raw)=='b7fc52e64ff4d85947fb7adc1d792107da222354c791ceef68d1b1ae632ae5d9'
rects={'HEAD_CAP_ROOT_COIL':[180,33,434,373],'CAP_V_ATTACHMENT':[214,36,430,133],'ROOT_COIL':[332,199,414,369],'EYES_TINY_O':[225,135,353,228],'HIGH_POINTING_HAND':[53,117,160,219],'LOW_CURLED_HAND':[486,477,593,541],'BOTH_SHOES':[122,817,486,1050]}
items=[]
for bg in ['white','black']:
 im=Image.open(R/f'qa_{bg}.png').convert('RGB')
 for tag,roi in rects.items():
  c=im.crop(roi)
  for z in [1,3]:
   p=D/f'{tag}_{bg}_{z}x.png';c.resize((c.width*z,c.height*z),Image.Resampling.NEAREST).save(p)
   items.append({**rec(p),'source':rec(R/f'qa_{bg}.png'),'source_roi_xyxy':roi,'scale':z,'read_only':True})
s=Image.open(R/'inputs/ref1_ORIGINAL2403_COMPLETE_UNMASKED_GUIDE.png').convert('RGB');n=Image.open(R/'qa_white.png').convert('RGB')
b=Image.new('RGB',(1264,1104),'white');b.paste(s,(0,32));b.paste(n,(640,32));dr=ImageDraw.Draw(b);dr.text((8,8),'Original2403 full guide',fill='black');dr.text((648,8),'G33-24 FIRST API - unapproved',fill='black');p=D/'SOURCE2403_vs_API24_FULL_1x_READONLY.png';b.save(p);items.append(rec(p))
res=json.loads((R/'result.json').read_text(encoding='utf-8-sig'));att=json.loads((R/'attempt.json').read_text(encoding='utf-8-sig'));lock=json.loads((R/'EXECUTION_LOCK_v01.json').read_text(encoding='utf-8-sig'))
for k in ['JOB','REGISTRATION_PLAN','immutable_prep_lock','formal_request']:assert sha(lock[k]['path'])==lock[k]['sha256']
i=Image.open(raw).convert('RGBA');h=i.getchannel('A').histogram()
out={'id':'ART-G33-24','created_utc':datetime.now(timezone.utc).isoformat(),'state':'KNOWN_ONE_FIRST_API_RETURN','raw':rec(raw),'actual_size':list(i.size),'mode':i.mode,'alpha_extrema':i.getchannel('A').getextrema(),'alpha0_pixels':h[0],'alpha254_pixels':h[254],'hidden_RGB_not_semantic_foreground':True,'provider':res['provider'],'model':res['model'],'quality':res['quality'],'elapsed_seconds':res['elapsed_seconds'],'API_calls':att['api_calls'],'automatic_retries':att['automatic_retries'],'native_calls':0,'attempt_status':att['status'],'http_status':att['http_status'],'effective_prompt':rec(R/'prompt_effective.txt'),'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),'original_return_records':[rec(R/f) for f in ['attempt.json','api_response.raw.json','response_headers.txt','result.json','request_manifest.json']],'request_LOCK_JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'technical_success_not_art_acceptance':True,'diagnostics':items}
p=R/'TECHNICAL_RETURN_QA.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'technical':rec(p),'raw':rec(raw),'actual_size':i.size,'API_calls':att['api_calls'],'elapsed_seconds':res['elapsed_seconds']},ensure_ascii=False,indent=2))
