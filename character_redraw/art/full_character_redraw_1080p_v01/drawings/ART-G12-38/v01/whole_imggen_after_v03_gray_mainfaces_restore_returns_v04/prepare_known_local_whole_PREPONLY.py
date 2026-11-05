from pathlib import Path
import hashlib,json,shutil,os
from datetime import datetime,timezone
from PIL import Image
RUN=Path(__file__).parent;B=RUN.parents[3];PROJECT=B.parents[1];LOCAL=RUN.parent/'local_material_gray_mainface_thinmint_api_v03';I=RUN/'inputs';I.mkdir(parents=True,exist_ok=True)
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
def cp(src,name):
 dst=I/name
 if dst.exists():raise RuntimeError('preserve '+str(dst))
 shutil.copyfile(src,dst);assert sha(src)==sha(dst);return dst
now=datetime.now(timezone.utc).isoformat();result=load(LOCAL/'result.json');raw=LOCAL/'character_api_original.png'
assert sha(raw)==result['output_sha256']=='f74f8e217f8e3b891d7a72c5f4f55c087d3f4148d30bb2f3f3af228c7eb38de8'
assert result['elapsed_seconds']==33.699 and result['n']==1 and result['response_size']=='1120x1392'
refs=[cp(raw,'ref1_KNOWN_LOCALV03_f74f8e21_COMPLETE_TARGET_GRAY_MAINFACES_RETURNS_PENDING.png'),
 cp(LOCAL/'inputs/SOURCE963_COMPLETE_UNMASKED_GUIDE_FUTURE_WHOLE_NOT_API_REF.png','ref2_ORIGINAL963_COMPLETE_UNMASKED_ACTION_GUIDE.png'),
 cp(LOCAL/'inputs/ref2_PURE_UNLIT_GRAY_ONLY_B6B4B2.png','ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png')]
roles=['Known localv03 complete identity/body/lowLEFT/mass target, broadfaces nowgray but narrowreturns/turnback width not accepted; whole must unify real opaque returns rather than trace thin strands.',
 'Original963 sole own leftheadtilt/unequal roundeyes/singlearcclosedsmile/two separate frontoblique-backvertical highpalms/crossedsleeves/clothes/bottomcut authority; redhair highdoublecoil not identity.',
 'Pure gray pigment only no geometry/spatial partition. Thinmint belongs to existing edge routing, no new widegreen reference.']
diag=[]
for bg in ['white','black']:
 src=LOCAL/f'qa_{bg}.png'
 for tag,xy,scale in [('ROOT_RETURN_C',[520,365,700,625],5),('EYES_MOUTH',[245,300,545,490],3)]:
  q=RUN/f'PREP_PRIOR_CANDIDATE_f74f8e21_LOCALV03_{tag}_{bg}_{scale}x.png'
  with Image.open(src) as im:t=im.crop(tuple(xy));t.resize((t.width*scale,t.height*scale),Image.Resampling.NEAREST).save(q)
  diag.append({'file':meta(q),'source_image':str(src),'source_sha256':sha(src),'raw_source_image':str(raw),'raw_source_sha256':sha(raw),'crop_xyxy':xy,'scale':scale,'prepared_before_future_return':True,'not_future_whole_v04_evidence':True})
q=RUN/'PREP_PRIOR_CANDIDATE_f74f8e21_LOCALV03_RETURN_ALPHA_5x.png'
with Image.open(raw) as im:t=im.getchannel('A').crop((520,365,700,625));t.resize((t.width*5,t.height*5),Image.Resampling.NEAREST).save(q)
diag.append({'file':meta(q),'source_image':str(raw),'source_sha256':sha(raw),'crop_xyxy':[520,365,700,625],'scale':5,'channel':'A','prepared_before_future_return':True,'not_future_whole_v04_evidence':True})
prov=save('INPUT_PROVENANCE_AND_PRIOR_RETURN_DIAGNOSTICS.json',{
 'id':'ART-G12-38','known_local_result':meta(LOCAL/'result.json'),'known_raw':meta(raw),'known_execution_receipt':meta(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
 'reference_records':[{'number':n,'file':meta(p),'role':role,'operation':'byte_identical_copy_no_art_edit'} for n,(p,role) in enumerate(zip(refs,roles),1)],
 'source_frame':963,'source_pts':514112,'first_scene_frames':[962,965],
 'diagnostics':diag,'old_conditional_future_whole_draft_preserved':meta(LOCAL/'future_mandatory_whole_PREPONLY/request_imggen_DRAFT.json'),
 'excluded_generation_refs':['old478560 wrong mintC/widegreen coil crop','gloss userdetail','other-state fullheadcoil','AIbody','G02 half-lid aperture'],
 'PREPONLY':True,'API_calls':0,'native_calls':0,'HTTP_calls':0,'art_pixel_changes':False,'prepared_utc':now})
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''\n\n以图1已知保存的局修中间人物为基准，一次连贯重绘整个当前可见人物，真实透明背景。图1上第一宽面和下大C的错误mint主面已回灰，但窄返回/回折边可能比原来更纤细，不是全部正确或缩卷已通过的模板。保图1中性灰短圆润bob、自然灰刘海/贴颊发、画右远侧同耳后低LEFT双红珠、当前整头相对合理的固有发量与原动作；图2只本帧原963动作/眼口手衣和裁切，图3只有无打光GRAY颜料。\n\n将可见卷统一成同一条宽GRAY发带：前面自然翻向不透明内/后返回，真实接到下一圈，下转渐细成C及末端。主面与返回均为bob同类无打光GRAY#B6B4B2，细mint仅沿窄材料边连贯绕行，不能把上宽面或大C再涂成宽mint主面。保全束占用和合理体量，不将局修可能变窄的返回继续画成细线绳/小挂件；内后返回是实体灰发带，不是全部挖空或只有绿色线圈围着空气。真正可见圈间空气仍透明，以线和互遮画绕行，不能封成实心锥/椭圆盘堆；不固定洞数、圈数、轴或像素长度，不为证明结构增粗或硬露完整尾。低根不动，bob/原白肩frill/袖的自然遮挡保持，不扩大衣肩盖卷。\n\n原963表演只按图2：头向画左倾，双眼不等圆睁/原视线与单一charcoal实色虹膜、普通小白点保留，单弧闭口笑不改。两只手在画右分开，前手斜起、后手近竖，保各自拇指/分指与掌线、两个斜白袖口、交叉黑长袖和原肘位，不能合成泛用合十或复制相邻动作。白cap两主要黑叶、暖桃肤、红bow金扣、白肩fan/竖frill、围裙腰后带与源半身底裁保持；图2原红发/尖额发/双高卷不是目标，不补画外腿鞋或改躯干凑底。\n\n整个人物统一头颈帽肩、衣袖和发卷连接，不局部贴卷/贴眼、不开局部蒙版、不warp或拼部件。所有gray前/返回/C统一平涂，无独立深灰内底、银白高光或渐变。图1透明像素内的隐藏RGB渐变不是实体背景，不把它描入人物；只输出真实透明当前可见人物，无背景字幕棋盘格色卡。\n'''
pp=RUN/'prompt_imggen.txt';pp.write_text(prompt,encoding='utf-8')
request={
 'id':'ART-G12-38','run':str(RUN),'operation_kind':'whole_character_redraw','whole_character_one_generation':True,
 'local_repair_parent':str(LOCAL),'mandatory_whole_imggen':True,'mandatory_whole_redraw_after_local_repair':True,
 'refs':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],'reference_roles':roles,
 'prompt_file':str(pp),'prompt_sha256':sha(pp),'prompt':prompt,'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(p) for p in refs],'transparent_background':True},
 'known_local_result':meta(LOCAL/'result.json'),'known_local_raw':meta(raw),'known_API_elapsed_seconds':33.699,
 'local_result_all_correct':False,'remaining_width_continuity_concern':'Narrow returns/turnback edges may be thinner after local API. Do not certify geometry/mass from local result. Whole unifies actual wide gray front-to-opaque-return-to-taperC, retains lowLEFT/intrinsic mass/sourceexpression and separated palms.',
 'source_frame':963,'source_pts':514112,'first_scene_frames':[962,965],'source_canvas_guidance':[800,992],'known_local_canvas':[1120,1392],
 'excluded_bad_anchors':['old mintC/widegreen coil crop','gloss detail','another-state coil geometry'],
 'PREPONLY':True,'submitted':False,'dispatchable_by_artist':False,'root_release_received':False,'native_calls_authorized_this_record':0,'planned_one_native_only_after_future_release':True,
 'API_calls':0,'native_calls':0,'HTTP_calls':0,'automatic_retries':0,'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_size_parameter_exposed':False,
 'whole_imggen_completed':False,'fresh_root_and_Sol_required':True,'dynamic_validated':False,'user_accepted':False,'prepared_utc':now}
rp=save('request_imggen.json',request)
statuspath=LOCAL/'LOCAL_REPAIR_STATUS.json';oldsha=sha(statuspath);before=load(statuspath)
sp=RUN/'PARENT_LOCAL_STATUS_BEFORE_ARTIST_KNOWN_RETURN_UPDATE.json';shutil.copyfile(statuspath,sp);assert sha(sp)==oldsha
new={**before,'status':'KNOWN_MASKED_API_INTERMEDIATE_GRAY_MAINFACES_CHANGED_RETURN_WIDTH_PENDING_MANDATORY_WHOLE','planned_local_repair':False,'locally_repaired':True,'local_repair_completed':True,
 'PREPONLY':False,'submitted':True,'API_calls':1,'native_calls':0,'known_result_saved':True,'result_unknown':False,
 'known_local_raw':str(raw),'known_local_raw_sha256':sha(raw),'known_API_elapsed_seconds':33.699,
 'requires_whole_imggen':True,'mandatory_whole_imggen':True,'whole_imggen_completed':False,'fresh_root_Sol_required':True,'direct_final_selection_allowed':False,
 'pending_whole_run':str(RUN),'pending_whole_request_sha256':sha(rp),
 'artist_observation_only_not_ROOT_PRIMARY':'Own actual newraw/WB: upper wrongmint mainface and lowerC visibly changedgray; some narrowturn/return edges look thinner, not a claim local geometry or shrinking passed. Whole must unify coherent visible widegray fronts/opaque returns/taperC while preserving lowLEFT/mass/monoeyes/source963 palms/smile/crossedsleeves.',
 'artist_observation_recorded_utc':now,'status_before_update_sha256':oldsha,'status_before_update_saved_at':str(sp),'central_registry_or_binding_updated_by_artist':False,'ROOT_PRIMARY_or_Sol_written_by_artist':False}
assert sha(statuspath)==oldsha
temp=LOCAL/'LOCAL_REPAIR_STATUS_ARTIST_UPDATE_TEMP.json';temp.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(temp,statuspath)
after=save('PARENT_LOCAL_STATUS_KNOWN_RETURN_AFTER_ARTIST_UPDATE.json',{'source_path':str(statuspath),'source_sha256':sha(statuspath),'record':new,'update_explicitly_requested_by_parent':True,'no_ROOT_or_central_review_written':True})
lock=save('REQUEST_LOCK_PREPONLY.json',{'id':'ART-G12-38','request':meta(rp),'prompt':meta(pp),'refs':[meta(p) for p in refs],'provenance':meta(prov),
 'known_API_result':meta(LOCAL/'result.json'),'known_API_root_execution_receipt':meta(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
 'parent_status_current':meta(statuspath),'parent_status_before':meta(sp),'parent_status_after_snapshot':meta(after),
 'prefix_text':prefix,'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
 'PREPONLY':True,'root_release_received':False,'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'mandatory_whole_after_local':True,'fresh_root_Sol_required_after_future_return':True})
print(json.dumps({'request':meta(rp),'prompt':meta(pp),'lock':meta(lock),'parent_status':meta(statuspath),'qpaths':[d['file'] for d in diag]},ensure_ascii=False,indent=2))
