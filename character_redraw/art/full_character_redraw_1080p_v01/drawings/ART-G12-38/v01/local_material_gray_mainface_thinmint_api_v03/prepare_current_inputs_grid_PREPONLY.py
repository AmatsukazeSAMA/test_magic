from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageFont
RUN=Path(__file__).parent;B=RUN.parents[3];PRIOR=RUN.parent/'whole_imggen_source963_connectedgray_occlusion_v02';I=RUN/'inputs';I.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def meta(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 return d
target=PRIOR/'character_imggen_original.png'
assert sha(target)=='4785609114b9b57113db98decde0f12909d077b79faf09799221db6ad61c7aa5'
ref1=I/'ref1_CURRENT38_V02_47856091_COMPLETE_RGBA_TARGET.png';shutil.copyfile(target,ref1)
ref2=I/'ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2.png';Image.new('RGB',(192,128),(182,180,178)).save(ref2)
src=PRIOR/'inputs/ref1_ORIGINAL963_COMPLETE_UNMASKED_POSE_GUIDE.png';source=I/'SOURCE963_COMPLETE_UNMASKED_GUIDE_FUTURE_WHOLE_NOT_API_REF.png';shutil.copyfile(src,source)
xy=[548,405,700,600];scale=8
with Image.open(PRIOR/'qa_white.png') as im:tile=im.crop(tuple(xy)).resize(((xy[2]-xy[0])*scale,(xy[3]-xy[1])*scale),Image.Resampling.NEAREST).convert('RGB')
d=ImageDraw.Draw(tile);font=ImageFont.load_default()
for x in range(550,700,10):
 px=(x-xy[0])*scale;d.line([(px,0),(px,tile.height)],fill=(210,100,190));d.text((px+2,0),str(x),fill=(210,0,0),font=font)
for y in range(410,600,10):
 py=(y-xy[1])*scale;d.line([(0,py),(tile.width,py)],fill=(210,100,190));d.text((0,py+1),str(y),fill=(210,0,0),font=font)
gp=RUN/'PREP_PRIOR_CANDIDATE_47856091_COIL_MATERIAL_COORDINATE_GRID_8x.png';tile.save(gp)
pro={'id':'ART-G12-38','refs':[meta(ref1),meta(ref2)],'source_current':meta(target),'source_guide':meta(src),'future_whole_source':meta(source),
 'reference_roles':['current coherent exact full character; only wide upper front and lowerC wrongly mint instead of gray; identity geometry action retained','pure unlit gray pigment only no spatial palette/shape'],
 'excluded_refs':['old mint bigC or green mainface crop','glossy user detail','full other-state headcoil','AIbody','extra G02 eye crop'],
 'readonly_grid':{**meta(gp),'source_image':str(PRIOR/'qa_white.png'),'source_sha256':sha(PRIOR/'qa_white.png'),'raw_source_image':str(target),'raw_source_sha256':sha(target),'crop_xyxy':xy,'scale':scale,'prepared_before_future_return':True,'not_art_or_API_ref':True},
 'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'target_art_pixel_changes':False}
(RUN/'INPUT_PROVENANCE_PREPONLY.json').write_text(json.dumps(pro,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(pro,ensure_ascii=False,indent=2))
