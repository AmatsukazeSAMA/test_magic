from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
PRIOR=RUN.parent/'whole_imggen_after_lowroot_upturn_continuous_gray_local_v07'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
q=json.loads((RUN/'request_imggen.json').read_text(encoding='utf-8'))
assert sha(RUN/'request_imggen.json')=='dd1061a7d89d0e376fcefcbdc25d205f68baa78e0bc0f95ee23463d4c098a481'
for p,h in zip(q['refs'],q['reference_sha256']):assert sha(p)==h
actual=[PRIOR/'qa_white.png',PRIOR/'qa_black.png',BASE/'coverage/source_frames/F001058.png']+[Path(p) for p in q['refs']]
out=RUN/'ARTIST_ACTUAL_AND_HANDOFF_PREPONLY.json'
assert not out.exists()
out.write_text(json.dumps({
    'id':'ART-G12-55','reviewer':'xhigh_pending_artist','status':'READY_PREPONLY_ROOT_ACTUAL_RELEASE_PENDING',
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(RUN/'prompt_imggen.txt'),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),
    'actual_viewed_by_tools_view_image':[rec(p) for p in actual],
    'observations':[
        'Native1058 full checked. Exact pose rectangle [670,120,1140,1080] excludes highredcoil while preserves own eyes/chin/collar/highOKhand/lowerdownhand/crossedsleeves/waist in original one coordinate system. Only referencescale of this commonlayout owns distances.',
        'Leftbackfrill/backbow/apron contour has cropped parts. Cropedge is not outputcut or permission to delete these originallyvisible clothes; full native source was actually checked. No hiddenlegs/shoes added.',
        'V07 head rectangle contains twoMAINcapleaves/roundbob/lowfarLEFTbeads, no body or hands; lowerbobtips cut and some partialcoil remain on side, identityonly not action/bodyratio. Full v07body is excluded.',
        'V07 coil rectangle contains continuous lowbeads-to-grayC with widegrayfront/opaquegrayreturn and mediumoutwardupturn. Tiny incidental face/bob/handedge at rectangle corners has no actionauthority. Refs2/3 cropaspect and pixelscale never set bodygeometry.',
        'NativeOK reference has fullthumb-indexcontact and three fingers/cuff, no redcoil. Position is exclusively sourcepose ref1; ref4 only detailedshape.',
        'Knownv07curl186static is history and does not validate its failedphotographypose. Newwhole requires fresh fullwhiteblack/sourceanduniformphotography checks; no inherited pass.',
    ],
    'full_V07_body_or_highred_source_coil_not_in_tool_refs':True,
    'all_crops_readonly_rectangles_no_paint_paste_warp':True,
    'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
    'central_modified':False,'root_review_not_forged':True,'user_accepted':False,'dynamic_tested':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'actual_handoff':rec(out),'request':rec(RUN/'request_imggen.json')},ensure_ascii=False))
