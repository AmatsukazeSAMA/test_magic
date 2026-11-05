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
old=P/'whole_imggen_v01';local=P/'local_round_drill_v01'
assert sha(old/'character_imggen_original.png')=='01f613ade86c7951f59440e5f0cd7abf658a18569579d732c713d12e27ade798'
assert sha(P/'character_api_original.png')=='c955214821b17bfc5f041fcd09e67e75e4e97594140a7d93a9d257b1f11bf2eb'
key=BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
assert sha(key)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'
refs=[]
for src,name,role in [
    (P/'inputs/source_pose_guide.png','ref1_ORIGINAL32_SOURCE_ACTION_EYES_MOUTH_HANDS_CROP_ONLY.png','Original936 owns round-open eye aperture/gaze, tiny open-O mouth, head tilt/head-body, overlapping individual fingers/contacts/wrists, costume and half-body crop. Red twin high coils/root/identity forbidden.'),
    (old/'qa_white.png','ref2_OLD32_WHOLE_WHITE_POSE_SINGLE_LOWROOT_EDIT_TARGET.png','Existing coherent32 character white QA; preserve sole same-side low-nape bead root, bob identity, hands/clothes and wide opaque gray front/return connections. Repeated dark returns are explicitly defective material to unify, not geometry to delete. White background/air not opaque.'),
    (old/'qa_black.png','ref3_OLD32_WHOLE_BLACK_SAME_EDIT_TARGET.png','Same old32 character in black QA, not another pose. Use both backgrounds to distinguish real air from opaque gray returns/mint/white frill/black costume. Preserve gray returns, remove only repeated deep shading, no new coil.'),
    (key,'ref4_UNLIT_GRAY_MINT_CONTOUR_PIGMENTS_ONLY.png','Three flat pigments only: gray B6B4B2 for every existing bob/gray front-inner-return surface; muted mint B0C8BA for original mint regions; contour171717. Swatch positions are not a spatial partition/lighting map; do not recolor all gray as mint.')]:
    dst=IN/name;assert not dst.exists();shutil.copyfile(src,dst)
    assert sha(dst)==sha(src)
    refs.append(dict(**info(dst),source=info(src),operation='exact byte copy',role=role))
status=local/'LOCAL_REPAIR_STATUS.json'
before=RUN/'LOCAL_REPAIR_PARENT_STATUS_BEFORE.json';assert not before.exists();shutil.copyfile(status,before)
assert sha(status)==sha(before)
report=BASE/'review/sol_xhigh_round94.json'
reportj=json.loads(report.read_text(encoding='utf-8-sig'))
entry=next(x for x in reportj['entries'] if x['id']=='ART-G12-32')
assert entry['image_sha256']==sha(old/'character_imggen_original.png')
save('SOL94_EXACT32_FAILURE_ENTRY_COPY.json',{'source_report':info(report),'entry':entry,'art_pass_inherited':False})
motion=BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000081.png'
mb=(393,218,434,270)
mc=D/'R000081_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png'
Image.open(motion).crop(mb).save(mc)
Image.open(mc).resize((41*4,52*4),Image.Resampling.NEAREST).save(D/'R000081_HAIR_ONLY_OBSERVATION_4x.png')
for src,bg in [(old/'qa_white.png','white'),(old/'qa_black.png','black')]:
    box=(675,470,855,935);im=Image.open(src).crop(box)
    im.save(D/f'OLD32_ROOT_COIL_RETURNS_{bg}_1x.png')
    im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(D/f'OLD32_ROOT_COIL_RETURNS_{bg}_3x.png')
source=Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G12-32\source.png')
source_evidence=[old/'character_imggen_original.png',old/'qa_white.png',old/'qa_black.png',source,BASE/'coverage/source_frames/F000933.png',P/'inputs/source_pose_guide.png',key,BASE/'inputs/user_drill_structure_20261101_v01.png',motion]
registry=BASE/'ASSET_REGISTRY.json';j=json.loads(registry.read_text(encoding='utf-8-sig'))
save('REGISTRY_READONLY_SNAPSHOT.json',{'captured_utc':datetime.now(timezone.utc).isoformat(),'source_registry':info(registry),'entry':j['ART-G12-32'],'central_written':False})
save('REF_INPUT_PROVENANCE.json',{'id':'ART-G12-32','refs':refs,'source_evidence':[info(p) for p in source_evidence],'old_whole_failure':info(old/'PRIMARY_GOAL_REVIEW.json'),'sol94_exact_failure':info(report),'local_repair_parent':str(local),'local_parent_status_before':info(before),'local_parent_status_source':info(status),'first_API_already_saved':info(P/'character_api_original.png'),'first_API_receipt':info(P/'result.json'),'motion_observation_only':dict(**info(mc),source=info(motion),source_xyxy=list(mb),submitted=False),'generation_refs_exactly_four':True,'no_user_bare_horizontal_turns_or_extra_curl_crop_submitted':True,'final_art_pixels_modified':False,'native_calls':0,'api_calls':0,'central_writes':0})
print(json.dumps({'run':str(RUN),'refs':[dict(path=r['path'],sha256=r['sha256'],size=r['size']) for r in refs],'local_before_sha256':sha(before),'sol94_sha256':sha(report),'motion_crop':info(mc)},ensure_ascii=False,indent=2))
