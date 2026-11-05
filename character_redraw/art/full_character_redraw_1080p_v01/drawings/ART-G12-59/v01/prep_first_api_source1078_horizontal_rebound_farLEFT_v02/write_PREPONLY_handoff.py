from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
lock=read(R/'REQUEST_LOCK.json');pre=read(R/'API_PREVIEW_PROOF_PREPONLY.json');p=read(R/'INPUT_PROVENANCE.json')
assert pre['submitted']==False and pre['size']=='816x1040' and pre['input_count']==6
assert not any(R.parent.rglob('attempt.json')) and not any(R.parent.rglob('character_api_original.png'))
for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
o={'id':'ART-G12-59','created_utc':datetime.now(timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable_by_artist':False,'root_actual_view_and_personal_network_submit_required':True,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prepared8fields':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'prompt':rec(R/'prompt_api.txt'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'reference_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'provenance':rec(R/'INPUT_PROVENANCE.json'),'references':lock['references'],'size':[816,1040],'quality':'high','background':'transparent','n':1,'retry':0,'canonical_frame':1078,'canonical_pts':575504,'first_scene_frames':[1075,1078],'first_scene_pts':[573904,576048],'root_projection':'右向三分之四远侧画右bob/nape唯一LEFT低根；画左可见近耳下无双珠','phase_warning':'原1078几乎水平外甩；R195更下收，仅次级压缩，不作axis authority。没有55..58整头旧表情动作bitmap。','expression_hands':'源不对称半睁+高张开笑口粉内口；高画右角形闭合OK环/三余指，胸前另一手垂指，原袖口/肩褶在远侧路径前景。','source_canvas':'原816x1040完整未挖头guide不改、无额外trim、REGPLAN未修改、无代码艺术patch','hair_ROI_revision':rec(R/'CHANGED_HAIR_ROI_PREFLIGHT_v02.json'),'API_calls':0,'HTTP_calls':0,'native_calls':0,'inflight':0,'attempt_created':False,'no_raw_or_unknown':True,'central_registry_modified':False,'REGPLAN_JOB_modified':False,'no_generation_release_in_this_handoff':True,'no_artistic_or_dynamic_PASS':True}
dest=R/'ARTIST_PREPONLY_HANDOFF.json';assert not dest.exists();dest.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':rec(dest),'formal':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'artist_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'calls':0},ensure_ascii=False,indent=2))
