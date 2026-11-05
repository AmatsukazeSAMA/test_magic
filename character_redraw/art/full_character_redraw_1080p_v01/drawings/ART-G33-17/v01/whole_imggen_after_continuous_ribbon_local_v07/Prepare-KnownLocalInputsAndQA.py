from pathlib import Path
from PIL import Image
import json, hashlib, shutil
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
RUN=Path(__file__).resolve().parent
LOCAL=B/'drawings/ART-G33-17/v01/local_v06_continuous_gray_ribbon_no_fork_api_v01'
inputs=RUN/'inputs';inputs.mkdir(exist_ok=True)
refs=[(LOCAL/'character_api_original.png','ref1_KNOWN_LOCAL_7ac2b5ab_COMPLETE_RGBA_TARGET.png','7ac2b5ab14558eaa8714e8890b80a43129e175d358fcde1fc3fd48b3018748c1'),(LOCAL/'inputs/ref2_ORIGINAL2374_COMPLETE_UNMASKED_ACTION_GUIDE.png','ref2_ORIGINAL2374_COMPLETE_UNMASKED_ACTION_GUIDE.png','ccabdaf57ec5ff9b3bab5963c41da69c58491e3614791910a685cc13d7b14eea'),(LOCAL/'inputs/ref3_USER_APPROVED11_COMPLETE_SPIRAL_TAPER_C_GEOMETRY_ONLY.png','ref3_USER_APPROVED11_COMPLETE_SPIRAL_TAPER_C_GEOMETRY_ONLY.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'),(LOCAL/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751')]
for src,name,h in refs:
 assert hashlib.sha256(src.read_bytes()).hexdigest()==h
 dst=inputs/name;assert not dst.exists();shutil.copyfile(src,dst)
im=Image.open(inputs/refs[0][1]).convert('RGBA');assert im.size==(960,1648)
roi=(475,325,675,580)
for bg in ['white','black']:
 qa=Image.new('RGBA',im.size,bg);qa.alpha_composite(im)
 qa.convert('RGB').save(RUN/f'PREP_PRIOR_LOCAL_7ac2b5ab_FULL_{bg}.png')
 crop=qa.crop(roi).convert('RGB')
 crop.save(RUN/f'PREP_PRIOR_LOCAL_7ac2b5ab_COIL_{bg}_1x.png')
 crop.resize((800,1020),Image.Resampling.NEAREST).save(RUN/f'PREP_PRIOR_LOCAL_7ac2b5ab_COIL_{bg}_4x.png')
im.crop(roi).getchannel('A').resize((800,1020),Image.Resampling.NEAREST).save(RUN/'PREP_PRIOR_LOCAL_7ac2b5ab_COIL_ALPHA_4x.png')
(RUN/'PREP_DIAGNOSTIC_SOURCE.json').write_text(json.dumps({'source_image':str(inputs/refs[0][1]),'source_sha256':refs[0][2],'prepared_before_future_return':True,'ROI_xyxy':roi,'art_pixels_modified':False,'calls':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'run':str(RUN),'input_size':im.size,'refs':4,'calls':0},ensure_ascii=False))
