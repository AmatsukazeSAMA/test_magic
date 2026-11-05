"""Two source-faithful hair-color previews; no production selection or art patching."""
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json, hashlib

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
palette = base / 'review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v01/inputs/user_attachment_04_GRAY_MINT_PALETTE_ONLY_NOT_HAIRSTYLE.png'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
jobs = [('ART-G27-01', 'api_user_fast_loose_recolor_original_face_clothes_v03', '1024x1536'),
        ('ART-G26-04', 'api_user_fast_loose_recolor_original_face_clothes_v02', '1536x1024')]
for ident, name, size in jobs:
    run = base / 'drawings' / ident / 'v01' / name
    run.mkdir(parents=True, exist_ok=True)
    assert not (run / 'DIRECT_REQUEST.json').exists(), 'Preserve previous prepared previews.'
    inputs = run / 'inputs'
    inputs.mkdir(exist_ok=True)
    # Read-only palette crops exclude face, eyes, clothes and hairstyle outline.
    palette_crop = inputs / 'GRAY_MINT_MATERIAL_COLORS_ONLY.png'
    Image.open(palette).crop((243, 130, 316, 230)).save(palette_crop)
    own = base / 'drawings' / ident / 'v01/inputs/source_pose_guide.png'
    note = ('床上坐姿，宽松灰色短袖家居上衣、同一张脸、同一双黑瞳白高光，嘴部小短线；保留短于胸口的原散发长度及肩旁的原折弯发梢，不拉长成腰发。床、白毯、原手部及遮挡保持。'
            if ident == 'ART-G27-01' else
            '原片紧贴脸部的近景，保持原圆脸轮廓、下颌宽度、下巴位置、眼型/大小/瞳孔位置/高光、嘴短线、刘海和两侧波浪散发；原图裁到哪里就保持哪里，不新增头顶或身体。原黑色文字遮挡板和衣领保持，不补遮挡后细节。')
    prompt = ('这是严格的发色编辑预览，不是重新设计人物。图1为本张原PV，是全部轮廓、线条、脸型、五官位置、神态、视线、头部角度、发型、姿势、服装、裁切和背景的唯一依据。'
              '尽最大可能逐像素保留图1，唯一修改是将原红色头发换成偏中性的浅灰，并在人物自身左侧（画面右侧）的少量原发束内部添加很细的柔和薄荷绿色挑染。'
              '图2只有一小块头发材料配色，只负责灰与薄荷色，不能借它改发型、脸或光照。'
              '灰色以一块平涂为主；原黑色发丝线、原波浪、刘海形状、每束发尾和长短完全保持，不做发光、浓渐变、3D或精修立绘。'
              '原皮肤颜色、脸轮廓和五官必须保持，绝对不要重新画成精致小脸。保留原PV粗细略不均的简笔墨线和大黑瞳白高光画法。'
              '散发不绑起，不加钻发、短bob、双红珠、头饰、女仆帽。原灰色衣服不换成白裙。'
              + note + ' 输出一张与图1同构图、同裁切、同背景的完整不透明预览，除发色外其它区域保持原样，不加新文字或标记。')
    pf = run / 'prompt_api.txt'
    pf.write_text(prompt + '\n', encoding='utf-8')
    rec = {'id': ident, 'created_utc': datetime.now(timezone.utc).isoformat(),
           'purpose': 'User requested fastest loose-hair preview before sleep; original clothes and face; no artwork selected',
           'preview_only': True, 'provider': 'OpenAI API', 'quality': 'high', 'n': 1, 'retry': 1,
           'size': size, 'background': 'opaque', 'source_hairstyle_mode': 'loose_recolor',
           'source_hairstyle_policy_id': 'source_loose_recolor_only_20261104_v02',
           'inputs': [{'path': str(p), 'sha256': sha(p)} for p in [own, palette_crop]],
           'palette_crop_provenance': {'source': str(palette), 'sha256': sha(palette), 'box': [243,130,316,230], 'read_only_reference_crop': True},
           'prompt_file': str(pf), 'prompt_sha256': sha(pf), 'user_accepted': False,
           'generation_calls_by_preparer': 0}
    (run / 'DIRECT_REQUEST.json').write_text(json.dumps(rec, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'id': ident, 'run': str(run), 'palette_crop': str(palette_crop), 'size': size}, ensure_ascii=False))
