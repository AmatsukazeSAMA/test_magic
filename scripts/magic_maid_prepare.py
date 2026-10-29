"""Preserve the two supplied videos and build PTS-based, read-only surveys."""
from pathlib import Path
from fractions import Fraction
import bisect, hashlib, json, shutil, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'magic_maid_20261029'
FFDIR = Path(r'D:\CODEX\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\runtime')
FFMPEG, FFPROBE = FFDIR/'ffmpeg.exe', FFDIR/'ffprobe.exe'
INPUTS = {
    'original': Path('D:/downloads/【本家投稿】マジック・メイド (魔法女仆) _ MIMI feat. 重音テトSV P1 【本家投稿】マジック・メイド (魔法女仆) _ MIMI feat. 重音テトSV.mp4'),
    'reference': Path('D:/downloads/“魔法女仆”逐帧描改素材！ P1 video_260103_025433.mp4'),
}
for p in ['source','data','sheets','frames','reference_frames','logs','previews','cels']:
    (OUT/p).mkdir(parents=True, exist_ok=True)

def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def run(args, name):
    started=time.monotonic()
    p=subprocess.run([str(a) for a in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (OUT/'logs'/f'{name}.stderr.txt').write_bytes(p.stderr)
    if p.returncode: raise RuntimeError(p.stderr.decode('utf-8', errors='replace'))
    return p.stdout

def survey(name, step):
    src=INPUTS[name]
    copy=OUT/'source'/f'{name}.mp4'
    if not copy.exists(): shutil.copy2(src,copy)
    assert sha(src)==sha(copy)
    probe=json.loads(run([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',copy],name+'_probe'))
    write(OUT/'data'/f'{name}_ffprobe.json',probe)
    timeline=json.loads(run([FFPROBE,'-v','error','-select_streams','v:0','-show_frames','-show_entries',
        'frame=best_effort_timestamp,best_effort_timestamp_time,pkt_duration,pkt_duration_time,key_frame,pict_type',
        '-of','json',copy],name+'_pts'))['frames']
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    a=next(s for s in probe['streams'] if s['codec_type']=='audio')
    tb=Fraction(v['time_base'])
    ts=[float(int(f['best_effort_timestamp'])*tb) for f in timeline]
    rows=[{'frame':i,'pts':int(f['best_effort_timestamp']),'time_s':ts[i],
        'duration_s':(ts[i+1] if i+1<len(ts) else float(v['duration']))-ts[i]} for i,f in enumerate(timeline)]
    write(OUT/'data'/f'{name}_timeline.json',rows)
    thumbpath=OUT/'data'/f'{name}_thumbs.npy'
    if not thumbpath.exists():
        args=[FFMPEG,'-hide_banner','-nostdin','-v','error','-threads','4','-i',str(copy),'-map','0:v:0','-an',
            '-vf','scale=480:270:flags=area','-vsync','0','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
        p=subprocess.Popen([str(a) for a in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arr=np.lib.format.open_memmap(thumbpath,mode='w+',dtype=np.uint8,shape=(len(rows),270,480,3))
        for i in range(len(rows)):
            size=480*270*3
            buf=bytearray()
            while len(buf)<size:
                block=p.stdout.read(size-len(buf))
                if not block: break
                buf.extend(block)
            if len(buf)!=size: raise RuntimeError(f'{name}: short decode at {i}')
            arr[i]=np.frombuffer(buf,dtype=np.uint8).reshape(270,480,3)
        remaining=p.stdout.read()
        err=p.stderr.read()
        assert p.wait()==0 and not remaining, err
        arr.flush()
        del arr
    arr=np.load(thumbpath,mmap_mode='r')
    previous=None
    metrics=[]
    for i,im in enumerate(arr):
        g=(im[:,:,0].astype(np.float32)*.299+im[:,:,1]*.587+im[:,:,2]*.114).astype(np.uint8)
        if previous is None: mae=frac=0.
        else:
            diff=np.abs(g.astype(np.int16)-previous.astype(np.int16))
            mae=float(diff.mean()); frac=float((diff>12).mean())
        metrics.append({'frame':i,'time_s':ts[i],'adjacent_mae':round(mae,5),'changed_gt12':round(frac,6)})
        previous=g
    write(OUT/'data'/f'{name}_metrics.json',metrics)
    indices=sorted(set(min(bisect.bisect_left(ts,t),len(ts)-1) for t in np.arange(0,ts[-1]+step,step)))
    font=ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf',16)
    for page,off in enumerate(range(0,len(indices),24),1):
        ids=indices[off:off+24]
        board=Image.new('RGB',(4*384,((len(ids)+3)//4)*242),'#161d2a')
        d=ImageDraw.Draw(board)
        for j,f in enumerate(ids):
            x,y=j%4*384,j//4*242
            board.paste(Image.fromarray(arr[f]).resize((384,216),Image.Resampling.LANCZOS),(x,y))
            d.text((x+6,y+219),f'{name} F{f:06d} {ts[f]:07.3f}s',font=font,fill='white')
        board.save(OUT/'sheets'/f'{name}_survey_{page:02d}.jpg',quality=93)
    summary={'name':name,'path':str(src),'copy':copy.relative_to(OUT).as_posix(),'sha256':sha(src),
        'bytes':src.stat().st_size,'frame_count':len(rows),'width':v['width'],'height':v['height'],
        'r_frame_rate':v['r_frame_rate'],'avg_frame_rate':v['avg_frame_rate'],'time_base':v['time_base'],
        'video_duration_s':float(v['duration']),'audio_duration_s':float(a['duration']),
        'container_duration_s':float(probe['format']['duration']),
        'thumbs_are_scaled_analysis_images':True,'source_files_unchanged':sha(src)==sha(copy)}
    write(OUT/'data'/f'{name}_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False),flush=True)

def extract_original():
    summary=json.loads((OUT/'data/original_summary.json').read_text('utf-8'))
    if len(list((OUT/'frames').glob('F*.png')))==summary['frame_count']:
        print('Native original frames already complete',flush=True);return
    run([FFMPEG,'-hide_banner','-nostdin','-v','warning','-threads','4','-i',OUT/'source/original.mp4',
        '-map','0:v:0','-an','-vsync','0','-start_number','0','-compression_level','3','-y',
        OUT/'frames/F%06d.png'],'extract_original_native')
    assert len(list((OUT/'frames').glob('F*.png')))==summary['frame_count']
    print('All native original PNG frames extracted',flush=True)

if __name__=='__main__':
    if '--extract-original' in sys.argv: extract_original()
    elif '--reference' in sys.argv: survey('reference',5.)
    else:
        survey('original',2.5)
        survey('reference',5.)
