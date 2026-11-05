from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,shutil
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01');RUN=Path(__file__).resolve().parent
OLD=B/'drawings/ART-G12-55/v01/whole_imggen_after_upturn_gray_mask_v05'
I=RUN/'inputs';I.mkdir(exist_ok=True)
refs=[(OLD/'character_imggen_original.png','ref1_KNOWN_V05_fde9e95a_COMPLETE_RGBA_TARGET.png','fde9e95ad9c4c78372525f345c4c358e375f78c788254f6b22dcfdd92e77eef1'),(B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png','ref2_USER_ROMAN_DETAIL_GEOMETRY_ONLY_NOT_LIGHTING.png','4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'),(B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref3_APPROVED11_COMPLETE_SPIRAL_TAPER_C_GEOMETRY_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'),(B/'drawings/ART-G33-17/v01/local_v06_continuous_gray_ribbon_no_fork_api_v01/inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751')]
for src,name,h in refs:
 assert hashlib.sha256(src.read_bytes()).hexdigest()==h
 dst=I/name;assert not dst.exists();shutil.copyfile(src,dst)
im=Image.open(I/refs[0][1]).convert('RGBA');assert im.size==(1105,1424)
roi=(640,330,960,650)
for bg in ['white','black']:
 full=Image.new('RGBA',im.size,bg);full.alpha_composite(im)
 crop=full.crop(roi).resize((960,960),Image.Resampling.NEAREST).convert('RGB')
 crop.save(RUN/f'PREP_PRIOR_V05_fde9e95a_ROOT_COIL_HAND_{bg}_3x.png')
 grid=crop.copy();d=ImageDraw.Draw(grid)
 for x in range(640,961,10):
  xx=(x-640)*3;d.line((xx,0,xx,960),fill=(70,130,255));d.text((xx+1,2),str(x),fill=(220,30,40))
 for y in range(330,651,10):
  yy=(y-330)*3;d.line((0,yy,960,yy),fill=(70,130,255));d.text((1,yy+2),str(y),fill=(220,30,40))
 grid.save(RUN/f'PREP_PRIOR_V05_fde9e95a_COORDINATES_{bg}_3x_QA_ONLY.png')
print(json.dumps({'run':str(RUN),'refs':4,'input_size':im.size,'ROI':roi,'calls':0},ensure_ascii=False))
