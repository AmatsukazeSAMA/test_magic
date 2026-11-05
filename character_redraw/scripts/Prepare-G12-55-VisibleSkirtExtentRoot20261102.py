"""Prepare one whole redraw extending only original-visible lower garment coverage."""
from pathlib import Path
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
family = base / 'drawings/ART-G12-55/v01'
prior = family / 'whole_imggen_v08_complete_left_edges_widecanvas_v09'
old = json.loads((prior / 'request_imggen_ROOT_AUTHORIZED.json').read_text(encoding='utf-8'))
run = family / 'whole_imggen_extend_original_visible_skirt_v10_ROOT'
assert not run.exists()
(run / 'inputs').mkdir(parents=True)
source = base / 'coverage/source_frames/F001058.png'
crop = run / 'inputs/ORIGINAL1058_VISIBLE_WAIST_APRON_SKIRT_ONLY.png'
with Image.open(source) as im:
    im.crop((600, 735, 1020, 1080)).save(crop)
refs = [str(prior / 'character_imggen_original.png'), str(crop), old['refs'][4]]
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '''

以图1为目标，整张连贯重绘透明人物，保住已修正的头、脸、眼口、双手、腰与卷发。现在图1下裙画得不够长，按原片大小定位会在画内露出横向断边。本次只增加原片已经可见的下裙范围：新画布宽高严格约3:5（例如1060×1768），向下扩展画面，保持眼线、下颌、衣领、高手OK接点与另三指、胸前低手、交叉袖、腰带之间现有相对比例；整个上半身可同倍率整体适配和统一平移，不得拉长上躯干、抬腰、改手势或放大全人来遮住缺口。

图2只是原1058的腰和画面底部可见的黑裙、白围裙参考，腰带下方继续同一黑裙与白围裙，到新画布底部。腰带下缘至画布底缘的可见裙段，应约为眼线至腰带距离的0.8倍，保留原透视和自然衣褶，让后续原大小定位有足够覆盖。不要画完整裙摆底边、腿或鞋，不补原片外的隐藏人体；不要复制图2粉背景或文字。左侧后结和裙外轮廓自然延续，不出现画内直切口或拼接。

图1完整灰bob、白女仆帽及两片主黑叶必须全在画布内，左、右、顶部保留透明边距。保持人物自身LEFT远侧低耳后双红珠，画右的中等卷量略向外上摆；宽灰发带正面连续翻回不透明同灰返回，接下一转并渐细为同一灰C，不能变成灰囊、封口盘、实心锥或独立绿环。图3只定无打光灰色，bob和全部卷正面/返回/C同灰平涂，薄荷只窄边，无高光渐变。暖桃肤色、半眯单色charcoal眼、小w闭嘴、黑白女仆服红结金扣保持。整个人重新连画，真实透明背景和空气，不画字幕、色卡或道具。
'''
q = {'id': 'ART-G12-55', 'run': str(run), 'PREPONLY': True,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'refs': refs, 'reference_sha256': [sha(f) for f in refs], 'prompt': prompt,
     'local_repair_parent': old['local_repair_parent'], 'source_frame': 1058,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'native_calls_authorized': 0, 'automatic_retries': 0,
     'changed_hypothesis': 'Keep repaired upper pose and curl; taller 3:5 whole redraw supplies original-visible skirt coverage instead of enlarging the entire cel.',
     'reference_crop_provenance': {'source': str(source), 'sha256': sha(source),
                                   'crop_xyxy': [600, 735, 1020, 1080],
                                   'readonly_original_pixel_rectangle': True},
     'fresh_root_Sol_and_photography_required': True, 'user_accepted': False}
(run / 'prompt_imggen.txt').write_text(prompt, encoding='utf-8')
out = run / 'request_imggen.json'
out.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(out), 'sha256': sha(out), 'refs': refs,
                  'native_calls': 0}, ensure_ascii=False))
