from pathlib import Path
from PIL import Image
import json,hashlib,datetime,shutil

P=Path(__file__).resolve().parent
PROJECT=P.parents[5]
B=P.parents[3]
CEL=P.parent
OLD=CEL/'whole_imggen_source2365_frontshoulder_headcrop_puregray_v06'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):
 p=Path(p);return dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
assert PROJECT.name=='魔术之心',PROJECT
for name in ['attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png']:
 assert not (P/name).exists(),name
initial=load(P/'INPUT_PROVENANCE_INITIAL_PREPONLY.json')
refs=initial['reference_inputs']
for r in refs:assert sha(r['path'])==r['sha256']
maskprov=load(P/'MASK_PROVENANCE_PREPONLY_v02.json')
mask=Path(maskprov['mask']);assert sha(mask)==maskprov['mask_sha256']
assert Image.open(mask).size==Image.open(refs[0]['path']).size==(957,1644)
defaults=load(PROJECT/'image_defaults.json')
prefix=defaults['generation_prompt_prefix']['text']
assert defaults['generation_prompt_prefix']['enabled']
policy=B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json'
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
assert sha(policy)=='fe7f8b650bf4b621bb5aaa0b4d4d6d958809100d4278b6635d74e3a36217e39d'
job=load(CEL/'JOB.json');receipt=load(OLD/'NATIVE_CALL_RECEIPT.json')
assert job['source_frame']==2365 and job['source_pts']==1262592
assert receipt['known_result_saved'] and not receipt['result_unknown'] and receipt['raw_sha256']==refs[0]['sha256']
prompt=prefix+'''\n\n只编辑图1当前完整透明人物的蒙版开放区域。用户对这张v06明确说“钻发反了”：可见近侧后颈两红珠、从它横跨后颈和背肩的整束卷都是错误路线，不能保留此根只把尾尖挪到右边。清除开放区内这组错误红珠及全部旧横卷/C，在原位置恢复自然bob下缘、原黑高领、原白肩褶/肩带及黑泡袖，接回各自真实线条，不扩大或改造衣肩。蒙版开放的背景不是要画满的轮廓。\n\n这是身体背3/4、头向画右转的2365姿势。唯一的发根仍在人物自身LEFT低耳后/颈侧，当前是远侧，可完全被bob、颈肩遮住，不能在可见后脑近侧重挂红珠，不能抬到眼高或太阳穴。保持头身手脚原方向，不镜像，不另长第二束。从同一远侧低根自然绕到同侧肩FRONT，只有在画右的前颈肩/胸侧外沿露出合理有分量的宽灰螺旋片段及渐细返回/C；被bob或肩遮住的连接不必强露。不能再画一条横跨可见后颈/黑上背/白肩褶的灰带来冒充肩前，也不能全藏成tiny细S。可见宽度与整头固有体量相称，不把蒙版空间全部填满，不放大到粗柱，不为露卷扩肩、挪手或掀bob。\n\n宽GRAY发带的正面连续翻入不透明gray内/后返回，再接下一转并渐细收尾；上端也要真实前返回折连接，不是封口椭圆帽片堆、实体锥上缠绿色装饰或分节小柱。只有真正空气透明，实体gray返回保持不透明，不固定孔数、圈数、轴长或强露完整尖。图3仅给无光照GRAY颜料#B6B4B2，bob与卷前/内/后/返回同灰平涂，mutedmint只是较细材料条带；不加独立深灰体积内底、银白高光或渐变。\n\n图2原2365完整guide只拥有本稿头颈/身体朝向、动作、衣装和可见裁切。保持图1现有灰短圆润bob身份、白maidcap及同基部两片主要黑叶、原有脸部边缘；源没有可读眼口，不新增眼、笑嘴或正脸。保持原黑高领、两肩白fan/frill真实大小和位置、白X交叉、腰后双臂与手袖原遮挡、白腰后结及每条尾带、黑裙摆向/腿/踝带和两只完整鞋。除恢复旧错误珠卷所遮住的必要衣面及新卷自然压住的极窄前侧轮廓外，其他头脸/肩/手/衣身保持。图2红发/双高卷不是本OC身份或正确发根，不复制；没有AI身体或旧14背垂图参与。\n\n输出完整当前可见人物的一张透明RGBA中间稿，不画背景、棋盘、字幕或色卡。图1 alpha为0的隐藏RGB不是实体，不能描入背景。此局修后仍必须另做一次内置imggen整个人物连贯重绘并重新实际查看、root及独立复审；本局修本身不能直接入库。\n'''
promptpath=P/'prompt_api.txt';assert not promptpath.exists();promptpath.write_text(prompt,encoding='utf-8')
formal=dict(InputImages=[r['path'] for r in refs],PromptFile=str(promptpath),MaskFile=str(mask),OutputDirectory=str(P),OutputFileName='character_api_original.png',Size='960x1648',Quality='high',Background='transparent')
assert len(formal)==8
dump(P/'API_PREPARED_REQUEST.json',formal)
userrecord=dict(id='ART-G33-15',record_type='artist_preparation_parent_relay_readback_not_ROOT_review',user_quote_verbatim='钻发反了',quote_source='Parent /root latest task message, exact known v06 QA_black identified; original chat not independently queried.',target_raw=rec(OLD/'character_imggen_original.png'),user_rejected_qa_black=rec(OLD/'qa_black.png'),existing_front_policy=rec(policy),existing_user_quotes=load(policy)['user_requests'],interpretation='Both current visible near-side rear-nape red-bead root and entire diagonal rear/back-shoulder coil are rejected. Clear old route; same anatomical LEFT far low root may be fully occluded, while substantial gray coil fragments naturally emerge only at viewer-right shoulder FRONT / anterior neck-chest edge. Not merely a tail move from existing root.',no_user_acceptance_claim=True,static_only=True)
dump(P/'USER_EXPLICIT_V06_REVERSED_ROUTE_READBACK_PREPONLY.json',userrecord)
history=dict(id='ART-G33-15',current_known_return=rec(OLD/'character_imggen_original.png'),native_receipt=rec(OLD/'NATIVE_CALL_RECEIPT.json'),known_result_saved=True,result_unknown=False,new_known_v06_defect_not_unknown_retry=True,current_whole_local_repair_parent=None,current_whole_operation='whole_character_redraw',old_versions_preserved=True,prior_primary_is_historical_v01_not_v06=True,planned_api_calls_on_future_specific_root_release=1,automatic_retries=0,PREPONLY=True,api_calls=0,native_calls=0,HTTP_calls=0)
dump(P/'KNOWN_RETURN_AND_HISTORY_BOUNDARY_PREPONLY.json',history)
shutil.copyfile(OLD/'NATIVE_CALL_RECEIPT.json',P/'PRIOR_V06_KNOWN_NATIVE_RECEIPT_EXACT_COPY.json')
shutil.copyfile(OLD/'BUILTIN_GENERATION.json',P/'PRIOR_V06_BUILTIN_GENERATION_EXACT_COPY.json')
shutil.copyfile(CEL/'PRIMARY_GOAL_REVIEW.json',P/'PRIOR_CEL_PRIMARY_HISTORICAL_SNAPSHOT_NOT_V06_REVIEW.json')
localstatus=dict(id='ART-G33-15',status='PREPONLY_KNOWN_V06_ROUTE_DEFECT_MASKED_API_NOT_SUBMITTED_MANDATORY_WHOLE_PLANNED',PREPONLY=True,locally_repaired=False,local_repair_planned=True,local_repair_completed=False,api_submitted=False,api_calls=0,native_calls=0,HTTP_calls=0,automatic_retries=0,root_release_received=False,source_current=refs[0],requires_whole_character_redraw=True,mandatory_whole_character_redraw=True,mandatory_whole_redraw_after_local_repair=True,whole_character_redraw_completed=False,direct_selection_allowed=False,fresh_root_and_independent_review_required=True,artist_observation_not_ROOT_or_Sol=True)
dump(P/'LOCAL_REPAIR_STATUS.json',localstatus)
scope=dict(id='ART-G33-15',PREPONLY=True,authorization=rec(auth),authorized_endpoint='https://api.openai.com/v1/images/edits',provider_wrapper=rec(PROJECT/'scripts/Invoke-ReferenceImage.ps1'),existing_user_scope_covers_subsequent_same_GOAL_characters_references_and_necessary_masks=True,not_new_permission_request=True,current_parent_instruction='Preparation only; no execution/API/HTTP/native; await ROOT actual/release and fresh174.',root_specific_generation_release_received=False,api_calls_authorized_this_prep=0,planned_calls_on_future_release=1,automatic_retries=0,exact_refs=[rec(r['path']) for r in refs],exact_mask=rec(mask),transparent_background=True)
dump(P/'PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',scope)
request=dict(id='ART-G33-15',operation_kind='masked_route_correction_intermediate',PREPONLY=True,dispatchable=False,root_release_received=False,transparent_background=True,provider='OpenAI API',endpoint='https://api.openai.com/v1/images/edits',model='gpt-image-2.5-sunburst',n=1,retry=0,quality='high',size='960x1648',actual_input_size=[957,1644],output_size_note='Output rounded to16px whole-image dimensions; input target+mask remain exact957x1644; no partwise transform. Output proportion tiny difference handled uniformly only.',source_frame=2365,source_pts=1262592,first_case_frames=[889,891],refs=refs,prompt_file=str(promptpath),prompt_sha256=sha(promptpath),mask=rec(mask),mask_provenance=rec(P/'MASK_PROVENANCE_PREPONLY_v02.json'),api_prepared_request=rec(P/'API_PREPARED_REQUEST.json'),changed_hypothesis='Explicit user side reversal invalidates visible near rear root as well as entire diagonal back route. An edit mask can clear both wrong root and route while reserving far-side shoulder-FRONT visible window; this is an untested control of reference competition, not proof of model-internal causality.',old_current_root_not_correct_anchor=True,user_rejection=rec(P/'USER_EXPLICIT_V06_REVERSED_ROUTE_READBACK_PREPONLY.json'),current_local_parent=None,mandatory_whole_after_local=True,future_whole_dispatchable=False,API_calls=0,native_calls=0,HTTP_calls=0,automatic_retries=0,dynamic_tested=False,user_accepted=False)
dump(P/'request_api_PREPONLY.json',request)
future=P/'future_mandatory_whole_PREPONLY';future.mkdir(exist_ok=True)
futureprompt=prefix+'''\n\n以下仅是未来局修已知返图并实际查看后才能定稿的整人草案。图1应为新局修完整透明人物，不是旧v06。以原2365完整source保持背3/4头向画右、无可读眼口、腰后双臂手袖、白X/腰后结尾带、裙腿双鞋及裁切，一次连贯重绘完整当前可见人物，统一头颈bob/帽/衣肩与新卷接合，不拼接、不warp。去掉可见近侧后颈错误双珠和跨后颈/背肩横卷；唯一人物LEFT低根在本远侧，可完全被bob颈肩遮住，不能为露珠换侧或抬根。宽灰卷片段只在viewerRIGHT肩FRONT/前颈胸侧自然露出，保持合理整头体量，不微型/巨大，不强露整尾。宽GRAY前面连续翻入不透明gray返回接下转渐细C，真实空气透明，gray返回不能一律挖空；同bob的无光照gray和薄mint材料条，不深暗体积/银光/渐变。不复制原红尖额发/双高卷或改原动作、衣肩大小。实际局修若仍错根/错路线/衣肩损坏、缩卷或结构材质缺陷，必须先据新返图改此草案，不能声称局修已正确。透明背景，返后freshroot/Sol；此草案目前不得调用。\n'''
(future/'prompt_imggen_DRAFT.txt').write_text(futureprompt,encoding='utf-8')
futureargs=dict(prompt=futureprompt,referenced_image_paths=[str(P/'character_api_original.png'),refs[1]['path'],refs[2]['path']],transparent_background=True)
dump(future/'request_imggen_DRAFT.json',dict(id='ART-G33-15',operation_kind='whole_character_redraw',PREPONLY=True,dispatchable=False,root_release_received=False,transparent_background=True,local_repair_parent=str(P),mandatory_whole_after_local=True,local_result_not_yet_exists=True,local_target_path=str(P/'character_api_original.png'),local_target_sha256=None,requires_known_return_and_actual_new_WB_review_before_finalization=True,tool_arguments=futureargs,prompt_file=str(future/'prompt_imggen_DRAFT.txt'),prompt_sha256=sha(future/'prompt_imggen_DRAFT.txt'),native_quality_parameter_exposed=False,user_quality_preference='high',api_calls=0,native_calls=0,automatic_retries=0,static_and_placement_review_pending=True))
print(json.dumps(dict(run=str(P),formal=rec(P/'API_PREPARED_REQUEST.json'),request=rec(P/'request_api_PREPONLY.json'),prompt=rec(promptpath),mask=rec(mask),future_whole=rec(future/'request_imggen_DRAFT.json')),ensure_ascii=False))
