"""Preserve user 360 reference and extract exact frames for rear-bob structure review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
folder = base / 'inputs/user_upper_body_360_hair_structure_20261103_v01'
frames = folder / 'frames'
frames.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
video_source = Path('C:/Users/11515/Desktop/upper_body_360_720p24.mp4')
clip_source = Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-cbe31e5b-8851-46cc-bdba-daa4e374d2bc.png')
for source, name in [(video_source, video_source.name), (clip_source, 'user_rear_bob_screenshot.png')]:
    target = folder / name
    if target.exists():
        assert sha(target) == sha(source)
    else:
        shutil.copy2(source, target)
bin_dir = Path('D:/CODEX/GPT-SoVITS-v2pro-20250604-nvidia50/GPT-SoVITS-v2pro-20250604-nvidia50/runtime')
probe = json.loads(subprocess.check_output([str(bin_dir/'ffprobe.exe'), '-v', 'error', '-select_streams', 'v:0',
    '-show_entries', 'stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,time_base:frame=best_effort_timestamp,best_effort_timestamp_time,pkt_duration',
    '-show_frames', '-of', 'json', str(folder/video_source.name)], text=True, encoding='utf-8'))
(folder/'FRAME_PTS.json').write_text(json.dumps(probe, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
count = len(probe['frames'])
if len(list(frames.glob('R*.png'))) != count:
    subprocess.run([str(bin_dir/'ffmpeg.exe'), '-v', 'error', '-nostdin', '-n', '-i', str(folder/video_source.name),
        '-map', '0:v:0', '-vsync', '0', '-start_number', '0', str(frames/'R%06d.png')], check=True)
samples = [0, 9, 18, 27, 36, 45, 54, 63, 72, 81, 90, count-1]
page = Image.new('RGB', (1920, 1570), '#e4e4e4')
draw = ImageDraw.Draw(page)
draw.text((12, 8), 'USER 360 REFERENCE | back bob geometry only | own R frame / video time, NOT original PV timing', fill='black')
for i,n in enumerate(samples):
    x,y = (i%3)*640, 32+(i//3)*384
    draw.text((x+8,y+2), f"R{n:03d} | {probe['frames'][n]['best_effort_timestamp_time']}s", fill='black')
    with Image.open(frames/f'R{n:06d}.png') as im:
        page.paste(im.convert('RGB').resize((640,360)), (x,y+22))
overview = folder/'OVERVIEW_12_ACTUAL_FRAMES.png'
page.save(overview)
manifest = {'recorded_utc': datetime.now(timezone.utc).isoformat(), 'user_verbatim': '后发太乱，参考该视频',
    'video': {'source': str(video_source), 'preserved': str(folder/video_source.name), 'sha256': sha(folder/video_source.name), 'stream': probe['streams'][0]},
    'screenshot': {'source': str(clip_source), 'preserved': str(folder/'user_rear_bob_screenshot.png'), 'sha256': sha(folder/'user_rear_bob_screenshot.png')},
    'decoded_frame_count': count, 'frames': str(frames), 'exact_video_PTS': str(folder/'FRAME_PTS.json'),
    'sample_frames': samples, 'overview': {'path': str(overview), 'sha256': sha(overview)},
    'reference_role': 'Latest user-authorized posterior bob contour, large strand grouping, volume and nape closure. Distinct from earlier AI-video motion-only reference.',
    'original_PV_still_controls': 'Own character pose, head/body orientation, eyes/mouth/hands, costume, crop, action and 4763-frame exposure/PTS.',
    'not_transferred': 'Polished highlights, gradient shading, vest/shirt costume, video body motion or video timing.',
    'actual_continuous_playback_review': False, 'actual_visual_frame_review_completed': False,
    'generation_calls': 0, 'user_accepted_art': False}
(folder/'REFERENCE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'manifest':str(folder/'REFERENCE_MANIFEST.json'), 'decoded_frames':count, 'overview':str(overview), 'video_sha256':manifest['video']['sha256']},ensure_ascii=False))
