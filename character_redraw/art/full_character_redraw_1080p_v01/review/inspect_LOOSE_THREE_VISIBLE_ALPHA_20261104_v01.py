from pathlib import Path
from PIL import Image
import hashlib,json
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
E=B/'review/SOL_LOOSE_THREE_VISIBLE_ALPHA_20261104_v01_evidence';E.mkdir(exist_ok=True)
cases=[('G28','ART-G28-01','api_user_original_loose_graymint_visible_alpha_v02',(280,435,745,866),{'box':(500,600),'outside_raw_glow':(100,700),'eye_black':(440,360)}),('G29','ART-G29-01','api_user_original_loose_graymint_visible_alpha_v05',(180,660,875,982),{'box':(500,850),'outside_raw_glow':(30,500),'eye_black':(425,530)}),('OPT','OPT-BROOCH-PORTRAIT','api_user_own_loose_portrait_redraw_trial_v02',(210,580,845,980),{'outside_raw_glow':(30,800),'eye_fill':(385,705),'mouth_ink':(547,895),'crown_ink':(520,70),'skin':(520,800)})]
items=[]
for label,ident,run,box,pts in cases:
 raw=B/'drawings'/ident/'v01'/run/'character_api_original.png';im=Image.open(raw).convert('RGBA');crop=im.crop(box);panel=Image.new('RGB',(crop.width*3,crop.height))
 for i,color in enumerate(['white','black']):
  bg=Image.new('RGBA',crop.size,color);bg.alpha_composite(crop);panel.paste(bg.convert('RGB'),(i*crop.width,0))
 panel.paste(crop.getchannel('A').convert('RGB'),(2*crop.width,0))
 path=E/f'{label}_WHITE_BLACK_ALPHA_READONLY.png';assert not path.exists();panel.save(path)
 items.append({'id':ident,'raw':str(raw),'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'box':box,'diagnostic':str(path),'supporting_points':{k:{'xy':xy,'RGBA':im.getpixel(xy)}for k,xy in pts.items()}})
(E/'PROVENANCE.json').write_text(json.dumps({'operation':'Readonly crop and exact alpha composite white/black with grayscale alpha column; no threshold/cleanup/recolor/warp','columns':['WHITE','BLACK','ALPHA'],'cases':items},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(str(E))
