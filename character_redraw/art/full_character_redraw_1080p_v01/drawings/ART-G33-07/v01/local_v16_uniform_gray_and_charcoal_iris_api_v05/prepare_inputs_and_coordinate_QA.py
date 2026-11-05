from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime,timezone
RUN=Path(__file__).parent;B=RUN.parents[3]
PRIOR=RUN.parent/'whole_imggen_after_gray_material_restore_mint_returns_v16'
I=RUN/'inputs';I.mkdir(exist_ok=True,parents=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def meta(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
def outjson(name,o):
 p=RUN/name
 if p.exists():raise RuntimeError('preserve '+str(p))
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cp(src,name):
 dst=I/name
 if dst.exists():raise RuntimeError('preserve '+str(dst))
 shutil.copyfile(src,dst);assert sha(src)==sha(dst)
 return dst
target=PRIOR/'character_imggen_original.png'
assert sha(target)=='194d01e113fb275957c254789857abaf5e8bf25afe2313f900a32f7ce10cac92'
refs=[cp(target,'ref1_CURRENT_V16_194d01e1_COMPLETE_RGBA_TARGET.png')]
gray=I/'ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2.png';Image.new('RGB',(192,128),(182,180,178)).save(gray);refs.append(gray)
g02=B/'inputs/eye_G02-01_F100.png'
g02xy=[450,78,510,104]
g02out=I/'ref3_G02_IRIS_INTERIOR_PIGMENT_ONLY_NO_LID_GLINT.png'
with Image.open(g02) as im:im.crop(tuple(g02xy)).save(g02out)
refs.append(g02out)
guide=B/'drawings/ART-G33-07/v01/local_upper_connected_gray_envelope_api_v02/inputs/ref4_ORIGINAL2333_COMPLETE_UNMASKED_ACTION_GUIDE.png'
sourceeyesxy=[278,188,396,233]
sourceeyes=I/'ref4_ORIGINAL2333_OWN_ROUND_EYES_APERTURE_ONLY.png'
with Image.open(guide) as im:im.crop(tuple(sourceeyesxy)).save(sourceeyes)
refs.append(sourceeyes)
full=cp(guide,'SOURCE2333_COMPLETE_UNMASKED_GUIDE_FOR_FUTURE_WHOLE_NOT_API_REF.png')
font=ImageFont.load_default()
grids=[]
for tag,xy,scale,step in [
 ('EYE_VIEWER_LEFT',[425,230,484,291],10,5),
 ('EYE_VIEWER_RIGHT',[529,222,585,284],10,5),
 ('COIL',[600,305,860,510],5,10)]:
 with Image.open(PRIOR/'qa_white.png') as im:
  tile=im.crop(tuple(xy)).resize(((xy[2]-xy[0])*scale,(xy[3]-xy[1])*scale),Image.Resampling.NEAREST).convert('RGB')
 d=ImageDraw.Draw(tile)
 for x in range(((xy[0]+step-1)//step)*step,xy[2],step):
  px=(x-xy[0])*scale;d.line([(px,0),(px,tile.height)],fill=(180,95,200),width=1);d.text((px+1,0),str(x),fill=(220,0,0),font=font)
 for y in range(((xy[1]+step-1)//step)*step,xy[3],step):
  py=(y-xy[1])*scale;d.line([(0,py),(tile.width,py)],fill=(180,95,200),width=1);d.text((0,py+1),str(y),fill=(220,0,0),font=font)
 p=RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_{tag}_COORDINATE_GRID_{scale}x.png';tile.save(p)
 grids.append({'file':meta(p),'source_image':str(PRIOR/'qa_white.png'),'source_sha256':sha(PRIOR/'qa_white.png'),'raw_source_image':str(target),'raw_source_sha256':sha(target),'crop_xyxy':xy,'scale':scale,'prepared_before_future_return':True,'QA_only_not_art_or_API_ref':True})
outjson('INPUT_PROVENANCE_INITIAL_PREPONLY.json',{'id':'ART-G33-07','target':meta(target),'refs':[meta(p) for p in refs],
 'G02_source':meta(g02),'G02_crop_xyxy':g02xy,'G02_role':'iris pigment only no eyelid/aperture/glint geometry',
 'own_source':meta(guide),'own_source_eye_crop_xyxy':sourceeyesxy,'own_eye_role':'2333 round aperture/gaze only; not source red identity',
 'future_whole_source':meta(full),'diagnostics':grids,
 'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'final_art_pixel_changes':False,
 'prepared_utc':datetime.now(timezone.utc).isoformat()})
print(json.dumps({'run':str(RUN),'refs':[meta(p) for p in refs],'grids':[g['file'] for g in grids]},ensure_ascii=False,indent=2))
