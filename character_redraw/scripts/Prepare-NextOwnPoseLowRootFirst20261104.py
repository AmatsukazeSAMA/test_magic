"""Prepare actually inspected next poses; no network or generation."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'art/full_character_redraw_1080p_v01'
read=lambda f:json.loads(Path(f).read_text(encoding='utf-8-sig'))
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
ev=lambda f:{'path':str(Path(f).resolve()),'sha256':sha(f)}
p=argparse.ArgumentParser(__doc__);p.add_argument('ids',nargs='+');a=p.parse_args()
actions={
'ART-G33-49':'本F2520身体/胸/头仍向画右轻转，耳颌/颈领的斜角保持，眼睛只微向镜头看，不把整个头转正。双眼已正常睁开，嘴为细小带短折的闭口笑，不冻结48闭眼下弧笑。本态双臂交叉在胸前：画右高手只有一根长食指斜向左上，其余指在靠右拳块内折，拇指侧上短出；另一只手在胸bow前手背朝上，四指向画右下垂、拇指侧伸。手掌、指间尖缝、两白cuff不同角度与前后黑袖叠压依本源，不能套48画左竖食指/另一水平手的左右位置。原黑红白长袖maid、肩frill、红bow金扣、长apron与裙摆新折线/向画左甩开的白腰后带保持；两腿错位，画左较直且鞋尖向下，画右足踝向右斜悬，两鞋全部可见，不拉直/对称腿。',
'ART-X01-15':'本F4082身体向画右倾、头略向画左roll，耳颌颈领仍服从源，不能套14的头肩姿态。两眼开合不等：画左眼较圆开、画右眼受较低上睑裁切，保各自视线/小glint和小闭弧笑。两只手都是黑手套：画右手更高且掌向上，前臂斜上、肘在侧外，长指贴合向右上；画左手在腰肩之间向外平托，长指朝左、短拇指下分。两裸前臂与黑手套/白短袖cuff边界、异角尖折指间隙依本源，不复制14竖侧掌或向外张开的指组。原短泡袖、黑胸结金扣、白肩frill/小围裙/腰后bow和后带保持，只把红衣色换成图6灰绿。裙摆向画左展开；画左腿向左下外伸且鞋完整，画右腿近竖向下且鞋底被1080源底切断，保各自长短/膝踝轴和真实裁切，不能为了全鞋补画外鞋底。原画前景花瓣/粉底/字幕均是独立后期层不画。',
}
progress={r['id']:r for r in read(BASE/'PROGRESS.json')['records']}
registry=read(BASE/'ASSET_REGISTRY.json'); defaults=read(ROOT/'image_defaults.json')
req=Path(read(BASE/'GOAL_EXECUTION.json')['review']['mandatory_curl_requirements']['path'])
bob=BASE/'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png'
coil=BASE/'drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png'
eye=BASE/'inputs/eye_palette_and_internal_arc_NO_OUTLINE_20261104_v01/DARK_AND_LIGHT_LOWER_ARC_ONLY.png'
junction=BASE/'inputs/reviewed_low_root_no_eyes_20261104_v03/LOW_BOB_TWO_BEADS_JUNCTION_ONLY.png'
cloth=BASE/'inputs/ending_gray_green_clothing_palette_only_v01.png'
for ident in a.ids:
    assert ident in actions
    assert progress[ident]['status']=='pending' and not registry.get(ident,{}).get('image')
    parent=BASE/'drawings'/ident/'v01'
    assert not any(list(parent.parent.rglob(n)) for n in ['attempt.json','result.json','BUILTIN_GENERATION.json'])
    job=read(parent/'JOB.json');reg=read(parent/'REGISTRATION_PLAN.json')
    source=Path(job['source_image']);guide=parent/'inputs/source_pose_guide.png'
    assert sha(source)==job['source_image_sha256']
    previous=registry[job['previous_in_family']]
    assert previous['status']=='reviewed_static_candidate' and previous['primary_static_pass'] and previous['independent_static_pass']
    assert sha(previous['image'])==previous['sha256']
    run=parent/f"direct_first_api_source{job['source_frame']}_ownPose_reviewedLowRoot_roundArc_postPassEye_v17"
    run.mkdir(exist_ok=False)
    refs=[guide,bob,coil,eye,junction]+([cloth] if ident.startswith('ART-X01') else [])
    size='x'.join(map(str,reg['guide_dimensions']))
    action=actions[ident]
    prompt=f'''{ident}，缺失原画首次API绘制。{action}
图1自身原PV是唯一动作、头颈/躯干透视、脸颌耳、各眼外轮廓/开合/视线/原白高光、口、手/指形/袖口互遮、原衣裁切、疏简手书线条和实际可见范围的依据。其它图不能把图1的头转向镜头、修成写实五指或改衣。保原白maidcap倾角和两片主要黑叶，灰短bob自然刘海替换原红刘海/双红高卷，不镜像人物。
图2只给无眼的灰bob和刘海身份/中性灰色；不复制它的脸型、头角、光影或衣装。图3只参考已认可的单束开放宽灰卷带画法：恰两个大转、再有自带灰front及不透明灰内返回的一个小转，然后渐细连续C。不能把小C同时充小转，不能多一大圈。所有被手、袖、肩褶隐藏的部分仍计入整束总圈数，遮挡后不重新长一套卷。实际空气孔才透明，实质灰返回保持不透明，mint仅一条窄材料边；不封成长方筒、柱体/实心锥、叠盘、密集圆环或独立吊坠。正常体量按本头肩透视，不能缩小首圈来凑全卷入框，末端可以真实被遮住或落到画幅外。
图5是最新实际审核过连接的无眼只读小裁片，只取关系：本体bob下缘的低耳后/nape灰发，经恰两颗红珠扎结，直接接同一束灰钻发。它不是另一套圈数、垂轴、衣服、头角或尺寸模板。该裁片只露局部首转，绝不能再在它下方加图3一整套卷。根不能高挂帽叶/太阳穴；两珠不能分到另一耳，珠与卷不得悬空断开，也无第三红点/碎珠。
本人物自身LEFT固定不换，近正面通常画右。按图1实际头转向保持远近耳关系；本源画左近耳只有短bob，LEFT低根在画右下bob末端，根珠可被头发/脸颌真实遮住一部分。唯一灰卷落在本人左肩前的颈胸一侧，宽灰正面覆盖白肩frill内侧/胸前衣料，不能整束挂在肩外空白处。前景食指、横手、交叉前臂/袖口可以遮中下段，露出部分保持正常首圈宽和体量，不为露全改原手势或把卷放到手上。
图4只眼内两灰及浅灰上凸圆弧，眼外形、眼白/黑睫/眼线、白glint全由图1决定。深灰主体RGB72/69/67，底部浅灰RGB129/128/128；参照认可基线的饱满向上拱起圆弧，深灰仍占主体，不做覆盖大半iris的浅灰，也不压成底部扁窄条。按本眼宽高、头倾斜和遮挡适配内部色界，无独立中央黑瞳点。保原小白高光，不加尖锐巨大高光，不新增眼下装饰痣。每张人物通过审核后，正常睁开的眼睛仍另外Python局部校准；眯眼、闭眼或全遮眼逐眼实际核查后跳过，不能强行睁眼或造虹膜。
简笔灰/mint平涂，内侧灰返回略深可接受；不带银白高光、金属渐变或密发丝，不因局部灰色差挖空实体。保原PV不规整轮廓、疏简粗细起伏黑线和尖收笔，不能向量化精修。只输出当前源中实际可见的整个人物{size}透明RGBA PNG；保所有已可见帽叶/手/衣边/鞋，源底截断不补隐藏身体。无背景、字幕/底块、导框、花瓣或其它独立后期层。'''
    if len(refs)==6:prompt+='\n图6仅给片尾原制服的灰绿色衣身/短泡袖/裙与黑胸结配色；衣服版型、手套、长袜/鞋和裁切全部按图1，不改成白裙或长袖。\n'
    pf=run/'prompt_api.txt';pf.write_text(prompt+'\n',encoding='utf-8')
    q={'schema':'direct_missing_first_own_pose_reviewed_junction_baseline_round_arc_v17',
       'id':ident,'source_frame':job['source_frame'],'source_pts':job['source_pts'],'source_time_base':'1/16000',
       'source':ev(source),'guide':ev(guide),'guide_frame':job['source_frame'],'guide_pts':job['source_pts'],
       'parameters':{'PromptFile':str(pf),'InputImages':[str(x) for x in refs],'OutputDirectory':str(run),'Size':size,'Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':ident+'_FIRST_OWN_POSE_REVIEWED_LOW_ROOT_ROUND_ARC_V17','DrawingId':ident,'OperationKind':'first_missing'},
       'model':defaults['api_request_policy']['model'],'n':defaults['api_request_policy']['n'],'retry':defaults['api_request_policy']['retry'],'provider':ev(ROOT/'scripts/Invoke-ReferenceImage.ps1'),
       'prompt':ev(pf),'refs':[ev(x) for x in refs],'eye_color_policy':defaults['eye_color_policy'],
       'requirements':ev(req),'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04','own_action':action,
       'controlled_reference_change':'Add exact newly reviewed no-eye low-bob/two-bead junction ONLY after prior no-junction FIRSTs placed roots high or beads on wrong ear. It cannot supply coil count or pose. Retain complete approved coil construction. No polished threeview, failed full art or rejected shoulder placement crop supplied.',
       'root_junction_provenance':ev(junction.parent/'PROVENANCE.json'),
       'latest_eye_baseline_clarification':ev(BASE/'review/USER_X01_14_LIGHT_ARC_BASELINE_CHECK_20261104_v01/BASELINE_COMPARISON_AND_USER_FEEDBACK.json'),
       'previous_family_candidate':{'id':job['previous_in_family'],'image':ev(previous['image'])},
       'source_provenance':{'JOB':ev(parent/'JOB.json'),'registration':ev(parent/'REGISTRATION_PLAN.json'),'source_bbox':job['source_bbox_xyxy'],'crop':job['crop_xyxy'],'guide_is_reference_only_not_photography_proof':True},
       'prepared_utc':datetime.now(timezone.utc).isoformat(),'prep_only':True,'submitted':False,
       'scope_boundary':'Own current source/guide determines exact visible scope. No temporal playback, source equivalence or user acceptance certified.'}
    (run/'DIRECT_REQUEST.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'id':ident,'run':str(run),'request':ev(run/'DIRECT_REQUEST.json'),'API_calls':0},ensure_ascii=False))
