from pathlib import Path
import hashlib, json, shutil
from datetime import datetime, timezone
from PIL import Image

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
RUN=Path(__file__).parent
PRIOR=RUN.parent/'whole_imggen_source2339_connectedgray_occlusion_v02'
INPUTS=RUN/'inputs'
INPUTS.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(name,obj):
    p=RUN/name
    if p.exists(): raise RuntimeError(f'preserve existing file: {p}')
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def meta(p):
    p=Path(p); d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    try:
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    except Exception: pass
    return d
def copy_ref(src,name):
    dest=INPUTS/name
    if dest.exists(): raise RuntimeError(f'preserve {dest}')
    shutil.copyfile(src,dest)
    assert sha(src)==sha(dest)
    return dest

target=PRIOR/'character_imggen_original.png'
assert sha(target)=='da4a0c93fb2b783131f9cf2bfcd168894138cb095b8568966a62d69bceeedd45'
guide=PRIOR/'inputs/ref1_ORIGINAL2339_COMPLETE_UNMASKED_POSE_GUIDE.png'
assert sha(guide)=='8539fcc1d586d0b62307c1face34d77bc8a94bcace0074cc2b99e568b58adea6'
motion=B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000028.png'
refs=[copy_ref(target,'ref1_CURRENT09_da4a0c93_COMPLETE_CHARACTER_OCCLUSION_REPAIR_TARGET.png'),
      copy_ref(guide,'ref2_ORIGINAL2339_COMPLETE_UNMASKED_POSE_GUIDE.png')]
crop_motion=[521,268,560,296]
motion_crop=INPUTS/'ref3_R028_HAIR_ONLY_RECOIL_PHASE_NO_FACE_ROOT_CLOTH.png'
with Image.open(motion) as im:
    im.crop(tuple(crop_motion)).save(motion_crop)
    im.crop((500,240,580,330)).resize((480,540),Image.Resampling.NEAREST).save(RUN/'PREP_R028_CONTEXT_READONLY_NOT_GENERATION_REF_6x.png')
with Image.open(motion_crop) as im:im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST).save(RUN/'PREP_REFERENCE_R028_HAIR_ONLY_8x.png')
refs.append(motion_crop)
crop_fan=[235,270,342,405]
fan=INPUTS/'ref4_ORIGINAL2339_OWN_WHITE_FAN_BLACK_PUFF_SLEEVE_BOUNDARY_NO_HAIR.png'
with Image.open(guide) as im: im.crop(tuple(crop_fan)).save(fan)
with Image.open(fan) as im: im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(RUN/'PREP_REFERENCE_SOURCE2339_SHOULDER_BOUNDARY_3x.png')
refs.append(fan)
gray=INPUTS/'ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'
Image.new('RGB',(192,128),(182,180,178)).save(gray)
refs.append(gray)
registry=read(B/'ASSET_REGISTRY.json')
assert registry['ART-G33-09']['sha256']==sha(target)
write('CURRENT_SELECTED_STATUS_SNAPSHOT.json',{'captured_utc':datetime.now(timezone.utc).isoformat(),'record':registry['ART-G33-09'],'selected_image_verified':meta(target),'snapshot_only_not_central_write':True})
write('INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G33-09','PREPONLY':True,'submitted':False,'API_calls':0,'native_calls':0,
    'source_frame':2339,'source_pts':1248720,'first_exposure_frames':[867,868,869,870],
    'reference_records':[
        {'reference_number':1,'file':meta(refs[0]),'source':meta(target),'operation':'byte_identical_copy','role':'CURRENT coherent full identity/body/low LEFT root/connected gray volume; lower turns and C in front of sleeve are WRONG and are the sole repair target'},
        {'reference_number':2,'file':meta(refs[1]),'source':meta(guide),'operation':'byte_identical_copy','role':'Original2339 is exclusive action, own eyes/tiny neutral mouth, hands, garment/frill shape and original visible bottom cutoff authority; red identity/high coils must not copy'},
        {'reference_number':3,'file':meta(refs[2]),'source':meta(motion),'crop_xyxy':crop_motion,'operation':'readonly_original_pixel_rectangular_crop_no_rescale','role':'Secondary compact/retracted hair phase ONLY. No face/beads/root/AI clothing. Crop size is NOT intrinsic hair mass; its closed gray cone/line pattern is NOT geometry/material reference'},
        {'reference_number':4,'file':meta(refs[3]),'source':meta(guide),'crop_xyxy':crop_fan,'operation':'readonly_original_pixel_rectangular_crop_no_rescale','role':'Own original white fan/frill and black puff sleeve actual boundary only; no original red hair or root. Do not enlarge garment to cover coil'},
        {'reference_number':5,'file':meta(refs[4]),'operation':'new_input_only_uniform_RGB_card','RGB':[182,180,178],'role':'Pure gray pigment only, no spatial material or geometry. Mint partition already belongs to current09, not replaced by card'}
    ],
    'excluded_generation_references':['correct11 full vertical hanging head-coil volume image','polished gray-return detail with light/shadow','current08 head/body as new action authority','AI fullframe or AI shoulder geometry','G02 half-lid template'],
    'readonly_preparation_changes_final_art_pixels':False,
    'diagnostic_naming_rule':'All new crops of prior selected candidate use PREP_PRIOR_CANDIDATE_<hash> and explicitly prepared_before_future_return=true; no future return exists.',
    'future_generated_art_exists':False
})
print(json.dumps({'run':str(RUN),'refs':[meta(p) for p in refs]},ensure_ascii=False,indent=2))
