from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[5]
B = ROOT / 'art/full_character_redraw_1080p_v01'
CEL = Path(__file__).resolve().parent
R = CEL / 'prep_first_api_source4634_closed_smile_horizontal_outward_gloves_fullshoes_graygreen_v06'
PREV = B / 'drawings/ART-G51-11/v01/prep_first_api_source4630_roundeyes_asymmetric_outward_low_gloves_fullshoes_graygreen_v07_explicit_small_turn'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
read = lambda p: json.loads(Path(p).read_text('utf-8-sig'))
ev = lambda p: {'path': str(Path(p).resolve()), 'sha256': sha(p)}
def save(p, x):
    assert not p.exists(), p
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

assert not R.exists()
job = read(CEL / 'JOB.json')
assert job['id'] == 'ART-G51-12' and job['source_frame'] == 4634 and job['source_pts'] == 2474480
assert sha(job['source_image']) == job['source_image_sha256']
timeline = Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json')
assert read(timeline)[4634]['pts'] == job['source_pts']
registry = read(B / 'ASSET_REGISTRY.json')
assert job['id'] not in registry
blocked_names = {'attempt.json', 'result.json', 'request_manifest.json', 'character_api_original.png',
                 'character_imggen_original.png', 'NATIVE_CALL_RECEIPT.json', 'ROOT_API_EXECUTION_RECEIPT.json', 'BUILTIN_GENERATION.json'}
blocked = [str(p) for p in CEL.rglob('*') if p.is_file() and (p.name in blocked_names or 'unknown' in p.name.lower())]
assert not blocked, blocked
before = [ev(p) for p in CEL.rglob('*') if p.is_file() and p != Path(__file__).resolve()]
assert sha(PREV / 'character_api_original.png') == '124e316dc34866a127f75e66d41023941dc5aaa28fa9e822ad3e00e4a6773f7c'
(R / 'inputs').mkdir(parents=True)
specs = [
    (CEL/'inputs/source_pose_guide.png', 'ref1_OWN4634_COMPLETE_POSE_HORIZONTAL_OUTWARD_GLOVES_FULLSHOES.png', None,
     'Own4634 only: pose, unequal round eyes, small closed smile, two glove groups, skirt/legs/shoes/crop. Red hair and background are replaced.'),
    (PREV/'character_api_original.png', 'ref2_PREVIOUS11_SAFE_INTERIOR_GRAYGREEN_CLOTH_LINE_ONLY.png', [414,480,437,504],
     'Previous11 safe interior graygreen cloth and sparse ink only. No outline, head, hands, pose, coil or shoulder-depth transfer.'),
    (B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png', 'ref3_USER_APPROVED_X01_CURL_DRAWING_ONLY.png', None,
     'User approved curl drawing only: two large turns plus own small turn with opaque gray return then C. No fixed size/axis or wholecharacter acceptance.'),
    (PREV/'inputs/ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png', 'ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png', None,
     'Gray rounded shortbob upper fringe/cap identity only. Own4634 owns face, cap projection and head/body pose. No old coil or lower-eye marks.'),
    (CEL/'inputs/source_pose_guide.png', 'ref5_OWN4634_ROUND_UNEQUAL_EYES_SMALL_CLOSED_SMILE.png', [308,130,406,203],
     'Own4634 full eye openings and small closed upward mouth arc, unlike previous11 neutral mouth. Tiny eye-corner tolerance applies; no obvious decorative mole.')
]
refs=[]
for src,name,box,role in specs:
    dst=R/'inputs'/name
    if box:
        Image.open(src).crop(box).save(dst)
    else:
        shutil.copyfile(src,dst)
        assert src.read_bytes() == dst.read_bytes()
    refs.append({**ev(dst), 'source': ev(src), 'crop_xyxy': box, 'scale': 1,
                 'operation': 'readonly rectangle, no paint/alpha cleanup/warp' if box else 'exact byte copy', 'role': role})
diagnostics=[]
for name,box,m in [
    ('OWN4634_EYES_MOUTH_READONLY_5x.png',[308,130,406,203],5),
    ('OWN4634_TWO_DIFFERENT_OUTWARD_GLOVES_READONLY_2x.png',[26,320,697,430],2),
    ('OWN4634_BOTH_COMPLETE_SHOES_READONLY_2x.png',[275,698,430,915],2)]:
    src=CEL/'inputs/source_pose_guide.png'
    im=Image.open(src).crop(box)
    out=R/name
    im.resize((im.width*m,im.height*m),Image.Resampling.NEAREST).save(out)
    diagnostics.append({**ev(out),'source':ev(src),'crop_xyxy':box,'magnification':m,'operation':'readonly nearest diagnostic'})
src=PREV/'qa_white.png';im=Image.open(src).copy();ImageDraw.Draw(im).rectangle([414,480,437,504],outline=(255,0,255),width=2)
out=R/'QA_PREVIOUS11_SAFE_INTERIOR_CLOTH_CROP_BOUNDARY.png';im.save(out)
diagnostics.append({**ev(out),'source':ev(src),'labelled_crop_xyxy':[414,480,437,504],'operation':'readonly labelled context; not API input'})
save(R/'INPUT_COPY_AND_CROP_PROVENANCE.json',{'id':job['id'],'references':refs,'diagnostics':diagnostics,'art_pixels_modified':False})
save(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json',{
    'id':job['id'],'recorded_utc':datetime.now(timezone.utc).isoformat(),'registry_entry_absent':True,
    'searched':str(CEL),'blocked_names_checked':sorted(blocked_names),'existing_attempt_raw_result_unknown_files':blocked,
    'files_present_before_PREP':before,'source':ev(job['source_image']),'JOB':ev(CEL/'JOB.json'),
    'REGISTRATION_PLAN':ev(CEL/'REGISTRATION_PLAN.json'),'timeline':ev(timeline),'source_frame':4634,'source_pts':2474480,
    'old_unknown_reopened':False,'API_calls':0,'native_calls':0,'network_calls':0})
print(json.dumps({'run':str(R),'references':refs,'diagnostics':diagnostics},ensure_ascii=False))
