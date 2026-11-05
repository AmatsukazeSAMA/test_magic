from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json
import hashlib
import shutil

HERE=Path(__file__).resolve().parent
B=HERE.parents[3]
PROJECT=B.parents[1]
H=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
    p=Path(p);r={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        with Image.open(p) as im:r.update(size=list(im.size),mode=im.mode)
    return r
def put(r,name,d):
    f=r/name;assert not f.exists(),f
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return record(f)

registry=read(B/'ASSET_REGISTRY.json')
scope=read(B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json')['states']
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
identity=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
palette=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
userpolicy=B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json'
requirements=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
previous_request=B/'drawings/ART-G33-15/v01/whole_imggen_source2365_frontshoulder_continuity_v05/request_imggen.json'
previous15=read(previous_request)
assert previous15['submitted'] is False
assert sha(identity)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
assert sha(detail)=='4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'
assert sha(palette)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'
assert sha(userpolicy)=='fe7f8b650bf4b621bb5aaa0b4d4d6d958809100d4278b6635d74e3a36217e39d'
assert not (previous_request.parent/'character_imggen_original.png').exists()
now=datetime.now(timezone.utc).isoformat()
rows=[
    {
        'id':'ART-G12-20','run':'whole_imggen_source892_frontshoulder_continuity_v05',
        'source':892,'pts':476208,'first':[892,894],'first_pts':[476208,477808],
        'selected_sha':'57171170293fbc210c8b4733d35f8f8f63d6eabec87ac8076556ba42ef834355',
        'expected_API_count':1,'expected_native_count':4,'first_result_relative':'result.json',
        'face_crop':[365,240,535,405],
        'face_name':'ref5_SOURCE892_CLOSED_LASH_PROFILE_NO_IRIS_NO_ROOT.png',
        'face_role':'仅本892闭合睫线/眉弧、鼻颏和不显独立口线的profile表演；无虹膜/白点，不复制身份图正脸大眼。',
        'action':'本原892严格右向profile、闭眼仅睫线/眉弧，鼻/下颏及闭口轮廓依源，不加可读正脸或虹膜。头颈不改成前/背三分之四。可见近侧臂屈回腰后，手被身体/袖口/后腰遮住，远臂与手按原遮挡，不补可见抓裙手。black长袖/黑领、原白肩fan竖frill/袖口、红bow金扣、腰带后bow、白apron/black裙原线和比例保持。白maidcap与画左侧两个黑主叶按原角度，不沿图2正脸帽位置套。',
        'extent':'640x1040完整原892 guide共同布局不移动部位，原只见半身与下apron/黑裙到1080底裁，不加隐藏腿鞋；不是G33-20，不用其闭眼抓裙全身作动作。',
        'route':'用户明确本G12-20卷在肩膀前。右向profile的人物LEFT低根在远耳后/低bob-nape，可被bob/颈遮住；不得在画左可见近耳/后肩新挂珠卷。保持同一LEFT根，发束自然绕同侧肩到身前，当前可见宽卷段落在画右颈肩前轮廓/胸侧，与原白frill/红bow边自然互遮；不能整束照旧垂在画左后肩，也不能全藏掉只留一珠/细绿S。根遮挡可少露双珠，不能为露全抬根到眼侧。头身/衣掌不镜像，不扩大肩frill或改领结来装发。',
        'phase':'实际R48只有近颈压紧/回收的hair相位可参考；其背肩珠卷位置不是当前肩前路线依据，AI身体/闭眼笑与小卷位图均不发。压紧不等于缩固有发量，肩前转译仍按整头肩与正确11判断。',
        'repair':'当前PRIMARY明确用户肩前/相邻连贯重开，旧Sol73保留是历史。旧v04把灰卷压在画左后肩、根被bob挡住；这不能替代用户指定肩前。卷本身有宽gray/mint但上段返回连通仍须fresh看，不把少露/零洞直接叫实心。当前closed profile/腰后手/衣与半身底裁可保；不以旧完整头作生成锚。',
        'eye_prompt':'图5仅本source闭眼profile；只画闭合睫线与源眉，不画虹膜/白点、不补另一只眼或可读笑口。',
        'previous_actual':'ART-G33-15','next_actual':'ART-G33-17',
        'future_dependency':'G33-15新v05尚未生成；其未来通过肩前路由到20的进入方向、露出量与摆幅需实际比图后再定。此请求只有源向+用户肩前的prepared assumption，不称已经连续。',
        'risks':['正脸correct11身份上下文可能把profile转正或补睁眼，故图1+5独占头向闭眼。','低远LEFT根可被挡，但不能把全束隐藏或换近侧画左根。','15没有返图，肩前路由和体量的逐帧承接尚待实际检查。'],
    },
    {
        'id':'ART-G33-17','run':'whole_imggen_source2374_twoleaves_frontshoulder_returns_v04',
        'source':2374,'pts':1267408,'first':[895,898],'first_pts':[477808,479952],
        'selected_sha':'ddcb5327f416ad04f10ddfdc1bd2d8644f69a12c4506ba118671fbbf83f7f240',
        'expected_API_count':2,'expected_native_count':0,'first_result_relative':'first_api_source2374_user11_fullcontext_v02/result.json',
        'face_crop':[292,146,403,226],
        'face_name':'ref5_SOURCE2374_OWN_ROUND_OPEN_EYES_TINY_CLOSED_SMILE.png',
        'face_role':'仅本2374左右不对称圆睁弧/iris露出视线和小闭弧笑；不送G02半睑或灰环眼，不贴入艺术像素。',
        'action':'原2374头向画右的正面三分之四，两眼圆睁且视线/睫弧不对称，小闭弧笑，不借前892闭眼。画左可见近臂折回腰后，白袖口/后腰接触和隐藏指节按源；另一臂手受躯干遮挡，不补可读腰手或抓裙手。原黑长袖黑领、白肩fan竖frill、红bow金扣、腰后bow每条尾带、斜向白apron/黑裙摆均保持。双腿交错，后脚与前脚不同角度及踝带低跟鞋均依原完整可见轮廓。白maidcap只有源中两片主黑叶，位置与互遮按本2374，不抄当前三叶或图2帽角。',
        'extent':'624x1072原guide保canonical2374全部可见裙腿和两只完整鞋，鞋端不按后238?态底裁截掉。first895..898是放大半身曝光，不能据其没见鞋把canonical下身裁掉；不缩手脚或改裙长来让卷露全。',
        'route':'本右向front3/4，画左可见近耳为RIGHT，不能给它珠卷；唯一LEFT低根在画右远耳后/低bob-nape，按自然遮挡接同一肩前胸侧发束。保持当前已修正确的低远根和肩前趋势，不让珠挂在卷中段或另长高bob根。承接15→20→17同一发束，随本转正投影自然绕到画右胸侧，但不复制旧15后背垂挂或旧20近后肩路径。不能换边/镜像/强露全部根尾或抹掉整束。',
        'phase':'实际R50只低颈侧更回收、部分卷被bob/肩frill挡住的hair相位，不能沿AI的小隐藏段缩卷或更改原圆睁/小笑/腰后手。这里不喂AI位图；原2374本body与完整双鞋为唯一动作依据。',
        'repair':'当前PRIMARY与Sol129明确三片独立黑帽叶P1，必须恢复源两片；已修正确的画右远LEFT低根/肩前方向、原眼笑/腰后手/双完整鞋应保。上端几处gray面规则圆钝、入口出口可读性OPEN，并非Sol129已认证完整卷，也不伪称其以不透明gray/零孔判P1。旧wrong-near-root首API与当前三叶整头都不作生成模板。',
        'eye_prompt':'图5只本2374圆睁开度/视线与tiny闭弧笑，iris只一种charcoal实色+普通小圆白点；不变半睑，不画灰环/黑中心双层。',
        'previous_actual':'ART-G12-20','next_actual':'ART-G33-18',
        'future_dependency':'真正前邻是G12-20(first892..894)，不是机械family16；20肩前修复尚未返回，且其前15v05也未生成。当前仅保本17已知正确LEFT远根/肩前趋势，具体相邻位置/摆幅须15和20新返图后核，不认证连续。',
        'risks':['两帽叶不能被身份图角度或当前三叶整头诱导为第三独立叶。','上段宽返回仍需新图实际看入口/出口，不靠孔数判定。','20/15没有新通过返图，肩前路线逐帧承接未认证。'],
    },
]

for row in rows:
    id=row['id'];C=B/'drawings'/id/'v01';R=C/row['run']
    (R/'inputs').mkdir(parents=True,exist_ok=True)
    assert not (R/'request_imggen.json').exists()
    selected=registry[id];job=read(C/'JOB.json');state=next(x for x in scope if x['id']==id)
    assert selected['status']=='repair_required' and sha(selected['image'])==selected['sha256']==row['selected_sha']
    assert job['source_frame']==state['existing_source_canonical_frame']==row['source'] and job['source_pts']==row['pts']
    assert [state['first_frame'],state['last_frame']]==row['first']
    assert [state['first_pts'],state['end_pts']]==row['first_pts']
    original=Path(job['source_image']);guide=C/'inputs/source_pose_guide.png'
    assert sha(original)==job['source_image_sha256']
    api=[];native=[];unknown=[]
    for f in C.rglob('attempt.json'):
        attempt=read(f);e={'attempt':record(f),'status':attempt.get('status'),'exact':attempt}
        if attempt.get('status')!='completed':unknown.append(e)
        else:
            raw=Path(attempt['image']);result=f.parent/'result.json'
            if not raw.exists() or sha(raw)!=read(result)['output_sha256']:unknown.append(e)
            else:e.update(raw=record(raw),result=record(result),known_saved=True)
        api.append(e)
    for f in C.rglob('BUILTIN_GENERATION.json'):
        obj=read(f);raw=Path(obj['output_path']);e={'receipt':record(f),'local_repair_parent':obj.get('local_repair_parent')}
        if not raw.exists() or sha(raw)!=obj['output_sha256']:unknown.append(e)
        else:e.update(raw=record(raw),known_saved=True)
        native.append(e)
    locals_found=[{'file':record(f),'exact':read(f)} for f in C.rglob('LOCAL_REPAIR_STATUS.json')]
    ancestry={'id':id,'API_attempts':api,'saved_native':native,'local_ancestors':locals_found,'unknown_records':unknown,'new_calls':0,'whole_API_repair_is_not_masked_patch':id=='ART-G33-17'}
    put(R,'KNOWN_HISTORY_AND_ANCESTRY.json',ancestry)
    if unknown:
        put(R,'STOP_UNKNOWN_NO_REQUEST.json',{'id':id,'reason':'Unknown prior result requires recovery before new preparation','calls':0})
        print(id,'STOP_UNKNOWN');continue
    assert len(api)==row['expected_API_count'] and len(native)==row['expected_native_count'] and not locals_found
    assert all(not e['local_repair_parent'] for e in native)
    refs=[]
    def cp(name,source,role,xy=None):
        target=R/'inputs'/name;assert not target.exists()
        if xy is None:shutil.copyfile(source,target)
        else:
            with Image.open(source) as im:im.crop(xy).save(target)
        e={**record(target),'source':record(source),'role':role}
        if xy is not None:e['source_crop_xyxy']=xy
        refs.append(e)
    cp(f'ref1_ORIGINAL{row["source"]}_COMPLETE_UNMASKED_SOURCE_GUIDE.png',guide,'原PV唯一动作/构图/头向/眼口/手衣/cap两叶/真实可见下裁，不挖头不移部件。红发尖长额发/双高卷不是OC身份。')
    cp('ref2_CORRECT11_GRAY_BOB_HEAD_COIL_RELATIVE_VOLUME_CONTEXT.png',identity,'只OC中性灰短圆润bob/自然灰刘海/贴颊侧发与合理整头卷体量、连续宽gray返回/C；不复制原眼口/帽叶投影/pose/body或固定axis/root屏幕位置。')
    cp('ref3_USER_GRAY_FRONT_INNER_BACK_RETURN_NEXT_TURN_DETAIL.png',detail,'仅宽GRAY前面→不透明内后返回→下一圈→渐细C的连续构造、薄mutedmint材料；不取精修打光/深暗体积，不定root/孤立大小。',[35,58,146,260])
    assert refs[2]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
    cp('ref4_PURE_UNLIT_GRAY_MINT_MATERIAL_KEY.png',palette,'所有bob/coil前内背返回同一gray平涂，mint仅薄材料带，非明暗/方向色/几何模版。')
    cp(row['face_name'],guide,row['face_role'],row['face_crop'])
    prompt='\n\n'.join([
        prefix,
        '主角换成图2的中性灰短圆润bob女孩：自然灰刘海、贴颊短侧发、唯一LEFT低耳后双红珠，不是把图1红尖额发/侧刺和双高卷仅改灰。图1完整原PV拥有所有动作、头向/眼口、cap两叶、衣手及真实裁切；图2只身份与整头卷相对体量，不得改本表演。',
        f'这是已保存API稿{id}的一次完整当前可见人物连贯重绘；source-first按原{row["source"]}。'+row['action'],
        row['route'],
        '同一宽GRAY发带起卷前面向内/后翻回，opaque返回实际接入下一圈，再自然渐细到末C；上段也要有连续入口/出口，不是封口椭圆帽盘/实心锥柱外贴mint螺线。gray前/内/背/返回面不透明，只有真实露出的空气透明，不把gray返回一律挖成洞；无固定孔数/圈数/长轴。整头肩上下文定合理体量，不巨粗、不micro挂件；真实bob/肩/frill遮挡可隐部分，不能硬拉全尾或靠缩发避错。',
        row['phase'],
        row['eye_prompt']+' 所有gray短bob与卷front/inner/back/return同无打光灰#B6B4B2，较薄mutedmint#B0C8BA只是材料带；黑简笔线#171717/暖桃肤。没有独立银白亮边、渐变或深gray体积内底，不把宽gray主体全改mint。',
        row['extent']+' 整个人物一次连贯重新绘制低根/头颈/cap/肩前发带/衣手，不贴卷贴眼或拼部件、不代码涂改成品；输出真实透明人物，无粉色字幕背景/棋盘/色卡/额外道具或第二束卷。'
    ])+'\n'
    promptfile=R/'prompt_imggen.txt';assert not promptfile.exists();promptfile.write_text(prompt,encoding='utf-8')
    future={'enabled_in_current_payload':False,'future_replace_slot_index_1_based':5,'current_slot':record(refs[4]['path']),'candidate_not_yet_available':row['previous_actual'],'replacement_scope':'Only future fresh-reviewed predecessor LOW-LEFT-root to FRONT-shoulder crop if needed; exclude its body/face/cap/incorrect coil. Keep own source guide action authority.','requires_new_immutable_request_and_root_release':True,'never_append_sixth_native_ref':True,'no_unseen_predecessor_pixels_or_claimed_pass':True}
    request={
        'id':id,'run':str(R),'operation_kind':'whole_character_redraw','existing_saved_API_repair_not_new_FIRST':True,'source_first':True,
        'refs':[e['path'] for e in refs],'reference_sha256':[e['sha256'] for e in refs],'prompt_file':str(promptfile),'prompt_sha256':sha(promptfile),'prompt':prompt,
        'tool_arguments':{'prompt':prompt,'referenced_image_paths':[e['path'] for e in refs],'transparent_background':True},
        'transparent_background':True,'whole_character_one_generation':True,'source_frame':row['source'],'source_pts':row['pts'],'first_case_frames':row['first'],'source_canvas_guidance':job['output_size'],
        'repair_of_selected':record(selected['image']),'repair_reason':row['repair'],
        'changed_reference_hypothesis':'完整未挖头ownsource独占动作，排除当前错误后肩卷/三帽叶整头锚和AIbitmap；correct11完整上下文+latestgraydetail重建宽返回，key只颜料，本源眼口第5张防身份表情竞争。移除错误锚是否有效待验，不宣称已证实内部原因。',
        'user_front_shoulder_policy':record(userpolicy),'prepared_route_assumption':row['route'],'continuity_dependency_not_resolved':row['future_dependency'],
        'previous_actual_state_id':row['previous_actual'],'next_actual_state_id':row['next_actual'],'true_first_dance_order':['ART-G33-14','ART-G33-15','ART-G12-20','ART-G33-17'],
        'G33_15_new_v05_request_only_no_generated_output':record(previous_request),'future_replace_slot':future,
        'local_repair_parent':None,'new_operation_is_not_a_local_patch':True,'masked_local_ancestor_found':False,
        'mandatory_whole_character_redraw_for_repair':True,'whole_character_completed_for_this_request':False,'fresh_root_Sol_photography_and_temporal_review_required':True,
        'PREPONLY':True,'submitted':False,'dispatchable_by_artist':False,'native_calls_authorized':0,'native_calls_authorized_this_record':0,'planned_single_native_after_future_root_release':1,
        'API_calls':0,'native_calls':0,'automatic_retries':0,'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,
        'user_accepted':False,'static_pass':False,'dynamic_validated':False,'risks':row['risks'],
    }
    put(R,'request_imggen.json',request)
    neighbor_records=[]
    for nid in ['ART-G33-14','ART-G33-15','ART-G12-20','ART-G33-17']:
        nr=registry[nid];nrun=Path(nr['selected_run'])
        neighbor_records.append({'id':nid,'registry_exact':nr,'qa_white':record(nrun/'qa_white.png'),'qa_black':record(nrun/'qa_black.png'),'used_as_generation_reference':False,'current_actual_viewed':True})
    evidence=[original,guide,Path(selected['image']),Path(selected['selected_run'])/'qa_white.png',Path(selected['selected_run'])/'qa_black.png']
    evidence += [B/'coverage/source_frames'/f'F{n:06d}.png' for n in [888,889,891,892,894,895,898]]
    evidence += [H/'cels/G33-14/source.png',H/'cels/G33-15/source.png',Path(state['motion_reference_path'])]
    put(R,'INPUT_PROVENANCE_AND_PREPARED_ASSUMPTIONS.json',{
        'id':id,'created_utc':now,'refs':refs,'JOB':record(C/'JOB.json'),'REGISTRATION_PLAN':record(C/'REGISTRATION_PLAN.json'),
        'source_full':record(original),'source_guide':record(guide),'source_PROVENANCE':record(H/'cels'/id.removeprefix('ART-')/'PROVENANCE.json'),
        'source_frame':row['source'],'source_pts':row['pts'],'source_time_base':'1/16000','priority_exact_row':state,
        'source_action':row['action'],'source_extent':row['extent'],'source_route':row['route'],'AI_phase_observation_text_only':row['phase'],
        'current_SELECTED':selected,'current_PRIMARY':record(selected['primary_review']),'current_independent':record(selected['independent_review']),
        'user_policy':record(userpolicy),'current_assessment_requirements':record(requirements),
        'known_history_and_ancestry':record(R/'KNOWN_HISTORY_AND_ANCESTRY.json'),'actual_evidence_paths':[record(f) for f in evidence],
        'neighbor_current_actual_views_not_template':neighbor_records,'G33_15_new_request_only':record(previous_request),'G33_15_new_art_exists':False,
        'route_prepared_assumptions':row['future_dependency'],'future_replace_slot':future,'risks':row['risks'],
        'old_wrong_G33_15_and_G12_20_back_coil_not_route_baseline':True,'G33_20_not_G12_20':True,
        'all_old_images_reviews_requests_untouched':True,'new_art_pixels_created':False,'API_calls':0,'native_calls':0
    })
    print(json.dumps({'id':id,'request':record(R/'request_imggen.json'),'prompt':record(promptfile),'refs':refs,'calls':0},ensure_ascii=False))
