"""Prepare whole redraws only after actual local-result inspection."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
configs=[
 ('ART-G51-01','local_single_iris_v01',
  '实际看raw与白黑，已变单色深灰眼并保持圆睁，小直嘴/红短袖服与手套袜鞋姿态保留。旧钻发中下卷仍像空隙过大的短弹簧，不能作新发型母型。whole须以完整identity补足圆厚连续中下卷和自然细尾，眼补丁也需整体统一。',
  '''Redraw the ENTIRE visible character of reference 1 in ONE cohesive transparent animation cel. This is the source's front full-body standing drawing, not a new generic pose. Reference 2 controls the exact current body/shoulder stance, hands near skirt, leg overlap, shoes, framing and garments. Preserve the RED SHORT-SLEEVED maid dress and red standing collar, BLACK chest bow with gold clasp, white shoulder frills and short white apron/waist/back ribbons, BLACK GLOVES and long BLACK STOCKINGS and shoes. No long black dress, bare hands, ankle-strap shoes, school vest or changed pose.

Keep CURRENT ROUND WIDE-OPEN eyes and neutral tiny straight mouth. The local repair has made each iris ONE solid dark-charcoal oval with a small white glint. Preserve that rendering and source gaze/opening; no separate black pupil inside a gray ring, no lower gray band or gradient. Reference 4 gives eye ink/color construction only, not its half-lidded expression.

Restore the substantial original identity corkscrew as you redraw the whole character. The old current lock is too thin and spring-like, with early tapering and big empty spaces. Reference 3 contains the COMPLETE original gray/mint thick-to-thin drill: use its rounded broad upper AND middle turns, solid hair volume and continuous tapering fine tip. Keep the same anatomical-left root (image right), exactly TWO red beads, and natural shoulder overlap. Do not copy the old miniature spring or make three thin floating ribbon slices. Do not cut out a middle segment, add another lock, or stretch a wire tail. Short ash-gray bob, no polished reflective green bob highlights. Identity reference clothes/shading are irrelevant.

Unify hair/root/neck, cap seated on bob with exactly two attached black leaves, frills and skin edges. Warm light peach skin, sparse dark Japanese hand-drawn PV ink, flat source fills and only restrained simple shadow shapes. Entire visible character generated coherently; no local patch collage. Real transparent alpha outside, no pink background, text, petals, frame, props or cast shadow. Preserve full shoes in the existing full-body crop. This whole redraw receives fresh primary and Sol review; no prior verdict is inherited.'''),
 ('OPT-BROOCH-PORTRAIT','local_source_scope_v01',
  '实际看raw及白黑，误加帽/黑叶和红披肩/大红结已去掉，保留细颈和极窄浅色圆领。两珠与连续宽钻发可见，嘴中性/圆睁眼保持。仍必须whole统一所有发根头颈领边，不沿用局修结论；原金框/网点/色滤另层。',
  '''Create ONE cohesive whole redraw of the visible portrait in reference 1 on genuine transparent alpha. Redraw all visible hair, face, neck and the tiny pale neckline fragment as a unified Japanese PV cel, not a patch or collage. Keep the current front-facing wide-open single dark-charcoal eyes with one small white glint each, neutral tiny straight mouth, warm peach face, rounded short ash-gray bob and exactly two red beads attached to one substantial gray/mint continuous corkscrew. Reference 2 controls the original printed portrait's face direction, simple expression and SOURCE-VISIBLE extent inside the locket. Reference 3 supplies the complete identity hair/coil volume only; ignore its school clothes and polished shading. Reference 4 is eye INK/COLOR only, never its half-lidded expression.

There is NO maid headband, white cap or black leaf ornament in this printed source portrait. Keep the natural gray bob crown without any headgear. There is NO red cape, red neck bow, scarf, broad pointed white school collar, chest, shoulder or maid uniform here. Draw only the thin visible neck and a narrow plain pale round-neck garment edge as in reference 1/source 2; all area below/outside that small fragment stays transparent except the naturally continuing hair curl. The only red in the character is the TWO hair beads. The large red bow OUTSIDE the original oval is an independent PROP and must never become clothing.

The full lock is rounded and substantial with continuous broad gray/mint turns and a natural fine taper. Do not sever the middle, add a second coil or turn it into a tiny spring. Preserve face expression, natural neck and grouped bob contours. Sparse economical dark PV ink, flat gray hair/muted mint stripe, warm peach skin; no glossy polished portrait, airbrush, fabric texture or hair highlight bands. Do not draw any metal oval, oval border, golden tint, halftone dots, golden glints, prop bow, caption, background or shadow. Original oval clipping/tint/glints and occlusion are post-production. Return the entire currently visible character portrait coherently, with real transparent alpha, for new independent review.''')]
for id_,suffix,note,prompt in configs:
    parent=base/f'drawings/{id_}/v01'
    local=parent/suffix
    run=parent/'whole_imggen_v01'
    if (run/'request_imggen.json').exists(): raise SystemExit('Existing request; no duplicate submission.')
    run.mkdir(parents=True,exist_ok=True)
    current=local/'character_api_original.png'
    review={'id':id_,'image':str(current),'image_sha256':hashlib.sha256(current.read_bytes()).hexdigest(),
      'reviewed_utc':datetime.now(timezone.utc).isoformat(),'actual_viewed_inputs':[str(local/n) for n in ['character_api_original.png','qa_white.png','qa_black.png']]+[str(parent/'inputs/source_pose_guide.png')],
      'status':'intermediate_only_requires_whole_character_redraw','observation':note,'user_accepted':False,'dynamic_validated':False}
    (local/'PRIMARY_INTERMEDIATE_REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    refs=[str(current),str(parent/'inputs/source_pose_guide.png'),str(base/'inputs/identity_full_drill_three_views.png'),str(base/'inputs/eye_G02-01_F100.png')]
    request={'id':id_,'run':str(run),'refs':refs,'prompt':prompt,'transparent_background':True,
      'local_repair_parent':str(local),'user_quality_preference':'high','builtin_quality_parameter_exposed':False}
    (run/'request_imggen.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (run/'prompt_imggen.txt').write_text(prompt+'\n',encoding='utf-8')
    print(run/'request_imggen.json')
