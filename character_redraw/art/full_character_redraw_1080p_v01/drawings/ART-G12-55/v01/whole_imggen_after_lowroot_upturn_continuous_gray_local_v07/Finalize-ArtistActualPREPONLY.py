from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

RUN=Path(__file__).resolve().parent
LOCAL=RUN.parent/'local_v05_lowroot_continuous_gray_upturn_api_v01'
BASE=RUN.parents[3]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p): return {'path':str(p),'sha256':sha(p)}
def dump(p,x):
    assert not p.exists(), str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
request=json.loads((RUN/'request_imggen.json').read_text(encoding='utf-8'))
assert sha(RUN/'request_imggen.json')=='84184c2e16fce4b3aef8ae6d77a878de7cffa2eb724c91043c2e42aed15623ca'
assert request['native_calls_authorized']==0 and not request['root_release_received']
for p,h in zip(request['refs'],request['reference_sha256']): assert sha(p)==h
actual=[LOCAL/'character_api_original.png',LOCAL/'qa_white.png',LOCAL/'qa_black.png',
        BASE/'coverage/source_frames/F001058.png',RUN.parent/'inputs/source_pose_guide.png',
        LOCAL/'future_mandatory_whole_PREPONLY/inputs/source1058_MAIN_FACE_BODY_NO_HIGH_RED_COIL.png',
        LOCAL/'future_mandatory_whole_PREPONLY/inputs/source1058_OWN_HALFOPEN_EYES_SMALLW_MOUTH.png',
        LOCAL/'future_mandatory_whole_PREPONLY/inputs/source1058_OWN_HIGH_OK_THREE_FINGERS.png',
        LOCAL/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png',
        RUN/'diagnostics/PREP_PRIOR_LOCAL_8f180a6b_ROOT_COIL_white_1x.png',
        RUN/'diagnostics/PREP_PRIOR_LOCAL_8f180a6b_ROOT_COIL_white_3x.png',
        RUN/'diagnostics/PREP_PRIOR_LOCAL_8f180a6b_ROOT_COIL_black_3x.png']
review={
    'id':'ART-G12-55','reviewer':'xhigh_pending_artist','review_scope':'PREPONLY known local intermediate, not new whole output/root/Sol art pass',
    'actual_view_method':'tools.view_image current raw/full white/full black/sourcefull/guide/all five reference contents and newly derived currentlocalcoil white1x/white3x/black3x',
    'actual_viewed_files':[rec(p) for p in actual],
    'exact_local_raw_sha256':'8f180a6bf5c751cf5c657c8082d1e6fee2e1f6f827499604a284b9b9faaf2e0d',
    'observations':[
        'Full white/black confirms current farLEFT low redbead root remains viewerRIGHT under bob, not high viewerLEFT/source nearredroot.',
        'Coil has wide gray front and opaque inner/back returns leading into taper gray C. Old graypouch and independent coarse green ring are removed. Current medium volume/outward slightly rising phase can be preserved.',
        'Gray returns/face still show mild material value differences/soft rendering. Whole prompt explicitly unifies bob and every gray front/inner/back/C to unlit gray; this is not a claim local material fully passed.',
        'Air changes white/black while gray returns remain visibly opaque. Do not hollow out all returns or split continuous path into independent bowls.',
        'Two MAIN black cap leaves, own asymmetric halfopen eyes/small w mouth, OK thumb-index contact and three fingers, crossed sleeves/chest downfingers, redbowgold/white frill/waist/apron and visible bottom retained in local.',
        'Raw hidden RGB renders smoky background in direct raw display; full white/black QA shows no opaque background. Prompt tells whole to ignore alpha0 hidden RGB.',
        'Own original reference rectangles exclude high red curl; original forehead fragments remain only action evidence, not identity. Main body rectangle cuts upper OK hand/cap; own complete hand ref and full target cap cover those roles.',
    ],
    'status':'READY_FOR_ROOT_SPECIFIC_ONE_WHOLE_REVIEW_RELEASE_ONLY',
    'whole_generated':False,'local_intermediate_only':True,'mandatory_whole_pending':True,
    'native_calls_authorized':0,'native_calls':0,'API_calls_by_artist_this_prep':0,'HTTP_calls_by_artist_this_prep':0,
    'no_central_or_binding_writes':True,'technical_hash_validation_not_art_pass':True,
    'dynamic_tested':False,'user_accepted':False,'created_utc':datetime.now(timezone.utc).isoformat(),
}
dump(RUN/'ARTIST_ACTUAL_LOCAL_AND_REFERENCE_REVIEW_PREPONLY.json',review)
dump(RUN/'ARTIST_HANDOFF_PREPONLY.json',{
    'id':'ART-G12-55','status':'READY_PREPONLY_NO_NATIVE_RELEASE',
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(RUN/'prompt_imggen.txt'),
    'immutable_lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),
    'actual_artist_review':rec(RUN/'ARTIST_ACTUAL_LOCAL_AND_REFERENCE_REVIEW_PREPONLY.json'),
    'provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),
    'exact_local_known':rec(LOCAL/'character_api_original.png'),
    'reference_count':5,'native_calls_authorized':0,'native_calls':0,
    'automatic_retries':0,'central_modified':False,'fresh_root_Sol_and_photography_required':True,
})
print(json.dumps({'handoff':rec(RUN/'ARTIST_HANDOFF_PREPONLY.json'),'actual_review':rec(RUN/'ARTIST_ACTUAL_LOCAL_AND_REFERENCE_REVIEW_PREPONLY.json')},ensure_ascii=False))
