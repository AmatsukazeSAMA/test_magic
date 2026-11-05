from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-29/v01/direct_first_api_canonical1324_wider3766_fourRefs_noShoulderCrop_postPassEye_v16");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G13_29_MASK_PREP_v01");a=np.array(Image.open(R/"character_api_original.png"))
for name,box in [("viewer_left_upper",[296,276,343,298]),("viewer_right_upper",[435,327,483,350])]:
 x0,y0,x1,y1=box;sc=16
 out=Image.new("RGB",((x1-x0)*sc+48,(y1-y0)*sc+28),"white");d=ImageDraw.Draw(out)
 for y in range(y0,y1):
  d.text((0,(y-y0)*sc+29),str(y),fill="black")
  for x in range(x0,x1):
   ax=48+(x-x0)*sc;ay=28+(y-y0)*sc;d.rectangle([ax,ay,ax+sc-1,ay+sc-1],fill=tuple(a[y,x,:3]),outline=(170,120,120))
 for x in range(x0,x1,3):d.text((48+(x-x0)*sc,5),str(x),fill="black")
 out.save(P/(name+"_PIXEL_GRID.png"))

