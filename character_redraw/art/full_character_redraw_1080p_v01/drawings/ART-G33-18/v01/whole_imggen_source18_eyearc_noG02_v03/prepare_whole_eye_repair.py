from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
from PIL import Image

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01');C=B/'drawings/ART-G33-18/v01'
P=C/'first_api_source2377_user11_leftroot_v02';R=Path(__file__).resolve().parent;I=R/'inputs';I.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert read(P/'attempt.json')['status']=='completed'
assert sha(P/'character_api_original.png')=='91b39addcaaad2e6a431c276cefdebc09d78533504fd4d30e0f03d45a39afae9'
assert not (R/'character_imggen_original.png').exists()
defaults=Path('D:/CODEX/魔术之心/image_defaults.json');pref=read(defaults)['generation_prompt_prefix'];assert pref['enabled']
sources=[P/'character_api_original.png',C/'inputs/source_pose_guide.png',P/'artist_return_diagnostics_v01/SOURCE_EYES_1x.png']
names=['ref1_CURRENT18_TRANSPARENT_WHOLE_TARGET_KEEP_ROOT_CAP_HANDS_CUTOFF.png','ref2_ORIGINAL2377_UNMASKED_GUIDE_SOURCE_ACTION_APERTURE.png','ref3_SOURCE2377_EYES_ONLY_ARCHED_OPENING_NOT_G02.png']
roles=[
 '当前已知18完整透明原raw，整人保持基准：画右低LEFT远侧珠根、卷势/相对体量/灰前返回/C、两黑帽叶、衣身、提裙抓点/腰后手/原鞋端截断；唯一需修的眼睛当前太横平半睑，不复制此缺陷。原alpha0隐藏RGB不作背景。',
 '原2377完整未挖头guide624x1072，唯一原动作/头倾/眼口、提裙手/腰后手/衣身/鞋端源底裁权威；原红双高卷/根/身份不复制，当前18正确画右低LEFT根保留。',
 '源guide只读裁图[260,136,385,206]，125x70原像素，眼上缘为弧形仍睁开，非当前横平半睑，也不是夸张瞪圆。只眼开度/视线/倾斜轮廓，红发/肤色边缘仅上下文不作身份/新根/位置或拼贴。']
refs=[]
for s,n,role in zip(sources,names,roles):
 p=I/n;assert not p.exists();shutil.copyfile(s,p);refs.append({**ev(p),'source':ev(s),'role':role})
now=datetime.now(timezone.utc).isoformat()
prompt=pref['text']+'''\n\n这是ART-G33-18已保存API稿的眼开度修复。用参考1当前完整透明人物为保持基准，整个人物一次连贯重绘，透明背景；主要改掉当前横向压低的半睑眼，不局部粘贴眼像素。参考2原2377完整guide与参考3同一源眼局部唯一决定当前弧形睁眼轮廓、视线与原小闭弧笑；G02半睑图已完全移除。

源眼是较窄但仍清楚睁开的弧形上缘，当前目标把上缘画得过平/过低，虹膜被水平盖住太多。恢复参考3的原上睑拱弧、可见虹膜高度及两眼随头倾的不同投影；不夸张瞪圆、不做AI闭眼，也不照身份参大圆眼。眼仍只一种深charcoal平填虹膜配普通小白点，原小闭口弧笑和头倾/脸型不改。参考3是只读绘画依据，不能把红发/皮肤矩形或现成眼片贴进成品。

其余按参考1和原2377：不镜像人物、头身或手脚，保持画右远耳/低颈的解剖LEFT双红珠低根及bob连贯接合；不要把珠卷改到画左近耳，不为露全根上抬。保现有肩前胸侧卷势、自然遮挡、合理相对头肩体量、宽灰正面/返回绕行和渐细末C，不缩发/加粗为巨大挂件，不套07或17待修几何。上端同样应是连续宽灰发带向内/后返回下一圈，不封口椭圆片堆/实心柱外绕绿线；若源遮住部分不强露尖端/固定洞数。

白maidcap和恰好2片黑叶、黑长袖红bow金扣白肩frill/袖口/围裙/腰后带、画右提裙指尖V隙与裙折抓点、另一腰后手、交错腿与原鞋端截断全部保留。前景鞋在原2377的1080底被切掉鞋端，维持当前平截边，不补完整鞋尖/鞋底，不缩全人把裁外鞋端塞进图内。原PV只管表演与衣身；原红双高卷不继承。

短灰bob和卷的所有灰前/内/背/返回面统一无打光灰#B6B4B2，mint#B0C8BA只材料条带，墨线#171717；保宽灰主体，不全绿、不加深灰体积内底/渐变/银白高光。暖桃肤色，简洁手书墨线平涂。保当前完整可见人物整体比例与构图，一次整人重新绘成无接缝RGBA，真实背景与露空透明；不画目标A0隐藏灰黑光斑、粉底、字幕、参考框、色卡或棋盘格。
'''
pp=R/'prompt_imggen.txt';assert not pp.exists();pp.write_text(prompt,encoding='utf-8')
release={'id':'ART-G33-18','recorded_utc':now,'source':'Root exact current release after actual18 raw/full whiteblack/canonical2377 review',
 'authorized_operation':'ONE built-in imagegen whole current visible character redraw, correcting eye aperture by original2377 arched-open source, noG02 input; preserve correct root/coil/cap/hands/costume/source shoe cutoff; actualview then stop no19',
 'n':1,'max_native_refs':5,'chosen_ref_count':3,'why_only3':'current coherent target + unmasked original performance + actual source eye arc; no new geometry/pigment bitmap competing during eye-only hypothesis',
 'not_unknown_retry':True,'known_parent':ev(P/'character_api_original.png'),'known_parent_attempt':ev(P/'attempt.json'),
 'root_quota_note':'Latest 1-reset conditional authorization is root centrally managed; this agent has no quota read/reset control and performs0 resets.',
 'API_calls_this_repair':0,'native_calls_authorized':1,'automatic_retries':0,'19_released':False}
save(R/'ROOT_ONE_NATIVE_RELEASE.json',release)
save(R/'READONLY_REFERENCE_PROVENANCE.json',{'id':'ART-G33-18','refs':refs,'source_eye_crop_xyxy':[260,136,385,206],'source_eye_crop_technical_selection_only':True,'art_parts_spliced':False,'G02_bitmap_present':False,'other_failed_coil_bitmap_present':False,'changed_hypothesis':'Remove G02 half-lid image entirely, source-eye arched-open contour as direct positive reference, current coherent correct-root whole figure retained. No repeated API call.','preserved_originals':[ev(C/'JOB.json'),ev(C/'REGISTRATION_PLAN.json'),ev(C/'inputs/source_pose_guide.png'),ev(P/'character_api_original.png'),ev(P/'artist_return_diagnostics_v01/ARTIST_PRIVATE_RETURN_REVIEW.json')], 'prefix_evidence':{'path':str(defaults),'sha256_at_read':sha(defaults),'text':pref['text']}})
request={'id':'ART-G33-18','run':str(R),'operation_kind':'whole_character_redraw','local_repair_parent':None,
 'source_saved_API_parent':str(P),'source_saved_API_sha256':sha(P/'character_api_original.png'),
 'refs':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'reference_roles':roles,
 'prompt_file':str(pp),'prompt_sha256':sha(pp),'transparent_background':True,'n':1,
 'user_quality_preference':'high','quality_parameter_exposed':False,'native_model_not_exposed':True,
 'whole_character_one_generation':True,'local_mask_used':False,'parts_spliced':False,
 'G02_bitmap_present':False,'ROOT_RELEASE':ev(R/'ROOT_ONE_NATIVE_RELEASE.json'),
 'provenance':ev(R/'READONLY_REFERENCE_PROVENANCE.json'),'fresh_root_Sol_review_required':True,
 'generation_submitted':False,'native_calls':0,'API_calls':0,'automatic_retries':0,'dynamic_validated':False,'user_accepted':False,'central_write':False,'quota_resets':0}
save(R/'request_imggen.json',request)
print(json.dumps({'request':ev(R/'request_imggen.json'),'prompt':ev(pp),'refs':refs,'run':str(R)},ensure_ascii=False,indent=2))
