"""Explicit user-requested palette trial; never changes production selection."""
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
run=base/'drawings/ART-G51-01/v01/ending_palette_gray_green_trial_v01'
if (run/'request_imggen.json').exists(): raise SystemExit('Existing trial request; no duplicate.')
run.mkdir(parents=True,exist_ok=True)
source=base/'drawings/ART-G51-01/v01/whole_imggen_v01/character_imggen_original.png'
prompt='''Make a restrained COLOR PALETTE TRIAL of this exact complete transparent character. Change ONLY the currently bright RED CLOTHING fabric (standing collar, short puff sleeves, bodice, skirt and small exposed side fabric) to a harmonious muted medium GRAY-GREEN / sage green, approximately #7E9586 with simple deeper gray-green shadow fills around #596E61. This should coordinate with her ash-gray bob and the mint stripe in the drill. Keep the fabric distinctly desaturated gray-green, not vivid emerald, teal, turquoise, olive yellow or blue.

Preserve the exact original drawing, figure pose, proportions, hand and leg placement, cap/black double leaves, facial expression, single dark-charcoal eyes and tiny white glints, healthy warm peach skin, gray/mint continuous substantial drill and exactly TWO RED hair beads. The two red beads remain red as a small accent. Keep the large chest BOW, gloves, long stockings and shoes BLACK, the clasp GOLD and apron/frills/waist/back ribbons warm WHITE. Do not recolor hair, skin, beads, eyes, white cloth, black accessories or line art. No new costume pieces, no changed skirt length, sleeves, body, face or anatomy.

Render this as one cohesive full-character transparent image, preserving simplified PV flat-color ink rather than making a polished fashion illustration. No background, checkerboard, colored halo, words, palette swatches or frame. Genuine alpha outside the character. This is one exploratory color variant for user review, not automatic replacement of the red production version.'''
request={'id':'ART-G51-01','run':str(run),'refs':[str(source)],'prompt':prompt,
 'transparent_background':True,'user_quality_preference':'high','builtin_quality_parameter_exposed':False,
 'user_request':'最后换色尝试灰绿色，与灰发协调','trial_only':True,'production_selection_changed':False,
 'reference_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
(run/'request_imggen.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(run/'prompt_imggen.txt').write_text(prompt+'\n',encoding='utf-8')
print(run/'request_imggen.json')
