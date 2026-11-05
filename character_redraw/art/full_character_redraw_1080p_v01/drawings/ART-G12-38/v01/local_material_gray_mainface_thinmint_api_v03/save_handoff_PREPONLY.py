from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):return {'path':str(p),'sha256':sha(p)}
lp=RUN/'REQUEST_LOCK_PREPONLY.json';lock=load(lp);req=load(lock['formal']['path']);preview=load(RUN/'API_PREVIEW_VALIDATION.json')
for k in ['formal','prompt','mask','mask_provenance','provenance','review','actual_view_list','history','scope','auth','provider','provider_configuration','Sol170','local_repair_status','future_whole_draft']:
 assert sha(lock[k]['path'])==lock[k]['sha256'],k
for r in lock['refs']:assert sha(r['path'])==r['sha256']
assert len(req)==8 and len(req['InputImages'])==2 and req['Size']=='1120x1392' and req['Quality']=='high' and req['Background']=='transparent'
assert preview['actual_preview']['submitted'] is False
assert not any((RUN/n).exists() for n in ['attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png'])
future=load(lock['future_whole_draft']['path']);assert not future['dispatchable'] and future['reference_sha256'][0] is None
record={'id':'ART-G12-38','status':'PREPONLY_EXACT_KNOWN_V02_MATERIAL_REPAIR_READY_FOR_ROOT_ACTUAL_REVIEW',
 'formal':lock['formal'],'prompt':lock['prompt'],'mask':lock['mask'],'lock':meta(lp),'preview':meta(RUN/'API_PREVIEW_VALIDATION.json'),'exact_preview':preview['actual_preview'],
 'refs':lock['refs'],'source_review':lock['Sol170'],'current_known_saved_raw_sha256':lock['refs'][0]['sha256'],
 'input_mask_size':[1126,1397],'output_size':[1120,1392],'output_size_note':'Near same aspect, whole fit only; no individual art pixel transform or claim of model hard limit.',
 'mask_A0_editable_pixels':2254,'mask_planes':['upper first wrong mint wide front','lowerC wrong mint wide front','separate Cterminal wrong mint wide front'],
 'protected':['central already correct gray and actual opaque returns','existing narrowmint band and2px retained surface rim','ink and1px safety','real air and original alpha below235','lowLEFT/root/beads/BOB','source963 eyes/mouth/cap/palms/cuffs/body/bottomcut'],
 'actual_final_full_overlay_and_coil5x_alpha5x_viewed':[meta(RUN/f'PREP_PRIOR_CANDIDATE_47856091_MATERIAL_MASKv02_{s}.png') for s in ['OVERLAY_FULL_1x','OVERLAY_COIL_5x','ALPHA_COIL_5x']],
 'full_API_and_future_whole_prompts_read_back':True,'no_old_mint_C_or_gloss_detail_in_future_whole_refs':True,
 'future_whole':lock['future_whole_draft'],'future_whole_dispatchable':False,'future_new_local_result_missing':True,
 'mandatory_builtin_whole_and_fresh_root_Sol':True,'PREPONLY':True,'execution_released':False,'API_calls':0,'native_calls':0,'HTTP_calls':0,'central_writes':0,'source_art_pixel_changed':False,
 'historical_inputs_rejections_and_maskv01_preserved':True,'user_accepted':False,'dynamic_validated':False,'recorded_utc':datetime.now(timezone.utc).isoformat()}
p=RUN/'ARTIST_HANDOFF_PREPONLY.json'
if p.exists():raise RuntimeError('preserve prior handoff')
p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':meta(p),'formal':record['formal'],'prompt':record['prompt'],'mask':record['mask'],'lock':record['lock'],'preview':record['preview'],'future_whole':record['future_whole']},ensure_ascii=False,indent=2))
