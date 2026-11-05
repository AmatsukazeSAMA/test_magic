from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
P=RUN.parent
BASE=RUN.parents[3]
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

raw=P/'character_api_original.png';white=P/'qa_white.png';black=P/'qa_black.png';guide=P/'inputs/source_pose_guide.png'
assert sha(raw)=='0b6e1c2f8a422c66fabf32ac4e98d0a9229bf52a8bd089d0c086ae1c15236ae0'
assert sha(guide)=='8781ac19a48e4e6c767c8962ec9b4d647955eea26ca916538da373b870432865'
leaf=P/'whole_imggen_source44_capleaves_userturns_v01/inputs/ref4_REVIEWED08_TWO_BLACK_CAP_LEAVES_ATTACHMENT_ONLY.png'
assert sha(leaf)=='629446499e9abdcaaa6675ea5abbbdc643682505da153d31469e3f5f09c2f5f6'
ref(white,'ref1_FIRST_API44_SINGLE_LOWCOIL_WHITE_EDIT_TARGET.png','FIRST API44 complete white QA EDIT TARGET; same single low-ear/nape two-bead coil and source44 face/hands/body/costume/crop. Cap leaves missing here must be restored from ref5. No new coil at the cap. Background white/air are not opaque output.')
ref(black,'ref2_FIRST_API44_SINGLE_LOWCOIL_BLACK_SAME_TARGET.png','Same FIRST API44 full character on black QA, not a second pose. Background-dependent areas are true transparent background/air; gray front/return and mint stay opaque. Same missing cap leaves must be added, not an extra curl.')
ref(guide,'ref3_ORIGINAL993_FACE_PERFORMANCE_ONLY_NO_CAP_COILS_ROOT.png','Original993 face aperture/gaze and small curved closed smile ONLY. Crop excludes all original red side-coils, cap and high temple root. A small central red fringe fragment is incidental source context, not gray-bob identity or a new root. Crop is not output head boundary.',(434,273,623,407))
ref(guide,'ref4_ORIGINAL993_BODY_ONLY_NO_HEAD_COILS.png','Original993 body/costume/low palm/forearm/waist/rear tie and actual half-body lower crop evidence ONLY. Entire original head, cap, red coils and roots excluded. Top crop omits high palm; full targets1/2 retain correct high-palm performance. Source crop is not a new output edge.',(26,427,1110,1024))
ref(leaf,'ref5_REVIEWED08_EXACT_TWO_BLACK_CAP_LEAVES_ONLY.png','Reviewed08v04 exactly two black cap leaves and small attachment base only, no head/face/ear/root/coil/body. Gray bob-top wedge incidental, black base not third leaf. Adapt placement/orientation to current44 cap and head tilt, not08 whole head.')
for src,bg in [(white,'white'),(black,'black')]:
    for name,box in [('SINGLE_LOWCOIL_ORIGINAL44',(590,310,728,574)),('CAP_MISSING_TWO_LEAVES',(350,35,780,225))]:
        im=Image.open(src).crop(box);im.save(D/f'{name}_{bg}_1x.png')
        im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(D/f'{name}_{bg}_3x.png')
j=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
save('REGISTRY_READONLY_SNAPSHOT.json',{'captured_utc':datetime.now(timezone.utc).isoformat(),'entries':{k:j[k] for k in ['ART-G12-44','ART-G33-08']},'central_written':False})
save('REF_INPUT_PROVENANCE.json',{'id':'ART-G12-44','preparation_only':True,'submitted':False,'refs':refs,'first_api_raw_not_submitted':info(raw),'first_api_result':info(P/'result.json'),'source_guide_not_submitted':info(guide),'first_api_primary_repair':info(P/'PRIMARY_GOAL_REVIEW.json'),'previous_failed_v01_not_submitted':info(P/'whole_imggen_source44_capleaves_userturns_v01/character_imggen_original.png'),'previous_failed_v01_artist_HOLD':info(P/'whole_imggen_source44_capleaves_userturns_v01/DRAFT_PRIMARY_REVIEW.json'),'excluded':['user bare horizontal turns-only prototype','full original red twin-coil head or guide','failedv01 duplicate-coil whole and upper coil pixels','any full07 head or full08 head','AI body/face bitmap','raw hiddenRGB target'],'fixed_holes_axis_length_ratio':False,'final_art_pixels_modified':False,'native_calls':0,'api_calls':0,'central_writes':0})
print(json.dumps({'run':str(RUN),'refs':[dict(path=r['path'],sha256=r['sha256'],size=r['size']) for r in refs],'calls':0},ensure_ascii=False,indent=2))
