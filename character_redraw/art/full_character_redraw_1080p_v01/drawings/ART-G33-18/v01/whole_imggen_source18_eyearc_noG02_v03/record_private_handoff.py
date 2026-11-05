from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image

R=Path(__file__).resolve().parent;D=R/'artist_return_diagnostics_v01'
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
request=read(R/'request_imggen.json');prov=read(R/'READONLY_REFERENCE_PROVENANCE.json')
assert sha(R/'character_imggen_original.png')=='902b585fae3f65d4c2d11b48b858b4b29af52054cb4c4d5b1615846c5dfa88cd'
builtin=read(R/'BUILTIN_GENERATION.json');assert sha(builtin['source_generated_file'])==sha(R/'character_imggen_original.png')
for x in prov['preserved_originals']:assert sha(x['path'])==x['sha256']
assert all(sha(p)==s for p,s in zip(request['refs'],request['reference_sha256']))
now=datetime.now(timezone.utc).isoformat()
viewed=[R/'character_imggen_original.png',R/'qa_white.png',R/'qa_black.png']
viewed += [D/n for n in ['NATIVE_NORMALIZED_QA_608x1136_white.png','NATIVE_EYES_QA_NORMALIZED_2x.png','HEAD_ROOT_COIL_white_1x.png','COIL_white_3x.png','COIL_black_3x.png','CAP_LEAVES_white_2x.png','SKIRT_GRIP_white_2x.png','SHOE_CUTOFF_white_2x.png']]
viewed += [Path(x) for x in request['refs']]
findings=[
 {'criterion':'原眼开度/本次修复目标','result':'P1_REPAIR_NOT_SUFFICIENT_HOLD','observation':'已实际看原source眼c90339、API目标和新native，含新native只读缩放到608x1136后的相同眼区。新眼仍为明显横平/低上睑的半睑读法，源2377的上缘拱弧和可见iris高度没有可靠恢复；虽没再输入G02 bitmap，仍不能据此声称开度已修。单charcoal和普通小白点保留，小闭弧笑保留，但不抵消开度P1。'},
 {'criterion':'卷根侧与连接','result':'可见保持正确侧；pending_root_Sol','observation':'仍画右远侧低nape/颈侧红珠接卷，在同侧肩前胸侧；无画左近耳另一卷，不镜像身体。bob/双珠/颈领接合可见，真实隐藏根内部不认证。'},
 {'criterion':'体量与连续卷形','result':'整体体量/末C保持，上端返回读法待fresh核查','observation':'完整头肩/全稿与正常局部后再3x，卷没有极端放大或缩成微型挂件，灰前面连续到渐尖C。上端夹缝返回仍偏窄分节小单元，不能仅因下C正确或整体锥形认定上端已达宽gray前返绕行要求；不拿07/17错误稿作模板，不固定洞/轴/圈数。'},
 {'criterion':'材质与无光照','result':'soft_material_difference_requires_fresh_review','observation':'灰宽主面与mint较薄条带仍可见，但3x见软色阶、灰到mint的渐接及边缘亮暗，未达到可凭此认证严格无光平涂的程度；不把当前稿作为新的发面/光照master。无证据把隐藏夹缝强判为实心内腔。'},
 {'criterion':'原动作/衣手/帽/裁切','result':'基本保持；摄影未认证','observation':'两黑帽叶与白cap保留；原头倾/小闭笑、黑长袖红bow金扣白肩frill/袖口/围裙/腰后带、画右提裙V指隙抓点与另一腰后手、交错腿保持。前景鞋仍下缘平截，未补成完整鞋尖/鞋底；不能由孤立layer判断最终1080截断落位通过。'},
 {'criterion':'整人透明/边缘','result':'full_raw_white_black_actually_viewed_no_adoption','observation':'完整raw和白黑已实看，项目raw为原generated文件逐字节复制，918x1714 RGBA；原API A0隐藏灰黑RGB未画成背景。技术透明通过不能代替艺术/隐藏几何/摄影通过；正常化和所有crops仅QA，不替换原画。'},
 {'criterion':'时序/工作边界','result':'PENDING_UNVALIDATED','observation':'只有本次1native整人重绘，无局部粘贴/修色、无第2native/API重试、无19；前17仍待修，未做实际绑定原速/慢速PTS播放，不声明动态/用户接受。'}
]
review={'id':'ART-G33-18','reviewer':'xhigh_pending_artist private draft only','reviewed_utc':now,
 'state':'HOLD_EYE_ARC_REPAIR_NOT_SUFFICIENT_PENDING_ROOT_SOL','exact_raw':ev(R/'character_imggen_original.png'),
 'actual_viewed_paths':[ev(p) for p in viewed],'findings':findings,
 'changed_hypothesis_result':'去G02图+源弧眼正例+当前整人target 的一次尝试仍未可靠修开度，已停该假设，不叠prompt自动重试。',
 'whole_character_redraw':True,'local_mask_used':False,'parts_spliced':False,'art_pixel_edits':False,
 'native_calls':1,'API_calls_this_repair':0,'automatic_retries':0,'inflight':0,
 'primary_static_pass':False,'independent_static_pass':False,'dynamic_validated':False,'photography_validated':False,'user_accepted':False,
 'central_write':False,'REGPLAN_central_changed':False,'exposure_binding_changed':False,'19_not_started':True,'quota_resets':0}
save(D/'ARTIST_PRIVATE_RETURN_REVIEW.json',review)
names=['character_imggen_original.png','BUILTIN_GENERATION.json','TECHNICAL_CHECK.json','NATIVE_CALL_INTENT.json','NATIVE_CALL_RECEIPT.json','request_imggen.json','prompt_imggen.txt','ROOT_ONE_NATIVE_RELEASE.json','READONLY_REFERENCE_PROVENANCE.json','qa_white.png','qa_black.png']
handoff={'id':'ART-G33-18','recorded_utc':now,'run':str(R),'state':'KNOWN_NATIVE_RETURN_ARTIST_HOLD_EYE_ARC_UNRESOLVED',
 'raw':ev(R/'character_imggen_original.png'),'native_original':ev(Path(builtin['source_generated_file'])),'generated_original_bytes_preserved':True,
 'dimensions':[918,1714],'provider':'built-in imagegen','model':'not exposed','quality_parameter_exposed':False,'user_quality_preference':'high',
 'native_calls':1,'API_calls_this_repair':0,'API_calls_known18_total':1,'automatic_retries':0,'cell_id':'758','cell_status':'completed','inflight':0,
 'started_utc':'2026-11-01 17:27:03 UTC','finished_utc':'2026-11-01 17:27:31 UTC','elapsed_seconds_approx':28,'clock_precision':'whole seconds',
 'artist_private_review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'receipts':[ev(R/n) for n in names],
 'P1':['原弧形睁眼尚未可靠恢复，新稿仍横半睑'],
 'retained':['画右低LEFT根/肩前接合','两黑帽叶','提裙抓点/腰后手/衣身','前鞋原平截','整束合理体量与末C'],
 'other_fresh_review_pending':['上端宽gray返回读法','gray/mint软渐接与光照','最终摄影和时序'],
 'stop_boundary':'ONE native已实际看后停；无第二次/API/19，0中央/REGPLAN/曝光/绑定改写。quota授权由root统一处理，本代理0重置。',
 'preserved_originals_unchanged':[{'path':x['path'],'sha256':sha(x['path']),'matches_before':sha(x['path'])==x['sha256']} for x in prov['preserved_originals']]}
save(D/'ARTIST_RETURN_HANDOFF.json',handoff)
print(json.dumps({'raw':ev(R/'character_imggen_original.png'),'review':ev(D/'ARTIST_PRIVATE_RETURN_REVIEW.json'),'handoff':ev(D/'ARTIST_RETURN_HANDOFF.json'),'native_calls':1,'API_calls_this_repair':0,'inflight':0},ensure_ascii=False,indent=2))
