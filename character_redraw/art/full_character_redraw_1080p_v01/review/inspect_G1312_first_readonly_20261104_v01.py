from PIL import Image
from pathlib import Path
import hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-12/v01/direct_first_api_source1200_flat_originalref_attached_curl_v03'
E=B/'review/SOL_FIRST_G13_12_SINGLE_UNLIT_GRAY_20261104_v01_evidence'
E.mkdir(exist_ok=True)
im=Image.open(R/'character_api_original.png').convert('RGBA')
boxes={'COIL':(550,420,712,700),'EYES':(325,335,590,430),'HANDS':(290,570,880,860)}
for k,box in boxes.items():
 crop=im.crop(box)
 for b,c in [('WHITE','white'),('BLACK','black')]:
  p=E/f'{k}_{b}_3x.png';assert not p.exists()
  bg=Image.new('RGBA',crop.size,c);bg.alpha_composite(crop)
  bg.convert('RGB').resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(p)
(E/'PROVENANCE.json').write_text(json.dumps({'raw':str(R/'character_api_original.png'),'raw_sha256':hashlib.sha256((R/'character_api_original.png').read_bytes()).hexdigest(),'boxes':boxes,'operation':'Readonly crop, alpha composite white/black then nearest3x; no artwork edit'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(str(E))
