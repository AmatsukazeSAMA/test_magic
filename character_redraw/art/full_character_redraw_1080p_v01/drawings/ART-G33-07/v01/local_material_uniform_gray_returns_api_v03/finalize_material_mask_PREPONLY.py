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
    p=R/name;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
lp=R/'REQUEST_LOCK_PREPONLY.json';assert sha(lp)=='5ac9e23a2297b9bf79f52a6873c50468392295a15e3a804faca79282dda0faa8';l=read(lp)
for e in [l[k] for k in ['formal','prompt','mask','mask_provenance','provenance','review','actual_view_list','history','scope','auth','provider','provider_configuration','Sol162','local_repair_status']]+l['refs']:
    assert sha(e['path'])==e['sha256'],e['path']
q=read(l['formal']['path']);assert len(q)==8 and len(q['InputImages'])==2
assert q['MaskFile']==l['mask']['path'] and q['Size']=='960x1648' and q['Quality']=='high' and q['Background']=='transparent'
mask=Image.open(q['MaskFile']).convert('RGBA');target=Image.open(q['InputImages'][0]).convert('RGBA');assert mask.size==target.size==(957,1643)
h=mask.getchannel('A').histogram();assert h[0]==1240 and sum(h[1:255])==0
for y in range(1643):
    for x in range(957):
        if mask.getpixel((x,y))[3]==0:
            r,g,b,a=target.getpixel((x,y))
            assert a>=235 and min(r,g,b)>=65 and max(r,g,b)<=175 and max(r,g,b)-min(r,g,b)<=14 and g-r<=8 and g-b<=10
history=read(l['history']['path'])
for f in history['old_v15_file_inventory_before']:assert sha(f['path'])==f['sha256']
ancestor=C/'local_upper_connected_gray_envelope_api_v02/LOCAL_REPAIR_STATUS.json'
assert sha(ancestor)==history['ancestor_status_before']['sha256']
p=read(l['provenance']['path'])
for k in ['source_JOB','source_REGPLAN','source_original','source_guide_not_sent']:assert sha(p[k]['path'])==p[k]['sha256']
preview=read(R/'API_PREVIEW_VALIDATION.json')['actual_preview'];assert not preview['submitted'] and preview['input_count']==2 and preview['mask_provided'] and preview['n']==1
for n in ['attempt.json','result.json','api_response.raw.json','response_headers.txt','prompt_effective.txt','request_manifest.json','character_api_original.png']:
    assert not (R/n).exists(),n
validation=put('PREPONLY_TECHNICAL_VALIDATION.json',{
 'id':l['id'],'recorded_utc':datetime.now(timezone.utc).isoformat(),'technical_preparation_valid':True,'artistic_pass':False,
 'checks':['knownv15 raw4a0c2fd4/native receipt and priorlocal API completed result verified',
   'freshSol162 exactv15 material-onlyP1 read; no inherited old prep crop as output',
   'two exact refs currenttarget/puregray-only card actual viewed and hash locked',
   'mask matches957x1643 firstinput; alpha0 only1240 grayinterior pixels; air/mint/ink/root/body protected',
   'actual fullwhiteblack/coil5x/protectionzones and alpha QA viewed with exact prior-sourceSHA',
   'configured officialsunburst/high960x1648/transparent/n1/MaskFile Preview returnedsubmittedfalse',
   'allv15files/oldlocalstatus/JOB/REGPLAN/source remain unchanged',
   'no API/native/HTTPattempt/result or centralbindingwrite'],
 'mask_editable_pixels':1240,'mask_protected_pixels':957*1643-1240,'latest_lock':rec(lp),
 'no_causal_claim_about_old_reference_material_competition':True,
 'required_future_whole_after_API_and_fresh_reviews_pending':True,
 'API_calls':0,'native_calls':0,'central_modified':False
})
qa=[R/'qa_readonly'/('PREP_PRIOR_CANDIDATE_4a0c2fd4_'+n) for n in [
 'MASKv02_OVERLAY_FULL_white_READONLY.png','MASKv02_OVERLAY_FULL_black_READONLY.png',
 'MASKv02_OVERLAY_COIL_white_5x_READONLY.png','MASKv02_OVERLAY_COIL_black_5x_READONLY.png',
 'MASKv02_ALPHA_COIL_5x_READONLY.png','MASKv02_PROTECTION_ZONES_COIL_4x_READONLY.png']]
handoff=put('ARTIST_HANDOFF_PREPONLY.json',{
 'id':l['id'],'status':'DRAFT_READY_WITHOUT_SUBMIT','PREPONLY':True,'run':str(R),
 'formal_request':l['formal'],'formal_field_count_including_MaskFile':8,'prompt':l['prompt'],'mask':l['mask'],'request_lock':rec(lp),
 'exact_ordered_refs':l['refs'],'source_target_sha256':l['refs'][0]['sha256'],
 'input_mask_size':[957,1643],'API_output_size':'960x1648','quality':'high','background':'transparent','n':1,'automatic_retries':0,
 'mask_editable_pixels':1240,'mask_bbox_xyxy':[677,345,814,471],
 'reviewable_full_local_and_protection_QA':[rec(f) for f in qa],
 'actual_viewed_and_ref_review':l['review'],'actual_list':l['actual_view_list'],'input_provenance':l['provenance'],
 'diagnostic_source_identity':rec(R/'READONLY_DIAGNOSTIC_SOURCE_IDENTITY.json'),
 'mask_provenance':l['mask_provenance'],'known_local_and_native_history':l['history'],
 'latestSol162':l['Sol162'],'scopeproof':l['scope'],
 'preview':rec(R/'API_PREVIEW_VALIDATION.json'),'preview_only_guard':rec(R/'Preview-ExactPreparedMaterialMask.ps1'),'validation':validation,
 'hypothesis':'Known v15 geometry/volume/lowLEFT outwardphase retained. Only currenttarget plus pureGRAY pigment replaces prior polished detail/identity sources for material; no causal inference asserted.',
 'material_constraint':'Edited inner/backgrayreturns and C gray bands remain opaque solid graypigment, same unlitgray as bob/front; no newholes/removal or mint recolor.',
 'required_future_work_after_known_API_return':['Actual newcomplete raw/whiteblack and normalscale/3x grayreturn+C compare',
  'Mandatory builtin coherent whole-visible-character redraw linked to THIS localrun',
  'New whole raw/whiteblack/source actualfresh root andSol review',
  'Separate first861862 and canonical2333 photography; originalcutoff fronttoe notcertified'],
 'root_execution_release_pending':True,'mandatory_whole_pending':True,'new_whole_completed':False,
 'API_calls':0,'native_calls':0,'http_attempts':0,
 'central_registry_or_old_localparent_or_bindings_modified':False,'dynamic_validated':False,'user_accepted':False
})
print(json.dumps({'formal':l['formal'],'prompt':l['prompt'],'mask':l['mask'],'lock':rec(lp),'key':l['refs'][1],'handoff':handoff,'preview':rec(R/'API_PREVIEW_VALIDATION.json'),'calls':0},ensure_ascii=False))
