from pathlib import Path
import hashlib,json,os,shutil
from datetime import datetime,timezone
from PIL import Image
RUN=Path(__file__).parent;B=RUN.parents[3];PROJECT=B.parents[1];LOCAL=RUN.parent/'local_v16_uniform_gray_and_charcoal_iris_api_v05';I=RUN/'inputs'
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
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
now=datetime.now(timezone.utc).isoformat()
refs=[I/'ref1_KNOWN_LOCALV05_6dc87198_FULL_TARGET_EYES_CORRECT_GRAY_RETURN_ALPHA_WRONG.png',I/'ref2_ORIGINAL2333_COMPLETE_UNMASKED_ACTION_GUIDE.png',I/'ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png',I/'ref4_ORIGINAL2333_OWN_ROUND_EYES_ONLY.png']
assert sha(refs[0])==sha(LOCAL/'character_api_original.png')=='6dc87198fd68f1d49b93146d1cdf240122aff750b7caea5c67263934c1197968'
result=load(LOCAL/'result.json');assert result['output_sha256']==sha(refs[0]) and result['elapsed_seconds']==29.399
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''\n\n以图1这个已知保存的局修中间人物为基准，一次连贯重绘整个当前可见人物，透明背景。图1两眼的均匀charcoal已修好，但部分灰返回面被误变成透明/半透明，不能照它的错误alpha直接采用。保图1中性灰短圆润bob身份、自然灰刘海贴颊发、同耳后画右低LEFT双红珠、细mint材料路线、当前合理外甩体量和C走向。图2只原2333动作/衣手/裁切；图3只无打光GRAY颜料；图4只原2333自己的圆眼开度/视线。\n\n本次必须恢复实体灰返回带：首圈上背口应有的灰内/后返回、中段回折和C内弧的灰带，不能因局修透明而消失或透底。画清同一条宽灰发带的前面翻向内/后面、以不透明灰返回接下一圈，再渐细成C；所有这些实体灰面与bob同类无光照GRAY#B6B4B2，用墨线和互遮表现前后。保持现有薄mint沿带边绕行，不能再挖掉gray返回、变成只剩绿色边的空壳，也不能把整卷画实心锥/封口椭圆盘堆。真正圈间空气仍透明；恢复的是发带返回面，不是把每个露空一律填满。不固定洞数、圈数、轴向或像素长度，不增粗缩小整束、不硬拉全尾露出。\n\n保持图1已修好的整块charcoal虹膜，原普通小白点、眼白/眼睑和略不等的圆睁/视线不变，不能重新长黑芯、灰环/月牙或套半睑。原极小中性短闭口、不加笑。图2仅原2333表演：一臂腰后、另一黑长袖斜跨身体向画左低掌，原指形/白袖口角度、白cap两片主要黑叶、白肩frill、红bow金扣、腰后带、长apron/黑裙、屈膝交错腿保留；不复制图2红头发/尖额发/双高卷，不换动作或镜像。\n\n全部灰前面/内后返回/C统一平涂，无独立深灰体积内底、银白高光或渐变；细mint与不透明gray材料分区保持，不变全mint。头颈、帽、肩衣、低珠根和卷发整个人物连贯接合，不局部贴眼/贴卷、不开局部蒙版、不warp或拼部件。源前鞋在1080底边的可见裁断由后续整体摄影恢复，不补画源未见鞋尖、不改手身来露全脚。图1全透明区内的隐藏RGB渐变不是背景或发面，输出只保真实透明人物，无背景、字幕、棋盘格、色卡或独立物件。\n'''
pp=RUN/'prompt_imggen.txt';pp.write_text(prompt,encoding='utf-8')
request={
 'id':'ART-G33-07','run':str(RUN),'operation_kind':'whole_character_redraw','whole_character_one_generation':True,
 'local_repair_parent':str(LOCAL),'mandatory_whole_imggen':True,'mandatory_whole_redraw_after_local_repair':True,
 'refs':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],
 'reference_roles':['Known localv05 fulltarget preserves corrected iris/body/identity/root/mass/mint; gray-return alpha is wrong and requires restoration','Original2333 sole own action/eye-mouth/hands/costume/visibleextent authority, not red identity','PureGRAY pigment only','Original2333 own round eyes aperture/gaze only'],
 'prompt_file':str(pp),'prompt_sha256':sha(pp),'prompt':prompt,
 'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(p) for p in refs],'transparent_background':True},
 'known_local_result':meta(LOCAL/'result.json'),'known_local_raw':meta(LOCAL/'character_api_original.png'),
 'known_API_elapsed_seconds':29.399,'local_result_all_correct':False,
 'remaining_local_defect':'Some upper-back/inner-return/C gray ribbon surfaces are wrongly alpha transparent or semitransparent. Restore actual opaque gray return strips while preserving real air, current width/connection/phase/root and new uniform iris.',
 'source_frame':2333,'source_pts':1245520,'first_scene_frames':[861,862],
 'changed_from_unreturned_future_draft':'Now exact4ref SHA bound to known6dc87198 local. Removed conditional assumption local was fully correct; explicitly restore lost gray opacity; old draft preserved as history. No oldv15/v16 darkcoil or usergloss crop included.',
 'not_unknown_API_retry':True,'historical_unknown_records_unchanged':True,
 'source_canvas_guidance':[624,1072],'known_local_canvas':[960,1648],
 'source_fronttoe_extra_not_certified_photography_pending':True,
 'PREPONLY':True,'submitted':False,'dispatchable_by_artist':False,'root_release_received':False,
 'native_calls_authorized_this_record':0,'planned_native_n_after_future_release':1,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
 'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_size_parameter_exposed':False,
 'fresh_primary_and_Sol_required':True,'whole_imggen_completed':False,'user_accepted':False,'dynamic_validated':False,'prepared_utc':now}
rp=save('request_imggen.json',request)
statuspath=LOCAL/'LOCAL_REPAIR_STATUS.json';old_sha=sha(statuspath);before=load(statuspath)
snapshot=RUN/'PARENT_LOCAL_STATUS_BEFORE_ARTIST_KNOWN_RETURN_UPDATE.json';shutil.copyfile(statuspath,snapshot);assert sha(snapshot)==old_sha
new={**before,'status':'KNOWN_MASKED_API_INTERMEDIATE_IRIS_CORRECT_GRAY_OPACITY_REPAIR_WHOLE_PENDING','planned_local_repair':False,'locally_repaired':True,'local_repair_completed':True,
 'PREPONLY':False,'submitted':True,'API_calls':1,'native_calls':0,'known_result_saved':True,'result_unknown':False,'known_local_raw':str(LOCAL/'character_api_original.png'),'known_local_raw_sha256':sha(refs[0]),'known_API_elapsed_seconds':29.399,
 'requires_whole_imggen':True,'mandatory_whole_imggen':True,'whole_imggen_completed':False,'fresh_primary_and_independent_review_pending':True,'direct_final_selection_allowed':False,
 'pending_whole_run':str(RUN),'pending_whole_request_sha256':sha(rp),
 'artist_observation_only_not_ROOT_PRIMARY':'Own actual fullraw/white/black and new5x coil+alpha/4xeyes: iris uniformcharcoal corrected; upperback/partinner/C return gray alpha wrongly missing. Local remains intermediate and art HOLD; newwhole must restore opaquegray returns without losingthinmint/lowLEFT/phase/body.',
 'artist_observation_recorded_utc':now,'status_before_update_sha256':old_sha,'status_before_update_saved_at':str(snapshot),'central_registry_or_binding_updated_by_artist':False,
 'root_or_Sol_artistic_pass_written_by_artist':False}
assert sha(statuspath)==old_sha
tmp=LOCAL/'LOCAL_REPAIR_STATUS_ARTIST_UPDATE_TEMP.json';tmp.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(tmp,statuspath)
parent=save('PARENT_LOCAL_STATUS_KNOWN_RETURN_AFTER_ARTIST_UPDATE.json',{'path':str(statuspath),'sha256':sha(statuspath),'record':new,'updated_only_as_explicitly_requested_by_parent':True,'no_ROOT_PRIMARY_or_central_review_written':True})
rawim=Image.open(refs[0]).convert('RGBA');samples=[{'xy':list(xy),'RGBA':list(rawim.getpixel(xy))} for xy in [(675,329),(730,424),(805,456),(813,480),(700,350)]]
seen=[*refs,LOCAL/'character_api_original.png',LOCAL/'qa_white.png',LOCAL/'qa_black.png',
 *[RUN/f'PREP_PRIOR_CANDIDATE_6dc87198_LOCALV05_{suffix}.png' for suffix in ['ROOT_RETURN_C_white_5x','ROOT_RETURN_C_black_5x','RETURN_ALPHA_5x','EYES_white_4x','EYES_black_4x']]]
review=save('ARTIST_ACTUAL_LOCAL_RETURN_AND_V17_REFERENCE_REVIEW.json',{
 'id':'ART-G33-07','reviewer':'xhigh_pending_artist own actual tool image views, not ROOT or Sol','recorded_utc':now,
 'actual_viewed':[meta(p) for p in seen],'source_local_raw_sha256':sha(refs[0]),
 'own_observation':'Current uniform charcoal iris has no separate blackcenter/lowergrayring partition at4x. FullWB and5xalpha/coil show upper backmouth and C innerreturn in particular change to white/black background, with noisy partialalpha; not all gray return is lost, some mid opaque strips survive. Preserve corrected iris/mint and actual connected faces, restore lost opaque gray ribbon surfaces; do not fill realair or infer fixed hole count.',
 'alpha_samples_QA_only_not_art_PASS':samples,'old_future_draft_inaccurate_after_actual_return':True,
 'excluded_generation_inputs':['any oldv15/v16 darkcoil crop or fullhead','gloss userdrill','separate geometryboard','G02 aperture'],
 'preserve':['lowLEFTnape root/currentthinmint','normal wholehead relative mass/outwardswing','original2333 round gaze/tinyneutralmouth','sourcehands/bodyclothing and crop'],
 'source_fronttoe_photography_pending':True,'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'user_accepted':False,'dynamic_validated':False})
lock=save('REQUEST_LOCK_PREPONLY.json',{'id':'ART-G33-07','request':meta(rp),'prompt':meta(pp),'refs':[meta(p) for p in refs],
 'provenance':meta(RUN/'INPUT_PROVENANCE_AND_PRIOR_RETURN_DIAGNOSTICS.json'),'artist_actual_review':meta(review),'parent_status_current':meta(statuspath),'parent_status_before':meta(snapshot),'parent_status_after_snapshot':meta(parent),
 'known_API_result':meta(LOCAL/'result.json'),'known_API_root_execution_receipt':meta(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
 'prefix_text':prefix,'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
 'PREPONLY':True,'root_release_received':False,'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
 'mandatory_whole_after_local':True,'fresh_root_Sol_after_future_return_required':True})
print(json.dumps({'request':meta(rp),'prompt':meta(pp),'lock':meta(lock),'parent_status':meta(statuspath),'parent_before':meta(snapshot),'review':meta(review),'alpha_samples':samples},ensure_ascii=False,indent=2))
