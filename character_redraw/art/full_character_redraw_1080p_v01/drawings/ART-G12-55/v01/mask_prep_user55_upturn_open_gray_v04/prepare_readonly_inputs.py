from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,shutil

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01');C=B/'drawings/ART-G12-55/v01'
P=C/'whole_imggen_reviewed54_source1058_perspective_occlusion_v03';R=Path(__file__).resolve().parent
I=R/'inputs';Q=R/'readonly_QA';I.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
target=P/'character_imggen_original.png';assert sha(target)=='71dca7e1c84330c3543cbed29b4222702e2759c102bc4540fd43f018c8e61d8e'
assert Image.open(target).size==(1103,1426)
copy_specs=[(target,'ref1_CURRENT55_RAW_KEEP_LOW_LEFT_ROOT_CAP_HANDS_BODY.png'),(C/'inputs/source_pose_guide.png','ref2_ORIGINAL1058_COMPLETE_UNMASKED_GUIDE_ACTION_ONLY.png'),(B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png','ref4_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png')]
e=[]
for s,n in copy_specs:
 dst=I/n;assert not dst.exists();shutil.copyfile(s,dst);e.append({**ev(dst),'source':ev(s)})
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
dp=I/'ref3_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png';assert not dp.exists();Image.open(detail).crop([35,58,146,260]).save(dp)
e.append({**ev(dp),'source':ev(detail),'source_crop_xyxy':[35,58,146,260]})
motions=[]
for f,box in [(1054,[394,186,592,416]),(1058,[412,212,643,382])]:
 src=B/f'coverage/source_frames/F{f:06d}.png';dst=I/f'MOTION_SOURCE_F{f}_NEAR_RED_COIL_ONLY.png'
 assert not dst.exists();Image.open(src).crop(box).save(dst);motions.append({**ev(dst),'source':ev(src),'source_crop_xyxy':box,'role':'visible original red coil axis/secondary-motion phase only; no new identity/root/side/material/body authority'})
board=Image.new('RGB',(520,274),'white');bd=ImageDraw.Draw(board)
for x,f,rec in [(12,1054,motions[0]),(270,1058,motions[1])]:
 im=Image.open(rec['path']).convert('RGB');board.paste(im,(x,32));bd.text((x,8),f'F{f} ORIGINAL NEAR CURL',fill='black')
bp=I/'ref5_ORIGINAL1054_TO_1058_CURL_MOTION_ONLY_COMPARISON.png';assert not bp.exists();board.save(bp)
e.append({**ev(bp),'source_crops':motions,'role':'earlier54 axis downward -> current55 near-horizontal/slightly upward; qualitative phase only, no anatomical root/identity/gray topology or mirrored new body'})
white=Image.open(P/'qa_white.png')
white.crop([620,450,850,730]).save(Q/'CURRENT55_ROOT_VISIBLE_COIL_1x_white.png')
white.crop([620,450,850,730]).resize((690,840),Image.Resampling.NEAREST).save(Q/'CURRENT55_ROOT_VISIBLE_COIL_3x_white.png')
grid=white.crop([620,450,850,730]).convert('RGB');g=ImageDraw.Draw(grid)
for x in range(620,851,20):g.line([(x-620,0),(x-620,279)],fill=(80,160,255),width=1);g.text((x-620+1,2),str(x),fill=(255,0,0))
for y in range(460,731,20):g.line([(0,y-450),(229,y-450)],fill=(80,160,255),width=1);g.text((1,y-450+1),str(y),fill=(255,0,0))
grid.resize((690,840),Image.Resampling.NEAREST).save(Q/'CURRENT55_ROOT_COIL_COORDINATE_GRID_3x_READONLY.png')
save(R/'READONLY_INPUT_PROVENANCE_v01.json',{'id':'ART-G12-55','created_utc':datetime.now(timezone.utc).isoformat(),'state':'MASK_PREP_ONLY_NOT_RELEASED','inputs':e,'motions':motions,'raw_art_modified':False,'API_calls':0,'native_calls':0,'attempt_written':False,'18_not_accessed':True,'central_write':False,'quota_resets':0})
print(json.dumps({'run':str(R),'target':ev(target),'inputs':[{k:v for k,v in x.items() if k in ['path','sha256','size']} for x in e]},ensure_ascii=False,indent=2))
