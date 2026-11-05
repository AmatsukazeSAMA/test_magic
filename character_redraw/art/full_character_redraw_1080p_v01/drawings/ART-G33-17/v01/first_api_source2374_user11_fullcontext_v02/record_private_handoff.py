from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image

R=Path(__file__).resolve().parent
D=R/'artist_return_diagnostics_v01'
B=R.parents[3]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
def save(p,v):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
result=read(R/'result.json');attempt=read(R/'attempt.json');lock=read(R/'AUTHORIZED_CALL_LOCK.json')
assert attempt['status']=='completed' and attempt['api_calls']==1 and attempt['automatic_retries']==0
assert attempt['http_status']=='200' and attempt['curl_exit_code']==0
assert sha(R/'character_api_original.png')==result['output_sha256']=='3bd6d12bef111c96b0b0d81d3eb049a13237d4780f52b7960260b7e940ac8e84'
assert result['elapsed_seconds']==25.618
for e in lock['references']+lock['preserved_originals']:assert sha(e['path'])==e['sha256']
viewed=[R/'character_api_original.png',R/'qa_white.png',R/'qa_black.png']
viewed += [D/n for n in ['HEAD_EAR_ROOT_COIL_white_1x.png','COIL_NORMAL_white_1x.png','COIL_NORMAL_white_3x.png','COIL_NORMAL_black_3x.png','CAP_LEAVES_white_2x.png','EYES_white_2x.png','BOTH_SHOES_white_1x.png']]
source_review=read(R/'ARTIST_REFERENCE_REVIEW.json')
findings=[
 {'criterion':'原PV动作/表演/衣装/裁切','private_result':'基本保留，整体摄影比例仍待root实核','observation':'与原2374 full/guide及895/898对照：右向正面3/4、双圆睁mono眼普通小圆白点、小闭弧笑、两手腰后/画左外肘弯、黑长袖红bow金扣白肩frill袖口围裙腰后带及不同行腿鞋基本保留；两只踝带鞋完整见于画内，不是首段半身裁切。'},
 {'criterion':'固定LEFT根侧/连接','private_result':'P1_REPAIR_REQUIRED','observation':'返图根珠约raw[191..226,229..245]接在画左可见近耳下、画左肩前；原头向画右，画左可见耳属近侧，唯一解剖LEFT应在远侧低nape。本图根高度低且珠卷接通，但所属侧错误；不能把“低根”当作侧别合格。不得镜像整人。'},
 {'criterion':'帽饰','private_result':'P1_REPAIR_REQUIRED','observation':'CAP_LEAVES_white_2x明确见三独立黑形：帽后小尖叶、直立叶、朝画右叶。源及要求恰两黑叶，新增小尖叶需修，白maidcap仍存在。'},
 {'criterion':'灰螺旋卷形/返回与尖C','private_result':'待root/Sol复核，不认证完整形态','observation':'正常尺度及3x见宽灰前面、较薄mint沿边、收细下段及C钩；不是仅因灰色或椭圆投影就判坏。上两圈前面较平行，薄返面在夹缝，连续绕行读法仍需root独立核；不能凭下C正确认证上端。错侧根已构成整稿P1。'},
 {'criterion':'发量与相对体量','private_result':'当前可见态未见极端粗大或微型挂件，空间错误仍未通过','observation':'先在完整头肩/上臂图再看正常卷局部：卷有足量宽灰面，长度到胸结附近，未按R50 10x17裁片缩成tiny饰物；与用户正确11完整head/coil上下文对照，仍须在正确远侧投影/前态actual中核体量，不能拿本错侧尺寸作后续模板。'},
 {'criterion':'材料平涂','private_result':'待root细核','observation':'灰主面与细mint可读，未全mint化。3x首圈灰面有轻微软色差，bob/裙围裙亦有软灰变化；不能以技术像素判断艺术通过，不将其光照升级为新默认。所有gray前返仍须按无光照要求审核。'},
 {'criterion':'肩前路径/真实遮挡与透明','private_result':'空间侧别P1；隐藏几何未认证','observation':'当前卷在画左近肩/红结前，是错误根侧的前置路径；不能等同承接前20正确LEFT肩前路径。白黑完整QA未显原粉背景/字幕，原raw透明A0区域隐藏灰黑RGB的光斑在两底不显，不能描成背景。当前衣后/发内隐藏结构不可观察。'},
 {'criterion':'相邻PTS动态连续','private_result':'PENDING_UNVALIDATED','observation':'前G12-20 F892..894仍肩前修复待actual；本17 F895..898独立首图本次仅静态查看，无实际原速/慢速已绑定播放，不声明动态连贯或用户接受。'},
]
review={'id':'ART-G33-17','reviewer':'xhigh_pending_artist private draft only','reviewed_utc':now,
 'state':'HOLD_REPAIR_REQUIRED_PENDING_ROOT_SOL_FRESH_REVIEW','exact_raw':ev(R/'character_api_original.png'),
 'actual_viewed_return_paths':[ev(p) for p in viewed],
 'actual_source_and_reference_evidence':source_review,
 'findings':findings,'root_and_Sol_have_not_been_substituted_by_artist':True,
 'primary_static_pass':False,'independent_static_pass':False,'user_accepted':False,'dynamic_validated':False,'photography_validated':False,
 'API_calls':1,'native_calls':0,'automatic_retries':0,'inflight':0,
 'no18_generation_or_prepare_progressed':True,'central_write':False,'REGPLAN_central_changed':False,'exposure_binding_changed':False,'quota_reset_used':False}
save(D/'ARTIST_PRIVATE_RETURN_REVIEW.json',review)
receiptpaths=[R/x for x in ['character_api_original.png','api_response.raw.json','request_manifest.json','response_headers.txt','result.json','attempt.json','ARTIST_API_EXECUTION_RECEIPT.json','API_PREPARED_REQUEST.json','DRAFT_API_REQUEST_v02.json','AUTHORIZED_CALL_LOCK.json','ROOT_SPECIFIC_RELEASE.json','PROJECT_SCOPE_REFERENCE_RELEASE.json','prompt.txt','qa_white.png','qa_black.png']]
handoff={'id':'ART-G33-17','run':str(R),'recorded_utc':now,
 'status':'KNOWN_RETURN_ARTIST_HOLD_WRONG_NEAR_SIDE_ROOT_PLUS_EXTRA_CAP_LEAF',
 'raw':ev(R/'character_api_original.png'),'Size':[560,1216],'provider':'OpenAI API','model':'gpt-image-2.5-sunburst','quality':'high',
 'elapsed_seconds':result['elapsed_seconds'],'http_status':attempt['http_status'],'curl_exit_code':attempt['curl_exit_code'],
 'API_calls':1,'native_calls':0,'n':1,'automatic_retries':0,'live_session_id':77798,'session_status':'terminal_exit0','inflight':0,
 'all_original_receipts_preserved':[ev(p) for p in receiptpaths],
 'artist_private_review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'technical_QA':ev(D/'TECHNICAL_QA.json'),
 'P1':['唯一解剖LEFT根错搬至画左可见近耳','黑帽叶由2变3'],
 'retained_observations':['原开眼小笑/腰后手及衣身基本保','原两鞋完整','宽灰/薄mint/C可读，形态及材料仍待独立复核'],
 'stop_boundary':'一图即停，不重试/不native修/不18，等待root；0中央/曝光/绑定/REGPLAN改写，quota reset未使用',
 'preserved_originals_unchanged':[{'path':x['path'],'sha256':sha(x['path']),'matches_before':sha(x['path'])==x['sha256']} for x in lock['preserved_originals']]}
save(D/'ARTIST_RETURN_HANDOFF.json',handoff)
print(json.dumps({'review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'handoff':ev(D/'ARTIST_RETURN_HANDOFF.json'),'raw':ev(R/'character_api_original.png'),'elapsed_seconds':25.618,'API_calls':1,'inflight':0},ensure_ascii=False,indent=2))
