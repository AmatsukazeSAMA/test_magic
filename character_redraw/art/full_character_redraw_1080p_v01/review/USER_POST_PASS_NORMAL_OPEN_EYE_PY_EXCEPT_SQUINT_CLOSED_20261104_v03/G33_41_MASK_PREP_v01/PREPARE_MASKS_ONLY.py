from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,hashlib,json,math
BASE=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
OUT=Path(__file__).resolve().parent
SOURCE=BASE/'drawings/ART-G33-41/v01/direct_first_api_source2480_approvedCoil_innerGray_eyeArcNoOutline_v11/character_api_original.png'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
EXPECTED='636b913a402e8619cc352c0af830862a4aca5b5b1aece3a4b923158a201d4aaa'
assert sha(SOURCE)==EXPECTED
original=Image.open(SOURCE);assert original.mode=='RGBA' and original.size==(640,1056)
# Per-row inclusive native-pixel spans manually read from THIS image. No threshold mask inference.
spans={
'viewer_left':{139:(378,382),140:(377,385),141:(376,386),142:(376,387),143:(375,390),144:(375,390),145:(375,390),146:(375,390),147:(375,390),148:(375,390),149:(375,390),150:(375,390),151:(375,390),152:(375,390),153:(375,390),154:(376,390),155:(376,390),156:(376,389),157:(377,389),158:(378,388),159:(379,388),160:(380,388)},
'viewer_right':{147:(438,449),148:(437,452),149:(436,453),150:(436,453),151:(435,453),152:(435,453),153:(435,453),154:(434,453),155:(434,454),156:(434,454),157:(434,454),158:(434,454),159:(434,453),160:(435,453),161:(435,453),162:(435,452),163:(436,452),164:(436,452),165:(437,451),166:(438,450),167:(439,449),168:(439,448),169:(443,446)}}
glint_spans={
'viewer_left':{141:(385,386),142:(385,387),143:(385,387),144:(385,387),145:(385,386)},
'viewer_right':{147:(444,446),148:(444,447),149:(444,447),150:(445,447)}}
items=[];allow=np.zeros((1056,640),bool);protected=allow.copy()
for name in spans:
 m=np.zeros((1056,640),np.uint8);g=m.copy()
 for y,(x0,x1) in spans[name].items():m[y,x0:x1+1]=255
 for y,(x0,x1) in glint_spans[name].items():g[y,x0:x1+1]=255
 m[g>0]=0
 assert not np.any((m>0)&allow)
 assert not np.any((m>0)&(g>0))
 allow|=m>0;protected|=g>0
 mp=OUT/f'{name}_FULL_IRIS_MASK.png';gp=OUT/f'{name}_GLINT_PROTECTION.png';Image.fromarray(m).save(mp);Image.fromarray(g).save(gp)
 items.append({'name':name,'interior_mask':{'path':str(mp),'sha256':sha(mp)},'protected_glint_mask':{'path':str(gp),'sha256':sha(gp)},'allowed_pixels':int((m>0).sum()),'protected_glint_pixels':int((g>0).sum()),'manual_native_row_spans_inclusive':{str(y):list(v) for y,v in spans[name].items()},'glint_native_row_spans_inclusive':{str(y):list(v) for y,v in glint_spans[name].items()}})
white=Image.new('RGBA',original.size,'white');white.alpha_composite(original);white=np.array(white.convert('RGB'))
roi=(350,110,475,185);x0,y0,x1,y1=roi
ov=white.copy();ov[allow]=(255,0,255);ov[protected]=(0,230,255)
for label,a in [('FULL_IRIS_MASK_REVIEW_10x',ov),('SOURCE_EYES_10x',white)]:
 Image.fromarray(a).crop(roi).resize(((x1-x0)*10,(y1-y0)*10),Image.Resampling.NEAREST).save(OUT/f'{label}.png')
# Outline-only cap geometry diagnostic; no recolored preview is made.
geometry={'viewer_left':{'center_xy':[382.5,149.5],'down_unit_xy':[-0.14,math.sqrt(1-0.14**2)],'light_cap':{'center_local_xy':[0,10.5],'radii_xy':[6.3,9.9]},'light_transition_width_px':1.5},'viewer_right':{'center_xy':[443.8,158.0],'down_unit_xy':[-0.14,math.sqrt(1-0.14**2)],'light_cap':{'center_local_xy':[0,11.3],'radii_xy':[7.1,10.5]},'light_transition_width_px':1.5}}
line=Image.fromarray(white.copy());d=ImageDraw.Draw(line)
for name,v in geometry.items():
 cx,cy=v['center_xy'];dx,dy=v['down_unit_xy'];rx,ry=v['light_cap']['radii_xy'];ux,uy=v['light_cap']['center_local_xy'];pts=[]
 for t in np.linspace(0,2*math.pi,241):
  ac=ux+rx*math.cos(t);dn=uy+ry*math.sin(t);x=cx+ac*dy+dn*dx;y=cy-ac*dx+dn*dy
  if (0<=int(y)<1056 and 0<=int(x)<640 and allow[int(y),int(x)]):pts.append((x,y))
  else:
   if len(pts)>1:d.line(pts,fill=(0,190,230),width=1)
   pts=[]
 if len(pts)>1:d.line(pts,fill=(0,190,230),width=1)
line.crop(roi).resize(((x1-x0)*10,(y1-y0)*10),Image.Resampling.NEAREST).save(OUT/'LOWER_CAP_OUTLINE_ONLY_10x.png')
assert sha(SOURCE)==EXPECTED
(OUT/'MASK_PROVENANCE.json').write_text(json.dumps({'input':{'path':str(SOURCE),'sha256':EXPECTED},'dimensions':[640,1056],'mask_items':items,'cap_geometry':geometry,'review_roi_xyxy':list(roi),'overlay_key':'magenta=RGB-authorized iris; cyan=original glint+AA protected; lower-cap image is outline only, no applied RGB.','source_art_bytes_unchanged':True,'color_edit_applied':False,'generation_calls':0,'central_writes':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mask_counts':[{'name':x['name'],'allowed_pixels':x['allowed_pixels'],'glint_pixels':x['protected_glint_pixels']} for x in items],'color_edit_applied':False},ensure_ascii=False))
