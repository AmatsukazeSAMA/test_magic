from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib

R=Path(__file__).resolve().parent;D=R/'artist_return_diagnostics_v01';C=R.parent
P=C/'first_api_source2374_user11_fullcontext_v02'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();a=read(R/'attempt.json');res=read(R/'result.json')
lock=read(R/'AUTHORIZED_CALL_LOCK_after_shared_prefix_v02.json')
assert a['status']=='completed' and a['api_calls']==1 and a['automatic_retries']==0
assert a['http_status']=='200' and a['curl_exit_code']==0
assert sha(R/'character_api_original.png')==res['output_sha256']=='ddcb5327f416ad04f10ddfdc1bd2d8644f69a12c4506ba118671fbbf83f7f240'
assert sha(R/'prompt_effective.txt')==res['prompt_sha256']=='5295f4d23a6dcaac0989f9ba3629d6b6786b7d5af5cab86135522c5fb191fa01'
assert res['spatial_prefix_applied'] is True and res['elapsed_seconds']==23.192
assert len(res['inputs'])==5
for x in lock['preserved_originals']+lock['references']:assert sha(x['path'])==x['sha256']
assert sha(P/'character_api_original.png')=='3bd6d12bef111c96b0b0d81d3eb049a13237d4780f52b7960260b7e940ac8e84'
viewed=[R/'character_api_original.png',R/'qa_white.png',R/'qa_black.png',C/'inputs/source_pose_guide.png',P/'qa_white.png']
viewed += [D/x for x in ['HEAD_ROOT_COIL_white_1x.png','COIL_white_3x.png','COIL_black_3x.png','CAP_LEAVES_white_2x.png','EYES_white_2x.png','BOTH_SHOES_white_1x.png']]
findings=[
 {'criterion':'用户指定LEFT根侧与低根','result':'可见改善，待root/Sol fresh复核','observation':'原画左近耳下两珠卷已清除；现红珠约raw[322..352,238..258]在画右远侧低颈，与远侧bob边及卷接通，未镜像身体/脸/手脚。珠有下颌/bob自然局部遮挡，卷走画右肩前胸侧；不把根侧改善等同全稿通过。'},
 {'criterion':'帽饰恰两黑叶','result':'P1_REPAIR_REQUIRED','observation':'CAP_LEAVES_white_2x仍有帽后小三角黑尖、直立大叶和朝右大叶，共3独立黑形；明确要求删第三小尖未完成，白maidcap保留。'},
 {'criterion':'连续灰螺旋上端返回/尖C','result':'HOLD_VISIBLE_UPPER_RETURN_READABILITY_REQUIRES_REPAIR_OR_FRESH_INDEPENDENT_RESOLUTION','observation':'下端灰带收细连接C清楚；但正常头肩和3x可见上端几段近封口灰块，以窄绿色链状夹缝分隔，宽GRAY返回弧接续读法弱。与用户正确11完整头卷对照，上端未同样呈现宽发带前返绕行的明确读法；不能仅凭下C正确或整体锥形放行。此处评的是可见上端读法，不凭固定洞数判断、不声称隐藏内部已证实实心。'},
 {'criterion':'体量与投影','result':'未见极端粗大或微型；正确投影体量仍需root核','observation':'卷在完整头肩/胸结尺度有宽灰主面和足量长度，未把R50 tinyROI当固有发量；转到正确远侧后保持一束可见卷而非抹掉整束。具体大小以源转向/正确11上下文和前稿actual复核，不立新全片比例/模板。'},
 {'criterion':'材质与画风','result':'灰主面/细mint可见，软色差待root复核','observation':'没有全mint主面，灰面仍为主体；正常和3x灰面有轻微软调，未据像素统计声明无光照合格。保持所有gray前返同bob灰的要求，不能把本图作为材料master。'},
 {'criterion':'原PV表演/衣手/腿鞋/裁切','result':'基本保留，整体摄影未认证','observation':'与原2374guide+已实看native full对照：朝右正面3/4，原两眼圆睁单色charcoal/小圆白点及小闭弧笑、腰后双手与画左肘腕、黑长袖红bow金扣白frill围裙腰后带、不同方向交错腿和两只完整黑踝带鞋仍在。无近耳旧卷、无身体镜像，构图/服装新增帽叶问题另列P1。'},
 {'criterion':'透明边缘与隐藏几何','result':'完整白黑已实看；隐藏几何未认证','observation':'原raw的A0区有灰黑光斑RGB，但完整白/黑QA不显背景实体，不当发面或背景；maxalpha254留原字节，不修改。实际发内露空/衣后遮挡只能按可见段说明，不认证隐藏圈数或局部alpha数值等于美术通过。'},
 {'criterion':'相邻实际PTS连续','result':'PENDING_NO_DYNAMIC_PASS','observation':'前20肩前修复仍待actual；本17仅完成当前图静态实际查看，未进行已绑定原速/慢速播放，不声明连贯、摄影或用户接受。'}
]
review={'id':'ART-G33-17','reviewer':'xhigh_pending_artist private draft','reviewed_utc':now,
 'state':'HOLD_PENDING_FRESH_ROOT_SOL_NOT_ARTIST_APPROVAL','exact_raw':ev(R/'character_api_original.png'),
 'actual_viewed_paths':[ev(x) for x in viewed],'user_directed_release':ev(R/'USER_DIRECTED_API_REPAIR_RELEASE.json'),
 'reference_review':ev(R/'ARTIST_REFERENCE_REVIEW.json'),'findings':findings,
 'operation_kind':'whole_character_redraw','local_mask_used':False,'parts_spliced':False,
 'mandatory_followup_imggen_whole':False,'mandatory_boundary':'当前API本身是整人重绘，未采用局修/拼接；若后续实际局修/拼接，需新记mandatory imggen whole。',
 'primary_static_pass':False,'independent_static_pass':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'API_calls_this_repair':1,'API_calls_known_17_total':2,'native_calls':0,'automatic_retries':0,'inflight':0,
 '18_not_started':True,'central_write':False,'REGPLAN_central_changed':False,'exposure_binding_changed':False,'quota_reset_used':False}
save(D/'ARTIST_PRIVATE_RETURN_REVIEW.json',review)
files=['character_api_original.png','api_response.raw.json','request_manifest.json','response_headers.txt','result.json','attempt.json','ARTIST_API_EXECUTION_RECEIPT.json','prompt.txt','prompt_effective.txt','API_PREPARED_REQUEST.json','WHOLE_CHARACTER_REPAIR_REQUEST.json','AUTHORIZED_CALL_LOCK.json','AUTHORIZED_CALL_LOCK_after_shared_prefix_v02.json','USER_DIRECTED_API_REPAIR_RELEASE.json','qa_white.png','qa_black.png']
handoff={'id':'ART-G33-17','run':str(R),'recorded_utc':now,'status':'KNOWN_RETURN_ARTIST_HOLD_LOWLEFT_ROOT_CORRECTED_CAP_THIRD_LEAF_REMAINS_UPPER_RETURN_UNRESOLVED',
 'raw':ev(R/'character_api_original.png'),'provider':'OpenAI API','model':'gpt-image-2.5-sunburst','quality':'high','dimensions':[560,1216],
 'elapsed_seconds':23.192,'http_status':'200','curl_exit_code':0,'API_calls_this_repair':1,'API_calls_known_17_total':2,'n':1,'automatic_retries':0,'native_calls':0,
 'live_session_id':15077,'session_status':'terminal_exit0','inflight':0,
 'effective_prompt':ev(R/'prompt_effective.txt'),'spatial_prefix_applied':True,
 'artist_review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'technical_QA':ev(D/'TECHNICAL_QA.json'),
 'receipt_evidence':[ev(R/x) for x in files],
 'retained':['画右远侧低根替代画左错误近耳根','原开眼小笑/腰后手和衣装腿鞋保留','双完整鞋','宽灰主面与下C可见'],
 'remaining':['第三黑尖帽叶仍未删','上端GRAY返回连续读法不足，待root/Sol fresh；不宣称隐藏实心'],
 'stop_boundary':'本次用户定向repair1call已完成，保持0在途；无第三次/无18，等root。中央registry/绑定/曝光/REGPLAN未改；quota reset禁用。',
 'originals_unchanged':[{'path':x['path'],'sha256':sha(x['path']),'matches_before':sha(x['path'])==x['sha256']} for x in lock['preserved_originals']]}
save(D/'ARTIST_RETURN_HANDOFF.json',handoff)
print(json.dumps({'raw':ev(R/'character_api_original.png'),'review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'handoff':ev(D/'ARTIST_RETURN_HANDOFF.json'),'effective_prompt':ev(R/'prompt_effective.txt'),'API_calls_this_repair':1,'API_calls_known_17_total':2,'inflight':0},ensure_ascii=False,indent=2))
