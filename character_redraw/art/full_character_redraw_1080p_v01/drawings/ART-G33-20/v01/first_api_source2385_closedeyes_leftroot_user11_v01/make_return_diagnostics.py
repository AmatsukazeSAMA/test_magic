from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
D=R/'diagnostics'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if p.suffix=='.png':
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
raw=R/'character_api_original.png'
expected='289aabbd6fb2b694adecf550a0fede43e5e8e4fdfe063dd9e95e62f0e750f46e'
assert sha(raw)==expected
im=Image.open(raw).convert('RGBA')
rects={'HEAD_EAR_ROOT_COIL':[248,8,510,355],'ROOT_COIL':[395,180,495,342],'EYES_MOUTH':[295,125,435,204],'SKIRT_GRIP_HAND':[224,482,316,599],'BOTH_SHOES':[155,777,490,1062]}
outputs=[]
for bg in ['white','black']:
 qa=Image.open(R/f'qa_{bg}.png').convert('RGB')
 for tag,box in rects.items():
  crop=qa.crop(box)
  for scale in [1,3]:
   p=D/f'{tag}_{bg}_{scale}x.png';assert not p.exists()
   crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST).save(p)
   outputs.append({**info(p),'source':info(R/f'qa_{bg}.png'),'crop_xyxy':box,'scale':scale,'read_only_diagnostic_not_art':True})
source=Image.open(R/'inputs/ref1_ORIGINAL2385_COMPLETE_UNMASKED_624x1072_GUIDE.png').convert('RGB')
new=Image.open(R/'qa_white.png').convert('RGB')
board=Image.new('RGB',(1264,1104),'white')
board.paste(source,(0,32));board.paste(new,(640,32))
draw=ImageDraw.Draw(board)
draw.text((8,8),'ORIGINAL 2385 GUIDE - body / expression / costume / crop',fill='black')
draw.text((648,8),'G33-20 FIRST API - 1 call - unapproved',fill='black')
p=D/'SOURCE2385_vs_API20_FULL_1x_READONLY.png';assert not p.exists();board.save(p);outputs.append(info(p))
attempt=json.loads((R/'attempt.json').read_text(encoding='utf-8-sig'))
result=json.loads((R/'result.json').read_text(encoding='utf-8-sig'))
hist=im.getchannel('A').histogram()
technical={'id':'ART-G33-20','created_utc':datetime.now(timezone.utc).isoformat(),'provider':result['provider'],'model':result['model'],'quality':result['quality'],'size_requested':result['size'],'size_actual':list(im.size),'mode':im.mode,'raw':info(raw),'elapsed_seconds':result['elapsed_seconds'],'attempt_status':attempt['status'],'http_status':attempt['http_status'],'api_calls':attempt['api_calls'],'automatic_retries':attempt['automatic_retries'],'native_calls':0,'alpha_extrema':im.getchannel('A').getextrema(),'alpha0_pixels':hist[0],'alpha254_pixels':hist[254],'alpha255_pixels':hist[255],'hidden_RGB_not_semantic_foreground':True,'raw_unchanged_after_QA':sha(raw)==expected,'prompt_effective':info(R/'prompt_effective.txt'),'full_white_QA':info(R/'qa_white.png'),'full_black_QA':info(R/'qa_black.png'),'receipts':[info(R/n) for n in ['attempt.json','request_manifest.json','result.json','response_headers.txt','api_response.raw.json']],'source_JOB_and_REGPLAN_unchanged':True,'central_registry_not_modified':True,'technical_success_is_not_art_pass':True,'diagnostics':outputs}
lock=json.loads((R/'REQUEST_LOCK.json').read_text(encoding='utf-8-sig'))
for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
p=R/'TECHNICAL_RETURN_QA.json';assert not p.exists();p.write_text(json.dumps(technical,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'technical':info(p),'raw':info(raw),'actual_size':im.size,'elapsed_seconds':result['elapsed_seconds'],'API_calls':attempt['api_calls'],'alpha0_pixels':hist[0],'alpha254_pixels':hist[254]},ensure_ascii=False,indent=2))
