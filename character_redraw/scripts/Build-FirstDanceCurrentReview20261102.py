"""Package 300 exact current bindings for review; never certify visual playback."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
from fractions import Fraction
import struct
import shutil
import subprocess
import zipfile
from PIL import Image


TIME_BASE = '1/16000'
CLIP_START, CLIP_END = 445248, 605248


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def binding_evidence_sha256(binding, asset):
    """Must match Render-DanceCurrentBindings' render-time evidence fields."""
    return {
        'binding': hashlib.sha256(json.dumps(binding, ensure_ascii=False, sort_keys=True,
                                            separators=(',', ':')).encode('utf-8')).hexdigest(),
        'master_image': file_sha(asset['image']),
        'selected_layer': file_sha(binding['layer_1080']),
        'registration_proposal': file_sha(binding['registration_proposal']),
        'root_placement_review': file_sha(binding['root_placement_review']),
        'independent_placement_review': file_sha(binding['independent_placement_review']),
        'master_primary_review': file_sha(asset['primary_review']),
        'master_independent_review': file_sha(asset['independent_review']),
    }


def validate_timing(manifest, bindings, coverage):
    """Production admission: never accept a partial timeline or inferred last hold."""
    assert manifest['all_exposures_rendered'] and not manifest['explicit_gaps']
    assert manifest['source_time_base'] == bindings['source_time_base'] == coverage['time_base'] == TIME_BASE
    assert manifest['clip_start_pts'] == bindings['clip_start_pts'] == CLIP_START
    assert manifest['clip_end_pts_exclusive'] == bindings['clip_end_pts_exclusive'] == CLIP_END
    rows = manifest['records']
    assert len(rows) == len(bindings['frames']) == 300
    assert [r['frame'] for r in rows] == [r['source_frame'] for r in bindings['frames']] == list(range(834, 1134))
    original = {r['frame']: r for r in coverage['frames']}
    for i, (row, bound) in enumerate(zip(rows, bindings['frames'])):
        source = original[row['frame']]
        pts, end = source['pts'], min(source['end_pts'], CLIP_END)
        assert all(type(row[key]) is int for key in ('frame', 'pts', 'end_pts', 'duration_ticks'))
        assert source['duration_ticks'] == source['end_pts'] - pts > 0
        assert (row['pts'], row['end_pts'], row['duration_ticks']) == (pts, end, end - pts)
        assert (bound['source_pts'], bound['original_end_pts'], bound['clip_end_pts'],
                bound['clip_duration_ticks'], bound['clip_relative_pts']) == (
                    pts, source['end_pts'], end, end - pts, pts - CLIP_START)
        assert end > pts and (i == 299 or end == rows[i + 1]['pts'])
    assert rows[0]['pts'] == CLIP_START and rows[-1]['frame'] == 1133
    assert (rows[-1]['pts'], rows[-1]['end_pts'], rows[-1]['duration_ticks']) == (604864, CLIP_END, 384)
    assert sum(r['duration_ticks'] for r in rows) == 160000


def validate_current_bindings(manifest, bindings, snapshot, registry, policy_index, manifest_path):
    """Compare every live selection and its review hashes with the frozen render."""
    old = {r['source_frame']: r for r in snapshot['frames']}
    live = {r['source_frame']: r for r in bindings['frames']}
    layers = {r['id']: r for r in manifest['unique_rendered_layers']}
    assert len(layers) == len(manifest['unique_rendered_layers'])
    frozen = manifest['binding_evidence_sha256']  # Legacy renders must be rendered again.
    checked, cached = [], {}
    def evidence(binding, asset):
        key = json.dumps([binding, asset], ensure_ascii=False, sort_keys=True)
        if key not in cached:
            cached[key] = binding_evidence_sha256(binding, asset)
        return cached[key]
    for row in manifest['records']:
        frame = row['frame']
        current, before = live[frame], old[frame]
        binding = current['actual_selected_asset_binding']
        assert binding and binding == before['actual_selected_asset_binding'], ('Binding changed since render', frame)
        assert current['source_ids'] == before['source_ids'] == [row['id']] == [binding['id']]
        for key in ('source_pts', 'original_end_pts', 'clip_end_pts', 'clip_duration_ticks'):
            assert current[key] == before[key], (frame, key)
        asset = registry[row['id']]
        item = layers[row['id']]
        fingerprints = evidence(binding, asset)
        assert fingerprints == frozen[str(frame)], ('Evidence changed since render', frame)
        assert asset['primary_static_pass'] and asset['independent_static_pass']
        assert binding['static_registration_review_passed']
        assert asset['sha256'] == binding['master_sha256'] == item['master_image_sha256'] == fingerprints['master_image']
        assert Path(asset['image']).resolve() == Path(binding['master_image']).resolve()
        assert Path(item['selected_layer']).resolve() == Path(binding['layer_1080']).resolve()
        assert item['selected_layer_sha256'] == binding['layer_sha256'] == fingerprints['selected_layer']
        assert Path(item['path']).resolve() == Path(row['image']).resolve()
        assert item['sha256'] == row['image_sha256'] == file_sha(row['image'])
        recorded = current['render_readback_receipt']
        assert current['actual_render_binding_verified'] and recorded['sha256'] == row['image_sha256']
        assert Path(recorded['manifest']).resolve() == Path(manifest_path).resolve()
        index = policy_index['records'][row['id']]
        assert index['sha256'] == asset['sha256']
        assert index['primary_review_sha256'] == fingerprints['master_primary_review']
        assert index['independent_review_sha256'] == fingerprints['master_independent_review']
        assert index['curl_structure_policy_id'] == manifest['curl_structure_policy_id']
        proposal = read_json(binding['registration_proposal'])
        primary = read_json(binding['root_placement_review'])
        independent = read_json(binding['independent_placement_review'])
        assert proposal['current_art_sha256'] == asset['sha256']
        assert proposal['rendered_character_layer_sha256'] == binding['layer_sha256']
        assert proposal['current_asset_to_first_scene_scale'] == binding['scale']
        assert proposal['current_asset_to_first_scene_translation'] == binding['translation']
        assert primary['primary_static_registration_pass'] and independent['static_registration_review_passed']
        assert independent['proposal_sha256'] == fingerprints['registration_proposal']
        assert independent['current_registered_candidate_sha256'] == binding['layer_sha256']
        assert binding['independent_placement_review_sha256'] == fingerprints['independent_placement_review']
        assert all(file_sha(path) == digest for path, digest in primary['viewed_sha256'].items())
        checked.append({'frame': frame, 'id': row['id'], 'render_evidence_sha256': fingerprints})
    return checked


def mp4_boxes(data):
    """Read ordinary non-fragmented MP4 boxes; reject malformed boundaries."""
    offset = 0
    while offset < len(data):
        assert offset + 8 <= len(data), 'Truncated MP4 box'
        size, kind = struct.unpack_from('>I4s', data, offset)
        header = 8
        if size == 1:
            size, header = struct.unpack_from('>Q', data, offset + 8)[0], 16
        elif size == 0:
            size = len(data) - offset
        assert size >= header and offset + size <= len(data), 'Invalid MP4 box size'
        yield kind, data[offset + header:offset + size], offset, size
        offset += size


def mp4_box(kind, payload):
    assert len(payload) + 8 < 2**32
    return struct.pack('>I4s', len(payload) + 8, kind) + payload


def exact_mp4_sample_durations(path, durations):
    """Set video stts explicitly, updating moov sizes/chunk offsets, never media bytes.

    FFmpeg's last inferred sample hold is not the clip boundary. Only supported
    here: one video track, no B frames/ctts, no fragmented MP4, and ordinary edit
    lists. Every packet/frame is probed separately after this container repair.
    """
    assert durations and all(type(d) is int and d > 0 for d in durations)
    path = Path(path)
    original = path.read_bytes()
    top = list(mp4_boxes(original))
    assert not any(kind == b'moof' for kind, *_ in top)
    movies = [b for b in top if b[0] == b'moov']
    assert len(movies) == 1
    _, moov, moov_start, moov_size = movies[0]
    def children(payload): return {k: v for k, v, *_ in mp4_boxes(payload)}
    movie_header = children(moov)[b'mvhd']
    def time_fields(payload):
        assert payload[0] in (0, 1)
        return (12, 16, 4) if payload[0] == 0 else (20, 24, 8)
    def put_integer(payload, offset, size, value):
        assert 0 <= value < 1 << (8 * size)
        changed = bytearray(payload); changed[offset:offset + size] = value.to_bytes(size, 'big')
        return bytes(changed)
    movie_scale = struct.unpack_from('>I', movie_header, time_fields(movie_header)[0])[0]
    total = sum(durations)
    movie_duration = Fraction(total * movie_scale, 16000)
    assert movie_duration.denominator == 1
    movie_duration = int(movie_duration)
    runs = []
    for duration in durations:
        if runs and runs[-1][1] == duration: runs[-1][0] += 1
        else: runs.append([1, duration])
    tracks = [payload for kind, payload, *_ in mp4_boxes(moov) if kind == b'trak']
    video_count = 0
    def track_is_video(payload):
        return children(children(payload)[b'mdia'])[b'hdlr'][8:12] == b'vide'
    def repair(payload, video=False):
        result = []
        for kind, value, *_ in mp4_boxes(payload):
            if kind == b'trak':
                result.append(mp4_box(kind, repair(value, track_is_video(value)))); continue
            if kind in (b'mdia', b'minf', b'stbl', b'edts'):
                value = repair(value, video)
            elif kind == b'stts' and video:
                sample_count = sum(count for count, _ in struct.iter_unpack('>II', value[8:]))
                assert sample_count == len(durations), ('MP4 video sample count', sample_count)
                value = value[:4] + struct.pack('>I', len(runs)) + b''.join(struct.pack('>II', *r) for r in runs)
            elif kind == b'ctts' and video:
                assert all(delta == 0 for _, delta in struct.iter_unpack('>II', value[8:])), 'B-frame offsets unsupported'
            elif kind in (b'mvhd', b'mdhd') and (kind == b'mvhd' or video):
                scale_at, duration_at, width = time_fields(value)
                if kind == b'mdhd': assert struct.unpack_from('>I', value, scale_at)[0] == 16000
                value = put_integer(value, duration_at, width, total if kind == b'mdhd' else movie_duration)
            elif kind == b'tkhd':
                offset, width = (20, 4) if value[0] == 0 else (28, 8)
                if video: value = put_integer(value, offset, width, movie_duration)
                else: assert int.from_bytes(value[offset:offset + width], 'big') <= movie_duration, 'Audio extends beyond exact clip'
            elif kind == b'elst' and video:
                assert struct.unpack_from('>I', value, 4)[0] == 1, 'Nontrivial video edit list unsupported'
                width = 4 if value[0] == 0 else 8
                assert int.from_bytes(value[8 + width:8 + 2 * width], 'big', signed=True) == 0
                assert value[8 + 2 * width:12 + 2 * width] == b'\x00\x01\x00\x00'
                value = put_integer(value, 8, width, movie_duration)
            result.append(mp4_box(kind, value))
        return b''.join(result)
    video_count = sum(track_is_video(track) for track in tracks)
    assert video_count == 1
    changed = repair(moov)
    delta = len(changed) - len(moov)
    def relocate(payload):
        result = []
        for kind, value, *_ in mp4_boxes(payload):
            if kind in (b'trak', b'mdia', b'minf', b'stbl'):
                value = relocate(value)
            elif kind in (b'stco', b'co64'):
                width = 4 if kind == b'stco' else 8
                count = struct.unpack_from('>I', value, 4)[0]
                assert len(value) == 8 + count * width
                buf = bytearray(value)
                for i in range(count):
                    at = 8 + i * width
                    offset = int.from_bytes(value[at:at + width], 'big')
                    if offset >= moov_start + moov_size: offset += delta
                    assert 0 <= offset < 1 << (8 * width)
                    buf[at:at + width] = offset.to_bytes(width, 'big')
                value = bytes(buf)
            result.append(mp4_box(kind, value))
        return b''.join(result)
    changed = relocate(changed)
    output = b''.join(mp4_box(kind, changed) if kind == b'moov'
                      else original[offset:offset + size] for kind, _, offset, size in top)
    assert [hashlib.sha256(value).hexdigest() for kind, value, *_ in mp4_boxes(output) if kind == b'mdat'] == [
        hashlib.sha256(value).hexdigest() for kind, value, *_ in top if kind == b'mdat']
    path.write_bytes(output)
    return {'samples': len(durations), 'duration_ticks': total, 'last_sample_duration_ticks': durations[-1],
            'moov_size_delta_bytes': delta, 'media_payload_bytes_unchanged': True,
            'before_sha256': hashlib.sha256(original).hexdigest(), 'after_sha256': file_sha(path)}


def validate_video_probe(probe, rows, scale, dimensions=(1920, 1080)):
    """Validate every packet duration, decoded PTS and final exclusive endpoint."""
    stream = probe['streams'][0]
    assert (stream['width'], stream['height'], stream['time_base']) == (*dimensions, TIME_BASE)
    expected_pts = [scale * (r['pts'] - CLIP_START) for r in rows]
    expected_duration = [scale * r['duration_ticks'] for r in rows]
    packets = probe['packets']
    frames = probe['frames']
    assert len(packets) == len(frames) == len(rows)
    for i, (packet, frame, pts, duration) in enumerate(zip(packets, frames, expected_pts, expected_duration)):
        assert int(packet['pts']) == int(packet['dts']) == int(frame['best_effort_timestamp']) == pts, i
        assert int(packet['duration']) == duration, (i, packet, duration)
        assert int(frame['pkt_duration']) == duration, (i, frame, duration)
        assert pts + duration == (expected_pts[i + 1] if i + 1 < len(rows) else 160000 * scale)
    assert int(stream['start_pts']) == 0 and int(stream['duration_ts']) == 160000 * scale
    assert Fraction(probe['format']['duration']) == 10 * scale
    return {'decoded_frames': len(rows), 'packets': len(rows), 'PTS_multiplier': scale,
            'max_PTS_error_ticks': 0, 'all_sample_durations_exact': True,
            'last_sample_duration_ticks': expected_duration[-1], 'end_pts_exclusive': 160000 * scale,
            'duration_seconds': 10 * scale, 'actual_continuous_visual_review': False}


def exact_pts_filter(rows):
    """Balanced lookup avoids both concat's 25fps quantization and parser depth."""
    pts = [row['pts'] - CLIP_START for row in rows]
    def expression(lo, hi):
        if hi - lo == 1:
            return str(pts[lo])
        mid = (lo + hi) // 2
        return f'if(lt(N,{mid}),{expression(lo, mid)},{expression(mid, hi)})'
    return "settb=expr=1/16000,setpts='" + expression(0, len(pts)) + "'"

def main():
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
    rows = manifest['records']
    registry_path = base / 'ASSET_REGISTRY.json'
    bindings_path = base / 'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json'
    policy_path = bindings_path.with_name('CURRENT_POLICY_STATIC_REVIEW_INDEX.json')
    coverage_path = base / 'coverage/EXPOSURE_LEDGER.json'
    registry, bindings, coverage, policy_index = map(read, (registry_path, bindings_path, coverage_path, policy_path))
    snapshot_path = a.render_manifest.parent / 'EXPOSURE_BINDINGS_before_render.json'
    snapshot = read(snapshot_path)
    validate_timing(manifest, bindings, coverage)
    binding_checks = validate_current_bindings(manifest, bindings, snapshot, registry, policy_index, a.render_manifest)
    input_hashes = {str(path): sha(path) for path in (a.render_manifest, snapshot_path,
                    registry_path, bindings_path, coverage_path, policy_path)}
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

    save(out / 'evidence/CURRENT_BINDING_VALIDATION.json', {'all_bindings_current': True,
         'input_sha256': input_hashes, 'per_frame_evidence': binding_checks,
         'actual_continuous_visual_review': False})

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
        lines += [f"file '{path}'", f"duration {r['duration_ticks']/16000:.9f}"]
    concat.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    start, end = rows[0]['pts'] / 16000, rows[-1]['end_pts'] / 16000
    duration = end - start
    common = ['-c:v', 'mpeg4', '-q:v', '2', '-bf', '0', '-pix_fmt', 'yuv420p',
              '-vsync', '0', '-enc_time_base', '1:16000', '-video_track_timescale', '16000', '-movflags', '+faststart']
    original = out / '01_original_F0834-F1133.mp4'
    filters = (f'[0:v]trim=start_frame=834:end_frame=1134,setpts=PTS-STARTPTS,trim=end={duration:.9f}[v];'
               f'[0:a]atrim=start={start:.9f}:end={end:.9f},asetpts=PTS-STARTPTS[a]')
    run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', source,
         '-filter_complex', filters, '-map', '[v]', '-map', '[a]', *common,
         '-frames:v', '300', '-t', f'{duration:.9f}',
         '-c:a', 'aac', '-b:a', '192k', original], 'original_encode')
    sample_fixes = {original.name: exact_mp4_sample_durations(original, [r['duration_ticks'] for r in rows])}
    normal = out / '02_character_1080p_original_speed.mp4'
    run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-safe', '0',
         '-f', 'concat', '-i', concat, '-ss', f'{start:.9f}', '-i', source,
         '-map', '0:v:0', '-map', '1:a:0', '-vf', exact_pts_filter(rows),
         '-t', f'{duration:.9f}', '-frames:v', '300', *common,
         '-c:a', 'aac', '-b:a', '192k', normal], 'character_encode')
    sample_fixes[normal.name] = exact_mp4_sample_durations(normal, [r['duration_ticks'] for r in rows])
    slow = out / '03_character_1080p_half_speed.mp4'
    run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', normal,
         '-an', '-vf', 'setpts=2*(PTS-STARTPTS)', '-frames:v', '300', *common, slow], 'slow_encode')
    sample_fixes[slow.name] = exact_mp4_sample_durations(slow, [2 * r['duration_ticks'] for r in rows])
    save(out / 'evidence/EXACT_MP4_SAMPLE_DURATION_REPAIR.json', sample_fixes)
    videos = []
    for video, scale in ((original, 1), (normal, 1), (slow, 2)):
        probe = json.loads(run([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_streams',
            '-show_packets', '-show_format', '-show_entries',
            'packet=pts,dts,duration:stream=width,height,time_base,start_pts,duration_ts,nb_frames:format=duration',
            '-of', 'json', video], video.stem + '_probe'))
        probe['frames'] = json.loads(run([ffprobe, '-v', 'error', '-select_streams', 'v:0',
            '-show_frames', '-show_entries', 'frame=best_effort_timestamp,pkt_duration',
            '-of', 'json', video], video.stem + '_decoded_probe'))['frames']
        videos.append({'path': video.name, 'sha256': sha(video), **validate_video_probe(probe, rows, scale)})
    comparison = a.comparison_dir.resolve()
    assert read(comparison / 'LAYOUT_ACTUAL_REVIEW.json')['layout_sample_review_passed']
    for name in ('dance_all_66_original_vs_current.png', 'MANIFEST.json', 'LAYOUT_ACTUAL_REVIEW.json'):
        shutil.copyfile(comparison / name, out / ('comparison_' + name))
    for file in (a.render_manifest, bindings_path, snapshot_path, policy_path):
        shutil.copyfile(file, out / 'evidence' / file.name)
    (out / '先读我.txt').write_text(
        '首段舞蹈 F834–1133，66个绘制态，300个曝光。\n'
        '01为原PV截取（原声/原字幕保留）；02为人物层原速审阅片；03为无声0.5倍慢速。\n'
        '人物审阅视频使用粉底，不含最终背景、字幕、特效或道具合成。\n'
        'layers_1080p是真透明人物层；raw_returns是保留的完整返图。\n'
        '双击index.html可按真实PTS对照原片/人物层，切换速度与底色并逐帧查看。\n'
        '静态绘制与定位已逐稿经主审及Sol xhigh检查。视频编码/PTS核对不等于实际连续播放审评；后者仍待完成。用户艺术验收另记，GOAL未完成。\n', encoding='utf-8')
    # A long encode must not bless a selection/review changed while packaging.
    assert all(sha(path) == digest for path, digest in input_hashes.items()), 'Build inputs changed during encoding'
    final_checks = validate_current_bindings(manifest, read(bindings_path), snapshot,
                     read(registry_path), read(policy_path), a.render_manifest)
    assert final_checks == binding_checks
    receipt = {'created_utc': datetime.now(timezone.utc).isoformat(), 'source_sha256': sha(source),
        'source_frame_range': [834, 1133], 'time_base': '1/16000', 'exposures': 300,
        'unique_artworks': 66, 'artworks': list(masters.values()), 'videos': videos,
        'render_manifest_sha256': sha(a.render_manifest), 'all_bindings_current': True,
        'binding_evidence_checked_exposures': len(final_checks), 'exact_video_sample_durations_validated': True,
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


if __name__ == "__main__":
    main()
