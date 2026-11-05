"""Prepare the user's two flat gray eye tones as a new whole-cel trial."""
from pathlib import Path
import json
import hashlib

base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
prior=base/'drawings/ART-G50-01/v02/eye_two_tone_trial_v01/whole_imggen_v01'
def save(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save(prior/'USER_REVISION_REQUEST.json', {
  'user_instruction':'不要渐变的，双色灰和偏白的灰',
  'status':'superseded_trial_gradient_rejected',
  'image_sha256':hashlib.sha256((prior/'character_imggen_original.png').read_bytes()).hexdigest(),
  'whole_film_style_adopted':False, 'user_accepted':False})
run=base/'drawings/ART-G50-01/v02/eye_two_tone_trial_v02/whole_imggen_v01'
run.mkdir(parents=True,exist_ok=True)
if (run/'request_imggen.json').exists(): raise SystemExit('Request already prepared; do not overwrite.')
refs=[base/'drawings/ART-G50-01/v02/character_api_original.png',prior/'character_imggen_original.png']
prompt='''Edit the CURRENT visible character in reference 1 as one coherent whole PV cel, changing ONLY the iris fills to the user-requested TWO FLAT GRAY TONES. Reference 2 is the previous eye trial: its shape and gaze are usable but its gradient eyes are explicitly REJECTED. Remove that gradient; do not reproduce it.

EYES: inside EACH existing iris, use only TWO solid opaque flat fills: medium neutral gray approximately #777C82 for the upper portion and a near-white pale gray approximately #E1E4E7 for the lower portion. A crisp simple curved/horizontal division separates the two blocks, like flat cut-paper cel paint. Any small pupil mark uses the SAME medium gray as the upper block, so it does not introduce a third dark fill. Keep dark outer ink and the existing small white catchlight. No smooth shading, gradient, blend, gray ramp, glow, radial texture, translucent transition, soft lighting or glossy multiple reflections inside either iris. Both eyes have the SAME medium-gray and whitish-gray palette, not differently colored left and right eyes. Do not leave the old solid-black eye fill.

Preserve reference 1's EXACT current eye contours, eye opening, eyelid angles, pupil centers/gaze, simple upper lashes, eyebrows, mouth smile, head tilt and expression. Keep the whole face and body style as this simple PV drawing; no realistic or polished eyes. Keep all other existing character features: short gray bob, two red beads, long substantial continuous gray/mint drill with complete lower tapered curl, attached white maid cap and two black leaves, warm peach skin, RED stand collar and shoulder panels, BLACK bow and gold clasp, white shoulder frills, complete palm-up black glove and bare forearm down to current bottom crop. Keep the whole wide framing and source cap-top clipping, do not zoom or recenter or crop fingers. Re-unify the whole visible character in one generation without pasted seams. True transparent alpha outside the character, no scene, black backdrop, white halo, checkerboard, props, text, FX, borders or shadow. High clarity; preserve the original wide composition at approximately 1920x1120 or higher. This is a separate two-flat-gray eye trial, not whole-film adoption.'''
(run/'prompt_imggen.txt').write_text(prompt+'\n',encoding='utf-8')
save(run/'request_imggen.json',{'id':'ART-G50-01','run':str(run),'refs':[str(p) for p in refs],
 'prompt':prompt,'local_repair_parent':None,'transparent_background':True,
 'quality_preference':'high','quality_parameter_exposed':False,'trial_only':True,
 'automatic_adoption':False,'user_revision':'不要渐变的，双色灰和偏白的灰',
 'edit_strategy':'Single whole-character built-in redraw with two flat iris tones; no pixel patch.',
 'supersedes_trial':str(prior)})
print(run/'request_imggen.json')
