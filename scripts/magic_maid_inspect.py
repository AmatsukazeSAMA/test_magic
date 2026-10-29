"""Contact sheets and exact native samples for visual inspection, without retouching."""
from magic_maid_prepare import *
import argparse

def sheet(name, indices, filename, cols=4, width=384, crop=None, labels=None, native=False):
    rows=json.loads((OUT/'data'/f'{name}_timeline.json').read_text('utf-8'))
    arr=None if native else np.load(OUT/'data'/f'{name}_thumbs.npy',mmap_mode='r')
    srcsize=(1920,1080) if native else (480,270)
    crop=crop or (0,0,*srcsize)
    height=round(width*(crop[3]-crop[1])/(crop[2]-crop[0]))
    cellh=height+42
    board=Image.new('RGB',(cols*width,((len(indices)+cols-1)//cols)*cellh),'#172131')
    d=ImageDraw.Draw(board)
    font=ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf',14)
    zh=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',14)
    for j,f in enumerate(indices):
        if native:
            directory='frames' if name=='original' else 'reference_frames'
            im=Image.open(OUT/directory/f'F{f:06d}.png').convert('RGB')
        else: im=Image.fromarray(arr[f])
        im=im.crop(crop).resize((width,height),Image.Resampling.LANCZOS)
        x,y=j%cols*width,j//cols*cellh
        board.paste(im,(x,y))
        d.text((x+5,y+height+3),f'{name[:3]} F{f:06d} {rows[f]["time_s"]:07.3f}s',font=font,fill='white')
        if labels: d.text((x+5,y+height+21),labels[j],font=zh,fill='#a9c5e8')
    p=OUT/'sheets'/filename
    board.save(p,quality=94)
    print(str(p),flush=True)
    return p

def export_reference(indices):
    ids=sorted(set(indices))
    pending=[i for i in ids if not (OUT/'reference_frames'/f'F{i:06d}.png').exists()]
    if not pending:return
    directory=OUT/'logs'/'reference_export'
    directory.mkdir(exist_ok=True)
    expr='+'.join(f'eq(n\\,{f})' for f in pending)
    run([FFMPEG,'-hide_banner','-nostdin','-v','warning','-threads','4','-i',OUT/'source/reference.mp4',
         '-vf',f'select={expr}','-vsync','0','-start_number','0','-compression_level','3','-y',
         directory/'S%05d.png'],'reference_selected_native')
    for j,f in enumerate(pending):
        p=directory/f'S{j:05d}.png'
        assert p.exists(),f
        shutil.move(str(p),str(OUT/'reference_frames'/f'F{f:06d}.png'))
    print(f'Exported {len(pending)} exact native reference frames',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('name',choices=['original','reference'])
    p.add_argument('filename')
    p.add_argument('--start',type=float,default=0)
    p.add_argument('--end',type=float,default=10)
    p.add_argument('--step',type=float,default=1)
    p.add_argument('--frames',type=int,nargs='+')
    p.add_argument('--cols',type=int,default=4)
    p.add_argument('--width',type=int,default=384)
    p.add_argument('--crop',type=int,nargs=4)
    p.add_argument('--native',action='store_true')
    a=p.parse_args()
    ts=[r['time_s'] for r in json.loads((OUT/'data'/f'{a.name}_timeline.json').read_text('utf-8'))]
    ids=a.frames or sorted(set(min(bisect.bisect_left(ts,float(t)),len(ts)-1) for t in np.arange(a.start,a.end,a.step)))
    if a.native and a.name=='reference': export_reference(ids)
    sheet(a.name,ids,a.filename,a.cols,a.width,a.crop,native=a.native)
