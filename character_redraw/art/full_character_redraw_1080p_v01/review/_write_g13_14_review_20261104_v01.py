from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import hashlib, json

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-14/v01/direct_first_api_source1246_latest_grayeye_samegray_return_v05'
E=B/'review/SOL_FIRST_G13_14_GRAYEYE_SAMEGRAY_20261104_v01_evidence'
stem=B/'review/SOL_FIRST_G13_14_GRAYEYE_SAMEGRAY_20261104_v01'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
req=read(R/'DIRECT_REQUEST.json'); result=read(R/'result.json')
raw=R/'character_api_original.png'
assert sha(raw)=='e5a311040d746c2a2edc8905e353a43fc65b38d8f12a29a5c5caf5dcb1d72755'
source=Path(req['source']['path'])
guide=Path(req['guide']['path'])
wider=B/'coverage/source_frames/F003682.png'
curlpolicy=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
eyepolicy=Path(req['eye_color_policy']['path'])
style=B/'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08/USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'
eye=read(eyepolicy)
effective=R/'prompt_effective.txt'
prompt=effective.read_text(encoding='utf-8-sig').replace('\r\n','\n')
prefix=result['spatial_prefix'].replace('\r\n','\n')
viewed=[raw,R/'qa_white.png',R/'qa_black.png',source,wider,guide]
viewed += [Path(p) for p in req['parameters']['InputImages'][1:]]
viewed += [E/n for n in ['EYES_SOURCE_NEW_WHITE_3x.png','HANDS_SOURCE_NEW_WHITE_3x.png','COIL_WHITE_BLACK_ALPHA_3x.png']]
evidence=list(dict.fromkeys(viewed+[R/'DIRECT_REQUEST.json',R/'result.json',R/'prompt_api.txt',effective,curlpolicy,eyepolicy,style,E/'PROVENANCE.json']))
report={
 'id':'ART-G13-14','reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer':'Sol xhigh fresh independent actual review; not maker',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(Image.open(raw).size),
 'actual_viewed':True,'actual_viewed_paths':[str(p) for p in viewed],
 'review_status':'repair_required','status':'repair_required','independent_static_pass':False,
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'current_eye_policy_id':'eye_black_gray_palette_only_20261104_v01',
 'source':{
  'canonical':{'path':str(source),'frame':1246,'pts':665200},
  'existing_wider_extent':{'path':str(wider),'guide':str(guide),'frame':3682,'pts':1966224},
  'timebase':'1/16000','cameras_separate':True,'same_author_cel_certified':False,
  'scope':'Canonical owns action/exposure; existing wider is visible extent reference only. Neither camera photography validated.'},
 'current_policy':{'curl_requirements':str(curlpolicy),'eye_color':str(eyepolicy),'flat_style':str(style),'X01_scope':'Curl drawing only, not whole character/fixed size/axis'},
 'actual_checks':[
  '实际看新raw/完整白黑、canonical1246、wider3682/guide、全部4正式参考与3组只读近图。头向画左倾、颈耳/下颌斜关系、小粉O、不等圆睁/视线方向大体保；没有因灰眼改成另一套眼型或把脸旋正。',
  '眼黑为连续深灰主体加内下浅灰块，没有中心黑点。原两眼各一处上侧白glint/眼白/黑睫轮廓仍在。原左glint略不规则，新稿较圆，眼外线更规整，属重描差异，不能声称原眼几何逐像素不变；本FIRST不适用既有稿局部RGB替色的字节等同证明。',
  '两裸手仍以长指和内折角围不规则菱形，各白cuff独立，源左右不对称拇指/长指组合可辨；没有改成合十或心形。内角较平顺、两尖距离有重描偏差。黑红白衣/金扣/腰后结和源apron下裁保，无腿鞋补全。',
  '画右低人物LEFT的灰bob到两红珠再接单束灰卷可见。两MAIN帽叶同根。两大宽灰front、同灰opaque内后返回、独立小转前面/返回再C可追踪；mint为窄边，无独立大深灰内底板。上返回仍压紧，未仅按孔数或mint数认证空心。',
  '灰卷压在白肩frill前，前景长指实际压住卷下段，局部前后关系成立；被bob/手遮住的完整根路由和隐藏小转不补画、不认证。',
  '完整白黑未见raw渲染的大灰雾或粉色方块实体背景。抽查外空气alpha为0（如100,500 / 800,300 / 780,900），不能把隐藏RGB叫真实雾；未清理低alpha或改原图。底部实体apron裁口仍需以后各相机摄影将其置于画外。',
  '当前黑袖/衣身和bob本身存在可见连续明暗塑形，是本次实际新稿问题，区别于隐藏RGB；详P1。肤色只记录当前状态，统一校准延期，不据未定肤色基准退修。'
 ],
 'P1':[{'id':'P1_FLAT_STYLE_VOLUME_GRADIENT','location':'两黑袖、胸腹黑衣及灰bob大面','observation':'完整WB可见袖管由中段较亮向外缘/下缘变暗、衣身胸腹连续亮暗过渡、bob随头球面变化的柔和明暗；原PV这些区域是简单均匀平涂。当前已不是仅轮廓抗锯齿或少量软灰偏差。','required_result':'恢复原PV简笔黑线与均匀平涂；保当前眼形/灰配色、手动作、同灰实体返回和源裁幅，不以删alpha代替材料修复。'}],
 'P1_count':1,
 'P2':[
  {'id':'P2_TRACE_FIDELITY','observation':'白glint更圆、眼线及两手内角比源规整，仍可读本帧眼开度/视线和不规则菱形；未升为另一套动作或新眼型。'},
  {'id':'P2_COMPACT_RETURN','observation':'上返回与下一转连接较紧，内缘规则、C较圆；目前近图可追踪实际灰返回，不能仅因闭合灰面/白frill背景判实心或强挖空气。'}],
 'P2_count':2,
 'skin_palette_calibration_deferred':True,
 'front_shoulder_route_certified':'visible local frill/foreground-finger overlap only',
 'root_attachment_hidden_geometry_certified':False,
 'receipt':{'quality':'high','n':1,'configured_retry':1,'actual_retry':result['automatic_retries'],'transport_attempt_count':result['transport_attempt_count'],'elapsed_seconds':result['elapsed_seconds'],'spatial_prefix_occurrences':prompt.count(prefix),'eye_prefix_occurrences':prompt.count(eye['generation_prompt_prefix'].replace('\r\n','\n'))},
 'evidence_sha256':{str(p):sha(p) for p in evidence},
 'photography_validated':False,'exposure_binding_validated':False,'dynamic_validated':False,'actual_playback':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'art_pixels_modified':False
}
assert report['receipt']['spatial_prefix_occurrences']==1
assert report['receipt']['eye_prefix_occurrences']==1
j=stem.with_suffix('.json');m=stem.with_suffix('.md')
assert not j.exists() and not m.exists(), 'preserve previous reports'
j.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m.write_text('G13-14 独立实际静态评审：repair_required，1 P1 / 2 P2。\n\nP1 是当前黑袖、衣身及 bob 的连续体积渐变，仍偏离原PV均匀平涂；不是 raw 隐藏RGB的灰雾。灰眼主体/下浅块、无中心黑点，本帧不等圆睁/上侧白glint、斜头小O和双手不规则菱形基本保。glint与手内角有较规整的重描偏差。\n\n卷可追踪两大转、同灰不透明返回、独立小转再C，薄mint与低LEFT两珠保；白肩前/前景手遮挡局部可见。上返回较紧记P2，不认证隐藏结构。白黑未见大片实体背景污染。肤色统一校准延期。\n\ncanonical F1246 / PTS665200；wider F3682 / PTS1966224 仅extent参考，两相机均未摄影认证。未生成、未联网、未改中央/原图，非绑定、动态或用户整稿接受。\n\n原图 SHA256：'+sha(raw)+'\n',encoding='utf-8')
print(json.dumps({'json':str(j),'json_sha256':sha(j),'md':str(m),'md_sha256':sha(m),'image_sha256':sha(raw),'status':report['review_status'],'P1_count':1,'P2_count':2,'receipt':report['receipt']},ensure_ascii=False,indent=2))
