"""Read-only comparison of current bound drawings around the F1058 hair bounce."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
p = argparse.ArgumentParser(__doc__)
p.add_argument('--output-dir', type=Path, default=root / 'art/20261102_dance_curl_updown_current_v02')
p.add_argument('--source-dir', type=Path, default=root / 'art/20261102_first_dance_66states_review_v01')
a = p.parse_args()
out = a.output_dir.resolve()
assert not out.exists(), 'Preserve previous previews.'
out.mkdir()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bindings = read(base / 'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json')
registry = read(base / 'ASSET_REGISTRY.json')
cases = [(1054, '上一稿'), (1058, '开始上扬'), (1066, '向外抬起'),
         (1070, '回落稿'), (1071, '下一稿')]
font = lambda n: ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', n)
cw, header = 500, 116
sheet = Image.new('RGB', (5*cw, 1450), 'white')
draw = ImageDraw.Draw(sheet)
draw.text((20, 10), '钻发上下摆动：当前绘制稿与原 PV', font=font(40), fill='#161616')
draw.text((20, 65), '从左向右按曝光顺序；上：原 PV，中：当前人物定位，下：钻发近图。原件未修改。', font=font(24), fill='#555555')
records = []
for i, (frame, phase) in enumerate(cases):
    row = next(r for r in bindings['frames'] if r['source_frame'] == frame)
    binding = row['actual_selected_asset_binding']
    asset = registry[binding['id']]
    layer = Path(binding['layer_1080'])
    raw = Path(asset['image'])
    assert sha(layer) == binding['layer_sha256']
    assert sha(raw) == asset['sha256'] == binding['master_sha256']
    source = base / 'coverage/source_frames' / f'F{frame:06d}.png'
    original = Image.open(source).convert('RGB')
    character = Image.open(layer).convert('RGBA')
    pink = Image.new('RGBA', (1920, 1080), (212, 168, 168, 255))
    pink.alpha_composite(character)
    x = i*cw
    draw.text((x+14, header), f'F{frame} · {phase}', font=font(29), fill='#202020')
    draw.text((x+14, header+44), binding['id'], font=font(22), fill='#555555')
    # All columns use identical camera crops and display scales. No per-part alignment.
    for image, y in ((original, 200), (pink, 615)):
        crop = image.crop((350, 70, 1370, 870)).resize((484, 380), Image.Resampling.LANCZOS)
        sheet.paste(crop.convert('RGB'), (x+8, y))
    detail = pink.crop((740, 230, 1320, 744)).resize((484, 429), Image.Resampling.LANCZOS)
    sheet.paste(detail.convert('RGB'), (x+8, 1010))
    draw.line((x, 190, x, 1440), fill='#cccccc', width=2)
    records.append({'frame': frame, 'id': binding['id'], 'phase_label_for_display': phase,
        'source': str(source), 'source_sha256': sha(source),
        'raw': str(raw), 'raw_sha256': sha(raw), 'layer': str(layer), 'layer_sha256': sha(layer),
        'uniform_camera_crop_xyxy': [350,70,1370,870], 'detail_crop_xyxy': [740,230,1320,744]})
sheet.save(out / 'curl_updown_original_current_detail.png')
sheet.resize((1920,1114), Image.Resampling.LANCZOS).save(out / 'curl_updown_preview.jpg', quality=95)
source_dir = a.source_dir.resolve()
delivery_manifest = source_dir / 'DELIVERY_RECEIPT.json'
assert delivery_manifest.is_file(), 'A reviewed render package manifest is required.'
package = read(delivery_manifest)
package_art = {r['id']: r for r in package['artworks']}
for r in records:
    assert package_art[r['id']]['raw_sha256'] == r['raw_sha256'], 'Video package contains older artwork.'
    packaged = package_art[r['id']]
    packaged_layer = source_dir / packaged['layer']
    assert sha(packaged_layer) == packaged['layer_sha256'], 'Packaged layer bytes changed.'
    # The renderer clears hidden RGB under alpha=0. Check identical alpha and
    # visible pixels over all production QA backgrounds, not hidden RGB bytes.
    with Image.open(packaged_layer) as packed, Image.open(r['layer']) as bound:
        assert packed.size == bound.size == (1920, 1080)
        packed_rgba, bound_rgba = packed.convert('RGBA'), bound.convert('RGBA')
        assert packed_rgba.getchannel('A').tobytes() == bound_rgba.getchannel('A').tobytes(), 'Video package has older alpha.'
        for color in ((255, 255, 255, 255), (0, 0, 0, 255), (212, 168, 168, 255)):
            packed_bg = Image.new('RGBA', packed.size, color)
            bound_bg = Image.new('RGBA', bound.size, color)
            packed_bg.alpha_composite(packed_rgba)
            bound_bg.alpha_composite(bound_rgba)
            assert packed_bg.tobytes() == bound_bg.tobytes(), 'Video package contains older visible placement pixels.'
package_videos = {r['path']: r for r in package['videos']}
for name in ('01_original_F0834-F1133.mp4', '02_character_1080p_original_speed.mp4'):
    assert sha(source_dir / name) == package_videos[name]['sha256'], 'Video package bytes changed.'
ffmpeg = Path('D:/CODEX/GPT-SoVITS-v2pro-20250604-nvidia50/GPT-SoVITS-v2pro-20250604-nvidia50/runtime/ffmpeg.exe')
video = out / 'F1053-F1074_original_vs_current_quarter_speed.mp4'
filters = ('[0:v]trim=start_frame=219:end_frame=241,setpts=4*(PTS-STARTPTS),scale=960:540[a];'
           '[1:v]trim=start_frame=219:end_frame=241,setpts=4*(PTS-STARTPTS),scale=960:540[b];'
           '[a][b]hstack=inputs=2[v]')
cmd = [str(ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin', '-n',
       '-i', str(source_dir/'01_original_F0834-F1133.mp4'),
       '-i', str(source_dir/'02_character_1080p_original_speed.mp4'),
       '-filter_complex', filters, '-map', '[v]', '-an', '-c:v', 'mpeg4', '-q:v', '2',
       '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', str(video)]
result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out/'ENCODE.log').write_bytes(result.stdout+result.stderr)
assert result.returncode == 0, result.stderr.decode(errors='replace')
manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': 'User requested current last up/down hair drawings; read-only presentation.',
    'input_video_package_receipt': str(delivery_manifest),
    'input_video_package_receipt_sha256': sha(delivery_manifest),
    'records': records, 'generation_calls': 0, 'artwork_modified': False,
    'registry_or_exposure_binding_modified': False,
    'video': str(video), 'video_sha256': sha(video),
    'video_rule': 'Left original PV, right current bound people; F1053-1074, quarter-speed silent CFR30 review copy. Exact production PTS remain in main package.',
    'actual_continuous_visual_playback_review': False, 'user_accepted': False,
    'command': cmd}
(out/'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'sheet': str(out/'curl_updown_original_current_detail.png'),
                  'video': str(video), 'records': len(records), 'generation_calls': 0}, ensure_ascii=False))
