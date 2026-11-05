from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-14/v01/direct_first_api_source1246_latest_grayeye_samegray_return_v05'
E=B/'review/SOL_FIRST_G13_14_GRAYEYE_SAMEGRAY_20261104_v01_evidence'
E.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
raw=Image.open(R/'character_api_original.png').convert('RGBA')
white=Image.open(R/'qa_white.png').convert('RGB')
black=Image.open(R/'qa_black.png').convert('RGB')
guide=B/'drawings/ART-G13-14/v01/inputs/source_pose_guide.png'
src=Image.open(guide).convert('RGB')
records=[]
def board(name, parts):
    prepared=[]
    for im,box,label in parts:
        crop=im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3),Image.Resampling.NEAREST)
        prepared.append((crop,label,box))
    out=Image.new('RGB',(sum(i.width for i,_,_ in prepared),max(i.height for i,_,_ in prepared)+28),(225,225,225))
    d=ImageDraw.Draw(out);x=0
    for crop,label,box in prepared:
        out.paste(crop,(x,28));d.text((x+4,6),f'{label} {box}',fill=(0,0,0));x+=crop.width
    p=E/name
    if p.exists(): raise RuntimeError(f'preserve existing {p}')
    out.save(p)
    records.append({'path':str(p),'sha256':sha(p),'parts':[{'label':label,'bbox':list(box),'scale':3} for _,label,box in prepared]})
board('EYES_SOURCE_NEW_WHITE_3x.png',[(src,(350,295,615,435),'OWN WIDER GUIDE'),(white,(325,270,610,430),'NEW WHITE')])
board('HANDS_SOURCE_NEW_WHITE_3x.png',[(src,(270,515,720,790),'OWN WIDER GUIDE'),(white,(265,520,725,770),'NEW WHITE')])
board('COIL_WHITE_BLACK_ALPHA_3x.png',[(white,(575,360,750,690),'NEW WHITE'),(black,(575,360,750,690),'NEW BLACK'),(raw.getchannel('A').convert('RGB'),(575,360,750,690),'ACTUAL ALPHA')])
pts=[(100,500),(800,300),(780,900),(300,850),(500,805),(335,250),(445,250),(600,460),(650,485),(655,535)]
samples=[{'xy':list(p),'rgba':list(raw.getpixel(p))} for p in pts]
provenance={'operation':'read-only crops and 3x nearest-neighbor viewing, no art modifications','raw':{'path':str(R/'character_api_original.png'),'sha256':sha(R/'character_api_original.png')},'guide':{'path':str(guide),'sha256':sha(guide)},'generated':records,'rgba_samples_support_only':samples}
p=E/'PROVENANCE.json'
if p.exists(): raise RuntimeError('preserve existing provenance')
p.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'qa':records,'samples':samples},ensure_ascii=False,indent=2))
