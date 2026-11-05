from PIL import Image
import numpy as np,json
a=np.array(Image.open(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-03/v01/whole_imggen_user_twoLarge_trueSmall_C_v01/character_imggen_original.png"))
for name,box in [("backL",[180,334,262,464]),("backR",[410,404,465,527]),("midL",[591,337,675,471]),("midR",[851,411,938,539])]:
 print(name)
 x0,y0,x1,y1=box
 for y in range(y0,y1,5):
  v=a[y,x0:x1,:3].astype(int);idx=np.where((v.max(1)-v.min(1)<20)&(v.mean(1)<165))[0]+x0
  runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
  print(y,[(int(z[0]),int(z[-1])) for z in runs if len(z)>0])

