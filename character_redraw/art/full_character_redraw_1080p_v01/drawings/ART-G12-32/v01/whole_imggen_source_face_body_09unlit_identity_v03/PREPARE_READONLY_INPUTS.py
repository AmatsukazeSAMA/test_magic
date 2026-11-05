from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3];P=RUN.parent
IN=RUN/'inputs';IN.mkdir(exist_ok=True)
D=RUN/'diagnostics';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        im=Image.open(p);d.update(size=list(im.size),mode=im.mode)
    return d
def save(name,obj):
    p=RUN/name;assert not p.exists(),str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
refs=[]
def ref(src,name,role,box=None):
    dst=IN/name;assert not dst.exists(),str(dst)
    if box is None:shutil.copyfile(src,dst)
    else:Image.open(src).crop(box).save(dst)
    refs.append(dict(**info(dst),source=info(src),source_xyxy=list(box) if box else None,operation='exact byte copy' if box is None else 'readonly original-pixel crop, no resampling',role=role))
guide=P/'inputs/source_pose_guide.png'
assert sha(guide)=='d0d16c9ae9a5e27b2daf9fbfdb202a2f1febbb9d3b70eeb1ce975345c800ab8a'
nine=BASE/'drawings/ART-G33-09/v01/whole_imggen_sourcefirst_bodyonly_08lownape_userturns_v01'
assert sha(nine/'character_imggen_original.png')=='a425cc873b2a8ce69707a3b7fff7ab8a75ad1c5245b2ef05f51adfc2201ce1fc'
key=BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
assert sha(key)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'
registry=BASE/'ASSET_REGISTRY.json';j=json.loads(registry.read_text(encoding='utf-8-sig'))
assert j['ART-G33-09']['sha256']==sha(nine/'character_imggen_original.png')
assert j['ART-G33-09']['primary_static_pass'] and j['ART-G33-09']['independent_static_pass']
ref(guide,'ref1_ORIGINAL32_FACE_ROUND_OPEN_TINY_O_ONLY_NO_CAP_COILS_ROOT.png','Original32 FACE performance only: round-open eye aperture/gaze and tiny open-O mouth. No red side-coil, hat or high temple root. Small central red bangs/face-edge context is not identity/root authority. Keep current32 expression, not09 neutral mouth.',(280,255,469,398))
ref(guide,'ref2_ORIGINAL32_BODY_CONTACTS_COSTUME_CROP_NO_HEAD_COILS.png','Original32 BODY from neck/shoulders down: red costume bow/gold, black collar/long sleeves, white shoulder frills/vertical apron trim/cuffs, forward overlapping distinct fingers/contacts/wrists, waist/back ties and true half-body bottom crop. All original head/red side-coils/high roots/cap excluded; source crop is not output neck boundary.',(0,409,704,976))
ref(nine/'qa_white.png','ref3_REVIEWED09_GRAY_BOB_CAP_LOWROOT_COMPRESSED_RETURNS_IDENTITY_MATERIAL_ONLY.png','Both-reviewed09 current head/cap2leaves/bob identity, same-ear posterior low-nape two-bead connection, broad opaque gray front/returns and muted-mint material only. No09 neutral mouth, expression/aperture, head tilt/proportion, arm/body action or fixed outward axis/length/turn count; cropped bow/frill edge is incidental. This occluded visible curl is not a complete hidden-geometry master.',(125,15,610,472))
ref(key,'ref4_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','Flat pigments only: bob and all gray front/inner/back/return B6B4B2, original mint regions muted B0C8BA, line171717. Swatch placement is not spatial material allocation or lighting. Keep opaque broad gray returns rather than deleting or coloring them all mint.')
local=P/'local_round_drill_v01/LOCAL_REPAIR_STATUS.json'
before=RUN/'LOCAL_REPAIR_PARENT_STATUS_BEFORE.json';assert not before.exists();shutil.copyfile(local,before)
motion=P/'whole_imggen_unlit_returns_motion_v02/diagnostics/R000081_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png'
md=D/'R000081_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png';shutil.copyfile(motion,md)
Image.open(md).resize((164,208),Image.Resampling.NEAREST).save(D/'R000081_HAIR_ONLY_OBSERVATION_4x.png')
for bg in ['white','black']:
    src=nine/('qa_'+bg+'.png');box=(440,285,610,472)
    im=Image.open(src).crop(box);im.save(D/f'REVIEWED09_LOWROOT_GRAYRETURNS_{bg}_1x.png')
    im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(D/f'REVIEWED09_LOWROOT_GRAYRETURNS_{bg}_3x.png')
save('REGISTRY_READONLY_SNAPSHOT.json',{'captured_utc':datetime.now(timezone.utc).isoformat(),'source_registry':info(registry),'entries':{k:j[k] for k in ['ART-G12-32','ART-G33-09']},'central_written':False})
save('REF_INPUT_PROVENANCE.json',{'id':'ART-G12-32','preparation_only':True,'submitted':False,'refs':refs,'original_guide_not_submitted_whole':info(guide),'reviewed09_raw_not_submitted_whole':info(nine/'character_imggen_original.png'),'reviewed09_primary':info(nine/'PRIMARY_GOAL_REVIEW.json'),'reviewed09_independent':info(Path(j['ART-G33-09']['independent_review'])),'local_repair_parent':str(local.parent),'local_parent_before':info(before),'motion_only_diagnostic':info(md),'old32_whole_failure_not_submitted':info(P/'whole_imggen_v01/character_imggen_original.png'),'new32_v02_failure_not_submitted':info(P/'whole_imggen_unlit_returns_motion_v02/character_imggen_original.png'),'new32_v02_privateHOLD':info(P/'whole_imggen_unlit_returns_motion_v02/DRAFT_PRIMARY_REVIEW.json'),'excluded':['All32 old/new lit-coil full head/root/whole pixels','bare horizontal user turns prototype','full original red twin-coil head/guide','failed dual-coil44 or any full07 head','AI face/body bitmap'],'no_bad32_lit_coil_reference_pixels_submitted':True,'final_art_pixels_modified':False,'native_calls':0,'api_calls':0,'central_writes':0})
print(json.dumps({'run':str(RUN),'refs':[dict(path=r['path'],sha256=r['sha256'],size=r['size']) for r in refs],'local_before_sha256':sha(before),'reviewed09_independent_report':j['ART-G33-09']['independent_review'],'calls':0},ensure_ascii=False,indent=2))
