from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-X01-14/v01/direct_first_api_source4078_noThreeView_flatBob_totalTurnBudget_postPassEye_v16");D=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_FIRST_X01_14_NO_THREEVIEW_20261104_v16");D.mkdir(parents=True,exist_ok=True)
raw=R/"character_api_original.png";im=Image.open(raw);assert im.mode=="RGBA"
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
outs=[]
for label,color in [("white","white"),("black","black")]:
 c=Image.new("RGBA",im.size,color);c.alpha_composite(im);c=c.convert("RGB");p=D/("CURRENT_full_"+label+".png");c.save(p);outs.append({"path":str(p),"sha256":sha(p)})
 for name,box,sc in [("head_root_coil",[182,100,448,337],3),("lower_coil",[343,205,442,330],5),("hands",[90,32,612,449],1)]:
  cp=D/(name+"_"+label+f"_{sc}x.png");c.crop(box).resize(((box[2]-box[0])*sc,(box[3]-box[1])*sc),Image.Resampling.NEAREST).save(cp);outs.append({"path":str(cp),"sha256":sha(cp),"source_roi":box,"scale":sc})
guide=B/"drawings/ART-X01-14/v01/inputs/source_pose_guide.png"
g=Image.open(guide);g.crop((113,128,451,460)).resize((676,664),Image.Resampling.NEAREST).save(D/"OWN_GUIDE_HEAD_HANDS_2x.png")
a=np.array(im)
report={"raw":{"path":str(raw),"sha256":sha(raw)},"dimensions":list(im.size),"actual_raw_alpha_minmax":[int(a[:,:,3].min()),int(a[:,:,3].max())],"readonly_composites_only":True,"source_pixels_unchanged":True,"outputs":outs,"no_artwork_edited":True}
(D/"DIAGNOSTIC.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(report,ensure_ascii=False))

