from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json
import hashlib
import shutil

R=Path(__file__).resolve().parent
B=R.parents[3]
PROJECT=B.parents[1]
C=R.parent
ID='ART-G12-69'
OLD=C/'prep_first_api_source1123_graybob_ownpalms_v01'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    p=R/name;assert not p.exists(),p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rec(p)

assert not (R/'request_imggen.json').exists()
(R/'inputs').mkdir(parents=True,exist_ok=True)
registry=read(B/'ASSET_REGISTRY.json')[ID]
job=read(C/'JOB.json')
state=next(s for s in read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states'] if s['id']==ID)
target=OLD/'character_api_original.png'
assert sha(target)==registry['sha256']=='3a4ac695444da7cbba26c462f5e4fa229cbcd3ff0c5eca6b758daacc8804a3a0'
assert job['source_frame']==state['existing_source_canonical_frame']==1123 and job['source_pts']==599536
assert [state['first_frame'],state['last_frame']]==[1123,1128]
attempts=[];unknown=[]
for f in C.rglob('attempt.json'):
    a=read(f);e={'attempt':rec(f),'exact':a}
    result=f.parent/'result.json';raw=Path(a.get('image',''))
    if a.get('status')!='completed' or not raw.is_file() or not result.exists() or sha(raw)!=read(result)['output_sha256']:
        unknown.append(e)
    else:e.update(raw=rec(raw),result=rec(result),known_saved=True,elapsed_seconds=read(result)['elapsed_seconds'])
    attempts.append(e)
local=[{'file':rec(f),'exact':read(f)} for f in C.rglob('LOCAL_REPAIR_STATUS.json')]
native=[rec(f) for f in C.rglob('BUILTIN_GENERATION.json')]
put('KNOWN_FIRST_AND_ANCESTRY.json',{'id':ID,'API_attempts':attempts,'local_repair_ancestors':local,'existing_native_receipts':native,'unknown':unknown,'calls':0})
assert len(attempts)==1 and not unknown and not local and not native
source=Path(job['source_image']);guide=C/'inputs/source_pose_guide.png'
assert sha(source)==job['source_image_sha256']
g02=B/'inputs/eye_G02-01_F100.png'
key=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
assert sha(g02)=='6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'
assert sha(key)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'
assert sha(detail)=='4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'
refs=[]
def cp(name,p,role,xy=None):
    out=R/'inputs'/name;assert not out.exists()
    if xy is None:shutil.copyfile(p,out)
    else:
        with Image.open(p) as im:im.crop(xy).save(out)
    e={**rec(out),'source':rec(p),'role':role}
    if xy is not None:e['source_crop_xyxy']=xy
    refs.append(e)
cp('ref1_CURRENT69_SAVED_FIRST_RGBA_KEEP_COMPLETE_VISIBLE_CHARACTER.png',target,'已有known-FIRST完整人物edit target，仅保持灰bob身份/前bow/低LEFT根与宽gray返回C/两帽叶/手衣及原半身底切；两iris黑中心+下灰月牙是明确错误，不保留这种眼内分区。raw透明区隐藏RGB不是背景或新发面。')
cp('ref2_ORIGINAL1123_COMPLETE_UNMASKED_POSE_GUIDE.png',guide,'原PV1123唯一头前bow、不对称半开向下眼/原视线、小闭弧笑、低肘两手不同斜指拇指、衣身及底裁。完整不挖头像；红发尖长额发和双高卷不是目标身份。')
cp('ref3_G02_EYE_STYLE_ONLY_UNIFORM_CHARCOAL_NOT_APERTURE.png',g02,'仅眼内一块均匀charcoal填色与简笔线方法；不复制该图半睑开度/眼形/视线/表情，也不复制其近心形小白点，输出普通小白点数量不限一或二。',[380,15,638,143])
cp('ref4_UNLIT_GRAY_MINT_MATERIAL_KEY.png',key,'现bob及卷front/inner/back/return保持同一gray平涂，mint材料带；不重新设计卷或用色表变全mint。')
cp('ref5_LATEST_GRAY_FRONT_RETURN_DETAIL_ONLY_PRESERVE_CURRENT_C.png',detail,'只作现有宽gray前/不透明内后返回/下一圈/渐细C的防退化构造约束，不复制精修高光/深底/轴向/大小，不改变当前69已可读构造和低根。',[35,58,146,260])
assert refs[4]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'

# Original-source eye crop is diagnostic evidence only; it is not a sixth generation reference.
source_eyes=R/'SOURCE1123_OWN_HALFOPEN_DOWNGAZE_MOUTH_READONLY.png'
with Image.open(guide) as im:im.crop([555,280,770,395]).save(source_eyes)
sourceeyes_record={**rec(source_eyes),'source':rec(guide),'source_crop_xyxy':[555,280,770,395],'generation_reference':False,'no_pixels_pasted_into_art':True}
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt='\n\n'.join([
    prefix,
    '以图1现有完整透明人物为保持基准，一次连贯重绘整个当前可见人物。图2原PV1123只拥有本向前bow的头身动作、不对称半开向下眼/视线、小闭弧笑、低肘双手不同斜指和拇指、衣身与原底裁；不把原红尖发/高双卷换回来。保持图1中性灰短圆润bob/自然灰刘海贴颊侧发、低LEFT双红珠、当前宽gray前返回/C、白cap两黑主叶与原黑白衣红bow金扣。',
    '这次明确修两只虹膜的填色：每只iris从上到下只一块均匀charcoal实色，不留黑中心配灰下半月牙/灰环，不画另一个黑瞳芯或渐变分区。眼白保留眼白；不是把整只眼白涂黑。普通小圆白点即可，不规定只能一颗或两颗，不复制图3近心形点。图3仅提供这种单色填法，绝不拥有本稿眼开度；保持图2/图1原1123不对称半开、向下视线与前倾，不睁圆、不闭成线、不抬头换表情。',
    '唯一人物LEFT低耳后/bob-nape根按当前近正面投影保持在画右，双珠与bob/颈肩自然接合；不抬根到眼或镜像人物。当前宽GRAY发带前面向opaque内/后返回接下一圈并渐细C的形态/合理头肩体量/肩前路线保持，不变封口盘堆/实心锥贴绿线，不巨粗不micro，不为改眼强拉尾或新挖固定孔。图5仅防连接退化，不重设计当前卷。图4要求bob与卷所有gray面同无光照灰，mutedmint只是材料带，没有独立银亮/深灰体积暗底/渐变，不涂全mint。',
    '保持本稿低肘两长袖与两手不同侧斜指/独立拇指、原白袖口/肩frill/红bow金扣/腰后bow/apron及black裙；暖桃肤。1360x848原半身构图和底部直切边保留，最终摄影需把该原底切放到画外，不能为遮底缩人、加腿鞋或补隐藏裙。',
    '整个人物头脸、低根、颈领、cap、肩frill、卷和衣手一次重新画连贯，不局部贴眼/拼辫/代码修色。真实透明RGBA人物，无粉底字幕、棋盘、色表或额外物件。'
])+'\n'
promptfile=R/'prompt_imggen.txt';assert not promptfile.exists();promptfile.write_text(prompt,encoding='utf-8')
request={
    'id':ID,'run':str(R),'operation_kind':'whole_character_redraw','existing_known_FIRST_repair_not_new_FIRST':True,
    'edit_target':rec(target),'source_frame':1123,'source_pts':599536,'first_case_frames':[1123,1128],'source_canvas_guidance':[1360,848],
    'refs':[e['path'] for e in refs],'reference_sha256':[e['sha256'] for e in refs],'prompt_file':str(promptfile),'prompt_sha256':sha(promptfile),'prompt':prompt,
    'tool_arguments':{'prompt':prompt,'referenced_image_paths':[e['path'] for e in refs],'transparent_background':True},
    'repair_reason':'双方iris黑中心+下半gray月牙成块违反单charcoal实色；源半开/下视/小闭笑、当前低LEFT根/grayreturnC与body保留。root指出Sol158正在正式落盘；本次已独立实看其精确白黑3x诊断，正式报告状态在handoff单独记录。',
    'changed_hypothesis':'直接whole整个人物保当前几何，G02眼部只作单色颜料/线法、原1123与当前target独占眼开度。无局部贴眼或API局修，也不复制G02半睑角度；不把图1错误眼分区当保持项。',
    'local_repair_parent':None,'local_patch_this_turn':False,'masked_local_ancestor_found':False,
    'whole_character_one_generation':True,'mandatory_whole_for_this_repair':True,'whole_completed':False,
    'fresh_root_Sol_and_separate_photographic_review_required':True,
    'PREPONLY':True,'submitted':False,'dispatchable':False,'native_calls_authorized':0,'native_calls_authorized_this_record':0,
    'planned_native_count_on_future_release':1,'API_calls':0,'native_calls':0,'automatic_retries':0,
    'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,
    'transparent_background':True,'user_accepted':False,'dynamic_validated':False,
    'white_highlight_count_policy':'ordinary round glints, no forced one-or-two count','iris_policy':'one uniform charcoal region; no separate black core/gray ring or lower crescent',
}
put('request_imggen.json',request)
diagnostics=[B/'review/sol_xhigh_round158_diagnostics/EYES_LOW_ROOT_COIL_white_3x.png',B/'review/sol_xhigh_round158_diagnostics/EYES_LOW_ROOT_COIL_black_3x.png']
put('INPUT_PROVENANCE_AND_EYE_REPAIR_EVIDENCE.json',{
    'id':ID,'created_utc':datetime.now(timezone.utc).isoformat(),'refs':refs,'readonly_source_eye_diagnostic':sourceeyes_record,
    'JOB':rec(C/'JOB.json'),'REGISTRATION_PLAN':rec(C/'REGISTRATION_PLAN.json'),'source_full':rec(source),'source_guide':rec(guide),
    'registry_exact_snapshot':registry,'current_PRIMARY':rec(registry['primary_review']),'source_frame_priority':state,
    'source_full_and_current_raw_QA_paths':[rec(f) for f in [source,guide,target,OLD/'qa_white.png',OLD/'qa_black.png']],
    'Sol158_exact3x_diagnostics':[rec(f) for f in diagnostics],'history':rec(R/'KNOWN_FIRST_AND_ANCESTRY.json'),
    'plain_G02_method_not_source_aperture':True,'all_prior_candidates_and_reviews_preserved':True,
    'all_created_crops_only_inputs_or_readonly_QA_no_art_pixels_edited':True,'no_central_JOB_REGPLAN_or_binding_write':True,
    'API_calls':0,'native_calls':0
})
print(json.dumps({'request':rec(R/'request_imggen.json'),'prompt':rec(promptfile),'refs':refs,'source_eye_diagnostic':sourceeyes_record,'calls':0},ensure_ascii=False))
