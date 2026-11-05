"""Record the user's explicit rejection of the exact current 15 side/route."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base=Path(__file__).resolve().parents[1]/'art/full_character_redraw_1080p_v01'
run=base/'drawings/ART-G33-15/v01/whole_imggen_source2365_frontshoulder_headcrop_puregray_v06'
raw=run/'character_imggen_original.png'
qa=run/'qa_black.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(raw)=='c03c252b16f6454e20246884d1616d312c93e518c81f105de660f52215ebc5f7'
out=base/'USER_G33_15_V06_WRONG_CURL_SIDE_20261102_v01.json'
assert not out.exists()
v={'recorded_utc':datetime.now(timezone.utc).isoformat(),
   'user_quote_verbatim':'钻发反了','id':'ART-G33-15',
   'user_attached_file':str(qa),'attached_file_sha256':sha(qa),
   'rejected_raw':str(raw),'rejected_raw_sha256':sha(raw),
   'decision':'rejected_wrong_curl_side_and_front_shoulder_route',
   'actual_root_observation':'Visible posterior/nape red beads lead a diagonal curl across rear neck and back-facing shoulder/frill. A rightward tail alone did not fulfill the required anatomical side/front-shoulder route.',
   'existing_user_requirements':['Fixed character anatomical LEFT, front usually viewerRIGHT; projection follows the actual turn, never screen-left shorthand.',
       'G33-15 and G12-20 curl must follow a continuous FRONT-shoulder route.'],
   'implementation_interpretation':'Remove visible wrong near posterior root and diagonal rear curl; preserve source pose and clothing. The low far-side LEFT root may be occluded by bob/neck/shoulder. Show a natural, reasonably sized gray ribbon segment around the same shoulder FRONT at the viewerRIGHT front neck/chest edge. Do not merely move the tail while retaining the rejected root.',
   'preserve_body_source_frame':2365,'source_pts':1262592,
   'first_exposure_range':[889,891],
   'mandatory_whole_imggen_after_local_repair':True,
   'fresh_primary_Sol_and_neighbor_continuity_review_required':True,
   'not_bound_or_accepted':True,'generation_calls':0}
out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(out),'sha256':sha(out)},ensure_ascii=False))
