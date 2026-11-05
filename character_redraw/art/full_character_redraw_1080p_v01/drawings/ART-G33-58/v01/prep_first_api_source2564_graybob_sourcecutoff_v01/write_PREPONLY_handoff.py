from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
lock=read(R/'REQUEST_LOCK.json');pre=read(R/'API_PREVIEW_PROOF_PREPONLY.json')
assert not pre['submitted'] and pre['size']=='624x1072' and pre['input_count']==6
assert not any(R.parent.rglob('attempt.json')) and not any(R.parent.rglob('character_api_original.png')) and not (R/'EXECUTION_LOCK_v01.json').exists()
for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
d={'id':'ART-G33-58','created_utc':datetime.now(timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable_by_artist':False,'root_actual_view_and_personal_network_submit_required':True,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prepared8fields':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'prompt':rec(R/'prompt_api.txt'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'reference_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'provenance':rec(R/'INPUT_PROVENANCE.json'),'references':lock['references'],'size':[624,1072],'quality':'high','background':'transparent','n':1,'retry':0,'canonical_frame':2564,'canonical_pts':1368832,'first_scene_frames':[1088,1092],'first_scene_pts':[580848,583520],'identity_explicit_after_LEFT_prefix':'图3中性灰短圆润bob女孩，原红角色/尖长额发侧刺不是目标且非仅改色；图1只当前动作眼口衣手body。','root_projection':'已近正面，唯一LEFT画右同侧低耳后/bob下nape；不沿57侧向隐藏假设或搬根到近耳','phase':'原两红卷转正都可见只作相位，末主要外下/回收非持续升高；只目标单LEFT，不引入双卷身份。R205purehair只次级弹性。','expression_hands':'源圆睁眼/小浅波闭口，画左胸前折腕分指下垂/拇指左，画右外侧横摊/拇指上长指右，非57交叠高掌/60OK。','SOURCE_CUTOFF_EXCEPTION':'原full2564底1080裁掉脚鞋；只小腿、一踝带和贴底皮肤段可见，不存在完整两鞋。保持guide原裁断，不补隐藏脚尖/鞋、不缩人凑脚。','source_canvas':'6241072完整未挖头sourceguide不改，REGPLAN/JOB不改，无artpatch/单部位变换/新trim','API_calls':0,'HTTP_calls':0,'native_calls':0,'inflight':0,'execution_lock_created':False,'attempt_created':False,'no_raw_or_unknown':True,'central_registry_modified':False,'REGPLAN_JOB_modified':False,'59_60_files_untouched':True,'previous57_root_pipeline_pending_at_prep':True,'no_generation_release_in_this_handoff':True,'no_artistic_or_dynamic_PASS':True,'no_63_work':True}
p=R/'ARTIST_PREPONLY_HANDOFF.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':rec(p),'formal':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'artist_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'calls':0},ensure_ascii=False,indent=2))
