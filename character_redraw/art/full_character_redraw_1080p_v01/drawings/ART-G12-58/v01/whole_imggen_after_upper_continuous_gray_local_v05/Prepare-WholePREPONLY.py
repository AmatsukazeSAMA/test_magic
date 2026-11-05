from pathlib import Path
from PIL import Image
from datetime import datetime, timezone
import hashlib, json, shutil

RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
LOCAL=CEL/'local_source1071_upper_continuous_gray_returns_api_v04'
FUTURE=LOCAL/'future_mandatory_whole_PREPONLY'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p)
    x={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im: x.update(dimensions=list(im.size),mode=im.mode)
    return x
def dump(p,x):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

assert not (RUN/'request_imggen.json').exists()
(RUN/'inputs').mkdir(exist_ok=True)
(RUN/'diagnostics').mkdir(exist_ok=True)
template=json.loads((FUTURE/'TEMPLATE_GATES_ONLY.json').read_text(encoding='utf-8-sig'))
refs=[]
target=LOCAL/'character_api_original.png'
assert sha(target)=='f252366811e52e4b1a61b140cc761d6accc4337915582d9a884449412cc4adbd'
source_specs=[(target,'ref1_KNOWN_LOCAL_f2523668_COMPLETE_RGBA_TARGET.png',sha(target),'Complete known local intermediate, OC graybob/cap2MAINleaves/lowfarLEFTbeads/body/current compactrecovery broadGRAYfront-return and real foregroundhand/frill occlusion. Not final adopted art.')]
for item,name in zip(template['planned_references_only'][1:],[
    'ref2_SOURCE1071_OWN_FACE_EYES_OPEN_SMILE_NO_HIGH_REDCOIL.png',
    'ref3_SOURCE1071_OWN_BOTH_HANDS_CUFFS_NO_REDHAIR_v02.png',
    'ref4_SOURCE1071_OWN_CLOTH_TORSO_WAIST_NO_HIGH_REDCOIL.png',
    'ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png']):
    source_specs.append((Path(item['path']),name,item['sha256'],item['role']))
for source,name,expected,role in source_specs:
    assert sha(source)==expected,str(source)
    dest=RUN/'inputs'/name
    assert not dest.exists()
    shutil.copyfile(source,dest)
    assert sha(dest)==expected
    refs.append({**rec(dest),'source_image':str(source),'source_sha256':expected,'role':role,'copied_without_pixel_change':True})

im=Image.open(target).convert('RGBA')
assert im.size==(1104,1440)
diag=[]
roi=[595,410,805,680]
for bg,color in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
    composite=Image.alpha_composite(Image.new('RGBA',im.size,color),im).convert('RGB')
    for scale in [1,3]:
        out=RUN/'diagnostics'/f'PREP_PRIOR_LOCAL_f2523668_ROOT_COIL_OCCLUSION_{bg}_{scale}x.png'
        crop=composite.crop(roi)
        if scale!=1: crop=crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST)
        crop.save(out)
        diag.append({**rec(out),'source_image':str(target),'source_sha256':sha(target),'crop_xyxy':roi,'scale':scale,'background':bg,'QA_only_no_art_edit':True,'prepared_before_future_return':True,'not_future_whole_output':True})

prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''图1是本1071已知局修返图，作为完整人物目标，把整个当前可见人物一次连贯重绘，统一头颈帽肩、卷与衣手接合。保中性灰短圆润bob身份、画右人物LEFT远侧低耳后红双珠及自然遮挡、完整白maidcap两片MAIN黑叶、暖桃肤。保当前原眼开度和视线、开口笑：两虹膜各一块均匀charcoal加普通白点，不添黑芯灰环，不套别帧半睑。保高手拇指食指相接OK空孔与另三指、另一低垂手的指形、双袖袖口与交叠、红结金扣、白肩褶、腰后结/围裙和真实半身底裁，不补隐藏腿鞋。

保持图1本帧中等体量的紧凑回收卷和原低根：从低画右入口，宽GRAY前面连续翻回不透明同GRAY返回、再接下一转，顺自然路径渐细；下段仍由当前低手与肩白褶真实遮挡，不为露全C拉到前面，也不把卷缩成小挂件。上段入口出口和下一转连成同一发带，不拆成独立盖、豆块、封口碗盘或实心锥。根不上抬、不换近耳，不把55向外上摆方向套入本58。

图2仅本1071脸眼开度/视线/开口笑；图3仅完整两手、OK接点与袖口；图4仅本衣身腰围裙和实际可见底裁。它们是原片矩形裁图，无原高红卷，残留红额发不作身份；裁边不作输出断线，不独立拉伸或拼贴。完整cap与两MAIN叶由图1保持，不能因源裁缺帽而漏掉。

图5只定纯无光照GRAY #B6B4B2，bob和卷全部前面、内后返回同灰平涂，mint #B0C8BA只窄材料边，不画大绿面、深灰体积底、银亮或渐变。实体灰返回保持不透明，实际空气透明，不强制孔数/圈数或完整尾。只输出当前完整可见人物的真实透明层，忽略图1alpha0隐藏RGB，不画背景、字幕或色卡。'''
prompt_path=RUN/'prompt_imggen.txt'
prompt_path.write_text(prompt+'\n',encoding='utf-8')
prompt=prompt_path.read_text(encoding='utf-8')
assert prompt.startswith(prefix)
result=json.loads((LOCAL/'result.json').read_text(encoding='utf-8-sig'))
assert result['output_sha256']==sha(target) and result['n']==1
status_path=LOCAL/'LOCAL_REPAIR_STATUS.json'
before_hash=sha(status_path)
shutil.copyfile(status_path,RUN/'LOCAL_REPAIR_STATUS_BEFORE_V05_PREP.json')
assert sha(status_path)==before_hash,'concurrent local status update'
status_path.write_text(json.dumps({
    'id':'ART-G12-58','status':'known_saved_local_intermediate_mandatory_whole_pending',
    'PREPONLY':False,'submitted':True,'locally_repaired':True,'local_repair_completed':True,
    'intermediate_only':True,'result_unknown':False,'known_raw':rec(target),
    'result_metadata':rec(LOCAL/'result.json'),'root_execution_receipt':rec(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
    'API_calls':1,'executed_by':'root','quality':'high','elapsed_seconds_provider':result['elapsed_seconds'],
    'requires_whole_imggen':True,'mandatory_whole_imggen':True,'mandatory_whole_pending':True,
    'whole_imggen_completed':False,'fresh_primary_and_independent_review_pending':True,
    'direct_final_selection_allowed':False,'native_calls':0,'automatic_retries':0,
    'previous_status_snapshot':rec(RUN/'LOCAL_REPAIR_STATUS_BEFORE_V05_PREP.json'),
    'next_whole_PREP':str(RUN/'request_imggen.json'),'artist_observation_not_ROOT_review':True,
    'static_pass':False,'dynamic_validated':False,'user_accepted':False,
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
request={
    'id':'ART-G12-58','run':str(RUN),'PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'operation_kind':'whole_character_redraw','transparent_background':True,'whole_character_one_generation':True,
    'existing_saved_API_repair_not_new_FIRST':True,
    'refs':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],
    'reference_roles_in_tool_order':[x['role'] for x in refs],
    'prompt_file':str(prompt_path),'prompt_sha256':sha(prompt_path),'prompt':prompt,
    'tool_arguments':{'prompt':prompt,'referenced_image_paths':[x['path'] for x in refs],'transparent_background':True},
    'local_repair_parent':str(LOCAL),'local_repair_parent_raw_sha256':sha(target),
    'known_local_intermediate_not_final':True,'mandatory_whole_after_local_repair':True,
    'mandatory_whole_pending':True,'new_whole_completed':False,
    'source_frame':1071,'source_pts':571776,'first_case_frames':[1071,1074],
    'full_red_high_coil_guide_excluded_from_tool_refs':True,
    'changed_reference_hypothesis':'Use fresh known continuous local as full target; own source1071 face/openmouth, both complete hands/cuffs v02, clothwaist original rectangles only. No highredcoil sourcefull, no old rejected58 uppercap as anchor, no copied55 upturn phase. Preserve compactrecovery and hand/frill occlusion; unify wholeflatgray.',
    'native_calls_authorized':0,'planned_native_calls_on_future_specific_release':1,'native_calls':0,
    'API_calls_by_artist_this_prep':0,'HTTP_calls_by_artist_this_prep':0,'automatic_retries':0,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,
    'native_model_parameter_exposed':False,'native_size_parameter_exposed':False,
    'fresh_root_and_Sol_required':True,'fresh_photography_required':True,
    'user_accepted':False,'dynamic_tested':False,'created_utc':datetime.now(timezone.utc).isoformat(),
}
dump(RUN/'request_imggen.json',request)
dump(RUN/'INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G12-58','refs':refs,'source_crop_provenance':template['source_crop_provenance'],
    'diagnostics':diag,'source_full1071':rec(BASE/'coverage/source_frames/F001071.png'),
    'source_original_guide':rec(CEL/'inputs/source_pose_guide.png'),
    'known_result':rec(LOCAL/'result.json'),'root_execution_receipt':rec(LOCAL/'ROOT_API_EXECUTION_RECEIPT.json'),
    'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'no_art_pixels_painted_or_pasted':True,
})
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{
    'id':'ART-G12-58','PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(prompt_path),'refs':refs,
    'source_provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),
    'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
})
print(json.dumps({'request':rec(RUN/'request_imggen.json'),'prompt':rec(prompt_path),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json')},ensure_ascii=False,indent=2))
