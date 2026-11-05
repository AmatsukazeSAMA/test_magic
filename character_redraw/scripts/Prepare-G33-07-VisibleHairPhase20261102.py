"""Prepare a source-first whole redraw with an actual hair-only phase reference.

Only crops/copies references and records a PREPONLY request; never edits output art.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G33-07/v01/whole_imggen_source2333_upperreturn_lowerC_v13'
run = parent.parent / 'whole_imggen_source2333_visible_horizontal_hairphase_v14'
if run.exists():
    raise SystemExit('Existing preparation preserved; do not overwrite or resubmit.')
q = json.loads((parent / 'request_imggen_ROOT_AUTHORIZED.json').read_text(encoding='utf-8-sig'))
inputs = run / 'inputs'
inputs.mkdir(parents=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
refs, evidence = [], []

def copied(path, name):
    src = Path(path)
    dst = inputs / name
    shutil.copy2(src, dst)
    refs.append(str(dst))
    evidence.append({'source': str(src), 'source_sha256': sha(src), 'output': str(dst),
                     'output_sha256': sha(dst), 'operation': 'byte-identical reference copy'})

def cropped(path, box, name, role):
    src = Path(path)
    dst = inputs / name
    with Image.open(src) as im:
        im.crop(box).save(dst)
    refs.append(str(dst))
    evidence.append({'source': str(src), 'source_sha256': sha(src), 'output': str(dst),
                     'output_sha256': sha(dst), 'operation': 'read-only reference crop',
                     'source_pixel_box': list(box), 'role': role})

copied(q['refs'][0], 'ref1_ORIGINAL2333_COMPLETE_UNMASKED_ACTION.png')
cropped(q['refs'][1], (0, 0, 255, 216),
        'ref2_CORRECT11_BOB_CAP_FACE_LOW_BEADS_NO_HANGING_COIL_TEMPLATE.png',
        'OC gray bob/head/cap/low bead identity only; full hanging curl removed to avoid competing vertical axis')
copied(q['refs'][2], 'ref3_USER_BROAD_GRAY_CONTINUOUS_FRONT_INNER_RETURN.png')
phase = base / 'inputs/motion_reference_upright_first10_20261031_v01/frames/R000022.png'
cropped(phase, (546, 259, 611, 311), 'ref4_R22_HAIR_ONLY_OUTWARD_PHASE_NO_EYES_BODY.png',
        'only direction/elastic phase; excludes eyes, face expression, hands and body; not solid-cone construction')
copied(q['refs'][3], 'ref5_UNLIT_GRAY_MINT_INK_MATERIAL_KEY.png')

prompt = '''辫子固定在人物自身的左侧，不是画面左侧；正面通常位于画面右侧。人物转到侧面或背面时，仍保持同一个解剖左侧的低耳后发根，按当前转向和遮挡投影，不能换边或镜像人物。

整张重新绘制原PV2333当前可见人物，透明背景，保持图1共同构图和所有表演：近正面轻倾头、圆睁不对称眼、极小中性闭口；一臂折腰后、另一长臂斜跨身到画左下分指低掌；原黑白长袖女仆衣、红bow金扣、白frill袖口腰带/后bow、长apron锯齿边黑裙、屈膝后抬腿和前腿交错。原前鞋端贴底截断，不补源外鞋尖、不缩人露全鞋；其后first861..862半身摄影另定。图2只灰短bob/帽/低珠身份，不套图2眼口或动作；不要画图1红发双高卷。

本次重点是图4的外甩相位：唯一LEFT低耳后双红珠保持画右同一低根，主卷从珠下向画右伸出，轴线接近水平、末端略回弯，不能沿肩竖直下挂。根不随尾抬高；卷的主要体积在低耳向外的高度，与头侧留有自然回折。图4只头发的方向与弹性，不复制它的封闭实体造型，不改变原PV头眼身手。发量按整头肩常规宽卷，不巨粗或tiny绿挂件。

把图3连续宽灰发带构造沿这个外甩轴画出来：宽GRAY前面弯回内/后返回，接入下一圈，逐圈收细到自然C回钩；上端入口/出口也连成同一发带，不是独立椭圆盖盘，更不是实心锥柱外贴mint螺纹。用轮廓线、互遮和实际间隙表达绕行。opaque灰返回保留，只有真实空气透明；不固定圈数、孔数或轴长。bob/衣肩真实遮挡照画，不强露隐藏段。

图5是所有头发面的唯一材料：bob、卷的正面、内面、返回、背面均匀灰#B6B4B2；薄muted mint#B0C8BA只材料细带。返回不能另涂深灰楔块，C内弧也不能涂大块暗面。黑#171717只细轮廓/分界线，灰发没有光源、高光、体积阴影或渐变。暖桃肤，原黑白衣/红bow金扣不变；单色charcoal眼只依图1开度/视线，普通白小点。白cap两主要黑叶同根。

一次整人连贯重绘头颈、发根、外甩卷、领肩与衣身，不贴部件、不贴卷；只真实透明人物，不输出粉底、文字、棋盘格、色表、道具或第二束卷。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
out = {**q, 'run': str(run), 'refs': refs,
       'reference_sha256': [sha(Path(p)) for p in refs],
       'prompt': prompt, 'prompt_file': str(run / 'prompt_imggen.txt'),
       'prompt_sha256': sha(run / 'prompt_imggen.txt'),
       'tool_arguments': {'prompt': prompt, 'referenced_image_paths': refs, 'transparent_background': True},
       'PREPONLY': True, 'native_calls_authorized_this_record': 0,
       'native_calls': 0, 'submitted': False, 'automatic_retries': 0,
       'previous_known_return': {'path': str(parent / 'character_imggen_original.png'),
                                  'sha256': sha(parent / 'character_imggen_original.png')},
       'changed_reference_hypothesis': 'v13 text-only phase lost horizontal swing and returned large dark wedges. Remove full hanging-curl identity competitor; supply pure R22 hair bitmap for actual direction only, source-only action and no new dark inner material.',
       'repair_reason': 'v13 returned known saved; independent157 reports lost outward phase and large dark-gray return/C volume faces. No unknown-result retry.',
       'fresh_root_Sol_and_placement_required': True,
       'user_accepted': False, 'dynamic_validated': False}
for inherited in ['root_release', 'root_release_sha256', 'root_actual_input_review', 'root_actual_input_review_sha256',
                  'root_authorized_call_lock', 'root_authorized_call_lock_sha256']:
    out.pop(inherited, None)
(run / 'request_imggen.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(run / 'REFERENCE_CROP_PROVENANCE.json').write_text(json.dumps({
    'prepared_utc': datetime.now(timezone.utc).isoformat(), 'evidence': evidence,
    'generation_calls': 0, 'output_art_edited': False,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'run': str(run), 'request_sha256': sha(run / 'request_imggen.json'),
                  'refs': refs, 'generation_calls': 0}, ensure_ascii=False))
