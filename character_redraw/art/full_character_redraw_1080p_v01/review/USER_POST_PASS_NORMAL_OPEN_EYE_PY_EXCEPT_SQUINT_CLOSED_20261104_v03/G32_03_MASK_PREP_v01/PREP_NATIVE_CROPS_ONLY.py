from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-03/v01/whole_imggen_user_twoLarge_trueSmall_C_v01");P=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/G32_03_MASK_PREP_v01");P.mkdir(parents=True,exist_ok=True)
src=R/"character_imggen_original.png";assert hashlib.sha256(src.read_bytes()).hexdigest()=="794a386eec8c6e4cc1ffaf1f38f6997c43eef03ecec0d14ea84c198f2b5552d8"
im=Image.open(src);w=Image.new("RGBA",im.size,"white");w.alpha_composite(im)
rois={"back_viewer_left":[165,325,274,475],"back_viewer_right_partial":[397,388,477,534],"middle_viewer_left":[579,325,686,479],"middle_viewer_right_partial":[835,399,950,547],"front_closed_exempt":[1025,350,1510,548]}
for n,box in rois.items():
 part=w.convert("RGB").crop(box);part.save(P/(n+"_ORIGINAL_native_1x.png"))
 sc=8 if "closed" not in n else 2
 part.resize((part.width*sc,part.height*sc),Image.Resampling.NEAREST).save(P/(n+f"_ORIGINAL_{sc}x.png"))
(P/"NATIVE_ROIS_PREP.json").write_text(json.dumps({"source":str(src),"source_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"rois":rois},indent=2)+"\n",encoding="utf8")
print(json.dumps(rois))

