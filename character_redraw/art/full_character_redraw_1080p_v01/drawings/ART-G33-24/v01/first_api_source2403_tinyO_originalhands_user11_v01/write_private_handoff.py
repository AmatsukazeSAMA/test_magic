from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
raw=R/'character_api_original.png';expected='b7fc52e64ff4d85947fb7adc1d792107da222354c791ceef68d1b1ae632ae5d9'
assert sha(raw)==expected
pv=read(R/'INPUT_PROVENANCE.json');res=read(R/'result.json');att=read(R/'attempt.json');lock=read(R/'EXECUTION_LOCK_v01.json');now=datetime.now(timezone.utc).isoformat()
assert att['status']=='completed' and att['api_calls']==1 and att['automatic_retries']==0
for k in ['JOB','REGISTRATION_PLAN','immutable_prep_lock','formal_request']:assert sha(lock[k]['path'])==lock[k]['sha256']
view=[raw,R/'qa_white.png',R/'qa_black.png',Path(pv['source_full']['path']),Path(pv['source_guide']['path']),Path(pv['first_scene_source']['path']),Path(pv['refs'][1]['source']['path'])]+[Path(x['path']) for x in pv['refs']]
view += [R/'diagnostics'/n for n in ['ROOT_COIL_white_1x.png','ROOT_COIL_white_3x.png','ROOT_COIL_black_3x.png','CAP_V_ATTACHMENT_white_3x.png','SOURCE2403_vs_API24_FULL_1x_READONLY.png','EYES_TINY_O_white_3x.png','HIGH_POINTING_HAND_white_3x.png','LOW_CURLED_HAND_white_3x.png','BOTH_SHOES_white_1x.png']]
review=put('DRAFT_PRIMARY_REVIEW.json',{
 'id':'ART-G33-24','created_utc':now,'reviewer':'xhigh_pending_artist private actual-view draft; not root or Sol',
 'image':str(raw),'exact_raw_sha256':expected,'actual_viewed':[rec(x) for x in view],
 'decision':'VISIBLE_STATIC_CANDIDATE_WITH_REVIEW_POINTS_PENDING_FRESH_ROOT_SOL',
 'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
 'canonical_source':'2403/PTS1282880 verified by JOB+original sourcePROVENANCE/catalog+PRIORITY; first920..922/PTS491152..492752.',
 'source_action_eyes':{'observation':'原睁开弧/单charcoal普通白点与tinyO保留；画左前臂更竖、高手长指斜向画右上及原折指外形，另一画右低位小曲指/掌轮廓均保。没有沿23手势或AI手/嘴。全apron朝画右斜摆、源腰后白bow/黑裙右扬、两腿异角/踝带和完整两鞋保。','assessment':'当前主要源动作/可见手眼衣脚可保留；摄影定位和逐源线精度留root。'},
 'root_cap':{'observation':'唯一红双珠在画右同侧低耳后/nape、短bob自然邻接，没换画左近耳或抬到眼高；白maidcap和两长黑叶在，共同底有短尖。','cap_boundary':'按root最新对20/22/23同类短公共基部P2意见，本稿短底先记P2，不把正常连接底要求为0或自动触发整人生图；独立第三长叶/漏帽与此不同。'},
 'visible_curl':{
  'observation':'正常全头肩比例下有宽gray前面、斜向gray返回连接及连贯渐收C，不是微型细绿柱，也未扩大成巨束。上端可见前面与返回片互相盖叠，末C邻黑肩袖外侧。',
  'material_review_point':'gray主面/mint边仍有轻微柔灰与灰绿边混色，返回处深浅差可见；不在私评中声称全部flat严格已通过，请root/Sol fresh判断。未见需要本代理立即二次生成的新明确P1。',
  'boundary':'没有因无固定孔数把opaquegray返回挖洞；视角遮住的内腔/隐藏段不能认证，上端返回不由末C或整体锥轮廓单独保证。',
 },
 'spatial_temporal_boundary':'当前卷邻bob/白frill/黑袖，真实相邻相位/遮挡和发量连续需按920..922曝光另看；没有实际播放/摄影验证，不授动态通过。',
 'transparency':'raw A0隐藏RGB有灰glow，完整white/black不见独立实体背景；未清RGB或改原艺术像素。技术alpha和HTTP200不代艺术验收。',
 'review_points':[{'priority':'P2','part':'cap shared short base','observation':'同类短共同底，遵循root最新P2口径，不自动重绘。'},{'priority':'fresh_review','part':'hair material/upper-return readability','observation':'轻softgray/灰绿混色及返回深浅差，freshroot/Sol判断，不把候选当master。'}],
 'API_calls':1,'automatic_retries':0,'native_calls':0,'result_unknown':False,
 'source_JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'binding_modified':False,'progress_modified':False,
 'user_accepted':False,'dynamic_validated':False,'next_action':'首图一张结束交root/Sol，无自主native/第二API或下一状态。',
})
receipt=put('PRIVATE_CALL_RECEIPT.json',{
 'id':'ART-G33-24','created_utc':now,'tool':'exec_command require_escalated official exact-lock runner',
 'exec_session_id':72999,'status':'known_completed','API_calls':1,'automatic_retries':0,'native_calls':0,
 'provider':res['provider'],'model':res['model'],'quality':res['quality'],'size_actual':[624,1072],'background':res['background'],'elapsed_seconds':res['elapsed_seconds'],
 'raw':rec(raw),'formal_request':rec(R/'API_PREPARED_REQUEST.json'),'request_lock':rec(R/'REQUEST_LOCK.json'),'execution_lock':rec(R/'EXECUTION_LOCK_v01.json'),
 'root_release':rec(R/'ROOT_EXECUTION_RELEASE_v01.json'),'scope_proof':rec(R/'AUTHORIZATION_SCOPE_CHECK_v01.json'),'broad_authorization':rec(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
 'no_send_preview':rec(R/'API_PREVIEW_PROOF_v01.json'),'effective_prompt':rec(R/'prompt_effective.txt'),
 'original_response':rec(R/'api_response.raw.json'),'headers':rec(R/'response_headers.txt'),'attempt':rec(R/'attempt.json'),'result':rec(R/'result.json'),'manifest':rec(R/'request_manifest.json'),
 'only_locked6_drawing_refs_sent':True,'technical_success_not_art_acceptance':True,
})
handoff=put('ARTIST_HANDOFF.json',{
 'id':'ART-G33-24','created_utc':now,'state':'KNOWN_ONE_FIRST_API_RETURN_VISIBLE_CANDIDATE_PENDING_ROOT_SOL',
 'run':str(R),'raw':rec(raw),'actual_size':[624,1072],'elapsed_seconds':25.948,'model':res['model'],'quality':'high','background':'transparent',
 'API_calls':1,'automatic_retries':0,'native_calls':0,'inflight':0,
 'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),
 'normal_coil':rec(R/'diagnostics/ROOT_COIL_white_1x.png'),'coil3x_white':rec(R/'diagnostics/ROOT_COIL_white_3x.png'),'coil3x_black':rec(R/'diagnostics/ROOT_COIL_black_3x.png'),
 'source_comparison':rec(R/'diagnostics/SOURCE2403_vs_API24_FULL_1x_READONLY.png'),
 'private_review':review,'call_receipt':receipt,'technical_return':rec(R/'TECHNICAL_RETURN_QA.json'),
 'observation_summary':'原2403 tinyO/开眼/高手斜右上与低曲指/裙右斜摆/完整鞋、低LEFT根保；宽gray前返回+C可见，短帽公共底P2按root口径保留，gray/mint轻混色等freshreview。',
 'central_registry_modified':False,'binding_modified':False,'progress_modified':False,'JOB_REGPLAN_modified':False,'quota_resets':0,
 'fresh_root_and_Sol_required':True,'art_accepted':False,'dynamic_validated':False,'no_following_item_started':True,
})
print(json.dumps({'raw':rec(raw),'review':review,'receipt':receipt,'handoff':handoff,'API_calls':1,'inflight':0},ensure_ascii=False,indent=2))
