from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
B=R.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):return {'path':str(p),'sha256':sha(p)}
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return record(p)
raw=R/'character_api_original.png'
assert sha(raw)=='289aabbd6fb2b694adecf550a0fede43e5e8e4fdfe063dd9e95e62f0e750f46e'
result=json.loads((R/'result.json').read_text(encoding='utf-8-sig'))
provenance=json.loads((R/'INPUT_PROVENANCE.json').read_text(encoding='utf-8-sig'))
now=datetime.now(timezone.utc).isoformat()
view=[raw,R/'qa_white.png',R/'qa_black.png',Path(provenance['source_full']['path']),Path(provenance['first_source']['path']),Path(provenance['source_original_guide']['path'])]
view += [Path(x['path']) for x in provenance['refs']]
view += [Path(provenance['neighbor_snapshots'][k]['image']) for k in ['ART-G12-23','ART-G12-25']]
view += [R/'diagnostics'/n for n in ['ROOT_COIL_white_1x.png','ROOT_COIL_white_3x.png','ROOT_COIL_black_3x.png','EYES_MOUTH_white_3x.png','SKIRT_GRIP_HAND_white_3x.png','BOTH_SHOES_white_1x.png','SOURCE2385_vs_API20_FULL_1x_READONLY.png']]
review={
 'id':'ART-G33-20','created_utc':now,'reviewer':'xhigh_pending_artist private draft; not root or Sol',
 'image':str(raw),'exact_raw_sha256':sha(raw),'actual_viewed':[record(p) for p in view],
 'decision':'HOLD_FOR_FRESH_ROOT_ART_REVIEW_UPPER_RETURN_AND_MATERIAL',
 'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
 'source_expression':{'observation':'双眼完全闭合睫弧、小闭口曲笑；未跟AI/正确11睁眼，没有虹膜、眼白或白点。原头倾和近正面视角基本保留。','artist_assessment':'可保留；root独立新看必要'},
 'source_hands_body':{'observation':'前臂斜向画左下，曲指髋侧抓黑裙、白袖口和原腰后臂遮挡可保；白围裙长摆朝画左、腰后白bow、两腿不同行角、踝带及两只完整鞋均在。全身未截成907半身。','artist_assessment':'原大动作与可见手脚基本保留；摄影和源线精度未核通过'},
 'root_cap':{'observation':'唯一红珠/卷在画右同侧低耳后/nape，珠位低于闭眼线；短bob自然邻接，不在画左近耳。白帽+恰好两独立黑叶可见。','artist_assessment':'可保留；不因此批准卷内部几何'},
 'curl_shape_volume':{
  'observation':'整头肩尺度下是一束可见完整卷，宽gray面为主、mint较薄，末C明确；没有旧薄绿小柱。下端C开放，正常尺度上端仍读成几个横向封口椭圆帽样front，圈间是灰色斜向连接/纹理片。3x能见gray连接，但上端前面如何翻入返回面再进下一圈的连续路径不够清楚。',
  'assessment':'HOLD：请root/Sol对上端连接与封口叠片风险实看；不可仅凭末C或整体锥形通过。',
  'not_claimed':'未把所有gray返回片当空气，未因没有指定洞数自动判实心；隐藏拓扑不可认证，也未提出固定孔/轴/长度。',
 },
 'material':{
  'observation':'gray主面比例和mint薄带方向较合理；但bob及卷正面仍有柔和明暗差，卷内连接有灰色斑驳/暗纹，未达到单一无光照flat的清楚读法。黑裙也有软渐色。',
  'assessment':'HOLD：不把技术high或整体灰主色当平涂通过。需root判断修整，不能直接作为新的卷结构/材质模板。',
 },
 'transparent_layer':{
  'observation':'raw隐藏RGB带灰色光晕，完整white/black合成不见实体背景/独立光效；因此不把A0的RGB当发面或背景实体。alpha最大254、背景包含429389个A0，原字节保留。',
  'boundary':'这些统计只描述技术透明层；完整白黑实际查看仍是艺术边缘检查依据。',
 },
 'registration':{'observation':'source/new同624×1072对照中cap/脸腰位置略有差，整人摄影和原907半身匹配未做；不局部变形或自行绑定。','validated':False},
 'temporal':{'actual_previous':'ART-G12-23 first903..906','current':'ART-G33-20 first907..909','actual_next':'ART-G12-25 first910..913','not_family19':True,'observation':'前后current仅静态比较身份及卷体压紧读法，未按真实曝光播放，不认证大小/根/摆动连续性。','dynamic_validated':False},
 'issues_for_root':[{'priority':'P1_review_requested','part':'coil upper turns/returns','observation':'上端仍有封口横片读法，返回连接的方向不够清楚；末C正确不能替上端通过。'},{'priority':'P1_review_requested','part':'flat hair material','observation':'bob/coil柔灰光和返回斑驳暗纹仍可见。'}],
 'API_calls':1,'automatic_retries':0,'native_calls':0,'unknown_result':False,
 'central_registry_modified':False,'binding_modified':False,'progress_modified':False,
 'JOB_and_REGISTRATION_PLAN_unchanged':True,'art_accepted':False,'dynamic_validated':False,
 'next_action':'一图结束停交root；无自主修复/第二次/API/native/下一稿。',
}
review_proof=put('DRAFT_PRIMARY_REVIEW.json',review)
receipt=put('PRIVATE_CALL_RECEIPT.json',{
 'id':'ART-G33-20','created_utc':now,'tool':'exec_command require_escalated approved official wrapper',
 'exec_session_id':25992,'status':'known_completed','API_calls':1,'native_calls':0,'automatic_retries':0,
 'model':result['model'],'quality':result['quality'],'size_requested':result['size'],'size_actual':[624,1072],
 'background':result['background'],'elapsed_seconds':result['elapsed_seconds'],
 'raw':record(raw),'formal_request':record(R/'API_PREPARED_REQUEST.json'),'request_lock':record(R/'REQUEST_LOCK.json'),
 'effective_prompt':record(R/'prompt_effective.txt'),'auth':record(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
 'root_specific_release':record(R/'ROOT_SPECIFIC_RELEASE.json'),
 'preserved_original_response':record(R/'api_response.raw.json'),'response_headers':record(R/'response_headers.txt'),
 'attempt':record(R/'attempt.json'),'result':record(R/'result.json'),'manifest':record(R/'request_manifest.json'),
 'paid_success_not_art_pass':True,
})
handoff=put('ARTIST_HANDOFF.json',{
 'id':'ART-G33-20','created_utc':now,'status':'KNOWN_FIRST_API_RETURN_ARTIST_HOLD_PENDING_ROOT',
 'run':str(R),'raw':record(raw),'actual_size':[624,1072],'provider':result['provider'],'model':result['model'],'quality':'high','elapsed_seconds':24.717,
 'API_calls':1,'automatic_retries':0,'native_calls':0,'inflight':0,
 'full_white_QA':record(R/'qa_white.png'),'full_black_QA':record(R/'qa_black.png'),
 'normal_coil':record(R/'diagnostics/ROOT_COIL_white_1x.png'),'coil3x_white':record(R/'diagnostics/ROOT_COIL_white_3x.png'),'coil3x_black':record(R/'diagnostics/ROOT_COIL_black_3x.png'),
 'source_comparison':record(R/'diagnostics/SOURCE2385_vs_API20_FULL_1x_READONLY.png'),
 'private_review':review_proof,'technical_return':record(R/'TECHNICAL_RETURN_QA.json'),'call_receipt':receipt,
 'preserved':'original raw, full JSON response, headers, request/effective prompt, all6refs/provenance, QA and failure/HOLD observations',
 'artist_observation_summary':'闭眼/小笑、画右低LEFT根+2叶、源抓裙及后臂、两踝带和完整鞋保留；卷体gray主面/末C可见，但上端封口片读法与柔灰光/return暗纹HOLD。',
 'parent_action':'fresh root actual review/Sol排队；不要把私评当primary/independent pass。',
 'central_registry_modified':False,'bindings_modified':False,'JOB_or_REGPLAN_modified':False,'quota_resets':0,
 'no_following_cel_requested':True,
})
print(json.dumps({'review':review_proof,'receipt':receipt,'handoff':handoff,'raw':record(raw),'API_calls':1,'inflight':0},ensure_ascii=False,indent=2))
