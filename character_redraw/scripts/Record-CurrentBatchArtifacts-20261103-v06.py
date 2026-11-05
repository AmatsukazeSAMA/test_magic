"""Index known saved returns and actual reviews from this goal continuation."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from PIL import Image

root=Path(__file__).resolve().parent.parent
base=root/'art/full_character_redraw_1080p_v01'
out=base/'review/checkpoints/v20261103_four_FIRST_eye_tolerance_photo_v06'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p.resolve()),'sha256':sha(p)}
def create(p,obj):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
spec=[
 ('ART-G13-18','FIRST','prep_first_api_canonical1281_wider3731_separate_outpointing_barehands_blackred_v06',[1281,3731],[683888,1992384]),
 ('ART-G51-09','FIRST','prep_first_api_source4617_openeyes_single_downleft_glove_fullshoes_graygreen_v07_nativepaths',[4617],[2465392]),
 ('ART-G51-10','FIRST','prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06',[4625],[2469664]),
 ('ART-G13-19','FIRST','prep_first_api_canonical1284_wider3734_outward_partialhands_blackred_v07_visibleunion',[1284,3734],[685488,1994000]),
 ('ART-G51-09','whole','whole_imggen_remove_isolated_under_eye_dots_source4617_v01',[4617],[2465392]),
 ('ART-G51-10','whole','whole_imggen_remove_isolated_under_eye_dots_source4625_v01',[4625],[2469664]),
 ('ART-G13-19','whole','whole_imggen_graybob_visibleunion_remove_points_source1284_wider3734_v01',[1284,3734],[685488,1994000]),
]
records=[]
for ident,kind,name,frames,pts in spec:
    run=base/'drawings'/ident/'v01'/name
    raw=run/('character_api_original.png' if kind=='FIRST' else 'character_imggen_original.png')
    prompt=run/('prompt_api.txt' if kind=='FIRST' else 'prompt_imggen.txt')
    primary=read(run/'PRIMARY_GOAL_REVIEW.json')
    independent=Path(primary['independent_review'])
    assert sha(raw)==primary['image_sha256']
    with Image.open(raw) as im:dimensions=list(im.size);mode=im.mode
    result=run/('result.json' if kind=='FIRST' else 'BUILTIN_GENERATION.json')
    receipt=run/('ROOT_API_EXECUTION_RECEIPT.json' if kind=='FIRST' else 'NATIVE_CALL_RECEIPT.json')
    q=run/('API_PREPARED_REQUEST.json' if kind=='FIRST' else 'request_imggen_ROOT_AUTHORIZED.json')
    metadata=read(result)
    records.append({'id':ident,'operation':kind,'run':str(run),'source_frames':frames,'source_PTS':pts,
        'raw':ev(raw),'dimensions':dimensions,'mode':mode,'white':ev(run/'qa_white.png'),'black':ev(run/'qa_black.png'),
        'prompt':ev(prompt),'request':ev(q),'result':ev(result),'execution_receipt':ev(receipt),
        'provider':'OpenAI official API' if kind=='FIRST' else 'built-in imagegen',
        'quality':'high' if kind=='FIRST' else 'not exposed by built-in tool',
        'n':1,'configured_transport_retry':1 if kind=='FIRST' else 0,
        'actual_automatic_retries':metadata.get('automatic_retries',0),
        'primary_review':ev(run/'PRIMARY_GOAL_REVIEW.json'),'independent_review':ev(independent),
        'static_review_passed':primary['primary_static_pass'] and primary['independent_static_pass'],
        'review_observation':primary['observation'],'user_accepted_whole_art':False,'dynamic_validated':False,
        'raw_preserved':True,'alpha_cleanup':False})
status_path=out/'STATUS.json'; status=read(status_path)
queue=base/'CURL_REVISION_QUEUE_CURRENT.json'
counts=read(queue)['counts']
assert counts['existing_images']==176 and counts['pending_first_image']==131 and counts['current_policy_static_candidate']==22
supplemental=[
 'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json',
 'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v03.json',
 'review/PHOTOGRAPHY_PREP_EIGHT_MORE_STATIC_CANDIDATES_20261103_v01/PRIMARY_EIGHT_STATIC_PHOTOGRAPHY_REVIEW.json',
 'review/SOL_PHOTOGRAPHY_EIGHT_MORE_CURRENT_STATIC_20261103_v01.json',
 'review/SOURCE_G13_19_HAND_VISIBLE_RANGE_20261103_v01.json',
 'review/PRIMARY_G13_19_VISIBLE_UNION_SOURCE_SCOPE_20261103_v01.json',
 'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01.json',
 'drawings/ART-G51-09/v01/prep_first_api_source4617_openeyes_single_downleft_glove_fullshoes_graygreen_v06/ROOT_PREVIEW_PATH_GUARD_FAILURE_BEFORE_HTTP.json',
 'drawings/ART-G51-11/v01/prep_first_api_source4630_roundeyes_asymmetric_outward_low_gloves_fullshoes_graygreen_v06/PREP_SUMMARY.json',
 'GOAL_CURRENT_REQUIREMENTS.md',
]
batch={'recorded_utc':datetime.now(timezone.utc).isoformat(),'checkpoint':ev(status_path),'records':records,
 'known_saved_new_FIRSTs':4,'known_saved_new_builtin_returns':3,'supplemental_evidence':[ev(base/p) for p in supplemental],
 'revision_counts':counts,'user_latest_eye_instruction':'这种没事',
 'eye_tolerance':'G51-10 whole tiny corner marks are present but permitted; not a successful dot deletion, not whole-art approval. Old report retained; fresh v02 and root retain static candidate. No further dot-only generation.',
 'curl_baseline_scope':'Only X01-01 curl drawing method: hollow two large plus one small C, continuous opaque gray returns and thin mint. Size/axis/occlusion follow own PV.',
 'photography':'20 single-source review proposals across19 states;19 unconditional and1 conditional X01-07. No production selection or exposure binding.',
 'G13_19':'Graybob fixed, but current whole still repair for invented common hidden index bridge and third cap leaf; six original exposures preserved. G13-20 family gate closed.',
 'G51_11':'First PREP only, no call or root release and not counted drawn.',
 'all_new_generation_terminal':True,'goal_status':'active','goal_complete':False,'continuous_playback_validated':False,
 'user_accepted_whole_art':False,'no_reset':True,'no_G49_extra_operation':True,'no_Git_push':True}
jp=out/'BATCH_ARTIFACTS.json';create(jp,batch)
link=lambda label,p:f'[{label}]({str(p).replace(chr(92),chr(47))})'
md=['# 本轮图稿与当前要求','',
 '眼部按用户最新“这种没事”：G51-10 whole 眼角小短点可保留，不再为这些点重复生成；保留旧退修记录与新容差复核。该确认只限眼部细节。','',
 '钻发以 X01-01 的绘法为基线：空心两大卷加一个小末卷，实际灰返回连续，挑染为细边；大小、朝向和遮挡按各帧原 PV。','',
 '累计176个状态已有图，131个未出首图；最新要求下22个静态候选，154个已有稿仍列待修。','',
 '| 状态／原帧 | 版本／静态状态 | 图稿 | 提示词 | 方式 |','| --- | --- | --- | --- | --- |']
for r in records:
    good='静态候选' if r['static_review_passed'] else '待修（历史版本保留）'
    md.append(f"| {r['id']}／"+'/'.join('F'+str(f) for f in r['source_frames'])+f" | {r['operation']}／{good} | "+link('原RGBA',r['raw']['path'])+' · '+link('白底',r['white']['path'])+' | '+link('完整提示词',r['prompt']['path'])+' | '+('官方API high，n1/retry1，实际0' if r['operation']=='FIRST' else '内置imggen一次，模型/quality未暴露')+' |')
md+=['', 'G13-19 整体修复已改灰bob，但仍补全未知指桥、帽饰多第三叶，继续待修；不据此展开下一同组调用。G51-11 仅准备完成，尚未调用。','',
 '9组新定位对照经实际双评；索引共20组单原帧候选，X01-07保留为比例残差条件项，绑定前须解决。摄影候选不等于全曝光或动态通过。','',
 link('眼角容差正式记录',base/supplemental[0])+' · '+link('当前goal要求',base/'GOAL_CURRENT_REQUIREMENTS.md')+' · '+link('20组定位索引',base/supplemental[1]),'',
 link('全部回执及SHA记录',jp)+'。GOAL保持active且未完成；无新曝光绑定、实际播放认证、额度重置、G49额外调用或Git推送。','']
mp=out/'BATCH_ARTIFACTS.md'
with mp.open('x',encoding='utf-8') as f:f.write('\n'.join(md))
gp=base/'GOAL_EXECUTION.json';goal=read(gp)
create(out/'GOAL_BEFORE_BATCH_INDEX.json',goal)
if goal.get('latest_batch_artifacts'):goal.setdefault('batch_artifact_history',[]).append(goal['latest_batch_artifacts'])
goal['latest_batch_artifacts']={'json':ev(jp),'markdown':ev(mp),'checkpoint':ev(status_path),'scope':'four FIRST plus three builtin known returns, explicit user eye tolerance and9 fresh source placement proposals','goal_complete':False,'user_accepted_whole_art':False}
gp.write_text(json.dumps(goal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'batch_json':ev(jp),'batch_markdown':ev(mp),'known_saved_returns':len(records),'revision_counts':counts},ensure_ascii=False))
