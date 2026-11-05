from pathlib import Path
import json, hashlib
from datetime import datetime, timezone
from PIL import Image

RUN=Path(__file__).parent
B=RUN.parents[3]
PROJECT=B.parents[1]
PRIOR=RUN.parent/'whole_imggen_source2339_connectedgray_occlusion_v02'
I=RUN/'inputs'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(name,obj):
    p=RUN/name
    if p.exists(): raise RuntimeError(f'preserve existing {p}')
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return p
def meta(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    try:
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    except Exception:pass
    return d
now=datetime.now(timezone.utc).isoformat()
target=PRIOR/'character_imggen_original.png'
assert sha(target)=='da4a0c93fb2b783131f9cf2bfcd168894138cb095b8568966a62d69bceeedd45'
sol=B/'review/sol_xhigh_round166.json'
assert sha(sol)=='dfa2fd5efe5c4d8ace9d08fb176fd2307cd1c1b6b50ebfb691b3479248e0f845'
entry=next(e for e in load(sol)['entries'] if e['id']=='ART-G33-09')
refs=[I/'ref1_CURRENT09_da4a0c93_COMPLETE_CHARACTER_OCCLUSION_REPAIR_TARGET.png',
      I/'ref2_ORIGINAL2339_COMPLETE_UNMASKED_POSE_GUIDE.png',
      I/'ref4_ORIGINAL2339_OWN_WHITE_FAN_BLACK_PUFF_SLEEVE_BOUNDARY_NO_HAIR.png',
      I/'ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png']
roles=[
 '图1=当前09完整透明人物编辑目标，保中性灰短bob/头身体量/低LEFT珠根/连通宽灰返回/眼口衣手。其下圈和完整C悬在黑袖前是待改错误，不是需要保留的遮挡。',
 '图2=完整未挖头原2339，唯一动作、圆眼极小中性口、低斜摊掌/腰后隐手、衣裙腿及源底裁依据。原红发/尖额发/双高卷身份与高根不能复制。',
 '图3=图2原白肩fan/竖褶及黑泡袖的只读局部，crop[235,270,342,405]。只定真实衣肩轮廓、前后关系，不放大肩袖、不新增白褶遮盖。',
 '图4=纯GRAY RGB182/180/178(#B6B4B2)输入颜料，非几何/分区模板；薄mint保图1当前分区和muted色，不变整束绿色。'
]
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''\n\n将图1这个已有角色的完整可见人物一次连贯重画，透明背景。保它的中性灰短圆润bob女孩身份、自然灰刘海和贴颊短发、现有头身比例、画右低耳后LEFT双红珠、白cap和两片主要黑叶。图2是本帧原2339动作/衣肩/裁切的唯一依据；不要复制图2红发、尖长额发、双高卷或高根。图3是图2的原肩fan/黑泡袖轮廓局部，图4只是无打光灰颜料。\n\n这次仅修图1下段卷的回收与肩袖遮挡：目前下几圈连完整C都垂在黑泡袖前，改为从不动的同侧低耳后根，保宽灰发带的固有体量和上端连通，尾段随当前相位向颈肩后侧回收，让原白肩fan/竖frill及黑泡袖按原轮廓自然挡住下段。C可部分或全部藏在肩后，不能为露全尾拉到黑袖前；也不能扩大肩饰/袖子或缩成tiny挂件来遮盖。回收时是同一条宽灰前面翻入不透明内/后返回、接下一圈、渐细C，隐藏段不另长第二束、不抬根、不换边、不镜像身体。可见灰返回仍是实体，不能把它一律挖成空气；真正露空才透明。\n\n已实际查看R28全帧：只取头发在颈肩处紧压、下收回弹的次运动相位，R28不作为生成位图。向原肩后回收是结合原肩袖与相邻状态的静态转译，不复制AI的白frill形状、脸眼笑容、手臂或小实体卷。保图1正常整头相对发量，不因AI小ROI或隐藏尾段把整束缩小；不固定圈数、孔数、轴长。保图1现有可读宽灰前/返回连接，不重新设计为封口椭圆帽片堆、实心锥或绿线绕实体。\n\n严守图2自己的表演：双眼圆睁略不对称、原视线、极小中性短闭口不加笑；画右长臂斜向右下，低摊掌外朝、独立拇指右上、其余分指向右下，保白袖口角度与指形；画左臂弯向腰后，手被身躯挡住，不补露手。黑长袖、原白肩fan及竖褶、红bow金扣、白袖口/围裙/腰后带、黑裙、交错前腿与后抬腿保持本source。保源实际底裁，前景鞋尖贴原1080下边未见的部分不补，不加隐藏腿鞋，不缩人移位来露全脚。不得借相邻08低竖手或10高折腕换本帧动作。\n\n所有bob和灰卷的前/内后/返回都保持同一种无光照GRAY#B6B4B2，与当前薄mutedmint材料带清楚分区；用墨线和互遮表现绕行，不加独立深灰体积内底、银白亮边或渐变，不改成全mint。暖桃肤、单一均匀charcoal虹膜及普通小圆白点保留，眼开度仅原2339，不引入半睑模板/黑中心灰环。整个人物统一头颈、帽、肩衣和卷连接，一次整画；不局部贴卷、不warp、不开蒙版、不拼部件。只输出真实透明人物，无原粉色背景、字幕、棋盘格、色卡或独立物件。\n'''
pp=RUN/'prompt_imggen.txt'
if pp.exists():raise RuntimeError('preserve prompt')
pp.write_text(prompt,encoding='utf-8')
changed='以current09连贯整人为身份/身体/低根与宽灰连接主体，去掉完整correct11垂挂头卷和精修光影detail；原2339全guide+自己的无头肩fan局部独占动作与衣肩遮挡。R28实际纯hair crop仅39x28，缺少相对肩部语境且有旧实体卷条纹，保留其只读证据但不输入生成，改用实际全帧观察的回收文字；纯GRAYkey只约束颜料。检验移除竖挂几何竞争、保衣不变而尾段后收的参考假设，非已证实因果或隐藏路径认证。'
request={
 'id':'ART-G33-09','run':str(RUN),'operation_kind':'whole_character_redraw',
 'existing_saved_API_repair_not_new_FIRST':True,'source_first_authority':True,
 'refs':[str(p) for p in refs],'reference_sha256':[sha(p) for p in refs],
 'reference_roles_in_tool_order':roles,'prompt_file':str(pp),'prompt_sha256':sha(pp),'prompt':prompt,
 'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(p) for p in refs],'transparent_background':True},
 'transparent_background':True,'whole_character_one_generation':True,
 'current_repair_target':meta(target),'source_frame':2339,'source_pts':1248720,'first_case_frames':[867,870],
 'source_canvas_guidance':[624,1072],'source_pose_guide':meta(refs[1]),
 'independent_repair_review':meta(sol),'independent_review_exact_image_sha256':entry['image_sha256'],
 'sole_P1':'下段多圈与完整C前挂于黑泡袖前，当前回收相位与原肩fan真实遮挡未被转译；不是连通、固有体量、材料P1。',
 'changed_reference_hypothesis':changed,'lower_occlusion_route_is_static_translation_inference':True,
 'no_AI_clothing_mask_or_body_reference':True,'no_R28_bitmap_submitted':True,
 'no_original_art_patch_composite_or_warp':True,'local_repair_parent':None,
 'mandatory_whole_after_local_patch':False,'whole_visible_character_redraw_required_this_request':True,
 'historical_whole_completion_not_inherited':True,'fresh_root_and_Sol_required_after_return':True,
 'PREPONLY':True,'submitted':False,'dispatchable_by_artist':False,
 'native_calls_authorized_this_record':0,'planned_native_n_on_future_root_release':1,
 'native_calls':0,'API_calls':0,'automatic_retries':0,'user_quality_preference':'high',
 'native_quality_parameter_exposed':False,'native_size_parameter_exposed':False,'native_model_parameter_exposed':False,
 'user_accepted':False,'dynamic_validated':False,'prepared_utc':now
}
rp=write('request_imggen.json',request)
registry=load(B/'ASSET_REGISTRY.json')
assert registry['ART-G33-09']['sha256']==sha(target)
write('CURRENT_SELECTED_STATUS_FRESH166_SNAPSHOT.json',{'captured_utc':now,'record':registry['ART-G33-09'],'PRIMARY':load(PRIOR/'PRIMARY_GOAL_REVIEW.json'),'snapshot_only':True})
root=RUN.parent
attempts=[]
for p in root.rglob('attempt.json'):
    if RUN in p.parents:continue
    obj=load(p);res=p.parent/'result.json'
    attempts.append({'attempt':meta(p),'status':obj.get('status'),'result':meta(res) if res.exists() else None,'record':obj})
native=[]
for p in root.rglob('BUILTIN_GENERATION.json'):
    if RUN in p.parents:continue
    raw=p.parent/'character_imggen_original.png'
    native.append({'record':meta(p),'record_data':load(p),'original_output':meta(raw) if raw.exists() else None})
unknowns=[str(p) for p in root.rglob('*UNKNOWN*') if RUN not in p.parents]
local=[str(p) for p in root.rglob('LOCAL_REPAIR_STATUS.json') if RUN not in p.parents]
assert not unknowns
assert not local
write('KNOWN_FIRST_AND_LOCAL_ANCESTRY_CHECK.json',{
 'checked_utc':now,'known_FIRST_result':meta(root/'result.json'),'known_FIRST_original':meta(root/'character_api_original.png'),
 'FIRST_elapsed_seconds':load(root/'result.json')['elapsed_seconds'],'attempts':attempts,'known_builtin_records':native,
 'current_native_call_receipt':meta(PRIOR/'NATIVE_CALL_RECEIPT.json'),'current_native_known_saved':load(PRIOR/'NATIVE_CALL_RECEIPT.json')['known_result_saved'],
 'unknown_named_records':unknowns,'local_repair_status_ancestors':local,'local_repair_parent':None,
 'no_unknown_retry_or_extra_FIRST':True,'no_ancestor_status_modified':True,'new_native_completed':False,
 'old_repair_evidence_preserved':True,'future_new_art_requires_fresh_root_Sol':True,'API_calls':0,'native_calls':0})
seen=[
 target,PRIOR/'qa_white.png',PRIOR/'qa_black.png',
 B/'review/sol_xhigh_round166_diagnostics/CURRENT_ROOT_COIL_white_3x.png',
 B/'review/sol_xhigh_round166_diagnostics/CURRENT_ROOT_COIL_black_3x.png',
 B/'review/sol_xhigh_round166_diagnostics/CURRENT_EYES_white_3x.png',
 Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-09/source.png'),
 *[B/f'coverage/source_frames/F{f:06d}.png' for f in range(867,871)],
 B/'drawings/ART-G33-08/v01/whole_imggen_source2334_gray_connected_spiral_v05/qa_white.png',
 B/'drawings/ART-G33-08/v01/whole_imggen_source2334_gray_connected_spiral_v05/qa_black.png',
 Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-08/source.png'),
 Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-10/source.png'),
 B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000028.png',
 B/'review/sol_xhigh_round166_diagnostics/R028_SECONDARY_HAIR_SHOULDER_PHASE_3x.png',
 *refs,I/'ref3_R028_HAIR_ONLY_RECOIL_PHASE_NO_FACE_ROOT_CLOTH.png',
 RUN/'PREP_REFERENCE_R028_HAIR_ONLY_8x.png',RUN/'PREP_REFERENCE_SOURCE2339_SHOULDER_BOUNDARY_3x.png',
 RUN/'PREP_R028_CONTEXT_READONLY_NOT_GENERATION_REF_6x.png']
dedup=list(dict.fromkeys(seen))
write('ARTIST_REFERENCE_REVIEW_PREPONLY.json',{
 'id':'ART-G33-09','reviewer':'xhigh_pending_artist own actual tool image views','inspection_recorded_utc':now,
 'actual_viewed_existing_images':[meta(p) for p in dedup],
 'own_observations':[
  'da4a0 current完整白黑和3x直接可见下圈/完整C悬在黑泡袖前，肩fan在其后，没有下段回收遮挡；低LEFT画右nape/两珠、正常发量、宽灰返回与C连接可保。',
  '2339完整原源及未挖头guide：近正面轻侧倾、左右圆睁略异、极小中性闭口；画左臂腰后隐手，画右臂斜右下低摊掌，拇指朝右上其余分指右下。原画右白fan突出，后接黑泡袖，衣肩尺寸不能放大。',
  '867/868/869/870各全幅实际看：同态半身曝光，低掌出画底；不能据此删canonical2339原可见裙腿。曝光间无新手势判据，未认证播放。',
  '相邻08 current白黑及2334源为近竖低掌，保头肩上下文但不得借其动作；source10/2342已变画右高伸臂折腕垂指，本09不得提前。',
  'R28全幅与只读上下文显示颈肩侧发束紧压/回收，下端与AI肩饰重叠；这只能辅助相位，原肩袖权威来自2339。隐藏路径是静态转译推断，非原源有低灰卷的直接证据。',
  '最初39x28严格hair-only候选crop无眼/根/衣，但仅卷面条纹缺相对肩语境且有旧实体卷几何，最终4refs不发送它；保留旧输入草案与只读证据，不伪称删除后审图。',
  '原肩fan readonly crop确无原红coil、头、双珠，纯灰key无几何；当前mono iris小白点可保，不发G02半睑。'
 ],
 'scope_limits':['仅静态源/当前图对照，没有播放','隐藏卷体拓扑/体量不因C遮住被认证','当前连接与材料不是166 P1','新图不存在，不能记录为新图实际看或PASS','源前鞋贴1080底裁需保持，不认证当前多出的完整toe'],
 'chosen_final_reference_count':4,'final_roles':roles,
 'initial_provisional_five_ref_input_record_retained':'INPUT_PROVENANCE_PREPONLY.json',
 'final_hair_phase_mode':'text_only_from_actual_full_R28_observation; hair-only bitmap retained diagnostics only',
 'PREPONLY':True,'API_calls':0,'native_calls':0,'user_accepted':False,'dynamic_validated':False})
diag=[]
for bg in ['white','black']:
    source=PRIOR/f'qa_{bg}.png'
    xy=[345,270,535,575]
    with Image.open(source) as im:
        crop=im.crop(tuple(xy))
        for scale in [1,3]:
            out=RUN/f'PREP_PRIOR_CANDIDATE_da4a0c93_ROOT_RETURN_C_SHOULDER_{bg}_{scale}x.png'
            crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST).save(out)
            diag.append({'file':meta(out),'source_image':str(source),'source_sha256':sha(source),'raw_source_image':str(target),'raw_source_sha256':sha(target),'crop_xyxy':xy,'scale':scale,'prepared_before_future_return':True,'prior_candidate_only_not_future_return_evidence':True})
write('PREP_PRIOR_CANDIDATE_DIAGNOSTIC_PROVENANCE.json',{'diagnostics':diag,'future_return_exists':False})
lock=write('REQUEST_LOCK_PREPONLY.json',{
 'id':'ART-G33-09','request':meta(rp),'prompt':meta(pp),'ordered_refs':[meta(p) for p in refs],
 'source_review':meta(sol),'current_target_sha256':sha(target),
 'PREPONLY':True,'dispatchable_by_artist':False,'native_calls_authorized':0,'planned_future_one_native_only_after_root_release':True,
 'API_calls':0,'native_calls':0,'automatic_retries':0,'no_attempt_or_execution_created':True,
 'fresh_review_required_after_future_whole':True
})
print(json.dumps({'request':meta(rp),'prompt':meta(pp),'lock':meta(lock),'references':[meta(p) for p in refs],'diagnostics':[d['file'] for d in diag]},ensure_ascii=False,indent=2))
