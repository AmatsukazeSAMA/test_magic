from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json
import hashlib
import shutil

HERE = Path(__file__).resolve().parent
B = HERE.parents[3]
PROJECT = B.parents[1]
H = Path(r'D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p = Path(p)
    d = {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower() == '.png':
        with Image.open(p) as im: d.update(size=list(im.size),mode=im.mode)
    return d
def put(r,name,d):
    f=r/name;assert not f.exists(),f
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rec(f)

now=datetime.now(timezone.utc).isoformat()
registry_path=B/'ASSET_REGISTRY.json';registry=read(registry_path)
scope_path=B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json';states=read(scope_path)['states']
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
identity=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
palette=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
policy=B/'USER_DANCE_CURL_CORRECTIONS_20261102_v01.json'
requirements=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
assert sha(identity)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
assert sha(detail)=='4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'
assert sha(palette)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'

rows=[{'id': 'ART-G33-09',
  'source': 2339,
  'pts': 1248720,
  'first': [867, 870],
  'first_pts': [462864, 464992],
  'run': 'whole_imggen_source2339_connectedgray_occlusion_v02',
  'selected_sha': 'a425cc873b2a8ce69707a3b7fff7ab8a75ad1c5245b2ef05f51adfc2201ce1fc',
  'first_API_sha': '2d576fc092c80d5ba70508b983fd6bb06d96f16eabb91135d08c5405330c2c7a',
  'fifth_crop': [134, 154, 269, 242],
  'fifth_name': 'ref5_ORIGINAL2339_OWN_OPEN_EYES_TINY_NEUTRAL_MOUTH.png',
  'fifth_role': '仅本2339圆睁不对称眼弧/虹膜露出、视线及极小中性闭口。不是G02半睑模板，不贴艺术像素，不借身份图或AI小笑。',
  'evidence_frames': [866, 867, 870, 871],
  'action': '原2339头近正面略侧倾，双眼圆睁且左右睫弧/视线略不对称，极小中性短闭口，不加笑。画左臂向腰后弯折、手真实被身体挡住，不凭空补出；另一长臂从画右肩斜向右下伸出，低摊掌朝前外、独立拇指指向右上，四分指向右下，保原不规则指形/掌纹与白袖口斜角。不是前08近竖下掌，也不是下一10高伸臂折腕垂指。原black长袖/白肩fan和竖褶/白袖口、红bow金扣、腰带与后bow、长apron锯齿边黑裙、交错前腿/屈膝抬后腿及踝带鞋的原可见段保留，不拉直站姿。',
  'extent': 'canonical2339原前景鞋尖贴1080底边截断，后抬鞋可见；624x1072完整guide保原共同构图与底裁，不沿当前native补圆完整toe，也不缩人/上移以露全原未见鞋端。first867..870是放大半身曝光，不能拿其未露脚豁免canonical原见裙腿，摄影定位另审。',
  'motion': '已实际看R28全帧：低耳颈侧卷仍向肩侧下收、局部紧压回弹，白frill遮住下端；只有发丝次运动文字，不输入AI小实体卷/完整头眼/低臂身体位图。小可见段和自然遮挡不能定义固有发量变小，不能复制AI微笑或沿08旧外展固定轴。',
  'repair': 'current registry '
            'repair_required来自用户明确点名母2339钻发形态错误；PRIMARY与Sol95当时为retained，没有把其旧issues空列表篡改成Sol当时已判P1。用户后来否决覆盖旧静态保留。当前可见上端灰椭圆盖面接数片宽mint闭合弧带，宽灰前→内后返回的入口/出口仍不清，下端被白肩饰遮住，隐藏拓扑不可认证，也不能单凭没有洞判实心。低LEFT根、源眼口手body有可保范围；softgray/mint材料与投影原为P2，后续fresh实看，不能伪当已满足当前无打光要求。',
  'hypothesis': '改用完整未挖头2339 '
                'guide独占所有表演和比例，完全排除当前09整头/闭合卷与旧08/09低根head模板。用用户正确11完整head-coil上下文给OC中性灰bob和合理整头体量，最新graydetail只给宽灰连续前/返回，unlitkey给同灰材料，本source眼口第5张防身份/AI改表演。检验拿掉旧闭合弧带几何竞争的source-first假设，非已证实内部原因；保实际肩frill遮挡，不强拉全C。',
  'specific_prompt': '低LEFT双红珠下是同一条宽GRAY发带：上端灰前面翻向内/后、实际接回下一圈，不能独立椭圆盖片接一串封闭薄荷盘。沿本态颈肩回收时仍有宽灰主面和返回，不是只有一条薄荷装饰绕实心体。逐圈渐细C可部分被原白肩frill真实挡住，遮挡不是缩小发量，也不能为了证明结构硬拉整尾到肩褶前。图5只本源眼口，严守源圆睁/极小中性闭口、低斜摊掌与腰后隐藏手。',
  'neighbor': 'actual866前08仍近竖下垂臂，867/870本2339改成斜向右下外伸摊掌；actual871后10将该臂抬高、手腕折下，不能把后态手套给09。first867..870属一个PRIORITY状态，其首末PNG有微小RGB差异，不自动逐像素alias，也不机械新增人物项；本source与first放大构图只用于当前源态，非曝光定位或动态认证。'},
 {'id': 'ART-G33-10',
  'source': 2342,
  'pts': 1250320,
  'first': [871, 873],
  'first_pts': [464992, 466608],
  'run': 'whole_imggen_source2342_connectedgray_sleeveocclusion_v02',
  'selected_sha': '07c70b582c6b4401dc84d8b85dc6c1483dad2fdf7d0e692e7ab35462a462863d',
  'first_API_sha': '54cb01abe717c8df495248aa8965f51d5b59b9d1c8999bfa45d7c45ab79acc28',
  'fifth_crop': [119, 132, 244, 215],
  'fifth_name': 'ref5_ORIGINAL2342_OWN_OPEN_EYES_TINY_NEUTRAL_MOUTH.png',
  'fifth_role': '仅本2342原圆睁不对称眼开度/iris露出、视线及tiny中性闭口。不可抄AI小笑/身份图表情，不送G02半睑图，不贴艺术像素。',
  'evidence_frames': [870, 871, 873, 874],
  'action': '原2342头近正面略向画左倾，双眼圆睁、视线和两侧眼弧不对称，tiny中性短闭口。画右长臂高斜外伸、白袖口接折腕，原拇指向上、指尖水平/垂下的风格化轮廓分别保留，不是09低斜摊掌，也不是后874向上摊开的高掌。画左肘折回、手真实藏在腰后，不补隐藏手。高臂black袖下原本有锯齿轮廓，按source齿深/齿尖画，既不误当新破洞抹平，也不沿当前旧稿进一步夸大。原black领/长裙长袖、红bow金扣、白肩frill竖带/袖口、腰带后bow和apron、交错弯腿/后抬鞋均按2342。',
  'extent': '完整624x1056原guide而非09的624x1072，头/高折腕手/腰/长apron/黑裙/双腿鞋共同比例保持。canonical2342前鞋尖在1080边界贴底截断，后抬鞋可见；不沿当前native完整额外toe认作源已见几何，不能缩人抬人去露未见鞋尖。first871..873放大半身的摄影另审，不裁掉canonical原见裙腿或假称已绑定。',
  'motion': '已实际看R31全帧：低颈侧卷更压紧，随高袖/肩frill自然遮挡，只见少量回折灰发带；不发送AI完整头身/微笑和卷bitmap，仅相位文字。自然挡住不等于可以画成实心盖盘/微型挂件，也不强制拉出隐藏尖C或把根抬到上耳。',
  'repair': 'current registry repair_required由用户明确点名母2342钻发形态错误覆盖旧PRIMARY/Sol103 '
            'retained。Sol103当时没有可见结构P1，只保留softgray/mint色阶/相位等P2，不能伪说其当时已否决。本轮实际可见珠下上端仍似独立灰椭圆盖面与几片mint弧带，前面→内后返回路径需重建；后续被白肩frill/高black袖挡住，不认证隐藏完整卷/轴/C，也不能把真实遮挡当成必须露出整束。当前低LEFT根和主要源表演可保；原袖锯齿不是新服装破损，当前较深尖的袖廓应回依source。',
  'hypothesis': '排除曾喂入的09完整头/压紧闭合卷模板，也不以当前10整头作保持锚；完整未挖头2342 guide独占本帧动作与布局。correct11完整头卷只本OC '
                'graybob/低根身份与整头相对体量，graydetail只连通宽灰前返，palette只无打光同灰，第五本源眼口防表演漂移。以不同参考假设重建当前可见起卷的真实连通，仍遵原高袖/肩frill遮挡，不靠堆洞词或强露全C。',
  'specific_prompt': '低LEFT根双红珠下的起卷同一宽GRAY发带前面向内/后翻回进入下一圈，画清当前露出的连接，不是椭圆灰盖面后排一串封口mint片。该束在本态压紧于原肩frill和高black袖后，这些真实衣物遮挡继续不透明；被挡的整尾/C不强拉出来，也不挖空gray返回去强造洞。头肩上下文保固有发量，不巨粗、不微型。图5只本源眼口，高折腕手指/原袖齿深全听图1。',
  'neighbor': 'actual870前09是较低斜伸摊掌；871/873本2342抬臂到高位并折腕垂指；actual874下一态改为更高斜臂与向上摊掌，不能借下一态手或把09动作照搬。first871..873属同一个PRIORITY状态，首末图像即使微小RGB不同也不机械另造新item，不作整层像素alias/摄影通过。'}]

for row in rows:
    id=row['id'];C=B/'drawings'/id/'v01';R=C/row['run'];selected=registry[id];old=Path(selected['selected_run'])
    jobp=C/'JOB.json';regp=C/'REGISTRATION_PLAN.json';job=read(jobp);state=next(x for x in states if x['id']==id)
    assert job['source_frame']==state['existing_source_canonical_frame']==row['source'] and job['source_pts']==row['pts']
    assert [state['first_frame'],state['last_frame']]==row['first']
    assert [state['first_pts'],state['end_pts']]==row['first_pts']
    assert selected['status']=='repair_required' and selected['sha256']==row['selected_sha'] and sha(selected['image'])==row['selected_sha']
    first_raw=C/'character_api_original.png';receipt=C/'result.json';assert sha(first_raw)==row['first_API_sha']==read(receipt)['output_sha256']
    assert not (R/'character_imggen_original.png').exists() and not (R/'BUILTIN_GENERATION.json').exists()
    source=Path(job['source_image']);guide=C/'inputs/source_pose_guide.png'
    assert sha(source)==job['source_image_sha256']
    refs=[]
    def cp(name,p,role,xy=None):
        out=R/'inputs'/name;assert not out.exists()
        if xy is None:shutil.copyfile(p,out)
        else:
            with Image.open(p) as im:im.crop(xy).save(out)
        item={**rec(out),'source':rec(p),'role':role}
        if xy is not None:item['source_crop_xyxy']=xy
        refs.append(item)
    cp(f"ref1_ORIGINAL{row['source']}_COMPLETE_UNMASKED_POSE_GUIDE.png",guide,'唯一原PV当前动作、共同头身构图、眼口、不同手臂掌/衣腰裙腿鞋和真实底裁。全guide不挖头不移部位；红角色/尖长额发/双高卷不作为本OC身份。')
    cp('ref2_USER_CORRECT11_GRAY_BOB_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png',identity,'OC中性灰短圆润bob/自然灰刘海贴颊侧发及唯一低LEFT双珠身份；完整头卷仅合理相对发量与宽灰前返/渐细C，不复制原眼口/头姿/手body或固定卷轴。')
    cp('ref3_LATEST_USER_BROAD_GRAY_FRONT_RETURN_DETAIL_NO_FACE_ROOT.png',detail,'仅宽GRAY主面/内后返回实际连接/渐细C，薄mutedmint材料带。舍原精修高光暗体积面，不定本root/孤立大小/轴向。',[35,58,146,260])
    assert refs[2]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
    cp('ref4_PURE_UNLIT_GRAY_MINT_KEY.png',palette,'所有bob与灰发带前内背返回统一同gray平涂，mint独立材料条；不作方向打光/体积构造。')
    fifth_source=old/'qa_white.png' if id=='ART-G33-07' else guide
    cp(row['fifth_name'],fifth_source,row['fifth_role'],row['fifth_crop'])
    assert len(refs)==5
    source_prov=H/'cels'/id.removeprefix('ART-')/'PROVENANCE.json'
    assert read(source_prov)['source_frame']==row['source'] and read(source_prov)['source_pts']==row['pts']
    locals_before=[]
    for p in C.glob('*/LOCAL_REPAIR_STATUS.json'):
        snapname='ANCESTOR_BEFORE_'+p.parent.name+'.json'
        locals_before.append({'status_file':rec(p),'status_exact_before':read(p),'private_copy':put(R,snapname,read(p))})
    local_parent=C/'local_hollow_return_gray_api_v01' if id=='ART-G33-07' else None
    evidence_paths=[source,guide,old/'qa_white.png',old/'qa_black.png']
    frame_nums=row['evidence_frames']
    evidence_paths += [B/'coverage/source_frames'/f'F{n:06d}.png' for n in frame_nums]
    motion_path=Path(state['motion_reference_path']);evidence_paths.append(motion_path)
    prov={
        'id':id,'created_utc':now,'refs':refs,'source_full':rec(source),'source_guide':rec(guide),
        'JOB':rec(jobp),'REGISTRATION_PLAN':rec(regp),'source_PROVENANCE':rec(source_prov),
        'canonical_source_frame':row['source'],'canonical_pts':row['pts'],'source_time_base':'1/16000',
        'first_frames':row['first'],'first_pts':row['first_pts'],'PRIORITY_SCOPE':rec(scope_path),'priority_exact_row':state,
        'selected_registry_exact_snapshot':selected,'selected_image':rec(selected['image']),
        'current_PRIMARY':rec(selected['primary_review']),'current_independent_report':rec(selected['independent_review']),
        'user_correction_policy':rec(policy),'assessment_requirements':rec(requirements),
        'saved_first_API':rec(first_raw),'known_first_API_receipt':rec(receipt),'known_API_elapsed_seconds':read(receipt)['elapsed_seconds'],
        'local_ancestors_before':locals_before,'direct_historical_local_repair_parent':str(local_parent) if local_parent else None,
        'actual_read_only_source_selected_neighbor_motion_paths':[rec(p) for p in evidence_paths],
        'source_action':row['action'],'visible_extent':row['extent'],'phase_observation_text_only':row['motion'],
        'source_neighbors_and_no_duplicate_item':row['neighbor'],'repair_reason':row['repair'],'changed_reference_hypothesis':row['hypothesis'],
        'source_original_JOB_REGPLAN_and_policies_not_modified':True,'new_art_pixels_created_or_patched':False,
    }
    put(R,'INPUT_PROVENANCE_AND_REPAIR_CONTEXT.json',prov)
    put(R,'CURRENT_SELECTED_STATUS_SNAPSHOT.json',{'registry_exact_entry':selected,'PRIMARY_exact':read(selected['primary_review']),'snapshot_only_no_central_write':True,'legacy_review_is_not_current_user_acceptance':True})
    prompt='\n\n'.join([
        prefix,
        '人物身份采用图2中性灰短圆润bob女孩：自然灰刘海、贴颊短侧发、唯一人物LEFT低耳后双红珠。图1红发角色/尖长额发侧刺和双高卷不是目标，不只是改色；图1只拥有本帧头身动作、眼口、手衣裙腿与原裁切，图2不得改本动作/眼口。',
        f"这是已有API保存稿{id}的一次完整当前可见人物连贯重绘修复；图1原{row['source']}完整source-first构图为动作唯一依据。"+row['action'],
        '当前近正面/轻侧倾投影，人物LEFT根在画右同耳下缘后方的低bob-nape。红珠从这个低根连续接卷，不高于耳去接眼侧或帽边，不换画左、不镜像头身/手。bob、低根双珠、颈领、cap和肩褶自然衔接，实际遮挡可隐部分根，不能为露全珠或尾尖抬根/拉卷到前臂前。',
        row['specific_prompt']+' 图2整头与肩部上下文核相对体量：不巨粗、不小挂件，也不以孤立局部crop尺寸定发量。图3只宽灰返回连接，不复制高光/暗底。不要固定洞数/圈数/全片轴长，也不能把不透明灰返回面一律挖成洞；真正露出的空气才透明。',
        row['motion'],
        '所有gray短bob与卷的正面/内面/背面/返回都同一无打光灰#B6B4B2，较薄mutedmint#B0C8BA只材料带，墨线#171717；用线与互遮表达绕行，不画重复深灰体积内底/银白亮边/渐变。暖桃肤、原黑白女仆衣/红bow金扣、白cap与两主要黑叶保持，普通小共同帽根不另长第三垂叶。眼睛一种charcoal实色iris+普通小圆白点，开度/视线仅本source，禁止G02半睑模板/黑中心灰环。',
        row['extent']+' 整个人物一次重新画连贯，不局部贴辫子/贴眼/拼衣或代码补底。只输出真实透明可见人物，无粉色背景、字幕、棋盘格、色表或独立物件。'
    ])+'\n'
    prompt_path=R/'prompt_imggen.txt';assert not prompt_path.exists();prompt_path.write_text(prompt,encoding='utf-8')
    request={
        'id':id,'run':str(R),'operation_kind':'whole_character_redraw','existing_saved_API_repair_not_new_FIRST':True,
        'source_first':True,'refs':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],
        'prompt_file':str(prompt_path),'prompt_sha256':sha(prompt_path),'prompt':prompt,
        'tool_arguments':{'prompt':prompt,'referenced_image_paths':[x['path'] for x in refs],'transparent_background':True},
        'transparent_background':True,'whole_character_one_generation':True,'source_frame':row['source'],'source_pts':row['pts'],
        'first_case_frames':row['first'],'source_canvas_guidance':job['output_size'],
        'rejected_current_image':rec(selected['image']),'repair_reason':row['repair'],'changed_reference_hypothesis':row['hypothesis'],
        'local_repair_parent':str(local_parent) if local_parent else None,
        'historical_local_ancestors_whole_done_not_fresh_pass':bool(local_parent),
        'mandatory_whole_redraw_after_local_repair':bool(local_parent),'whole_character_imggen_completed_for_this_request':False,
        'fresh_root_Sol_and_placement_required':True,'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,
        'submitted':False,'PREPONLY':True,'dispatchable_by_artist':False,'native_calls_authorized_this_record':0,
        'planned_native_n_on_future_root_release':1,'API_calls':0,'native_calls':0,'automatic_retries':0,
        'whole_image_not_a_patch':True,'user_accepted':False,'dynamic_validated':False,
    }
    request_record=put(R,'request_imggen.json',request)
    put(R,'LOCAL_ANCESTRY_BEFORE_AND_FRESH_WHOLE_PENDING.json',{
        'id':id,'historical_local_parent':str(local_parent) if local_parent else None,'ancestor_before':locals_before,
        'no_new_local_patch_this_turn':True,'mandatory_visible_whole_requested':True,
        'historical_whole_completion_not_inherited_for_this_candidate':True,'new_whole_completed':False,
        'fresh_review_pending_after_future_whole_return':True,'eligible_for_final_selection':False,
        'no_parent_status_modified':True,'API_calls':0,'native_calls':0,
    })
    print(json.dumps({'id':id,'request':request_record,'prompt':rec(prompt_path),'refs':[{k:x[k] for k in ['path','sha256','size']} for x in refs],'calls':0},ensure_ascii=False))
