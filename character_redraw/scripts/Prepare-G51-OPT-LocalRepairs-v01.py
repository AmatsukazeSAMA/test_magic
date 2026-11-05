"""Prepare two explicitly observed local fixes, without calling any provider."""
from pathlib import Path
import json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
items=[
 ('ART-G51-01','local_single_iris_v01',[[263,151,39,38],[321,148,39,38]],[
   'Replace only the separate black pupils and gray iris rings with ONE uniform solid dark-charcoal oval per eye plus the existing tiny white glint. Keep current round wide-open eye outline, gaze, upper/lower lash shape and expression, not the half-lidded opening of the eye-style crop.',
   'Keep the full current red short-sleeve maid dress, red stand collar, black bow/gold clasp, white apron/frills, black gloves and long black stockings/shoes, pose, warm skin, bob and continuous single drill unchanged. No two-tone ring, separate pupil, lower gray band, iris gradient or additional glints.'
 ]),
 ('OPT-BROOCH-PORTRAIT','local_source_scope_v01',[[85,0,651,300],[0,677,736,235]],[
   'The CURRENT source printed portrait has NO maid cap or black leaf ornament. Remove the invented cap and both black leaves completely and restore only the natural short gray bob crown. Preserve face angle, wide-open single dark eyes, tiny neutral straight mouth and current two-bead connected substantial drill.',
   'Remove the invented red cape, red neck bow, broad white pointed school collar and extra shoulder/chest figure. The source shows only a thin neck and narrow pale plain round-neck garment edge below the face. Retain only that minimal SOURCE-VISIBLE pale neckline fragment, with transparency below/outside it and the continuing drill. No other red except exactly two red hair beads. The large red bow OUTSIDE the original locket is an independent prop, never clothing.',
   'Do not draw the oval metal rim, halftone dots, gold filter, red accessory bow or caption. Do not complete hidden shoulders, torso or full maid clothing. Later oval clipping and tint/glints are separate post-production.'
 ])]
for id_,suffix,rects,changes in items:
    parent=base/f'drawings/{id_}/v01'
    run=parent/suffix
    if (run/'attempt.json').exists(): raise SystemExit('No automatic paid retry.')
    run.mkdir(parents=True,exist_ok=True)
    spec={'id':id_,'input_image':str(parent/'character_api_original.png'),
      'output_directory':str(run),'source_pose_guide':str(parent/'inputs/source_pose_guide.png'),
      'edit_regions_xywh':rects,'changes':changes,
      'eye_reference_role':'G02 single dark-charcoal iris plus one glint RENDERING ONLY; CURRENT reference 1 and source 4 wide-open eye outlines/gaze must remain wide open.',
      'intermediate_only':True,'mandatory_whole_character_imggen_after_local':True}
    target=run/'REPAIR_SPEC.json'
    if target.exists(): raise SystemExit('Preserve existing specification.')
    target.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)
