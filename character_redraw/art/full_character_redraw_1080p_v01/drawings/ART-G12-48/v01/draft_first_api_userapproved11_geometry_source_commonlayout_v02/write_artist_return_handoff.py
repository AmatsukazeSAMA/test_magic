from pathlib import Path
from PIL import Image
import hashlib,json
from datetime import datetime,timezone

RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];DIAG=CEL/'artist_return_diagnostics_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return evidence(p)
now=datetime.now(timezone.utc).isoformat()
result=json.loads((CEL/'result.json').read_text(encoding='utf-8-sig'))
attempt=json.loads((CEL/'attempt.json').read_text(encoding='utf-8-sig'))
assert attempt['status']=='completed' and attempt['api_calls']==1 and attempt['automatic_retries']==0
assert result['n']==1 and result['quality']=='high' and result['response_background']=='transparent'
raw=CEL/'character_api_original.png'; assert sha(raw)==result['output_sha256']=='e69349aa27decf395526a8a33a7c63f3a1b850a791736d2659fcb4d18bb7daa7'
im=Image.open(raw); assert im.mode=='RGBA' and im.size==(704,944)
q=json.loads((RUN/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
assert sha(RUN/'DRAFT_API_REQUEST.json')=='27a829eac063c388fd63189afdfe3be9c7021268d9f8080e6cc3f0523be5119b'
assert sha(CEL/'prompt.txt')==q['prompt_sha256']
assert [v['sha256'] for v in result['inputs']]==q['reference_sha256']
files=['character_api_original.png','qa_white.png','qa_black.png','api_response.raw.json','response_headers.txt','request_manifest.json','result.json','attempt.json','ARTIST_API_EXECUTION_RECEIPT.json','API_PREPARED_REQUEST.json','PROJECT_SCOPE_REFERENCE_RELEASE.json','ROOT_SPECIFIC_RELEASE.json','prompt.txt']
technical=write(CEL/'ARTIST_TECHNICAL_RETURN_PROVENANCE.json',{
 'id':'ART-G12-48','recorded_at_utc':now,'provider':'OpenAI API','model':result['model'],'quality_requested':result['quality'],'quality_response':result['response_quality'],'size':list(im.size),'mode':im.mode,
 'alpha_extrema':list(im.getchannel('A').getextrema()),'visible_alpha_bbox':list(im.getchannel('A').getbbox()),
 'official_endpoint':result['endpoint'],'elapsed_seconds_provider_script':result['elapsed_seconds'],
 'attempt_started_utc':attempt['started_utc'],'attempt_finished_utc':attempt['finished_utc'],'attempt_status':attempt['status'],
 'http_status':attempt.get('http_status'),'curl_exit_code':attempt.get('curl_exit_code'),'API_calls':1,'automatic_retries':0,
 'exec_session_id':18271,'exec_session_terminal':True,'inflight':0,
 'retained_artifacts':[evidence(CEL/n) for n in files],
 'response_base64_not_printed':True,'DPAPI_key_not_printed_or_copied':True,'API_response_retained_original':True,
 'raw_not_reencoded':True,'source_JOB_guide_draft_not_modified':True,'central_write':False,
 'technical_checks_not_art_acceptance':True})
actual=[evidence(CEL/n) for n in ['character_api_original.png','qa_white.png','qa_black.png','inputs/source_pose_guide.png']]
actual.append(evidence(Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G12-48\source.png')))
for name in ['RETURN_HEAD_LOW_EAR_ROOT_COIL_1x.png','RETURN_HEAD_LOW_EAR_ROOT_COIL_3x.png','RETURN_HEAD_LOW_EAR_ROOT_COIL_BLACK_3x.png','RETURN_OPEN_MONO_EYES_3x.png','RETURN_DISTINCT_MOUTH_COVER_HANDS_3x.png','SOURCE48_EYES_HANDS_1x.png']:
    actual.append(evidence(DIAG/name))
review=write(CEL/'DRAFT_PRIMARY_REVIEW_xhigh_pending_artist_v01.json',{
 'id':'ART-G12-48','created_at_utc':now,'reviewer':'xhigh_pending_artist private actual-view draft; not root primary or Sol independent',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':[704,944],
 'recommendation':'CANDIDATE_FOR_FRESH_ROOT_SOL_REVIEW_WITH_MATERIAL_AND_PHOTOGRAPHY_OBSERVATIONS',
 'artist_artistic_pass':False,'central_select_or_binding_authorized_by_this_draft':False,
 'actual_viewed_paths':actual,'exact_reference_review':evidence(RUN/'ARTIST_REFERENCE_REVIEW.json'),
 'observations':[
 'Actual fullraw/white/black and source1012 checked. Both different spreadhands still cross at mouth/chin with original fingerfan/contact roles and cuff/forearm overlap; no added exposed O/smile. Original openeyes/gaze/headtilt read remains; single dark fill and ordinary small round glints, no heart points or half-lids.',
 'Graybob/whitecap exactly2blackleaves, warmpeachskin, blacklongsleeves/standingcollar/redbowgold/whitecuffs-frills/apron/waist-backribbons and originalhalfbody bottom remain visible. No added legs/shoes/background/subtitles/independentprops.',
 'Normalrootcoil and3x whiteblack show a single connected coil from sameear lowbob-nape redbead group: upperbead below visibleear loweredge; secondredbead partly boboccluded. No high-temple separate root or second independent coil observed.',
 'Compared directly with user-approved exact77x154 geometry: visible broad band follows linked oblique spiral, narrows toward lowerend and continues into inwardC terminalcurl. It is no longer the ade931 stack of separate sealed rounded plates. Narrow return connection strips remain readable. No fixed transparentwindow count imposed; broadopaque returns not carved out.',
 'R146 supplies only inspected nearshoulder elastic phase. Exact dynamic agreement and contiguous playback were not tested; the terminalcurl currently reads in front of shoulderfrill and must still be checked for source/projection occlusion during photography.',
 'Fullraw viewer shows hiddenRGB fog behind image, but corresponding fullwhite/fullblack do not show it as an opaque painted background or broadhalo. Originalraw and response retained; no alpha edits/reencoding were performed.' ],
 'issues_for_root_review':[
 {'severity':'P2_pending_root_assessment','region':'head/cap/body layout','observation':'Head/cap appear larger than originalsource; face/hands/waist lie somewhat higher within same704x944 saveframe. Apron/backribbon visible bottom is retained, but source extent/head-body fitting and actual1080 placement are not validated. Do not use blindwhole enlargement/partwarp or codebottom fill as a fix.'},
 {'severity':'P2_pending_root_assessment','region_raw_xyxy':[407,310,502,440],'observation':'Mutedgray-mint mainvisible coilfaces and narrowreturn strips have light soft tonal variation. User-specific continuousgeometry is preserved; material variation must not trigger redesign into discs or forcedairholes. No universal materialpartition master or strictflat certificate asserted.'},
 {'severity':'P2_pending_root_assessment','region':'capleaves/line/skin','observation':'Two capleaves are relativelylarge and linework somewhat cleaner/more regular than source. Warm skin retains slightsoftcolor. Mainreview decides scale/style significance against originalPV and photography.'}],
 'hidden_geometry_certified':False,'fixed_hole_count_required':False,'photographic_registration_validated':False,'source_visible_extent_coverage_verified':False,'dynamic_tested':False,'renderer_verified':False,
 'user_accepted':False,'new_generation_user_acceptance_inherited_from_old11':False,'requires_fresh_root_and_Sol':True,
 'no_additional_call_or_retry':True,'central_registry_binding_exposure_progress_count_write':False})
handoff=write(CEL/'ARTIST_RETURN_HANDOFF_v01.json',{
 'id':'ART-G12-48','created_at_utc':now,'status':'ONE_FIRST_OFFICIAL_API_RETURNED_ACTUALLY_VIEWED_AWAIT_ROOT_SOL',
 'raw':evidence(raw),'white_QA':evidence(CEL/'qa_white.png'),'black_QA':evidence(CEL/'qa_black.png'),
 'provider':'OpenAI API','model':result['model'],'quality':'high','size':'704x944','background':'transparent','n':1,'elapsed_seconds':result['elapsed_seconds'],
 'API_calls':1,'automatic_retries':0,'inflight':0,'native_calls':0,
 'technical_provenance':technical,'private_review':review,'diagnostics':evidence(DIAG/'DIAGNOSTIC_PROVENANCE.json'),
 'root_release':evidence(CEL/'ROOT_SPECIFIC_RELEASE.json'),'formal_request':evidence(CEL/'API_PREPARED_REQUEST.json'),'immutable_draft':evidence(RUN/'DRAFT_API_REQUEST.json'),
 'raw_response_and_receipts_retained':True,'new49_not_submitted':True,'12_history_unchanged':True,'32_unknown_not_retried':True,'no_central_write':True,
 'next_step':'Root actually views exactreturnedraw/fullQA/source and decides fresh primary/Sol assessment. No automatic secondgeneration or49API call.'})
print(json.dumps({'technical':technical,'private_review':review,'handoff':handoff,'raw':evidence(raw),'calls':1,'inflight':0},ensure_ascii=False))
