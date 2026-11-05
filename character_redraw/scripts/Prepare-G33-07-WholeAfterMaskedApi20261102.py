"""Prepare one coherent redraw of the known masked intermediate; no image edits/calls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G33-07/v01/local_upper_connected_gray_envelope_api_v02'
run = parent.parent / 'whole_imggen_after_upper_gray_mask_preserve_volume_v15'
assert not run.exists(), 'Preserve existing preparation or results.'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
api = read(parent / 'result.json')
target = parent / 'character_api_original.png'
assert sha(target) == api['output_sha256'] == '71c3786030b315642e098fa08d405cd475e5c5714d16e768459d35a2ec84a4b6'
refs = [target,
        parent / 'inputs/ref4_ORIGINAL2333_COMPLETE_UNMASKED_ACTION_GUIDE.png',
        parent / 'inputs/ref2_LATEST_USER_BROAD_GRAY_INNER_RETURN_DETAIL.png',
        parent / 'inputs/ref3_UNLIT_GRAY_MINT_INK_MATERIAL_KEY.png']
prefix = read(root / 'image_defaults.json')['generation_prompt_prefix']['text']
prompt = prefix + '''

对图1的完整当前人物进行一次连贯的整张重绘，真正透明背景。图1是已经过API局修的中间稿，不能继续贴片；整体统一灰短bob、低耳后红珠、螺旋发带、头颈、黑立领、白肩frill与衣身的线条连接。
保持图1现有头部大小和卷发相对于整个头的体量、低根、向画右外甩的轴线及末端C回钩位置。卷不能再次长到接近bob宽，不能竖直掉回肩上，不镜像。保留当前宽灰前面折入不透明灰内/背返回、再进入下一圈的连续发带；图3只解释此构造，不复制打光、衣服或竖直轴线。不要封成椭圆盖盘或实体锥柱，也不把真实灰返回挖成透明孔；只真实露空透明。
唯一必要材料校正：图4所有灰发面都用同一种无打光灰，卷的内/背返回和C内弧也与bob同灰。以细黑轮廓及遮挡区分返回，不保留图1卷里的深灰三角暗面、亮条或银色渐变。薄荷色只柔和细材料带。白cap保持两片主要黑叶同根。
图2原PV2333是动作、表情与可见裁切依据：圆睁但不对称的眼、极小中性闭口，一臂折腰后、另一臂斜跨身落向画左低掌，源指形、袖口接触、红bow金扣、黑白长袖衣、腰带后bow、长apron锯齿边、黑裙、屈膝后抬腿及前腿交错均保留。单色charcoal眼，无独立更黑圆芯/浅灰环，普通小白点即可。暖桃肤。前鞋尖在原画底边被裁，不为了露全鞋缩人或加源外脚尖；后续半身摄影另按真实曝光定位。
输出完整当前可见人物，不输出粉底、字幕、色表、背景、道具、局部贴片或拼接接缝。不用图2原红双高卷，也不复制图3制服或其光泽。'''
run.mkdir()
(run / 'prompt_imggen.txt').write_text(prompt, encoding='utf-8')
status = parent / 'LOCAL_REPAIR_STATUS.json'
(run / 'LOCAL_PARENT_BEFORE_WHOLE.json').write_bytes(status.read_bytes())
q = dict(id='ART-G33-07', run=str(run), operation_kind='whole_character_redraw',
         refs=[str(p) for p in refs], reference_sha256=[sha(p) for p in refs],
         prompt=prompt, transparent_background=True, local_repair_parent=str(parent),
         mandatory_whole_redraw_after_local_repair=True, source_canonical_frame=2333,
         source_pts=1245520, first_case_frames=[861, 862], PREPONLY=True,
         user_quality_preference='high', native_quality_parameter_exposed=False,
         native_model_parameter_exposed=False, native_calls=0, api_calls=0,
         automatic_retries=0, submitted=False, fresh_root_Sol_and_photography_required=True,
         known_local_result_sha256=sha(target), local_parent_before_sha256=sha(status),
         created_utc=datetime.now(timezone.utc).isoformat(), user_accepted=False,
         root_actual_input_observation='Exact returned API whole white/black and exact source2333, latest user broad-gray detail and unlit key viewed. API kept suitable outward moderate volume but inner returns still darker than bob; only material unification requested during mandatory whole. Source crop retained, no new hidden toes.')
(run / 'request_imggen.json').write_text(json.dumps(q, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'request':str(run/'request_imggen.json'),'sha256':sha(run/'request_imggen.json'),'generation_calls':0}, ensure_ascii=False))
