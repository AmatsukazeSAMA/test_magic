from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):return {'path':str(p),'sha256':sha(p)}
lock=load(RUN/'REQUEST_LOCK_PREPONLY.json');req=load(lock['formal']['path']);preview=load(RUN/'API_PREVIEW_VALIDATION.json')
for k in ['formal','prompt','mask','mask_provenance','provenance','review','actual_view_list','history','scope','auth','provider','provider_configuration','Sol168','local_repair_status','future_whole_draft']:
 assert sha(lock[k]['path'])==lock[k]['sha256'],k
for rec in lock['refs']:assert sha(rec['path'])==rec['sha256']
assert len(req)==8 and len(req['InputImages'])==4
assert not preview['actual_preview']['submitted']
assert req['Size']=='960x1648' and req['Quality']=='high' and req['Background']=='transparent'
assert not any((RUN/n).exists() for n in ['attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png'])
future=load(lock['future_whole_draft']['path']);assert not future['dispatchable'] and future['reference_sha256'][0] is None
record={'id':'ART-G33-07','status':'PREPONLY_EXACT_V16_MATERIAL_AND_IRIS_PAYLOAD_READY_FOR_ROOT_ACTUAL_REVIEW',
 'formal':meta(Path(lock['formal']['path'])),'prompt':meta(Path(lock['prompt']['path'])),'mask':meta(Path(lock['mask']['path'])),
 'lock':meta(RUN/'REQUEST_LOCK_PREPONLY.json'),'preview':meta(RUN/'API_PREVIEW_VALIDATION.json'),'exact_preview':preview['actual_preview'],
 'refs':lock['refs'],'fresh168':lock['Sol168'],'target_known_saved_v16_sha256':lock['refs'][0]['sha256'],
 'material_GRAY_editable_pixels':8130,'iris_editable_pixels':2152,'total_mask_A0':10282,'mask_input_size':[957,1643],'output_size':[960,1648],
 'actual_viewed_final_overlays':[meta(RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_MASKv02_{n}.png') for n in ['OVERLAY_FULL_1x','OVERLAY_COIL_5x','OVERLAY_EYES_5x','ALPHA_COIL_5x','ALPHA_EYES_5x']],
 'full_API_and_future_whole_prompt_readback_completed':True,
 'key_boundaries':['thinmint/ink/trueair/beads/root/contour/sourcehands protected','full iris interior including lower ring, not pupil-only','geometry/volume/phase/root not redesigned','historical v03/v04 unknown records not retried or overwritten','API return is intermediate; mandatory future builtin whole/fresh root+Sol'],
 'future_whole':lock['future_whole_draft'],'future_whole_dispatchable':False,'future_local_result_missing':True,
 'PREPONLY':True,'execution_authorized_this_record':False,'API_calls':0,'native_calls':0,'HTTP_calls':0,'central_writes':0,'new_art_pixel_changes':False,
 'recorded_utc':datetime.now(timezone.utc).isoformat(),'user_accepted':False,'dynamic_validated':False}
p=RUN/'ARTIST_HANDOFF_PREPONLY.json'
if p.exists():raise RuntimeError('preserve prior handoff')
p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':meta(p),'formal':record['formal'],'prompt':record['prompt'],'mask':record['mask'],'lock':record['lock'],'preview':record['preview'],'future_whole':record['future_whole']},ensure_ascii=False,indent=2))
