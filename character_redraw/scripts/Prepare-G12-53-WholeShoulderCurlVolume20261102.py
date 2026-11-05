"""Prepare whole repair of Sol148-confirmed extra curl length below the forearm."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-53/v01'
old = parent / 'whole_imggen_ORIGINAL1050_sourcefirst_farLEFT_v04'
run = parent / 'whole_imggen_source1050_leftroot_shoulder_volume_v05'
assert not (run / 'request_imggen.json').exists(), 'Existing request preserved.'
run.mkdir(exist_ok=True)
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
refs = [old / 'character_imggen_original.png', parent / 'inputs/source_pose_guide.png',
        base / 'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
        parent / 'draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
        base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png']
assert sha(refs[0]) == 'f7a5282b51f01d4b336e845a8605210c9b0932fe360ff10bd4b1e95536e85545'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''完整重新绘制参考1当前灰短bob女仆，保其已经正确的远侧LEFT低珠根和圆睁眼睛/原手势，但修复“钻发臂下额外延长到腰的大卷尾”。现在参考1根下已有合理宽灰前返，经过胸前手和黑前臂遮挡后，又在臂下露出很粗的灰波状面和大C，这一整块额外长度/尾团是错的；整束不能贯穿颌—胸—腰。不要仅把末尖缩小而保长轴，不把旧大C上贴成新接缝。
将钻发的固有完整长度与体量重新画回参考3那种相对于整头、肩与上胸的合理尺寸：宽灰上端和连续返回仍足量，随后自然渐细到C，不巨大长粗，也不能缩成小绿挂件。卷尾应回收在肩/上胸与胸前手附近的路线内；如果当前原手/原高黑前臂/白肩褶挡住末段或C，按真实前后关系让那部分在后面，不为了显示完整C再延长到臂下腰边。原手、原袖口、原黑臂、原白肩褶全部原尺寸/原位置，不能放大衣服或挪动手臂来假造遮挡。隐藏几何不强画出。
本正确根不能退回旧错误侧：唯一LEFT低耳后/nape双红珠在本向画右front3quarter的远侧画右bob下缘/颌后，画左清楚可见近RIGHT耳后无珠/卷。保参考1这个低根，不抬高、不镜像、不把原PV红近卷换灰贴到画左。bob/珠可自然互遮。
一束连续宽gray发带从此低根卷行，宽前面向内/后翻回并斜接下圈，再逐渐变细成合理C；参考4只给前/返构造，不抄打光。不是封口盘帽堆/实心锥柱贴绿线/断段管或细S；灰返回本身不透明，只有真实空气透明，不靠固定孔数/圈数/比例或挖灰面修。bob、全部卷面同一无打光gray，薄mutedmint材料边，图5只颜料，无独立体积暗底/高光/渐变。
动作与表达唯一图2原PV1050，图1已正确的圆睁高开度单charcoal眼与小白点、浅波浪闭口、暖桃肤、头肩角度、高画右小角形thumb-index闭环/两近竖长指/斜外指与另一胸前垂分指手/腕袖/交叉黑前臂全部保留，不能改半睑/图3中性口或别帧手。图3只灰短圆润bob身份和整头肩卷体量，不给当前动作/固定垂轴。保黑高领长袖、redbow金扣、白maidcap两黑主叶和正常短共同基部、白肩褶竖带/两袖口/腰围裙/后bow/原底裁，不补隐藏腿鞋。整张一次统一头颈领肩、低珠宽卷与手衣，无局部贴片，真实透明RGBA，只当前可见人物，无粉底/字幕/棋盘/色卡。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-53', 'run': str(run), 'refs': [str(f) for f in refs],
     'reference_sha256': [sha(f) for f in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'source_frame': 1050, 'first_case_frames': [1047, 1052],
     'repair_of_image_sha256': sha(refs[0]), 'local_repair_parent': None,
     'prior_fresh_Sol_rejection': str(base / 'review/sol_xhigh_round148.json'),
     'reason': 'Root and Sol148 confirm excessive added gray lower return/C from forearm to waist; preserve corrected root/source aperture/hands and reconstruct coherent shoulder/chest-scale volume.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'locally_repaired': False, 'new_edit_is_not_a_splice': True,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
f = run / 'request_imggen.json'
f.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(f), 'sha256': sha(f), 'calls': 0}, ensure_ascii=False))
