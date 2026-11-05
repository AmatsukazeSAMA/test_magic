from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json, hashlib
R=Path(__file__).resolve().parent
C=R.parent
B=R.parents[3]
PROJECT=B.parents[1]
OLD=C/'whole_imggen_source1123_uniform_charcoal_iris_v02'
ID='ART-G12-69'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
m=read(R/'MASK_PROVENANCE_v02.json')
assert sha(m['target']['path'])==m['target']['sha256']=='848f9fc11eb8b6bde3efe6671da32cec4c498906bb1b619bc2c274c8f4a68e90'
assert sha(m['mask']['path'])==m['mask']['sha256']=='c733fcd16a197f6cf5b0db6524c4eb6fa4a5057bdff2952287b9a2a7a223af69'
assert m['editable_pixels']==1679
refs=m['refs']
for ref in refs:assert sha(ref['path'])==ref['sha256']
assert len(refs)==4
for name in ['attempt.json','result.json','character_api_original.png','prompt_effective.txt','request_manifest.json']:
    assert not (R/name).exists(),name
attempts=[]
for p in C.rglob('attempt.json'):
    if R in p.parents:raise AssertionError('New local run unexpectedly has an attempt')
    a=read(p);rp=p.parent/'result.json';raw=Path(a.get('image',''))
    assert a['status']=='completed' and raw.is_file() and rp.exists()
    assert sha(raw)==read(rp)['output_sha256']
    attempts.append({'attempt':rec(p),'result':rec(rp),'raw':rec(raw),'known_saved':True})
natives=[]
for p in C.rglob('BUILTIN_GENERATION.json'):
    g=read(p);raw=Path(g['output_path']);assert sha(raw)==g['output_sha256']
    receipt=p.parent/'NATIVE_CALL_RECEIPT.json';rr=read(receipt)
    assert rr['known_result_saved'] and not rr['result_unknown']
    natives.append({'generation':rec(p),'receipt':rec(receipt),'raw':rec(raw),'known_saved':True})
assert len(attempts)==len(natives)==1
old_local=[rec(p) for p in C.rglob('LOCAL_REPAIR_STATUS.json') if R not in p.parents]
assert not old_local
history=put('KNOWN_HISTORY_AND_PARENT_BEFORE.json',{
    'id':ID,'recorded_utc':datetime.now(timezone.utc).isoformat(),'known_FIRST':attempts,'known_native':natives,
    'existing_local_ancestors':old_local,'unknown_results':[],
    'selected_before':read(B/'ASSET_REGISTRY.json')[ID],
    'parent_PRIMARY_before':{'file':rec(OLD/'PRIMARY_GOAL_REVIEW.json'),'exact':read(OLD/'PRIMARY_GOAL_REVIEW.json')},
    'parent_BUILTIN_before':{'file':rec(OLD/'BUILTIN_GENERATION.json'),'exact':read(OLD/'BUILTIN_GENERATION.json')},
    'old_art_reviews_and_receipts_preserved':True,'calls_this_preparation':0
})
solpath=B/'review/sol_xhigh_round160.json'
assert sha(solpath)=='02433265bee0ebd41c40ee6513e05f7d2bcc361a7a63051504ccb6124263dea3'
sol=read(solpath);entry=next(x for x in sol['entries'] if x['id']==ID)
assert entry['image_sha256']==m['target']['sha256'] and entry['review_status']=='repair_required'
solrec=put('FORMAL_SOL160_EXACT_READBACK.json',{'formal_report':rec(solpath),'exact_entry':entry,'readback_utc':datetime.now(timezone.utc).isoformat(),'new_API_or_whole_not_generated':True})
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
a=read(auth)
scope=put('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{
    'id':ID,'authorization':rec(auth),'question_text_readback':a['question_text'],'user_reply_verbatim':a['user_reply_verbatim'],
    'same_project_anime_character_references_and_necessary_eye_mask_covered':True,
    'endpoint':'https://api.openai.com/v1/images/edits','provider':'configured official OpenAI API',
    'current_parent_instruction':'PREPONLY API eye-iris local repair payload; no generation/network/attempt/central writes.',
    'PREPONLY':True,'execution_released':False,'API_calls_authorized_this_prep':0,
    'future_expected_count_on_separate_root_release':1,'no_new_permission_question_required_for_existing_project_scope':True,
    'unknown_paid_results_no_automatic_retry':True,'not_user_artistic_acceptance':True
})
defaults=read(PROJECT/'image_defaults.json');prefix=defaults['generation_prompt_prefix']['text']
prompt='\n\n'.join([
 prefix,
 '对图1这个已保存透明完整人物作一次必要的MASKED双虹膜颜料局修。只改蒙版alpha=0的两只iris内部，包含旧较黑圆芯和较浅外缘/下缘的整个颜料区；不是只改中央小圆。将它们融成图4同一种均匀charcoal（RGB48,48,48）实心平色形，不再保留独立瞳孔芯、黑圆、灰环、下月牙、径向层次或渐变。原虹膜外黑描线仍是描线，不向眼白扩张。',
 '蒙版alpha=255全部保护：原眼白、上/下睑外形、睫线、眉脸和已有普通圆白点不改。保图1/图2原1123前倾bow、不对称半开向下眼及当前视线、小闭弧笑，不能睁圆或压成闭线。图3只说明单色填法，不拥有开度/眼形/表情，不复制其近心形白点；原有白点数不增删。图4是单一颜料色块，没有眼形或瞳孔结构。',
 '图2仅供本源表演与衣裁核对，不复制红尖长额发/双高卷。蒙版外完整当前灰短圆润bob、帽两黑主叶、画右低解剖LEFT双珠根、肩前宽灰前返回渐细C、颈领、两手不同斜指/拇指与低肘、暖肤、红bow金扣/黑白衣/腰apron和半身底直切全部保持，不镜像不换根，不新画或重设计卷。',
 '返回完整当前可见人物的透明RGBA，不是眼部贴片、色卡或蒙版。保持当前整体头身/手位/实际半身裁切；输出1584x992只作接近原1587x991的整图尺寸适配，不单部位变换，不加隐藏腿鞋或背景字幕。此次局修是中间结果，之后必须另做一次内置imggen整体当前人物连贯重绘，再对新原字节实际复审；不能直接采用patch。'
])+'\n'
pf=R/'prompt_api.txt';assert not pf.exists();pf.write_text(prompt,encoding='utf-8')
request={
 'InputImages':[x['path'] for x in refs], 'PromptFile':str(pf),'MaskFile':m['mask']['path'],
 'OutputDirectory':str(R),'OutputFileName':'character_api_original.png',
 'Size':'1584x992','Quality':'high','Background':'transparent'
}
formal=put('API_PREPARED_REQUEST.json',request)
status=put('LOCAL_REPAIR_STATUS.json',{
 'id':ID,'operation_kind':'local_masked_whole_iris_pigment_repair','PREPONLY':True,'submitted':False,
 'intermediate_only':True,'must_follow_with_whole_character_imggen':True,
 'whole_character_imggen_completed':False,'mandatory_whole':True,'fresh_root_and_Sol_pending':True,
 'local_repair_parent_for_future_whole':str(R),'parent_known_native_raw_sha256':m['target']['sha256'],
 'not_inherit_parent_static_or_photography_pass':True,'API_calls':0,'native_calls':0,
 'user_accepted':False,'dynamic_validated':False
})
actual_paths=[
 OLD/'character_imggen_original.png',OLD/'qa_white.png',OLD/'qa_black.png',OLD/'ROOT_CURRENT_IRIS_WHITE_3x.png',
 B/'review/sol_xhigh_round160_diagnostics/EYES_black_3x.png',B/'review/sol_xhigh_round160_diagnostics/EYES_white_1x.png',
 B/'review/sol_xhigh_round160_diagnostics/LOW_ROOT_COIL_white_3x.png',
 Path(read(C/'JOB.json')['source_image']),OLD/'inputs/ref2_ORIGINAL1123_COMPLETE_UNMASKED_POSE_GUIDE.png',
 OLD/'inputs/ref3_G02_EYE_STYLE_ONLY_UNIFORM_CHARCOAL_NOT_APERTURE.png',OLD/'SOURCE1123_OWN_HALFOPEN_DOWNGAZE_MOUTH_READONLY.png'
]+[Path(x['path']) for x in refs]+[
 R/'qa_readonly/IMAGE_LEFT_IRIS_COORDINATE_GRID_10x_READONLY.png',R/'qa_readonly/IMAGE_RIGHT_IRIS_COORDINATE_GRID_10x_READONLY.png'
]+[R/'qa_readonly'/('PREP_PRIOR_CANDIDATE_848f9fc1_'+n) for n in [
 'MASKv02_OVERLAY_IMAGE_LEFT_IRIS_white_10x_READONLY.png','MASKv02_OVERLAY_IMAGE_RIGHT_IRIS_white_10x_READONLY.png',
 'MASKv02_ALPHA_BOTH_IRIS_6x_READONLY.png','MASKv02_OVERLAY_BOTH_IRIS_black_6x_READONLY.png',
 'MASKv02_OVERLAY_FULL_white_READONLY.png','MASKv02_OVERLAY_FULL_black_READONLY.png'
]]
actual=[{**rec(p),'actual_viewed_in_this_task':True,'not_a_future_API_result':True} for p in dict.fromkeys(actual_paths)]
review=put('ARTIST_REFERENCE_AND_MASK_REVIEW_PREPONLY.json',{
 'id':ID,'reviewer':'xhigh_pending_artist private input review','actual_viewed':actual,
 'P1_observed':'Both irises have a visibly darker round central region plus lighter outer/lower gray; reduced versus FIRST but still broad pigment shapes, not white glints or edge AA.',
 'changed_method':'Known failed direct whole method is preserved. New necessary API alpha-mask covers whole iris pigment, manually traced from outside boundary, including old core and lower/outer gray. Only boundary ink/sclera AA and existing glints protected.',
 'mask_v01_not_used':'Prelock diagnostic exposed six >80 sclera-AA edge pixels and outer ink; v01 unchanged preserved. V02 explicitly protects these boundary zones and re-viewed full white/black, both iris10x and alpha6x.',
 'mask_v02_observation':'Editable purple region spans old dark cores and lighter outer/lower pigment; black lid/contour, white sclera, white glints and face remain outside editable area. No whole eye/face rectangular edit.',
 'mask_statistics_not_artistic_pass':True,'entire_visible_iris_pigment_method_not_central_pupil_selection':True,
 'suggested_charcoal_RGB':[48,48,48],'this_color_number_is_input_choice_not_user_color_claim':True,
 'G02_method_only_not_aperture_or_glint_shape':True,
 'preserve_1123_asymmetric_halfopen_downgaze_smallclosed_smile_forwardbow':True,
 'crop_condition':'Preserve original halfbody straight bottom and current anatomy; later whole-layer 1080 photography must take straight bottom/empty strip offscreen. No hidden legs/shoes.',
 'post_API_required':'Actual full raw white/black/source eye compare, then mandatory coherent builtin whole redraw using successful patch as sole geometry target plus appropriate source method, then fresh root/Sol.',
 'risk':'Masked API may still drift protected pixels or retain dark center; output size slightly differs. Compare after whole-size alignment as readonly QA, no artwork compositing or automatic approval.',
 'API_calls':0,'native_calls':0,'user_accepted':False,'dynamic_validated':False
})
diag=[]
for p in sorted((R/'qa_readonly').glob('*.png')):
    diag.append({**rec(p),'source_image':m['target']['path'],'source_sha256':m['target']['sha256'],
                 'prepared_before_future_return':True,'not_evidence_of_future_API_or_whole_return':True,
                 'purpose':'readonly prior-candidate eye contour or API input mask permission overlay, not generated artwork'})
diagnames=put('READONLY_DIAGNOSTIC_SOURCE_IDENTITY.json',{
 'id':ID,'source_image':m['target']['path'],'source_sha256':m['target']['sha256'],
 'prepared_before_future_return':True,'all_diagnostics':diag,
 'v01_generic_filenames_preserved_not_deleted_or_relabelled':True,
 'v02_new_diagnostic_prefix':'PREP_PRIOR_CANDIDATE_848f9fc1_',
 'future_new_API_and_whole_return_diagnostics_must_use_new_raw_SHA':True
})
helper=PROJECT/'scripts/Invoke-ReferenceImage.ps1'
config=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
cfg=read(config);assert cfg['model']=='gpt-image-2.5-sunburst'
provenance=put('INPUT_PROVENANCE.json',{
 'id':ID,'source_frame':1123,'source_pts':599536,'first_case_frames':[1123,1128],
 'target':m['target'],'refs':refs,'mask':m['mask'],'mask_provenance':rec(R/'MASK_PROVENANCE_v02.json'),
 'formal_request':formal,'prompt':rec(pf),'formal_Sol160_readback':solrec,'known_parent_history':history,
 'source_JOB':rec(C/'JOB.json'),'source_REGISTRATION_PLAN':rec(C/'REGISTRATION_PLAN.json'),
 'source_original':rec(read(C/'JOB.json')['source_image']),
 'project_scope_existing_authorization':scope,'actual_input_review':review,'readonly_diagnostic_source_map':diagnames,
 'wrapper':rec(helper),'provider_configuration':rec(config),'configured_model':cfg['model'],
 'endpoint':'https://api.openai.com/v1/images/edits','n':1,'automatic_retries':0,
 'input_and_mask_exact_size':[1587,991],'output_size':'1584x992',
 'size_boundary':'Parent requested near-aspect 16-multiple output; wrapper accepts Size string and does not validate multiples/min. No unverified claim about Sunburst hard size limits; no test call.',
 'original_raw_inputs_and_prior_failed_native_preserved':True,
 'central_JOB_REGPLAN_asset_and_binding_modified':False,
 'PREPONLY':True,'execution_released':False,'API_calls':0,'native_calls':0
})
lock=put('REQUEST_LOCK_PREPONLY.json',{
 'id':ID,'PREPONLY':True,'dispatchable':False,'execution_released':False,
 'formal':formal,'prompt':rec(pf),'mask':m['mask'],'refs':[{k:x[k] for k in ('path','sha256','bytes','size','mode')} for x in refs],
 'provenance':provenance,'mask_provenance':rec(R/'MASK_PROVENANCE_v02.json'),
 'history':history,'Sol160':rec(solpath),'scope':scope,'auth':rec(auth),
 'provider':rec(helper),'provider_configuration':rec(config),'prefix_text':prefix,
 'local_repair_status':status,'mask_review':review,
 'formal_base_fields':8,'necessary_mask_extra_field':'MaskFile','formal_total_fields':9,
 'n':1,'retry':0,'API_calls':0,'native_calls':0,
 'future_release_required_before_network':True,'unknown_paid_result_no_retry':True
})
print(json.dumps({'formal':formal,'prompt':rec(pf),'mask':m['mask'],'lock':lock,'provenance':provenance,'calls':0},ensure_ascii=False))
