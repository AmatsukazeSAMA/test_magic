"""Package 300 exact current bindings for review; never certify visual playback."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from PIL import Image

p = argparse.ArgumentParser(__doc__)
p.add_argument('--render-manifest', type=Path, required=True)
p.add_argument('--output-dir', type=Path, required=True)
p.add_argument('--comparison-dir', type=Path, required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
out = a.output_dir.resolve()
out.relative_to(root)
assert not out.exists(), 'Preserve earlier delivery versions.'
read = lambda f: json.loads(Path(f).read_text(encoding='utf-8-sig'))
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
manifest = read(a.render_manifest)
assert manifest['all_exposures_rendered'] and not manifest['explicit_gaps']
rows = manifest['records']
assert len(rows) == 300 and [r['frame'] for r in rows] == list(range(834, 1134))
assert manifest['clip_end_pts_exclusive'] - manifest['clip_start_pts'] == 160000
assert all(r['end_pts'] == n['pts'] for r, n in zip(rows, rows[1:]))
registry = read(base / 'ASSET_REGISTRY.json')
coverage = read(base / 'coverage/EXPOSURE_LEDGER.json')
source = Path(coverage['source_video'])
assert sha(source) == coverage['source_sha256']
ffmpeg = Path(r'D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\ffmpeg.exe')
ffprobe = ffmpeg.with_name('ffprobe.exe')
out.mkdir(parents=True)
for d in ('layers_1080p', 'raw_returns', 'original_frames', 'preview_frames', 'evidence'):
    (out / d).mkdir()

def save(f, obj):
    Path(f).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def run(cmd, name):
    save(out / 'evidence' / (name + '.command.json'), [str(c) for c in cmd])
    result = subprocess.run([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out / 'evidence' / (name + '.log')).write_bytes(result.stdout + result.stderr)
    assert result.returncode == 0, (name, result.stderr[-1200:].decode(errors='replace'))
    return result.stdout

layers, masters = {}, {}
for item in manifest['unique_rendered_layers']:
    work_id = item['id']
    selected = registry[work_id]
    assert selected['primary_static_pass'] and selected['independent_static_pass']
    assert selected['sha256'] == sha(selected['image']) == item['master_image_sha256']
    assert item['sha256'] == sha(item['path'])
    layer = out / 'layers_1080p' / (work_id + '.png')
    shutil.copyfile(item['path'], layer)
    raw = out / 'raw_returns' / (work_id + '.png')
    shutil.copyfile(selected['image'], raw)
    with Image.open(layer) as im:
        im.load()
        assert im.mode == 'RGBA' and im.size == (1920, 1080)
        bg = Image.new('RGBA', im.size, (212, 168, 168, 255))
        bg.alpha_composite(im)
        bg.convert('RGB').save(out / 'preview_frames' / (work_id + '.png'))
    layers[work_id] = layer
    masters[work_id] = {'id': work_id, 'raw': raw.relative_to(out).as_posix(),
        'raw_sha256': selected['sha256'], 'layer': layer.relative_to(out).as_posix(),
        'layer_sha256': sha(layer), 'primary_static_pass': True,
        'Sol_xhigh_static_pass': True, 'user_accepted': False}
assert len(layers) == 66
play_rows = []
for r in rows:
    assert r['image_sha256'] == sha(r['image'])
    src = base / 'coverage/source_frames' / f"F{r['frame']:06d}.png"
    target = out / 'original_frames' / src.name
    shutil.copyfile(src, target)
    play_rows.append({'frame': r['frame'], 'pts': r['pts'], 'end_pts': r['end_pts'],
        'duration_ticks': r['duration_ticks'], 'id': r['id'],
        'source': target.relative_to(out).as_posix(),
        'layer': layers[r['id']].relative_to(out).as_posix(),
        'layer_sha256': sha(layers[r['id']])})
player = {'chapter': '首段舞蹈 F834–1133 审阅版', 'time_base': '1/16000',
    'start_pts': rows[0]['pts'], 'end_pts': rows[-1]['end_pts'], 'frames': play_rows,
    'all_frames_bound': True, 'actual_continuous_visual_playback_review': False,
    'user_accepted': False, 'whole_film_complete': False}
save(out / 'PLAYBACK_MANIFEST.json', player)
template = (root / 'scripts/templates/character_pts_player.html').read_text(encoding='utf-8')
template = template.replace('这是单镜头制作审核预览。', '这是首段舞蹈审阅预览。')
embedded = json.dumps(player, ensure_ascii=False).replace('<', '\\u003c')
(out / 'index.html').write_text(template.replace('__MANIFEST_JSON__', embedded), encoding='utf-8')
concat = out / 'evidence/character.ffconcat'
lines = ['ffconcat version 1.0']
for r in rows:
    path = (out / 'preview_frames' / (r['id'] + '.png')).as_posix()
    assert "'" not in path
    lines += [f"file '{path}'", 'option framerate 16000', f"duration {r['duration_ticks']/16000:.9f}"]
lines += [f"file '{(out / 'preview_frames' / (rows[-1]['id'] + '.png')).as_posix()}'", 'option framerate 16000']
concat.write_text('\n'.join(lines) + '\n', encoding='utf-8')
start, end = rows[0]['pts'] / 16000, rows[-1]['end_pts'] / 16000
duration = end - start
common = ['-c:v', 'mpeg4', '-q:v', '2', '-bf', '0', '-pix_fmt', 'yuv420p',
          '-vsync', '0', '-enc_time_base', '1:16000', '-video_track_timescale', '16000', '-movflags', '+faststart']
original = out / '01_original_F0834-F1133.mp4'
filters = (f'[0:v]trim=start_frame=834:end_frame=1134,setpts=PTS-STARTPTS[v];'
           f'[0:a]atrim=start={start:.9f}:end={end:.9f},asetpts=PTS-STARTPTS[a]')
run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', source,
     '-filter_complex', filters, '-map', '[v]', '-map', '[a]', *common,
     '-c:a', 'aac', '-b:a', '192k', original], 'original_encode')
normal = out / '02_character_1080p_original_speed.mp4'
run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-safe', '0',
     '-f', 'concat', '-i', concat, '-ss', f'{start:.9f}', '-i', source,
     '-map', '0:v:0', '-map', '1:a:0', '-t', f'{duration:.9f}', *common,
     '-c:a', 'aac', '-b:a', '192k', normal], 'character_encode')
slow = out / '03_character_1080p_half_speed.mp4'
run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', normal,
     '-an', '-vf', 'setpts=2*(PTS-STARTPTS)', *common, slow], 'slow_encode')
videos = []
expected = [r['pts'] - rows[0]['pts'] for r in rows]
for video, scale in ((original, 1), (normal, 1), (slow, 2)):
    probe = json.loads(run([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_streams',
        '-show_frames', '-show_entries', 'frame=best_effort_timestamp:stream=width,height,time_base',
        '-of', 'json', video], video.stem + '_probe'))
    stream = probe['streams'][0]
    assert (stream['width'], stream['height'], stream['time_base']) == (1920, 1080, '1/16000')
    actual = [int(f['best_effort_timestamp']) for f in probe['frames']]
    assert len(actual) == 300, (video.name, len(actual))
    error = max(abs(x - scale*y) for x, y in zip(actual, expected))
    assert error <= 1, (video.name, error)
    videos.append({'path': video.name, 'sha256': sha(video), 'decoded_frames': 300,
        'PTS_multiplier': scale, 'max_PTS_error_ticks': error,
        'actual_continuous_visual_review': False})
comparison = a.comparison_dir.resolve()
assert read(comparison / 'LAYOUT_ACTUAL_REVIEW.json')['layout_sample_review_passed']
for name in ('dance_all_66_original_vs_current.png', 'MANIFEST.json', 'LAYOUT_ACTUAL_REVIEW.json'):
    shutil.copyfile(comparison / name, out / ('comparison_' + name))
for file in (a.render_manifest, base / 'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json'):
    shutil.copyfile(file, out / 'evidence' / file.name)
(out / '先读我.txt').write_text(
    '首段舞蹈 F834–1133，66个绘制态，300个曝光。\n'
    '01为原PV截取（原声/原字幕保留）；02为人物层原速审阅片；03为无声0.5倍慢速。\n'
    '人物审阅视频使用粉底，不含最终背景、字幕、特效或道具合成。\n'
    'layers_1080p是真透明人物层；raw_returns是保留的完整返图。\n'
    '双击index.html可按真实PTS对照原片/人物层，切换速度与底色并逐帧查看。\n'
    '静态绘制与定位已逐稿经主审及Sol xhigh检查。视频编码/PTS核对不等于实际连续播放审评；后者仍待完成。用户艺术验收另记，GOAL未完成。\n', encoding='utf-8')
receipt = {'created_utc': datetime.now(timezone.utc).isoformat(), 'source_sha256': sha(source),
    'source_frame_range': [834, 1133], 'time_base': '1/16000', 'exposures': 300,
    'unique_artworks': 66, 'artworks': list(masters.values()), 'videos': videos,
    'render_manifest_sha256': sha(a.render_manifest), 'all_bindings_current': True,
    'actual_continuous_playback_validated': False, 'user_accepted': False, 'goal_complete': False}
save(out / 'DELIVERY_RECEIPT.json', receipt)
archive = out.with_suffix('.zip')
assert not archive.exists()
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path in sorted(out.rglob('*')):
        if path.is_file():
            z.write(path, path.relative_to(out))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size,
    'sha256': sha(archive), 'videos': videos, 'actual_playback_review': False}, ensure_ascii=False))
