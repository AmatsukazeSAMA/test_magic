from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib

R=Path(__file__).resolve().parent;D=R/'artist_return_diagnostics_v01';C=R.parent
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
now=datetime.now(timezone.utc).isoformat();a=read(R/'attempt.json');res=read(R/'result.json');lock=read(R/'AUTHORIZED_CALL_LOCK.json')
assert a['status']=='completed' and a['http_status']=='200' and a['curl_exit_code']==0 and a['api_calls']==1 and a['automatic_retries']==0
assert sha(R/'character_api_original.png')==res['output_sha256']=='91b39addcaaad2e6a431c276cefdebc09d78533504fd4d30e0f03d45a39afae9'
assert sha(R/'prompt_effective.txt')==res['prompt_sha256']=='31888fc3793c4e4c5d2db83b7c60652dd733ae80ea45850f6bae69023b072838'
assert res['elapsed_seconds']==28.046 and res['spatial_prefix_applied'] is True and len(res['inputs'])==6
for x in lock['preserved_originals']+lock['refs']:assert sha(x['path'])==x['sha256']
viewed=[R/'character_api_original.png',R/'qa_white.png',R/'qa_black.png',C/'inputs/source_pose_guide.png']
viewed += [D/n for n in ['SOURCE_EYES_2x.png','EYES_white_2x.png','HEAD_ROOT_COIL_white_1x.png','COIL_white_3x.png','COIL_black_3x.png','SOURCE_GRIP_2x.png','SKIRT_GRIP_white_2x.png','SOURCE_SHOE_CUTOFF_2x.png','SHOE_CUTOFF_white_2x.png','CAP_LEAVES_white_2x.png']]
findings=[
 {'criterion':'原眼开度/表情','private_result':'P1_REPAIR_REQUIRED','observation':'对SOURCE_EYES_2x和EYES_white_2x：原2377较窄但上睑弧形仍明显睁开，新稿变为横向更压扁的G02式半睑，iris上下被平切，表情更困倦。不能因两者都不是闭眼或mono正确而放行；原小闭弧笑保留。'},
 {'criterion':'原提裙手/腰后手/衣身','private_result':'基本保留，整体摄影待root','observation':'SOURCE_GRIP_2x与SKIRT_GRIP_white_2x见原V形指间隙、向裙折的两道指线/抓点保留；画右低手提裙、另一手腰后、肘腕和衣袖、提起裙边/围裙/后腰带，黑长袖红bow金扣白frills基本同源。'},
 {'criterion':'原真实鞋裁边','private_result':'截断读法保留，最终1080整体定位待root','observation':'源2377前景鞋在1080底被截掉鞋端；新SHOE_CUTOFF_white_2x仍呈前鞋下缘水平平截，没有补成完整闭合圆鞋尖/鞋底，后鞋可见。未沿17“双鞋全见”补隐形前鞋端。guide原有底部padding，具体截断落在1080何处仍须root整体摄影实核。'},
 {'criterion':'帽/低根与接合','private_result':'可见正确侧/两叶，待freshroot/Sol','observation':'白maidcap存在，CAP_LEAVES_white_2x恰2独立黑叶；唯一红珠卷在画右远侧低nape/颈肩前，与bob相接，无画左近耳另一卷。两珠可见、根高度低，仍需独立核当前转向与真实frill遮挡，不将单张侧别正确称动态通过。'},
 {'criterion':'螺旋卷形与上端返回连续性','private_result':'待root/Sol fresh裁决，不升为结构master','observation':'正常全头肩和3x见宽灰前面、斜向绕行、渐尖下C；灰主面不是整束mint小柱。上端前面间的可见返回弧较窄，呈串小灰单元/墨线，宽返回连续读法仍需独立比用户正确11核查。不能仅因整体锥形/C正确放行，也不因无固定洞数认定隐藏结构实心。'},
 {'criterion':'发量与投影','private_result':'未见明显巨大/微型，待正确投影及相邻actual核查','observation':'先实际全人/头肩再3x；coil在头/肩和胸结尺度有足量宽面，不按R54 37x43可见crop缩小固有发量。未使用17/07v11v12几何模板，不制定全片固定轴长/圈数/头卷比。'},
 {'criterion':'材料与透明','private_result':'可见灰主面/较薄mint，轻软调待root','observation':'3x宽面灰、mint较薄，bob/卷有软色差，未以像素统计当艺术平涂通过。完整白黑QA未显原raw A0隐藏灰黑光斑为背景实体；maxalpha254留原字节，技术解码不认证所有返回/空气几何。源衣装黑白红保持。'},
 {'criterion':'时序连续性/隐藏部分','private_result':'PENDING_UNVALIDATED','observation':'17仍HOLD，未拿其上端形态作参考；本18仅当前静态实际看，没做绑定原速/慢速PTS播放。源899..902首段半身和canonical2377全可见extent分开，隐藏鞋端/圈不认证，不声称用户接受/摄影或动态通过。'}
]
review={'id':'ART-G33-18','reviewer':'xhigh_pending_artist private draft only','reviewed_utc':now,'state':'HOLD_EYE_APERTURE_REPAIR_PENDING_FRESH_ROOT_SOL',
 'raw':ev(R/'character_api_original.png'),'actual_viewed_return_and_source_local_paths':[ev(p) for p in viewed],
 'original_full_source_reference_review':ev(R/'ARTIST_REFERENCE_REVIEW.json'),'findings':findings,
 'primary_static_pass':False,'independent_static_pass':False,'photography_validated':False,'dynamic_validated':False,'user_accepted':False,
 'API_calls':1,'native_calls':0,'automatic_retries':0,'inflight':0,'19_not_started':True,'central_write':False,'REGPLAN_central_changed':False,'exposure_binding_changed':False,'quota_reset_used':False}
save(D/'ARTIST_PRIVATE_RETURN_REVIEW.json',review)
names=['character_api_original.png','api_response.raw.json','request_manifest.json','response_headers.txt','result.json','attempt.json','ARTIST_API_EXECUTION_RECEIPT.json','prompt.txt','prompt_effective.txt','API_PREPARED_REQUEST.json','DRAFT_API_REQUEST_v02.json','AUTHORIZED_CALL_LOCK.json','ROOT_SPECIFIC_RELEASE.json','PROJECT_SCOPE_REFERENCE_RELEASE.json','qa_white.png','qa_black.png']
handoff={'id':'ART-G33-18','run':str(R),'recorded_utc':now,'status':'KNOWN_FIRST_API_RETURN_ARTIST_HOLD_EYE_APERTURE',
 'raw':ev(R/'character_api_original.png'),'provider':'OpenAI API','model':'gpt-image-2.5-sunburst','quality':'high','actual_dimensions':[608,1136],
 'elapsed_seconds':28.046,'http_status':'200','curl_exit_code':0,'n':1,'API_calls':1,'native_calls':0,'automatic_retries':0,'live_session_id':75912,'session_status':'terminal_exit0','inflight':0,
 'effective_prompt':ev(R/'prompt_effective.txt'),'spatial_prefix_applied':True,'artist_review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'technical_QA':ev(D/'TECHNICAL_QA.json'),
 'P1':['新眼相对原2377过于横向半睑/压扁'],
 'retained':['画右低远侧珠卷','2帽叶','原提裙指尖抓点/另一腰后手','前鞋源截断读法/不补隐藏鞋端','灰主面及C可见'],
 'fresh_review_pending':['上端宽gray返回连续读法','材料软色差','真实1080整体摄影/鞋截断位置','前后actual时序'],
 'original_receipts_preserved':[ev(R/n) for n in names],
 'originals_unchanged':[{'path':x['path'],'sha256':sha(x['path']),'matches_before':sha(x['path'])==x['sha256']} for x in lock['preserved_originals']],
 'stop_boundary':'18 ONE已完成即停，未第二call/修复/19。中央registry/曝光/绑定/REGPLAN无写入，quota reset禁用。'}
save(D/'ARTIST_RETURN_HANDOFF.json',handoff)
print(json.dumps({'raw':ev(R/'character_api_original.png'),'review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'handoff':ev(D/'ARTIST_RETURN_HANDOFF.json'),'effective_prompt':ev(R/'prompt_effective.txt'),'elapsed_seconds':28.046,'API_calls':1,'inflight':0},ensure_ascii=False,indent=2))
