"""Export a reviewed first-dance comparison; never certify visual playback."""
from argparse import ArgumentParser
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import json
import runpy
import shutil
import subprocess

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
DANCE = BASE / 'dance_first10_reference_redraw_v01'
FULL_BUILDER = ROOT / 'scripts/Build-FirstDanceCurrentReview20261102.py'
FFMPEG = Path(r'D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\ffmpeg.exe')
FFPROBE = FFMPEG.with_name('ffprobe.exe')
START = 445248
# Only explicitly reviewed spans; a longer manifest may contain later gaps.
CLIPS = {844: (451120, [('ART-G33-01', 7), ('ART-G33-02', 4)]),
         848: (453248, [('ART-G33-01', 7), ('ART-G33-02', 4), ('ART-G33-03', 4)]),
         866: (462864, [('ART-G33-01', 7), ('ART-G33-02', 4), ('ART-G33-03', 4),
                        ('ART-G33-04', 5), ('ART-G33-05', 4), ('ART-G12-10', 3),
                        ('ART-G33-07', 2), ('ART-G33-08', 4)])}
CLIPS[870] = (464992, [*CLIPS[866][1], ('ART-G33-09', 4)])
CLIPS[881] = (470864, [('ART-G33-11', 4), ('ART-G33-12', 4)])
CLIPS[891] = (476208, [*CLIPS[870][1], ('ART-G33-10', 3), *CLIPS[881][1],
                      ('ART-G33-13', 4), ('ART-G33-14', 3), ('ART-G33-15', 3)])
CLIPS[894] = (477808, [*CLIPS[891][1], ('ART-G12-20', 3)])
CLIPS[906] = (484224, [('ART-G12-23', 4)])
CLIPS[909] = (485824, [*CLIPS[906][1], ('ART-G33-20', 3)])
CLIPS[913] = (487952, [*CLIPS[909][1], ('ART-G12-25', 4)])
TIME_BASE = '1/16000'
PANEL = (1920, 1080)
VIDEO = (3840, 1080)
PINK = (212, 168, 168, 255)


def main():
    parser = ArgumentParser(__doc__)
    parser.add_argument('--render-manifest', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--last-frame', type=int, choices=tuple(CLIPS), default=844)
    args = parser.parse_args()
    last_frame = args.last_frame
    end, artworks = CLIPS[last_frame]
    first_frame = last_frame - sum(count for _, count in artworks) + 1
    clip_name = f'F{first_frame:04d}-F{last_frame:04d}'
    manifest_path, out = args.render_manifest.resolve(), args.output_dir.resolve()
    out.relative_to(BASE / 'review')
    assert not out.exists(), 'Use a new review directory; preserve earlier results.'
    reused = runpy.run_path(str(FULL_BUILDER))
    read, sha = reused['read_json'], reused['file_sha']
    assert reused['CLIP_START'] == START and reused['TIME_BASE'] == TIME_BASE
    manifest = read(manifest_path)
    manifest_rows = manifest['records']
    rows = [r for r in manifest_rows if first_frame <= r['frame'] <= last_frame]
    excluded = [r['frame'] for r in manifest_rows if not first_frame <= r['frame'] <= last_frame]
    clip_manifest = {**manifest, 'records': rows}
    assert manifest['source_time_base'] == TIME_BASE
    assert manifest['verified_exposures'] == len(manifest_rows)
    assert [r['frame'] for r in rows] == list(range(first_frame, last_frame + 1))
    assert [r['id'] for r in rows] == [work for work, count in artworks for _ in range(count)]
    assert rows[-1]['end_pts'] == end
    start = rows[0]['pts']
    if first_frame == 834:
        assert start == START
    ledger = manifest_path.with_name('SOURCE_EXPOSURE_LEDGER_before_render.json')
    live_ledger = BASE / 'coverage/EXPOSURE_LEDGER.json'
    source_ledgers = [read(ledger), read(live_ledger)]
    for data in source_ledgers:
        assert data['time_base'] == TIME_BASE
        source_rows = {r['frame']: r for r in data['frames']}
        for row in rows:
            assert all(type(row[k]) is int and row[k] == source_rows[row['frame']][k]
                       for k in ('pts', 'end_pts', 'duration_ticks'))
    assert all(r['pts'] + r['duration_ticks'] == r['end_pts'] for r in rows)
    assert all(a['end_pts'] == b['pts'] for a, b in zip(rows, rows[1:]))
    registry = BASE / 'ASSET_REGISTRY.json'
    bindings = DANCE / 'EXPOSURE_BINDINGS.json'
    policy = DANCE / 'CURRENT_POLICY_STATIC_REVIEW_INDEX.json'
    snapshot = manifest_path.with_name('EXPOSURE_BINDINGS_before_render.json')
    frozen = read(snapshot)

    def current_checks():
        return reused['validate_current_bindings'](clip_manifest, read(bindings), frozen,
                    read(registry), read(policy), manifest_path)

    before = current_checks()
    out.mkdir()
    evidence = out / 'evidence'
    evidence.mkdir()
    layers_dir = out / 'layers_1080p'
    layers_dir.mkdir()

    def save(name, value):
        (evidence / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def run(name, command, input_bytes=None):
        command = list(map(str, command))
        save(name + '.command.json', command)
        result = subprocess.run(command, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (evidence / (name + '.log')).write_bytes(result.stderr)
        assert result.returncode == 0, (name, result.stderr.decode(errors='replace'))
        return result.stdout

    layers, compositions, source_proof = {}, [], []
    fixed_inputs = {p: sha(p) for p in (manifest_path, ledger, snapshot, FULL_BUILDER)}
    for row in rows:
        work = row['id']
        if work not in layers:
            original = Path(row['image'])
            exported = layers_dir / f'{work}.png'
            shutil.copyfile(original, exported)
            assert sha(original) == sha(exported) == row['image_sha256']
            with Image.open(exported) as layer:
                assert layer.mode == 'RGBA' and layer.size == PANEL
                pink = Image.alpha_composite(Image.new('RGBA', PANEL, PINK), layer).convert('RGB')
            layers[work] = pink, exported, row['image_sha256']
            fixed_inputs[original] = row['image_sha256']
        src = BASE / 'coverage/source_frames' / f"F{row['frame']:06d}.png"
        fixed_inputs[src] = sha(src)
        with Image.open(src) as original:
            assert original.size == PANEL
            pair = Image.new('RGB', VIDEO)
            pair.paste(original.convert('RGB'), (0, 0))
            pair.paste(layers[work][0], (1920, 0))
        compositions.append(pair)
        source_proof.append({**{k: row[k] for k in ('frame', 'pts', 'end_pts', 'duration_ticks', 'id')},
            'source_path': str(src), 'source_sha256': fixed_inputs[src],
            'rgba_layer': layers[work][1].relative_to(out).as_posix(), 'rgba_sha256': row['image_sha256']})
    samples = b''.join(pair.tobytes() for pair in compositions)
    preview_size = (960, 270)
    thumbnail_expectations = [np.asarray(i.resize(preview_size, Image.Resampling.BOX), dtype=np.int16)
                              for i in compositions]
    video_records = []
    for factor, label in ((1, 'original_speed'), (2, 'half_speed')):
        name = f'{clip_name}_{label}'
        file = out / (name + '.mp4')
        title = f'{clip_name} | {"1x" if factor == 1 else "0.5x"} | Original PV left / current pink preview right'
        expected_pts = [factor * (r['pts'] - start) for r in rows]
        scaled_rows = [{'pts': START + pts} for pts in expected_pts]
        durations = [factor * r['duration_ticks'] for r in rows]
        duration = factor * (end - start)
        run(name + '_encode', [FFMPEG, '-hide_banner', '-v', 'error', '-nostdin', '-n',
            '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', '3840x1080', '-framerate', '30', '-i', 'pipe:0',
            '-vf', reused['exact_pts_filter'](scaled_rows), '-an', '-frames:v', str(len(rows)), '-vsync', '0',
            '-c:v', 'h264_mf', '-hw_encoding', '0', '-bf', '0', '-b:v', '36M', '-pix_fmt', 'yuv420p',
            '-enc_time_base', '1:16000', '-video_track_timescale', '16000',
            '-metadata', f'title={title}', '-movflags', '+faststart', file], samples)
        sample_fix = reused['exact_mp4_sample_durations'](file, durations)
        probes = json.loads(run(name + '_packets', [FFPROBE, '-v', 'error', '-select_streams', 'v:0',
            '-show_streams', '-show_packets', '-show_format', '-of', 'json', file]))
        probes['frames'] = json.loads(run(name + '_frames', [FFPROBE, '-v', 'error', '-select_streams', 'v:0',
            '-show_frames', '-show_entries', 'frame=best_effort_timestamp,pkt_duration', '-of', 'json', file]))['frames']
        save(name + '_ffprobe.json', probes)
        stream = probes['streams'][0]
        assert (stream['width'], stream['height'], stream['time_base'], stream['codec_name']) == (*VIDEO, TIME_BASE, 'h264')
        assert int(stream['start_pts']) == 0 and int(stream['duration_ts']) == duration
        assert Fraction(probes['format']['duration']) == Fraction(duration, 16000)
        assert probes['format']['tags']['title'] == title
        assert len(probes['packets']) == len(probes['frames']) == len(rows)
        for pkt, decoded, pts, hold in zip(probes['packets'], probes['frames'], expected_pts, durations):
            assert tuple(map(int, (pkt['pts'], pkt['dts'], decoded['best_effort_timestamp']))) == (pts, pts, pts)
            assert int(pkt['duration']) == int(decoded['pkt_duration']) == hold
        assert expected_pts[-1] + durations[-1] == duration
        pixels = run(name + '_route_decode', [FFMPEG, '-hide_banner', '-v', 'error', '-nostdin', '-i', file,
            '-vf', 'scale=960:270:flags=area', '-vsync', '0', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'])
        actual = np.frombuffer(pixels, dtype=np.uint8).reshape((-1, 270, 960, 3))
        assert len(actual) == len(rows)
        errors = [np.abs(a.astype(np.int16) - b) for a, b in zip(actual, thumbnail_expectations)]
        mae = [[round(float(e[:, :480].mean()), 4), round(float(e[:, 480:].mean()), 4)] for e in errors]
        assert max(max(e) for e in mae) < 8, ('Wrong panel or unexpected encode differences', mae)
        if factor == 1:
            diagnostic_indices = [0] + [n for n in range(1, len(rows)) if rows[n]['id'] != rows[n - 1]['id']]
            diagnostic_indices.append(len(rows) - 1)
            board = Image.new('RGB', (960, 270 * len(diagnostic_indices)))
            for j, n in enumerate(diagnostic_indices):
                board.paste(Image.fromarray(actual[n]), (0, j * 270))
            suffix = '_'.join(f"F{rows[n]['frame']:04d}" for n in diagnostic_indices)
            board.save(evidence / f'DECODED_ROUTING_{suffix}.png')
        video_records.append({'path': file.name, 'title': title, 'sha256': sha(file), 'speed': f'1/{factor}', 'codec': 'h264',
            'pts_ticks': expected_pts, 'hold_ticks': durations, 'duration_ticks': duration,
            'duration_seconds': duration / 16000, 'frames': len(rows), 'packets': len(rows),
            'decoded_panel_mean_absolute_RGB_error': mae, 'exact_mp4_sample_duration_fix': sample_fix})
    assert all(sha(p) == digest for p, digest in fixed_inputs.items())
    assert all(sha(copy) == digest for _, copy, digest in layers.values())
    assert current_checks() == before
    receipt = {'classification': 'partial_technical_preview', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'render_manifest': str(manifest_path), 'render_manifest_sha256': fixed_inputs[manifest_path],
        'source_frame_range': [first_frame, last_frame], 'source_time_base': TIME_BASE, 'source_pts_range': [start, end],
        'end_pts_is_exclusive': True, 'exposures': len(rows), 'total_dance_exposures': 300, 'frames': source_proof,
        'render_manifest_exposures': len(manifest_rows), 'excluded_manifest_frames': excluded,
        'interpolated_or_gap_fill_frames': 0,
        'exact_binding_evidence': before, 'video_dimensions': list(VIDEO), 'left_panel': 'source RGB at native dimensions',
        'right_panel': 'current native RGBA composited on RGB 212,168,168', 'audio': False, 'videos': video_records,
        'actual_continuous_visual_playback_review': False, 'artistic_acceptance': False, 'user_accepted': False,
        'full_dance_complete': False, 'registry_or_bindings_modified': False}
    (out / 'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    normal_seconds, slow_seconds = [r['duration_seconds'] for r in video_records]
    (out / '先读我.txt').write_text(f'{clip_name} 部分技术预览：左原PV，右当前人物透明层合成粉底。\n'
        f'原速{normal_seconds:g}秒，半速{slow_seconds:g}秒，均无声；两版{len(rows)}帧的真实PTS与每帧时长均经ffprobe逐项验证。\n'
        f'只播放原帧F{first_frame}–{last_frame}；区间外不拼接、不补帧。\n'
        'layers_1080p 是保留精确SHA的透明PNG，不含粉底。尚未实际连续观看，不代表首段完成或用户验收。\n', encoding='utf-8')
    print(json.dumps({'output': str(out), 'videos': video_records,
        'receipt_sha256': sha(out / 'DELIVERY_RECEIPT.json'), 'actual_playback_review': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
