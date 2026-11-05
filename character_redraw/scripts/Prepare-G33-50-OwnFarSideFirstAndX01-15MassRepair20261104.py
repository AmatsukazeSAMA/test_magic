"""Prepare source-specific next FIRST and one existing whole repair; zero calls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'art/full_character_redraw_1080p_v01'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
save=lambda p,q:Path(p).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assets=read(BASE/'ASSET_REGISTRY.json')
parent=BASE/'drawings/ART-G33-50/v01';job=read(parent/'JOB.json');reg=read(parent/'REGISTRATION_PLAN.json')
assert next(r for r in read(BASE/'PROGRESS.json')['records'] if r['id']=='ART-G33-50')['status']=='pending'
assert not any(list(parent.parent.rglob(n)) for n in ['attempt.json','result.json','BUILTIN_GENERATION.json'])
assert assets['ART-G33-49']['status']=='reviewed_static_candidate'
source=Path(job['source_image']);guide=parent/'inputs/source_pose_guide.png'
assert sha(source)==job['source_image_sha256']
run=parent/'direct_first_api_source2523_ownFarSideContext_normalCoil_roundArc_v19';run.mkdir(exist_ok=False)
bob=BASE/'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png'
coil=BASE/'drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png'
eye=BASE/'inputs/eye_palette_and_internal_arc_NO_OUTLINE_20261104_v01/DARK_AND_LIGHT_LOWER_ARC_ONLY.png'
far=BASE/'inputs/reviewed_oblique_far_left_root_no_eyes_20261104_v01/RIGHT_FACING_NEAR_RIGHT_EAR_FAR_LEFT_ROOT_STRIP.png'
refs=[guide,bob,coil,eye,far]
action='本F2523头和胸身更朝画右转，保持耳颌/颈领透视；只是两眼略向镜头看，不把整个头扳正面。双眼正常睁、原不等外形/小白glint和细闭弧笑保。两前臂在胸前比49更横向交叉，画右高手的长指更横向指左，其余短折指弯收；另一只胸前手背朝上、三四根长指向下垂，指缝/拇指侧分和两只异角白cuff依自身源，不能冻结49的高竖食指/横放短指。白长apron前片更移向画右、黑裙摆向画左甩、腰后白带向画左伸；两足更分开，画左踝后折/鞋侧斜，画右腿较直且踝带鞋向下，两鞋全可见。保自身黑红白长袖maid及所有这些重描差异，不改身体/手去适配卷。'
prompt=f'''ART-G33-50 F2523缺失首图，624x1072透明人物。{action}
图1是本张原PV唯一姿态/动作/脸头颈身体透视/眼形眼白睫线视线小高光/口/两手指组/cuff前后互遮/衣服裁切/实际可见范围/疏简笔道依据。删原红刘海及旧双红高卷，换短灰bob和唯一低LEFT灰钻发，不镜像人物。图2只无眼灰bob和刘海身份/中性灰色，不给眼型、姿势或打光。
本次更正此前同类FIRST的错侧假设：图1旧红大卷在画左不意味着OC也绑在那一侧。这个向画右转的头，画左暴露的是近侧本人RIGHT耳，它后面只能正常短bob，绝不放红珠/灰卷。图5是实际审核过同方向头的无眼下脸/耳-根横条，只示范同一空间关系：画左近RIGHT耳无珠无卷，远LEFT低bob末缘在画右、颌后，灰本体发经恰两红珠接同一束灰卷；不迁移它的嘴型/手指边缘/衣服/尺寸/带厚或圈数。按本F2523更强的转头和肩近远投影，far根珠可以被bob/下颌部分挡住，不能为了全露而移到近耳或帽叶/太阳穴高扎；无第三珠/碎红点。
灰卷在人物自身LEFT肩前颈胸侧，正常大卷灰front覆盖自己白肩褶内侧和胸衣，源下垂手、白cuff、前景交叉袖可挡住中下段。可遮就遮，露出段仍正常卷径体量，不能挂肩外空白、缩成领旁小挂件、穿到手上或为露全改源手势。隐藏段也算入整束总数，挡住后不重新长出一套卷。
图3是认可开放卷的连续宽灰发带画法：整束严格两大转，另一个自带灰front/opaque灰返回的真小转，再连续渐细C。不是两个大转直接C，不把C又算小转，不额外加圈。灰front→有实际宽度的不透明灰内返回→下一转连续，只有真实空气孔透明，实体返回不能挖掉；mint只是窄材料边。首大卷的带面厚度适中较薄，正常首圈卷径/体量保持，不能为了薄带把全束缩小，也不封成长方筒/实心锥/叠盘。图3不提供固定尺寸/轴向/他人衣物。
图4只眼内两灰和底部饱满向上拱起圆弧，深灰72/69/67占主体，底浅灰129/128/128，不能占大半或压成扁窄横条，无中央黑点。原眼黑外轮廓/开合/视线/原小白glint/眼白/眼线睫毛全部按图1，不套任何参考眼型/头角，不新增尖锐大高光或眼下装饰痣。人物通过后，正常睁眼仍另做Python局部眼色/内部圆弧校准；眯眼、闭眼和全遮眼按单眼实看跳过，不能强行睁眼。
保原手书疏简、不规整轮廓、粗细起伏黑线及尖收笔，灰bob/卷mint平涂，返回略深灰可接受，无银白发光带/金属质感/密发丝/精修衣褶。整张源实际可见人物RGBA透明，保所有帽/手/衣边及完整双鞋，源不可见部分不补。无粉底、字幕/白字、导框、花瓣、独立道具或其它后期层。'''
pf=run/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8')
q={'id':'ART-G33-50','source_frame':2523,'source_pts':job['source_pts'],'source_time_base':'1/16000','source':ev(source),'guide':ev(guide),'guide_frame':2523,'guide_pts':job['source_pts'],
   'parameters':{'PromptFile':str(pf),'InputImages':[str(p) for p in refs],'OutputDirectory':str(run),'Size':'624x1072','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'ART_G33_50_MISSING_FIRST_OWN_FAR_LEFT_ROOT_NORMAL_MASS_V19','DrawingId':'ART-G33-50','OperationKind':'first_missing'},
   'model':'gpt-image-2.5-sunburst','n':1,'retry':1,'provider':ev(ROOT/'scripts/Invoke-ReferenceImage.ps1'),'refs':[ev(p) for p in refs],'prompt':ev(pf),'own_action':action,
   'eye_color_policy':read(ROOT/'image_defaults.json')['eye_color_policy'],'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','requirements':read(BASE/'GOAL_EXECUTION.json')['review']['mandatory_curl_requirements'],
   'controlled_reference_change':'Replace generic front junction with actual reviewed same-yaw nearRIGHT/farLEFT no-eye ear-to-root strip after49 wrong-side FIRST. Own source alone controls head/body/hands/crop; not a retry or a fixed pose/coil scale template.',
   'previous_family_candidate':ev(assets['ART-G33-49']['image']),'root_strip_provenance':ev(far.parent/'PROVENANCE.json'),'JOB':ev(parent/'JOB.json'),'registration':ev(parent/'REGISTRATION_PLAN.json'),
   'prep_only':True,'submitted':False,'prepared_utc':datetime.now(timezone.utc).isoformat(),'no_source_camera_or_cel_equivalence_claim':True}
save(run/'DIRECT_REQUEST.json',q)
print(json.dumps({'id':q['id'],'run':str(run),'request':ev(run/'DIRECT_REQUEST.json'),'generation_calls':0},ensure_ascii=False))

ident='ART-X01-15';parent=BASE/'drawings'/ident/'v01'
assert assets[ident]['status']=='repair_required'
r=parent/'whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01';r.mkdir(exist_ok=False)
target=Path(assets[ident]['image']);normal=Path(assets['ART-X01-14']['image']);own=parent/'inputs/source_pose_guide.png'
prompt='''Use case: precise-object-edit. Repair image1 as one coherent whole visible character on true transparent alpha. Image2 is an adjacent static-reviewed character used ONLY to compare normal spiral-ribbon diameter and mass relative to the head/shoulder, not its hand pose, face, eyelid opening, body angle, costume folds or framing. Image3 is this character own original PV pose and visibility authority.
Image1目前错误是灰卷首两主转卷径/体量太小，缩成领旁小条饰。请保第一大卷灰发带较薄、自然开放的带面，同时把两个主要卷的外径明显恢复到正常头肩比例；减薄带面与缩小卷径是两件事。以当前自身头宽/肩透视为准，主卷横径可在本次试验约增至原先1.5倍，不能仅加厚灰带充体量，也不能直接把image2的像素尺寸贴上。保正常空心和连续不透明灰返回，mint细窄材料边；禁止厚板、封口圆筒、实心锥和叠盘。
唯一一束仍严格两个正常大转，再一个自带灰front/实体返回的真小转，连续渐细C尾；不能为了大体量加第三主圈，不把C当小转，任何被肩/衣/手遮的段也算在总数内。保持本体短灰bob→本人LEFT低耳后/nape恰两红珠→同束灰卷的原低连接，当前画右低根正确，不能换侧/上移。扩卷径后自然垂在本LEFT肩前颈胸一侧，宽灰front叠肩frill内侧/胸衣，可真实遮一点原衣/黑bow，不挪到肩外空白或漂浮，不改原手臂来露全卷。
保image1和自己的image3：头向画左roll、身体右倾，原两眼不等开度/视线/小白高光/小闭弧笑；尤其画右低上睑窄眼不变大圆眼。两个黑手套托掌方向和每一手短折长指/分叉、裸前臂、异角白袖口、原短泡袖灰greenmaid/黑胸结金扣/白frill小围裙后bow、裙摆与各腿膝踝轴全部保留。画左外伸长袜腿/鞋完整，画右近竖腿鞋底被原片底边裁切，保当前可见范围不补新鞋底，不冻成image2腿态。无源花瓣/粉底/字幕/道具。
仍原手书简笔不规整粗细黑线/疏简发丝/灰mint平涂，返回略深灰允许，不银白金属高光或精修密发丝。眼色暂保深灰主体和底部饱满圆浅灰，无中心黑点，原iris外形及小glint不重设计；人物过后仍另Python局部校准正常眼，窄眼按实际分类豁免。输出同一张当前完整可见人物、同纵幅取景和真透明背景，没有文字/拼板。'''
pf=r/'prompt_imggen.txt';pf.write_text(prompt+'\n',encoding='utf-8')
save(r/'REQUEST.json',{'id':ident,'provider':'built-in imagegen','calls_authorized':1,'prompt':ev(pf),'references':[ev(target),ev(normal),ev(own)],'transparent_background':True,'defect':'First two major coil diameters/mass undersized; restore normal volume independently from band thickness, keep existing correct lowLEFT shoulderfront route and original pose.','root_numeric_trial_not_user_hard_spec':'Approximate1.5x major diameter is current execution trial only, not a user/global ratio.','created_utc':datetime.now(timezone.utc).isoformat(),'user_accepted':False})
print(json.dumps({'id':ident,'run':str(r),'request':ev(r/'REQUEST.json'),'generation_calls':0},ensure_ascii=False))
