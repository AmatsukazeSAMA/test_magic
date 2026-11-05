from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def dump(p,x):
    assert not p.exists()
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=json.loads((RUN/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
assert sha(RUN/'API_PREPARED_REQUEST.json')=='f69378aa90d912a68e2ad6775c9596ef0c8851f1501468751f1732c6ee3f10cf'
for r in d['refs']:assert sha(r['path'])==r['sha256']
preview=json.loads((RUN/'API_PREVIEW_VALIDATION_PREPONLY.json').read_text(encoding='utf-8-sig'))
assert preview['submitted'] is False and preview['API_calls']==0
actual=[CEL/'inputs/source_pose_guide.png',Path(d['JOB']['path']),
    Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-71/source.png'),
    BASE/'coverage/source_frames/F001133.png',BASE/'coverage/source_frames/F001140.png',
    Path(d['current_previous_reviewed_asset']['selected_run'])/'qa_white.png',
    Path(d['current_previous_reviewed_asset']['selected_run'])/'qa_black.png']
# JOB was read as JSON, not visually rendered; retain a separate truthful readback entry.
visual=[p for p in actual if p.suffix.lower()=='.png']+[Path(r['path']) for r in d['refs']]
dump(RUN/'ARTIST_REFERENCE_REVIEW_PREPONLY.json',{
    'id':'ART-G12-71','reviewer':'xhigh_pending_artist','actual_view_method':'tools.view_image original1135guide/native, source1133/1140, selected70fullwhiteblack, each exactsixinput',
    'actual_viewed_images':[rec(p) for p in visual],'JOB_and_REG_read_as_JSON':[rec(CEL/'JOB.json'),rec(CEL/'REGISTRATION_PLAN.json')],
    'observations':[
        'Current1135 source is front lowhead, unequal halfopen downgaze, smallclosedsmile.1133 roundereyes and1140 moreclosedlids cannot substitute currentperformance.',
        'Both arms lowoutstretched with unequal hands: viewerLEFT longfinger group points diagonalup-left and thumb separates below; viewerRIGHT fingers flatterright and thumb down. No OK or generic mirrored palms.',
        'Originalguide1312x784 already contains complete twohands/head/cap and actual halfbodyapronbottom with sideclearance. Keep unchanged no partmove/stretch or newcompacttrim; JOB/REG untouched.',
        'Low anatomicalLEFT root viewerRIGHT after bow, naturalbob/frill occlusion. Previous70oldmechanicalcurl excluded from IDcrop. Correct11headcoilcontext owns intrinsicmass/continuousfront-return-taper only, never roundeyes/raisedarm or fullbody.',
        'Input2 identity RGBA contains alpha0 hiddenRGB; ignore hidden smokyRGB. It is a headcrop only, not fullwrongcoil/lightingtemplate. PureGRAY overrides softgrayvalue hints in references.',
        'Uniformcharcoalinputcard is illustrativemethodonly implementing singlefillG02rule, not claimed sampledG02pixels and has no eyelid aperture. Own1135eyecrop owns currentopening/gaze.',
    ],
    'AI_reference_not_invented':d['AI_hair_reference_not_submitted'],
    'PREPONLY':True,'root_release_received':False,'API_calls':0,'HTTP_calls':0,'native_calls':0,
    'no_final_art_pixels_painted_or_pasted':True,'technical_preview_not_art_pass':True,
    'central_JOB_REG_binding_unchanged':True,'dynamic_tested':False,'user_accepted':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
})
dump(RUN/'PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{
    'id':'ART-G12-71','existing_broad_project_authorization':d['auth'],
    'endpoint':d['endpoint'],'provider':d['provider'],'model':d['model'],'refs':d['refs'],
    'size':'1312x784','quality':'high','background':'transparent','n':1,'automatic_retries':0,
    'current_parent_instruction':'PREPONLY source1135 FIRST request, root actualreview and separate release required before execution',
    'root_execution_release_received':False,'execution_authorized_by_this_PREP_file':False,
    'does_not_request_new_credentials_or_repeat_user_scope_confirmation':True,
})
dump(RUN/'ARTIST_HANDOFF_PREPONLY.json',{
    'id':'ART-G12-71','status':'DRAFT_READY_WITHOUT_SUBMIT','dispatchable':False,'root_release_received':False,
    'formal':rec(RUN/'API_PREPARED_REQUEST.json'),'draft':rec(RUN/'DRAFT_API_REQUEST.json'),
    'prompt':rec(RUN/'prompt_api.txt'),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),
    'preview':rec(RUN/'API_PREVIEW_VALIDATION_PREPONLY.json'),'artist_actual':rec(RUN/'ARTIST_REFERENCE_REVIEW_PREPONLY.json'),
    'project_scope':rec(RUN/'PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json'),
    'API_calls':0,'HTTP_calls':0,'native_calls':0,'automatic_retries':0,'size':'1312x784','reference_count':6,
    'JOB_REG_central_binding_unchanged':True,
})
print(json.dumps({'handoff':rec(RUN/'ARTIST_HANDOFF_PREPONLY.json'),'actual':rec(RUN/'ARTIST_REFERENCE_REVIEW_PREPONLY.json'),'preview':rec(RUN/'API_PREVIEW_VALIDATION_PREPONLY.json')},ensure_ascii=False))
