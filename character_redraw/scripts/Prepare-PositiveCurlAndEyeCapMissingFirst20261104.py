"""Prepare latest positive-coil FIRST requests; no network/generation."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import hashlib

parser = argparse.ArgumentParser(__doc__)
parser.add_argument('ids', nargs='+')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
actions = {
    'ART-G13-28': '本态画右倾头、不等睁眼/原小白glint保持，但嘴已经打开为窄粉色笑缝，不能冻结27闭弧笑。胸前两臂交叉，画右脸旁两手再次换形：后手两根长指向上，其中右侧长指有明确折弯锯齿，前手横向朝画右大张，长直横指、下方并拢短指和向下分开的拇指均按源；保简笔尖角/怪折和斜交掌缘，不修成规整写实手或照抄27前竖掌。两白cuff各自角度、黑袖肘交叠、肩frill/红bow金扣/腰apron后带依自身宽guide，半身底裁不补腿鞋。帽仍只有自身两片主要黑叶。',
    'ART-G13-26': '本态双眼重新睁开，原不等圆眼黑/小白glint、画右倾头和小闭弧笑保持，不冻结25闭眼线。交叉前臂，两手抬在画右脸边：源刻意为大块尖角/锯齿掌指剪影，两簇长指尖向画右下，前后裸手有一条长斜分界且两白cuff角度不同；极简折角按源保留，不能美化成25向上五指展开手或写实手，不用本次两灰眼参考迁移外形。黑红白长袖maid、肩frill、红bow金扣、腰apron和后带按自身较宽guide，原半身底裁不补腿鞋。帽保自身两片主要黑叶。',
    'ART-G13-27': '头仍向画右斜但角度按自身源，不等圆睁眼/原glint和小闭弧笑保持。胸前交叉两臂，脸画右两手比26尖角团明显改为展开形：前手长指向上、侧指向右上斜张；后手在画右横向露出少量短长不等的指组，两手掌缘互叠、两只异角白cuff前后压着。保源极简不规整指长/指缝和关节省略，不把26下尖锯齿团或25横向前手冻结到本态，不补写实掌纹。黑红白长袖maid/白frill/红bow金扣/腰apron后带依自身较宽guide，原半身底裁不补腿鞋。帽依自身两片主要黑叶。',
    'ART-G13-25': '本态头向画右轻斜，双眼闭成粗黑弯弧，完全不见iris；保留自身闭眼线、小闭弧笑和颌耳/颈领透视，不套24半开眼或新增眼黑/高光。胸前交叉两臂，画右脸旁两裸手展开互叠：后手长指偏竖向上，前手指组大幅向画右横张，极简尖指和锯齿折角、拇指分支、两只不同角白cuff依自身guide逐一保留，不修成规整写实五指或合十。黑红白长袖maid/肩frill/红bow金扣及腰apron后带按自身宽guide，原半身底裁不补腿鞋。原帽只有自身两片主要黑叶和共同短根，不照24返图的第三整片黑叶。',
    'ART-G13-22': '头近正面但原轻斜/颌耳颈领关系保持，两不对称圆睁眼/原白glint与小闭弧笑。胸前交叉前臂，两裸手移到画右肩/脸侧互相交叠，长指是原PV尖角展开剪影、尖指组和拇指侧分彼此穿插，两手各自白cuff一前一后。不能把它画成上一帧两根竖食指V手、合十、握拳，不能把源尖角手指补成写实规整五指。两黑袖肘斜交、白frill/红bow金扣/腰围裙与后带依自身较宽guide可见范围。下方为原半身裁切，不补腿鞋。',
    'ART-G13-23': '头显著向画右倾斜，颌耳/颈领与身体仍同一原PV透视；双不等睁眼、原白glint和小闭弧笑保。交叉前臂，两张开的裸手在画右脸边互遮：画左的前手长指偏上，画右后手指组更横向张开；逐一保留源极简指长、指间尖缝、拇指分支及异角白cuff，不照抄22的收窄尖角剪影，不合十/同手镜像/补密掌纹。黑袖肘斜交、原白frill与红bow金扣、腰围裙后带及半身底裁照自身guide，不补腿鞋。',
    'ART-G13-24': '头仍明显向画右斜，但两眼比上一态压低为半开，原眼黑受上睑裁切、原小白glint和小闭弧笑保持，绝不能套23的大圆睁眼。胸前两前臂交叉，画右脸旁两手为原PV刻意简化的尖角剪影：长指组由朝上变为朝画右下/右外的大三角尖，掌缘和指缝有极简锯齿折角，两个异角白cuff分前后。不修成写实五根圆手指、不套上一张张开的正常手、不合十。黑长袖、白frill/红bow金扣、腰围裙及后带按实际较宽guide，半身底裁不补腿鞋。',
}
defaults = read(root / 'image_defaults.json')
eye_policy = Path(defaults['eye_color_policy']['path'])
assert sha(eye_policy) == defaults['eye_color_policy']['sha256']
requirements = Path(read(base / 'GOAL_EXECUTION.json')['review']['mandatory_curl_requirements']['path'])
progress = {r['id']: r for r in read(base / 'PROGRESS.json')['records']}
registry = read(base / 'ASSET_REGISTRY.json')
tail = [base / 'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png',
        base / 'inputs/approved_curl_and_root_NO_EYES_20261104_v02/APPROVED_X01_GRAY_COIL_NO_RED_ROOT.png',
        base / 'inputs/eye_palette_and_internal_arc_NO_OUTLINE_20261104_v01/DARK_AND_LIGHT_LOWER_ARC_ONLY.png',
        base / 'inputs/approved_curl_and_root_NO_EYES_20261104_v02/ORIGINAL_LOW_NAPE_TWO_BEADS_NO_EYES.png']
for drawing_id in args.ids:
    assert drawing_id in actions
    row = progress[drawing_id]
    assert row['status'] == 'pending' and not row.get('image') and not registry.get(drawing_id, {}).get('image')
    parent = base / 'drawings' / drawing_id / 'v01'
    assert not any(p.name in {'attempt.json', 'BUILTIN_GENERATION.json', 'result.json'} for p in parent.parent.rglob('*.json')), 'Prior execution exists.'
    job, reg = read(parent / 'JOB.json'), read(parent / 'REGISTRATION_PLAN.json')
    source, guide = Path(job['source_image']), parent / 'inputs/source_pose_guide.png'
    assert sha(source) == job['source_image_sha256']
    run = parent / f"direct_first_api_source{job['source_frame']}_positiveCoil_innerGrayTolerance_eyeCap_v11"
    run.mkdir(exist_ok=False)
    size = 'x'.join(map(str, reg['guide_dimensions']))
    prompt = f'''{drawing_id}，未出图原画的一次FIRST绘制。{actions[drawing_id]}

图1是自身原PV，只由它决定动作、眼形/视线、头颈身体透视、手势/互遮、衣服、简笔墨线和实际可见裁切。保原黑红白长袖maid制服、白肩frill/围裙、红bow和金扣；原白maid帽及两片主要黑叶依本头角。删原双红高卷和红刘海，替换为短圆灰bob以及唯一自身LEFT低耳后钻发，不镜像人物。
图2只短灰bob刘海身份/灰色，不含眼睛，不迁移参考正脸或上色光影。图3是用户认可X01的钻发画法：一条宽灰发带连续绕空心轴，两个正常大灰转、另一个真实小灰转，再连续收尖C；灰front经实际不透明灰内返回接下一转，窄mint材料边跟随发带。不把第二大钩/单独mint线当小灰转，不缩成堆小圆盘/碗/微型挂件，不加多圈/封成实心柱或挖掉实体灰返回。图3供结构和画法，不固定它的像素大小、轴向或头肩姿势。
图5仅低耳后/后颈连接：本体灰发→恰两颗红珠扎结→同束灰卷根，不在帽叶旁或太阳穴高扎，不新增第三红点/红碎块。按图1头角投影固定人物自身LEFT，本近正面通常画右，正常体量垂至自身左肩前的颈胸一侧。前景手、肩frill可以遮住一部分卷，隐藏部分不要硬露到手上；露出部分保持正常宽度卷径，不能为了展示全卷向脸外空白移开或缩小。
沿用原PV简笔黑线粗细起伏、简略尖收笔和不规则轮廓，以及灰/mint平涂。内侧返回可以是较暗灰，用户已说明此项问题不大，不要求所有卷面同一RGB，不为消除暗返回牺牲两大一小结构。避免银白闪带、金属高光、独立碎片、额外打光或精修密发丝。
图4只含眼黑内部两灰及下部向上拱起的浅灰圆弧，没有眼黑外轮廓、白glint或脸。深灰主体约RGB(72,69,67)，内下浅灰约RGB(129,128,128)，浅灰圆弧按本眼宽高、原头倾斜和遮挡适配，不能套水平直色带。原眼黑外形、开合、视线、白glint和墨线按图1，不加中心黑点；不把原纯黑iris留作大面积上半。闭眼/完全遮眼不新增iris。返图人物审核通过后，所有正常睁眼另做一次局部Python核色和内部浅弧校准，去中央黑瞳孔；眯眼、闭眼和全遮眼按单眼实查跳过，不能强行睁眼/补iris。人物待修先修人物再调眼，不为改眼色再用API。
只输出整张源中实际可见人物，{size} RGBA透明PNG，保全已可见帽/手/衣边。原半身底裁不补隐藏身体，不画粉背景/文字/文字块/独立道具/导框。'''
    prompt_path = run / 'prompt_api.txt'
    prompt_path.write_text(prompt, encoding='utf-8')
    refs = [guide, *tail]
    request = {'id': drawing_id, 'source_frame': job['source_frame'], 'source_pts': job['source_pts'],
        'source': ev(source), 'guide': ev(guide), 'guide_frame': reg.get('source_frame') or job['source_frame'],
        'guide_pts': reg.get('source_pts') or job['source_pts'],
        'parameters': {'PromptFile': str(prompt_path), 'InputImages': [str(p) for p in refs],
            'OutputDirectory': str(run), 'Size': size, 'Quality': 'high', 'Background': 'transparent',
            'OutputFileName': 'character_api_original.png', 'Stage': drawing_id + '_MISSING_FIRST_POSITIVE_COIL_LATEST_EYE_CAP',
            'DrawingId': drawing_id, 'OperationKind': 'first_missing'},
        'model': 'gpt-image-2.5-sunburst', 'n': 1, 'retry': 1,
        'provider': ev(root / 'scripts/Invoke-ReferenceImage.ps1'), 'refs': [ev(p) for p in refs],
        'prompt': ev(prompt_path), 'eye_color_policy': ev(eye_policy), 'curl_requirements': ev(requirements),
        'curl_structure_policy_id': 'hollow_two_large_one_small_20261102_v04',
        'own_action': actions[drawing_id],
        'controlled_reference_change': 'Restore positive approved X01 curl drawing/geometry after count failures without coil reference; permit inner gray depth; no strict same-RGB demand. Internal eye palette/arc crop excludes all outer eye shape and glints.',
        'scope_boundary': 'Each own wider original guide supplies actually visible extent, not proof of canonical/wider cel/camera equivalence or dynamic acceptance.',
        'prepared_utc': datetime.now(timezone.utc).isoformat(), 'prep_only': True, 'submitted': False}
    (run / 'DIRECT_REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'id': drawing_id, 'run': str(run), 'API_calls': 0}, ensure_ascii=False))
