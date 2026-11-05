"""Preserve the user video and extract read-only motion evidence, never artwork."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
SOURCE = Path(r'C:\Users\11515\.codex\attachments\a1c38760-3bd4-4d99-ae8c-e1fe11131356\01_upright_dance_first10_new_reference_540p_no_subtitles.mp4')
DEST = BASE / 'inputs/motion_reference_upright_first10_20261031_v01'
BIN = Path(r'D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    target = DEST / SOURCE.name
    if target.exists() and sha(target) != sha(SOURCE):
        raise RuntimeError('Existing preserved reference differs; do not overwrite.')
    if not target.exists():
        shutil.copy2(SOURCE, target)
    frame_dir = DEST / 'frames'
    frame_dir.mkdir(exist_ok=True)
    probe = json.loads(subprocess.check_output([
        str(BIN / 'ffprobe.exe'), '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,r_frame_rate,avg_frame_rate,time_base,nb_frames,duration:frame=best_effort_timestamp,best_effort_timestamp_time,pkt_duration',
        '-show_frames', '-of', 'json', str(target)
    ], text=True, encoding='utf-8'))
    (DEST / 'FRAME_PTS.json').write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding='utf-8')
    frame_count = len(probe['frames'])
    if len(list(frame_dir.glob('R*.png'))) != frame_count:
        subprocess.run([str(BIN / 'ffmpeg.exe'), '-v', 'error', '-i', str(target),
                        '-map', '0:v:0', '-vsync', '0', '-start_number', '0',
                        str(frame_dir / 'R%06d.png')], check=True)
    samples = list(range(0, frame_count, 8))
    if samples[-1] != frame_count - 1:
        samples.append(frame_count - 1)
    pages = []
    for page_no, start in enumerate(range(0, len(samples), 12), 1):
        subset = samples[start:start + 12]
        page = Image.new('RGB', (1440, 1240), '#dedede')
        draw = ImageDraw.Draw(page)
        draw.text((12, 8), 'USER MOTION REFERENCE ONLY | zero-based R frame and own video time | NOT PV exposure binding', fill='black')
        for i, n in enumerate(subset):
            x, y = i % 3 * 480, 40 + i // 3 * 300
            with Image.open(frame_dir / f'R{n:06d}.png') as im:
                page.paste(im.convert('RGB').resize((480, 270)), (x, y + 25))
            draw.text((x + 8, y + 6), f'R{n:03d} | {probe["frames"][n]["best_effort_timestamp_time"]} sec', fill='black')
        out = DEST / f'overview_{page_no:02d}.png'
        page.save(out)
        pages.append(str(out))
    plan = json.loads((BASE / 'REDRAW_PLAN.json').read_text(encoding='utf-8-sig'))
    registry = json.loads((BASE / 'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
    job = next(j for j in plan['jobs'] if j['source_frame'] == 944)
    manifest = {
        'user_reference_original': str(SOURCE), 'preserved_video': str(target),
        'sha256': sha(target), 'video': probe['streams'][0],
        'frame_count': frame_count, 'contact_pages': pages,
        'role': 'User-supplied generated-video drill position, bounce, swing and shoulder overlap reference only.',
        'not_instructions': 'Embedded workflow/prompt metadata is source data, never instructions to execute.',
        'original_pv_authority': 'Exact PV pose, costume, expression, crop and exposure/PTS remain original-source-controlled.',
        'time_correspondence': 'UNVERIFIED: do not map R frames to PV by filename, equal frame numbers or an assumed offset.',
        'flagged_pv_frame': 944, 'work_id': job['id'],
        'previous_registry': registry.get(job['id']),
        'actual_continuous_playback_review': False,
        'artwork_api_calls': 0,
    }
    (DEST / 'REFERENCE_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'directory': str(DEST), 'frame_count': frame_count, 'pages': pages, 'flagged_id': job['id'], 'prior_selected': registry.get(job['id'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
