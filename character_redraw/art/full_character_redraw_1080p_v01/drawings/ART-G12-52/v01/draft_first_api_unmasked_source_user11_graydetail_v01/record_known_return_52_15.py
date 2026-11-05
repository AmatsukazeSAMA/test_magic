from pathlib import Path
import datetime, hashlib, json
from PIL import Image

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
ITEMS=[('ART-G12-52','draft_first_api_unmasked_source_user11_graydetail_v01',{'HEAD_EAR_ROOT_COIL':(365,50,805,552),'COIL':(611,335,750,548),'HIGH_HAND':(14,232,218,427),'EYES_MOUTH':(443,252,661,370)}),('ART-G33-15','draft_first_api_rear_threequarter_unmasked_cap_user11_graydetail_v01',{'HEAD_EAR_ROOT_COIL':(100,38,365,368),'COIL':(184,205,261,364),'CAP_LEAVES':(99,34,306,145),'FULL_SHOES':(36,930,432,1176)})]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save_new(p,x):
 with Path(p).open('x',encoding='utf-8') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for cel_id,run_name,regions in ITEMS:
 cel=B/'drawings'/cel_id/'v01';run=cel/run_name
 req=json.loads((run/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
 result=json.loads((cel/'result.json').read_text(encoding='utf-8-sig'))
 attempt=json.loads((cel/'attempt.json').read_text(encoding='utf-8-sig'))
 assert attempt['status']=='completed' and str(attempt['http_status'])=='200' and attempt['curl_exit_code']==0
 raw=cel/'character_api_original.png';assert sha(raw)==result['output_sha256']
 im=Image.open(raw).convert('RGBA');assert f'{im.width}x{im.height}'==req['Size']
 diag=cel/'artist_return_diagnostics_v01';diag.mkdir(exist_ok=True)
 diagnostics=[]
 for name,box in regions.items():
  for bg in ['white','black']:
   qa=Image.open(cel/f'qa_{bg}.png');crop=qa.crop(box)
   for factor in [1,3]:
    p=diag/f'{name}_{bg}_{factor}x.png'
    if not p.exists():crop.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST).save(p)
    diagnostics.append({'path':str(p),'sha256':sha(p),'source':str(cel/f'qa_{bg}.png'),'source_xyxy':box,'zoom':factor})
  p=diag/f'{name}_raw_1x.png'
  if not p.exists():im.crop(box).save(p)
  diagnostics.append({'path':str(p),'sha256':sha(p),'source':str(raw),'source_xyxy':box,'zoom':1})
 tech={'id':cel_id,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw':{'path':str(raw),'sha256':sha(raw),'actual_size':list(im.size),'mode':Image.open(raw).mode,'alpha_extrema':im.getchannel('A').getextrema(),'alpha_bbox':im.getchannel('A').getbbox()},'result':{'path':str(cel/'result.json'),'sha256':sha(cel/'result.json')},'attempt':attempt,'elapsed_seconds':result['elapsed_seconds'],'provider':'OpenAI API','model':result['model'],'quality':result['quality'],'n':result['n'],'source_guide':req['original_guide_preserved'],'immutable_draft':{'path':str(run/'DRAFT_API_REQUEST.json'),'sha256':sha(run/'DRAFT_API_REQUEST.json')},'prompt':{'path':req['PromptFile'],'sha256':sha(req['PromptFile'])},'qa':[{'path':str(cel/f'qa_{bg}.png'),'sha256':sha(cel/f'qa_{bg}.png')} for bg in ['white','black']],'diagnostics':diagnostics,'raw_pixels_unchanged':True,'technical_success_not_art_pass':True,'API_calls':1,'automatic_retries':0,'inflight':0,'central_write':False,'user_accepted':False,'dynamic_validated':False,'photography_validated':False}
 save_new(diag/'TECHNICAL_RETURN_RECORD.json',tech)
 reg=Path(req['REGPLAN_current_preserved']['path'])
 assert sha(reg)==req['REGPLAN_current_preserved']['sha256'],'REGPLAN changed'
 assert sha(req['original_guide_preserved']['path'])==req['original_guide_preserved']['sha256']
 before=reg.read_bytes();old=json.loads(before.decode('utf-8-sig'))
 backup=cel/'REGPLAN_PRE_COMPACT_REFERENCE.json'
 with backup.open('xb') as f:f.write(before)
 backup.with_suffix('.json.sha256').write_text(sha(backup)+'\n',encoding='utf-8')
 new=dict(old);new.update(req['REGPLAN_expected_compact_private_not_applied'])
 reg.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 save_new(cel/'REGPLAN_COMPACT_UPDATE_RECEIPT.json',{'id':cel_id,'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorization':'Parent specific ONE52/ONE15 release permits only source commoncanvas compact coordinate synchronization after known result.','backup':{'path':str(backup),'sha256':sha(backup)},'REGPLAN_after':{'path':str(reg),'sha256':sha(reg),'content':new},'source_guide_unchanged':req['original_guide_preserved'],'JOB_unchanged':req['original_JOB_preserved'],'raw_output_sha256':sha(raw),'only_reference_whole_coordinates_changed':True,'actual_output_registration_not_yet_validated':True,'central_registry_or_binding_changed':False})
 assert sha(raw)==result['output_sha256'] and sha(req['original_JOB_preserved']['path'])==req['original_JOB_preserved']['sha256']
 print(json.dumps({'id':cel_id,'raw_sha256':sha(raw),'size':im.size,'seconds':result['elapsed_seconds'],'alpha_extrema':tech['raw']['alpha_extrema'],'diagnostics':str(diag),'REGPLAN_after_sha256':sha(reg),'backup_sha256':sha(backup),'inflight':0},ensure_ascii=False))
