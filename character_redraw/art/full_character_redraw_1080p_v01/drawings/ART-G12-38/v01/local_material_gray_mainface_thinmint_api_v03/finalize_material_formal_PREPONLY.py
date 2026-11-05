from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
from PIL import Image
RUN=Path(__file__).parent;B=RUN.parents[3];PROJECT=B.parents[1];PRIOR=RUN.parent/'whole_imggen_source963_connectedgray_occlusion_v02';I=RUN/'inputs'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def meta(p):
 p=Path(p);r={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:r.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return r
def save(name,o):
 p=RUN/name
 if p.exists():raise RuntimeError('preserve '+str(p))
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
refs=[I/'ref1_CURRENT38_V02_47856091_COMPLETE_RGBA_TARGET.png',I/'ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2.png']
assert sha(refs[0])=='4785609114b9b57113db98decde0f12909d077b79faf09799221db6ad61c7aa5'
mask=RUN/'mask_WRONG_MINT_UPPER_WIDE_AND_FULL_C_INTERIORS_KEEP_THINMINT_RIMS_v02.png'
assert Image.open(mask).size==Image.open(refs[0]).size==(1126,1397)
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''\n\n图1是已知保存的当前963整个人物，只修蒙版透明开放的发带材料内区，输出完整透明人物。上第一宽前面、下大C及其末端宽面现在误涂成mintgreen主面，改为图2的无打光GRAY#B6B4B2，与bob和当前合格中央灰面同类灰颜料；薄mint只沿发带窄边连贯绕行，不再占宽主面。图2只有GRAY颜色，不提供新卷形。\n\n蒙版只开错误宽绿面内部，原窄mint条和主面保留的细mint边、墨线/轮廓、中央正确灰前面与不透明内后返回、真正空气/alpha边界均保护。保持同一条宽发带的前面翻入实际返回、接下一圈、渐细C路径和整头相对体量；灰返回是实体，不能挖空气，不能封成盘堆/实心锥、缩成挂件或变巨粗。固定当前画右远侧同耳后低LEFT双珠根、bob自然遮挡和肩frill关系，不换边/抬根，不强露隐藏段。无渐变、深灰体积暗底、银白高光。\n\n其余当前原963左倾头、双眼不等圆睁/原视线、单弧闭口笑、画右两只不同张掌和拇指/指缝、双斜袖口/交叉黑袖、红bow金扣、白肩frill/腰后带/围裙与半身底裁全部保持。眼睛不重画成半睑或改眼色，不增帽叶，不补画外腿鞋，不改body动作。透明区保持透明，不把A0隐藏RGB画成背景。只改已开材料内区，不贴部件；这是局修中间稿，须再完整人物builtin重绘和新root/Sol评审才可考虑入库。\n'''
pp=RUN/'prompt_api.txt';pp.write_text(prompt,encoding='utf-8')
formal=save('API_PREPARED_REQUEST.json',{'InputImages':[str(p) for p in refs],'PromptFile':str(pp),'MaskFile':str(mask),'OutputDirectory':str(RUN),'OutputFileName':'character_api_original.png','Size':'1120x1392','Quality':'high','Background':'transparent'})
sol=B/'review/sol_xhigh_round170.json';assert load(sol)['entries'][0]['image_sha256']==sha(refs[0])
receipt=load(PRIOR/'NATIVE_CALL_RECEIPT.json');assert receipt['known_result_saved'] and not receipt['result_unknown']
before=save('KNOWN_TARGET_SOURCE_AND_STATUS_BEFORE.json',{
 'target':meta(refs[0]),'known_native_receipt':meta(PRIOR/'NATIVE_CALL_RECEIPT.json'),'known_native_receipt_data':receipt,'BUILTIN':meta(PRIOR/'BUILTIN_GENERATION.json'),
 'known_FIRST_result':meta(RUN.parent/'result.json'),'known_FIRST_original':meta(RUN.parent/'character_api_original.png'),'FIRST_elapsed_seconds':load(RUN.parent/'result.json')['elapsed_seconds'],
 'source_JOB':meta(RUN.parent/'JOB.json'),'source_frame':963,'source_pts':514112,'first_exposure_frames':[962,965],
 'source_canonical':meta(Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-38/source.png')),
 'PRIMARY_before':meta(PRIOR/'PRIMARY_GOAL_REVIEW.json'),'PRIMARY_snapshot':load(PRIOR/'PRIMARY_GOAL_REVIEW.json'),
 'fresh170':meta(sol),'local_repair_parent_before':None,'no_known_unknown_target':True,'this_is_new_material_repair_not_UNKNOWN_retry':True,'no_history_or_status_modified':True})
status=save('LOCAL_REPAIR_STATUS.json',{'id':'ART-G12-38','status':'PREPONLY_PENDING_ROOT_RELEASE_AND_KNOWN_API_RETURN','operation_kind':'local_mask_repair','planned_local_repair':True,'locally_repaired':False,'local_repair_completed':False,'requires_whole_imggen':True,'mandatory_whole_imggen':True,'whole_imggen_completed':False,'fresh_root_Sol_required':True,'direct_final_selection_allowed':False,'future_local_parent':str(RUN),'PREPONLY':True,'submitted':False,'API_calls':0,'native_calls':0,'automatic_retries':0})
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
provider=PROJECT/'scripts/Invoke-ReferenceImage.ps1';config=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json');assert load(config)['model']=='gpt-image-2.5-sunburst'
scope=save('PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json',{'id':'ART-G12-38','authorization':meta(auth),'question_id':load(auth)['question_call_id'],'user_reply_verbatim':load(auth)['user_reply_verbatim'],
 'scope':'Same GOAL known character material repair, current project art+puregray and necessary same-size mask only to configured official images/edits.',
 'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','n':1,'retry':0,'quality':'high','background':'transparent','output_size':[1120,1392],'input_mask_size':[1126,1397],
 'output_size_note':'Conservative nearby16px multiples; only complete-image fit, no part transform or claim about unverified model hard limits.',
 'refs':[meta(p) for p in refs],'mask':meta(mask),'formal':meta(formal),'PREPONLY':True,'root_specific_execution_release_pending':True,'API_calls':0,'native_calls':0,'HTTP_calls':0})
seen=[*refs,PRIOR/'qa_white.png',PRIOR/'qa_black.png',
 B/'review/sol_xhigh_round170_diagnostics/CURRENT_ROOT_RETURN_C_white_3x.png',B/'review/sol_xhigh_round170_diagnostics/CURRENT_ROOT_RETURN_C_black_3x.png',
 B/'review/sol_xhigh_round170_diagnostics/CURRENT_EYES_MOUTH_white_3x.png',B/'review/sol_xhigh_round170_diagnostics/CURRENT_PALMS_CUFFS_white_2x.png',
 Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-38/source.png'),I/'SOURCE963_COMPLETE_UNMASKED_GUIDE_FUTURE_WHOLE_NOT_API_REF.png',
 RUN/'PREP_PRIOR_CANDIDATE_47856091_COIL_MATERIAL_COORDINATE_GRID_8x.png',
 *[RUN/f'PREP_PRIOR_CANDIDATE_47856091_MATERIAL_MASKv02_{s}.png' for s in ['OVERLAY_FULL_1x','OVERLAY_COIL_5x','ALPHA_COIL_5x']]]
actual=save('ACTUAL_VIEWED_CURRENT_SOURCE_REFS_AND_MASK.json',{'reviewer':'xhigh_pending_artist own actual tool image views','recorded_utc':datetime.now(timezone.utc).isoformat(),'actual_viewed':[meta(p) for p in seen],'all_prior_candidate_diagnostics_prepared_before_future_return':True,'future_API_or_whole_return_exists':False})
review=save('ARTIST_MATERIAL_MASK_REVIEW_PREPONLY.json',{'id':'ART-G12-38','target_sha256':sha(refs[0]),'fresh170':meta(sol),'actual_viewed_record':meta(actual),
 'observations':['Actual currentraw/fullwhiteblack/new170 coil3x confirm upper first wideface and lowerlargeC are mint-dominant mainfaces; central broadgray face already good. This is material P1, not a new geometry/mass/root verdict.',
 'Actual source963 full/guide and current3x eye/palms show unequal round open eyes, singleclosedarc smile, left headtilt, two different high right-side palms, crossed sleeve/diagonal cuffs and original halfbody bottomcut preserved.',
 'Finalmaskv02 covers erroneous green upperface, lowerC and separately visible green terminal wideface, retains2px material rim and existing narrowmint bands. v01 missing small Cterminal face kept as prep history; v02 adds127 actual material pixels.',
 'LowLEFT root/viewerRIGHTfar nape/beads/bob occlusion, opaque grayreturn, air/ink and hands/costume/cap/face all protected; no finalart codepaint.'],
 'final_mask':meta(mask),'final_mask_provenance':meta(RUN/'MASK_PROVENANCE_v02.json'),'A0_pixels':2254,'API_refs_count':2,
 'reference_hypothesis':'Current coherent complete target plus pureGRAY pigment only; remove gloss/detail/old colored coil crop shape anchors. Test restricted material correction, not a proven cause of earlier failure.',
 'mandatory_future_builtin_whole':True,'future_whole_must_not_read_old_mint_C_crop':True,
 'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'art_PASS':False,'user_accepted':False,'dynamic_validated':False})
future=RUN/'future_mandatory_whole_PREPONLY';future.mkdir(exist_ok=True)
newlocal=RUN/'character_api_original.png';source=I/'SOURCE963_COMPLETE_UNMASKED_GUIDE_FUTURE_WHOLE_NOT_API_REF.png';fr=[str(newlocal),str(source),str(refs[1])]
wp=prefix+'''\n\n以图1本次已正确回灰的局修完整人物为唯一身份/卷几何主目标，一次连贯重绘全部可见人物，透明背景。保持新回灰的第一宽面、中央宽面、内/后返回、下C及末端都是bob同类无打光灰，薄mint只沿窄边连续绕行；图3只GRAY颜料。不可重新输入或复刻旧mint大C/宽绿主面，不能把返回挖空、变封口盘堆、增粗缩小或改当前根与折返/C走向。\n\n图2原963完整guide仅控制本帧左倾头、自己的不等圆睁/视线和单弧闭口笑、两只不同高手/拇指分指、双斜袖口与交叉黑袖、原白肩frill/红bow金扣/腰后带/围裙及半身底裁。保持图1中性灰短圆润bob/自然灰刘海和贴颊短发、画右远侧同耳后低LEFT双红珠，帽两主要黑叶、暖桃肤与单实色charcoal iris/普通白点不变；不复制原红发/尖额发/高双卷，源画外腿鞋不补。\n\n完整人物统一头颈帽肩、衣袖与发卷连接，不局部贴卷/贴眼，不warp或拼部件。保原灰实体/真实透明空气及细mint分区，无渐变/独立深灰内底/银亮高光，无背景字幕色卡。\n'''
fp=future/'prompt_imggen_DRAFT.txt';fp.write_text(wp,encoding='utf-8')
whole=save('future_mandatory_whole_PREPONLY/request_imggen_DRAFT.json',{'id':'ART-G12-38','operation_kind':'whole_character_redraw','local_repair_parent':str(RUN),'mandatory_whole_imggen':True,'requires_fresh_root_Sol':True,
 'prompt_file':str(fp),'prompt_sha256':sha(fp),'prompt':wp,'refs_expected_after_future_return':fr,'reference_sha256':[None,sha(source),sha(refs[1])],
 'tool_arguments_template':{'prompt':wp,'referenced_image_paths':fr,'transparent_background':True},
 'missing_input':{'path':str(newlocal),'must_have_known_result_and_exact_new_SHA':True,'must_actual_view_new_local_whiteblack_before_dispatch':True},
 'no_old_mint_C_geometry_crop_or_gloss_detail_allowed':True,'PREPONLY':True,'dispatchable':False,'native_calls_authorized':0,'API_calls':0,'native_calls':0,'automatic_retries':0,'native_quality_parameter_exposed':False,'user_quality_preference':'high'})
lock=save('REQUEST_LOCK_PREPONLY.json',{'id':'ART-G12-38','formal':meta(formal),'prompt':meta(pp),'mask':meta(mask),'mask_provenance':meta(RUN/'MASK_PROVENANCE_v02.json'),'refs':[meta(p) for p in refs],
 'provenance':meta(RUN/'INPUT_PROVENANCE_PREPONLY.json'),'review':meta(review),'actual_view_list':meta(actual),'history':meta(before),'scope':meta(scope),'auth':meta(auth),'provider':meta(provider),'provider_configuration':meta(config),'Sol170':meta(sol),'local_repair_status':meta(status),'future_whole_draft':meta(whole),
 'prefix_text':prefix,'prefix_text_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'formal_field_count_including_MaskFile':8,'n':1,'retry':0,'PREPONLY':True,'dispatchable':False,'execution_released':False,'API_calls':0,'native_calls':0,'mandatory_future_builtin_whole':True})
print(json.dumps({'formal':meta(formal),'prompt':meta(pp),'mask':meta(mask),'lock':meta(lock),'future_whole':meta(whole),'future_whole_prompt':meta(fp),'Sol170':meta(sol)},ensure_ascii=False,indent=2))
