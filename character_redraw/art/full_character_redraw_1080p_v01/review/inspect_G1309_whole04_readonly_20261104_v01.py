from PIL import Image
from pathlib import Path
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-09/v01/whole_imggen_unlit_samegray_returns_preserve_hands_v04'
O=R.parent/'direct_first_api_source1192_flat_originalref_attached_curl_v03'
E=B/'review/SOL_WHOLE_G13_09_UNLIT_RETURNS_20261104_v01_evidence'
E.mkdir(exist_ok=True)
im=Image.open(R/'character_imggen_original.png').convert('RGBA')
regions={'COIL':(665,480,865,835),'HANDS':(340,675,1085,1020),'EDGE_HAND':(835,670,1000,785),'BOTTOM':(80,1225,915,1274),'BOB':(340,170,590,350),'CLOTH':(75,870,330,1075)}
for key,box in regions.items():
 for bg,c in [('WHITE',(255,255,255,255)),('BLACK',(0,0,0,255))]:
  p=E/f'{key}_{bg}_3x.png'
  assert not p.exists(),str(p)
  crop=im.crop(box); canvas=Image.new('RGBA',crop.size,c);canvas.alpha_composite(crop)
  canvas.convert('RGB').resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(p)
old=Image.open(O/'character_api_original.png').convert('RGBA')
crop=old.crop((555,445,710,697)); canvas=Image.new('RGBA',crop.size,'white');canvas.alpha_composite(crop)
canvas.convert('RGB').resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST).save(E/'PREVIOUS_COIL_WHITE_3x.png')
points={'upper_front':(755,580),'upper_front_other':(728,600),'first_return':(784,641),'second_front':(777,684),'second_return':(791,727),'small_front':(796,757),'bob_center':(460,250),'bob_upper':(477,194),'sleeve_left':(100,1023),'sleeve_right':(200,975)}
obs={'raw':str(R/'character_imggen_original.png'),'raw_sha256':hashlib.sha256((R/'character_imggen_original.png').read_bytes()).hexdigest(),'regions':regions,'operation':'Read-only crops of original RGBA, alpha-composite white/black then nearest-neighbour3x; no artwork edited','point_samples_support_only':{k:{'xy':v,'RGBA':im.getpixel(v)}for k,v in points.items()}}
(E/'PROVENANCE.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(obs,ensure_ascii=False))
