from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-12/v01/direct_first_api_source1200_flat_originalref_attached_curl_v03'
E=B/'review/SOL_FIRST_G13_12_SINGLE_UNLIT_GRAY_20261104_v01_evidence'
F=B/'review/SOL_FIRST_G13_12_SINGLE_UNLIT_GRAY_20261104_v01.json'
M=F.with_suffix('.md')
assert not F.exists() and not M.exists(),'Do not overwrite prior reviews'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=load(R/'DIRECT_REQUEST.json');result=load(R/'result.json')
raw=R/'character_api_original.png';assert sha(raw)==result['output_sha256']
source=Path(q['source']['path']);wider=Path(q['active_generation_source']['path'])
refs=[Path(p)for p in q['parameters']['InputImages']]
req=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
style=B/'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08/USER_RETURN_REJECTION_FIRST_TURN_AND_STYLE.json'
viewed=[source,refs[0],wider,refs[1],refs[2],raw,R/'qa_white.png',R/'qa_black.png']+[E/n for n in ['COIL_WHITE_3x.png','COIL_BLACK_3x.png','EYES_WHITE_3x.png','HANDS_WHITE_3x.png']]
evidence=list(dict.fromkeys(viewed+[R.parent/'JOB.json',R.parent/'REGISTRATION_PLAN.json',R/'DIRECT_REQUEST.json',R/'result.json',R/'DIRECT_API_EXECUTION_RECEIPT.json',R/'prompt_effective.txt',req,style,E/'PROVENANCE.json']))
im=Image.open(raw).convert('RGBA')
points={'first_front':(615,500),'first_opaque_return':(655,535),'second_front':(645,575),'second_opaque_return':(665,603),'raw_background_glow':(180,95)}
prompt=(R/'prompt_effective.txt').read_text(encoding='utf-8-sig')
prefix_count=prompt.replace('\r\n','\n').count(result['spatial_prefix'].replace('\r\n','\n'))
d={
 'id':'ART-G13-12','reviewed_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'Sol xhigh fresh independent actual review; not payload maker',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':list(im.size),'actual_viewed':True,'actual_viewed_paths':[str(p)for p in viewed],
 'review_status':'repair_required','status':'repair_required','independent_static_pass':False,
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'source':{'canonical':{'path':str(source),'frame':1200,'pts':640640},'existing_wider_extent':{'path':str(wider),'frame':3650,'pts':1949152},'timebase':'1/16000','guide':str(refs[0]),'basis':str(R.parent/'JOB.json'),'cameras_separate':True,'same_author_cel_certified':False},
 'current_policy':{'requirements':str(req),'flat_style_clarification':str(style),'X01_scope':'curl drawing only, not whole character/fixed size/axis'},
 'actual_checks':[
  '已实看全部3正式ref及本canonical1200/wider3650/guide。两真实源均为完全闭睫与tiny O，并非09圆睁；wider仅提供实际可见范围，不证明同cel/摄影相同。',
  '返图双眼完全闭合，保粗短闭睫及眉，无虹膜或眼内白高光；tiny粉O、头倾与源相符。两个胸前错层铺开的独立长指手组、指缝/双拇指方向、两白cuff及黑袖肘、红bow金扣/白frill/腰apron后带保留，未见新增粘掌或未知皮肤桥P1。',
  '本体graybob低人物LEFT画右侧接恰好两颗红珠，再接graycoil；未镜像/高帽根。帽上两MAIN叶共根。卷正常头肩体量，灰面在LEFT白肩前frill之前，前手指又遮卷末段，局部T遮挡可读；不据此认证bob内隐藏根或全路由。',
  '可追踪两大宽前面、实际opaque内后返回、小转前面到手后C露段；返回没有被挖透明。窄mint保，但返回暗底及密套叠内线仍不符本次同单灰材质意图，详P1/P2；不能只数绿线或透明洞宣称空心通过。',
  '实际可见半身下apron/后带在raw约y1054直切，下面有透明余量；未补源外腿鞋。canonical和wider各自摄影、实体裁线出1080均未审。',
  'raw直接显示的大灰光晕在完整白黑合成中不存在，示例背景像素alpha0；不报实体光晕背景。实际WB未见明显彩边/字幕或粉底。未进行alpha清理。'
 ],
 'P1':[
  {'code':'SEPARATE_DARK_OPAQUE_RETURN_MATERIAL','region_raw_xyxy':[550,460,712,690],'finding':'两处内后返回仍被涂成独立较深灰底，与宽前面不是同一种无打光平灰。当前3x白黑均清楚可见，返回面近不透明，不能解释成alpha空气或藏色。','repair_direction':'保现有实体返回/手遮挡和源动作，以同类中性灰平涂前面与返回，用黑线和遮挡区分层次；不擦返回造孔。本报告不授权生成。'},
  {'code':'PERSISTENT_VOLUME_GRADIENT_PV_STYLE','finding':'bob及黑袖衣身仍有宽范围软明暗/连续体积渐变，轮廓也较规整；原PV与本次要求为疏简黑线和均匀平涂。此项不能因闭眼和手式正确自动放行。'}
 ],'P1_count':2,
 'P2':[{'code':'REPEATED_INNER_RETURN_ARCS','finding':'内返回增加了数条套叠弧线，像分格/多层螺纹，削弱单条宽带返回的读法；不把每条线算成一个新完整大圈，也不认证隐藏小C全形。'}],'P2_count':1,
 'supporting_point_samples':{k:{'xy':list(xy),'RGBA':list(im.getpixel(xy))}for k,xy in points.items()},
 'point_sample_limit':'Only supports actual WB judgment: differing opaque face fills and alpha0 hidden RGB. No strict per-pixel uniform-RGB acceptance threshold.',
 'evidence_sha256':{str(p):sha(p)for p in evidence},
 'receipt':{'provider':result['provider'],'quality':result['quality'],'n':result['n'],'configured_retry':result['retry'],'actual_retry':result['automatic_retries'],'transport_attempt_count':result['transport_attempt_count'],'elapsed_seconds':result['elapsed_seconds'],'effective_prefix_occurrences':prefix_count,'known_result_saved':True},
 'front_shoulder_route_certified':True,'front_shoulder_certified_scope':'Visible coil-before-white-frill and hand-before-coil T junctions only','root_attachment_hidden_geometry_certified':False,
 'photography_validated':False,'exposure_binding_validated':False,'dynamic_validated':False,'playback_performed':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_modified':False,'binding_modified':False,'adopted':False
}
F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
M.write_text('G13-12 FIRST：**repair_required**（2 P1 / 1 P2）。\n\n'
 '闭睫无虹膜白点、tiny O、双胸前错层铺指/指缝、两白袖口与半身裁切保住；两MAIN帽叶、低LEFT双珠连接、局部肩前与前手遮卷可读。\n\n'
 'P1：①opaque灰返回仍显著暗于前面，未满足同一无光平灰；②bob/黑衣仍有连续软体积渐变。P2：返回密套叠弧线偏螺纹化。未把真实灰返回当空气，也未把raw隐藏光晕当实体背景。\n\n'
 'canonical1200/PTS640640与wider3650/PTS1949152、3正式refs、完整新raw/WB及必要局部均实看；两摄影分开待审。high n1/retry1，实际retry0，39.301s。\n\n'
 'Raw SHA `'+sha(raw)+'`。路径与单份SHA证据见JSON。0生成/网络/中央/绑定；无用户整体验收、动态或摄影通过。\n',encoding='utf8')
print(json.dumps({'report':str(F),'report_sha256':sha(F),'md':str(M),'md_sha256':sha(M),'status':d['review_status'],'prefix_occurrences':prefix_count},ensure_ascii=False,indent=2))
