from pathlib import Path
from PIL import Image,ImageDraw
from datetime import datetime,timezone
import hashlib,json
R=Path(__file__).resolve().parent;D=R/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
raw=R/'character_api_original.png';assert sha(raw)=='612a02647fb0dc55e08a300c1a4bf4ed706bca278d817ce1b588a23dce971e7e'
rects={'HEAD_CAP_ROOT_COIL':[235,10,505,350],'ROOT_COIL':[391,171,491,346],'CAP_TWO_LEAVES':[285,15,488,120],'EYES_MOUTH':[292,111,425,197],'SKIRT_GRIP_HAND':[271,548,351,634],'BOTH_SHOES':[170,800,540,1060]}
outputs=[]
for bg in ['white','black']:
 im=Image.open(R/f'qa_{bg}.png').convert('RGB')
 for tag,box in rects.items():
  c=im.crop(box)
  for scale in [1,3]:
   p=D/f'{tag}_{bg}_{scale}x.png';assert not p.exists();c.resize((c.width*scale,c.height*scale),Image.Resampling.NEAREST).save(p)
   outputs.append({**rec(p),'source':rec(R/f'qa_{bg}.png'),'source_roi_xyxy':box,'scale':scale,'read_only':True})
source=Image.open(R/'inputs/ref1_ORIGINAL2394_COMPLETE_UNMASKED_GUIDE.png').convert('RGB');new=Image.open(R/'qa_white.png').convert('RGB')
board=Image.new('RGB',(1264,1104),'white');board.paste(source,(0,32));board.paste(new,(640,32));dr=ImageDraw.Draw(board);dr.text((8,8),'Original2394 source guide',fill='black');dr.text((648,8),'G33-22 FIRST API - unapproved',fill='black')
p=D/'SOURCE2394_vs_API22_FULL_1x_READONLY.png';assert not p.exists();board.save(p);outputs.append(rec(p))
attempt=json.loads((R/'attempt.json').read_text(encoding='utf-8-sig'));result=json.loads((R/'result.json').read_text(encoding='utf-8-sig'));lock=json.loads((R/'REQUEST_LOCK.json').read_text(encoding='utf-8-sig'))
for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
im=Image.open(raw).convert('RGBA');ah=im.getchannel('A').histogram()
out={'id':'ART-G33-22','created_utc':datetime.now(timezone.utc).isoformat(),'provider':result['provider'],'model':result['model'],'quality':result['quality'],'actual_size':list(im.size),'raw':rec(raw),'mode':'RGBA','alpha_extrema':im.getchannel('A').getextrema(),'alpha0_pixels':ah[0],'alpha254_pixels':ah[254],'hidden_RGB_not_semantic_foreground':True,'API_calls':attempt['api_calls'],'automatic_retries':attempt['automatic_retries'],'native_calls':0,'elapsed_seconds':result['elapsed_seconds'],'attempt_status':attempt['status'],'http_status':attempt['http_status'],'effective_prompt':rec(R/'prompt_effective.txt'),'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),'preserved_receipts':[rec(R/n) for n in ['attempt.json','api_response.raw.json','response_headers.txt','request_manifest.json','result.json']],'source_JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'technical_success_not_art_acceptance':True,'diagnostics':outputs}
p=R/'TECHNICAL_RETURN_QA.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'technical':rec(p),'raw':rec(raw),'actual_size':im.size,'API_calls':attempt['api_calls'],'elapsed_seconds':result['elapsed_seconds']},ensure_ascii=False,indent=2))
