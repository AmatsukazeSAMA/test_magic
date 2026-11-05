from pathlib import Path
from PIL import Image
import json,hashlib
from datetime import datetime,timezone
BASE=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
def write(p,data):
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return evidence(p)
tasks=[
 {'id':'ART-G12-50','run':'draft_first_api_compact_userapproved11_geometry_commonlayout_v01','sha':'1c381638325fe276b03a15fcc78e4df715dc84c8f95da0969c145aba08b5bafa','size':[720,976],'session':88998,'recommendation':'CANDIDATE_FOR_FRESH_ROOT_SOL_WITH_P2_MATERIAL_HEADSCALE_PHASE_OBSERVATIONS','diagnostics':['RETURN_OK_LOOP_THREE_UPRIGHT_FINGERS_3x.png','RETURN_OK_LOOP_THREE_UPRIGHT_FINGERS_BLACK_3x.png','RETURN_LOW_DROOP_HAND_3x.png','RETURN_FULL_LOW_ROOT_SPIRAL_1x.png','RETURN_FULL_LOW_ROOT_SPIRAL_3x.png','RETURN_FULL_LOW_ROOT_SPIRAL_BLACK_3x.png','RETURN_OPEN_EYES_TINY_O_3x.png'],
 'observations':[
 'Fullraw/whiteblack and original1027 full/guide re-viewed. HighIMAGELEFT thumb-index loop remainsclosedbytouch whileitsinteriorchangeswhite/blackwithQA backgrounds: trueair, notskinfill. Otherthreefingers upright anddistinct. Oppositehand crossesbody withsourcewristdroop andseparatedfingerfan; no49lowpalm/AIgesture substitution.',
 'Sourceopeneyes/gaze/headtilt andvisible tinyO retained. Singlecharcoalfill withordinarysmallroundglints, noheartpoints orcopiedAIclosedmouth. Warmpeachskin, blacklongsleeves/collar/redbowgold/whitecap2blackleaves/frills/cuffs/waist/apron/backbow/longbacktail andoriginalhalfbodybottom retained.',
 'Normalcompletecoil and3xwhiteblack showupperredbeadbelowvisibleearloweredge, lowerbeadpartlyboboccluded, attachingONEcoil onfrontprojectionIMAGE RIGHT/anatomicalLEFT. Nohighseparatetempleroot orsecondcoil observed.',
 'Visiblewidefrontsjoinobliquenarrowreturnsections, narrowtowardlowerend andcontinueintoattachedCcurl. Sameuserselectedlinkedspiralread retained, notade931independentsealedovalstack. Opaquegrayreturns notcarvedintofixedholes. Dynamicmatch/hiddenbackpath notcertified.',
 'Originalraw RGBfogoutsidealpha isnotanopaquebackdrop in fullwhite/fullblack. No finalartalphaclean/recolor/reencode performed.' ],
 'issues':[
 {'severity':'P2_pending_root_assessment','region':'head/cap and sourceheadbody relation','issue':'Graybob/cap arebroader than originalredhairidentity andface/O sittsomewhathigher againsthand/necklayout. Actual1080uniformfit/sourceextent needrootphotography; nocodepartwarp orautomaticrepair.'},
 {'severity':'P2_pending_root_assessment','region':'coil/material/phase','issue':'Softgraymint tonalvariation andlightedge traces remain. Visiblecoilrun is relativelyelongated againstthecompactR157phase; exactbouncelength/adjacentmotion notvalidated. Neitherissueauthorizesredesigningconnectedshape or freezingfullcoilasmaster.'}]},
 {'id':'ART-G33-13','run':'draft_first_api_rear_source_backbob_userapproved11_geometry_v02','sha':'f61f5924e434391be59f1ec43277528588658260eea84f7a7d82ae9633406ba4','size':[624,1072],'session':68912,'recommendation':'HOLD_REPAIR_REQUIRED_HIGH_BEAD_ROOT_P1_AWAIT_FRESH_ROOT_SOL','diagnostics':['RETURN_BACK_PROFILE_EAR_HIGH_BEAD_ROOT_1x.png','RETURN_BACK_PROFILE_EAR_HIGH_BEAD_ROOT_3x.png','RETURN_BACK_PROFILE_EAR_HIGH_BEAD_ROOT_BLACK_3x.png','RETURN_COMPLETE_CALVES_ANKLES_SHOES_3x.png','RETURN_FOLDED_HAND_3x.png','RETURN_WAIST_HAND_BOW_CONTACT_3x.png'],
 'observations':[
 'Fullraw/whiteblack/source2355 full/guide re-viewed. Rear3/4 headturnleft, narrowclosedlashstroke withnoinventediris/glint/frontopeneye, profilemouthcue andsourcecap/twoleaves retained. Backbobcut isadapted withoutcopyingpolishedmintcrownarc/vest/uniform.',
 'SourcefoldedsmallIMAGELEFThand andwhitecuff/bentarm retained; IMAGE RIGHThand remainsbehindwaist incontactwithwhitebow, withsourceverticalfinger/wrist/cuffoverlap. Crossedwhitebackstraps/frills/backwaistbow/longtails/blackdress stayrearview; nofrontredbow inventedonback.',
 'Entirecanonicalskirt/calves/twodifferentankleangles/blackanklestraps andcompleteblackshoe toes/heels arepresent. One shoe nearhorizontalpointleft, otherraiseddiagonal; notcroppedtothefirst882..885halfbodyappearance.',
 'Onecoil isonscreenLEFTsideofbackhead, withoutAIrightsidebeadcopy, anditsvisiblecompressedribbon/returnconnections/taper/attachedsmallC remain readable. These successes do notcancelthehighrootP1.',
 'Normalhead/ear/coil andboth3xbackgrounds confirmbeadgroup isaroundrawx291..316/y148..168, abovevisibleear approximatelyy174..211 andwellabovelowerbob/nape approximatelyy224..237. Redbeads sitonsidebob/upperearheight, notlowearafter/nape. Notageneralrejectionbasedonmintwidth/grayreturns/absenceofmandatoryholes.',
 'RawoutsideRGBfog notvisibleasanopaquebackdropinfullwhiteblack; originalbytes retained. Noautomaticrepair/native/secondAPI requested.' ],
 'issues':[
 {'severity':'P1','region_raw_xyxy':[287,143,325,176],'issue':'Beads/attachment too high onsidebob abovevisibleear; requiredlowanatomicalLEFTearafter/naperoot notmet despitecorrectscreenLEFTside. Needfreshroot/Solassessment andnewrelease beforeanyrepair.','visible_ear_approx_y':[174,211],'low_bob_nape_approx_y':[224,237]},
 {'severity':'P2_pending_root_assessment','region':'coil/material/style','issue':'Mintfacesrelativelyprominent/light; narrowgrayreturns andsimpler/regularlinework. Currentlinkedvisiblegeometryread doesnotcertifyhiddenpath/dynamics; defermaterialdecisionafterblockingrootreview.'}]}]
summaries=[]
for t in tasks:
    cel=BASE/'drawings'/t['id']/'v01';run=cel/t['run'];diag=cel/'artist_return_diagnostics_v01';raw=cel/'character_api_original.png'
    result=json.loads((cel/'result.json').read_text(encoding='utf-8-sig'));attempt=json.loads((cel/'attempt.json').read_text(encoding='utf-8-sig'));q=json.loads((run/'DRAFT_API_REQUEST.json').read_text(encoding='utf-8'))
    assert attempt['status']=='completed' and attempt['api_calls']==1 and attempt['automatic_retries']==0
    assert sha(raw)==result['output_sha256']==t['sha'];im=Image.open(raw);assert im.mode=='RGBA' and list(im.size)==t['size'];assert result['quality']=='high' and result['response_background']=='transparent' and result['n']==1
    assert [r['sha256'] for r in result['inputs']]==q['reference_sha256'] and sha(result['prompt_file'])==q['prompt_sha256']
    names=['character_api_original.png','qa_white.png','qa_black.png','api_response.raw.json','response_headers.txt','result.json','request_manifest.json','attempt.json','ARTIST_API_EXECUTION_RECEIPT.json','ROOT_SPECIFIC_RELEASE.json','PROJECT_SCOPE_REFERENCE_RELEASE.json','API_PREPARED_REQUEST.json']
    if(cel/'API_COMPACT_CANVAS_OVERRIDE.json').exists():names.append('API_COMPACT_CANVAS_OVERRIDE.json')
    now=datetime.now(timezone.utc).isoformat()
    tech=write(cel/'ARTIST_TECHNICAL_RETURN_PROVENANCE.json',{
      'id':t['id'],'recorded_at_utc':now,'provider':'OpenAI API','model':result['model'],'quality_requested':result['quality'],'quality_response':result['response_quality'],'size':list(im.size),'mode':im.mode,'alpha_extrema':list(im.getchannel('A').getextrema()),'visible_alpha_bbox':list(im.getchannel('A').getbbox()),
      'endpoint':result['endpoint'],'elapsed_seconds_provider_script':result['elapsed_seconds'],'started_utc':attempt['started_utc'],'finished_utc':attempt['finished_utc'],'http_status':attempt.get('http_status'),'curl_exit_code':attempt.get('curl_exit_code'),'exec_session_id':t['session'],'exec_terminal':True,
      'API_calls':1,'automatic_retries':0,'native_calls':0,'inflight':0,'retained_artifacts':[evidence(cel/n) for n in names],
      'exact_prompt':evidence(Path(result['prompt_file'])),'raw_not_reencoded':True,'original_response_retained':True,'no_base64_or_key_printed':True,'JOB_guide_draft_history_preserved':True,'technical_success_not_art_acceptance':True,'central_write':False})
    actual=[evidence(cel/n) for n in ['character_api_original.png','qa_white.png','qa_black.png','inputs/source_pose_guide.png']]
    job=json.loads((cel/'JOB.json').read_text(encoding='utf-8'));actual.append(evidence(Path(job['source_image'])))
    actual.extend(evidence(diag/n) for n in t['diagnostics'])
    review=write(cel/'DRAFT_PRIMARY_REVIEW_xhigh_pending_artist_v01.json',{
      'id':t['id'],'created_at_utc':now,'reviewer':'xhigh_pending_artist private actualview draft, not root/Sol/centralapproval','image':str(raw),'image_sha256':sha(raw),'dimensions':t['size'],
      'recommendation':t['recommendation'],'artist_artistic_pass':False,'actual_viewed_paths':actual,'exact_reference_review':evidence(run/'ARTIST_REFERENCE_REVIEW.json'),'observations':t['observations'],'issues_for_root_review':t['issues'],
      'photographic_registration_validated':False,'source_visible_extent_coverage_verified':False,'hidden_geometry_certified':False,'strict_flat_material_certified':False,'dynamic_tested':False,'renderer_verified':False,'user_accepted':False,
      'requires_fresh_root_and_Sol':True,'no_automatic_second_call_or_repair':True,'central_registry_binding_exposure_progress_count_write':False})
    handoff=write(cel/'ARTIST_RETURN_HANDOFF_v01.json',{
      'id':t['id'],'created_at_utc':now,'status':t['recommendation'],'raw':evidence(raw),'white_QA':evidence(cel/'qa_white.png'),'black_QA':evidence(cel/'qa_black.png'),
      'provider':'OpenAI API','model':result['model'],'quality':'high','size':t['size'],'background':'transparent','n':1,'elapsed_seconds':result['elapsed_seconds'],
      'API_calls':1,'automatic_retries':0,'native_calls':0,'inflight':0,'technical_provenance':tech,'private_review':review,'diagnostics':evidence(diag/'DIAGNOSTIC_PROVENANCE.json'),
      'root_release':evidence(cel/'ROOT_SPECIFIC_RELEASE.json'),'formal_request':evidence(cel/'API_PREPARED_REQUEST.json'),'immutable_draft':evidence(run/'DRAFT_API_REQUEST.json'),
      'no_51_or14_submitted':True,'central_write':False,'next_step':'Freshroot/Solreview; highroot13HOLD retained, noartistautomaticrepairornewitemcall.'})
    summaries.append({'id':t['id'],'raw_sha256':sha(raw),'technical':tech,'private_review':review,'handoff':handoff,'API_calls':1,'inflight':0})
print(json.dumps(summaries,ensure_ascii=False))
