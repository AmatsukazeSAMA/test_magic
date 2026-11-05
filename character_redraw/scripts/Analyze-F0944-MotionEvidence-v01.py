"""Read-only comparison and audio timing evidence for the user-flagged cel."""
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
REF = BASE / 'inputs/motion_reference_upright_first10_20261031_v01'
DEST = REF / 'F0944_diagnostic'
BIN = Path(r'D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime')


def pcm(path, start=None, duration=None):
    args = [str(BIN / 'ffmpeg.exe'), '-v', 'error']
    if start is not None:
        args += ['-ss', str(start)]
    args += ['-i', str(path)]
    if duration is not None:
        args += ['-t', str(duration)]
    args += ['-vn', '-ac', '1', '-ar', '8000', '-f', 'f32le', 'pipe:1']
    return np.frombuffer(subprocess.check_output(args), dtype='<f4').astype(np.float64)


def panel(image, size):
    im = image.convert('RGBA')
    white = Image.new('RGBA', im.size, 'white')
    white.alpha_composite(im)
    out = Image.new('RGB', size, '#eeeeee')
    white.thumbnail(size)
    out.paste(white.convert('RGB'), ((size[0] - white.width) // 2, (size[1] - white.height) // 2))
    return out


def main():
    DEST.mkdir(exist_ok=True)
    ledger = json.loads((BASE / 'coverage/EXPOSURE_LEDGER.json').read_text(encoding='utf-8-sig'))
    manifest = json.loads((REF / 'REFERENCE_MANIFEST.json').read_text(encoding='utf-8'))
    source = Path(ledger['source_video'])
    a = pcm(source, 25, 17)
    b = pcm(manifest['preserved_video'])
    a -= a.mean()
    b -= b.mean()
    n = 1 << (len(a) + len(b) - 1).bit_length()
    conv = np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b[::-1], n), n)
    valid = conv[len(b) - 1:len(a)]
    sq = np.r_[0.0, np.cumsum(a * a)]
    energy = sq[len(b):] - sq[:-len(b)]
    score = valid / np.sqrt(np.maximum(energy * (b @ b), 1e-20))
    lag = int(np.argmax(score))
    offset = 25 + lag / 8000
    pv944_seconds = ledger['frames'][944]['pts'] / 16000
    ref_time = pv944_seconds - offset
    ref_frame = int(round(ref_time * 24))
    timing = {
        'method': 'Normalized cross correlation of decoded 8000Hz mono audio; original search window [25,42] seconds.',
        'reference_video_t0_at_pv_audio_seconds': offset,
        'peak_normalized_audio_correlation': float(score[lag]),
        'pv_frame': 944, 'pv_pts': ledger['frames'][944]['pts'],
        'pv_seconds': pv944_seconds, 'reference_seconds_for_pv944': ref_time,
        'nearest_reference_video_frame': ref_frame,
        'reference_frame_rate': '24/1', 'pv_time_base': '1/16000',
        'limitation': 'Audio alignment does not prove frame-exact choreography or validate generated hair geometry; compare visible poses independently.',
        'artwork_or_exposure_bindings_modified': False,
    }
    (DEST / 'AUDIO_ALIGNMENT.json').write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding='utf-8')
    samples = list(range(max(0, ref_frame - 8), min(240, ref_frame + 9), 2))
    page = Image.new('RGB', (1440, 1240), '#dedede')
    draw = ImageDraw.Draw(page)
    draw.text((12, 8), 'Motion diagnostic: reference video neighbors only; R frames are NOT original PV frame numbers', fill='black')
    for i, r in enumerate(samples):
        x, y = i % 3 * 480, 40 + i // 3 * 400
        with Image.open(REF / 'frames' / f'R{r:06d}.png') as im:
            page.paste(im.resize((480, 270)), (x, y + 25))
            # Crop for observing beads, shoulder and raised-arm occlusion. Evidence only.
            page.paste(panel(im.crop((330, 120, 650, 350)), (480, 100)), (x, y + 295))
        draw.text((x + 8, y + 6), f'R{r:03d} | {r/24:.6f} sec', fill='black')
    page.save(DEST / 'reference_neighbors.png')
    # Full-resolution evidence, not a drawing input mashup.
    source_frame = BASE / 'coverage/source_frames/F000944.png'
    with Image.open(source_frame) as im:
        im.crop((447, 86, 1322, 1080)).save(DEST / 'original_PV_F0944_crop.png')
    with Image.open(REF / 'frames' / f'R{ref_frame:06d}.png') as im:
        im.save(DEST / 'nearest_reference_full.png')
        im.crop((330, 120, 650, 350)).save(DEST / 'nearest_reference_hair_arm_crop.png')
    panels = [
        ('Original PV F0944: exact pose/costume authority', DEST / 'original_PV_F0944_crop.png'),
        ('Rejected G12-34 v01: coil overlays crossing forearm', BASE / 'drawings/ART-G12-34/v01/qa_white.png'),
        (f'User motion R{ref_frame:03d}: timing reference, not pose tracing', DEST / 'nearest_reference_full.png'),
    ]
    comparison = Image.new('RGB', (1800, 1050), '#dddddd')
    draw = ImageDraw.Draw(comparison)
    for i, (label, path) in enumerate(panels):
        with Image.open(path) as im:
            comparison.paste(panel(im, (600, 970)), (i * 600, 70))
        draw.text((i * 600 + 8, 15), label, fill='black')
    comparison.save(DEST / 'F0944_position_comparison.png')
    print(json.dumps(timing, ensure_ascii=False))


if __name__ == '__main__':
    main()
