from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
PRIOR=CEL/'whole_imggen_after_lowroot_upturn_continuous_gray_local_v07'
LOCAL=CEL/'local_v05_lowroot_continuous_gray_upturn_api_v01'
SRC=BASE/'coverage/source_frames/F001058.png'
HEAD=PRIOR/'character_imggen_original.png'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p)
    x={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:x.update(dimensions=list(im.size),mode=im.mode)
    return x
def dump(p,x):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (RUN/'request_imggen.json').exists()
assert sha(SRC)=='06b0b174d2ffde52c2b107d09841664e3aff451a4373a3648e3d612f7fcb7faf'
assert sha(HEAD)=='8487944cc93d80c6578b797a0afd84459a3ffc7cb10533328a08209f25acfa9e'
(RUN/'inputs').mkdir(exist_ok=True)
specs=[
    (SRC,[670,120,1140,1080],'ref1_NATIVE1058_COMMON_POSE_NO_HIGH_RED_COIL.png','Original native1058 common-coordinate pose authority: own eyes/chin/collar/highhand/lowhand/crossedsleeves/waist and apron vertical extent. No original highredcoil. Leftbackfrill/backbow/apron parts fall outside rectangle; cropedge is not finalcut. Never move/independently scale components.'),
    (HEAD,[30,0,785,592],'ref2_V07_8487944c_HEAD_CAP_TWOLEAVES_LOWERBEADS_IDENTITY_ONLY.png','Known v07 readonly head identity/cap2MAINleaves/roundgraybob/lowfarLEFTbeads only. No hands/body proportion. Incidental partialcurl/face expression not action or fullcoil authority; lower bob tips cropped, not outputedge.'),
    (HEAD,[630,425,896,615],'ref3_V07_8487944c_LOWBEADS_TO_TAPER_C_STRUCTURE_ONLY.png','Known v07 readonly complete lowbeads-to-C geometry/mediummass/outward-upturn only. Incidental bob/face/frill or tiny hand context not action/layout authority; do not transfer v07 head-to-hand or eye-to-waist distances.'),
    (SRC,[980,240,1135,535],'ref4_NATIVE1058_COMPLETE_OK_THREE_FINGERS_CUFF.png','Original native1058 entire highthumb-index OKcontact and 3otherfingers/cuff only, no original redcoil. Detailed shape; commoncoordinates and relative position exclusively reference1.'),
]
refs=[]
for source,roi,name,role in specs:
    dest=RUN/'inputs'/name
    with Image.open(source) as im:im.crop(roi).save(dest)
    refs.append({**rec(dest),'source_image':str(source),'source_sha256':sha(source),'crop_xyxy':roi,'role':role,'readonly_original_pixels_rectangular_crop':True,'no_art_paint_or_warp':True})
gray=LOCAL/'inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'
assert sha(gray)=='249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751'
dest=RUN/'inputs/ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png'
shutil.copyfile(gray,dest)
refs.append({**rec(dest),'source_image':str(gray),'source_sha256':sha(gray),'role':'pureGRAY#B6B4B2 unlit material only; thinmutedmint described in text','copied_without_pixel_change':True})
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''图1原PV1058的同坐标动作构图是唯一比例依据：眼线、下颌、衣领、高手OK接点与手腕、胸前低手指端、交叉袖和腰的位置必须保持同一连贯关系，按原PV把头/肩/双臂/腰围裙一次画全。不要沿图2或图3旧人物的眼到高手、眼到腰距离。图1只是从原片取的矩形，裁边不是输出切口；左边被裁的肩白褶、腰后结与源可见围裙要在完整半身画布自然延续，底边仍按原片实际可见围裙，不能补隐藏腿鞋，也不能拉躯干、移动低手或拉高腰来凑画面。

主角换成本OC中性灰短圆润bob女孩。图2仅给灰bob/完整白maidcap/两片MAIN黑叶和低耳后双珠的身份，弃用其身体与手的位置比例；图3仅给已经连贯的卷结构与适中发量。原图1红头发、尖额发不是目标身份，原高红卷没有送入参考。原1058不对称半眯但仍睁开的视线、小w闭嘴保持；两虹膜各单一均匀charcoal加普通白点，无黑芯灰环。图4仅核高手拇指食指相接的OK孔和另三指，手腕位置仍由图1控制；低手在胸前向下分指，交叉袖、红结金扣、黑长袖、白肩褶/袖口/腰后结/围裙依图1。

从同一画右人物LEFT远侧低nape入口接出一束卷，双珠和根低位可被bob自然遮住，画左近耳不长珠卷，不镜像或抬到帽边。保持图3中等体量和从本1058开始向画右外略上扬的连续螺旋：宽GRAY前面翻回不透明同GRAY内后返回，接下一转，再逐细成同一灰C。不要拆成独立碗片、封口盘、灰囊或独立绿粗尾环；按源bob/肩/手臂自然遮挡，不强露所有返回与尾，不固定孔数或圈数。

图5只定纯无光照GRAY #B6B4B2；bob与卷全部前/内/后返回/C同灰平涂，mint #B0C8BA仅窄材料边，无深灰体积底、银亮或渐变。整个当前可见半身人物一次连贯重绘，头颈帽肩卷衣手无拼接，不分部件缩放，不用整幅放大掩盖比例问题。真实透明人物层，实体灰返回不透明、实际空气透明；不画原片粉底/字幕/色卡或alpha0隐藏RGB。'''
pp=RUN/'prompt_imggen.txt'
pp.write_text(prompt+'\n',encoding='utf-8')
prompt=pp.read_text(encoding='utf-8')
shutil.copyfile(LOCAL/'LOCAL_REPAIR_STATUS.json',RUN/'LOCAL_REPAIR_STATUS_BEFORE_V08_PREP.json')
request={
    'id':'ART-G12-55','run':str(RUN),'PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'operation_kind':'whole_character_redraw','transparent_background':True,'whole_character_one_generation':True,
    'source_first':True,'existing_saved_API_repair_not_new_FIRST':True,
    'refs':[r['path'] for r in refs],'reference_sha256':[r['sha256'] for r in refs],
    'reference_roles_in_tool_order':[r['role'] for r in refs],'prompt_file':str(pp),'prompt_sha256':sha(pp),'prompt':prompt,
    'tool_arguments':{'prompt':prompt,'referenced_image_paths':[r['path'] for r in refs],'transparent_background':True},
    'source_frame':1058,'source_pts':564832,'source_native_size':[1920,1080],
    'source_pose_native_crop_xyxy':[670,120,1140,1080],
    'local_repair_parent':str(LOCAL),'known_local_raw_sha256':'8f180a6bf5c751cf5c657c8082d1e6fee2e1f6f827499604a284b9b9faaf2e0d',
    'mandatory_whole_after_local_repair':True,'new_whole_completed':False,'previous_whole_complete_pass_is_history':True,
    'v07_curl_static186_not_pose_photography_pass':True,
    'pose_photo_rejection_as_reported_by_root':{'uniform_common_solution':False,'eye_offset_x_approx':-46,'high_wrist_offset_x_approx':78,'low_fingers_offset_y_approx':79,'waist_offset_y_approx':68,'artist_did_not_recompute_these_numbers':True},
    'changed_reference_hypothesis':'Remove v07 fullbody composition target. Native1058 one common-coordinate rectangle exclusively sets face/chin/collar/arms/hands/waist relationships; v07 head identity and coil geometry are independent scoped rectangles only. Preserve known correct lowroot/medium upturn continuousgrayreturnC without inherited old pose distances.',
    'full_original_highredcoil_not_in_refs':True,'v07_fullbody_not_in_refs':True,
    'native_calls_authorized':0,'planned_native_calls_on_future_release':1,'native_calls':0,'API_calls':0,'HTTP_calls':0,'automatic_retries':0,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_size_parameter_exposed':False,'native_model_parameter_exposed':False,
    'fresh_root_Sol_and_actual_uniform_photography_required':True,'dynamic_tested':False,'user_accepted':False,
    'created_utc':datetime.now(timezone.utc).isoformat(),
}
dump(RUN/'request_imggen.json',request)
dump(RUN/'INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G12-55','refs':refs,'source_full':rec(SRC),'prior_v07':rec(HEAD),
    'v07_known_receipt':rec(PRIOR/'NATIVE_CALL_RECEIPT.json'),'v07_primary_static_only':rec(PRIOR/'PRIMARY_GOAL_REVIEW.json'),
    'local_known_result':rec(LOCAL/'result.json'),'local_status_before':rec(RUN/'LOCAL_REPAIR_STATUS_BEFORE_V08_PREP.json'),
    'source_cropped_out_visible_parts_note':'Nativepose rectangle excludes some leftbackfrill/backbow/apron contour. Full native source must be actually checked; rectangle is not output trim or authority to delete those parts.',
    'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'no_art_pixels_painted_pasted_or_warped':True,
})
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{
    'id':'ART-G12-55','PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),'refs':refs,
    'provenance':rec(RUN/'INPUT_PROVENANCE_PREPONLY.json'),'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
})
print(json.dumps({'request':rec(RUN/'request_imggen.json'),'prompt':rec(pp),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),'refs':refs},ensure_ascii=False,indent=2))
