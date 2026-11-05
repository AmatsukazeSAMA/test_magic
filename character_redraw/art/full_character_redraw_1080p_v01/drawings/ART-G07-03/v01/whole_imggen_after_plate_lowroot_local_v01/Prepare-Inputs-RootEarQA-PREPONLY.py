"""Read-only input copies and labelled diagnosis; never edit artwork or call a model."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import hashlib, json, shutil, math

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p / 'image_defaults.json').exists())
base = root / 'art/full_character_redraw_1080p_v01'
local = run.parent / 'local_api_plate_and_lowroot_scope_refined_api_v04'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p), 'sha256': sha(p)}
def save(path, data):
    assert not path.exists(), f'Preserve: {path}'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
refs = [
    (local/'character_api_original.png', 'ref1_KNOWN_LOCAL_b9fbe360_COMPLETE_RGBA_SOLE_POSE.png',
     'Only current complete pose/visible matte/expression/hands/gray-sleeve and connected curl path. Red root at crown-end is WRONG and must move toward same ear jaw/nape, screen-up in this inverted pose.'),
    (local/'inputs/ref3_APPROVED11_EAR_LOWBEAD_RELATION_ONLY_NO_CAP_EYES.png', 'ref2_EAR_LOWBEAD_RELATION_ONLY_NO_CAP_EYES.png',
     'Tiny unchanged41x57 ear/lowbead relationship only, no eyes or cap. Not currentpose/axis; do not paste upright pixels or enlarge the ear.'),
    (local/'inputs/ref4_PURE_GRAY_PIGMENT_ONLY.png', 'ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY.png',
     'Pure neutralGRAY pigment only: bob/front/opaque inside-back return/next/C flatgray; thin mutedmint material edge only. No light/geometry/body authority.')]
expected=['b9fbe360fd4bcaacf8e5098a79e1b74948f8e1cac8b1636f1c00d94b63faf30a',
          'a3db75e3ee1c7e2c9b03f79d24c7433e39f05b40695f84d19f8cf6dfa97bdb72',
          '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
records=[]
for (src,name,role),expected_sha in zip(refs,expected):
    assert sha(src)==expected_sha
    dst=run/'inputs'/name
    assert not dst.exists()
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dst)
    records.append({**ev(dst),'source':ev(src),'role':role,'exact_original_bytes':True})
target=refs[0][0]
with Image.open(target) as im:
    assert im.size==(1344,1024) and im.mode=='RGBA'
    art=im.copy()
a=np.asarray(art)
qa=run/'readonly_QA';qa.mkdir(exist_ok=True)
for color in ['white','black']:
    dst=qa/f'PRIOR_LOCAL_COMPLETE_{color}.png'
    assert not dst.exists()
    shutil.copyfile(local/f'qa_{color}.png',dst)

fontpath=Path('C:/Windows/Fonts/arial.ttf')
font=lambda size: ImageFont.truetype(str(fontpath),size) if fontpath.exists() else ImageFont.load_default(size=size)
def arrow(d,start,end,color,width=5):
    d.line([start,end],fill=color,width=width)
    ang=math.atan2(end[1]-start[1],end[0]-start[0])
    pts=[end,(end[0]-18*math.cos(ang-0.5),end[1]-18*math.sin(ang-0.5)),(end[0]-18*math.cos(ang+0.5),end[1]-18*math.sin(ang+0.5))]
    d.polygon(pts,fill=color)

root_region=(275,365,340,435)
ear_region=(288,405,343,553)
wrong_region=(275,540,340,600)
rootcenter=(305,570)
crop=(210,320,430,660)
for bg in ['white','black']:
    comp=Image.new('RGBA',art.size,bg);comp.alpha_composite(art)
    full=Image.new('RGB',(1344,1164),'#eeeeee');full.paste(comp.convert('RGB'),(0,140))
    d=ImageDraw.Draw(full)
    d.text((20,12),'READ-ONLY DIAGNOSIS - NOT A GENERATION REFERENCE',font=font(24),fill='black')
    d.text((20,47),'Current bead near y570 = crown-end, WRONG. Same-ear jaw/nape is screen-UP.',font=font(21),fill='#a00030')
    d.text((20,80),'Cyan region is an orientation hypothesis, not a fixed root pixel or hidden-body claim.',font=font(20),fill='#006070')
    d.text((20,109),'Keep ear/face/pose. Bob may hide beads. No disc, hidden jaw/mouth/neck completion.',font=font(19),fill='black')
    shift=lambda b:(b[0],b[1]+140,b[2],b[3]+140)
    d.rectangle(shift(root_region),outline='#00c8de',width=4)
    d.rectangle(shift(ear_region),outline='#f0b000',width=3)
    d.rectangle(shift(wrong_region),outline='#ff3e7a',width=4)
    arrow(d,(257,570+140),(257,390+140),'#00c8de',5)
    d.text((32,386+140),'toward jaw / nape',font=font(18),fill='#00b0ce')
    d.text((30,584+140),'crown-end bead: wrong',font=font(17),fill='#ff3e7a')
    f=qa/f'READONLY_ROOT_EAR_DIRECTION_{bg}_FULL.png';assert not f.exists();full.save(f)
    # Same pixels, nearest-neighbor enlargement for diagnosis only.
    loc=comp.convert('RGB').crop(crop).resize(((crop[2]-crop[0])*3,(crop[3]-crop[1])*3),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(loc.width+420,loc.height),'#eeeeee');canvas.paste(loc,(0,0));dd=ImageDraw.Draw(canvas)
    tr=lambda b:((b[0]-crop[0])*3,(b[1]-crop[1])*3,(b[2]-crop[0])*3,(b[3]-crop[1])*3)
    dd.rectangle(tr(root_region),outline='#00c8de',width=5)
    dd.rectangle(tr(ear_region),outline='#f0b000',width=4)
    dd.rectangle(tr(wrong_region),outline='#ff3e7a',width=5)
    arrow(dd,((255-crop[0])*3,(570-crop[1])*3),((255-crop[0])*3,(390-crop[1])*3),'#00c8de',7)
    for y,text,color in [(25,'READ-ONLY ROOT DIAGNOSIS','black'),(75,'INVERTED head: jaw is UP.','black'),(120,'Cyan: same-ear nape region.','#006f80'),(163,'Not a fixed new bead point.','#006f80'),(220,'Yellow: currently visible ear.','#996000'),(267,'Keep its skin and contour.','#996000'),(325,'Pink: wrong crown-end root.','#b00040'),(370,'Larger visible ear is no fix.','#b00040'),(445,'Bob may hide the new beads.','black'),(490,'Do not expose hidden anatomy.','black'),(570,'Local raw SHA b9fbe360...','black'),(615,'ROI [210,320,430,660], 3x','black'),(660,'Never send this overlay as art.','black')]:
        dd.text((loc.width+14,y),text,font=font(19),fill=color)
    f=qa/f'READONLY_ROOT_EAR_DIRECTION_{bg}_LOCAL_3x.png';assert not f.exists();canvas.save(f)
    # Plain local-pixel crop without any imposed root drawing.
    f=qa/f'LOCAL_EAR_WRONG_ROOT_UNANNOTATED_{bg}_3x.png';assert not f.exists();loc.save(f)

f=qa/'LOCAL_ALPHA_FULL.png';assert not f.exists();art.getchannel('A').save(f)
source=base/'coverage/source_frames/F000507.png'
with Image.open(source) as src:
    sf=qa/'ORIGINAL507_NATIVE_SAMEEAR_CONTEXT_READONLY_2x.png'
    assert not sf.exists()
    src.crop((340,250,660,620)).resize((640,740),Image.Resampling.NEAREST).save(sf)
alpha=a[:,:,3]
red=(alpha>=200)&(a[:,:,0].astype(np.int16)>100)&(a[:,:,0].astype(np.int16)>1.5*a[:,:,1])&(a[:,:,0].astype(np.int16)>1.4*a[:,:,2])
red[:500]=False;red[650:]=False;red[:,:240]=False;red[:,360:]=False
y,x=np.where(red)
data={'id':'ART-G07-03','status':'INPUT_AND_READONLY_ROOT_QA_PREPARED_NOT_GENERATED','refs':records,'target':ev(target),
      'source507_QA_only':ev(source),'current_local_result':ev(local/'result.json'),
      'current_local_execution_receipt':ev(local/'ROOT_API_EXECUTION_RECEIPT.json'),
      'bad_red_root_bbox_xyxy':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],
      'bad_red_root_centroid':[float(x.mean()),float(y.mean())],
      'approx_visible_ear_region_xyxy':list(ear_region),'new_nape_orientation_region_only':list(root_region),
      'diagnostic_coordinate_space':[1344,1024],'root_region_not_final_root_or_hidden_geometry_certification':True,
      'readonly_crop_ROI':list(crop),'source_native_QA_crop_xyxy':[340,250,660,620],
      'original_source_not_in_toolrefs':True,'annotated_diagnostics_not_in_toolrefs':True,
      'art_pixels_modified':False,'API_calls':0,'native_calls':0,'network_calls':0}
save(run/'INPUT_AND_DIAGNOSTIC_PROVENANCE_PREPONLY.json',data)
print(json.dumps({'run':str(run),'refs':[r['path'] for r in records],'badroot_bbox':data['bad_red_root_bbox_xyxy'],'badroot_centroid':data['bad_red_root_centroid'],'API_calls':0,'native_calls':0},ensure_ascii=False))
