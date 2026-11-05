from pathlib import Path
from PIL import Image
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-13/v01/direct_first_api_source1211_samegray_return_material_factor_v04'
E=B/'review/SOL_FIRST_G13_13_SAMEGRAY_MATERIAL_FACTOR_20261104_v01_evidence';E.mkdir(exist_ok=True)
im=Image.open(R/'character_api_original.png').convert('RGBA')
boxes={'COIL_C':(570,425,748,720),'OUTSIDE_LEFT':(210,770,350,950),'NECK_GAP':(245,430,445,540),'OUTSIDE_HAND':(985,875,1136,1040)}
for k,box in boxes.items():
 crop=im.crop(box);panel=Image.new('RGB',(crop.width*3,crop.height))
 for i,c in enumerate(['white','black']):
  bg=Image.new('RGBA',crop.size,c);bg.alpha_composite(crop);panel.paste(bg.convert('RGB'),(i*crop.width,0))
 panel.paste(crop.getchannel('A').convert('RGB'),(2*crop.width,0))
 p=E/f'{k}_WHITE_BLACK_ALPHA_3x.png';assert not p.exists();panel.resize((panel.width*3,panel.height*3),Image.Resampling.NEAREST).save(p)
points={'neck_gap_visible_fog':(350,498),'left_arm_body_gap_visible_fog':(275,850),'outside_right_hand_block':(1120,1020),'outside_right_hand_haze':(1080,940),'hidden_background_control':(50,50)}
proof={'raw':str(R/'character_api_original.png'),'raw_sha256':hashlib.sha256((R/'character_api_original.png').read_bytes()).hexdigest(),'boxes':boxes,'panel_columns':['original_alpha_over_white','original_alpha_over_black','original_alpha_channel_grayscale'],'operation':'Readonly exact crops/composites plus nearest3x; no alpha threshold, cleanup, recolor or artwork change','supporting_points':{k:{'xy':list(xy),'RGBA':list(im.getpixel(xy))}for k,xy in points.items()}}
(E/'PROVENANCE.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(proof['supporting_points'],ensure_ascii=False,indent=2))
