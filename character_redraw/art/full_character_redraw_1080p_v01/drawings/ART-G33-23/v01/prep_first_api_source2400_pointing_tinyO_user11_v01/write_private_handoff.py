from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
raw=R/'character_api_original.png';expected='963d83c21099916505b5c20bd2fd4eb14644d3a2a8bb0d6b90843d5779cc0822'
assert sha(raw)==expected
assert sha(R/'REQUEST_LOCK.json')=='31f0d82bb17a7bad2ef9ebd3f88a09e68fb5842c3101d3a18583fdca542fc0c1'
assert sha(R/'API_PREPARED_REQUEST.json')=='70cd087e7b25e93583522bc223177d668c9ea90906b0181e9fb58f37c337e617'
res=read(R/'result.json');att=read(R/'attempt.json');pv=read(R/'INPUT_PROVENANCE.json');lock=read(R/'EXECUTION_LOCK_v01.json');now=datetime.now(timezone.utc).isoformat()
assert att['status']=='completed' and att['api_calls']==1 and att['automatic_retries']==0
for key in ['JOB','REGISTRATION_PLAN']:assert sha(lock[key]['path'])==lock[key]['sha256']
view=[raw,R/'qa_white.png',R/'qa_black.png',Path(pv['source_full']['path']),Path(pv['first_scene_source']['path']),Path(pv['source_guide']['path']),Path(pv['refs'][1]['source']['path'])]
view += [Path(x['path']) for x in pv['refs']]
view += [R/'diagnostics'/n for n in ['CAP_V_ATTACHMENT_white_3x.png','SOURCE2400_CAP_V_ATTACHMENT_3x_READONLY.png','ROOT_COIL_white_1x.png','ROOT_COIL_white_3x.png','ROOT_COIL_black_3x.png','SOURCE2400_vs_API23_FULL_1x_READONLY.png','EYES_TINY_O_white_3x.png','POINT_INDEX_HAND_white_3x.png','DOWN_HAND_white_3x.png','BOTH_SHOES_white_1x.png']]
review=put('DRAFT_PRIMARY_REVIEW.json',{
 'id':'ART-G33-23','created_utc':now,'reviewer':'xhigh_pending_artist private visual draft; not root or Sol',
 'image':str(raw),'exact_raw_sha256':expected,'actual_viewed':[rec(p) for p in view],
 'decision':'HOLD_CAP_EXTRA_LOWER_TIP_AND_CURL_FLAT_MATERIAL_PENDING_ROOT',
 'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
 'source_identity_verification':'original catalog/PROVENANCE/REDRAW_PLAN/JOB/PRIORITY均2400/PTS1281280，首917..919；不是2397猜帧。',
 'source_action_expression':{'observation':'原明显睁眼弧和单charcoal普通白点、tiny竖O开口保留；画左只单index斜上、其它曲指/拇指折，画右臂手并指斜下，白cuffs及当前掌向基本保。全apron双白竖frill、红bowgold、腰后白bow、黑裙向画右扬、异角双腿/踝带/完整两鞋在。','assessment':'大动作/眼口/可见手脚可保留，未做摄影对齐或原线逐像素认可。'},
 'root':{'observation':'画右同侧低耳后/bob下缘/nape双红珠接唯一卷，低于眼线；身体/头手未镜像，没换到画左近耳。','boundary':'不因此认证全部卷几何和隐藏段。'},
 'cap':{'observation':'两长黑叶共同小底下仍另接一片朝下短尖瓣，源V两叶仅厚连接底，无此独立下尖。source/new cap3x已实际对照。','priority':'P1_review_requested','boundary':'需要root/Sol对该下尖定级，不把自然连接底面积要求为0，也未自动数像素批准。'},
 'curl_shape_material':{'observation':'宽gray front/斜返回/末C和合理整头相对体量仍在，不是微型薄绿挂件。但前面gray/mint有渐混/柔灰光，内返回有较深灰片/条纹。上端仍横椭圆帽样front，返回路径未清楚读成连续绕行；不能只靠末C或整体螺旋轮廓通过。','assessment':'HOLD upper-return/material fresh review; not a master.','boundary':'不以无指定孔判实心、不将所有opaquegray返回片挖空；被遮内腔不可认证。'},
 'occlusion_review_point':{'observation':'本稿下C明显露于画右肩袖前/外，部分gray返回邻白frill；R68下段有白frill遮挡。AI身体不同，不能直接按其像素轮廓定原PV衣发前后；须root结合当前源与相位新看。','validated':False,'not_claimed':'未把完整末C出现自动当通过，也不在本私评中虚构隐藏完整形。'},
 'transparent_background':'raw A0隐藏RGB含灰glow，完整white/black不见实体背景/独立特效，未代码清RGB或改art；技术透明统计不代替艺术边缘验收。',
 'temporal':'未真实PTS播放917..919与相邻22/后稿，不认证动态连续或家族通过。',
 'issues_for_root':[{'priority':'P1_review_requested','part':'cap lower short tip','description':'原V两叶之外下垂尖瓣再次出现。'},{'priority':'P1_review_requested','part':'curl front-return flat material','description':'gray/mint渐混及返回深灰，上端帽片读感，需fresh看。'},{'priority':'review_point','part':'lower curl vs shoulder frill','description':'当前C露肩袖前，源/相位遮挡关系未认证。'}],
 'API_calls':1,'automatic_retries':0,'native_calls':0,'result_unknown':False,
 'JOB_REGPLAN_unchanged':True,'immutable_PREP_LOCK_unchanged':True,'central_registry_modified':False,'binding_modified':False,'progress_modified':False,
 'user_accepted':False,'dynamic_validated':False,'next_action':'一图后停交root；无自动修、native、第二API或下一状态。',
})
receipt=put('PRIVATE_CALL_RECEIPT.json',{
 'id':'ART-G33-23','created_utc':now,'tool':'exec_command require_escalated approved official immutable guard wrapper',
 'exec_session_id':55032,'status':'known_completed','API_calls':1,'automatic_retries':0,'native_calls':0,
 'model':res['model'],'quality':res['quality'],'size_actual':[624,1072],'background':res['background'],'elapsed_seconds':res['elapsed_seconds'],
 'raw':rec(raw),'formal_request':rec(R/'API_PREPARED_REQUEST.json'),'immutable_prep_lock':rec(R/'REQUEST_LOCK.json'),'execution_lock':rec(R/'EXECUTION_LOCK_v01.json'),
 'root_release':rec(R/'ROOT_EXECUTION_RELEASE_v01.json'),'authorization_scope_proof':rec(R/'AUTHORIZATION_SCOPE_CHECK_v01.json'),'broad_authorization':rec(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
 'no_send_preview':rec(R/'API_PREVIEW_PROOF_v01.json'),'effective_prompt':rec(R/'prompt_effective.txt'),
 'original_response':rec(R/'api_response.raw.json'),'response_headers':rec(R/'response_headers.txt'),'attempt':rec(R/'attempt.json'),'result':rec(R/'result.json'),'manifest':rec(R/'request_manifest.json'),
 'outbound_files_only_locked6_drawing_references':True,'technical_success_not_art_acceptance':True,
})
handoff=put('ARTIST_HANDOFF.json',{
 'id':'ART-G33-23','created_utc':now,'state':'POST_EXPLICIT_RELEASE_KNOWN_FIRST_API_RETURN_PRIVATE_HOLD',
 'run':str(R),'raw':rec(raw),'actual_size':[624,1072],'elapsed_seconds':26.820,'model':res['model'],'quality':'high','background':'transparent',
 'API_calls':1,'automatic_retries':0,'native_calls':0,'inflight':0,
 'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),
 'normal_coil':rec(R/'diagnostics/ROOT_COIL_white_1x.png'),'coil3x_white':rec(R/'diagnostics/ROOT_COIL_white_3x.png'),'coil3x_black':rec(R/'diagnostics/ROOT_COIL_black_3x.png'),
 'cap3x':rec(R/'diagnostics/CAP_V_ATTACHMENT_white_3x.png'),'source_cap3x':rec(R/'diagnostics/SOURCE2400_CAP_V_ATTACHMENT_3x_READONLY.png'),
 'source_comparison':rec(R/'diagnostics/SOURCE2400_vs_API23_FULL_1x_READONLY.png'),
 'private_review':review,'call_receipt':receipt,'technical_return':rec(R/'TECHNICAL_RETURN_QA.json'),
 'observation_summary':'原source2400 tinyO/单index斜上/右手并指斜下/裙右扬/完整鞋、画右低LEFT根保；下帽尖再次多余，coil上端与材质HOLD，肩袖前C遮挡待审。',
 'historic_prep_only_records_preserved':'Old zero-call prep records remain immutable historical evidence; this POST_RELEASE handoff records the one now-known successful authorized call.',
 'central_registry_modified':False,'binding_modified':False,'progress_modified':False,'JOB_REGPLAN_modified':False,'quota_resets':0,'no_following_item_started':True,
 'fresh_root_and_Sol_required':True,'art_accepted':False,'dynamic_validated':False,
})
print(json.dumps({'raw':rec(raw),'review':review,'receipt':receipt,'handoff':handoff,'API_calls':1,'inflight':0},ensure_ascii=False,indent=2))
