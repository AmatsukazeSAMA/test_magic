from pathlib import Path
from PIL import Image
import hashlib,json
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];DIAG=CEL/'artist_return_diagnostics_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return evidence(p)
now=datetime.now(timezone.utc).isoformat();raw=CEL/'character_api_original.png'
result=json.loads((CEL/'result.json').read_text(encoding='utf-8-sig'));attempt=json.loads((CEL/'attempt.json').read_text(encoding='utf-8-sig'))
assert attempt['status']=='completed' and attempt['api_calls']==1 and attempt['automatic_retries']==0
assert sha(raw)==result['output_sha256']=='4c9822a4c7ee2aeabc93af53128cc9675adcbf5a7e05cd3d8e819996d71b5589'
im=Image.open(raw);assert im.mode=='RGBA' and im.size==(656,1040)
assert result['n']==1 and result['quality']=='high' and result['response_background']=='transparent'
q=json.loads((RUN/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'));assert sha(RUN/'DRAFT_API_REQUEST.json')=='b45f7063653b369846a433abf36cfc9d25cff9a2217d78ace3e29123be8bb93e'
assert sha(CEL/'prompt.txt')==q['prompt_sha256'] and [v['sha256'] for v in result['inputs']]==q['reference_sha256']
artifacts=['character_api_original.png','qa_white.png','qa_black.png','api_response.raw.json','response_headers.txt','result.json','request_manifest.json','attempt.json','ARTIST_API_EXECUTION_RECEIPT.json','ROOT_SPECIFIC_RELEASE.json','PROJECT_SCOPE_REFERENCE_RELEASE.json','API_PREPARED_REQUEST.json','API_COMPACT_CANVAS_OVERRIDE.json','prompt.txt']
tech=write(CEL/'ARTIST_TECHNICAL_RETURN_PROVENANCE.json',{
 'id':'ART-G12-49','recorded_at_utc':now,'provider':'OpenAI API','model':result['model'],'quality_requested':result['quality'],'quality_response':result['response_quality'],'size':list(im.size),'mode':im.mode,
 'alpha_extrema':list(im.getchannel('A').getextrema()),'visible_alpha_bbox':list(im.getchannel('A').getbbox()),'endpoint':result['endpoint'],
 'elapsed_seconds_provider_script':result['elapsed_seconds'],'attempt_started_utc':attempt['started_utc'],'attempt_finished_utc':attempt['finished_utc'],'attempt_status':attempt['status'],'http_status':attempt.get('http_status'),'curl_exit_code':attempt.get('curl_exit_code'),
 'exec_session_id':73163,'session_terminal':True,'API_calls':1,'automatic_retries':0,'inflight':0,
 'retained_artifacts':[evidence(CEL/n) for n in artifacts],'raw_not_reencoded':True,'original_response_retained':True,'base64_not_printed':True,'key_notprinted_orcopied':True,
 'JOB_guide_draft_selection_history_preserved':True,'technical_success_not_art_acceptance':True,'central_write':False})
actual=[evidence(CEL/n) for n in ['character_api_original.png','qa_white.png','qa_black.png','inputs/source_pose_guide.png']]
for n in ['RETURN_LOW_EAR_ROOT_COMPACT_SPIRAL_1x.png','RETURN_LOW_EAR_ROOT_COMPACT_SPIRAL_3x.png','RETURN_LOW_EAR_ROOT_COMPACT_SPIRAL_BLACK_3x.png','RETURN_OPEN_EYES_TINY_O_3x.png','RETURN_DISTINCT_LOWLEFT_HANDS_3x.png','SOURCE49_DISTINCT_LOWLEFT_HANDS_3x.png','SOURCE49_ORIGINAL_GUIDE_COMPACT_WINDOW_1x.png']:
    actual.append(evidence(DIAG/n))
coil=write(DIAG/'COIL_CONTINUITY_COMPARISON_xhigh_v01.json',{
 'id':'ART-G12-49','created_at_utc':now,'reviewer':'xhigh_pending_artist private visibleconnection opinion, not root/Sol approval','raw_sha256':sha(raw),
 'approved_shape_reference':evidence(BASE/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png'),
 'actual_viewed_return_crop_xyxy':[450,315,575,500],'actual_viewed_scales':[1,3],'both_QA_backgrounds_actually_viewed':True,
 'visible_form_reading':'Compressed continuous oblique spiral with taper and attached terminalC; not ade931 separate sealedoval stack.',
 'visible_evidence':['Upperbroadband joins narrow oblique return connection before the nextwidefront; another visible narrow return connects to the lowersegment, which narrows directly into attachedCcurl. The assessment uses those connectingpaths, not only overallcone silhouette.','Bothwhiteblack preserve opaquegray/graymint returnsegments. No mandatoryholecount or requirementtoerasegrayreturn is imposed.','Comparedwith48, visiblecoil is shorter/morecompressed; R152shows compactlowerturn phase. This is a staticphase observation, not validatedmotion or a frozenlengthtemplate.'],
 'material_observation':'Thin pale/silver-gray soft streaks remain on visibleupper/middlefronts. The broaderfront vs narrowreturn pigmentdivision is not a newmaster. Materialissue must not leadto changingapprovedcontinuousgeometry into discs or forcedholes.',
 'hidden_geometry_certified':False,'dynamic_certified':False,'artist_artistic_pass':False,'calls_in_comparison':0})
review=write(CEL/'DRAFT_PRIMARY_REVIEW_xhigh_pending_artist_v01.json',{
 'id':'ART-G12-49','created_at_utc':now,'reviewer':'xhigh_pending_artist private actualview draft, not root primary/Sol independent',
 'image':str(raw),'image_sha256':sha(raw),'dimensions':[656,1040],'recommendation':'CANDIDATE_FOR_FRESH_ROOT_SOL_WITH_MATERIAL_AND_HEADSCALE_OBSERVATIONS','artist_artistic_pass':False,
 'actual_viewed_paths':actual,'source_reference_review':evidence(RUN/'ARTIST_REFERENCE_REVIEW.json'),'coil_focused_opinion':coil,
 'observations':[
 'Original49 openeye/gaze/headtilt and visible tinyO remain, unlike48hiddenmouth. One solid darkiris/ordinaryroundwhiteglint method retained; no heartglint/AI smile or copiedold11neutralmouth.',
 'Actual3x newhands vs samecoordinate sourcehands show upperleft flippedpalm with longleftthumb and downfingers, and foregroundcrossing splayedhand with distinctfingers/thumb/wristbend. Contact/overlap and cuff/forearm layering remain close tooriginal, notclapping/prayer/48mouthcovering. Lowerface andhands remainapart.',
 'Originalblacklongsleeves/standingcollar/redbowgold/whitefrills-cuffs/waist/apron/blackskirt/rightbackbow/longbacktail andactualhalfbody bottom retained. No hiddenlegs/shoes/prop/background/subtitles added. Samecompactwindow sourcecomparison shows waist/body/cut close; actual1080 placement stillunverified.',
 'Single anatomicalLEFTlowear/bobnape beadgroup visibleIMAGE RIGHT. Upperbead lies belowvisibleearloweredge, secondredbead partlyboboccluded, then onecoherentcoil. No templehighroot/secondcoil observed.',
 'Normalcoil and3xwhiteblack comparedwith exactuser77x154 geometry: compressed continuous oblique winding, narrowvisible returns, taper andattachedC. Notade931stackedsealeddiscs; fixedairwindow count isnot acriterion.',
 'Originalraw viewer shows backgroundlike hiddenRGB fog, which doesnotappear asopaque backdrop in actualfullwhite/fullblackQA. Raw originalbytes/response retained; no alphaclean/recolor/reencode performed.' ],
 'issues_for_root_review':[
 {'severity':'P2_pending_root_assessment','region_raw_xyxy':[470,390,534,483],'observation':'Upper/middlecoil faces carry thin pale/silver-gray softstreaks and mildgraymint tonal variation. Visibleconnectedshape remains. Material concern recorded separately, not a reason to redesign or forceholes.'},
 {'severity':'P2_pending_root_assessment','region':'head/cap and canvasright edge','observation':'Graybob/cap/headwidth appears larger than oldsourcehair identityoutline; two blackleaf tips approachrightmargin but remain visible. Sourceheadbody andfinal1080 uniformplacement needrootphotography; no measuredoutputanchors/partwarp assumed.'},
 {'severity':'P2_pending_root_assessment','region':'style/dynamicphase','observation':'Linework iscleaner/moreregular than source, with warmsoftskin. Staticcompactcurl only; actualR152motion continuity/adjacentplayback notvalidated.'}],
 'source_visible_extent_coverage_verified':False,'photographic_registration_validated':False,'hidden_geometry_certified':False,'strict_flat_material_certified':False,'dynamic_tested':False,'renderer_verified':False,'user_accepted':False,
 'fresh_root_Sol_required':True,'no_automatic_repair_or_second_call':True,'central_registry_binding_exposure_progress_count_write':False})
handoff=write(CEL/'ARTIST_RETURN_HANDOFF_v01.json',{
 'id':'ART-G12-49','created_at_utc':now,'status':'ONE_OFFICIAL_FIRST_API_RETURNED_ACTUALLY_VIEWED_AWAIT_ROOT_SOL',
 'raw':evidence(raw),'white_QA':evidence(CEL/'qa_white.png'),'black_QA':evidence(CEL/'qa_black.png'),
 'provider':'OpenAI API','model':result['model'],'quality':'high','size':'656x1040','background':'transparent','n':1,'elapsed_seconds':result['elapsed_seconds'],
 'API_calls':1,'native_calls':0,'automatic_retries':0,'inflight':0,'technical_provenance':tech,'private_review':review,'coil_opinion':coil,'diagnostics':evidence(DIAG/'DIAGNOSTIC_PROVENANCE.json'),
 'root_release':evidence(CEL/'ROOT_SPECIFIC_RELEASE.json'),'formal_request':evidence(CEL/'API_PREPARED_REQUEST.json'),'compact_override':evidence(CEL/'API_COMPACT_CANVAS_OVERRIDE.json'),'immutable_draft':evidence(RUN/'DRAFT_API_REQUEST.json'),
 'new50_not_submitted':True,'12_and32_untouched':True,'central_write':False,'next_step':'Root actualreview andfreshSol; no artistautomaticrepair/50 submission.'})
print(json.dumps({'technical':tech,'private_review':review,'coil':coil,'handoff':handoff,'raw':evidence(raw),'calls':1,'inflight':0},ensure_ascii=False))
