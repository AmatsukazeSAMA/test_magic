from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parent;D=R/'diagnostics';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
proof=[]
for bg in ['white','black']:
 im=Image.open(R/f'qa_{bg}.png').convert('RGB')
 for tag,roi in [('HEAD_EAR_ROOT_COIL',[370,15,780,540]),('ROOT_COIL',[600,280,772,530]),('EYES_MOUTH',[455,190,673,316]),('SKIRT_GRIP_HAND',[350,765,480,906]),('BOTH_SHOES',[228,1185,752,1615])]:
  c=im.crop(roi)
  for scale in [1,3]:
   p=D/f'{tag}_{bg}_{scale}x.png';c.resize((c.width*scale,c.height*scale),Image.Resampling.NEAREST).save(p)
   proof.append({'path':str(p),'sha256':sha(p),'source':str(R/f'qa_{bg}.png'),'source_sha256':sha(R/f'qa_{bg}.png'),'source_roi_xyxy':roi,'scale':scale,'read_only':True})
src=Image.open(R/'inputs/ref2_ORIGINAL2385_COMPLETE_UNMASKED_GUIDE.png').convert('RGB')
new=Image.open(R/'qa_white.png').convert('RGB').resize(src.size,Image.Resampling.LANCZOS)
board=Image.new('RGB',(1264,1104),'white');board.paste(src,(0,32));board.paste(new,(640,32));dr=ImageDraw.Draw(board);dr.text((8,8),'Original2385 full guide',fill='black');dr.text((648,8),'Native20 v02 - uniform fit only - no art adoption',fill='black')
p=D/'SOURCE2385_vs_NATIVE20_FULL_READONLY.png';board.save(p);proof.append({'path':str(p),'sha256':sha(p),'read_only_whole_layer_diagnostic_fit':True})
(R/'DIAGNOSTIC_PROVENANCE.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
g=json.loads((R/'BUILTIN_GENERATION.json').read_text(encoding='utf-8-sig'));print(json.dumps({'raw_sha256':sha(R/'character_imggen_original.png'),'dimensions':g['dimensions'],'mode':Image.open(R/'character_imggen_original.png').mode,'diagnostics':str(D)},ensure_ascii=False))
