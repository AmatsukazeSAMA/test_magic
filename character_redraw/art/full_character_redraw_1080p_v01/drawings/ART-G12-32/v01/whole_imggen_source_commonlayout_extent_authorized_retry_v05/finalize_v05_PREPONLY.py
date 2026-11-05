from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent;C=R.parent;B=R.parents[3];PROJECT=B.parents[1]
OLD=C/'whole_imggen_source_commonlayout_extent_v04'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
request=R/'request_imggen.json';assert sha(request)=='a0b8e60a1fd13f04e3213dda3798e608dc95b9af737e79a36916bf784c57d567'
q=read(request);p=read(R/'REF_INPUT_PROVENANCE.json')
assert len(q['refs'])==4 and q['refs']==q['tool_arguments']['referenced_image_paths']
assert set(q['tool_arguments'])=={'prompt','referenced_image_paths','transparent_background'}
assert q['tool_arguments']['transparent_background'] is True
assert q['prompt']==q['tool_arguments']['prompt']==Path(q['prompt_file']).read_text(encoding='utf-8')
assert sha(q['prompt_file'])==q['prompt_sha256']=='38b0ef802bcec321f47ebccba2f1de65c33b4995d5cc9654f57247b2f4f255fa'
assert q['prompt'].startswith(read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text'])
for i,ref in enumerate(q['refs']):assert sha(ref)==q['reference_sha256'][i]
for key in ['source','JOB','REGISTRATION_PLAN','source_guide']:
    assert sha(p[key]['path'])==p[key]['sha256']
for f in p['old_unknown_file_inventory_before_preparation']:assert sha(f['path'])==f['sha256']
assert sha(C/'local_round_drill_v01/LOCAL_REPAIR_STATUS.json')==p['local_parent_instant_before']['sha256']
w=read(q['user_waiver']['path']);assert w['user_explicitly_approved_one_additional_generation']
assert w['reply_verbatim']=='允许这一张额外重绘一次' and w['question_id']=='call_1444d0931f4e41cb91c73c8f34eb627e'
assert w['additional_generation_limit']==1 and w['additional_generation_calls_used']==0 and w['automatic_retries']==0
for f in ['attempt.json','NATIVE_CALL_RECEIPT.json','BUILTIN_GENERATION.json','character_imggen_original.png','result.json']:
    assert not (R/f).exists()
sourceguide=C/'inputs/source_pose_guide.png'
oldprefix=OLD/'inputs/ref2_STATIC32V03_HEAD_CAP2_LOWROOT_CURRENT_GRAYRETURNS_PREFIX_ONLY.png'
oldv03=C/'whole_imggen_source_face_body_09unlit_identity_v03'
photo=B/'dance_first10_reference_redraw_v01/registration_proposals/ART-G12-32_F0933_v04_source933_new_unlit'
viewed=[Path(read(C/'JOB.json')['source_image']),sourceguide,
        B/'coverage/source_frames/F000933.png',B/'coverage/source_frames/F000937.png',
        oldv03/'qa_white.png',oldv03/'qa_black.png',oldprefix,
        OLD/'inputs/ref1_ORIGINAL32_COMMON_LAYOUT_FACE_BODY_CONTACTS_FULL_VISIBLE_APRON_NO_OLD_RED_HEAD.png',
        OLD/'inputs/ref3_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png',photo/'source_comparison.png',
        B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000081.png',
        B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
        B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png']+[Path(x) for x in q['refs']]+list((R/'qa_readonly').glob('*.png'))
review=put('ARTIST_REFERENCE_REVIEW_PREPONLY.json',{
 'id':q['id'],'reviewer':'xhigh_pending_artist private preparation input review',
 'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'actual_viewed':[dict(**rec(f),actual_viewed_in_this_task=True) for f in dict.fromkeys(viewed)],
 'canonical_source_frame':936,'canonical_PTS':499696,
 'own_first_native_frames_actually_viewed_this_task':[933,936,937],
 'other933_937_rows_not_falsely_claimed_actually_viewed_this_task':True,
 'source_findings':'Round-open eyes and tinyO; distinct front contacting hands with different finger and palm directions, original neck/waist, lower visible apron/black skirt runs to original bottom. Source does not show legs/shoes.',
 'source_layout_input_findings':'704x976 source selection keeps all face/hand/waist/lowerapron pixels in their original common coordinates. Cleared old head/hat/highcoil alpha is a reference omission, not final straight boundary or black block.',
 'existing_v03_findings':'Full white/black and source/photo comparison show broad/short composition and early lowerapron cutoff; own old cap/roundO/root are readable but oldcoil has closed-oval/broadmint read, not current shape authority.',
 'reference_change_root_PREPONLY_approval':'Root explicitly agreed: original commonlayout sole pose/facehandswaistbottom; correct11 head-lowroot-volume + latest0b88 + key, oldref2 history-only.',
 'reference_roles':[x['role'] for x in p['refs']],
 'current_curl_requirements':'Reasonable wholeheadshoulder-relative mass; broad gray front continuously turns into opaque inner/back return, next turn and taperC; no closed oval stack/solidcore/giant or micro, gray unlit allfaces, mint material only.',
 'occlusion_limit':'Current near-shoulder compression can hide lower return/C behind true shoulderfrill. Do not force visible full tail or move root; hidden geometry not certified.',
 'AI_motion_scope':'R81 full actual viewed only to describe compact near-shoulder recoil/occlusion. AI bitmap is not sent, no AI body/eye/root or intrinsic-mass copying; this is static phase evidence not played motion.',
 'risks':['Commonlayout missing original head may need careful cap reconstruction; future fresh check exact two leaves',
          'correct11 mouth/eyes/arm and verticalcoil must not replace own tinyO/contact source',
          'latestdetail polished shading must not become return shadows',
          'new output may still shorten lower apron; require actual whole-layer placement and source extent check, not blind enlarge/partwise warp'],
 'no_new_art_review_or_generation':True,'API_calls':0,'native_calls':0,'dynamic_validated':False,'user_accepted':False
})
lock=put('REQUEST_LOCK_PREPONLY.json',{
 'id':q['id'],'request':rec(request),'prompt':rec(q['prompt_file']),
 'ordered_refs':[rec(x) for x in q['refs']],
 'explicit_single_additional_user_waiver':q['user_waiver'],'provenance':rec(R/'REF_INPUT_PROVENANCE.json'),
 'source_and_artist_review':review,'local_parent_before':p['local_parent_instant_before'],
 'local_parent_whole_pending':rec(R/'LOCAL_PARENT_WHOLE_PENDING_FOR_V05.json'),
 'old_unknown_receipt':p['unknown_receipt'],'recovery_report':p['recovery_report'],
 'future_builtin_tool_arguments':q['tool_arguments'],'expected_additional_native_calls_after_root_release':1,
 'PREPONLY':True,'dispatchable':False,'root_execution_release_pending':True,
 'API_calls':0,'native_calls':0,'automatic_retries':0,
 'no_model_quality_size_parameters_exposed':True,'user_quality_preference':'high'
})
validation=put('PREPONLY_TECHNICAL_VALIDATION.json',{
 'id':q['id'],'technical_preparation_valid':True,'artistic_pass':False,
 'checks':['explicit user single-extra answer verbatim/id saved', 'old UNKNOWN receipt/recovery hashes read and preserved',
 'original source936/PTS499696 and first933..937 priority verified', 'four exact refs actual viewed and hash/order verified',
 'commonlayout selected source pixels equal original at same positions', 'current defaults LEFT prefix exact',
 'native tool arguments only prompt/refs/transparent_background', 'native size/quality/model not falsely exposed',
 'localparent exact instant snapshot and unchanged original', 'all oldv04 files unchanged',
 'no new imagegen/API/HTTP/attempt/central write'],
 'request_lock':lock,'API_calls':0,'native_calls':0,
 'generation_availability_or_quota_not_tested_in_PREPONLY':True,'quota_controls_not_read_or_reset':True
})
handoff=put('ARTIST_HANDOFF_PREPONLY.json',{
 'id':q['id'],'status':'DRAFT_READY_WITHOUT_SUBMIT','PREPONLY':True,'run':str(R),
 'request':rec(request),'prompt':rec(q['prompt_file']),'request_lock':lock,'waiver':q['user_waiver'],
 'ordered_refs':[rec(x) for x in q['refs']],
 'source_and_reference_provenance':rec(R/'REF_INPUT_PROVENANCE.json'),'artist_actual_input_review':review,'validation':validation,
 'old_unknown_receipt':p['unknown_receipt'],'old_recovery_report':p['recovery_report'],
 'local_parent_before':p['local_parent_instant_before'],'local_parent_new_whole_pending':rec(R/'LOCAL_PARENT_WHOLE_PENDING_FOR_V05.json'),
 'source_frame':936,'source_pts':499696,'first_case_frames':[933,937],
 'canvas_guidance':[704,976],'native_size_quality_model_parameters_exposed':False,
 'user_explicit_single_extra_generation':True,'additional_native_calls_used':0,'future_count_after_root_release':1,'automatic_retries':0,
 'old_v04_remote_unknown_not_resolved_or_erased':True,
 'reference_change':'Old32prefix with rejected coil removed from generation; correct11 fullhead216fd/latestgraydetail0b88/key. Single original source commoncanvas owns pose and complete visible lowerapron extent.',
 'must_preserve':['own round-open eyes/one uniformcharcoal and tinyO','own distinct front hand contacts',
 '704:976 common face-hand-waist-apron relation; no short body or new hidden legs/shoes',
 'low anatomicalLEFT/viewerRIGHT root; gray continuous front/opaque innerback return/nextturn/taperC and natural shoulderfrill occlusion'],
 'root_execution_release_still_pending':True,'before_future_call_refresh_localparent_snapshot_required':True,
 'future_result_needs_fresh_raw_white_black/source_extent_and_root_Sol_review_then_separate_photography':True,
 'API_calls':0,'native_calls':0,'central_registry_binding_exposure_written':False,'user_accepted':False,'dynamic_validated':False
})
print(json.dumps({'request':rec(request),'prompt':rec(q['prompt_file']),'waiver':q['user_waiver'],'lock':lock,'handoff':handoff,'calls':0},ensure_ascii=False))
