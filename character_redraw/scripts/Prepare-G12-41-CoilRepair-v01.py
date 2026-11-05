"""Prepare a current-pose-preserving intermediate coil correction, no API call."""
from pathlib import Path
import argparse,json,hashlib
from PIL import Image
p=argparse.ArgumentParser(__doc__)
p.add_argument("phase",choices=["specification","request"])
a=p.parse_args()
base=Path(__file__).resolve().parent.parent/"art/full_character_redraw_1080p_v01"
parent=base/"drawings/ART-G12-41/v01"
run=parent/"local_coil_continuity_v01"
run.mkdir(parents=True,exist_ok=True)
if (run/"attempt.json").exists():raise SystemExit("Paid attempt exists; no automatic retry.")
save=lambda f,x:f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
previous=base/"drawings/ART-G12-40/v01/whole_imggen_v02/qa_white.png"
crop=run/"preceding_complete_coil_reference.png"
if a.phase=="specification":
    Image.open(previous).crop((830,345,970,625)).save(crop)
    save(run/"CONTINUITY_CROP_RECORD.json",{"source":str(previous),"source_sha256":hashlib.sha256(previous.read_bytes()).hexdigest(),
         "crop_xyxy":[830,345,970,625],"crop_only_no_art_pixel_changes":True,
         "purpose":"Reviewed 40 complete two-bead root, broad gray/mint middle and complete tapered tail; not pose or gaze reference."})
    save(run/"REPAIR_SPEC.json",{"id":"ART-G12-41","input_image":str(parent/"character_api_original.png"),
         "output_directory":str(run),"source_pose_guide":str(parent/"inputs/source_pose_guide.png"),
         "edit_regions_xywh":[[730,385,112,168]],"continuity_reference":str(crop),
         "changes":["Tighten current middle/lower coil pitch and reduce the extended tail, preserving the current root, two beads, broad upper turn and complete taper.",
                    "The tip near y535 is too low; on this 1216x944 master aim around y500..510 at the same current bead-root position. This restores previous 40 length at current head scale without copying its head tilt.",
                    "Do not change current upright head, upper-right gaze, wavy closed smile, two different open palms, source sleeves/cuffs or any clothing."],
         "intermediate_only":True,"mandatory_whole_character_imggen_after_local":True})
else:
    path=run/"LOCAL_REPAIR_REQUEST.json"
    req=json.loads(path.read_text(encoding="utf-8-sig"))
    prompt='''Make ONE masked intermediate correction to reference 1, the complete current transparent character. Tighten ONLY the stretched middle/lower drill and tail; preserve its current root, two red beads and broad upper turn. The whole master is 1216x944, first gray coil around y326 and excessive complete tip around y535. End the intact natural fine taper around y500..510 instead, shortening by about 25..35 pixels. Retain the same solid broad gray/mint coil volume, smooth continuous overlaps and thick-to-thin taper. Do not add a loop, sever or erase the middle/tip, or shrink the whole lock into a little spring.

Reference 2 is the preceding reviewed COMPLETE coil including bead root and tip, at its own scale. It controls turn pitch and length, not this current head tilt, gaze or body. Reference 3 is the CURRENT ORIGINAL PV pose/costume. Keep reference 1's current more upright head, open single dark-charcoal eyes with small white glints looking upper right, tiny wavy smile, warm peach skin, low left open palm and different high right open palm. Preserve all fingers, sleeve bends, white cuffs/frills/apron/waist/back ribbons, black standing collar and long sleeves, red chest bow/gold clasp and seated white cap with two attached black leaves.

Use the same economical black PV ink, flat gray bob and muted mint stripe. Output the whole visible transparent character, not an isolated patch. No background, words, props, new body, polished shading or new detail. This remains an intermediate; a mandatory one-master whole-character imagegen redraw follows before fresh static reviews.'''
    (run/"prompt.txt").write_text(prompt+"\n",encoding="utf-8")
    req["InputImages"]=[str(parent/"character_api_original.png"),str(crop),str(parent/"inputs/source_pose_guide.png")]
    req["Stage"]="GOAL G12-41 current-pose lower coil continuity intermediate; mandatory whole imggen follows"
    save(path,req)
print(json.dumps({"phase":a.phase,"run":str(run),"reference_crop":str(crop),"api_calls":0},ensure_ascii=False))
