from pathlib import Path
from PIL import Image
import hashlib, json
from datetime import datetime, timezone
RUN=Path(__file__).resolve().parent
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
lockpath=RUN/'REQUEST_LOCK_PREPONLY.json'
lock=json.loads(lockpath.read_text(encoding='utf-8'))
entries=[value for value in lock.values()if isinstance(value,dict)and'path'in value and'sha256'in value]+lock['refs']
for item in entries:assert h(item['path'])==item['sha256'],item['path']
formal=json.loads(Path(lock['formal']['path']).read_text(encoding='utf-8'))
assert len(formal)==8 and len(formal['InputImages'])==4 and formal['Size']=='960x1648' and formal['Background']=='transparent'
assert Image.open(formal['InputImages'][0]).size==Image.open(formal['MaskFile']).size==(957,1644)
preview=json.loads((RUN/'API_PREVIEW_VALIDATION.json').read_text(encoding='utf-8-sig'))
assert preview['actual_preview']['submitted'] is False and preview['HTTP_calls']==0
for name in ['attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png','api_response.raw.json']:assert not(RUN/name).exists(),name
meta=json.loads((RUN/'MASK_PROVENANCE_PREPONLY_v02.json').read_text(encoding='utf-8'))
assert meta['alpha0_edit_pixels']==12791 and meta['other_alpha_pixels']==0
assert all(p['mask_alpha']==255 for p in meta['protection_samples'].values())
proof={'id':'ART-G33-17','status':'DRAFT_READY_WITHOUT_SUBMIT','verified_utc':datetime.now(timezone.utc).isoformat(),'PREPONLY':True,'root_release_received':False,'request_sha256':lock['request']['sha256'],'formal_sha256':lock['formal']['sha256'],'prompt_sha256':lock['prompt']['sha256'],'mask_sha256':lock['mask']['sha256'],'lock_sha256':h(lockpath),'preview_sha256':h(RUN/'API_PREVIEW_VALIDATION.json'),'handoff_sha256':h(RUN/'ARTIST_HANDOFF_PREPONLY.json'),'four_refs_hashes_match':True,'mask_input_dimensions_match':[957,1644],'output_size':'960x1648','edit_pixel_count':12791,'protected_pixel_count':1560517,'edit_bbox_xyxy':meta['actual_edit_bbox_xyxy'],'outside_mask_alpha255':True,'source_target_original_bytes_retained':True,'mandatory_future_whole_not_dispatchable':True,'all_generation_execution_artifacts_absent':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'technical_verification_not_artistic_pass':True,'central_changes':False}
p=RUN/'FINAL_PREP_COMPLETION.json';assert not p.exists();p.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(proof,ensure_ascii=False,indent=2))
