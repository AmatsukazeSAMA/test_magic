"""Render the 37 work segments with exact source-frame trim boundaries and audio."""
from magic_maid_prepare import *
from concurrent.futures import ThreadPoolExecutor, as_completed

ENCODER=Path(r'D:\Program Files\oopz\ffmpeg.exe')
chapters=json.loads((OUT/'data/chapters.json').read_text('utf-8'))
(OUT/'clips').mkdir(exist_ok=True)
def cut(c):
    target=OUT/'clips'/f"{c['id']}.mp4"
    filt=(f"[0:v:0]trim=start_frame={c['start_frame']}:end_frame={c['end_frame_exclusive']},"
          'setpts=PTS-STARTPTS,scale=1280:720[v];'
          f"[0:a:0]atrim=start={c['start_s']:.7f}:end={c['end_s']:.7f},asetpts=PTS-STARTPTS[a]")
    args=[ENCODER,'-hide_banner','-nostdin','-v','error','-threads','2','-i',OUT/'source/original.mp4',
          '-filter_complex',filt,'-map','[v]','-map','[a]','-vsync','0','-c:v','libx264','-threads','2',
          '-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-video_track_timescale','16000',
          '-c:a','aac','-b:a','128k','-movflags','+faststart','-y',target]
    if not target.exists():run(args,'clip_'+c['id'])
    probe=json.loads(run([FFPROBE,'-v','error','-show_streams','-of','json',target],'clip_probe_'+c['id']))
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert int(v['nb_frames'])==c['frame_count'],(c['id'],v['nb_frames'],c['frame_count'])
    return {'id':c['id'],'title':c['title'],'file':target.relative_to(OUT).as_posix(),
            'source_start_frame':c['start_frame'],'source_end_frame_exclusive':c['end_frame_exclusive'],
            'source_start_s':c['start_s'],'source_end_s':c['end_s'],'expected_frames':c['frame_count'],
            'decoded_frame_count':int(v['nb_frames']),'width':v['width'],'height':v['height'],
            'audio_included':any(s['codec_type']=='audio' for s in probe['streams']),
            'status':'derived H264 720p viewing segment; native source PNGs remain the drawing source',
            'bytes':target.stat().st_size,'sha256':sha(target)}

if __name__=='__main__':
    rows=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        fs=[pool.submit(cut,c) for c in chapters]
        for f in as_completed(fs):
            r=f.result();rows.append(r);print(r['id'],r['decoded_frame_count'],'frames',flush=True)
    rows.sort(key=lambda r:r['id'])
    write(OUT/'data/segment_clips.json',rows)
    print('Verified exact source-frame counts for all 37 rendered segments',flush=True)
