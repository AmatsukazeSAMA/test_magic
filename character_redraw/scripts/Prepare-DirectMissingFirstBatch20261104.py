"""Prepare inspected original-PV FIRSTs; never submit an image request."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

p = argparse.ArgumentParser(__doc__)
p.add_argument('--low-root-reference', action='store_true')
p.add_argument('--approved-curl-no-eyes', action='store_true')
p.add_argument('ids', nargs='+')
a = p.parse_args()
if a.approved_curl_no_eyes:
    a.low_root_reference = True
root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda f: json.loads(f.read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
ev = lambda f: {'path': str(f.resolve()), 'sha256': sha(f)}
actions = {
    'ART-G12-73': '头低俯、闭眼下弧短睫与小闭弧笑，保持头颈下颌耳位。本张无眼黑，不准为应用灰眼配色睁眼。两黑长袖臂向左右低位外展，画左手长指斜上朝外、分出的拇指朝下，画右手指组水平朝外，指组轮廓和各自白cuff照自身源，不把两手画对称。半身底裁，不补腿鞋。',
    'ART-G12-74': '头抬起近正面，两不对称睁眼、原白glint和小闭弧笑照源，保持颌耳与颈领关系。黑袖双臂低位侧展，两裸手更张开，画左与画右的长指/拇指分叉方向不同，逐侧依原线不要镜像对称或换手。白cuff、白肩frill、红bow金扣、腰围裙与后带保原半身底裁。',
    'ART-G12-75': '头抬起近正面、两不对称睁眼与小闭弧笑。胸bow一侧有横线另一侧是斜折，金扣略斜，与上一张不同。双侧黑袖臂低位外展，两裸手指组张开，画右指组折角不同、各自拇指朝下分开，双手不能套上一张或镜像对称；白cuff倾斜、黑袖折线、后带和半身底裁全部依图1，不补腿鞋。',
    'ART-G13-15': '头向画左倾斜，两眼闭合短黑睫，细小粉O嘴；不能睁圆眼或把斜头摆正。本张没有眼黑可改色。两肘侧张、胸前双裸手为原PV极简角形剪影，画左手上尖/侧横指轮廓和画右高位横向尖指轮廓不同；保留它们在bow/白frill前的互遮及不完整指节，不补写实完整五指/掌纹。白cuff、黑长袖、红bow金扣、白腰围裙和两侧后带依自身较宽guide可见范围。',
    'ART-G13-16': '头向画左斜，两不对称睁眼和原白glint、细小粉O。胸前两裸手张开，画左手较低/长指斜竖/拇指向画右下分，画右手更高/两长指竖立其余指与拇指侧下分，指间空隙和掌内少量弧线照自身源；不能套上一张闭眼尖角剪影手、改为爱心/合十或补密掌纹。黑袖肘侧张、白cuff/frill、红bow金扣、腰围裙后带及实际底裁依源。',
    'ART-G13-20': '头轻斜画左，两眼不等睁开、原小白glint，细小粉O嘴。两肘向侧外折、前臂斜上，双手各有一根斜朝外上的长食指，其余指各自内折且拇指位置不同，保自身简笔折角/指间空隙及异角白cuff，不对称化为相同手、不补写实手掌。黑长袖、红bow金扣/白frill、腰围裙后带按guide实际可见半身底裁。',
    'ART-G13-21': '头与身体的原三分之四关系和倾角保持，双不等睁眼/原白glint、小闭弧笑与嘴角短笔依源，不把头转成镜头正面。胸前两前臂交叉，两个手分别有一个竖向食指、拇指侧分与其余内折，手的位置一高一低靠画右脸侧形成分开的V形，白cuff/黑袖与手互遮逐侧照图1，不能合成一只普通V手、不沿用上一张向两外指的动作。黑红白maid衣、bow/frill、腰围裙后带及实际底裁依源，脸边手/肩可遮住部分低LEFT钻发，不为露全移到手上。',
}
progress = read(base / 'PROGRESS.json')
api_policy = read(root / 'image_defaults.json')['api_request_policy']
registry = read(base / 'ASSET_REGISTRY.json')
inventory_path = base / 'review/xhigh_pending_artist/PENDING_FIRST_INVENTORY_AUDIT_20261104_v01/REPORT.json'
inventory = read(inventory_path)
eye_policy = base / 'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/POLICY.json'
refs_tail = [
    base / 'drawings/ART-G07-05/v01/direct_first_api_source510_samegray_return_material_factor_v04/inputs/ref2_USER_GRAYBOB_FACE_IDENTITY_ONLY_NO_CLOTHING_NO_COIL.png',
    base / 'inputs/samegray_coil_material_without_red_root_20261104_v01/GRAY_FRONT_RETURN_MINT_ONLY.png',
    base / 'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/EYE_GRAY_PALETTE_ONLY_NO_SHAPE.png',
]
if a.low_root_reference:
    refs_tail.append(base / 'inputs/identity_LOW_LEFT_ROOT_GEOMETRY_ONLY_20261104_v01/LOW_NAPE_EAR_TWO_BEADS.png')
if a.approved_curl_no_eyes:
    refs_tail[0] = base / 'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png'
    refs_tail[1] = base / 'inputs/approved_curl_and_root_NO_EYES_20261104_v02/APPROVED_X01_GRAY_COIL_NO_RED_ROOT.png'
    refs_tail[3] = base / 'inputs/approved_curl_and_root_NO_EYES_20261104_v02/ORIGINAL_LOW_NAPE_TWO_BEADS_NO_EYES.png'
for i in a.ids:
    assert i in actions, i
    row = next(r for r in progress['records'] if r['id'] == i)
    audit = next(r for r in inventory['rows'] if r['id'] == i)
    assert row['status'] == 'pending' and not row.get('image') and not registry.get(i, {}).get('image')
    assert audit['inventory_eligible_never_issued_FIRST'] and not audit['G49_restricted']
    parent = base / 'drawings' / i / 'v01'
    assert not list(parent.parent.rglob('attempt.json')), 'Prior execution must be classified before any new FIRST.'
    assert not list(parent.parent.rglob('BUILTIN_GENERATION.json'))
    job = read(parent / 'JOB.json')
    reg = read(parent / 'REGISTRATION_PLAN.json')
    guide = parent / 'inputs/source_pose_guide.png'
    canonical = Path(job['source_image'])
    assert sha(canonical) == job['source_image_sha256']
    suffix = 'grayeye_materialNoRedRoot_lowNapeContext_v07' if a.low_root_reference else 'grayeye_materialNoRedRoot_v06'
    if a.approved_curl_no_eyes:
        suffix = 'approvedCurl_noEyes_grayRGB_v09'
    run = parent / f"direct_first_api_source{job['source_frame']}_{suffix}"
    run.mkdir(exist_ok=False)
    size = 'x'.join(map(str, reg['guide_dimensions']))
    prompt = f'''{i} FIRST。{actions[i]}

图1是本帧原PV的唯一动作、眼形、手势、服装、可见范围与简笔平涂依据。图2只取短圆灰bob身份与发色，不取其眼形/纯黑眼色/正脸/发光渲染。把原红尖刘海与双红高卷换成本OC灰短bob与唯一低左根钻发；头、颈、身体原透视保持，不镜像身体。原白maidcap与恰好两片MAIN黑叶依自身倾角连接。
本体灰发→恰好两颗红珠扎结→同束灰卷发实际连接。仅两颗，绝无第三小红珠、红碎块或孤立红白小点。本近正面自身LEFT低耳后根通常投影画右。卷自然垂于自身LEFT肩膀前的颈胸一侧，按本肩、手和frill真实遮挡；遮住就不画隐藏段，露出部分仍有正常体量，不能缩成小挂件或为了显全移到肩袖外。
固有两大转、另一个真实小转、然后渐细C尾。连续宽灰front经有宽度的不透明灰内后返回接下一转，空心轴仅真实空隙透明；不封口成柱、不盘堆、不加圈，不把第二大钩或一条粗mint钩当作小灰转，不挖掉灰返回。
图3是删去所有红珠/红结的只读材料小裁片：只参考灰front与opaque灰返回使用同种灰、mint是窄边；不参考它的圈数、尺寸、轴、缺陷或渐变，它的父整稿仍待修。bob、所有卷面/返回/小转/C用同一无打光灰，衣物也按原PV色块平涂。以黑线和遮挡表达结构，不用深灰底板、白银反光、连续体积渐变、柔光云雾。保留原手书疏简粗细起伏黑线、尖收笔与不规则轮廓，不向量精修或增加密发丝/衣褶。
图4仅眼黑内部深灰主体+较浅灰色的配色条，不含眼形。若有可见眼黑，保持图1自身外轮廓、开合、视线、白glint并使用两灰配色，不新增中心黑点；闭眼不睁开，不借图2眼型。眼白/黑眼线和真实短睫保持，明显独立装饰痣不加。
整张当前可见人物RGBA真实透明，所有源中已可见的帽/手/衣边保全，原底裁不补隐藏身体。粉背景、字幕、黑文字块、导框和独立道具均不画。输出{size}透明PNG。'''
    if a.low_root_reference:
        prompt += '\n图5仅原人设耳下/低nape根部连接几何：bob末端和低耳后头发经两红珠扎向卷根，根不在帽叶旁/头顶/太阳穴。只取这个连接关系，不抄原参考的衬衣背心、头角、银白高光和光影；仍按图1本头角投影。红珠与MAIN黑帽叶分属不同高度与不同结构。\n'
    if a.approved_curl_no_eyes:
        prompt = prompt.replace('图3是删去所有红珠/红结的只读材料小裁片：只参考灰front与opaque灰返回使用同种灰、mint是窄边；不参考它的圈数、尺寸、轴、缺陷或渐变，它的父整稿仍待修。',
            '图3改用用户认可X01卷发的只读局部，已裁去红根：只参考连贯灰发带、两大另小转/C和实质opaque灰返回的画法，mint是窄边；不固定其像素尺寸/轴/姿势，不取旁边衣物或柔色差。旧待修稿G13-09材料已经不作为输入。')
        prompt += '\n图2与图5都不含眼睛；眼黑全部主体（包括上半）用认可图dark约RGB(72,69,67)，内下较浅灰约RGB(129,128,128)，不是在纯黑虹膜上叠灰圈。黑色只用于源睫/眼线等墨线，不作iris主面；无中心黑点。仍保持图1眼黑真实外形/开合/视线/glint，不能搬调色母图的眼型或浅灰块形状。\n'
    pf = run / 'prompt_api.txt'
    pf.write_text(prompt, encoding='utf-8')
    refs = [guide, *refs_tail]
    request = {
        'id': i, 'source_frame': job['source_frame'], 'source_pts': job['source_pts'],
        'source': ev(canonical), 'guide': ev(guide),
        'guide_frame': reg.get('source_frame', job['source_frame']),
        'guide_pts': reg.get('source_pts', job['source_pts']),
        'parameters': {'PromptFile': str(pf.resolve()), 'InputImages': [str(f.resolve()) for f in refs],
            'OutputDirectory': str(run.resolve()), 'Size': size, 'Quality': 'high',
            'Background': 'transparent', 'OutputFileName': 'character_api_original.png',
            'Stage': i + '_MISSING_FIRST_GRAYEYE_MATERIAL_NO_RED_ROOT',
            'DrawingId': i, 'OperationKind': 'first_missing'},
        'model': api_policy['model'], 'n': api_policy['n'], 'retry': api_policy['retry'],
        'provider': ev(root / 'scripts/Invoke-ReferenceImage.ps1'), 'prompt': ev(pf),
        'refs': [ev(f) for f in refs], 'own_action': actions[i],
        'eye_color_policy': ev(eye_policy), 'inventory_audit': ev(inventory_path),
        'curl_structure_policy_id': 'hollow_two_large_one_small_20261102_v04',
        'controlled_reference_change': ('Replace failed repair-candidate material with user-approved X01 curl-only crop; exclude all eyes from identity/root refs, retain low nape geometry and actual accepted gray-eye color examples. No success assumed.' if a.approved_curl_no_eyes else 'Add original-identity low nape/ear/two-bead connection context after high-root failures; geometry only, never its clothing or lighting. Material-only crop still excludes red fragments.' if a.low_root_reference else 'Material crop excludes all red root beads/bow; no rejected extra red fragment can transfer. Not a new geometry or user baseline.'),
        'scope_boundary': 'Own wider original guide may supply actually visible extent; not proof of identical original cel, camera, exposure or temporal continuity.',
        'prep_only': True, 'submitted': False, 'root_release': False,
    }
    (run / 'DIRECT_REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'id': i, 'run': str(run.resolve()), 'input_count': len(refs), 'generation_calls': 0}, ensure_ascii=False))
