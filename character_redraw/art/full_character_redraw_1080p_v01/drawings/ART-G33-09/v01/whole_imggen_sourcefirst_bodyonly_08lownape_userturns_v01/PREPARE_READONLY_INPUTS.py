from pathlib import Path
from PIL import Image
import hashlib, json, shutil
from datetime import datetime, timezone

BASE = Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
RUN = Path(__file__).resolve().parent
INPUTS = RUN / 'inputs'
DIAG = RUN / 'diagnostics'
INPUTS.mkdir(exist_ok=True)
DIAG.mkdir(exist_ok=True)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def info(p):
    p = Path(p)
    data = dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)
    if p.suffix.lower() == '.png':
        im = Image.open(p)
        data.update(size=list(im.size), mode=im.mode)
    return data

def write_new(p, obj):
    if p.exists():
        raise FileExistsError(p)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

sourceguide = BASE / 'drawings/ART-G33-09/v01/inputs/source_pose_guide.png'
current = BASE / 'drawings/ART-G33-09/v01/character_api_original.png'
white = current.with_name('qa_white.png')
black = current.with_name('qa_black.png')
reviewed08 = BASE / 'drawings/ART-G33-08/v01/whole_imggen_old08_lownape_flatmaterial_v04/character_imggen_original.png'
white08 = reviewed08.with_name('qa_white.png')
turns = BASE / 'inputs/user_drill_turns_only_no_root_20261101_v01.png'
motion = BASE / 'inputs/motion_reference_upright_first10_20261031_v01/frames/R000028.png'
fullsource = Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G33-09\source.png')
first = BASE / 'coverage/source_frames/F000867.png'
initial = BASE / 'inputs/identity_full_drill_three_views.png'
user = BASE / 'inputs/user_drill_structure_20261101_v01.png'
report70 = BASE / 'review/sol_xhigh_goal_round70.json'
report86 = BASE / 'review/sol_xhigh_goal_round86.json'
registry = BASE / 'ASSET_REGISTRY.json'
expected = {
    current: '2d576fc092c80d5ba70508b983fd6bb06d96f16eabb91135d08c5405330c2c7a',
    sourceguide: '8539fcc1d586d0b62307c1face34d77bc8a94bcace0074cc2b99e568b58adea6',
    reviewed08: '663617241b31f5a39f5c6a5bae101639c6b90d5af42c98143e4bb3a3b4a71052',
    turns: '4edbd2131353520b61382bfcbcdfd6360cf71765a7b133cccfaef72c3150d8b2',
    report86: 'dd992783f6c7094857611e8ca5a081ab1622083e41589c3e50d70a54453abbae',
}
for p, digest in expected.items():
    assert sha(p) == digest, (str(p), sha(p))
refs = []

def copy_ref(src, filename, role):
    dst = INPUTS / filename
    if not dst.exists():
        shutil.copyfile(src, dst)
    assert sha(dst) == sha(src)
    refs.append(dict(**info(dst), source=info(src), operation='exact_byte_copy', role=role))

def crop_ref(src, box, filename, role):
    dst = INPUTS / filename
    im = Image.open(src)
    crop = im.crop(box)
    if dst.exists():
        previous = Image.open(dst)
        assert previous.size == crop.size and previous.mode == crop.mode and previous.tobytes() == crop.tobytes(), str(dst)
    else:
        crop.save(dst)
    refs.append(dict(**info(dst), source=info(src), source_xyxy=list(box), operation='readonly_original_pixel_crop_no_resampling', role=role))

copy_ref(sourceguide, 'ref1_ORIGINAL09_SOURCE_ACTION_APERTURE_CROP_ONLY.png', 'Original PV2339 exclusively controls action, round-open eye aperture/gaze, small neutral closed mouth, head/body ratio, hands, costume structure and source-visible framing. Red hair identity and red side-drill roots are not identity references.')
crop_ref(white, (30, 375, 610, 1072), 'ref2_CURRENT09_BODY_ONLY_NO_HEAD_ROOT_OR_COIL.png', 'Only current saved API body/clothes/hand/legs drawing continuity below the entire old shiny coil. Upper edge is a diagnostic crop, not output framing; source1 owns complete pose and costume. No old head, ear, bead, root or curl pixels submitted.')
crop_ref(white08, (285, 80, 656, 405), 'ref3_REVIEWED08_GRAY_BOB_FACE_LOW_EAR_NAPE_RELATION_ONLY.png', 'Both-reviewed08v04 short gray bob/face identity and same-ear posterior lower-bob/nape low-root relationship only. Not current09 expression, eye aperture, head tilt, scale, body action, fixed coil axis/length or geometry master. The small clipped attachment edge is not a complete coil model.')
copy_ref(turns, 'ref4_USER_TURNS_ONLY_NO_ROOT.png', 'Latest user broad gray opaque front/return folds and mint partition with progressive taper only. No root, fixed horizontal axis, length, turn count, hole count or forced exposed tip. Overlap can hide cavities.')

motion_box = (522, 266, 564, 311)
motion_crop = DIAG / 'R000028_HAIR_ONLY_OBSERVATION_NOT_SUBMITTED.png'
Image.open(motion).crop(motion_box).save(motion_crop)
Image.open(motion_crop).resize((42 * 4, 45 * 4), Image.Resampling.NEAREST).save(DIAG / 'R000028_HAIR_ONLY_OBSERVATION_4x.png')
motion_meta = dict(**info(motion_crop), source=info(motion), source_xyxy=list(motion_box), submitted_as_generation_reference=False, role='Read-only hair compression/rebound observation, no face/body/hand or identity authority. Do not adopt AI closed cone topology, one bead, materials, smile or body motion.')

head_box = (80, 65, 360, 375)
for src, suffix in [(white, 'white'), (black, 'black')]:
    crop = Image.open(src).crop(head_box)
    crop.save(DIAG / f'CURRENT09_HEAD_ROOT_BAD_COIL_DIAGNOSTIC_{suffix}_1x.png')
    crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.NEAREST).save(DIAG / f'CURRENT09_HEAD_ROOT_BAD_COIL_DIAGNOSTIC_{suffix}_2x.png')

registry_obj = json.loads(registry.read_text(encoding='utf-8-sig'))
snapshot = dict(captured_at_utc=datetime.now(timezone.utc).isoformat(), source_registry_path=str(registry), source_registry_sha256_at_read=sha(registry), entries={k: registry_obj[k] for k in ('ART-G33-09', 'ART-G33-08')}, central_written=False)
if not (RUN / 'REGISTRY_READONLY_SNAPSHOT.json').exists():
    write_new(RUN / 'REGISTRY_READONLY_SNAPSHOT.json', snapshot)
write_new(RUN / 'REF_INPUT_PROVENANCE.json', dict(preparation_only=True, submitted=False, refs=refs, motion_observation_only=motion_meta, excluded_references=['current09 full head/ear/root/shiny closed coil', 'full polished initial three-view', 'AI R28 full body or solid-cone bitmap', 'unreviewed07v09 and all withdrawn07 head references'], source_evidence=[info(p) for p in (current, white, black, fullsource, sourceguide, first, motion, initial, user, turns)], existing_api_result=info(current.with_name('result.json')), independent_current_failure_report=dict(path=str(report70), sha256=sha(report70)), reviewed08_independent_report=dict(path=str(report86), sha256=sha(report86)), art_pixels_modified=False, generation_calls=0, api_calls=0, central_writes=0))
print(json.dumps(dict(run=str(RUN), refs=[dict(path=r['path'],sha256=r['sha256'],size=r['size']) for r in refs], motion_crop=motion_meta), ensure_ascii=False, indent=2))
