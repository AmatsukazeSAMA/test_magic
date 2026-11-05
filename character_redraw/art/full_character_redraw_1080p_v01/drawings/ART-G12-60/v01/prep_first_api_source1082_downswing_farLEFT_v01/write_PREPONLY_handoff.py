from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
lock=read(R/'REQUEST_LOCK.json');pre=read(R/'API_PREVIEW_PROOF_PREPONLY.json')
assert not pre['submitted'] and pre['size']=='736x1072' and pre['input_count']==6
assert not any(R.parent.rglob('attempt.json')) and not any(R.parent.rglob('character_api_original.png')) and not (R/'EXECUTION_LOCK_v01.json').exists()
for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
d={'id':'ART-G12-60','created_utc':datetime.now(timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable_by_artist':False,'root_actual_view_and_personal_network_submit_required':True,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prepared8fields':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'prompt':rec(R/'prompt_api.txt'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'reference_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'provenance':rec(R/'INPUT_PROVENANCE.json'),'references':lock['references'],'size':[736,1072],'quality':'high','background':'transparent','n':1,'retry':0,'canonical_frame':1082,'canonical_pts':577648,'first_scene_frames':[1079,1083],'first_scene_pts':[576048,578720],'root_projection':'右向三分之四远画右bob/nape唯一LEFT低根；近画左可见耳无珠，不追露珠换根','phase':'原1082近红卷尖低于根，60重新下摆，不继续59水平外甩；近红卷只相位，非镜像根身份。R198只次级近颈压缩弹性。','expression_hands':'当前半睁不对称眼+小U形开笑粉内口；高画右角形闭OK/钩指，胸前手仅保当前可见指，被前臂/袖口挡住部分不补全，原衣腰底裁保持。','source_canvas':'7361072完整未挖头guide保持，REGPLAN/JOB未改，无代码artpatch','API_calls':0,'HTTP_calls':0,'native_calls':0,'inflight':0,'execution_lock_created':False,'attempt_created':False,'no_raw_or_unknown':True,'central_registry_modified':False,'REGPLAN_JOB_modified':False,'59_files_untouched':True,'no_generation_release_in_this_handoff':True,'no_artistic_or_dynamic_PASS':True}
p=R/'ARTIST_PREPONLY_HANDOFF.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':rec(p),'formal':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'artist_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'calls':0},ensure_ascii=False,indent=2))
