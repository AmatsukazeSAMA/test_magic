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

rows=[
    {'id':'ART-G33-07','source':2333,'pts':1245520,'first':[861,862],'first_pts':[459664,460720],
     'run':'whole_imggen_source2333_upperreturn_lowerC_v13',
     'selected_sha':'128d9e7ae103f5904b4a2a13cdbb817661595c93522a3cc12d4a0b482fd4f3b3',
     'first_API_sha':'6cdd55fdc5ad107fb94eae56a81ff7bfec3c652a7844288fb7323686f9fc1c74',
     'fifth_crop':[765,436,816,481],
     'fifth_name':'ref5_USER_CONFIRMED_V11_LOWER_C_PATH_ONLY_NO_HEAD_ROOT_UPPER.png',
     'fifth_role':'仅用户确认下端正确的末C回钩路径，来自当前v11白QA裁[765,436,816,481]；无头/珠/root/错误上端。绝不复制其暗灰内底、宽mint颜色分区或把51x45孤立裁图当整束体量/轴长。',
     'action':'原2333较近正面、轻侧倾头，双眼圆睁且左右睫弧/视线不同，极小中性短闭口，不加笑。画左臂折向腰后，另一长臂斜跨身体到画左下，低手原分指/拇指轮廓保留；不是下一08近竖下垂臂，也不是前860双手胸前曲指。原白肩fan/竖褶/袖口、black长袖、红bow金扣、腰带/后bow、倾斜apron锯齿边/黑裙和抬起后腿/前腿交错姿保持。',
     'extent':'canonical2333后抬脚可见完整鞋，前景脚鞋末端在原1080底边截断；624x1072原guide对应保原平切，不为补圆鞋尖缩人/抬人。first861..862是放大半身曝光，不拿它裁掉canonical已见裙腿，也不称本输出已完成曝光定位。',
     'motion':'已实际看R22完整图，唯一LEFT卷从低耳颈向画右外甩、近横向而略回弯；仅作为弹性相位文字，不发送其小型封口卷/半睑笑脸/身体位图。原2333仍唯一动作/眼口。',
     'repair':'用户对精确v11说“钻发下端对了上端还是错的”；Sol128与当前PRIMARY均repair_required。上端靠珠的灰椭圆帽面和上中粗圆段缺清楚前面→内后返回入口/出口；另有重复深灰返回体积暗面。当前v11大小较v10明显收回、低LEFT根/外甩方向与下C有可保范围，不重新放大、不缩成挂件；v10巨大发量和v12失败上端均不可当正模板。',
     'hypothesis':'从原完整2333动作guide重建整个人物，不继续edit错误07完整头/帽片卷，不再输入v10/v11/v12整头或旧07高根QA。正确11完整头卷只给OCgraybob与合理相对体量；最新graydetail给连续宽灰前返；第5仅保用户确认的末C路径。此举检验移除错误上端几何竞争是否改善连接，是待验证参考假设，非内部原因已证实。',
     'specific_prompt':'上端宽灰发带从双红珠下连续伸出，先弯成灰前面，再向内/后翻回接入下一圈，入口和出口清楚，不做独立灰椭圆盖盘。后段逐圈收细并保图5用户确认的自然末C回钩。图5仅这一小段路径，不是整卷大小/暗面材料模板。保已收回的合理头肩相对体量和本态向画右外甩回弹，不能回到v10巨卷或v09封口盘堆。',
     'neighbor':'actual860双手在胸前曲指、头更倾且半睑；861/862换成本2333圆睁与跨身长臂，不能沿860表演。后863/866换08长臂近竖下垂/掌在裙前，coil由外甩进入颈肩回收。861/862为同一源态曝光，不能机械另造两新人物项。',
    },
    {'id':'ART-G33-08','source':2334,'pts':1246048,'first':[863,866],'first_pts':[460720,462864],
     'run':'whole_imggen_source2334_gray_connected_spiral_v05',
     'selected_sha':'663617241b31f5a39f5c6a5bae101639c6b90d5af42c98143e4bb3a3b4a71052',
     'first_API_sha':'010a6071bbbc0eb4df535d3355e9b599ef1b49b757944c53a44046351cef041a',
     'fifth_crop':[260,163,395,250],
     'fifth_name':'ref5_ORIGINAL2334_OWN_ROUND_OPEN_EYES_TINY_NEUTRAL_MOUTH.png',
     'fifth_role':'只本2334圆睁不对称眼弧/虹膜露出/视线与极小中性闭口。不得沿正确11或AI眼口，不送G02半睑bitmap，不能贴到艺术稿。',
     'action':'原2334近正面略侧倾，双眼圆睁、极小中性闭口；画左臂折向腰后，另一长臂从画右肩近竖直下垂，掌停在apron下部/黑裙前，原并指间线和外分拇指保留。不是07斜跨身下掌，也不是下一867斜向外伸摊掌。原black长袖、白袖口和肩frill、红bow金扣、腰带后bow/长apron锯齿边/黑裙、交叉小腿和前后鞋可见段均按2334。',
     'extent':'原2334前景脚鞋端在1080底裁截断，后脚仅原露出部分；不得沿当前v04补完圆toe，不能缩人/上移去把未见鞋尖露全。624x1072原guide保持源共同比例与下裁。first863..866为同态放大半身，不能用首段裁去canonical可见裙腿。旧Sol86逆uniform诊断只说明补尖可在原视窗外，不是源完整toe认证或当前发型接受。',
     'motion':'已实际看R25全图，本时段卷靠低耳/颈肩压缩下收，区别R22向外较横弹；只文字相位，不输入R25实心卷或其斜外伸手/body。源2334手仍近竖下垂，不跟AI或后867改手。',
     'repair':'current registry repair_required来自用户明确点名母帧2334卷形错误；PRIMARY和Sol86旧retained仍是历史记录，不伪写成Sol86当时失败。当前v04灰/mint闭合弧面叠成封口渐尖锥体，缺宽灰前返实际连通与末C；低LEFT根基本正确，仍不能因旧材料静态pass当完整卷母参。',
     'hypothesis':'不再用旧v04整个封口锥头作edit target，也不重复两ref纯材质策略；换完整原2334动作source-first，正确11完整灰bob/卷体量和最新grayreturndetail重建同一条连续宽灰发带，纯key统一无光。第五张是本source眼口裁图。移除旧封口几何竞争是否有效待返图验证，不称已证明模型内部原因。',
     'specific_prompt':'低LEFT双红珠下只有同一条宽灰发带，前面翻回内/后返回再接下一圈，沿本态颈肩紧收并自然渐尖C。上中下都必须连成绕行，不是实心锥外贴薄荷螺线或一串封闭椭圆圆盘。肩frill/bob会真实挡住部分，按遮挡画，不为露全C硬拉到肩褶/手臂前；不能缩成微型绿挂件。',
     'neighbor':'actual861/862的07是斜跨身长臂与抬后腿；863..866本2334长臂近竖下垂、掌在裙前，腰/裙和腿重心不同。actual867下一态已改手向外摊，但只是后邻观察，不准备09或复制其动作。863/866原画态相同，仅曝光延续不造重复item。',
    },
]

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
    frame_nums=[860,861,862,863,866] if id=='ART-G33-07' else [861,862,863,866,867]
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
