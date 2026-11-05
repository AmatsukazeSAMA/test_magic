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
old=R.with_name('prep_first_api_source2558_openpalms_downrecoil_farLEFT_v01')
rev={'previous_immutable_draft':rec(old/'DRAFT_API_REQUEST.json'),'previous_hair_ROI':[594,216,633,255],'reason':'v01 top edge retained a small AI red bead sliver; must not provide AI root pixels','current_hair_ROI':[594,222,633,255],'current_hair':lock['references'][1],'current_crop_size':[39,33],'actual_viewed_current_all6':True,'other5ref_and_prompt_bytes_same':True,'previous_version_preserved_no_send':True}
rp=R/'HAIR_ONLY_ROI_REVISION_v02.json';assert not rp.exists();rp.write_text(json.dumps(rev,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d={'id':'ART-G33-57','created_utc':datetime.now(timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable_by_artist':False,'root_actual_view_and_personal_network_submit_required':True,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prepared8fields':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'prompt':rec(R/'prompt_api.txt'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'reference_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'provenance':rec(R/'INPUT_PROVENANCE.json'),'hair_revision':rec(rp),'references':lock['references'],'size':[624,1072],'quality':'high','background':'transparent','n':1,'retry':0,'canonical_frame':2558,'canonical_pts':1365632,'first_scene_frames':[1084,1087],'first_scene_pts':[578720,580848],'root_projection':'右向更转正，LEFT唯一画右低bob/nape；不追近画左可见耳加双珠，不镜像','phase':'近红卷斜外下、远侧被头遮，57延续向下回收；只转译phase而非红近root/整轮廓','expression_hands':'圆睁眼+张开笑粉内口，双展开掌同时高位画右脸旁交叠，后掌只当前可见指；不能继承60OK或AI分开低手/闭笑','fullbody':'canonical完整裙腿与两踝带鞋均保持，不能照first1084半身裁掉','source_canvas':'6241072完整未挖头原坐标guide，JOB/REGPLAN不改，无artpatch','API_calls':0,'HTTP_calls':0,'native_calls':0,'inflight':0,'execution_lock_created':False,'attempt_created':False,'no_raw_or_unknown':True,'central_registry_modified':False,'REGPLAN_JOB_modified':False,'59_60_files_untouched':True,'no_generation_release_in_this_handoff':True,'no_artistic_or_dynamic_PASS':True}
p=R/'ARTIST_PREPONLY_HANDOFF.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'handoff':rec(p),'formal':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'artist_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'calls':0},ensure_ascii=False,indent=2))
