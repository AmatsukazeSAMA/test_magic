from pathlib import Path
from PIL import Image
import hashlib, json, shutil
from datetime import datetime, timezone

RUN=Path(__file__).resolve().parent
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
PROJECT=Path('D:/CODEX/魔术之心')
CUR=B/'drawings/ART-G33-17/v01/whole_imggen_source2374_openeyes_bobonly_20v06_frontshoulder_v06'
NOW=datetime.now(timezone.utc).isoformat()
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
 p=Path(p);return {'path':str(p),'sha256':h(p),'bytes':p.stat().st_size}
def save(name,obj):
 p=RUN/name;assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
def savetext(name,text):
 p=RUN/name;assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');return p

refs=[RUN/'inputs/ref1_KNOWN_V06_194be4c4_COMPLETE_RGBA_TARGET.png',RUN/'inputs/ref2_ORIGINAL2374_COMPLETE_UNMASKED_ACTION_GUIDE.png',RUN/'inputs/ref3_USER_APPROVED11_COMPLETE_SPIRAL_TAPER_C_GEOMETRY_ONLY.png',RUN/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png']
expected=['194be4c44f1c4e61991b62230a2140795f78c25368fec78ed4c007846f6984ed','ccabdaf57ec5ff9b3bab5963c41da69c58491e3614791910a685cc13d7b14eea','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959','249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
assert [h(p)for p in refs]==expected
mask=RUN/'mask_V06_VISIBLE_COIL_RIBBON_FORKS_JOINS_ONLY_957x1644_v02.png'
assert Image.open(mask).size==Image.open(refs[0]).size==(957,1644)
maskmeta=RUN/'MASK_PROVENANCE_PREPONLY_v02.json'
defaults=PROJECT/'image_defaults.json'
prefix=json.loads(defaults.read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
provider=PROJECT/'scripts/Invoke-ReferenceImage.ps1'
cfg=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert json.loads(cfg.read_text(encoding='utf-8-sig'))['model']=='gpt-image-2.5-sunburst'
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert h(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
sol=B/'review/sol_xhigh_round179.json'
soldata=json.loads(sol.read_text(encoding='utf-8-sig'))
entry=next(e for e in soldata['entries']if e['id']=='ART-G33-17')
assert entry['image_sha256']==expected[0] and entry['repair_required']
native=CUR/'NATIVE_CALL_RECEIPT.json';builtin=CUR/'BUILTIN_GENERATION.json'
native_data=json.loads(native.read_text(encoding='utf-8-sig'))
assert native_data['known_result_saved'] and not native_data['result_unknown']
assert native_data['raw_sha256']==expected[0]
assert json.loads(builtin.read_text(encoding='utf-8-sig'))['local_repair_parent'] is None

prompt=prefix+'\n\n'+'''图1是当前完整人物编辑目标，蒙版的透明区才可重画；保留其余全部人物像素与完整两鞋，输出960×1648真实透明人物，不改变构图、头身、姿势或裁切。

只修画右肩前可见钻发：把中段分成数个毛尖/叉口、下面另鼓出圆灰囊的形状，改成同一条宽GRAY发带持续绕行。宽灰前面翻向内侧，仍是不透明同灰返回面，顺畅接入下一转，再渐细收向C形末端；内外回折的边线和互遮要能追踪，不用薄荷条绑住直发束。上下都连贯，不画封口椭圆片堆、实心锥、分叉发梢或独立灰囊。存在的真实空气保留透明，灰返回面保留实体；不按固定洞数挖孔。保当前中等发量和整头、肩部的相对体量，不能缩成小挂件或放大成粗柱。

保图1现有同一解剖LEFT低耳后根：当前朝画右的正面三分之四，远侧画右低根由bob自然遮住，卷沿肩前胸侧露出；不换近耳、不抬根、不另长第二束。上部未开放的颈后接点、红结金扣和白肩褶构成现有遮挡边，均保持，不能用扩大衣肩遮掉问题。

图2原2374只决定本张圆睁眼的开度视线、小闭笑、头向、腰后双臂、帽的两片主要黑叶、衣裙腿及完整两鞋，不复制红头发、高红卷或尖刘海。图3只说明连续灰发带前返、接下转、渐细与末C的结构，不复制它的小红珠/根位、白褶、衣服、固定轴向或圈数，不把裁图尺寸当人物发量比例。图4只定无光照GRAY颜料#B6B4B2，所有灰前面/内后返回同灰，薄mint#B0C8BA仅为沿发带绕行的窄材料边，无格纹、方向暗底、银白高光或渐变。当前单charcoal虹膜、普通白点、暖桃肤色、灰短bob、两主帽叶与原身体表演全部保持。'''
promptpath=savetext('prompt_api.txt',prompt+'\n')
formal=save('API_PREPARED_REQUEST.json',{'InputImages':[str(p)for p in refs],'PromptFile':str(promptpath),'MaskFile':str(mask),'OutputDirectory':str(RUN),'OutputFileName':'character_api_original.png','Size':'960x1648','Quality':'high','Background':'transparent'})
roles=[
 'Complete exact known current17 V06 957x1644 RGBA EDIT TARGET. Source body/round-openeyes/tinyclosedsmile/cap2leaves/low-farLEFT FRONT route and full shoes preserved; visible forked mid/lower grayhair geometry is explicitly wrong and edited only inside mask.',
 'Unmasked original canonical2374 guide; sole own current action, face aperture/gaze/closed smile, headturn, waistback arms, costume, cap2mainleaves and complete legs/two shoes. Original redhair/highredcoils are not target identity/root.',
 'User-approved old11 complete77x154 spiral/taper/C geometry ONLY, from old11raw[274,228,351,382]. Small bead/bob/frill/cloth slivers do not determine root, head, clothes, pose, scale, fixed axis/circle/hole count or illumination.',
 'Pure uniformGRAY #B6B4B2 pigment only. Thinmint described in words; no equalmintpalette, gloss detail, shaded coil or bob-hairtuft geometry template.'
]
sources=[CUR/'character_imggen_original.png',B/'drawings/ART-G33-17/v01/inputs/source_pose_guide.png',B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png',CUR/'inputs/ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png']
records=[dict(rec(p),reference_number=i+1,source_image=str(sources[i]),source_sha256=h(sources[i]),dimensions=list(Image.open(p).size),role=roles[i],copied_bytes_unchanged=p.read_bytes()==sources[i].read_bytes(),source_pixels_actual_viewed_this_prep=True)for i,p in enumerate(refs)]
provenance=save('INPUT_PROVENANCE_PREPONLY.json',{'id':'ART-G33-17','PREPONLY':True,'recorded_utc':NOW,'references':records,'source_frame':2374,'source_pts':1267408,'time_base':'1/16000','first_exposure_frames':[895,898],'first_exposure_pts_range':[477808,479952],'source_guide_unmodified':True,'original_canonical':rec('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-17/source.png'),'existing_target_known':rec(native),'mask_is_input_only_not_art_patch':True,'source_art_pixels_modified':False,'reference3_no_reframe_or_scale_teacher':True,'references_excluded':['20 grayblob/frontcoil geometry crop','07 wrong coil templates','G02 aperture template','AI fullbody or eyes','gloss or dark-return material example'],'api_calls':0,'native_calls':0,'HTTP_calls':0})
history=save('KNOWN_RETURN_HISTORY_BOUNDARY_PREPONLY.json',{'id':'ART-G33-17','target':rec(refs[0]),'native_receipt':rec(native),'builtin_generation':rec(builtin),'current_known_result_saved':True,'current_result_unknown':False,'current_native_elapsed_wall_ms':35254,'current_local_repair_parent':None,'new_operation_kind':'masked_visible_hair_ribbon_geometry_repair','not_an_unknown_paid_retry':True,'fresh179':rec(sol),'fresh179_status':entry['status'],'fresh179_P1':entry['issues'][0],'old_raw_and_reviews_preserved':True,'root_review_not_written_by_artist':True,'no_existing_new_run_attempt_or_result':True})
actual_paths=[refs[0],CUR/'qa_white.png',CUR/'qa_black.png',refs[1],refs[2],refs[3],B/'review/sol_xhigh_round179_diagnostics/CURRENT_V06_194be4c4_FULL_FRONT_COIL_BOW_T_TIPS_white_4x.png',RUN/'PREP_PRIOR_CANDIDATE_194be4c4_COIL_COORDINATES_white_4x_QA_ONLY.png']+[RUN/name for name in ['MASK_OVERLAY_FULL_white_QA_ONLY.png','MASK_OVERLAY_FULL_black_QA_ONLY.png','MASK_OVERLAY_COIL_white_4x_QA_ONLY.png','MASK_OVERLAY_COIL_black_4x_QA_ONLY.png','MASK_ALPHA_COIL_4x_QA_ONLY.png','MASK_PROTECTED_BOW_GOLD_WHITE_FRILL_4x_QA_ONLY.png','MASK_V02_OVERLAY_FULL_white_QA_ONLY.png','MASK_V02_OVERLAY_FULL_black_QA_ONLY.png','MASK_V02_OVERLAY_COIL_white_4x_QA_ONLY.png','MASK_V02_OVERLAY_COIL_black_4x_QA_ONLY.png','MASK_V02_ALPHA_COIL_4x_QA_ONLY.png','MASK_V02_PROTECTED_BOW_GOLD_WHITE_FRILL_4x_QA_ONLY.png']]
actual=save('ARTIST_ACTUAL_INPUT_AND_MASK_VIEW_PREPONLY.json',{'id':'ART-G33-17','reviewer':'xhigh_pending_artist; private artist observations only','recorded_utc':NOW,'source_raw_sha256':expected[0],'actual_viewed':[dict(rec(p),dimensions=list(Image.open(p).size),actually_viewed=True)for p in actual_paths],'byteidentical_refs2_4_viewed_at_source_paths':[str(p)for p in sources[1:]],'observations':['Current mid/lower visible graywideface splits into 2-3 hairtips, with separate rounded grayface below; agree fresh179 P1. This is not a test of hole count or visible hidden3D topology.','V02 fullwhite/fullblack and4x overlay: edit region covers grayfronts/returns/forked silhouette/round pouch and small connection margin, while bow/gold/whitefrill remain visually untouched. Face, bob, low root/top contact, cap, hands/body/full skirt and two shoes are outside mask.','Initial unrestricted white-label mask had protection islands at low-alpha white edge values; original mask/QA preserved. V02 restricts white labels to actual frill windows and alpha>128, making fork-geometry edit region continuous.','Geometryref3 has a small bead/bob/frill context; role is only complete ribbon topology, not new root/body/volume projection.','Mask geometry/protection is technically prepared; no repaired artwork exists, no art pass or temporal continuity certification.'],'selected_mask':rec(mask),'mask_metadata':rec(maskmeta),'actual_overlay_preparation_accepted_for_root_review_only':True,'api_calls':0,'native_calls':0,'HTTP_calls':0,'root_release_received':False})
scope=save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{'id':'ART-G33-17','PREPONLY':True,'root_execution_release_received':False,'authorized_api_calls_this_prep':0,'broad_authorization':rec(auth),'user_reply_verbatim':'允许本次44及GOAL后续同类素材','original_question_includes':'此GOAL后续同类人物稿、参考图及必要蒙版发送至同一官方API，范围仅限本项目绘制素材','endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','operation_scope':'Same-project known character and necessary hair geometry input mask; future one official high edit only after root actual review/release. Current command Preview only.','exact_payload_refs':records,'mask':rec(mask),'provider':rec(provider),'provider_configuration':rec(cfg),'no_other_files_to_be_sent':True,'n':1,'retry':0,'execution_not_authorized_here':True,'user_unknown_no_auto_retry_preserved':True})
local=save('LOCAL_REPAIR_STATUS.json',{'id':'ART-G33-17','PREPONLY':True,'status':'prepared_not_submitted_pending_root_review_release','target':rec(refs[0]),'intermediate_only':True,'local_repair_required':True,'local_repair_performed':False,'mandatory_whole_character_redraw_after_local_repair':True,'mandatory_whole_pending':True,'whole_character_completed':False,'fresh_primary_review_required':True,'fresh_independent_review_required':True,'final_asset_selectable':False,'parent_whole_known_no_local_ancestor':rec(builtin),'api_calls':0,'native_calls':0,'HTTP_calls':0,'root_release_received':False,'automatic_retries':0})
request=save('request_api_PREPONLY.json',{'id':'ART-G33-17','PREPONLY':True,'dispatchable':False,'recorded_utc':NOW,'operation_kind':'masked_visible_hair_ribbon_geometry_repair','transparent_background':True,'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','quality':'high','n':1,'retry':0,'size':'960x1648','input_mask_size':[957,1644],'formal_request':rec(formal),'prompt':rec(promptpath),'mask':rec(mask),'references':records,'changed_reference_hypothesis':'Known V06 full target + own source + user-approved complete spiral geometry + pureGRAY. Remove20 frontcoil/blob reference as geometry teacher; open the failing grayfront/return/fork/join region while preserving compatible route/body. This controls a reference conflict; no causal mechanism is claimed proven.','fresh179':rec(sol),'local_repair_parent':None,'mandatory_whole_after_local':True,'root_release_received':False,'api_calls_authorized_this_prep':0,'technical_prepared_is_not_artistic_pass':True,'no_central_changes':True})

future_dir=RUN/'future_mandatory_whole_PREPONLY';future_dir.mkdir(exist_ok=True)
future_prompt=savetext('future_mandatory_whole_PREPONLY/prompt_imggen_TEMPLATE_NOT_DISPATCHABLE.txt',prefix+'\n\n'+'''以图1未来局修的完整人物返图为当前人物，按图2原2374保原圆睁视线/小闭笑/头向/腰后手与衣裙腿完整两鞋，将整个当前可见人物一次连贯重绘，统一头颈帽肩与卷发接合。保已实看确认的同一远LEFT低根、肩前白褶/红结T遮挡和中等发量；宽灰前面翻入同灰不透明返回面、接下一转再渐细C，卷不要变直发叉尖、独立灰囊或封口片堆。不强露根/两珠/全C、不固定孔数。图3仅无光照gray颜料，灰front/inner/back/return同色，薄mint材料边；不添暗底、高光或渐变。整个人物透明。未来局修必须先保存与实际查看；若仍结构失败或新增错误，先报告root，不据此模板自动提交或宣称修复成功。\n''')
future=save('future_mandatory_whole_PREPONLY/request_imggen_DRAFT.json',{'id':'ART-G33-17','PREPONLY':True,'dispatchable':False,'operation_kind':'whole_character_redraw','transparent_background':True,'local_repair_parent':str(RUN),'mandatory_whole_after_local':True,'future_local_result_required':str(RUN/'character_api_original.png'),'future_local_result_sha256':None,'future_local_actual_review_required':True,'references':[{'path':str(RUN/'character_api_original.png'),'sha256':None,'role':'Future known locally repaired complete character; must be actually reviewed before selecting a whole redraw hypothesis.'},records[1],records[3]],'prompt_template':rec(future_prompt),'input_files_not_ready':True,'root_release_received':False,'native_calls_authorized':0,'requires_new_immutable_exact_request_after_local_known_actual_review':True,'fresh_root_and_Sol_required_after_whole':True,'API_patch_never_final':True,'quality_preference':'high','native_quality_parameter_exposed':False,'automatic_retry':False})

lockdata={'id':'ART-G33-17','PREPONLY':True,'root_release_received':False,'api_calls_authorized_this_prep':0,'n':1,'retry':0,'transparent_background':True,'prefix_text':prefix,'prefix_sha256':hashlib.sha256(prefix.encode()).hexdigest(),'formal':rec(formal),'request':rec(request),'prompt':rec(promptpath),'mask':rec(mask),'mask_provenance':rec(maskmeta),'refs':[rec(p)for p in refs],'provenance':rec(provenance),'artist_actual_view':rec(actual),'history':rec(history),'scope':rec(scope),'auth':rec(auth),'provider':rec(provider),'provider_configuration':rec(cfg),'local_status':rec(local),'future_whole':rec(future),'future_prompt':rec(future_prompt),'fresh179':rec(sol)}
lock=save('REQUEST_LOCK_PREPONLY.json',lockdata)
locksha=h(lock)
guard='''#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCKSHA__'){throw 'Immutable lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
$entries=@($locked.formal,$locked.request,$locked.prompt,$locked.mask,$locked.mask_provenance,$locked.provenance,$locked.artist_actual_view,$locked.history,$locked.scope,$locked.auth,$locked.provider,$locked.provider_configuration,$locked.local_status,$locked.future_whole,$locked.future_prompt,$locked.fresh179)+@($locked.refs)
foreach($item in $entries){if((Get-FileHash -LiteralPath $item.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256){throw ('Prepared item changed: '+$item.path)}}
$request=Get-Content -LiteralPath $locked.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($request.Count -ne 8 -or $request.InputImages.Count -ne 4 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '960x1648' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Exact8-field parameters changed.'}
for($i=0;$i -lt 4;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $locked.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured provider model changed.'}
$defs=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defs.generation_prompt_prefix.enabled -or $defs.generation_prompt_prefix.text -ne $locked.prefix_text -or -not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix changed.'}
foreach($name in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png','api_response.raw.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw ('Existing execution artifact; recover, never resubmit: '+$name)}}
# PREVIEW ONLY. Wrapper returns before key decryption, attempt creation and HTTP.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.n -ne 1 -or -not $preview.mask_provided -or $preview.input_count -ne 4 -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Preview boundary changed.'}
$output=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $output){throw 'Existing Preview evidence preserved.'}
$proof=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;exact_lock_sha256='__LOCKSHA__';formal_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;execution_released=$false;root_release_received=$false;api_calls=0;native_calls=0;HTTP_calls=0;automatic_retries=0;no_key_decryption_or_network=$true;technical_preview_not_art_acceptance=$true}
[IO.File]::WriteAllText($output,($proof|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
'''.replace('__LOCKSHA__',locksha)
guardpath=savetext('Preview-ExactVisibleRibbonMaskOnly.ps1',guard)
handoff=save('ARTIST_HANDOFF_PREPONLY.json',{'id':'ART-G33-17','status':'DRAFT_READY_WITHOUT_SUBMIT','PREPONLY':True,'dispatchable':False,'root_release_received':False,'run':str(RUN),'request':rec(request),'formal':rec(formal),'prompt':rec(promptpath),'lock':rec(lock),'mask':rec(mask),'mask_dimensions':[957,1644],'requested_output':'960x1648','quality':'high','background':'transparent','n':1,'retry':0,'reference_count':4,'refs':[rec(p)for p in refs],'mask_provenance':rec(maskmeta),'artist_actual_view':rec(actual),'fresh179':rec(sol),'future_whole_template':rec(future),'Preview_only_guard':rec(guardpath),'root_look_first':['MASK_V02_OVERLAY_FULL_white_QA_ONLY.png','MASK_V02_OVERLAY_FULL_black_QA_ONLY.png','MASK_V02_OVERLAY_COIL_white_4x_QA_ONLY.png','MASK_V02_OVERLAY_COIL_black_4x_QA_ONLY.png','MASK_V02_ALPHA_COIL_4x_QA_ONLY.png','MASK_V02_PROTECTED_BOW_GOLD_WHITE_FRILL_4x_QA_ONLY.png'],'api_calls':0,'native_calls':0,'HTTP_calls':0,'central_registry_modified':False,'art_pixels_modified':False,'no_art_pass_claim':True})
print(json.dumps({'run':str(RUN),'request':rec(request),'formal':rec(formal),'prompt':rec(promptpath),'mask':rec(mask),'lock':rec(lock),'handoff':rec(handoff),'fresh179_sha256':h(sol),'api_calls':0,'native_calls':0,'HTTP_calls':0},ensure_ascii=False,indent=2))
