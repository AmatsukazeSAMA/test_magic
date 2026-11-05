"""Change reference hypothesis after the whole edit copied the old head tilt."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
parent = base / 'drawings/ART-G12-56/v01'
local = parent / 'mask_prep_source1066_headpose_aperture_v03'
run = parent / 'whole_imggen_upright_localpose_identity11_no_oldtilt_v05'
if (run / 'request_imggen.json').exists():
    raise SystemExit('Existing request preserved; no automatic repeat.')
run.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
refs = [local / 'character_api_original.png',
        base / 'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
        parent / 'inputs/source_pose_guide.png',
        base / 'drawings/ART-G12-53/v01/draft_first_api_unmasked_source53_user11_graydetail_v01/inputs/ref4_LATEST_USER_BROAD_GRAY_THIN_MINT_DETAIL_NO_ROOT_FACE.png',
        base / 'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png']
assert sha(refs[0]) == 'afe5487fff47da45a8ec96cb59077c09ae80f24c075c0f5fbdc9e0853052409d'
prefix = json.loads((root / 'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt = prefix + '\n\n' + '''保持参考1人物当前脸部/头颈相对衣领与腰带的较直立姿态、两眼开度、小波闭口、两手和衣身动作，只将整个发型重画成参考2这位短灰bob人物的身份，并对整个可见人物连贯重绘统一连接。
当前画面不是大幅歪头。参考1脸的头身姿态与参考3原1066吻合，必须保留；不要把头朝左下重新压歪。当前原1066自己的弧形睁眼与视线照参考1/3，左眼不压成半睑，不复制参考2的眼口。单charcoal平填瞳、普通白点，无独立黑圆心灰环。身体/手臂/黑领/腰带均不旋转。
参考1的长尖刘海和画面左上巨大高钻卷、灰珠与三黑尖帽饰是错误的原角色发型，全部替换。改为参考2的圆润耳际短灰bob和两片黑主叶白maidcap。只有一组红双珠和一束宽灰罗马卷，低根在本朝右近正面人物的远侧LEFT耳后/下颌后/颈侧，即画面右边；bob可自然遮部分低根，不复制参考1画左高根，不抬到眼高。
本1066承接1058开始上扬的惯性，卷从远侧正确低根向外/上翻，露出的卷在bob下侧向右翻起，而非从珠下竖挂或缩成迷你挂件。体量按参考2完整头/卷比例，不照细节图放大；不穿原白肩褶和胸前手。参考4只给连续宽灰发带前面翻回内/后返回面再接下一圈、渐收C的结构，不复制打光，不成封口盘堆/实心柱，不挖掉不透明灰返回面，实际露空才透明。参考5只给bob与卷同一平涂灰和细薄荷材料带，无独立亮边/暗内腔/渐变。
原1066高举手角形OK及另外三指弯伸、另一胸前横张分指、腕袖接触与前臂交叠均严格保留参考1/3。暖桃肤、黑高领长袖、红胸结金扣、白肩褶/袖口/围裙/腰带后结与裙底裁切不变，不补裁切外腿鞋。一次完整连贯重画头发珠卷颈领肩手衣，修掉局修接缝。高质量真实透明RGBA，无背景字幕色卡棋盘格。'''
(run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
q = {'id': 'ART-G12-56', 'run': str(run), 'refs': [str(p) for p in refs],
     'reference_sha256': [sha(p) for p in refs], 'prompt': prompt,
     'operation_kind': 'whole_character_redraw', 'transparent_background': True,
     'local_repair_parent': str(local), 'source_frame': 1066, 'first_case_frames': [1062,1066],
     'changed_hypothesis': 'No old tilted55/56 artwork supplied. Exact upright local head/body target first; upright correct11 full-head context supplies short-gray-bob identity only.',
     'native_calls_authorized': 1, 'api_calls': 0, 'automatic_retries': 0,
     'user_quality_preference': 'high', 'native_quality_parameter_exposed': False,
     'fresh_root_Sol_and_placement_review_required': True,
     'created_utc': datetime.now(timezone.utc).isoformat(), 'submitted': False}
request = run / 'request_imggen.json'
request.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'request': str(request), 'sha256': sha(request), 'calls': 0}, ensure_ascii=False))
