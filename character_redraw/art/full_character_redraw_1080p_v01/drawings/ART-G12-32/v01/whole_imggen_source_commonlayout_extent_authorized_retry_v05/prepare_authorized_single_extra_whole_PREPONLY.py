from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageChops
import json,hashlib,shutil
R=Path(__file__).resolve().parent;C=R.parent;B=R.parents[3];PROJECT=B.parents[1]
OLD=C/'whole_imggen_source_commonlayout_extent_v04';LOCAL=C/'local_round_drill_v01'
ID='ART-G12-32'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
assert not (R/'request_imggen.json').exists()
I=R/'inputs';I.mkdir(exist_ok=True)
Q=R/'qa_readonly';Q.mkdir(exist_ok=True)
old_inventory=[rec(p) for p in sorted(OLD.rglob('*')) if p.is_file()]
oldrequest=OLD/'request_imggen.json';receipt=OLD/'NATIVE_CALL_RECEIPT.json'
assert sha(oldrequest)=='dbf44b07d47454926a6f82a36f7fafc29477b04d358f5229a8fff69dbe05c9e3'
assert sha(receipt)=='e1959b23bfe598afb59850c7d4ca6ab275ce95b06aea79ae9895f4ed80047890'
assert read(receipt)['remote_processing_result_unknown'] and not read(receipt)['known_unsent_before_HTTP']
recovery=B/'review/G12-32_UNKNOWN_READONLY_RECOVERY_SOL_20261102_v02.json'
assert sha(recovery)=='27c5f0efe6bd416f8b0755d76e1a6a2b39e4d217d3e3ddf3d9cbd7ad1dc2dcdf'
assert read(recovery)['fresh_local_recovery_scan']['candidate_count']==0
job=read(C/'JOB.json');assert job['source_frame']==936 and job['source_pts']==499696
source=Path(job['source_image']);assert sha(source)==job['source_image_sha256']
state=next(x for x in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if x['id']==ID)
assert [state['first_frame'],state['last_frame']]==[933,937]
snapshot=R/'LOCAL_REPAIR_PARENT_STATUS_BEFORE_PREPARATION.json';assert not snapshot.exists()
shutil.copyfile(LOCAL/'LOCAL_REPAIR_STATUS.json',snapshot)
assert sha(snapshot)==sha(LOCAL/'LOCAL_REPAIR_STATUS.json')
waiver=put('USER_EXPLICIT_SINGLE_ADDITIONAL_GENERATION_WAIVER.json',{
 'id':ID,'mother_frame':936,'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'user_explicitly_approved_one_additional_generation':True,
 'reply_verbatim':'允许这一张额外重绘一次',
 'question_text':'G12-32（母帧 F936）上次 imggen 整体重绘因网络中断未留下返图，重新检索本地输出后仍无法恢复。是否允许在新版本中额外提交一次透明人物整体重绘？这里单独确认，是遵照你要求的“结果未知不自动重试”；其他稿件继续进行。',
 'question_id':'call_1444d0931f4e41cb91c73c8f34eb627e',
 'approval_source':'Parent root relayed the actual user answer in this active thread; not inferred from pending dispatch accepted:true.',
 'old_unknown_run':str(OLD),'old_unknown_receipt':rec(receipt),'old_unknown_request':rec(oldrequest),
 'latest_readonly_recovery_report':rec(recovery),
 'old_recovery_scans':[rec(OLD/n) for n in ['NATIVE_RECOVERY_SCAN_CURRENT_DIRECTORY.json','NATIVE_RECOVERY_SCAN_ALL_GENERATED_DIRECTORIES.json']],
 'old_unknown_remote_processing_still_unknown':True,'old_unknown_HOLD_preserved':True,
 'earlier_recovery_report_pending_answer_is_historical_before_this_explicit_answer':True,
 'this_waiver_does_not_change_global_no_unknown_automatic_retry_rule':True,
 'new_target_run':str(R),'operation_kind':'whole_character_redraw','provider':'built-in imagegen',
 'onecall':True,'additional_generation_limit':1,'additional_generation_calls_used':0,'automatic_retries':0,
 'current_parent_task':'PREPONLY; root actual refs/prompt review and a separate execution release still pending.',
 'root_dispatch_release_received_for_v05':False,'API_calls':0,'native_calls':0,
 'quota_controls_not_used':True
})
refs=[]
def cp(name,src,role,expected):
    src=Path(src);assert sha(src)==expected
    out=I/name;assert not out.exists();shutil.copyfile(src,out)
    refs.append({**rec(out),'source':rec(src),'role':role,'byte_identical_readonly_copy':True})
cp('ref1_ORIGINAL936_COMMON704x976_FACE_HANDCONTACT_WAIST_ALL_VISIBLE_APRON.png',
   OLD/'inputs/ref1_ORIGINAL32_COMMON_LAYOUT_FACE_BODY_CONTACTS_FULL_VISIBLE_APRON_NO_OLD_RED_HEAD.png',
   '唯一动作/圆睁tinyO/原头倾、脸—手—腰—下apron/黑裙底裁共同坐标。旧红整头只技术排除、原脸已原位恢复；不能当输出断头/矩形切线，不分别缩放部位。',
   '95b20617ed8c004cb8b7f840a6b602ca72b50a25ec156bd36908bc4fdeb3b362')
cp('ref2_USER_CORRECT11_GRAYBOB_CAP_LOWLEFT_FULL_HEAD_COIL_VOLUME_CONTEXT.png',
   B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png',
   '用户认可correct11完整头部/低LEFT珠/灰短bob与连续前返回收细C的相对头肩体量身份；不复制中性闭口、眼开度、抬臂、颈身比例/固定竖轴或光照。当前圆睁tinyO和手衣底裁仍ref1。',
   '216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528')
cp('ref3_LATEST_USER_BROAD_GRAY_FRONT_OPAQUE_INNER_BACK_RETURN_TAPER_C_DETAIL.png',
   B/'drawings/ART-G12-69/v01/whole_imggen_source1123_uniform_charcoal_iris_v02/inputs/ref5_LATEST_GRAY_FRONT_RETURN_DETAIL_ONLY_PRESERVE_CURRENT_C.png',
   '最新宽gray前→opaque内后返回→下一圈→渐细C，mint仅材料条带；不复制精修银亮、深体积暗底、根位置、衣服、固定轴长/圈孔或isolatedcrop体量。',
   '0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7')
cp('ref4_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png',
   OLD/'inputs/ref3_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png',
   '所有bob/灰卷front-inner-back-return统一无光照gray，mint材料而非光；不让色表重分全卷mint或固定孔数。',
   'd1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0')

# Verify existing common-coordinate source selection without changing any source/art.
common=Image.open(refs[0]['path']).convert('RGBA');guide=Image.open(C/'inputs/source_pose_guide.png').convert('RGBA')
selection=Image.open(OLD/'inputs/SOURCE32_COMMON_LAYOUT_SELECTION_MASK.png').convert('L')
assert common.size==guide.size==selection.size==(704,976)
for channel in ImageChops.difference(common,guide).split():
    assert ImageChops.multiply(channel,selection).getbbox() is None
for bg in ['white','black']:
    qa=Image.new('RGBA',common.size,bg);qa.alpha_composite(common)
    out=Q/f'PREP_REFERENCE_95b20617_ORIGINAL_COMMON_LAYOUT_{bg}_READONLY.png';assert not out.exists();qa.convert('RGB').save(out)

prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt='\n\n'.join([
 prefix,
 '根据图1同一704×976原PV共同画布布局，一次连贯重绘整个当前可见人物为图2中性灰短圆润bob女孩身份。输出竖幅704:976比例、真实透明RGBA。图1独占本936头倾/脸大小、圆睁眼视线、tiny O开口、不同两手搭触和衣身/底裁；图2不得改成自己的中性闭口或抬臂。',
 '图1旧红整头/高根/帽已技术隐藏，原脸恢复原坐标；其余肩frill、两手、腰带、白围裙/黑裙和后带均是原像素原位置。alpha缺头区域不是黑块或输出裁断，需重新画完整灰bob与白帽两黑主叶；图1粉底/字幕不画。不要分别放大脸、缩身体或拼部件。',
 '脸—颈肩—两手接触点—腰—底裙保持图1共同坐标关系。特别保留腰以下一直到原画布底附近的全部已露白apron/黑裙，不能沿旧v03在腰下提前平切或构成宽短身体；不能靠拉躯干、抬腰、挪手或盲整体放大填底。只重建原已可见裙身，不加隐藏腿鞋。',
 '保原圆睁而非半睑、左右原视线、一种均匀charcoal实色虹膜和普通小圆白点，无独立黑中心/灰环/下月牙；嘴是小tiny O，不改闭笑。两只前搭手分别保原掌向、斜指/曲指与指尖接触，不变generic合十。暖桃肤、黑长袖立领、红bow金扣、白肩frill与竖带/袖口、围裙腰后带及恰好两片黑帽叶服从图1。',
 '唯一钻发根在人物LEFT低耳后/bob-nape，当前近正面为画右，双红珠与bob/颈肩连贯，不抬到眼/上耳、不镜像或加第二束。图2给整头肩中的合理发量，不巨粗、不micro。卷从宽gray前面连续翻回到opaque内后返回，接入下一圈再逐渐收细C，上端也要有入口/出口，不变封口椭圆盘堆或实心芯外绕绿线。图3只给这种宽灰回折连接，不复制高光或阴影。',
 'R81仅已实际观察的文字相位：靠近肩颈压紧回收、下段可由原白frill自然遮挡；不是复制AI身体或根。保合理固有发量，遮挡可改变可见尾长，不为露完整C强拉到frill/手前，也不借遮挡缩成小饰品；看不见的后绕不强画固定洞/圈数/轴长。',
 '图4仅颜料：bob与所有gray前/内/背/返回同一无光照灰#B6B4B2，mutedmint#B0C8BA只是材料带，线#171717；没有银亮、渐变或独立深灰体积底，不把opaque返回当空气挖掉、不全卷mint。真实露空才透明。头脸/颈领/帽/低珠卷/肩frill/两手衣裙一次整人连画，无贴片拼缝、独立碎块、背景或字幕。'
])+'\n'
pf=R/'prompt_imggen.txt';assert not pf.exists();pf.write_text(prompt,encoding='utf-8')
changed={
 'source_extent_problem':'Current16f629 photographic/source evidence lacks about70px lowerapron coverage at fitted933..937; do not compensate with partwise warp or blind enlargement.',
 'old_v04_unknown_not_a_result':'No image exists for that unknown invocation; reuse only known readonly inputs.',
 'reference_change_approved_by_root':'Oldv04 ref2 full head still contains closed-oval/broadmint prior coil and user F936 curl rejection. Keep it history-only. Ref2 now correct11 complete head-volume context216fd plus latestdetail0b88; original commonlayout/key preserved.',
 'old101_static_prefix_not_current_curl_standard':True,
 'source_layout_hypothesis':'Single original source canvas anchors all face/hand/waist/lowerapron rather than independently sized crops; output coherent whole.',
 'method_does_not_prove_provider_cause_or_success':True
}
request={
 'id':ID,'run':str(R),'operation_kind':'whole_character_redraw',
 'refs':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],
 'reference_roles':[x['role'] for x in refs],
 'prompt_file':str(pf),'prompt_sha256':sha(pf),'prompt':prompt,
 'tool_arguments':{'prompt':prompt,'referenced_image_paths':[x['path'] for x in refs],'transparent_background':True},
 'source_canonical_frame':936,'source_pts':499696,'first_case_frames':[933,937],
 'source_canvas_requested_in_prompt':[704,976],
 'native_size_parameter_exposed':False,'native_model_parameter_exposed':False,'native_quality_parameter_exposed':False,'user_quality_preference':'high',
 'transparent_background':True,'whole_character_one_generation':True,
 'user_explicitly_approved_one_additional_generation':True,'user_waiver':waiver,
 'old_unknown_remote_result_resolved':False,'old_unknown_run_preserved':str(OLD),
 'local_repair_parent':str(LOCAL),'local_parent_before_preparation':rec(snapshot),
 'local_parent_status_unchanged':True,'before_native_call_snapshot_must_refresh':True,
 'mandatory_whole_redraw_after_local_repair':True,'whole_redraw_completed_for_v05':False,
 'existing_v03_completed_flag_not_inherited_for_v05':True,
 'changed_reference_hypothesis':changed,
 'planned_additional_native_count_after_root_release':1,'automatic_retries':0,
 'PREPONLY':True,'submitted':False,'dispatchable':False,'awaiting_specific_root_release':True,
 'native_calls_authorized_this_prep':0,'native_calls':0,'api_calls':0,
 'fresh_root_Sol_and_separate_extent_photography_required':True,
 'hidden_geometry_certified':False,'source_visible_extent_coverage_verified':False,
 'user_accepted':False,'dynamic_validated':False,'central_registry_binding_exposure_written':False
}
req=put('request_imggen.json',request)
local_sem=put('LOCAL_PARENT_WHOLE_PENDING_FOR_V05.json',{
 'id':ID,'local_parent':str(LOCAL),'instant_before_preparation':rec(snapshot),
 'old_parent_exact_contents':read(snapshot),'parent_bytes_unchanged':True,
 'old_v03_completion_does_not_complete_new_extent_curl_repair':True,
 'new_v05_whole_completed':False,'fresh_whole_root_Sol_and_extent_photo_pending':True,
 'before_future_call_snapshot_must_refresh_without_rewriting_this_snapshot':True,'API_calls':0,'native_calls':0
})
prov=put('REF_INPUT_PROVENANCE.json',{
 'id':ID,'recorded_utc':datetime.now(timezone.utc).isoformat(),'request':req,'prompt':rec(pf),'refs':refs,
 'source':rec(source),'JOB':rec(C/'JOB.json'),'REGISTRATION_PLAN':rec(C/'REGISTRATION_PLAN.json'),
 'source_guide':rec(C/'inputs/source_pose_guide.png'),'source_commonlayout_selection':rec(OLD/'inputs/SOURCE32_COMMON_LAYOUT_SELECTION_MASK.png'),
 'old_commonlayout_provenance':rec(OLD/'SOURCE_COMMONLAYOUT_AND_PREFIX_PROVENANCE.json'),
 'source_commonlayout_selected_pixels_unchanged_at_original_positions':True,
 'layout_source_action_pixels_not_newly_drawn_or_composited_into_art':True,
 'source_exposure':state,'current_registry_snapshot_readonly':read(B/'ASSET_REGISTRY.json')[ID],
 'user_single_additional_waiver':waiver,'unknown_receipt':rec(receipt),'recovery_report':rec(recovery),
 'old_unknown_file_inventory_before_preparation':old_inventory,'old_unknown_reclassified_or_modified':False,
 'user_F936_curl_change_record':rec(B/'USER_DANCE_CURL_CORRECTIONS_20261102_v01.json'),
 'current_curl_requirements':rec(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'),
 'changed_reference_hypothesis':changed,'old_v04_ref2_excluded_from_generation':rec(OLD/'inputs/ref2_STATIC32V03_HEAD_CAP2_LOWROOT_CURRENT_GRAYRETURNS_PREFIX_ONLY.png'),
 'local_parent_instant_before':rec(snapshot),'local_parent_new_whole_pending':local_sem,
 'latest_detail_original_source':rec(B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'),
 'latest_detail_readonly_crop_xyxy':[35,58,146,260],
 'motion_R81_actual_viewed_full_not_generation_ref':rec(B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000081.png'),
 'motion_role':'text only close-to-shoulder compact return/naturalfrill occlusion; no body/eye/root or intrinsic-volume authority',
 'source_sourceguide_reference_QA_prepared_before_future_return':True,
 'PREPONLY':True,'API_calls':0,'native_calls':0,'quota_controls_invoked':False
})
for old in old_inventory:assert sha(old['path'])==old['sha256']
assert sha(LOCAL/'LOCAL_REPAIR_STATUS.json')==sha(snapshot)
print(json.dumps({'request':req,'prompt':rec(pf),'waiver':waiver,'provenance':prov,'refs':refs,'calls':0},ensure_ascii=False))
