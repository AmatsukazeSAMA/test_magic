from pathlib import Path
from datetime import datetime, timezone
import json,hashlib,sys

ROOT=Path(__file__).resolve().parents[5]
B=ROOT/'art/full_character_redraw_1080p_v01'
CEL=Path(__file__).resolve().parent
R=(CEL/'prep_first_api_source4634_closed_smile_horizontal_outward_gloves_fullshoes_graygreen_v06').resolve()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(p,x):
    assert not p.exists(),p
    p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

helper=ROOT/'scripts/Release-RootReviewedFirstApi.py'
stop="release = run / 'ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json'"
code=helper.read_text('utf-8-sig');assert code.count(stop)==1
checks=code.split(stop)[0]
assert checks.count('save(')==1 and 'save(release' not in checks
sys.argv=[str(helper),str(R),'--observation','PREPONLY original guard assertions; not root actual review or release.']
exec(compile(checks,str(helper),'exec'),{'__file__':str(helper),'__name__':'__PREPONLY_GUARD_ASSERTIONS__'})
q=read(R/'API_PREPARED_REQUEST.json');l=read(R/'REQUEST_LOCK.json');v=read(R/'API_PREVIEW_PROOF_PREPONLY.json')
draft=read(R/'DRAFT_API_REQUEST.json')
prompt=Path(q['PromptFile']).read_text('utf-8-sig')
assert prompt.count(l['mandatory_prefix'])==1 and v['effective_prompt_characters']==len(prompt)
assert q['OutputDirectory']==str(R.resolve()) and '\\' in q['OutputDirectory']
for x in read(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json')['files_present_before_PREP']:
    assert sha(x['path'])==x['sha256']
registry=read(B/'ASSET_REGISTRY.json');assert 'ART-G51-12' not in registry
for name in ('attempt.json','result.json','character_api_original.png','character_imggen_original.png',
             'ROOT_API_EXECUTION_RECEIPT.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json',
             'ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json','Invoke-RootReviewedFirstOnce.ps1'):
    assert not list(CEL.rglob(name)),name
compat=R/'FIRST_HELPER_COMPATIBILITY_PREPONLY.json'
save(compat,{'id':'ART-G51-12','checked_utc':datetime.now(timezone.utc).isoformat(),'helper':ev(helper),
    'executed_guard_prefix_sha256':hashlib.sha256(checks.encode('utf-8')).hexdigest(),
    'execution_stopped_before':stop,'all_original_assertions_before_first_ROOT_write_passed':True,
    'formal_exact_eight_fields':True,'Windows_native_OutputDirectory_exact_str_resolve':True,
    'real_preview':ev(R/'API_PREVIEW_PROOF_PREPONLY.json'),'mandatory_prefix_occurrences':1,
    'effective_prompt_characters_match':True,'root_release_created':False,'attempt_created':False,
    'API_native_network_calls':0,'JOB_REG_source_guide_existing_bytes_unchanged':True})
summary={'id':'ART-G51-12','status':'PREPONLY_READY_FOR_ROOT_ACTUAL_REVIEW_NOT_RELEASED','run':str(R),
    'source_frame':4634,'source_pts':2474480,'timebase':'1/16000','source':draft['source'],
    'formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(Path(q['PromptFile'])),'request_lock':ev(R/'REQUEST_LOCK.json'),
    'references':l['references'],'provenance':draft['provenance'],'actual_reference_review':draft['actual_reference_review'],
    'actual_source_observation':draft['actual_source_observation'],'source_action_authority':'Own4634 only',
    'current_policy':draft['requirements'],'curl_scope':draft['curl_scope'],'missing_turn_clarification':draft['user_missing_turn'],
    'eye_tolerance':draft['eye_tolerance'],'wrapper':l['wrapper'],'preview':ev(R/'API_PREVIEW_PROOF_PREPONLY.json'),
    'readonly_helper_compatibility':ev(compat),'predecessor_gate':draft['predecessor_gate'],
    'predecessor_current_registry_readback':registry.get('ART-G51-11'),
    'quality':'high','size':'720x944','n':1,'retry':1,'background':'transparent','operation_kind':'first_drawing',
    'first_drawing':True,'planned_logical_requests':1,'mandatory_prefix_occurrences':1,
    'API_calls':0,'native_calls':0,'network_calls':0,'root_release_received':False,'submitted':False,
    'front_shoulder_route_certified':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
    'central_JOB_REG_registry_index_binding_modified':False}
summarypath=R/'PREP_SUMMARY.json';save(summarypath,summary)
md=R/'PREP_SUMMARY.md';assert not md.exists()
md.write_bytes(('''G51-12 FIRST PREP完成，未释放/未发送。

Own F4634 / PTS2474480：不等圆睁、小闭笑弧；画左腕下折弯指，画右近横并指和下分拇指；裙向画右摆。画左靴较短近竖平底，画右鞋较低前斜，两鞋完整。原左颈后粉瓣排除。动作与眼口不借11。

五参考：完整own guide；11衣内灰绿颜料；用户X01仅卷画法；无眼/旧卷的上bob帽身份；own眼口原矩形。已逐张实际看及核裁界。两大转后另有自己的小灰正面/opaque返回，再收C；2adfb1和4cab79均入锁。肩前深度等待返图实际判断。

720×944 / high / n1 / retry1 / transparent。正式8字段为Windows原生路径；前缀一次。真实Preview与release helper首个写入前的原始只读断言通过，0HTTP/0API/0native。11登记状态按PREP时真实读回记录，付费前由root确认双审及实际输入。未改中央、JOB/REG、索引或绑定。

精确SHA与职责见PREP_SUMMARY.json和INPUT_COPY_AND_CROP_PROVENANCE.json。
''').encode('utf-8'))
print(json.dumps({'summary':ev(summarypath),'markdown':ev(md),'formal':summary['formal'],'prompt':summary['prompt'],
    'lock':summary['request_lock'],'preview':summary['preview'],'helper_compatibility':ev(compat),
    'reference_sha256':[x['sha256'] for x in l['references']],'source':draft['source'],'calls':0},ensure_ascii=False))
