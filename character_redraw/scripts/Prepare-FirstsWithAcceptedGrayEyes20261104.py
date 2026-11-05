from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

r = Path(__file__).resolve().parent.parent
b = r / 'art/full_character_redraw_1080p_v01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p), 'sha256': sha(p)}
for i, oldname, newname in [
    ('ART-G06-04', 'direct_first_api_source459_samegray_return_material_factor_v04', 'direct_first_api_source459_grayeye_palette_samegray_v05'),
    ('ART-G07-05', 'direct_first_api_source510_samegray_return_material_factor_v04', 'direct_first_api_source510_grayeye_palette_samegray_v05')]:
    old = b / 'drawings' / i / 'v01' / oldname
    new = old.parent / newname
    new.mkdir(exist_ok=False)
    q = json.loads((old / 'DIRECT_REQUEST.json').read_text(encoding='utf-8-sig'))
    text = (old / 'prompt_api.txt').read_text(encoding='utf-8-sig').replace('iris单一均匀charcoal+普通小白点', '眼黑采用最新认可深灰主体+内下较浅灰色块，原白glint位置/形状不变，无中心小黑点')
    palette = b / 'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/EYE_GRAY_PALETTE_ONLY_NO_SHAPE.png'
    if i == 'ART-G07-05':
        q['parameters']['InputImages'].append(str(palette))
        text += '\n图4仅一条眼黑内部两种灰色调色样本，不含眼型。只参考这两灰配色，不能搬其它参考眼型或纯黑。保持本倒悬原眼黑弧边、原glint位置与颌耳方向；浅灰色块随眼睛倒置，不新增黑瞳小点。\n'
    else:
        text += '\n本张为闭眼，最新灰眼要求在本张没有可见眼黑可应用；必须保原闭弧短睫，不睁眼或新增虹膜。\n'
    pf = new / 'prompt_api.txt'
    pf.write_text(text, encoding='utf-8')
    q['parameters']['PromptFile'] = str(pf)
    q['parameters']['OutputDirectory'] = str(new)
    q['parameters']['Stage'] += '__LATEST_GRAY_EYE_COLOR_ONLY'
    q['refs'] = [ev(Path(x)) for x in q['parameters']['InputImages']]
    q['prompt'] = ev(pf)
    q['provider'] = ev(r / 'scripts/Invoke-ReferenceImage.ps1')
    q['source_eye_color_policy'] = ev(b / 'review/USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01/POLICY.json')
    q['root_actual_input_review'] = {
        'at': datetime.now(timezone.utc).isoformat(), 'all_inputs_viewed': True,
        'own_pose': 'F459 upside-down closed arcs / exposed toes, spread front hand and far grip, source tray occlusion' if i == 'ART-G06-04' else 'F510 upside-down independent half-open eyelids and clipped upper iris/white glints, loose gray sleeve and gripping hand, no mouth behind tray',
        'prior_prep_preserved': str(old)}
    (new / 'DIRECT_REQUEST.json').write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(str(new))
