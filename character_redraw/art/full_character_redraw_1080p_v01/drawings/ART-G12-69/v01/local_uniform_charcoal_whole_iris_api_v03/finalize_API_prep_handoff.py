from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent;C=R.parent;B=R.parents[3]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
lp=R/'REQUEST_LOCK_PREPONLY_v02.json';assert sha(lp)=='80a886fb29e5fafb8a224532b106b19aacde6d87d9c5e5fc8bd4fe19fb49aa07'
l=read(lp)
for item in [l[k] for k in ['formal','prompt','mask','provenance','mask_provenance','history','Sol160','scope','auth','provider','provider_configuration','local_repair_status','mask_review']]+l['refs']:
    assert sha(item['path'])==item['sha256'],item['path']
q=read(l['formal']['path']);assert len(q)==8 and q['MaskFile']==l['mask']['path']
assert q['Size']=='1584x992' and q['Quality']=='high' and q['Background']=='transparent'
assert q['InputImages']==[x['path'] for x in l['refs']] and len(q['InputImages'])==4
preview=read(R/'API_PREVIEW_VALIDATION.json');assert preview['actual_preview']['submitted'] is False
assert preview['actual_preview']['mask_provided'] and preview['actual_preview']['n']==1
assert preview['actual_preview']['model']=='gpt-image-2.5-sunburst'
assert not read(R/'LOCAL_REPAIR_STATUS.json')['whole_character_imggen_completed']
prov=read(l['provenance']['path'])
for k in ['source_JOB','source_REGISTRATION_PLAN','source_original']:
    assert sha(prov[k]['path'])==prov[k]['sha256']
raw=Path(q['InputImages'][0]);mask=Image.open(q['MaskFile']).convert('RGBA');im=Image.open(raw).convert('RGBA')
assert mask.size==im.size==(1587,991)
hist=mask.getchannel('A').histogram();assert hist[0]==1679 and hist[255]==1587*991-1679 and sum(hist[1:255])==0
for n in ['attempt.json','result.json','api_response.raw.json','response_headers.txt','prompt_effective.txt','request_manifest.json','character_api_original.png']:
    assert not (R/n).exists(),n
history=read(R/'KNOWN_HISTORY_AND_PARENT_BEFORE.json');assert not history['unknown_results']
assert len(history['known_FIRST'])==len(history['known_native'])==1 and not history['existing_local_ancestors']
validation=put('PREPONLY_TECHNICAL_VALIDATION.json',{
 'id':'ART-G12-69','recorded_utc':datetime.now(timezone.utc).isoformat(),
 'technical_preparation_valid':True,'artistic_pass':False,
 'checks':['eight formal fields including MaskFile exact', 'four ordered refs hash verified and actual viewed',
           'target and RGBA alpha mask exact native1587x991 match', 'mask alpha0 only1679 iris pixels, all remaining pixels alpha255',
           'v02 overlay actual full white/black, both iris10x, blackboth6x, alpha6x viewed',
           'preserve eye whites/lid contours/lashes/glints face and all other pixels in input mask',
           'old known FIRST/native each one, noUNKNOWN or older local ancestor',
           'Sol160 exact current raw hash checked and eye pigment P1 read',
           'official helper MaskFile/Preview read and no-key/no-network Preview returned expected model/high/size/n1',
           'no actual API/native/attempt/HTTP or generated result', 'JOB/REGPLAN/source and old raw bytes unchanged'],
 'latest_lock':rec(lp),'formal_request':l['formal'],'preview':rec(R/'API_PREVIEW_VALIDATION.json'),
 'prior_failed_preview_guard':'Local wrong key-count expectation halted before wrapper; corrected v02 guard preserves original formal bytes. No transport or approval rejection.',
 'input_mask_is_not_patched_final_art':True,'mandatory_builtin_whole_after_future_successful_API':True,
 'future_new_API_and_whole_outputs_require_fresh_actual_review':True,
 'central_registry_exposure_binding_written':False,'API_calls':0,'native_calls':0
})
keydiags=[R/'qa_readonly'/('PREP_PRIOR_CANDIDATE_848f9fc1_'+n) for n in [
 'MASKv02_OVERLAY_FULL_white_READONLY.png','MASKv02_OVERLAY_FULL_black_READONLY.png',
 'MASKv02_OVERLAY_IMAGE_LEFT_IRIS_white_10x_READONLY.png','MASKv02_OVERLAY_IMAGE_RIGHT_IRIS_white_10x_READONLY.png',
 'MASKv02_OVERLAY_BOTH_IRIS_black_6x_READONLY.png','MASKv02_ALPHA_BOTH_IRIS_6x_READONLY.png']]
handoff=put('ARTIST_HANDOFF_PREPONLY.json',{
 'id':'ART-G12-69','status':'DRAFT_READY_WITHOUT_SUBMIT','PREPONLY':True,'run':str(R),
 'formal_request':l['formal'],'formal_field_count_including_MaskFile':8,'prompt':l['prompt'],'mask':l['mask'],
 'latest_valid_lock':rec(lp),'preview_guard':rec(R/'Preview-ExactPreparedMaskedIris-v02.ps1'),
 'preview':rec(R/'API_PREVIEW_VALIDATION.json'),'validation':validation,
 'target_native_whole_sha256':l['refs'][0]['sha256'],'exact_ordered_refs':l['refs'],
 'mask_provenance':l['mask_provenance'],'input_provenance':l['provenance'],
 'read_only_review_overlays':[rec(p) for p in keydiags],
 'readonly_diagnostic_identity_map':rec(R/'READONLY_DIAGNOSTIC_SOURCE_IDENTITY.json'),
 'Sol160_report':l['Sol160'],'formal_Sol160_readback':rec(R/'FORMAL_SOL160_EXACT_READBACK.json'),
 'mask_editable_pixels':1679,'input_mask_dimensions':[1587,991],'API_output_size':'1584x992',
 'actual_preview_endpoint':'https://api.openai.com/v1/images/edits','actual_preview_model':'gpt-image-2.5-sunburst',
 'quality':'high','background':'transparent','n':1,'automatic_retries':0,
 'scope_proof':l['scope'],'existing_user_project_authorization':l['auth'],
 'current_parent_instruction_is_PREPONLY_execution_not_released':True,
 'required_followup_if_API_returns_known_success':['Actual full raw/white/black/source eyes comparison',
   'Mandatory builtin coherent whole-current-visible-character redraw linked to this local run',
   'Actual new whole raw/white/black/source normaleyes/rootcoil and fresh root+Sol review',
   'Separate 1080 whole-layer photographic placement of straight original bottom outside frame'],
 'mask_scope':'Entire visible iris pigment includes old dark center and lighter lower/outer gray; preserve boundary ink, sclera AA and ordinary white glints. Not a pupil-only center selection.',
 'new_card_scope':'Uniform RGB48/48/48 charcoal input only; no new eye shape and no color painted into any art. G02 method only, source/current owns aperture.',
 'future_whole_local_repair_parent':str(R),'local_repair_status':l['local_repair_status'],
 'no_inheritance_of_old_static_pass_or_dynamic_or_user_acceptance':True,
 'API_calls':0,'native_calls':0,'http_attempts':0,'central_registry_exposure_binding_written':False,
 'risks':['API mask protection and flat fill are untested behavior until actual return',
   'Input/output small size difference may shift pixels uniformly; only readonly comparison alignment allowed',
   'Mandatory whole may reintroduce iris rings or change source aperture; fresh actual review required',
   'Hair P2/hidden geometry and photographic coverage are not certified by this eye prep']
})
print(json.dumps({'formal':l['formal'],'prompt':l['prompt'],'mask':l['mask'],'lock':rec(lp),'handoff':handoff,'preview':rec(R/'API_PREVIEW_VALIDATION.json'),'calls':0},ensure_ascii=False))
