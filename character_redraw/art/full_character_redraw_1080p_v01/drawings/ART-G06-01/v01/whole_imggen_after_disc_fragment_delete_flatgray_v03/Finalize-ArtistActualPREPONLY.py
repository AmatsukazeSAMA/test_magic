from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
LOCAL=RUN.parent/'local_disc_rim_fragments_known400_size992x1600_api_v04'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
q=json.loads((RUN/'request_imggen.json').read_text(encoding='utf-8'))
assert sha(RUN/'request_imggen.json')=='8da2e9b3f9bac07d14b58f52a033bf027f775a3e49fbcb93412c1eb834df0459'
assert Path(q['run'])==RUN and q['operation_kind']=='whole_character_redraw' and q['transparent_background'] is True
for p,h in zip(q['refs'],q['reference_sha256'],strict=True):assert sha(p)==h
assert len(q['refs'])==2 and q['native_calls_authorized']==0
actual=[LOCAL/'qa_white.png',LOCAL/'qa_black.png',BASE/'coverage/source_frames/F000476.png',RUN.parent/'inputs/source_pose_guide.png']+[Path(p) for p in q['refs']]
out=RUN/'ARTIST_ACTUAL_AND_HANDOFF_PREPONLY.json'
assert not out.exists()
out.write_text(json.dumps({
    'id':'ART-G06-01','reviewer':'xhigh_pending_artist','status':'READY_PREPONLY_ROOT_ACTUAL_RELEASE_PENDING',
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(RUN/'prompt_imggen.txt'),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),
    'actual_view_method':'tools.view_image original476 full and guide, freshlocalwhiteblack and exact2refs',
    'actual_viewed_images':[rec(p) for p in actual],
    'observations':[
        'FreshWB: required rightpropwedge/lowergrayrim removed; foregroundhand and smallfargrip fragment remain, central originallydisc-occluded area is truealpha0. Do not reconstruct hiddenbody/wrist or harddisc/rim.',
        'Original476 QA confirms inverted barefootlegs/toeangles, loosegray sleeves, closedeyes and actual visibility. Originaldisc/sourcefull is not in toolrefs, preventing its geometry from competing with clearedtarget.',
        'AnatomicalLEFT root follows current inversion to viewerLEFT redbeads under same ear, never uprightviewerRIGHT formula. Existing continuous broadgrayfront/opaquegrayreturn/nextturn/grayC preserved, no fixedholecount.',
        'Bob/coil remain softly lit with returnvalue differences. SolepureGRAY key and wholeprompt unify allgray without changinggeometry or deletingopaque returns. Local not finalpassed.',
        'Direct raw has smokyalpha0 hiddenRGB; whiteblack QA confirms transparency. Whole must ignore hiddenRGB and keep centertransparent. Existing loosecloth at centeredge is realclothing, not remainingrim.',
    ],
    'readonly_fullQA_copies_are_exact_samebytes_as_actual_localQA':True,
    'helper_schema_checked_against':'scripts/Release-RootReviewedWholeImggen.py',
    'root_release_helper_not_executed':True,'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
    'central_modified':False,'local_intermediate_only':True,'mandatory_whole_pending':True,
    'technical_validation_not_art_pass':True,'fresh_root_Sol_required':True,'user_accepted':False,'dynamic_tested':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'actual_handoff':rec(out),'request_unchanged':rec(RUN/'request_imggen.json')},ensure_ascii=False))
