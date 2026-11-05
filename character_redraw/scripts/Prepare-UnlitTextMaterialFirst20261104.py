"""Prepare unissued FIRSTs with no shaded coil illustration in API inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
progress = read(base / 'PROGRESS.json')
registry = read(base / 'ASSET_REGISTRY.json')
for drawing_id, frame, previous in [
    ('ART-G13-21', 1290, 'direct_first_api_source1290_approvedCurl_noEyes_grayRGB_v09'),
    ('ART-G33-37', 2464, 'direct_first_api_source2464_grayeye_approvedCoil_noEyeLowNape_v09'),
]:
    parent = base / 'drawings' / drawing_id / 'v01'
    row = next(r for r in progress['records'] if r['id'] == drawing_id)
    assert row['status'] == 'pending' and not row.get('image') and not registry.get(drawing_id, {}).get('image')
    assert not list(parent.parent.rglob('attempt.json'))
    assert not list(parent.parent.rglob('BUILTIN_GENERATION.json'))
    old = parent / previous
    q = read(old / 'DIRECT_REQUEST.json')
    run = parent / f'direct_first_api_source{frame}_noCoilColorRef_unlitRGB_v10'
    run.mkdir(exist_ok=False)
    refs = [Path(q['parameters']['InputImages'][0]),
        base / 'inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png',
        base / 'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/EYE_GRAY_PALETTE_ONLY_NO_SHAPE.png',
        base / 'inputs/approved_curl_and_root_NO_EYES_20261104_v02/ORIGINAL_LOW_NAPE_TWO_BEADS_NO_EYES.png']
    action = q.get('own_action', '逐侧依图1本帧头颈、眼口手和全身动作，不套相邻稿。')
    if drawing_id == 'ART-G33-37':
        action = '头颈按本源轻斜，两不等圆弧睁眼/白glint与小闭弧笑。画左高手更上举、长指组靠拢且外侧指分开；画右低手长指朝右上扇开、拇指朝下，不套36近水平手。保黑红白maid衣、裙新折摆与腿错位：画左后鞋斜横、画右前鞋较直下，双踝带鞋完整可见，不裁补。'
    size = q['parameters']['Size']
    prompt = f'''{drawing_id} FIRST，{action}
图1是本帧原PV唯一姿态、头颈/身体透视、各眼形/开合/视线/glint、嘴、各手/指组/cuff和原衣装/可见范围依据，也是疏简粗细起伏黑线与平涂画法依据。不是精修插画，不加密发丝、写实指节或掌纹，不把斜头转正、不镜像人物。源红尖长发/高双红卷全部换成短圆灰bob自然刘海与唯一低LEFT卷；保原白maidcap倾角与两片MAIN黑叶。
本次没有输入任何彩绘卷发图，以避免把参考里的暗返回/亮带带入。图2仅无眼的灰bob/刘海身份局部；图4仅原人设低耳后/nape发根连接：灰本体发经恰好两红珠接同束灰发，不在帽叶旁/太阳穴，不额外加第三珠/碎红点，不搬它的衣物或光影。固定人物自身LEFT，按本帧头颈和肩的近远遮挡投影。近正面通常画右，从低根自然垂在自身LEFT肩前颈胸，肩frill/手可实际遮住部分，露出部分正常体量；不为显全穿手或整束挂在袖外空白。
卷是一条连续宽灰发带绕空心轴：两大完整转之后另有一个小完整转的灰front/不透明灰内后返回，再渐细为C。灰front→灰返回→下一转逐段连续；不用封口盘堆/实心锥、不加圈、不把窄C同时当作小转，不把第二大钩充第三小转。只在真实空气空隙透明，实体返回必须保留灰和alpha。
全部灰bob、各大转front、inner/back-return、小转和C都以同一个无打光灰RGB(179,174,173)作平涂。结构用黑墨线、遮挡和轮廓表达；返回仍是同灰的实际面，绝不沿用旧红卷暗楔、不另涂暗灰底板、不按受光/背光区分灰色。薄mint仅窄材料边，不能作大主面。衣物也按原PV平涂，不加柔亮带、银白闪线、体积渐变或云雾。图4的反光/阴影不得传给灰bob或返回。
图3只眼黑配色：全部主体包括上半用dark约RGB(72,69,67)，内下较浅灰约RGB(129,128,128)，保源真实眼黑形/大小/视线/开合/glint，不搬母图眼形和浅灰块形状。不新增中心黑点，不在纯黑iris上叠灰圈；黑仅作原墨线/睫线。闭眼/遮眼不造iris。眼白与真实小眼角短笔保，明显独立装饰痣不加。
整张当前可见人物RGBA透明，保全图1实际露出的帽/手/衣边/鞋，底裁按源，不画隐藏身体。无粉背景、字幕/文字底块、导框、独立道具。输出{size}透明PNG。'''
    pf = run / 'prompt_api.txt'
    pf.write_text(prompt, encoding='utf-8')
    q['parameters'].update({'PromptFile': str(pf.resolve()), 'InputImages': [str(p.resolve()) for p in refs],
        'OutputDirectory': str(run.resolve()), 'Stage': drawing_id + '_MISSING_FIRST_NO_COIL_COLOR_REF_UNLIT_RGB',
        'DrawingId': drawing_id, 'OperationKind': 'first_missing'})
    q.update({'provider': ev(root / 'scripts/Invoke-ReferenceImage.ps1'), 'prompt': ev(pf),
        'refs': [ev(p) for p in refs], 'own_action': action,
        'previous_zero_call_prep_preserved': str(old.resolve()),
        'reference_roles': ['Own PV pose/style/eye shape/glints/costume/extent', 'Gray bob bangs only; no eyes',
            'Accepted eye colors only; no eye geometry', 'Original low ear/nape two-bead attachment only; no eyes or lighting'],
        'controlled_reference_change': 'Remove all colored coil-rendering examples after repeated dark returns. Test textual continuous-ribbon geometry plus one explicit unlit gray for front/return, while keeping original low-root geometry and accepted eye colors. Normative user-approved X01 remains the review baseline, not an API input.',
        'prepared_utc': datetime.now(timezone.utc).isoformat(), 'prep_only': True, 'submitted': False, 'root_release': False})
    (run / 'DIRECT_REQUEST.json').write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'id': drawing_id, 'run': str(run.resolve()), 'input_count': len(refs), 'calls': 0}, ensure_ascii=False))
