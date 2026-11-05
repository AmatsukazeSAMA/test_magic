from pathlib import Path
from PIL import Image
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];INP=RUN/'inputs';INP.mkdir(exist_ok=True);QA=RUN/'diagnostics';QA.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
guide=CEL/'inputs/source_pose_guide.png';im=Image.open(guide).convert('RGBA');assert im.size==(848,976)
mask=Image.new('L',im.size,255);hide=[285,26,820,390];mask.paste(0,hide)
restore={'source_openeyes_tinyO_face':[355,154,588,380],'source_left_shoulderfrill':[263,345,405,441],'source_neck_fullcollar':[380,363,520,432]}
for box in restore.values():mask.paste(255,box)
for y in range(hide[1],hide[3]):
    for x in range(hide[0],hide[2]):
        r,g,b,a=im.getpixel((x,y))
        if r>70 and g<90 and b<90 and r>1.6*g and r>1.6*b:mask.putpixel((x,y),0)
selected=Image.new('RGBA',im.size,(0,0,0,0));selected.paste(im,(0,0),mask);trim=[16,0,736,976]
selected=selected.crop(trim);mask=mask.crop(trim);original=im.crop(trim)
assert all(not mask.getpixel((x,y)) or selected.getpixel((x,y))==original.getpixel((x,y)) for y in range(mask.height) for x in range(mask.width))
target=INP/'ORIGINAL50_COMMON_LAYOUT_OPEN_EYES_TINY_O_HIGH_OK_LOOP_LOW_DROOP_HAND_READONLY.png';assert not target.exists();selected.save(target)
maskpath=INP/'SOURCE50_PIXEL_SELECTION_MASK.png';mask.save(maskpath)
motion=BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000157.png';roi=[405,207,54,82]
hair=Image.open(motion).crop((roi[0],roi[1],roi[0]+roi[2],roi[1]+roi[3]));hp=INP/'R157_HAIR_ONLY_READONLY.png';hair.save(hp)
diagnostics=[]
for label,rgb in [('white',(255,255,255)),('black',(0,0,0))]:
    bg=Image.new('RGBA',selected.size,(*rgb,255));bg.alpha_composite(selected);p=QA/f'SOURCE50_COMMON_{label}.png';bg.convert('RGB').save(p);diagnostics.append(evidence(p))
for label,src,box,scale in [
 ('SOURCE50_HIGH_OK_LOOP',guide,[62,100,231,300],3),
 ('SOURCE50_LOW_DROOP_HAND',guide,[221,462,440,581],3),
 ('SOURCE50_FACE_NECK',guide,[347,151,594,429],2),
 ('SELECTED50_FACE_NECK_WHITE',QA/'SOURCE50_COMMON_white.png',[331,151,578,429],2),
 ('R157_HAIR_ONLY',hp,[0,0,hair.width,hair.height],4)]:
    crop=Image.open(src).crop(box);p=QA/f'{label}_{scale}x.png';crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST).save(p)
    diagnostics.append({'path':str(p),'sha256':sha(p),'source':str(src),'source_sha256':sha(src),'crop_xyxy':box,'scale':scale})
scope=json.loads((BASE/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json').read_text(encoding='utf-8-sig'));found=[]
def walk(v):
    if isinstance(v,dict):
        if v.get('id')=='ART-G12-50':found.append(v)
        for z in v.values():walk(z)
    elif isinstance(v,list):
        for z in v:walk(z)
walk(scope);assert len(found)==1
record={'id':'ART-G12-50','created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_HAIR_ONLY_PREPARATION_HOLD_NO_GENERATION_REQUEST',
 'guide':evidence(guide),'source_guide_size':[848,976],'source_layout':evidence(target),'selection_mask':evidence(maskpath),'head_hide_roi_xyxy':hide,'restore_rois_xyxy':restore,
 'red_fill_exclusion_rule':'OnlyoriginalheadROI redfill R>70,G/B<90,R>1.6G/B removed; no recolor/paint. warmneckshadow andbodyredbow preserved.',
 'compact_crop_xyxy':trim,'suggested_source_canvas':[720,976],'trim_transform':{'uniform_scale':1,'translation':[-16,0],'per_part_transform':False},'selectedpixels_equal_original':True,'selection_edges_not_outputcuts':True,
 'motion_full':evidence(motion),'motion_crop':evidence(hp),'motion_roi_xywh':roi,'priority_scope50':found[0],'diagnostics':diagnostics,'JOB_preserved':evidence(CEL/'JOB.json'),
 'identity_geometry_refs_not_copied_or_submitted':True,'API_PREPARED_REQUEST_written':False,'DRAFT_API_REQUEST_written':False,'attempt_written':False,'API_calls':0,'native_calls':0,'central_write':False}
p=RUN/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json';assert not p.exists();p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':evidence(p),'source_layout':evidence(target),'hair_crop':evidence(hp),'calls':0},ensure_ascii=False))
