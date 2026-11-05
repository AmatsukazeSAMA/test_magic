from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,datetime

P=Path(__file__).resolve().parent
B=P.parents[3]
CEL=P.parent
OLD=CEL/'whole_imggen_source2365_frontshoulder_headcrop_puregray_v06'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (P/'attempt.json').exists()
(P/'inputs').mkdir(exist_ok=True)
items=[
 ('ref1_CURRENT_KNOWN_WHOLEV06_c03c252b_COMPLETE_RGBA_TARGET.png',OLD/'character_imggen_original.png','c03c252b16f6454e20246884d1616d312c93e518c81f105de660f52215ebc5f7','Only complete edit target; current rear-nape bead/coil route is rejected, not a route template.'),
 ('ref2_ORIGINAL2365_COMPLETE_UNMASKED_ACTION_GUIDE.png',OLD/'inputs/ref1_ORIGINAL2365_COMPLETE_UNMASKED_POSE_GUIDE.png','0d3a358c1df91c5a9edcc00e9964163be86deea8021bb159fb344dfa4565543c','Sole original action/head-turn/body/costume/occlusion/leg/shoe/crop authority; do not copy red hair identity/high roots.'),
 ('ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png',OLD/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751','Only flat gray pigment, no spatial or geometric template.')]
records=[]
for name,source,expected,role in items:
 assert sha(source)==expected,(source,sha(source))
 dest=P/'inputs'/name
 if dest.exists(): assert sha(dest)==expected
 else: shutil.copyfile(source,dest)
 records.append(dict(path=str(dest),source_path=str(source),sha256=expected,source_sha256=expected,dimensions=Image.open(dest).size,role=role))
raw=Image.open(records[0]['path']).convert('RGBA')
assert raw.size==(957,1644)
roi=(375,275,715,605)
qa=[]
for bgname,color in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 comp=Image.alpha_composite(Image.new('RGBA',raw.size,color),raw).convert('RGB')
 out=P/f'PREP_PRIOR_CANDIDATE_c03c252b_FULL_{bgname}.png';comp.save(out);qa.append(dict(path=str(out),sha256=sha(out)))
 crop=comp.crop(roi).resize(((roi[2]-roi[0])*5,(roi[3]-roi[1])*5),Image.Resampling.NEAREST)
 out=P/f'PREP_PRIOR_CANDIDATE_c03c252b_NAPE_OLD_ROUTE_FRONTSPACE_{bgname}_5x.png';crop.save(out);qa.append(dict(path=str(out),sha256=sha(out)))
 if bgname=='white':
  draw=ImageDraw.Draw(crop)
  font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
  for x in range(380,716,10):
   xx=(x-roi[0])*5;draw.line((xx,0,xx,crop.height),fill=(170,50,50),width=1);draw.text((xx+1,2),str(x),font=font,fill=(170,0,0))
  for y in range(280,606,10):
   yy=(y-roi[1])*5;draw.line((0,yy,crop.width,yy),fill=(170,50,50),width=1);draw.text((2,yy+1),str(y),font=font,fill=(170,0,0))
  out=P/'PREP_PRIOR_CANDIDATE_c03c252b_NAPE_ROUTE_COORDINATE_GRID_5x.png';crop.save(out);qa.append(dict(path=str(out),sha256=sha(out)))
dump(P/'INPUT_PROVENANCE_INITIAL_PREPONLY.json',dict(id='ART-G33-15',source_image=str(OLD/'character_imggen_original.png'),source_sha256=records[0]['sha256'],prepared_before_future_return=True,reference_inputs=records,qa_only_crops=qa,crop_xyxy=roi,art_pixels_modified=False,PREPONLY=True,api_calls=0,native_calls=0,HTTP_calls=0,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
print(json.dumps(dict(run=str(P),refs=records,qa=qa),ensure_ascii=False))
