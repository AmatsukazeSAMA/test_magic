from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
from PIL import Image
RUN=Path(__file__).parent;B=RUN.parents[3];PROJECT=B.parents[1];PRIOR=RUN.parent/'whole_imggen_after_gray_material_restore_mint_returns_v16';I=RUN/'inputs'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
def save(name,o):
 p=RUN/name
 if p.exists():raise RuntimeError('preserve '+str(p))
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
now=datetime.now(timezone.utc).isoformat()
refs=[I/'ref1_CURRENT_V16_194d01e1_COMPLETE_RGBA_TARGET.png',I/'ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2.png',I/'ref3_G02_IRIS_INTERIOR_PIGMENT_ONLY_NO_LID_GLINT.png',I/'ref4_ORIGINAL2333_OWN_ROUND_EYES_APERTURE_ONLY.png']
assert sha(refs[0])=='194d01e113fb275957c254789857abaf5e8bf25afe2313f900a32f7ce10cac92'
mask=RUN/'mask_V16_GRAY_MATERIAL_INTERIORS_AND_WHOLE_IRIS_INTERIORS_v02.png'
assert Image.open(mask).size==Image.open(refs[0]).size==(957,1643)
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''\n\n只编辑图1蒙版透明开放的两类材料内区，输出完整透明人物。图1是已知保存的v16当前人物；保持全部原轮廓、宽灰前→内后返回→下一圈→C连接、正常整头相对体量、外甩相位、画右同侧低耳后双红珠和已恢复的薄mint。其几何/发量/根不是本次问题。\n\n卷发开放的灰色内区统一成图2的无光照GRAY#B6B4B2，与bob同灰：宽前面、内/后返回和C内面同一种灰颜料，不保留独立深灰体积暗面、不加高光/银亮/渐变。原thinmint边线与墨线、真正空气、全部alpha边界受保护；灰返回仍是不透明实体，不能挖成空气，不能涂成全mint或改变发带绕行。图2只给GRAY颜色，不替换图1灰/mint分区。\n\n两眼蒙版覆盖整个可见iris内部，包括原黑芯和下灰环/月牙；融合为一种均匀charcoal实色平形#303030，不是仅改内黑圆或再画暗芯/灰环。图3仅G02 iris内部颜料，没有睑形和白点可复制；图4仅原2333自己的圆睁开度/视线，保当前略不对称的圆睁和极小中性闭口，不改半睑/瞪眼/笑。眼白、原白glints、眼睑睫线眉脸都保护，不增心形glint、不规定白点数量。\n\n其余人物保持当前原2333斜跨低掌、腰后臂、衣服帽两主黑叶、肩frill、裙腿和底裁。未开放区域保持；不镜像、不挪珠根、不重设计卷、不增删发量，不改手指或source动作。保透明区透明，raw全透明像素内的隐藏RGB不是实体背景/灰发。该返回仅局修中间稿，之后另做整个人物连贯重绘并新审，不能直接当成最终稿。\n'''
promptpath=RUN/'prompt_api.txt';promptpath.write_text(prompt,encoding='utf-8')
formal=save('API_PREPARED_REQUEST.json',{'InputImages':[str(p) for p in refs],'PromptFile':str(promptpath),'MaskFile':str(mask),'OutputDirectory':str(RUN),'OutputFileName':'character_api_original.png','Size':'960x1648','Quality':'high','Background':'transparent'})
sol=B/'review/sol_xhigh_round168.json'
solentry=load(sol)['records'][0];assert solentry['image_sha256']==sha(refs[0])
localparent=RUN.parent/'local_material_uniform_gray_returns_extra_authorized_api_v04'
parentstatus=localparent/'LOCAL_REPAIR_STATUS.json'
save('ANCESTOR_LOCAL_REPAIR_STATUS_BEFORE_PREPARATION.json',{'source':meta(parentstatus),'snapshot':load(parentstatus),'read_only_snapshot_not_status_update':True,'snapshot_utc':now})
history=save('KNOWN_V16_TARGET_AND_HISTORICAL_UNKNOWN_BOUNDARY.json',{
 'target':meta(refs[0]),'v16_known_receipt':meta(PRIOR/'NATIVE_CALL_RECEIPT.json'),'v16_known_receipt_data':load(PRIOR/'NATIVE_CALL_RECEIPT.json'),
 'v16_operation':meta(PRIOR/'BUILTIN_GENERATION.json'),'v16_historical_local_parent':str(localparent),'v04_execution_receipt':meta(localparent/'ROOT_API_EXECUTION_RECEIPT.json'),
 'v03_historical_record':meta(RUN.parent/'local_material_uniform_gray_returns_api_v03/ROOT_API_EXECUTION_RECEIPT.json'),
 'old_unknown_receipts_and_recovery_unmodified':True,'historical_unknown_not_declared_resolved_by_this_request':True,
 'this_is_known_saved_v16_new_material_and_iris_defect':True,'this_is_not_unknown_v03_or_v04_retry':True,
 'this_is_not_new_FIRST':True,'fresh168':meta(sol),'original_source_frame':2333,'source_pts':1245520,
 'no_ancestor_status_or_raw_modified':True,'new_API_calls':0,'new_native_calls':0})
status=save('LOCAL_REPAIR_STATUS.json',{'id':'ART-G33-07','status':'PREPONLY_PENDING_ROOT_RELEASE_AND_API_RETURN','operation_kind':'local_mask_repair','planned_local_repair':True,'locally_repaired':False,'local_repair_completed':False,'requires_whole_imggen':True,'mandatory_whole_imggen':True,'whole_imggen_completed':False,'fresh_primary_and_independent_review_pending':True,'direct_final_selection_allowed':False,'future_local_parent':str(RUN),'historical_parent_before_snapshot':'ANCESTOR_LOCAL_REPAIR_STATUS_BEFORE_PREPARATION.json','PREPONLY':True,'submitted':False,'API_calls':0,'native_calls':0,'automatic_retries':0})
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
provider=PROJECT/'scripts/Invoke-ReferenceImage.ps1';config=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert load(config)['model']=='gpt-image-2.5-sunburst'
scope=save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{
 'id':'ART-G33-07','authorization':meta(auth),'question_id':load(auth)['question_call_id'],'user_reply_verbatim':load(auth)['user_reply_verbatim'],
 'scope':'Same project known-character repair, current drawing plus gray pigment/G02 iris-material-only/own2333 eye crop and necessary same-size RGBA mask to same official endpoint.',
 'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','n':1,'retry':0,'quality':'high','background':'transparent','output_size':'960x1648','input_and_mask_size':[957,1643],
 'refs':[meta(p) for p in refs],'mask':meta(mask),'formal':meta(formal),'root_specific_execution_release_received':False,'PREPONLY':True,'submitted':False,'API_calls':0,'native_calls':0,'HTTP_calls':0,'no_new_user_permission_flow_needed_for_preparation':True})
seen=[refs[0],*refs[1:],PRIOR/'qa_white.png',PRIOR/'qa_black.png',
 B/'review/sol_xhigh_round168_diagnostics/CURRENT_V16_ROOT_COIL_white_3x.png',B/'review/sol_xhigh_round168_diagnostics/CURRENT_V16_ROOT_COIL_black_3x.png',B/'review/sol_xhigh_round168_diagnostics/CURRENT_V16_OWN_EYES_white_4x.png',
 Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-07/source.png'),I/'SOURCE2333_COMPLETE_UNMASKED_GUIDE_FOR_FUTURE_WHOLE_NOT_API_REF.png',
 RUN/'PREP_PRIOR_CANDIDATE_194d01e1_EYE_VIEWER_LEFT_COORDINATE_GRID_10x.png',RUN/'PREP_PRIOR_CANDIDATE_194d01e1_EYE_VIEWER_RIGHT_COORDINATE_GRID_10x.png',RUN/'PREP_PRIOR_CANDIDATE_194d01e1_COIL_COORDINATE_GRID_5x.png',
 *[RUN/f'PREP_PRIOR_CANDIDATE_194d01e1_MASKv02_{s}.png' for s in ['OVERLAY_COIL_5x','OVERLAY_EYES_5x','ALPHA_COIL_5x','ALPHA_EYES_5x']]]
actual=save('ACTUAL_VIEWED_INPUTS_AND_PRIOR_DIAGNOSTICS.json',{'reviewer':'xhigh_pending_artist own tool image inspection','recorded_utc':now,'actual_viewed':[meta(p) for p in seen],'future_API_return_exists':False,'future_whole_return_exists':False,'all_prior_candidate_diagnostics_prepared_before_future_return':True})
review=save('ARTIST_SOURCE_REFERENCE_MASK_REVIEW_PREPONLY.json',{
 'id':'ART-G33-07','target_sha256':sha(refs[0]),'fresh168':meta(sol),'actual_viewed_list':meta(actual),
 'observations':['Currentv16 whole/raw/fullwhiteblack and new168 coil3x/eyes4x actually seen; normal external-swing volume/lowLEFT/root/two maincapleaves/grayopaque returns and thinmint restoration retained.',
 'P1 confirmed as distinct darker mid gray inner-back face and C gray inner band plus whole iris black-center/lowergrayring partitions; not currentgeometry/volume/phase/root P1.',
 'Maskv02 eyes each cover full iris fill and lower ring, not isolated pupil disks; source white glints plus1px safety protected, original round/asymmetric aperture unchanged.',
 'Maskv02 gray includes actual front/returns/C pigment interiors only, with mint/ink/air/alpha boundaries protected; conservative v01 C patch expanded50 interior pixels after actual5x, old files kept.',
 'Original2333 actual full and guide preserve slanted crossbody low hand/waistback arm, tinyneutralclosedmouth, originalfrills/legs/bottom cutoff. NewG02 crop is pure iris interior pigment, noF100 eyelid or heartglint pixels.'],
 'input_roles':['Currentv16 full target owns identity/geometry/mass/root/phase/action','PureGRAYkey only pigment','G02 iris interior only pigment no aperture/glint','Own2333 roundeyes only aperture/gaze no redidentity'],
 'excluded_generation_references':['oldv15 shaded coilcrop','glossy userdrill detail','full user11 verticalcoil identity','F100 half-lid image','AIbody or old07 geometryhead'],
 'mask_provenance':meta(RUN/'MASK_PROVENANCE_v02.json'),'alpha_EDITABLE_count':10282,'gray_editable_count':8130,'iris_editable_count':2152,
 'protect':['thinmint','ink','air','bob/root/beads','eye sclera/glints/lids','face/body/sourcehands/costume/crop'],
 'unknown_boundary':'Historical v03/v04 files are untouched; only current194d01 v16 known saved character is target. This request does not repeat any unknown result.',
 'mandatory_future_builtin_whole':True,'future_whole_dispatchable':False,'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'art_pass':False,'dynamic_validated':False,'user_accepted':False})
future=RUN/'future_mandatory_whole_PREPONLY';future.mkdir(exist_ok=True)
futuretarget=RUN/'character_api_original.png'
future_refs=[str(futuretarget),str(I/'SOURCE2333_COMPLETE_UNMASKED_GUIDE_FOR_FUTURE_WHOLE_NOT_API_REF.png'),str(refs[1]),str(refs[3])]
wp=prefix+'''\n\n以图1本次局修已正确的完整当前人物为基准，一次连贯重绘全部可见人物，透明背景；保持图1新修正的统一charcoal iris与灰/薄mint原分区，头颈帽肩发卷自然接合。所有可见灰前面/不透明内后返回/C都同bob无光照灰，图3只无打光GRAY颜料，不重新读回旧独立深暗体积面；薄mint与opaque返回、真实空气保图1，不挖gray返回。\n\n图2原2333完整guide仅拥有本帧动作、眼口/指形/衣肩/源裁切：原斜跨低掌/另一腰后臂、圆睁略异与极小中性闭口、屈膝裙腿不变。图4只原2333圆眼开度，不变半睑，不复制图2红发/尖长额发/双高卷。人物仍图1中性灰短bob，画右同耳后低LEFT双珠不动，当前合理外甩/宽灰前返回连通渐细C和整头发量保持，不改巨大/微型/竖挂。\n\niris完整内部是一种均匀charcoal平形，没有独立黑芯/灰环/月牙；原普通白点和眼白/睑线、视线保持。保持帽两片主要黑叶、暖桃肤、原黑白衣/红bow金扣/腰后带/手和原底裁，源未见鞋尖不补。整个人物一次统一线条与接合，不局部贴眼/贴卷或warp，真实透明无背景字幕色卡。\n'''
wholeprompt=future/'prompt_imggen_DRAFT.txt';wholeprompt.write_text(wp,encoding='utf-8')
whole=save('future_mandatory_whole_PREPONLY/request_imggen_DRAFT.json',{
 'id':'ART-G33-07','operation_kind':'whole_character_redraw','local_repair_parent':str(RUN),'mandatory_whole_imggen':True,'requires_fresh_root_and_Sol':True,
 'prompt_file':str(wholeprompt),'prompt_sha256':sha(wholeprompt),'prompt':wp,'refs_expected_after_future_return':future_refs,
 'reference_sha256':[None,sha(future_refs[1]),sha(future_refs[2]),sha(future_refs[3])],
 'tool_arguments_template':{'prompt':wp,'referenced_image_paths':future_refs,'transparent_background':True},
 'missing_input':{'path':str(futuretarget),'known_result_required':True,'must_actual_view_local_return_and_new_whiteblack_before_dispatch':True,'must_bind_exact_new_raw_sha256':True},
 'not_allowed_to_substitute_current_v16_or_old_dark_crop_for_future_result':True,
 'PREPONLY':True,'dispatchable':False,'native_calls_authorized':0,'API_calls':0,'native_calls':0,'automatic_retries':0,
 'native_quality_parameter_exposed':False,'user_quality_preference':'high','submitted':False})
lock=save('REQUEST_LOCK_PREPONLY.json',{
 'id':'ART-G33-07','formal':meta(formal),'prompt':meta(promptpath),'mask':meta(mask),'mask_provenance':meta(RUN/'MASK_PROVENANCE_v02.json'),'refs':[meta(p) for p in refs],
 'provenance':meta(RUN/'INPUT_PROVENANCE_INITIAL_PREPONLY.json'),'review':meta(review),'actual_view_list':meta(actual),'history':meta(history),'scope':meta(scope),'auth':meta(auth),'provider':meta(provider),'provider_configuration':meta(config),'Sol168':meta(sol),'local_repair_status':meta(status),'future_whole_draft':meta(whole),
 'prefix_text':prefix,'prefix_text_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'formal_field_count_including_MaskFile':8,
 'n':1,'retry':0,'PREPONLY':True,'dispatchable':False,'execution_released':False,'API_calls':0,'native_calls':0,'mandatory_future_builtin_whole':True})
print(json.dumps({'formal':meta(formal),'prompt':meta(promptpath),'mask':meta(mask),'lock':meta(lock),'future_whole_draft':meta(whole),'future_whole_prompt':meta(wholeprompt),'source_review':meta(sol)},ensure_ascii=False,indent=2))
