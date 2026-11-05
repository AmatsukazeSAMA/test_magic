"""Prepare whole-character imagegen requests after actually inspected API prop cleanup.

No generation, image alteration, or visual acceptance is performed here.
"""
from pathlib import Path
import json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
for ident, eye in [('ART-G06-03', 'CLOSED eyes: retain two economical curved closed-lid marks; do not open them.'),
                   ('ART-G07-02', 'HALF-OPEN eyes: retain current sleepy opening and gaze, ONE flat solid dark-charcoal iris and one small white glint per eye; no separate pupil, iris rings, shading bands or gradients.')]:
    parent = base / 'drawings' / ident / 'v03/local_prop_cleanup_v01'
    assert (parent / 'qa_white.png').is_file()
    run = parent.parent / 'whole_imggen_v01'
    run.mkdir(exist_ok=True)
    refs = [str(parent / 'qa_white.png'), str(base / 'inputs/identity_full_drill_three_views_rot180.png')]
    prompt = f'''Redraw the WHOLE CURRENTLY VISIBLE CHARACTER from reference 1 as ONE coherent hand-drawn PV animation cel on genuine transparent alpha. Reference 1 is the corrected visible character on WHITE FOR INSPECTION ONLY: all this white empty space must be truly TRANSPARENT, not a white fill, and the character pose/crop/position must stay unchanged. This is complete unification after local removal of an independent circular foreground prop. Keep all currently visible head/hair, gray casual garment fragments, bare limbs and fingers; do not invent any torso or arm hidden in the large empty circular area. Do not reconnect the disconnected grasping fingers to the sleeve through unseen anatomy. Preserve all source-visible leg, hand and gray-garment contours, current framing and source eye state. {eye}

The large circular disc and ALL of its arcs/rim lines are independent props: output NO disc, NO circular outline, NO white crescent, NO gray circular fill, NO isolated black arc and NO prop residue. The empty areas beside the head and between hands/garment must remain clean genuine transparency. Keep actual fingers, hand creases and garment edge lines. Reference 1's pose already encodes the original visible occlusion; no additional source prop image is supplied to avoid restoring its discarded outlines.

The head is UPSIDE DOWN. Keep the anatomical LEFT paired red beads and substantial single gray/mint corkscrew attached on IMAGE LEFT, exactly as reference 1. Reference 2 was technically rotated 180 degrees for matching identity and full corkscrew mass only; ignore ALL school clothes, armbands, glossy shading and mint bob reflections. Keep the current continuous full drill, thick broad turns tapering naturally to a complete tip. No cut middle, tiny thin coil, extra drill, side flip or forced shoulder crossing. Plain ash-gray short bob, warm healthy light peach skin. Remove any remaining old PV RED HAIR triangular sliver at the nape beside the gray sleeve: hair is ash-gray there too, following existing hair/neck contours. Only the TWO attached beads are red; do not add a red garment or extra red nape ornament.

Unify every hair/head/neck/gray-sleeve connection with consistent economical slightly uneven dark PV ink and flat solid fills. No seam, pasted outline, floating hair, duplicate contour, gradients, skin airbrush, glossy highlights, fine individual strands, cast shadow or polished illustration rendering. Only the existing visible character extent on true transparent alpha. No props, captions, background, checkerboard, floor or contact shadow. High quality.'''
    request = {'id': ident, 'run': str(run), 'local_repair_parent': str(parent), 'refs': refs,
               'prompt': prompt, 'primary_pre_whole_inspection': 'Actually viewed corrected white and black QA; disc arcs removed. Whole stage must also remove residual old-red nape hair and freshly review all connections.'}
    (run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
    (run / 'BUILTIN_REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(run / 'BUILTIN_REQUEST.json')
