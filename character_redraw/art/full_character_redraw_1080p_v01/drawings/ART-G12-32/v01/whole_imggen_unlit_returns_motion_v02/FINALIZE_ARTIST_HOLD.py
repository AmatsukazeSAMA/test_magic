from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib

RUN=Path(__file__).resolve().parent
BASE=RUN.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def e(p):return {'path':str(p),'sha256':sha(p)}
def save(name,obj):
    p=RUN/name;assert not p.exists(),str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return e(p)
raw=RUN/'character_imggen_original.png'
expected='22dc5dfd5f3c3418c0d74c4200cac5823fe917ae2b29ce1b6090941c96a65d75'
assert sha(raw)==expected
assert sha(RUN/'request_imggen.json')=='aeab71230c9743abc4628c249ea2b4bf2562c4c2d4f230059e20a7796aa9ad79'
assert (RUN/'request_imggen.json').read_bytes()==(RUN/'REQUEST_AT_NATIVE_CALL.json').read_bytes()
receipt=json.loads((RUN/'NATIVE_CALL_RECEIPT.json').read_text(encoding='utf-8'))
assert raw.read_bytes()==Path(receipt['source_generated_file']).read_bytes()
diag=json.loads((RUN/'RETURN_DIAGNOSTIC_PROVENANCE.json').read_text(encoding='utf-8'))
after=json.loads((RUN/'LOCAL_REPAIR_PARENT_STATUS_AFTER_REGISTER.json').read_text(encoding='utf-8'))
assert after['whole_character_imggen_result']==str(raw)
assert after['whole_character_imggen_completed'] is True
assert after['fresh_whole_image_visual_review']=='pending'
actual=[RUN/n for n in [
    'character_imggen_original.png','qa_white.png','qa_black.png',
    'diagnostics/RETURN_HEAD_ROOT_COIL_white_1x.png',
    'diagnostics/RETURN_LOW_ROOT_COIL_white_1x.png','diagnostics/RETURN_LOW_ROOT_COIL_black_3x.png',
    'diagnostics/OLD_NEW_COIL_RETURNS_NORMAL1X_white.png','diagnostics/OLD_NEW_COIL_RETURNS_NORMAL1X_black.png',
    'diagnostics/RETURN_EYES_MOUTH_white_2x.png','diagnostics/RETURN_HANDS_CONTACTS_white_1x.png',
    'diagnostics/ORIGINAL_OLDWHOLE_NEW_RETURN_COMPARISON_READONLY.png']]
review={
    'id':'ART-G12-32','reviewer':'xhigh_pending_artist private actual-view draft, not root or Sol',
    'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'image':str(raw),'image_sha256':expected,
    'dimensions':list(Image.open(raw).size),'status':'HOLD_REPAIR_REQUIRED_REPEATED_DARK_RETURNS_P1_PERSISTS',
    'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
    'not_a_central_PRIMARY_GOAL_REVIEW':True,
    'observations':[
        'Actually viewed raw/full white/full black; normal1x head/low-root coil and old-new coil both-background comparisons; black3x returns, eyes2x, hands1x and source-old-new figure comparison.',
        'Original round-open mono-charcoal eyes/ordinary white dots and tiny open-O mouth, original overlapping distinct fingers/contacts and white cuffs are broadly retained; no smile or AI body substitution.',
        'Only the same anatomical LEFT / IMAGE RIGHT low bob-nape two-bead coil remains, with two black cap leaves. Side/root not elevated or mirrored, no second cap coil.',
        'Wide opaque gray front/return folds remain continuously connected and taper; the darker returned surfaces are hair, not air to delete. Mint still separate, not all-mint. Hidden axis/air and complete topology not certified.',
        'Material correction did not succeed: at normal1x, multiple repeated returns still read as clearly darker underside panels than adjacent gray front and bob, closely matching the prior rejected lighting pattern. This persists on both backgrounds, not raw hidden RGB or one AA pixel.',
        'Body/costume/half-body crop, black collar/long sleeves/red bow gold/white cap, shoulder frill/vertical trim/apron/waist/rear ties and warm skin retained. Whole drawing remains coherent.',
        'Raw edge/bottom hidden RGB noise is not visible as opaque background debris in full white/black QA. No separate matte failure is asserted from raw preview alone.',
        'Raw preserved exactly as generated. One native whole call; no retry, code recolor, local patch or second reference test.'
    ],
    'issues':[
        {'severity':'P1','code':'repeated_dark_return_shading_persists','region_raw_xyxy_approx':[700,610,835,885],
         'observation':'Upper/middle/lower gray return panels repeatedly remain markedly darker than bob/front gray at normal1x, still forming shaded underside volume. The unlit-key instruction did not unify these opaque surfaces. This repeats the Sol94 material P1.',
         'required_boundary':'Retain opaque gray returns and continuous connection; do not fix by cutting holes, turning all returns mint, or certifying hidden geometry.'},
        {'severity':'P2','code':'long_exposed_projection_not_R81_verified','region_raw_xyxy_approx':[675,470,855,935],
         'observation':'Curl remains comparatively long/exposed and downward rather than the R81 compact near-shoulder occluded state. This is motion/projection uncertainty, not a fixed-length/hole automatic P1 and not dynamic validation.'}
    ],
    'material_samples_support_only':{
        'basis':'Supplement to actual normal1x/full-QA visual judgment; same-size old/new internal surface samples, not pass thresholds or substitutes for visual review.',
        'samples':diag['material_sample_support_only']
    },
    'hypothesis_result':{
        'tested':'Original action guide + old coherent whole full white/black + pure unlit key, exact4refs.',
        'outcome':'Pose/gray-mint partition preserved but repeated dark gray returns remained, so this reference/material hypothesis failed the intended correction.',
        'inference_only':'Old target dark-surface appearance may have outweighed the pigment-key role, but no internal model cause is proven.',
        'next_action':'Stop and report. Any changed-reference hypothesis or next call requires parent decision; no prompt-stacking retry.'
    },
    'actual_viewed_paths_with_sha256':[e(p) for p in actual],
    'source_observation_before_call':e(RUN/'SOURCE_OBSERVATION_xhigh_v02.json'),
    'old_failure_report':e(BASE/'review/sol_xhigh_round94.json'),
    'local_repair_parent':receipt['local_repair_parent'],
    'local_parent_before':e(RUN/'LOCAL_REPAIR_PARENT_STATUS_BEFORE.json'),
    'local_parent_after_register':e(RUN/'LOCAL_REPAIR_PARENT_STATUS_AFTER_REGISTER.json'),
    'mandatory_whole_character_generation_completed':True,
    'fresh_whole_visual_review_status':'pending root and independent actual view; technical mandatory generation completion is not art acceptance',
    'old_pass_inherited':False,'technical_success_is_art_pass':False,'user_accepted':False,
    'hidden_geometry_certified':False,'dynamic_validated':False,'photographic_registration_validated':False,
    'native_calls_this_release':1,'api_calls':0,'automatic_retries':0,'in_flight':0,
    'central_registry_binding_exposure_progress_count_write':False,
    'next_step':'Stop after this one authorized whole and hand off failed material evidence to parent fresh review.'
}
draft=save('DRAFT_PRIMARY_REVIEW.json',review)
handoff={
    'id':'ART-G12-32','run':str(RUN),'status':'RETURNED_ONE_WHOLE_HOLD_MATERIAL_P1_PERSISTS',
    'raw':e(raw),'raw_dimensions':list(Image.open(raw).size),'original_generated_file':e(Path(receipt['source_generated_file'])),
    'original_bytes_preserved':True,'full_white_qa':e(RUN/'qa_white.png'),'full_black_qa':e(RUN/'qa_black.png'),
    'private_artist_draft':draft,'call_receipt':e(RUN/'NATIVE_CALL_RECEIPT.json'),
    'request':e(RUN/'request_imggen.json'),'parent_endtoend_release':e(RUN/'PARENT_ENDTOEND_RELEASE.json'),
    'source_comparison':e(RUN/'diagnostics/ORIGINAL_OLDWHOLE_NEW_RETURN_COMPARISON_READONLY.png'),
    'normal_material_comparisons':[e(RUN/'diagnostics'/n) for n in ('OLD_NEW_COIL_RETURNS_NORMAL1X_white.png','OLD_NEW_COIL_RETURNS_NORMAL1X_black.png')],
    'diagnostic_provenance':e(RUN/'RETURN_DIAGNOSTIC_PROVENANCE.json'),
    'decisive_failure':'Repeated dark gray underside/return panels persist at normal1x; not an unlit-material repair success.',
    'preserved':'Original round mono/O-mouth, touching forward hands, sole correct low root/two beads, two leaves, wide opaque returns, costume/half-body crop.',
    'local_repair_parent':receipt['local_repair_parent'],
    'local_parent_status_before':e(RUN/'LOCAL_REPAIR_PARENT_STATUS_BEFORE.json'),
    'local_parent_status_after_register':e(RUN/'LOCAL_REPAIR_PARENT_STATUS_AFTER_REGISTER.json'),
    'mandatory_whole_generation_completed':True,'fresh_whole_visual_review':'pending root/Sol, no legacy pass inherited',
    'native_wrapper_elapsed_ms':receipt['wrapper_elapsed_ms'],
    'calls':{'native':1,'API':0,'automatic_retries':0,'in_flight':0},
    'central_registry_binding_exposure_progress_count_write':False,
    'next_step':'No second call, local fix or adjacent item. Await parent actual review and any changed-reference authorization.'
}
handoff_record=save('ARTIST_RETURN_HANDOFF.json',handoff)
print(json.dumps({'raw':e(raw),'draft':draft,'receipt':e(RUN/'NATIVE_CALL_RECEIPT.json'),'handoff':handoff_record,'status':'HOLD','in_flight':0},ensure_ascii=False,indent=2))
