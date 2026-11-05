"""Prepare two distinct existing-art repairs; does not generate images."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'art/full_character_redraw_1080p_v01'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
coil=BASE/'drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png'

def prepare(ident,name,refs,prompt,defect,change):
    run=BASE/'drawings'/ident/'v01'/name
    run.mkdir(exist_ok=False)
    pf=run/'prompt_imggen.txt';pf.write_text(prompt+'\n',encoding='utf-8')
    request={'id':ident,'provider':'built-in imagegen','calls_authorized':1,
             'prompt':ev(pf),'references':[ev(p) for p in refs],
             'transparent_background':True,'defect':defect,'changed_hypothesis':change,
             'root_actually_viewed_all_references':True,'user_accepted':False,
             'created_utc':datetime.now(timezone.utc).isoformat()}
    (run/'REQUEST.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'run':str(run),'request':ev(run/'REQUEST.json')},ensure_ascii=False))

parent=BASE/'drawings/ART-X01-15/v01'
prepare('ART-X01-15','whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02',
        [parent/'whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01/character_imggen_original.png',coil,parent/'inputs/source_pose_guide.png'],
'''Edit image1 as one coherent whole visible character on true transparent alpha. Image2 ONLY supplies the complete continuous ribbon topology, including its independent smaller front/opaque return before the C tip. Image3 is this character own original PV pose/costume cut/visibility, no copied pose from any neighboring drawing.
Image1's two LARGE turns now have normal mass and normal large outer diameters. Keep those restored diameters and the thinner open gray band; do not regress to a tiny narrow collar ornament or thicken into a solid cylinder. The current defect is at the bottom: second Large goes straight into C, so an independent TRUE SMALL TURN is missing. Rebuild the continuous lower path so there are exactly two Large turns, then one distinctly smaller gray front which bends through its own opaque gray return, THEN a separate continuous tapering C tip. The C itself is not the small turn. Follow image2's readable small front/return/C relationship, never add a third large turn.
Fit this complete 2L+small+C construction within the current bob-root-to-waist-tip envelope by making the axial spacing more compact; do not elongate the lock down the apron or remove a main large turn to make space. No strip rings, stacked discs, sealed rectangular tubes or solid cones. Only actual air is transparent; real gray inner returns are opaque. Mint is a narrow material edge, not green lighting. The current top white area belongs to underlying white shoulder frill: do not force-delete white cloth to manufacture an alpha hole.
Keep current correct low anatomicalLEFT root at imageRIGHT, short gray bob connects through exactly two red beads into the same single lock at neck/shoulder front. Natural overlaps onto original white frill/graygreen chest/black bow, never move to shoulder exterior. Keep own head left-roll, face angle, unequal eye opening and original small white glints, small smile, both black-glove palmsup and actual short fingers/thumbs, bare arms/white cuffs, graygreen short puff-sleeve maid/black chest bow/gold clasp/white apron and rear ribbons, original leg axes/stockings/shoes. Right eye stays narrowed, do not open it to a round eye. Right source shoe-bottom cropping remains source visibility, not a new sole. No petals/text/background/new props.
Original handdrawn sparse irregular black line and simple gray/mint material fills, no metallic silver highlights or dense refined hair/garment linework. Preserve current eye shape and small highlights; eyes will be corrected separately by local Python only AFTER whole-character review. Return same whole visible character and portrait framing, not an insert, diagram or comparison.''',
        'Missing independent true Small between second Large and C; main diameters were restored.',
        'Remove neighboring whole-body mass reference; use complete coil topology crop plus own source. Preserve restored large diameter, compact axial pitch instead of stretching total length.')

parent=BASE/'drawings/ART-G33-50/v01'
prepare('ART-G33-50','whole_imggen_restore_far_left_root_with_reviewed_neighbor_context_v01',
        [parent/'direct_first_api_source2523_ownFarSideContext_normalCoil_roundArc_v19/character_api_original.png',
         BASE/'drawings/ART-G33-49/v01/whole_imggen_restore_far_left_root_shoulderfront_v01/character_imggen_original.png',
         parent/'inputs/source_pose_guide.png',coil],
'''Edit image1 as a coherent whole current visible character on true transparent alpha. Its source action is image3 ONLY. Image2 is the actually reviewed immediately preceding same-yaw character, used ONLY for low anatomicalLEFT bead/root side and shoulderFRONT route; do not freeze its face, hand angles, legs or skirt. Image4 supplies complete wide-gray ribbon 2Large+trueSmall+C construction only.
Current image1 head is turned toward imageRIGHT. The clearly exposed ear at imageLEFT is the near anatomicalRIGHT ear. Its two red beads and whole gray coil are incorrectly attached there. REMOVE that entire wrong nearRIGHT bead/coil attachment, restore continuous ordinary short bob at that near ear and ordinary source white shoulder/back clothing behind it. Do not retain leftover red specks, spare beads or a second ghost coil on imageLEFT.
Attach the unique pair of red beads LOW at far anatomicalLEFT bob/nape edge, on imageRIGHT behind the jaw, not at cap/temple. Bob hair→exactly two red beads→one gray lock must visibly connect wherever not genuinely occluded. Like image2's side relation, the far root may be partly hidden by own bob/jaw; hiding is allowed, swapping it back onto the exposed near ear is forbidden. Body/head must not mirror or turn front to make the repair easy.
The normal-size gray ribbon hangs forward over the anatomicalLEFT shoulder at imageRIGHT neck/chest and inner white shoulder frill. Own downward chest fingers, white cuff and crossed foreground sleeve may naturally hide middle/lower ribbon. Keep normal exposed large-turn diameter and band mass; do not put a tiny full coil outside the shoulder to display everything. Count the occluded middle material in the total: exactly two LARGE turns, an independent SMALL gray front/opaque return, then continuous tapering C. Do not restart a second coil below the sleeve or extend the lock to waist. No sealed tubes/rectangular column/solid cone/discs. Opaque gray returns continuous with broad fronts, only true air transparent, mint narrow edge. Moderate thinner first-band thickness independently from normal first diameter.
Keep image1 with its OWN image3: head/neck yaw and gaze toward camera by eyes only; two normally open unequal irises and original tiny glints, small closed curved smile. Both forearms more horizontal than image2: high hand long index points leftward, other folded fingers bend down; chest hand's separated long fingers hang DOWN, cuff angles/occlusion distinct. Keep exact body lean, long black/red/white maid collar and bow/gold center, apron toward imageRIGHT, black skirt swinging imageLEFT, rear white waist ribbons to left, spread legs and both complete strap shoes. Do not copy image2's upright finger, horizontal chest fingers, feet-together leg stance or skirt folds. No source text/pink background/props.
Sparse irregular original PV linework and simple neutral gray/mint hair, no silver highlights or polished new line density. Eye interiors may use quiet desaturated gray without a central black pupil, but retain current original contour/glints; all normal-open dance eyes are separately adjusted to user-selected B style by local Python AFTER art passes. Whole visible character only, no diagram/comparison or pasted seams.''',
        'Wrong nearRIGHT low attachment and rear/outside shoulder route on right-facing head.',
        'Replace narrow no-eye ear/root strip hypothesis with complete actually reviewed same-yaw neighbor context; source3 exclusively owns changed hands/pose. Existing whole builtin repair, no official FIRST retry.')
