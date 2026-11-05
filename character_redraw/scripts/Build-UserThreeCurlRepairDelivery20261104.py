"""Package exact reviewed replacements and a before/after review contact."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
assets = read(base / 'ASSET_REGISTRY.json')
parser = argparse.ArgumentParser(__doc__)
parser.add_argument('--baseline-round-arc', action='store_true', help='Package the new reference-matched arc in a separate v02 delivery; preserve v01.')
args = parser.parse_args()
items = [
    ('ART-G33-48', 'direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16', 'whole_imggen_lower_root_own_shoulder_front_v01', '低根双珠，钻发移到肩前', (.30, .035, .79, .45)),
    ('ART-X01-14', 'direct_first_api_source4078_noThreeView_flatBob_totalTurnBudget_postPassEye_v16', 'py_post_pass_user_round_ribbon_smaller_light_cap_v02', '去多余圈、弧形卷带、缩小浅灰眼区', (.23, .025, .79, .43)),
    ('ART-G13-28', 'direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12', 'py_post_pass_correct_left_whole_two_gray_v01', '整束换到画面右侧，本人左肩前', (.10, .025, .77, .76))
]
if args.baseline_round_arc:
    ident, before, after, caption, roi = items[1]
    items[1] = (ident, before, 'py_post_pass_user_baseline_round_light_arc_v03', '弧形卷带，眼内浅灰恢复基线圆弧', roi)
for ident, before, after, caption, roi in items:
    selected = assets[ident]
    assert selected['status'] == 'reviewed_static_candidate'
    assert Path(selected['selected_run']).name == after
    assert sha(Path(selected['image'])) == selected['sha256']
    if ident != 'ART-G33-48':
        assert selected['secondary_eye_local_passed'] is True

dest = base / 'review/USER_THREE_ROOT_COUNT_SIDE_CORRECTIONS_20261104_v01/DELIVERY'
if args.baseline_round_arc:
    dest = dest.with_name('DELIVERY_v02_BASELINE_ROUND_ARC')
dest.mkdir(exist_ok=False)
canvas = Image.new('RGB', (1280, 1980), '#eeeeee')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 22)
small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
records = []
for index, (ident, before, after, caption, roi) in enumerate(items):
    selected = assets[ident]
    parent = base / 'drawings' / ident / 'v01'
    before_run, after_run = parent / before, parent / after
    top = index * 660
    draw.text((18, top + 10), f'图{index + 1}  {ident}  {caption}', font=font, fill='black')
    draw.text((18, top + 44), '修改前', font=small, fill='#666666')
    draw.text((658, top + 44), '修正版（静态复核，待您审阅）', font=small, fill='#333333')
    display_crops = []
    for column, run in enumerate((before_run, after_run)):
        qa = run / 'qa_white.png'
        im = Image.open(qa).convert('RGB')
        crop = tuple(round(v * (im.width if i % 2 == 0 else im.height)) for i, v in enumerate(roi))
        preview = ImageOps.contain(im.crop(crop), (612, 568), Image.Resampling.LANCZOS)
        canvas.paste(preview, (column * 640 + (640 - preview.width) // 2, top + 78 + (568 - preview.height) // 2))
        display_crops.append({'input': ev(qa), 'crop_xyxy': list(crop), 'presentation_only_resize': True})
    files = []
    for src, name in [(Path(selected['image']), f'IMAGE{index + 1}_{ident}_transparent.png'), (after_run / 'qa_white.png', f'IMAGE{index + 1}_{ident}_white.png'), (after_run / 'qa_black.png', f'IMAGE{index + 1}_{ident}_black.png')]:
        target = dest / name
        shutil.copy2(src, target)
        assert sha(target) == sha(src)
        files.append(ev(target))
    records.append({'id': ident, 'correction': caption,
        'rejected_original': ev(before_run / 'character_api_original.png'),
        'selected_replacement': ev(Path(selected['image'])), 'selected_run': selected['selected_run'],
        'primary_review': ev(Path(selected['primary_review'])), 'independent_review': ev(Path(selected['independent_review'])),
        'inherited_parent_art_review': selected.get('inherited_parent_art_review'),
        'eye_status': selected.get('secondary_eye_local_status'), 'presentation_crops': display_crops,
        'files': files, 'user_accepted': False, 'dynamic_validated': False})
contact = dest / 'THREE_CURL_REPAIRS_BEFORE_AFTER.png'
canvas.save(contact)
manifest = {'recorded_utc': datetime.now(timezone.utc).isoformat(), 'entries': records, 'contact': ev(contact),
    'provider': 'built-in imagegen for 3 structural whole repairs; Python for applicable iris RGB/cap only',
    'user_artistic_acceptance': False, 'actual_dynamic_playback_validated': False, 'goal_complete': False,
    'originals_and_all_rejected_returns_preserved': True, 'contact_is_review_layout_not_production_art': True}
(dest / 'DELIVERY.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'delivery': ev(dest / 'DELIVERY.json'), 'contact': ev(contact)}, ensure_ascii=False))
