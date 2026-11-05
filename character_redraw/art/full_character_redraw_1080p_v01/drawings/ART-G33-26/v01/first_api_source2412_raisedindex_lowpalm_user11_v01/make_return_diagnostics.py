from pathlib import Path
from PIL import Image,ImageDraw
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;D=R/'diagnostics';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
raw=R/'character_api_original.png';assert sha(raw)=='a8cc6a8c3b170a7ed84a3e5256e3338a55a11fd4d373a24c01f6c1e94607602b'
rects={'HEAD_CAP_ROOT_COIL':[166,30,430,365],'CAP_V_ATTACHMENT':[215,30,428,132],'ROOT_COIL':[304,183,403,357],'EYES_CLOSED_NEUTRAL_MOUTH':[214,117,354,216],'HIGH_RAISED_INDEX_HAND':[40,60,127,188],'LOW_OPEN_PALM':[493,426,615,494],'BOTH_SHOES':[128,810,414,1014]}
items=[]
for bg in ['white','black']:
 im=Image.open(R/f'qa_{bg}.png').convert('RGB')
 for tag,roi in rects.items():
  c=im.crop(roi)
  for z in [1,3]:
   p=D/f'{tag}_{bg}_{z}x.png';c.resize((c.width*z,c.height*z),Image.Resampling.NEAREST).save(p)
   items.append({**rec(p),'source':rec(R/f'qa_{bg}.png'),'source_roi_xyxy':roi,'scale':z,'read_only':True})
s=Image.open(R/'inputs/ref1_ORIGINAL2412_COMPLETE_UNMASKED_GUIDE.png').convert('RGB');n=Image.open(R/'qa_white.png').convert('RGB')
b=Image.new('RGB',(1296,1072),'white');b.paste(s,(0,32));b.paste(n,(656,32));dr=ImageDraw.Draw(b);dr.text((8,8),'Original2412 full guide',fill='black');dr.text((664,8),'G33-26 FIRST API - unapproved',fill='black');p=D/'SOURCE2412_vs_API26_FULL_1x_READONLY.png';b.save(p);items.append(rec(p))
res=json.loads((R/'result.json').read_text(encoding='utf-8-sig'));att=json.loads((R/'attempt.json').read_text(encoding='utf-8-sig'));lock=json.loads((R/'EXECUTION_LOCK_v01.json').read_text(encoding='utf-8-sig'))
for k in ['JOB','REGISTRATION_PLAN','immutable_prep_lock','formal_request']:assert sha(lock[k]['path'])==lock[k]['sha256']
assert res['output_sha256']==sha(raw) and att['api_calls']==1 and att['status']=='completed'
i=Image.open(raw).convert('RGBA');h=i.getchannel('A').histogram()
out={'id':'ART-G33-26','created_utc':datetime.now(timezone.utc).isoformat(),'state':'KNOWN_ONE_FIRST_API_RETURN_APPROVAL_BLOCK_RESOLVED','raw':rec(raw),'actual_size':list(i.size),'mode':i.mode,'alpha_extrema':i.getchannel('A').getextrema(),'alpha0_pixels':h[0],'alpha254_pixels':h[254],'hidden_RGB_not_semantic_foreground':True,'provider':res['provider'],'model':res['model'],'quality':res['quality'],'elapsed_seconds':res['elapsed_seconds'],'usage':res['usage'],'API_calls':att['api_calls'],'automatic_retries':att['automatic_retries'],'native_calls':0,'attempt_status':att['status'],'http_status':att['http_status'],'effective_prompt':rec(R/'prompt_effective.txt'),'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),'original_return_records':[rec(R/f) for f in ['attempt.json','api_response.raw.json','response_headers.txt','result.json','request_manifest.json']],'historical_before_CreateProcess_rejection':rec(R/'KNOWN_UNSENT_AUTO_REVIEW_REJECTION_v01.json'),'root_scope_readback_after_rejection':rec(R/'ROOT_EXISTING_USER_CONSENT_READBACK_AFTER_REJECTION_v01.json'),'same_command_same_payload_then_approved_by_review':True,'historical_zero_sent_handoff_is_not_current_final_status':True,'request_LOCK_JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'technical_success_not_art_acceptance':True,'diagnostics':items}
p=R/'TECHNICAL_RETURN_QA.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'technical':rec(p),'raw':rec(raw),'actual_size':i.size,'API_calls':att['api_calls'],'elapsed_seconds':res['elapsed_seconds']},ensure_ascii=False,indent=2))
