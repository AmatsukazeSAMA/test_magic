from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import hashlib

R=Path(__file__).resolve().parent
manifest=json.loads((R/'READONLY_INPUTS_AND_QA_MANIFEST.json').read_text(encoding='utf-8'))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
def rec(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
out=[]
for row in manifest['states']:
    with Image.open(row['actual_source_first_full']['path']) as im:source=im.convert('RGB')
    with Image.open(row['exact_current_bound_layer']['path']) as im:rgba=im.convert('RGBA')
    current=Image.new('RGBA',rgba.size,'white');current.alpha_composite(rgba);current=current.convert('RGB')
    board=Image.new('RGB',(1920,1350),(243,243,240));d=ImageDraw.Draw(board)
    d.text((12,6),f'{row["id"]} F{row["first_frame"]}..{row["last_frame"]} | SOURCE / EXACT CURRENT BOUND 1080 LAYER',font=font,fill='black')
    d.text((12,42),'Source full uniform0.5',font=small,fill='black')
    d.text((972,42),'Current full white alpha uniform0.5',font=small,fill='black')
    board.paste(source.resize((960,540),Image.Resampling.LANCZOS),(0,68))
    board.paste(current.resize((960,540),Image.Resampling.LANCZOS),(960,68))
    roi=row['diagnostic_same_fixed_canvas_head_ROI']
    d.text((12,611),f'Original same fixed canvas crop {roi} at1x',font=small,fill='black')
    d.text((972,611),'Current same crop1x, no reanchor or part warp',font=small,fill='black')
    board.paste(source.crop(roi),(5,640));board.paste(current.crop(roi),(965,640))
    p=R/f'{row["id"]}_F{row["first_frame"]}_SOURCE_CURRENT_FULL_AND_CONTEXT_v02.png'
    assert not p.exists();board.save(p);out.append({'id':row['id'],'panel':rec(p),'size':[1920,1350],'ROI':roi,'complete_700px_context_no_bottom_clip':True,'previous_v01_panel_preserved':row['panel']})
f=R/'COMPLETE_CONTEXT_PANELS_v02.json';assert not f.exists()
f.write_text(json.dumps({'reason':'QA board canvas extended20px so complete1x fixed context fits. Original v01 panels and manifest preserved; no input asset, binding or pixel-art changes.','panels':out,'generation_calls':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rec(f),ensure_ascii=False))
