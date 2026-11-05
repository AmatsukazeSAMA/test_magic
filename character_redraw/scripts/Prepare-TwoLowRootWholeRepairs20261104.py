"""Freeze two root/connection repairs; no generation and no pixel changes."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
jobs = [
    ('ART-G33-48', 'direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16', 'whole_imggen_lower_root_own_shoulder_front_v01',
     '''Edit image1, the complete current character, preserving its own pose and simple PV drawing. Image2 is ONLY this frame's original pose/expression/costume/crop guide, not its red high hair. Fix the single gray drill attachment and depth coherently across the complete transparent character.
The two red beads are currently wrongly high beside the black cap leaves, above the closed eyelids, and the entire coil hangs in empty air outside the head/shoulder. Remove that high attachment and restore the short bob outline there. Put the SAME exactly two red beads down at the lowest imageRIGHT bob edge behind the jaw, at the ear-nape/neck-collar level. Gray bob hair must visibly feed into the beads, and the beads must directly feed into the only coil. One bundle, no stray neck beads or second stem.
From that low root, let normal broad gray ribbon loops fall IN FRONT of the character's own imageRIGHT shoulder, toward the neck/chest. Its broad gray face overlaps the inner white shoulder frill and black/red chest clothing. The real forward horizontal bare hand and cuff may cover its lower continuation; preserve those hands and their position. Do not leave the complete coil hanging in clear space outside the sleeve, do not move the shoulder or hands to display it, and do not miniaturize the coil. Total construction is exactly TWO large turns, then one genuinely smaller turn, then a tapering C. All segments hidden behind a hand or cuff still count; do not restart a complete turn set below an occluder. A short tip or only the upper turns may be visible. Gray front and opaque gray return remain continuous, actual air gaps are transparent; slight darker return is allowed. Thin mint edge, no silver highlights, no solid stacked discs.
Keep both eyes FULLY CLOSED, their lashes and tiny closed smile. Keep the head yaw/roll and head-neck-body relationship, unequal chest hand/finger groups, black long sleeves/long skirt, red chest bow/gold clasp, white cap/two main black leaves/frills/cuffs/apron/waist/back tails, crossed legs and BOTH complete original black shoes. No added iris or white eye glint. Keep original restrained irregular black line and flat gray fill, no polished rendering. Deliver only the complete visible character on genuine transparent alpha, same composition and framing.'''),
    ('ART-X01-14', 'direct_first_api_source4078_noThreeView_flatBob_totalTurnBudget_postPassEye_v16', 'whole_imggen_same_left_root_two_beads_connected_v01',
     '''Edit image1, preserving this complete character's own pose, simple PV style and transparent framing. Image2 is ONLY its own original F4078 pose/head/eyes/hands/clothing-cut/crop guide, not its red high hairstyle.
Fix one specific structural mistake: the two red beads are currently under the imageLEFT bob at the near RIGHT ear, while the only gray drill starts on imageRIGHT. Remove both red beads from imageLEFT and restore plain short gray bob there. Move exactly those TWO beads to the LOW imageRIGHT bob end behind the jaw, immediately ABOVE the existing coil's first broad turn, at left ear-nape/neck level. Gray main bob hair -> exactly two red beads -> gray coil must form one visibly continuous same-side attachment. Do not move the coil across the face, add another bundle or connect through an imaginary path across the back of the neck.
The existing imageRIGHT coil belongs to the character's anatomicalLEFT shoulder FRONT and should keep normal head-relative broad ribbon width, overlapping the inside of the white shoulder frill toward neck/chest. Root may partly hide under bob but not rise toward cap leaves. Exactly TWO large continuous turns, one TRUE smaller turn with its own opaque gray return, then a taper C for the ENTIRE one bundle including any frill-hidden continuation. No added set below overlap; do not lengthen or shrink. Gray front and gray return remain opaque with real air gaps transparent, thin mint edge, no silver light band or metallic shading.
Keep the own unequal NORMAL-open eye silhouettes, gaze and original small white glints; dark gray plus broad lighter gray lower cap and no central black pupil, with no change to the face. Keep the small closed smile and head roll, imageRIGHT raised narrow glove fingers, imageLEFT shoulder-side horizontally spread glove, separated hands and exact arm/elbow relationships. Keep muted gray-green short puff sleeves/body/skirt, black bow/gloves/stockings/shoes, gold clasp, white cap/frills/cuffs/apron/waist/backtails and two main black cap leaves. Keep exact source lower cut: imageLEFT shoe partly off-frame and imageRIGHT shoe near bottom, do not extend canvas to invent shoes. No extra costume, no polished hair highlights, no captions or background. Whole visible character coherently redrawn on genuine transparent alpha, preserve framing and silhouette except the bead/bob connection correction.''')
]
for ident, first, suffix, prompt in jobs:
    parent = base / 'drawings' / ident / 'v01'
    source_run = parent / first
    source = source_run / 'character_api_original.png'
    q = read(source_run / 'DIRECT_REQUEST.json')
    run = parent / suffix
    run.mkdir(exist_ok=False)
    pf = run / 'prompt_imggen.txt'
    pf.write_text(prompt + '\n', encoding='utf-8')
    refs = [source, parent / 'inputs/source_pose_guide.png']
    request = {'id': ident, 'prepared_utc': datetime.now(timezone.utc).isoformat(),
        'operation': 'coherent_whole_existing_frame_repair', 'provider': 'built-in imagegen',
        'calls_authorized': 1, 'automatic_retry': 0, 'prompt': ev(pf),
        'references': [ev(p) for p in refs],
        'reference_roles': ['Exact current FIRST edit target', 'Own original PV pose/expression/costume/crop only'],
        'actual_root_viewed_all_inputs': True, 'source_frame': q['source_frame'], 'source_pts': q['source_pts'],
        'source': q['source'], 'eye_color_policy': q['eye_color_policy'], 'curl_structure_policy_id': q['curl_structure_policy_id'],
        'local_pixel_edit_before_whole': False, 'normal_open_eye_separate_Python_after_new_art_pass': True,
        'user_accepted': False, 'dynamic_validated': False, 'status': 'prepared_no_call_yet'}
    (run / 'REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'id': ident, 'run': str(run), 'request': ev(run / 'REQUEST.json'), 'new_calls': 0}, ensure_ascii=False))
