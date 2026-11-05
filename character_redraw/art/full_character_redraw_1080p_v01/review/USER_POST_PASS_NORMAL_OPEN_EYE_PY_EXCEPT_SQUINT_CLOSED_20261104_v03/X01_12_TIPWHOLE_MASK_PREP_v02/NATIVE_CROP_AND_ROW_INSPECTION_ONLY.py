from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-12/v01/whole_imggen_user_delete_remaining_lower_turn_only_tip_v03");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_12_TIPWHOLE_MASK_PREP_v02");P.mkdir(parents=True,exist_ok=True)
src=R/"character_imggen_original.png";assert hashlib.sha256(src.read_bytes()).hexdigest()=="b893298201832a346c36fb496714a2a97216f3c1586fa4d094988741c29bc07f"
im=Image.open(src);assert im.mode=="RGBA" and im.size==(956,1645)
white=Image.new("RGBA",im.size,"white");white.alpha_composite(im)
for name,box in [("viewer_left",[344,252,402,306]),("viewer_right",[434,225,485,278])]:
 crop=white.convert("RGB").crop(box);crop.save(P/(name+"_ORIGINAL_native_1x.png"));crop.resize((crop.width*12,crop.height*12),Image.Resampling.NEAREST).save(P/(name+"_ORIGINAL_12x.png"))
a=np.array(im)
for name,box in [("viewer_left",[354,260,399,301]),("viewer_right",[440,233,479,274])]:
 print(name)
 x0,y0,x1,y1=box
 for y in range(y0,y1):
  v=a[y,x0:x1,:3].astype(int);idx=np.where((v.max(1)-v.min(1)<30)&(v.mean(1)<165))[0]+x0
  runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1);print(y,[(int(z[0]),int(z[-1])) for z in runs if len(z)])

