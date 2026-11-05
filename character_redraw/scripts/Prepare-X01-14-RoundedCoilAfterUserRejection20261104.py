"""Supersede X01-14's column-like art without rewriting historical proofs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
save = lambda p, q: p.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
now = datetime.now(timezone.utc).isoformat()
ident = 'ART-X01-14'
parent = base / 'drawings' / ident / 'v01'
eye_run = parent / 'py_post_pass_user_minus_one_turn_two_gray_v01'
target = eye_run / 'character_eye_gray_local.png'
old_whole = parent / 'whole_imggen_user_remove_one_turn_same_left_beads_v02'
reference = base / 'drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png'
verification = read(eye_run / 'VERIFICATION.json')
assert verification['outside_mask_changed_pixels'] == 0 and verification['alpha_changed_pixels'] == 0
assert verification['output']['sha256'] == sha(target)
folder = base / 'review/USER_X01_14_RECTANGULAR_COIL_REJECTION_20261104_v01'
folder.mkdir(exist_ok=False)
registry_path = base / 'ASSET_REGISTRY.json'
registry = read(registry_path)
old = registry[ident]
assert old['sha256'] == verification['source']['sha256']
save(folder / 'SELECTED_ART_BEFORE_USER_REJECTION.json', old)
record = {'id': ident, 'recorded_utc': now, 'user_verbatim': '什么长方形圆柱体，修改钻发',
    'exact_user_image': ev(eye_run / 'qa_black.png'), 'exact_user_RGBA': ev(target),
    'same_hair_parent': verification['source'], 'eye_only_verification': ev(eye_run / 'VERIFICATION.json'),
    'art_status': 'user_rejected_requires_shape_repair',
    'root_actual_observation': 'Broad turn faces have almost straight sides and parallel slab-like ends, creating a rectangular cylinder/stacked sleeve reading. Correct side/count does not establish acceptable rounded hollow hair-band geometry.',
    'required_change': 'Restore naturally rounded tapering continuous helical hair ribbon using approved complete-coil reference; keep lowLEFT two beads, shoulder-front route and total2Large+trueSmall+C including occlusion.',
    'eye_scoped_pass_is_not_whole_art_acceptance': True, 'historical_art_reviews_unchanged': True,
    'user_accepted': False, 'generation_calls_by_this_record': 0}
rp = folder / 'USER_REJECTION_AND_REQUIRED_ROUNDED_RIBBON.json'
save(rp, record)
registry[ident] = {**old, 'status': 'repair_required', 'primary_static_pass': False,
    'independent_static_pass': False, 'user_accepted': False,
    'historical_review_pass_flags_before_user_rejection': {k: old[k] for k in ('primary_static_pass', 'independent_static_pass')},
    'review_superseded_by_user_rejection': ev(rp)}
save(registry_path, registry)

run = parent / 'whole_imggen_user_remove_rectangular_column_round_ribbon_v03'
run.mkdir(exist_ok=False)
prompt = '''Edit image1, the complete existing character. Change ONLY the drill braid's DRAWN SHAPE to the naturally rounded hollow hair ribbon shown in image2. The user rejects image1 because its turns look like rectangular cylindrical sleeves stacked on a pole.
Replace those straight-sided panels and flat slab ends with a continuous soft curved corkscrew ribbon: each broad front bulges in a smooth rounded arc, gently narrows as it curves into its real opaque gray return, and then sweeps into the next turn. The rims are rounded, oblique, asymmetrical curves in perspective. Clearly read as one flowing strand of hair with open space between successive turns, not three detached rigid cups, a cut hose, blocky cylinders, a rectangular tower or a mint line drawn around a solid rod. Keep the gray return surfaces real and opaque; only genuine air gaps are transparent. No artificial hole count, no digging out gray material. Image2 governs only this exact flowing gray-front/gray-return/mint-edge construction; do not copy its clothing, skin, root position, camera or size.
Keep the CORRECT existing low imageRIGHT/anatomicalLEFT connection: gray bob -> exactly TWO red beads -> the single gray coil, resting at the FRONT of the same shoulder toward neck/chest, overlapping its white frill/black bow. Keep normal upper-loop width. The TOTAL single bundle is exactly TWO LARGE rounded turns, then ONE distinctly SMALLER true turn with its own return, then tapering C; count any occluded segments in that same budget. Do not add a third large turn, extend its length, restart after overlap, shrink the braid into an ornament or move it to the other ear. Keep the two beads and root where they are now.
Preserve EVERYTHING ELSE from image1: face/head angle and outline, unequal normal-open eyes and exact gaze/small white glints, dark-and-light-gray eye interior with NO black central pupil, small closed smile, short neutral gray bob, white maid cap and two black leaves, both separate black-gloved hands/fingers and arm/elbow positions, gray-green short puff sleeves/dress, black bow/stockings/shoes, gold clasp, white frills/apron/waist/backtails, legs and original bottom shoe crop. Do not mirror, re-pose, beautify, recolor the costume, add hair highlights or sharpen the eyes. Keep simple irregular PV black lines and flat gray/mint hair color. Return the entire character on genuine transparent alpha with the same tall composition. Only the rounded braid geometry needs correction.'''
pf = run / 'prompt_imggen.txt'
pf.write_text(prompt + '\n', encoding='utf-8')
q = {'id': ident, 'prepared_utc': now, 'operation': 'coherent_whole_existing_frame_repair', 'provider': 'built-in imagegen', 'calls_authorized': 1, 'automatic_retry': 0,
    'prompt': ev(pf), 'references': [ev(target), ev(reference)],
    'reference_roles': ['Exact user-rejected current RGBA edit target; preserve pose and all noncoil features', 'Approved complete rounded helical ribbon construction only; no incidental body/root transfer'],
    'actual_root_viewed_all_inputs': True, 'user_rejection': ev(rp), 'source_frame': 4078, 'source_pts': 2177648,
    'source': read(old_whole / 'REQUEST.json')['source'], 'eye_color_policy': read(root / 'image_defaults.json')['eye_color_policy'], 'curl_structure_policy_id': 'hollow_two_large_one_small_20261102_v04',
    'local_pixel_edit_before_whole': False, 'previous_eye_verification_not_inherited_to_new_whole': True,
    'normal_open_eye_separate_Python_after_new_art_pass': True, 'user_accepted': False, 'dynamic_validated': False,
    'status': 'prepared_no_call_yet'}
save(run / 'REQUEST.json', q)
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(folder / 'GOAL_EXECUTION_BEFORE_USER_COLUMN_REJECTION.json', goal)
goal['latest_user_X01_14_rectangular_column_rejection'] = ev(rp)
goal['updated_utc'] = now
save(goal_path, goal)
print(json.dumps({'rejection': ev(rp), 'request': ev(run / 'REQUEST.json'), 'run': str(run), 'status': 'repair_required', 'new_calls': 0}, ensure_ascii=False))
