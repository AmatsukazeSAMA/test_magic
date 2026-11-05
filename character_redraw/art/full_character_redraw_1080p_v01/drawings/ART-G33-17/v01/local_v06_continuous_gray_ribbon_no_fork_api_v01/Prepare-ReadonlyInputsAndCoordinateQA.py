from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, shutil

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
RUN=Path(__file__).resolve().parent
CUR=B/'drawings/ART-G33-17/v01/whole_imggen_source2374_openeyes_bobonly_20v06_frontshoulder_v06'
INPUTS=RUN/'inputs'
INPUTS.mkdir(exist_ok=True)
refs=[
 (CUR/'character_imggen_original.png','ref1_KNOWN_V06_194be4c4_COMPLETE_RGBA_TARGET.png','194be4c44f1c4e61991b62230a2140795f78c25368fec78ed4c007846f6984ed'),
 (B/'drawings/ART-G33-17/v01/inputs/source_pose_guide.png','ref2_ORIGINAL2374_COMPLETE_UNMASKED_ACTION_GUIDE.png','ccabdaf57ec5ff9b3bab5963c41da69c58491e3614791910a685cc13d7b14eea'),
 (B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref3_USER_APPROVED11_COMPLETE_SPIRAL_TAPER_C_GEOMETRY_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'),
 (CUR/'inputs/ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png','ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751')]
for src,name,h in refs:
 assert hashlib.sha256(src.read_bytes()).hexdigest()==h, str(src)
 dst=INPUTS/name
 assert not dst.exists(),str(dst)
 shutil.copyfile(src,dst)
 assert dst.read_bytes()==src.read_bytes()
im=Image.open(INPUTS/refs[0][1]).convert('RGBA')
roi=(480,330,700,590)
for bg,label in [('white','white'),('black','black')]:
 qa=Image.new('RGBA',im.size,bg);qa.alpha_composite(im)
 crop=qa.crop(roi).convert('RGB').resize((880,1040),Image.Resampling.NEAREST)
 crop.save(RUN/f'PREP_PRIOR_CANDIDATE_194be4c4_COIL_{label}_4x.png')
 grid=crop.copy(); d=ImageDraw.Draw(grid)
 for x in range(480,701,10):
  xx=(x-480)*4
  d.line((xx,0,xx,1040),fill=(80,130,250),width=1)
  d.text((xx+1,2),str(x),fill=(200,40,10),stroke_width=0)
 for y in range(330,591,10):
  yy=(y-330)*4
  d.line((0,yy,880,yy),fill=(80,130,250),width=1)
  d.text((1,yy+1),str(y),fill=(200,40,10),stroke_width=0)
 grid.save(RUN/f'PREP_PRIOR_CANDIDATE_194be4c4_COIL_COORDINATES_{label}_4x_QA_ONLY.png')
print(json.dumps({'run':str(RUN),'refs_copied_unchanged':4,'source_sha256':refs[0][2],'ROI_xyxy':roi,'API_calls':0,'native_calls':0,'art_pixels_modified':False},ensure_ascii=False))
