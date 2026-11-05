from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np
R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-12/v01/whole_imggen_user_delete_remaining_lower_turn_only_tip_v03");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/X01_12_TIPWHOLE_MASK_PREP_v02");im=Image.open(R/"character_imggen_original.png");a=np.array(im)
for name,box in [("viewer_left",[353,258,396,299]),("viewer_right",[439,231,476,271])]:
 x0,y0,x1,y1=box;sc=18
 panel=Image.new("RGB",((x1-x0)*sc+48,(y1-y0)*sc+30),"white");d=ImageDraw.Draw(panel)
 for y in range(y0,y1):
  d.text((0,(y-y0)*sc+31),str(y),fill="black")
  for x in range(x0,x1):
   xy=(48+(x-x0)*sc,30+(y-y0)*sc);d.rectangle([xy,(xy[0]+sc-1,xy[1]+sc-1)],fill=tuple(a[y,x,:3]),outline=(170,130,130))
 for x in range(x0,x1,2):d.text((48+(x-x0)*sc,5),str(x),fill="black")
 panel.save(P/(name+"_PIXEL_COORDS.png"))

