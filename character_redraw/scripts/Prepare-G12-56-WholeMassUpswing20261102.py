"""Prepare a whole repair with a curl-only motion reference and no old tilted face."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-56/v01'
run = parent / 'whole_imggen_wholecoil_out_up_from_lowroot_v06'
if (run / 'request_imggen.json').exists():
    raise SystemExit('Existing request preserved.')
(run / 'inputs').mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
target = parent / 'whole_imggen_upright_localpose_identity11_no_oldtilt_v05/character_imggen_original.png'
previous = base / 'drawings/ART-G12-55/v01/whole_imggen_after_upturn_gray_mask_v05/character_imggen_original.png'
assert sha(target) == 'cf2ff71bb4aed96556ca599be6fedb9da515046bef3a45d3911a2aa4f5e21fb2'
assert sha(previous) == 'fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1'
crop = run / 'inputs/ref2_PREVIOUS55_LOW_BEADS_WHOLE_UPTURN_NO_EYES_READONLY_CROP.png'
box = [666, 400, 900, 620]
with Image.open(previous) as im:
    im.crop(tuple(box)).save(crop)
save(run / 'inputs/READONLY_CROP_PROVENANCE.json', {
    'source': str(previous), 'source_sha256': sha(previous), 'crop_xyxy': box,
    'output': str(crop), 'output_sha256': sha(crop),
    'operation': 'Unrotated unretouched native crop only; no target-art editing, pose drawing, compositing or adoption.',
    'role': 'Previous55 whole curl mass relative to low beads, continuation of outward/upward phase only; no eye/face/head tilt template or absolute scale authority.'})
refs = [target, crop, parent / 'inputs/source_pose_guide.png',
        base / 'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
        base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png']
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''参考1整个人连贯重画，只修钻发整体摆向，保持这张已正确的较直立头姿、眼开度视线、小波闭口、短灰bob、两只手/衣领/肩褶和身体。参考3当前原PV1066是动作唯一依据，不复制原高红钻发身份。
现在参考1的错误是两块主灰卷整体往珠根下方垂，只有小C尾勾向上。这不算整束继续上扬。把整束主轴从固定低珠根向画面右侧外甩并斜向上提，主体宽灰前面/返回面在珠根侧边接近同高并继续向外上抬，不能仍将两块主卷叠在珠根下。末端C随整个灰卷一起转移，不是只把C抬高。参考2为上一稿55同一低根附近的整个外翻灰卷，只给整束主面/返回面相对珠根的外翻趋势；本56继续外上扬，绝不回挂。参考2没有眼和整体头，不用它改变参考1已修好的头姿或相同身体手式。
低红珠安装点不动，仍在画面右侧远侧LEFT低耳后/下颌后颈侧，root不能随上扬抬到眼下或太阳穴。让卷绕这个固定根甩起。上扬部分在bob后、抬高手/白褶后时按真正层次遮住，不为展示整卷穿手或抬肩，不强露全部尾端。只一组红双珠和一束卷，不镜像人物。固有发量和灰带宽度沿参考1与前55合理比例，不缩成细饰品，不扩大成巨卷。
同一连续宽灰发片的前面翻回内后返回面再接下一圈、收细C，参考4给此构造。所有可见返回面保持宽灰且不透明，真正空气才透明，不挖固定洞，不画封口盘堆/实心筒芯贴绿线。灰bob和卷全部面同无打光平涂灰，较细薄荷材料带，参考5只色料，无独立亮边、暗内腔或渐变。
原1066高角形OK拇食合环+另三指弯伸、胸前横张分指与腕袖/前臂交叠、单charcoal平填瞳和普通小白点、暖桃肤、白maidcap两黑主叶、黑高领长袖、红胸结金扣、白肩褶袖口/围裙腰带后结和裙底裁切全部保留。不要回到旧55歪头/半睑或改变手。一次完整连贯重画头发珠卷颈领肩手衣的连接，高质量真实透明RGBA，只人物，无背景字幕色卡棋盘，不补画外腿鞋。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-56', 'run': str(run), 'refs': [str(p) for p in refs],
     'reference_sha256': [sha(p) for p in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'local_repair_parent': str(parent / 'mask_prep_source1066_headpose_aperture_v03'),
     'source_frame': 1066, 'first_case_frames': [1062,1066],
     'changed_hypothesis': 'Current upright56 full target retained; previous55 low-beads plus entire curling mass cropped without eyes/old tilted face supplies actual outward/upward whole-mass reference, not terminalC-only lift.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
save(run / 'request_imggen.json', q)
print(json.dumps({'request': str(run / 'request_imggen.json'), 'sha256': sha(run / 'request_imggen.json'),
                  'readonly_motion_crop': str(crop), 'calls': 0}, ensure_ascii=False))
