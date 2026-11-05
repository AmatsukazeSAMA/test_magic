from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
LOCAL=CEL/'local_source1071_upper_continuous_gray_returns_api_v04'
FUTURE=LOCAL/'future_mandatory_whole_PREPONLY'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p): return {'path':str(p),'sha256':sha(p)}
def dump(p,x):
    assert not p.exists()
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q=json.loads((RUN/'request_imggen.json').read_text(encoding='utf-8'))
assert sha(RUN/'request_imggen.json')=='24f7748f47dbd5ce7a07c3d50decddfb287b7c6643909826cc1706e7111b1aa3'
for p,h in zip(q['refs'],q['reference_sha256']): assert sha(p)==h
actual=[LOCAL/'character_api_original.png',LOCAL/'qa_white.png',LOCAL/'qa_black.png',
    BASE/'coverage/source_frames/F001071.png',CEL/'inputs/source_pose_guide.png',
    FUTURE/'SOURCE1071_OWN_FACE_EYES_OPEN_SMILE_NO_HIGH_REDCOIL.png',
    FUTURE/'SOURCE1071_OWN_BOTH_HANDS_CUFFS_NO_REDHAIR_v02.png',
    FUTURE/'SOURCE1071_OWN_CLOTH_TORSO_WAIST_CROP_NO_HIGH_REDCOIL.png',
    LOCAL/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY.png',
    RUN/'diagnostics/PREP_PRIOR_LOCAL_f2523668_ROOT_COIL_OCCLUSION_white_1x.png',
    RUN/'diagnostics/PREP_PRIOR_LOCAL_f2523668_ROOT_COIL_OCCLUSION_white_3x.png',
    RUN/'diagnostics/PREP_PRIOR_LOCAL_f2523668_ROOT_COIL_OCCLUSION_black_3x.png']
dump(RUN/'ARTIST_ACTUAL_LOCAL_AND_REFS_PREPONLY.json',{
    'id':'ART-G12-58','reviewer':'xhigh_pending_artist','scope':'known local intermediate and exact whole PREP refs only; no new whole return',
    'actual_view_method':'tools.view_image full raw/white/black, source1071 full/guide, three ownsource rectangular crops and pureGRAY, new local coil white1x and whiteblack3x',
    'actual_viewed_files':[rec(p) for p in actual],
    'exact_local_raw_sha256':'f252366811e52e4b1a61b140cc761d6accc4337915582d9a884449412cc4adbd',
    'observations':[
        'Current unique farLEFT lowviewerRIGHT root and redbeads remain under bob, full cap2MAINleaves/own openeyes/open smile/OKcontact plus three fingers/downhand/crossed sleeves/clothwaist/sourcebottom remain visible.',
        'Upper separate lid/bean removed. Wide gray front turns into opaque gray returns and next turn; lower path remains behind foreground lowhand/frill. Do not force C exposure or substitute55 sideways upswing.',
        '3x shows top return narrow brightvalue and some innergray value differences. Whole prompt requires unlit grayfront/inner/back uniform with bob, preserving opaque returns. No material pass asserted.',
        'Whiteblack differ in actual air while gray ribbons remain opaque. Direct raw hiddenRGB smokybackground is not opaque art and must not be drawn into future whole.',
        'Own face crop includes redfrontalbang fragments only as action context, never identity. Hands v02 has no redhair sliver; sourcecrop edges are not output seams. Full redhighcoil guide is not among toolrefs.',
    ],
    'status':'READY_PREPONLY_FOR_ROOT_SPECIFIC_ONE_WHOLE_RELEASE',
    'local_intermediate_only':True,'mandatory_whole_pending':True,'whole_completed':False,
    'native_calls_authorized':0,'native_calls':0,'API_calls_by_artist_this_prep':0,'HTTP_calls_by_artist_this_prep':0,
    'technical_validation_not_art_pass':True,'no_central_binding_write':True,'dynamic_tested':False,'user_accepted':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
})
dump(RUN/'ARTIST_HANDOFF_PREPONLY.json',{
    'id':'ART-G12-58','status':'READY_PREPONLY_NO_GENERATION',
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(RUN/'prompt_imggen.txt'),
    'immutable_lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),
    'artist_actual_review':rec(RUN/'ARTIST_ACTUAL_LOCAL_AND_REFS_PREPONLY.json'),
    'provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),
    'reference_count':5,'native_calls_authorized':0,'native_calls':0,'automatic_retries':0,
    'root_release_received':False,'fresh_root_Sol_photography_required':True,'central_modified':False,
})
print(json.dumps({'handoff':rec(RUN/'ARTIST_HANDOFF_PREPONLY.json'),'actual':rec(RUN/'ARTIST_ACTUAL_LOCAL_AND_REFS_PREPONLY.json')},ensure_ascii=False))
