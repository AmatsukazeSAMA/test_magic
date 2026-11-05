from pathlib import Path
from PIL import Image
import datetime,hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
cel=B/'drawings/ART-G12-53/v01';run=cel/'draft_first_api_unmasked_source53_user11_graydetail_v01';diag=cel/'artist_return_diagnostics_v01';diag.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def put(p,v):
 with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
d=json.loads((run/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
result=json.loads((cel/'result.json').read_text(encoding='utf-8-sig'));attempt=json.loads((cel/'attempt.json').read_text(encoding='utf-8-sig'))
raw=cel/'character_api_original.png';im=Image.open(raw).convert('RGBA')
assert sha(raw)==result['output_sha256']=='ab16239d402234d97d8f3b2bea6f59423787d939d6079fbca3eebffedc63c551'
assert im.size==(720,992) and attempt['status']=='completed' and str(attempt['http_status'])=='200' and attempt['curl_exit_code']==0
regions={'HEAD_EAR_ROOT_COIL':(111,0,511,588),'WRONG_NEAR_ROOT_COIL':(132,286,254,588),'EYES_MOUTH':(250,183,459,327),'CAP_LEAVES_BLACK_EXTENSIONS':(367,0,484,139),'HIGH_OK_HAND':(558,260,720,479)}
diagnostics=[]
for name,box in regions.items():
 for bg in ['white','black']:
  q=Image.open(cel/f'qa_{bg}.png');z=q.crop(box)
  for factor in [1,3]:
   p=diag/f'{name}_{bg}_{factor}x.png';assert not p.exists();z.resize((z.width*factor,z.height*factor),Image.Resampling.NEAREST).save(p)
   diagnostics.append({**rec(p),'source':rec(cel/f'qa_{bg}.png'),'source_xyxy':box,'zoom':factor,'readonly_diagnostic_not_art_patch':True})
 p=diag/f'{name}_raw_1x.png';assert not p.exists();im.crop(box).save(p);diagnostics.append({**rec(p),'source':rec(raw),'source_xyxy':box,'zoom':1,'readonly_diagnostic_not_art_patch':True})
source=Image.open(d['InputImages'][0]).convert('RGB')
for bg in ['white','black']:
 q=Image.open(cel/f'qa_{bg}.png').convert('RGB');panel=Image.new('RGB',(source.width+q.width,max(source.height,q.height)),(238,238,238));panel.paste(source,(0,0));panel.paste(q,(source.width,0))
 p=diag/f'SOURCE_COMPACT_VS_RETURN_{bg}_SAME_NATIVE_CANVAS.png';assert not p.exists();panel.save(p);diagnostics.append({**rec(p),'sources':[rec(d['InputImages'][0]),rec(cel/f'qa_{bg}.png')],'operation':'readonly side-by-side at original1x, no scaling/part registration','not_art_output':True})
put(diag/'TECHNICAL_RETURN_RECORD.json',{'id':'ART-G12-53','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider':'OpenAI API','model':result['model'],'quality':result['quality'],'raw':{**rec(raw),'actual_dimensions':list(im.size),'mode':Image.open(raw).mode,'alpha_extrema':im.getchannel('A').getextrema(),'alpha_bbox':im.getchannel('A').getbbox()},'result':rec(cel/'result.json'),'attempt_record':rec(cel/'attempt.json'),'attempt_state':attempt,'elapsed_seconds':result['elapsed_seconds'],'n':1,'API_calls':1,'automatic_retries':0,'inflight':0,'raw_response':rec(cel/'api_response.raw.json'),'response_headers':rec(cel/'response_headers.txt'),'execution_receipt':rec(cel/'ARTIST_API_EXECUTION_RECEIPT.json'),'formal_request':rec(cel/'API_PREPARED_REQUEST.json'),'immutable_draft':rec(run/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'inputs':[rec(x) for x in d['InputImages']],'qa':[rec(cel/'qa_white.png'),rec(cel/'qa_black.png')],'diagnostics':diagnostics,'raw_pixels_unchanged':True,'technical_success_not_art_pass':True,'central_registry_or_binding_written':False,'user_accepted':False,'dynamic_validated':False})
print(json.dumps({'id':'ART-G12-53','raw':rec(raw),'size':list(im.size),'seconds':result['elapsed_seconds'],'alpha_extrema':im.getchannel('A').getextrema(),'diagnostics':str(diag),'API_calls':1,'inflight':0},ensure_ascii=False))
