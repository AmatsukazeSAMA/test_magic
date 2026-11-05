from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import sys
from PIL import Image

project = Path(__file__).resolve().parents[4]
base = project / 'art/full_character_redraw_1080p_v01'
asset_id = sys.argv[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
write = lambda p, value: Path(p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
registry_file = base / 'ASSET_REGISTRY.json'
bindings_file = base / 'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json'
asset = read(registry_file)[asset_id]
raw = Path(asset['image'])
assert sha(raw) == asset['sha256']
bindings = [r for r in read(bindings_file)['frames'] if r.get('actual_selected_asset_binding', {}).get('id') == asset_id]
assert bindings
binding = bindings[0]['actual_selected_asset_binding']
assert all(r['actual_selected_asset_binding']['master_sha256'] == asset['sha256'] for r in bindings)
assert all((r['actual_selected_asset_binding']['scale'], r['actual_selected_asset_binding']['translation']) == (binding['scale'], binding['translation']) for r in bindings)
assert sha(binding['layer_1080']) == binding['layer_sha256']
image = Image.open(raw)
assert image.mode == 'RGBA'
scale = binding['scale']
tx, ty = binding['translation']
viewport_bottom_raw = (1080 - ty) / scale
crop_bottom = min(image.height, math.ceil(viewport_bottom_raw + 60))
xyxy = [0, 0, image.width, crop_bottom]
crop = image.crop(xyxy)
run = base / 'drawings' / asset_id / 'v01/whole_imggen_HD_preserve_handdrawn_lines_v01'
assert not run.exists(), f'Existing preparation preserved: {run}'
(run / 'inputs').mkdir(parents=True)
ref = run / 'inputs' / f'ref1_CURRENT_{asset["sha256"][:12]}_RGBA_VISIBLE_EXTENT_PLUS60px.png'
crop.save(ref)
assert Image.open(ref).tobytes() == image.crop(xyxy).tobytes()
prefix = read(project / 'image_defaults.json')['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + (
    '高清化需要保留线条风格。以唯一参考图为当前人物、动作、构图与线条的全部依据，'
    '将整个当前可见人物一次连贯重绘成高像素密度透明人物图，保持参考图的宽高比例，尽量长边约2048像素。'
    '保留原手书墨线的粗细起伏、不规则轮廓、简笔形状和相对线宽，不做向量化、平滑精修，不新增发丝、阴影或高光。'
    '动作、表情、眼开度、视线、肤色、服装、双手手指接触、帽子及两片主要黑叶均原样保留。'
    '人物LEFT低耳后双红珠根位、钻发轨迹、相对整头体量和原遮挡原样保留；'
    '宽灰前面连到不透明灰返回面、下一圈及渐细C的路径不改，薄mint边保持原分区，灰与bob同样无打光平涂。'
    '完整保留当前头帽和全部手指，四周透明边距保持。底部沿当前裁切，只画参考中可见的衣裙，不补隐藏腿鞋。'
    '背景和现有空气缝是真透明；透明像素的隐藏RGB不是背景或发面。'
)
prompt_file = run / 'prompt_imggen.txt'
prompt_file.write_text(prompt, encoding='utf-8')
transform = {
    'id': asset_id, 'prepared_utc': datetime.now(timezone.utc).isoformat(),
    'source_raw': str(raw), 'source_raw_sha256': asset['sha256'], 'source_size': list(image.size),
    'crop_xyxy_original_raw_coordinates': xyxy, 'crop_size': list(crop.size),
    'crop_sha256': sha(ref), 'crop_operation': 'Rectangle only; original RGBA pixels retained byte-for-byte within rectangle. No painting, alpha cutout, resampling or part transform.',
    'screen_viewport_bottom_y': 1080, 'screen_bottom_in_raw_y': viewport_bottom_raw,
    'raw_pixel_bottom_guard_requested': 60, 'raw_pixel_bottom_guard_actual': crop_bottom - viewport_bottom_raw,
    'original_alpha_bbox': list(image.getbbox()) if image.getbbox() else None,
    'cropped_alpha_bbox': list(crop.getbbox()) if crop.getbbox() else None,
    'source_registry_path': str(registry_file), 'source_registry_sha256_at_prepare': sha(registry_file),
    'exposure_bindings_path': str(bindings_file), 'exposure_bindings_sha256_at_prepare': sha(bindings_file),
    'source_frames': [r['source_frame'] for r in bindings], 'binding': binding,
    'registration_proposal_sha256': sha(binding['registration_proposal']),
    'crop_to_1920x1080_uniform_transform': {'scale': scale, 'translation': [tx + scale * xyxy[0], ty + scale * xyxy[1]]},
    'formula': 'canvas_x = scale * crop_x + tx; canvas_y = scale * crop_y + ty; crop origin is (0,0).',
    'future_HD_registration': 'Fresh uniform fit and actual root/independent photography review required. Native output dimensions and pixel correspondence are not guaranteed.',
    'art_pixels_changed': False, 'central_files_changed': False,
}
write(run / 'PARENT_CROP_TRANSFORM.json', transform)
request = {
    'id': asset_id, 'run': str(run), 'operation_kind': 'whole_character_redraw',
    'PREPONLY': True, 'dispatchable': False, 'root_release_received': False,
    'transparent_background': True, 'refs': [str(ref)], 'reference_sha256': [sha(ref)],
    'reference_roles': ['Only pose, identity, proportions, handdrawn lines, colors, curl geometry/mass/occlusion and visible extent reference; current RGBA rectangle, not a screenshot.'],
    'prompt': prompt, 'prompt_file': str(prompt_file), 'prompt_sha256': sha(prompt_file),
    'tool_arguments': {'prompt': prompt, 'referenced_image_paths': [str(ref)], 'transparent_background': True},
    'native_calls_authorized': 0, 'planned_native_calls_after_root_release': 1,
    'native_calls': 0, 'API_calls': 0, 'HTTP_calls': 0, 'automatic_retries': 0,
    'user_requirement_verbatim': '高清化需要保留线条风格',
    'preferred_long_edge_px': 2048, 'native_size_parameter_exposed': False, 'native_quality_parameter_exposed': False,
    'source_crop_transform': str(run / 'PARENT_CROP_TRANSFORM.json'), 'source_raw_sha256': asset['sha256'],
    'fresh_primary_independent_and_uniform_registration_required': True,
    'user_accepted': False, 'dynamic_validated': False,
}
q = run / 'request_imggen.json'
write(q, request)
print(json.dumps({'id': asset_id, 'q': str(q), 'q_sha256': sha(q), 'prompt_sha256': sha(prompt_file), 'ref': str(ref), 'ref_sha256': sha(ref), 'crop_xyxy': xyxy, 'crop_size': list(crop.size), 'transform_sha256': sha(run/'PARENT_CROP_TRANSFORM.json'), 'calls': 0}, ensure_ascii=False, indent=2))
