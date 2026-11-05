from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil
from PIL import Image,ImageDraw
JOBROOT=Path(__file__).resolve().parent
BASE=JOBROOT.parents[2]
ROOT=BASE.parent.parent
RUN=JOBROOT/'prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(p,v):
 assert not p.exists(),p
 p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
job=read(JOBROOT/'JOB.json');reg=read(JOBROOT/'REGISTRATION_PLAN.json')
registry=read(BASE/'ASSET_REGISTRY.json');prev=registry['ART-G51-09']
assert job['id']=='ART-G51-10' and job['source_frame']==4625 and job['source_pts']==2469664
assert job['previous_in_family']=='ART-G51-09'
assert 'ART-G51-10' not in registry
assert prev['sha256']=='9b4cbec6a9496613b20f6136bf7b5ee10470a53b0ed0de61278f078bf4d18dcc'
assert prev['primary_static_pass'] and prev['independent_static_pass']
src=Path(job['source_image']);assert sha(src)==job['source_image_sha256']
assert sha(prev['image'])==prev['sha256']
files=[p for p in JOBROOT.rglob('*') if p.is_file()]
for p in files:
 assert p.name not in ['attempt.json','result.json','character_api_original.png','character_imggen_original.png','ROOT_API_EXECUTION_RECEIPT.json','response_headers.txt'],p
assert not RUN.exists();RUN.mkdir();(RUN/'inputs').mkdir()
save(RUN/'PRE_FIRST_LOCAL_STATE_AUDIT.json',{'id':job['id'],'checked_utc':datetime.now(timezone.utc).isoformat(),'source':ev(src),'JOB':ev(JOBROOT/'JOB.json'),'REGISTRATION_PLAN':ev(JOBROOT/'REGISTRATION_PLAN.json'),'files_present_before_PREP':[ev(p) for p in files],'registry_target_absent':True,'no_existing_attempt_raw_result_or_UNKNOWN_in_target_tree':True,'review_search_hits':'Only historical progress/policy/source-review files; no G51-10 generated/request-result evidence found.','scope':'Local exact-target tree and current registry; no network or recovery attempt','submitted':False})
save(RUN/'PREDECESSOR_DUAL_REVIEW_AND_ROOT_RELEASE_GATE.json',{'id':job['id'],'previous_in_family':prev,'root_and_Sol_static_candidate_known':True,'scope':'09 passed static; only a small interior cloth color/ink crop may be sent. Its face/pose/camera/curl/lowalpha or front-depthP2 do not transfer.','root_release_received':False,'API_calls':0,'native_calls':0})
old=BASE/'drawings/ART-G51-08/v01/prep_first_api_source4613_relaxedeyes_bentforearm_single_glove_fullshoes_graygreen_v06/inputs'
spec=[
 ('ref1_ORIGINAL4625_COMPLETE_UNMASKED_TWO_UNEQUAL_GLOVES_FULLSHOES.png',JOBROOT/'inputs/source_pose_guide.png',None,'Own4625 sole pose/expression/handcount/skirt/backties/legs/shoes/layout authority. Original high red curls and pink petals are not output.'),
 ('ref2_PREVIOUS09_SAFE_INTERIOR_GRAYGREEN_CLOTH_LINE.png',Path(prev['image']),(423,851,486,881),'Only previous09 interior graygreen cloth and sparse black ink. No face/pose/hand/camera/curl/depth or body contour transfer.'),
 ('ref3_USER_APPROVED_X01_CURL_RENDERING_ONLY.png',BASE/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png',None,'Userapproved curl drawing only:two large plus smallC,actual opaque gray returns and thinmint. Not wholeperson/size/axis/rootprojection.'),
 ('ref4_SAFE_GRAY_UPPER_BOB_CAP_FRINGE_NO_EYES_DOTS_COIL.png',old/'ref4v02_GRAY_BOB_CAP_FRINGE_IDENTITY_ONLY_NO_EYES_DOTS_COIL.png',None,'Gray rounded upperbob/fringe/cap material identity only. No eyes,under-eye dots,oldcoil or body. Own4625 overrides headtilt and cap projection.'),
 ('ref5_OWN4625_TIGHT_EYES_UPPER_OUTER_LINES_NO_UNDEREYE_POINTS.png',src,(860,215,979,253),'Own4625 eye opening,white/upperouterlash contours and gaze only; tight rectangle avoids separated under-eye points. Mouth is only own full guide/text tinyclosedmouth, not anotherframe.')
]
refs=[]
for name,p,box,role in spec:
 dest=RUN/'inputs'/name
 if box:Image.open(p).crop(box).save(dest)
 else:shutil.copyfile(p,dest)
 item={**ev(dest),'source':ev(p),'operation':'readonly rectangle crop; no artpixel edits' if box else 'unchanged bytecopy','role':role}
 if box:item['crop_xyxy']=list(box)
 refs.append(item)
qa=[]
for name,box,mag in [('OWN4625_EYES_MOUTH_POINTS_READONLY_4x.png',(848,207,986,299),4),('OWN4625_TWO_UNEQUAL_GLOVES_READONLY_2x.png',(687,470,1055,728),2),('OWN4625_COMPLETE_SHOES_READONLY_2x.png',(715,875,1011,1037),2)]:
 p=RUN/name;im=Image.open(src).crop(box);im.resize((im.width*mag,im.height*mag),Image.Resampling.NEAREST).save(p);qa.append({**ev(p),'source':ev(src),'crop_xyxy':list(box),'magnification':mag,'operation':'readonly nearest diagnostic'})
cp=RUN/'QA_PREVIOUS09_SAFE_CLOTH_CROP_BOUNDARY_READONLY.png'
im=Image.open(prev['image']).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);ImageDraw.Draw(bg).rectangle(spec[1][2],outline=(255,0,255),width=3);bg.convert('RGB').save(cp)
save(RUN/'INPUT_COPY_AND_CROP_PROVENANCE.json',{'id':job['id'],'references':refs,'readonly_QA':qa,'cloth_crop_boundary_QA':ev(cp),'art_pixels_modified':False,'API_calls':0,'native_calls':0,'network_calls':0})
print(json.dumps({'run':str(RUN),'refs':refs,'QA':qa},ensure_ascii=False,indent=2))
