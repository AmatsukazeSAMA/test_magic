from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
B=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01");R=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/whole_imggen_lower_root_own_shoulder_front_v01");V=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01");O=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16");D=Path(r"D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/SOL_WHOLE_G33_48_LOW_ROOT_SHOULDER_FRONT_20261104_v01");D.mkdir(parents=True,exist_ok=True)
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
src=R/"character_imggen_original.png";assert sha(src)=="556550bc741a8d09d013bc12a2d63b93c465ca7a510b5ae8c0d69ea31ae92679"
im=Image.open(R/"qa_white.png");sz=im.size;s=624/sz[0];target=(624,1072)
new=Image.new("RGB",target,"white");part=im.resize((624,round(sz[1]*s)),Image.Resampling.BICUBIC);new.paste(part,(0,0));new.save(D/"NEW_WHOLE_UNIFORM_624x1072_READONLY.png")
for label in ["white","black"]:
 pic=Image.open(R/("qa_"+label+".png"))
 for name,roi,sc in [("root_shoulder_occlusion",[430,340,698,620],3),("eyes_actual_closed",[422,263,630,329],5)]:
  p=D/(name+"_"+label+f"_{sc}x.png");crop=pic.crop(roi);crop.resize((crop.width*sc,crop.height*sc),Image.Resampling.NEAREST).save(p)
g=Image.open(V/"inputs/source_pose_guide.png").convert("RGB");o=Image.open(O/"qa_white.png").convert("RGB")
panel=Image.new("RGB",(624*3+20,1098),"#ddd");dr=ImageDraw.Draw(panel)
for i,(pic,title) in enumerate([(g,"OWN F2513 guide"),(o,"FIRST history (not current)"),(new,"NEW WHOLE uniform only")]):
 panel.paste(pic,(i*634,26));dr.text((i*634+4,5),title,fill="black")
panel.save(D/"SOURCE_FIRST_CURRENT_UNIFORM_READONLY.png")
(D/"DIAGNOSTIC.json").write_text(json.dumps({"readonly":True,"parent":{"path":str(src),"sha256":sha(src)},"uniform_only":{"scale":s,"translation":[0,0],"no_rotation_shear_or_localwarp":True,"production_placement_approved":False},"source":{"path":str(V/"inputs/source_pose_guide.png"),"sha256":sha(V/"inputs/source_pose_guide.png")},"originals_unchanged":True},ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({"uniform_scale":s,"diagnostic":str(D)},ensure_ascii=False))

