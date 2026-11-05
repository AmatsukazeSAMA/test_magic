from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(__file__).resolve().parents[3]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
out=[]
for n,f,v in [(64,1098,2),(65,1103,3)]:
 aid=f'ART-G12-{n}';CEL=B/'drawings'/aid/'v01';R=CEL/f'prep_first_api_source{f}_graybob_sourcehands_v{v:02d}'
 d=read(R/'DRAFT_API_REQUEST.json');lock=read(R/'REQUEST_LOCK.json');p=read(R/'INPUT_PROVENANCE.json');pre=read(R/'API_PREVIEW_PROOF_PREPONLY.json')
 assert not pre['submitted'] and pre['size']==d['Size'] and pre['input_count']==6
 assert not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png')) and not (R/'EXECUTION_LOCK_v01.json').exists()
 for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
 h={'id':aid,'created_utc':datetime.now(timezone.utc).isoformat(),'state':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable_by_artist':False,'root_actual_view_and_personal_network_submit_required':True,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prepared8fields':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'prompt':rec(R/'prompt_api.txt'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'reference_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'provenance':rec(R/'INPUT_PROVENANCE.json'),'hair_input_refinement':rec(R/'PURE_HAIR_ROI_REFINEMENT_HISTORY.json'),'references':lock['references'],'size':d['Size'],'quality':'high','background':'transparent','n':1,'retry':0,'canonical_frame':f,'canonical_pts':d['source_pts'],'first_scene_frames':d['first_case_frames'],'first_scene_pts':d['first_case_pts'],'identity_explicit_after_LEFT_prefix':True,'root_projection':'viewerRIGHT同侧低耳后/nape/bob下LEFT，按当前轻转/正面投影，不追露脸抬珠/换近耳或镜像','expression_hands':p['frame_specific_action'],'source_body_cutoff':p['frame_specific_body'],'phase':p['frame_specific_phase'],'AI_visibility_limit':('R213purehair38x19' if n==64 else 'R216大部被白肩挡，只purehair36x7局部，不能认证隐藏phase/构造')+'；只次级回弹，不按tinyROI缩固有发量/复制AIbody/root或实心coil。','continuity':'前63肩前路线需连贯转接，不无依据整束跳背后；本实际源肩手遮挡优先，动态另经真实曝光核，不由prep推定前驱passed。','source_canvas':'原JOB同guide完整未挖头，全部原掌尖/腰/apron半身底裁保，无新trim/warp/艺术patch/补隐藏腿鞋','API_calls':0,'HTTP_calls':0,'native_calls':0,'inflight':0,'execution_lock_created':False,'attempt_created':False,'no_raw_or_unknown':True,'central_registry_modified':False,'REGPLAN_JOB_modified':False,'63_and_previous_requests_untouched':True,'no_generation_release_in_this_handoff':True,'no_artistic_or_dynamic_PASS':True,'no_66_work':True}
 dest=R/'ARTIST_PREPONLY_HANDOFF.json';assert not dest.exists();dest.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 out.append({'id':aid,'handoff':rec(dest),'formal':rec(R/'API_PREPARED_REQUEST.json'),'lock':rec(R/'REQUEST_LOCK.json'),'prompt':rec(R/'prompt_api.txt'),'preview':rec(R/'API_PREVIEW_PROOF_PREPONLY.json'),'artist_review':rec(R/'ARTIST_REFERENCE_REVIEW.json'),'calls':0})
print(json.dumps(out,ensure_ascii=False,indent=2))
