from pathlib import Path
from PIL import Image
import json,hashlib,shutil,datetime

P=Path(__file__).resolve().parent
B=P.parents[3];PROJECT=P.parents[5];CEL=P.parent
LOCAL=CEL/'local_route_frontshoulder_from_known_wholev06_api_v01'
PRIOR=CEL/'whole_imggen_source2365_no_wrong_root_bodycrop_frontshoulder_v07'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
(P/'inputs').mkdir(exist_ok=True)
assert not (P/'request_imggen.json').exists()
oldrefs=load(PRIOR/'INPUT_PROVENANCE_PREPONLY.json')['reference_records']
refs=[]
for index in [0,1,2,3]:
 old=oldrefs[index]
 if index!=1:
  dest=P/'inputs'/Path(old['path']).name;shutil.copyfile(old['path'],dest)
  assert sha(dest)==old['sha256']
  refs.append({**old,'path':str(dest),'source_path':old['path'],'source_sha256':old['sha256']})
 else:
  rawpath=LOCAL/'character_api_original.png';assert sha(rawpath)=='84a7c984ce4d437d37a7b55bf6da1ac9fa42afa2b3d1daf68793227b57497a6a'
  raw=Image.open(rawpath).convert('RGBA');assert raw.size==(960,1648)
  roi=(140,580,880,1610);crop=raw.crop(roi)
  dest=P/'inputs/ref2_KNOWN_LOCAL84a7_BODY_ONLY_BELOW580_NO_SHOULDER_NECK_ROOT_COIL.png';crop.save(dest)
  refs.append(dict(tool_order=2,path=str(dest),sha256=sha(dest),dimensions=crop.size,source_path=str(rawpath),source_sha256=sha(rawpath),source_dimensions=raw.size,crop_xyxy=roi,operation='readonly_plain_rectangle_original_pixels_no_paint',role='Only lower X/waistback arms/cuffs/bow/tails/skirt/legs/shoes clothing detail. Entire shoulder/neck/head/root/coil excluded. Ref1 sole all body action/proportions/output framing; crop top not output cut.'))
  for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
   out=P/f'PREP_INPUT_LOCAL84a7_BODY580_ONLY_{name}.png';Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB').save(out)
defaults=load(PROJECT/'image_defaults.json');prefix=defaults['generation_prompt_prefix']['text'];assert defaults['generation_prompt_prefix']['enabled']
prompt=prefix+'''\n\n图1原PV2365独占本稿动作、背3/4身体与向画右转头、头身比例、手衣裙腿鞋和完整裁切。整个人物一次连贯重绘成图3中性灰短圆润bob女孩，白maidcap和两片主要黑叶按当前头向投影；图3只给上帽/bob身份，不给根、卷或姿势。保原有脸部边缘；本源没有可读眼口，不添加正脸、眼或笑嘴。原红尖发/双高卷不是目标身份。\n\n当前人物LEFT低耳后根在远侧，根与双红珠全部由远侧bob和颈肩自然遮住。肩遮住发束的中段，只有同侧肩FRONT的画右前颈/胸侧外沿露出少量、但有正常发束宽度厚度的灰带返回。露出的部分属于同一束有固有发量的卷，不是小挂件；可以不见完整C。画面可见的黑背领、白X及近侧泡袖前保持清楚无遮挡，没有灰卷横带。保原bob/肩的形状大小，不掀发、不扩肩、不抬根、不镜像、不另长第二束。\n\n可见宽GRAY前面连续翻回不透明gray内/后返回、接下一转并渐细，mint仅薄的muted材料条带。图4定所有bob/卷灰面同一无光照灰#B6B4B2，线与互遮表达返回，实体gray不挖空、真实空气透明；不画封口盘堆、实心锥或深暗体积/银光/渐变。合理整头发量保持，被遮挡不等于缩小整束，不强露尾或固定孔、圈、轴。\n\n图2只有局修人物y580以下原像素衣身，参考下部白X、腰后双臂手袖、白腰结各尾带、裙腿和两只完整鞋的细节；没有头颈、肩或卷，不拥有构图，裁边不是输出断线。全身严格保图1自己肩褶/黑领/泡袖、X交叉、不同双臂手位、裙摆方向和双腿鞋，不加隐藏肢体。完整头颈帽肩卷衣手裙腿一次连画统一接合，无拼贴/warp，只输出真实透明人物；输入alpha0隐藏RGB不画为背景。此为失败局修后的mandatory whole新候选，必须新看新审，不继承旧通过。\n'''
(P/'prompt_imggen.txt').write_text(prompt,encoding='utf-8')
before=LOCAL/'LOCAL_REPAIR_STATUS.json';shutil.copyfile(before,P/'PARENT_LOCAL_STATUS_BEFORE_ACTIVE_PREP_POINTER_UPDATE.json')
status=load(before);status['whole_redraw_preparation']=str(P);status['superseded_whole_preponly_draft']=str(PRIOR);dump(before,status);shutil.copyfile(before,P/'PARENT_LOCAL_STATUS_KNOWN_FAILURE_MANDATORY_PENDING_SNAPSHOT.json')
shutil.copyfile(PRIOR/'ARTIST_KNOWN_LOCAL_INTERMEDIATE_FAILURE_READBACK.json',P/'ARTIST_KNOWN_LOCAL_INTERMEDIATE_FAILURE_READBACK.json')
provenance=dict(id='ART-G33-15',source_frame=2365,source_pts=1262592,first_case_frames=[889,891],reference_records=refs,changed_hypothesis='Discard current whole head/neck/grayS and front-facing fullcoil reference pixels. Original fullsource owns current turn; previous14 uppercap/bob only identity; local rectangle restricted belowy580; short positive far-root/bob/shoulder occlusion route.',prior_prep_preserved=dict(run=str(PRIOR),request=rec(PRIOR/'request_imggen.json'),lock=rec(PRIOR/'REQUEST_LOCK_PREPONLY.json')),prior_prep_never_called=True,current_local_failure=rec(P/'ARTIST_KNOWN_LOCAL_INTERMEDIATE_FAILURE_READBACK.json'),local_repair_parent=str(LOCAL),all_drawing_refs_exclude_wrong_generated_root_neck_coil=True,body_crop_xyxy=[140,580,880,1610],source_image=str(LOCAL/'character_api_original.png'),source_sha256=sha(LOCAL/'character_api_original.png'),prepared_before_future_return=True,art_pixels_modified=False,PREPONLY=True,api_calls=0,native_calls=0,HTTP_calls=0)
dump(P/'INPUT_PROVENANCE_PREPONLY.json',provenance)
request=dict(id='ART-G33-15',run=str(P),operation_kind='whole_character_redraw',whole_character_one_generation=True,PREPONLY=True,dispatchable=False,root_release_received=False,transparent_background=True,refs=[r['path'] for r in refs],reference_sha256=[r['sha256'] for r in refs],reference_roles_in_tool_order=[r['role'] for r in refs],prompt_file=str(P/'prompt_imggen.txt'),prompt_sha256=sha(P/'prompt_imggen.txt'),prompt=prompt,tool_arguments=dict(prompt=prompt,referenced_image_paths=[r['path'] for r in refs],transparent_background=True),source_frame=2365,source_pts=1262592,source_canvas_guidance=[624,1072],first_case_frames=[889,891],local_repair_parent=str(LOCAL),local_repair_parent_raw=rec(LOCAL/'character_api_original.png'),local_intermediate_failed=True,mandatory_whole_character_redraw=True,mandatory_whole_redraw_after_local_repair=True,whole_character_redraw_completed=False,local_status_snapshot=rec(P/'PARENT_LOCAL_STATUS_KNOWN_FAILURE_MANDATORY_PENDING_SNAPSHOT.json'),source_first=True,wrong_current_generated_head_neck_coil_excluded=True,body_crop_xyxy=[140,580,880,1610],far_LEFT_low_root_and_beads_fully_occluded=True,front_shoulder_fragment_required=True,full_C_required=False,visible_backcollar_X_nearpuff_not_crossed_by_hair=True,fresh_root_Sol_and_photography_review_required=True,no_old_pass_inherited=True,supersedes_unexecuted_prep=provenance['prior_prep_preserved'],native_calls_authorized=0,planned_native_n_on_future_release=1,native_calls=0,API_calls=0,HTTP_calls=0,automatic_retries=0,user_quality_preference='high',native_quality_parameter_exposed=False,native_size_parameter_exposed=False,native_model_parameter_exposed=False,new_generated_art_exists=False,user_accepted=False,dynamic_tested=False,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'request_imggen.json',request)
print(json.dumps(dict(run=str(P),request=rec(P/'request_imggen.json'),prompt=rec(P/'prompt_imggen.txt'),refs=refs,body_white=rec(P/'PREP_INPUT_LOCAL84a7_BODY580_ONLY_white.png'),body_black=rec(P/'PREP_INPUT_LOCAL84a7_BODY580_ONLY_black.png')),ensure_ascii=False))
