from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
PARENT=RUN.parent
IN=RUN/'inputs'; IN.mkdir(exist_ok=True)
D=RUN/'diagnostics'; D.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def info(p):
    p=Path(p); d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        im=Image.open(p);d.update(size=list(im.size),mode=im.mode)
    return d
def write_new(name,obj):
    p=RUN/name
    assert not p.exists(),str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

raw=PARENT/'character_api_original.png'
guide=PARENT/'inputs/source_pose_guide.png'
white=PARENT/'qa_white.png';black=PARENT/'qa_black.png'
old08=BASE/'drawings/ART-G33-08/v01/whole_imggen_old08_lownape_flatmaterial_v04'
turns=BASE/'inputs/user_drill_turns_only_no_root_20261101_v01.png'
motion=BASE/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000126.png'
assert sha(raw)=='0b6e1c2f8a422c66fabf32ac4e98d0a9229bf52a8bd089d0c086ae1c15236ae0'
assert sha(guide)=='8781ac19a48e4e6c767c8962ec9b4d647955eea26ca916538da373b870432865'
assert sha(old08/'character_imggen_original.png')=='663617241b31f5a39f5c6a5bae101639c6b90d5af42c98143e4bb3a3b4a71052'
assert sha(turns)=='4edbd2131353520b61382bfcbcdfd6360cf71765a7b133cccfaef72c3150d8b2'
refs=[]
def ref(src,name,role,box=None):
    dst=IN/name
    assert not dst.exists(),str(dst)
    if box is None: shutil.copyfile(src,dst)
    else: Image.open(src).crop(box).save(dst)
    d=info(dst);d.update(source=info(src),source_xyxy=list(box) if box else None,
        operation='readonly original-pixel crop, no resampling' if box else 'exact byte copy',role=role)
    refs.append(d)
ref(guide,'ref1_ORIGINAL44_ACTION_CAPLEAF_POSITION_CROP.png','Original PV993 exclusively owns current action, relaxed-open eye aperture/gaze, small curved closed smile, head-body relationship, asymmetric hands/cuffs/costume, two black cap-leaf placement/orientation and half-body framing. Original red twin-drill identity/root must not be copied.')
ref(white,'ref2_CURRENT44_EXPRESSION_LOWEAR_BEADS_NO_CAP.png','Current44 lower-face performance/gray-bob identity and low same-ear/nape two-bead connection only. Entire missing-leaf cap/top silhouette excluded. Tiny clipped first band at lower edge is context, not a full curl topology/axis or material master. Crop boundary is not output framing.',(420,245,690,414))
ref(white,'ref3_CURRENT44_LOWERBODY_HAND_COSTUME_NO_HEAD_CAP_COIL.png','Current44 lower-body/low palm/forearm, black sleeves/red bow lower tip, white apron waist/rear tie drawing continuity only. Begins below the entire head, cap, beads and visible coil; no missing-cap silhouette. Original source1 controls raised palm/upper body and true bottom crop, not this crop boundary.',(25,575,1108,1024))
ref(old08/'qa_white.png','ref4_REVIEWED08_TWO_BLACK_CAP_LEAVES_ATTACHMENT_ONLY.png','Both-reviewed08v04 exactly two black cap leaves and their attachment to white cap/bob top only. No face, ears, beads, root, coil or body pixels. Tiny bob-top edge is incidental context; not head tilt/scale, expression, cap orientation or whole identity.',(555,5,677,152))
ref(turns,'ref5_USER_TURNS_ONLY_NO_ROOT.png','Latest user broad opaque gray front/return folds, distinct mint partitions and progressive taper only; not root, fixed horizontal axis/length/turn count/hole count, and not an instruction to expose currently occluded tail.')

motion_box=(582,199,626,260)
mc=D/'R000126_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png'
Image.open(motion).crop(motion_box).save(mc)
Image.open(mc).resize((44*4,61*4),Image.Resampling.NEAREST).save(D/'R000126_HAIR_ONLY_OBSERVATION_4x.png')
for src,bg in [(white,'white'),(black,'black')]:
    for name,box in [('CAP_MISSING_LEAVES',(350,35,780,225)),('LOWEAR_COIL',(590,310,728,574))]:
        im=Image.open(src).crop(box)
        im.save(D/f'CURRENT44_{name}_{bg}_1x.png')
        im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(D/f'CURRENT44_{name}_{bg}_3x.png')
source=Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G12-44\source.png')
source_cap_box=(958,104,1310,280)
Image.open(source).crop(source_cap_box).save(D/'SOURCE993_CAP_TWO_LEAVES_ORIGINAL_PIXELS.png')
registry=BASE/'ASSET_REGISTRY.json';j=json.loads(registry.read_text(encoding='utf-8-sig'))
snapshot={'captured_utc':datetime.now(timezone.utc).isoformat(),'registry_path':str(registry),'registry_sha256_at_read':sha(registry),'entries':{k:j[k] for k in ['ART-G12-44','ART-G33-08']},'central_written':False}
assert snapshot['entries']['ART-G12-44']['sha256']==sha(raw)
assert snapshot['entries']['ART-G33-08']['primary_static_pass'] and snapshot['entries']['ART-G33-08']['independent_static_pass']
write_new('REGISTRY_READONLY_SNAPSHOT.json',snapshot)
evidence_paths=[raw,white,black,guide,source,BASE/'coverage/source_frames/F000993.png',motion,BASE/'inputs/user_drill_structure_20261101_v01.png',BASE/'inputs/identity_full_drill_three_views.png',old08/'qa_white.png']
write_new('REF_INPUT_PROVENANCE.json',{'id':'ART-G12-44','preparation_only':True,'submitted':False,'refs':refs,'source_evidence':[info(p) for p in evidence_paths],'motion_only_diagnostic':dict(**info(mc),source=info(motion),source_xyxy=list(motion_box),submitted=False),'current_root_primary_failure':info(PARENT/'PRIMARY_GOAL_REVIEW.json'),'saved_first_API_result':info(PARENT/'result.json'),'reviewed08_reference_raw':info(old08/'character_imggen_original.png'),'reviewed08_independent_report':info(BASE/'review/sol_xhigh_goal_round86.json'),'source_cap_diagnostic':dict(**info(D/'SOURCE993_CAP_TWO_LEAVES_ORIGINAL_PIXELS.png'),source=info(source),source_xyxy=list(source_cap_box)),'no_raw_hidden_RGB_reference_submitted':True,'no_current44_cap_or_missing_leaf_top_silhouette_submitted':True,'final_art_pixels_modified':False,'generation_calls':0,'api_calls':0,'central_writes':0})
print(json.dumps({'run':str(RUN),'refs':[dict(path=r['path'],sha256=r['sha256'],size=r['size']) for r in refs],'motion_hair_crop':info(mc),'calls':0},ensure_ascii=False,indent=2))
