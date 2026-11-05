"""Record two independent whole-character imagegen requests, without adoption."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from PIL import Image

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def request(id, run, refs, prompt, parent=None, **extra):
    run.mkdir(parents=True, exist_ok=True)
    target = run / 'request_imggen.json'
    if target.exists():
        raise SystemExit(f'Request already prepared: {target}; do not overwrite or resubmit.')
    (run / 'prompt_imggen.txt').write_text(prompt + '\n', encoding='utf-8')
    save(target, dict(id=id, run=str(run), refs=[str(p) for p in refs], prompt=prompt,
        local_repair_parent=str(parent) if parent else None,
        transparent_background=True, quality_preference='high', quality_parameter_exposed=False,
        prepared_utc=datetime.now(timezone.utc).isoformat(), **extra))
    print(str(target))

g45 = base / 'drawings/ART-G45-01/v01'
local = g45 / 'local_restore_source_visible_collar_v02'
local_image = local / 'character_api_original.png'
save(local / 'PRIMARY_INTERMEDIATE_REVIEW.json', {
    'id': 'ART-G45-01', 'image': str(local_image),
    'sha256': hashlib.sha256(local_image.read_bytes()).hexdigest(),
    'actual_viewed_paths': [str(local / f'qa_{c}.png') for c in ['white', 'black']] +
        [str(g45 / 'inputs/source_pose_guide.png'), str(local / 'original_visible_collar_detail.png')],
    'status': 'intermediate_repair_required', 'user_accepted': False,
    'observation': 'Black stand collar and small red cloth edge restored, but API also drew independent basket and bread despite local mask. Preserve return as failure evidence, never adopt this sprite or propagate its props. Whole-image repair will use prior coherent prop-free body plus a cropped collar reference and untouched source. No further local API call.',
    'whole_redraw_required': True})
run45 = g45 / 'whole_imggen_v02'
run45.mkdir(parents=True, exist_ok=True)
collar_crop = run45 / 'corrected_local_collar_detail.png'
box = (785, 410, 925, 565)
with Image.open(local_image) as im:
    im.crop(box).save(collar_crop)
save(run45 / 'COLLAR_REFERENCE_PROVENANCE.json', {
    'source_image': str(local_image), 'source_sha256': hashlib.sha256(local_image.read_bytes()).hexdigest(),
    'crop_xyxy': list(box), 'scope': 'Reference crop only, not pasted into production pixels. Exclude any basket/bread pixels from final character.',
    'previous_cyan_annotation_excluded': True})
prompt45 = '''Redraw the WHOLE currently visible character as ONE coherent hand-drawn PV animation cel with genuine transparent alpha. Reference 1 is the existing coherent PROP-FREE body and exact action/crop/negative space to preserve. Restore only its missing small black stand collar joining the visible neck and the narrow red clothing edge beside the original foreground basket, using references 2 and 3. Re-unify head, neck, collar, hair, cap, shoulders, cuff, hand and costume ink in this whole generation.

Reference 2 is a close crop of a local repair: it shows the CORRECT black collar below the chin and the narrow red clothing strip. Brown basket and yellow bread accidentally visible in this crop are INDEPENDENT PROPS and MUST NOT appear in the output. Reference 3 is the untouched original action, including the basket/bread ONLY as an occlusion guide; never copy the original red twin hairstyle or its props, captions or pink background. Under the visible chin, keep the little black stand collar, and below it the small source-visible red strip at the side of the bread. Do not erase those genuinely visible clothing pixels, and do not invent a full hidden chest, red bow, belly or second hand behind the prop.

PRESERVE THE TRANSPARENT PROP HOLE from reference 1. The large original basket-and-bread region between the knees and chest is transparent, with only the existing ONE foreground bare gripping hand and its attached white cuff / black forearm crossing it. No basket rim, weave, handle, bread, brown/yellow fill, solid placeholder or outline. Do not fill that hole with clothes or anatomy. Keep the exact existing gripping fingers and near forearm, bent legs, skirt/apron, black ankle shoes and long white back-waist bow tails from reference 1. No added open palms, hidden far hand or extra fingers.

Keep reference 1's gray bob, two red beads and substantial complete continuous gray/muted-mint corkscrew with its full lower taper and curled tip. Its present length and turns are already correct; do not shorten, disconnect or move the root. Attached white cap and exactly two pointed black leaves sharing one mount. Warm light peach skin, source black maid uniform and white ruffles/apron. Preserve current open monochrome dark eyes, gaze and smile. Simple PV dark ink, flat fills and economical folds, no glossy polishing. The whole subject stays in the same square framing and source-visible action, with real alpha outside visible character AND inside the independent prop occlusion. No scene, text, basket, bread, FX, shadow, checkerboard or pasted join.'''
request('ART-G45-01', run45,
    [g45 / 'whole_imggen_v01/character_imggen_original.png', collar_crop, g45 / 'inputs/source_pose_guide.png'],
    prompt45, local)

g50 = base / 'drawings/ART-G50-01/v02'
eye = Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-fd99dc88-3446-4a93-b22e-14304c1f0cd0.png')
run50 = g50 / 'eye_two_tone_trial_v01/whole_imggen_v01'
run50.mkdir(parents=True, exist_ok=True)
eye_copy = run50 / 'user_eye_reference_original.png'
eye_copy.write_bytes(eye.read_bytes())
prompt50 = '''Use case: identity-preserve. Make a single WHOLE-character redraw of reference 1 for a controlled eye-color rendering trial. Reference 1 is the transparent production cel, NOT a black-background painting. Reference 2 is EYE COLOR/CONSTRUCTION ONLY. The requested two-tone eyes mean a dark charcoal pupil within a softer medium cool-gray iris in EACH eye, like reference 2; BOTH eyes have the same palette. Do not make left and right eyes different colors.

Change only how the interiors of the existing eyes are rendered: distinguish the charcoal/near-black pupil from the neutral gray iris, with a restrained lighter gray lower area and the small white catchlight. Keep the CURRENT eye outlines, opening, eyelid angle, pupil centers/gaze, economical dark upper lashes, eyebrows, gentle smile and facial expression. The tiny reference's eye shape and glossy painting style must not replace this PV face. Keep the two gray values simple and readable, no rainbow colors, elaborate radial iris texture, multiple sparkles or photoreal eyes.

Redraw and unify the entire CURRENTLY VISIBLE character in one pass while preserving all other parts of reference 1: gray bob and grouped bangs, warm peach skin, two red beads, the complete substantial gray/muted-mint drill with continuous middle and tapering curled tip, attached white maid cap and two black leaves, exact top crop of the cap/ornament, RED stand collar and shoulder panels, BLACK bow with gold clasp, white frills, complete raised black palm-up glove with the same fingers and bare forearm continuing down to the same bottom crop. This shot's red collar / black bow are correct. Do not swap them to the earlier black collar / red bow uniform, add a white wrist cuff, lose fingertips, shorten the drill, change the pose/crop, recenter or zoom. Keep source-like simple PV ink density and flat body fills. True transparent alpha outside the visible person, no black or colored backdrop, white halo, checkerboard, text, props, petals, FX, cast shadow or border. Preserve the full wide cel composition at high clarity, approximately 1856 by 1088 pixels or higher without a tighter crop. This is a separate trial, not automatic adoption of a new whole-film eye standard.'''
request('ART-G50-01', run50, [g50 / 'character_api_original.png', eye_copy], prompt50,
    trial_only=True, automatic_adoption=False,
    edit_strategy='One whole-character built-in generation with eye tonal change; no manual pixel patch or API local stage.',
    baseline_image=str(g50 / 'character_api_original.png'))
