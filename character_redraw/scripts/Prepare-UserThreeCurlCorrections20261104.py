"""Record exact three-image feedback and prepare its unissued whole repairs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
now = datetime.now(timezone.utc).isoformat()
review = base / 'review/USER_THREE_ROOT_COUNT_SIDE_CORRECTIONS_20261104_v01'
review.mkdir(exist_ok=False)
entries = []
for ident, first, issue in [
    ('ART-G33-48', 'direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16', '钻发位置有误：高根、肩外悬挂，改低LEFT根与肩前'),
    ('ART-X01-14', 'direct_first_api_source4078_noThreeView_flatBob_totalTurnBudget_postPassEye_v16', '图2多了一圈；并修现已独审证实的珠组错侧与断开'),
    ('ART-G13-28', 'direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12', '图三钻发左右反了：整束含两珠从viewerLEFT移到viewerRIGHT，不镜像身体')]:
    run = base / 'drawings' / ident / 'v01' / first
    entries.append({'id': ident, 'exact_rejected_raw': ev(run / 'character_api_original.png'), 'user_feedback': issue, 'user_accepted': False})
(review / 'USER_INSTRUCTION_AND_EXACT_ARTIFACTS.json').write_text(json.dumps({'recorded_utc': now, 'user_words': '钻发位置有误，图2多了一圈，图三钻发左右反了', 'entries': entries, 'total_count_includes_occluded_parts': True, 'unchanged_full_goal_active': True}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

parent = base / 'drawings/ART-X01-14/v01'
old = parent / 'whole_imggen_same_left_root_two_beads_connected_v01'
assert not (old / 'BUILTIN_GENERATION.json').exists()
q = read(old / 'REQUEST.json')
run = parent / 'whole_imggen_user_remove_one_turn_same_left_beads_v02'
run.mkdir(exist_ok=False)
prompt = Path(q['prompt']['path']).read_text(encoding='utf-8')
addition = '''USER CORRECTION: Image1 also has ONE EXTRA COMPLETE BROAD TURN. Remove one full substantial winding, rather than merely squeezing the three existing broad faces into a shorter space. There must be only TWO normal large turns followed by one distinctly narrower true small turn and the C tip. The small turn is not another large broad cylinder. Count every hidden shoulder/frill interval in that same total. Shorten the one bundle by the excess turn while preserving normal width of the upper two. Do this together with moving exactly two red beads from imageLEFT to the low imageRIGHT bob-to-coil junction.\n'''
pf = run / 'prompt_imggen.txt'
pf.write_text(addition + prompt, encoding='utf-8')
q.update({'prepared_utc': now, 'prompt': ev(pf), 'supersedes_unissued_PREP': ev(old / 'REQUEST.json'), 'user_feedback': ev(review / 'USER_INSTRUCTION_AND_EXACT_ARTIFACTS.json'), 'changed_hypothesis': 'Delete one complete excess broad winding and restore sameLEFT bob -> two beads -> coil; not a compressed unchanged three-large coil.'})
(run / 'REQUEST.json').write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'run': str(run), 'request': ev(run / 'REQUEST.json'), 'new_calls': 0}, ensure_ascii=False))

parent = base / 'drawings/ART-G13-28/v01'
first = parent / 'direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12'
run = parent / 'whole_imggen_user_restore_anatomical_left_low_root_v01'
run.mkdir(exist_ok=False)
refs = [first / 'character_api_original.png', parent / 'inputs/source_pose_guide.png']
prompt = '''Edit image1, the complete current character, to correct the drill hairstyle side. Image2 is ONLY this frame's original F1313 pose/expression/hands/costume/framing guide (actual wider F3763 drawing reference), not the red high double-drill identity.
The current complete gray coil and exactly two red beads are WRONG on imageLEFT, beside the near RIGHT ear. Remove that entire bundle and bead group from imageLEFT, restoring plain short gray bob/white shoulder frill/black clothing there. Reattach the only gray drill and the same exactly TWO red beads to anatomicalLEFT: imageRIGHT, at the low bob end behind the jaw beside the neck-collar. Main bob hair -> red bead pair -> gray coil must be a continuous same-side path. Do not mirror the whole character, face, cap leaves, arms or hands. Do not keep a second root or isolated beads on the old imageLEFT side.
The relocated coil rests in FRONT of its own imageRIGHT shoulder toward neck/chest. Normal broad first loops overlap the white shoulder-frill inner edge, red/black chest clothing, and may be partly hidden by the existing foreground vertical fingers, horizontal open palm and crossed sleeves. Keep the exact hands in place, no forced full visibility. Keep normal head-relative width; do not miniaturize or hang the whole coil outside the sleeve in air. The TOTAL single bundle including hidden intervals is TWO large turns, one true smaller turn with its own opaque gray return, then taper C. Hidden turns still count; no repeated full winding set below a hand/cuff. The C or small turn may be partly or completely hidden. Gray front and actual opaque gray returns stay continuous, real air gaps transparent; thin mint edge, neutral gray flat fill, slightly darker inner return allowed. No extra turn, solid column, metal plates or silver shine.
Preserve this frame's head tilt/yaw, jaw-neck-body relation, unequal round NORMAL-open eye outlines/gaze and their existing small white glints, and the NARROW small pink smile of image1/image2 (not the wider open smile of next G13-29). Dark gray interior plus lighter broad upward-convex lower gray cap, no central black pupil, exact eye silhouette unchanged. Preserve chest-crossing black forearms and both unequal bare hands: front lower hand fingers spread horizontally imageRIGHT, rear higher hand with vertical split fingers, original finger lengths/contact and white cuffs. Keep original black long-sleeved dress, red chest bow/gold clasp, white cap/two main black leaves/shoulder frills/cuffs/waist/apron visible top. Maintain actual square crop and visible waist from wider source, do not invent lower body. Simple restrained PV black lines/flat colors, no beautification or polished hair. Whole visible character coherently redrawn with only correct-side hair connection on genuine transparent alpha, no pink/captions/FX.'''
pf = run / 'prompt_imggen.txt'
pf.write_text(prompt + '\n', encoding='utf-8')
job = read(parent / 'JOB.json')
q = {'id': 'ART-G13-28', 'prepared_utc': now, 'operation': 'coherent_whole_existing_frame_repair', 'provider': 'built-in imagegen', 'calls_authorized': 1, 'automatic_retry': 0,
    'prompt': ev(pf), 'references': [ev(p) for p in refs], 'reference_roles': ['Exact wrong-side FIRST edit target', 'Own original PV pose/expression/costume/crop only'],
    'actual_root_viewed_all_inputs': True, 'source_frame': job['source_frame'], 'source_pts': job['source_pts'], 'source': ev(Path(job['source_image'])),
    'production_reference': job.get('production_reference'), 'eye_color_policy': read(root / 'image_defaults.json')['eye_color_policy'], 'curl_structure_policy_id': 'hollow_two_large_one_small_20261102_v04',
    'user_feedback': ev(review / 'USER_INSTRUCTION_AND_EXACT_ARTIFACTS.json'), 'local_pixel_edit_before_whole': False, 'normal_open_eye_separate_Python_after_new_art_pass': True,
    'user_accepted': False, 'dynamic_validated': False, 'status': 'prepared_no_call_yet'}
(run / 'REQUEST.json').write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'id': q['id'], 'run': str(run), 'request': ev(run / 'REQUEST.json'), 'new_calls': 0}, ensure_ascii=False))
