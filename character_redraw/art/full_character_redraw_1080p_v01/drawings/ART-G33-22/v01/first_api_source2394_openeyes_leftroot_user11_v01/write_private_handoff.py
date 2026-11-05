from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
raw=R/'character_api_original.png';assert sha(raw)=='612a02647fb0dc55e08a300c1a4bf4ed706bca278d817ce1b588a23dce971e7e'
pv=read(R/'INPUT_PROVENANCE.json');res=read(R/'result.json');attempt=read(R/'attempt.json');lock=read(R/'REQUEST_LOCK.json');now=datetime.now(timezone.utc).isoformat()
assert attempt['status']=='completed' and attempt['api_calls']==1 and attempt['automatic_retries']==0
for k in ['JOB','REGISTRATION_PLAN']:assert sha(lock[k]['path'])==lock[k]['sha256']
view=[raw,R/'qa_white.png',R/'qa_black.png',Path(pv['source_full']['path']),Path(pv['first_scene_source']['path']),Path(pv['source_guide']['path']),Path(pv['refs'][1]['source']['path']),Path(pv['previous_current']['image'])]
view += [Path(x['path']) for x in pv['refs']]
view += [R/'diagnostics'/n for n in ['ROOT_COIL_white_1x.png','ROOT_COIL_white_3x.png','ROOT_COIL_black_3x.png','CAP_TWO_LEAVES_white_3x.png','SOURCE2394_CAP_LEAF_ATTACHMENT_3x_READONLY.png','EYES_MOUTH_white_3x.png','SKIRT_GRIP_HAND_white_3x.png','BOTH_SHOES_white_1x.png','SOURCE2394_vs_API22_FULL_1x_READONLY.png']]
review=put('DRAFT_PRIMARY_REVIEW.json',{
 'id':'ART-G33-22','created_utc':now,'reviewer':'xhigh_pending_artist private visual draft; not root or Sol',
 'image':str(raw),'exact_raw_sha256':sha(raw),'actual_viewed':[rec(p) for p in view],
 'decision':'HOLD_CAP_EXTRA_BLACK_TIP_AND_HAIR_MATERIAL_PENDING_ROOT',
 'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
 'source_action_expression':{'observation':'明显睁开的原弧形双眼及小闭口笑保住，非AI举指/O口；眼3x未见独立黑中心+灰外环，charcoal主fill与普通白点可保。原前臂低握裙束点/曲指、另一臂在背后遮挡、横向画左黑裙折片、白apron/腰后bow与不同行腿角/踝带/完整两鞋均可保留。','boundary':'未做摄影匹配、逐源线或真实曝光动态验证。'},
 'root':{'observation':'唯一低位双红珠与灰卷位于画右bob下缘/耳后nape，低于睁眼水平，不在画左近耳，身体未镜像。','artist_assessment':'原大关系可保；不同时认证卷全部几何。'},
 'cap':{'observation':'两片长黑叶之外，结下多出朝下短尖黑瓣；source2394帽叶attachment只见两叶和厚连接底，没有这片向下独立尖瓣。已对照source原像素crop和当前cap3x。','priority':'P1_repair_requested','source_crop':{'source':pv['source_guide'],'crop_xyxy':[425,40,505,130],'scale':3,'path':str(R/'diagnostics/SOURCE2394_CAP_LEAF_ATTACHMENT_3x_READONLY.png')},'boundary':'不自行改艺术像素或按自动数叶通过；交root fresh实看。'},
 'curl':{'observation':'整头肩中是可见完整宽gray为主的卷，mint较薄；根位低、末C明确，未成薄绿小柱。上端front仍偏横椭圆帽读法，圈间能见gray斜返回，但内返有较深灰杂纹/体积感，未稳定达到所有gray面同色无打光。','assessment':'HOLD upper continuous-return reading and material; cannot use as master.','boundary':'不以没固定洞数判实心，不删grayopaque返回面；真正被前/返回互遮的内腔不可认证。末C也不代上端通过。'},
 'transparent_background':{'observation':'raw A0隐藏RGB带灰glow，完整白黑实际不见实体背景或独立特效；没有因此代码清RGB或改人物。','technical_only':True},
 'temporal':{'actual_previous':'ART-G12-25 first910..913 current30831370','current':'ART-G33-22 first914..916','actual_next':'ART-G33-23 first917..919 not drawn','not_previous_family21':True,'dynamic_validated':False,'observation':'只静态原片/邻current比较，不声称根/发量/摆动时序已经连续。'},
 'issues_for_root':[{'priority':'P1','part':'cap leaf attachment','description':'两长叶外向下短尖黑瓣，与原两叶连接底不同。'},{'priority':'P1_review_requested','part':'hair returns/flat material','description':'内返回暗纹/graysoft明暗，上端封口片读感待fresh判断。'}],
 'API_calls':1,'automatic_retries':0,'native_calls':0,'result_unknown':False,
 'JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'binding_modified':False,'progress_modified':False,
 'user_accepted':False,'dynamic_validated':False,'next_action':'本首图结束停交root，不自动修或画下一稿。',
})
receipt=put('PRIVATE_CALL_RECEIPT.json',{
 'id':'ART-G33-22','created_utc':now,'tool':'exec_command require_escalated approved official wrapper',
 'exec_session_id':21624,'status':'known_completed','provider':res['provider'],'model':res['model'],'quality':res['quality'],
 'actual_size':[624,1072],'background':res['background'],'elapsed_seconds':res['elapsed_seconds'],
 'API_calls':1,'native_calls':0,'automatic_retries':0,
 'raw':rec(raw),'formal_request':rec(R/'API_PREPARED_REQUEST.json'),'lock':rec(R/'REQUEST_LOCK.json'),
 'effective_prompt':rec(R/'prompt_effective.txt'),'broad_authorization':rec(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),'root_release':rec(R/'ROOT_SPECIFIC_RELEASE.json'),
 'original_response':rec(R/'api_response.raw.json'),'response_headers':rec(R/'response_headers.txt'),'attempt':rec(R/'attempt.json'),'result':rec(R/'result.json'),'manifest':rec(R/'request_manifest.json'),
 'technical_success_is_not_art_pass':True,
})
handoff=put('ARTIST_HANDOFF.json',{
 'id':'ART-G33-22','created_utc':now,'status':'KNOWN_FIRST_API_RETURN_PRIVATE_HOLD',
 'run':str(R),'raw':rec(raw),'actual_size':[624,1072],'elapsed_seconds':26.082,'provider':res['provider'],'model':res['model'],'quality':'high',
 'API_calls':1,'automatic_retries':0,'native_calls':0,'inflight':0,
 'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),
 'normal_coil':rec(R/'diagnostics/ROOT_COIL_white_1x.png'),'coil3x_white':rec(R/'diagnostics/ROOT_COIL_white_3x.png'),'coil3x_black':rec(R/'diagnostics/ROOT_COIL_black_3x.png'),
 'cap3x':rec(R/'diagnostics/CAP_TWO_LEAVES_white_3x.png'),'source_cap3x':rec(R/'diagnostics/SOURCE2394_CAP_LEAF_ATTACHMENT_3x_READONLY.png'),
 'source_comparison':rec(R/'diagnostics/SOURCE2394_vs_API22_FULL_1x_READONLY.png'),
 'private_review':review,'call_receipt':receipt,'technical_return':rec(R/'TECHNICAL_RETURN_QA.json'),
 'artist_observation':'原睁眼小笑/root/手衣/完整两鞋保留；两长帽叶下多短尖黑瓣，coil内返回暗纹/softgray与上端连接HOLD。',
 'preserved':'raw原样、全部response/header/attempt、6refs来源/提示及effective、full QA和私评',
 'central_registry_modified':False,'binding_modified':False,'progress_modified':False,'JOB_REGPLAN_modified':False,'quota_resets':0,
 'not_art_pass':True,'not_dynamic_pass':True,'no_following_item_started':True,
})
print(json.dumps({'raw':rec(raw),'review':review,'receipt':receipt,'handoff':handoff,'API_calls':1,'inflight':0},ensure_ascii=False,indent=2))
