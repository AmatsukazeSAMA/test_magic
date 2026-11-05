from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import hashlib

R=Path(__file__).resolve().parent
m=json.loads((R/'READONLY_INPUTS_AND_QA_MANIFEST.json').read_text(encoding='utf-8'))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',23)
small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
labels=['54 低位 / low','55 从本态开始上 / upswing starts','56 继续外上 / out-up','57 下摆 / downswing','58 抬回 / rebound','59 外水平 / horizontal','60 下收 / down-retract','33-57 转正/双掌展开','33-58 更正面/不同双掌','63 肩前 / front shoulder']
out=[]
for part in range(2):
    board=Image.new('RGB',(1096,1800),(247,247,245));d=ImageDraw.Draw(board)
    d.text((24,12),f'F1053..1097 原PV / 实时绑定1080层 — 静态序列 {part+1}/2',font=font,fill=(25,30,35))
    for j,row in enumerate(m['states'][part*5:(part+1)*5]):
        y=62+j*338;label=labels[part*5+j]
        d.text((24,y),f'原 F{row["first_frame"]} · {label}',font=small,fill=(25,30,35))
        d.text((560,y),f'当前 F{row["first_frame"]} · {label}',font=small,fill=(25,30,35))
        with Image.open(row['actual_source_first_full']['path']) as im:source=im.convert('RGB')
        with Image.open(row['exact_current_bound_layer']['path']) as im:rgba=im.convert('RGBA')
        bg=Image.new('RGBA',rgba.size,(211,166,168,255));bg.alpha_composite(rgba)
        board.paste(source.resize((512,288),Image.Resampling.LANCZOS),(24,y+28))
        board.paste(bg.convert('RGB').resize((512,288),Image.Resampling.LANCZOS),(560,y+28))
    d.text((24,1760),'仅静态：未播放，不认证动态/物理跳跃/隐藏拓扑。所有缩略整幅等比，未移动任何人物部件。',font=small,fill=(80,85,90))
    p=R/f'FRESH_SOURCE_VS_BOUND_SEQUENCE_{part+1:02d}.png';assert not p.exists();board.save(p)
    out.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(board.size)})
p=R/'FRESH_SEQUENCE_BOARD_OUTPUTS.json';assert not p.exists()
p.write_text(json.dumps({'boards':out,'basis':'New live bound layer snapshot + each own source first exposure; no old actual-view claims inherited.','calls':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
