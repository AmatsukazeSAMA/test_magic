"""Prepare a coherent whole redraw, without native/API calls or root authorization."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image

run=Path(__file__).resolve().parent
root=next(p for p in run.parents if (p/'image_defaults.json').exists())
base=root/'art/full_character_redraw_1080p_v01'
local=run.parent/'local_api_plate_and_lowroot_scope_refined_api_v04'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p),'sha256':sha(p)}
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,value):
    p=run/name
    assert not p.exists(),f'Preserve existing file: {p}'
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return p

for name in ['request_imggen.json','request_imggen_ROOT_AUTHORIZED.json','character_imggen_original.png',
             'BUILTIN_GENERATION.json','NATIVE_CALL_RECEIPT.json','ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_NATIVE_CALL_RELEASE_v01.json']:
    assert not (run/name).exists(),f'Preserve existing execution: {name}'
refs=[run/'inputs'/n for n in ['ref1_KNOWN_LOCAL_b9fbe360_COMPLETE_RGBA_SOLE_POSE.png',
      'ref2_EAR_LOWBEAD_RELATION_ONLY_NO_CAP_EYES.png','ref3_PURE_UNLIT_GRAY_PIGMENT_ONLY.png']]
expected=['b9fbe360fd4bcaacf8e5098a79e1b74948f8e1cac8b1636f1c00d94b63faf30a',
          'a3db75e3ee1c7e2c9b03f79d24c7433e39f05b40695f84d19f8cf6dfa97bdb72',
          '249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751']
assert [sha(p) for p in refs]==expected
assert sha(local/'character_api_original.png')==expected[0]
result=read(local/'result.json')
assert result['output_sha256']==expected[0] and result['n']==1 and result['elapsed_seconds']==42.236
assert Image.open(refs[0]).size==(1344,1024) and Image.open(refs[1]).size==(41,57)
prefix=read(root/'image_defaults.json')['generation_prompt_prefix']['text']
assert read(root/'image_defaults.json')['generation_prompt_prefix']['enabled'] is True
auth=base/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
requirements=base/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
source=base/'coverage/source_frames/F000507.png'
ledger=base/'coverage/EXPOSURE_LEDGER.json'
timing=[{k:f[k] for k in ['frame','pts','end_pts','duration_ticks']} for f in read(ledger)['frames'] if f['frame']==507]
assert timing[0]['pts']==270672
input_prov=run/'INPUT_AND_DIAGNOSTIC_PROVENANCE_PREPONLY.json'
ip=read(input_prov)
prompt_text=prefix+'''

图1是已经完成局部盘道具清除的完整透明人物，是这次唯一完整动作、人物比例、表情、可见范围和画幅裁切目标。将整个当前实际可见人物一次连贯重绘，保持倒悬近景，不镜像、不翻正、不旋转头身或另换动作；保持约1344×1024的横画幅语境，不拉远变立绘。图2仅是很小的耳后低珠关系示意，图3仅是无打光纯灰色键。只有三张参考，不能用图2替换当前姿态。

本次必须明确改正图1尚未修好的发根。图1画左露耳的图下端，靠头冠方向，现在仍有一颗明显红珠及被bob遮住的另一珠/旧根；它们约在耳的冠端，属于错误位置，不能保留。当前是倒悬头：实际下颌和颈部的方向在图上方，头冠及尖bob在图下方。“低耳后/nape”要沿当前真实头颌轴，在同一可见耳的图上端、靠颌颈的耳后bob接缝重接，不能把屏幕向下的冠端当低根。去掉冠端旧珠和旧根接缝，把同一束灰卷真正接回同侧耳上端的颌颈侧；不要只把耳画大、耳垂拉长或红珠改遮挡，就声称已经纠正根位。不要改动耳本身、脸、眼睛、主体bob头型或头相对灰袖的角度来凑新位置。

新低根可自然位于bob后，红珠可以部分遮住、只露一珠或全部藏住，不强露两颗完整珠。这里的低耳后是沿同一耳颌颈端的局部区域，不是帽端、高冠或固定屏幕点；当前裸头，绝不能加帽子、黑叶或额外头饰。卷的露出路径要从这处同侧低根自然接入头旁，不画额外长S细杆去硬连图1旧第一转或旧C。允许当前卷在原头旁适中窄范围内随新根重新衔接，保留全头语境中的合理发量；既不放成粗巨大卷，也不缩成小挂件。不要为了展示连接而扒开bob、露出隐藏下颌/颈部或画第二束卷。

图1现有灰卷已经能读出单束宽前面、翻回、下一转和末C，这种连续发带结构应保留并自然接到纠正后的根。正面是宽GRAY头发，转入的内侧/背面返回也是实际不透明GRAY头发，再斜向接下一转，逐渐收细成同一灰C。不能拆成封口盖盘、灰碗片、实心锥或堆叠短柱；返回不是mint细线。只在实际露出的空气处保持alpha透明，不删除宽灰返回来强挖孔，不强制圈数、孔数或固定每转大小。薄mint只作窄材料边，不能扩大成绿宽主面或绿C。新根、卷主体和C须一体连接，不留孤立旧珠、小白点或第二条尾。

图1原盘面和独立双盘沿已清除。头上方、前景灰袖与右上抓指之间的原盘遮挡区域继续真实alpha透明，不能再画白盘、黑圆圈、灰楔/盘片或硬物。只保留原实际可见的脸/灰bob/灰袖及手指；人物在原遮挡处的可见边界可以自然简洁收线，但不补出盘后看不见的下颌、嘴、脖颈、胸身、腕臂或手指。右上抓沿手的每个已见分指、指缝、指尖和黑轮廓、左上前景宽松灰袖及袖旁已露暖色皮肤，均按图1保留。灰袖是实体衣服，不是盘；不能挖掉前景袖或手来扩大透明缺口，也不能把抓指连成新隐藏手掌或新腕。

保留原左右不等的圆睁开度和注视、单charcoal平填眼睛及普通小白反光，不能新增黑瞳心、灰色同心环或统一成对称半睑。不新增当前被遮挡的嘴。暖桃肤与原灰松袖色保持，原裁切仍裁到袖和抓手，不补源外身体、腿鞋，不穿女仆领、裙或围裙。只画一个当前可见人物。

将bob、卷宽前面、内/后返回、下一转和末C统一为图3同类的无打光中性GRAY平涂，普通黑线说明结构，薄而柔和的mint作材料细边。图1现有柔和亮暗和C端小亮片不是必须保留的材料：去掉银白高光、白亮闪片、光泽边、深灰独立体积底和明显渐变；不要为了统一灰色而把返回改透明或删掉层次连接。头发形体依靠轮廓与T遮挡表达。

图2只说明同一耳后靠实际颌颈端的低珠接发关系，不提供当前头轴、脸、眼、耳大小、帽、身体或灯光；不能把正立小裁图按像素贴到倒悬头，也不采用它的亮暗。完整人物应连贯重画，保图1透明可见范围，忽略alpha0内隐藏RGB。不生成背景、圆盘、字幕、色板、示意箭头或额外人物。
'''
prompt=run/'prompt_imggen.txt';assert not prompt.exists()
prompt.write_text(prompt_text,encoding='utf-8',newline='\n')
assert prompt.read_text(encoding='utf-8').startswith(prefix)
roles=[r['role'] for r in ip['refs']]
request=save('request_imggen.json',{
    'id':'ART-G07-03','run':str(run),'PREPONLY':True,'dispatchable':False,'root_release_received':False,
    'operation_kind':'whole_character_redraw','transparent_background':True,'whole_character_one_generation':True,
    'existing_saved_API_repair_not_new_FIRST':True,'refs':[str(p) for p in refs],
    'reference_sha256':expected,'reference_roles_in_tool_order':roles,
    'prompt_file':str(prompt),'prompt_sha256':sha(prompt),'prompt':prompt_text,
    'tool_arguments':{'prompt':prompt_text,'referenced_image_paths':[str(p) for p in refs],'transparent_background':True},
    'local_repair_parent':str(local),'local_repair_parent_raw_sha256':expected[0],
    'known_local_intermediate_not_final':True,'mandatory_whole_after_local_repair':True,'new_whole_completed':False,
    'source_frame':507,'source_pts':270672,'source_time_base':'1/16000','source_timing':timing,
    'original_source_is_QA_only_not_tool_reference':True,'annotated_diagrams_not_tool_reference':True,
    'current_pose_is_inverted_same_ear_nape_screen_up':True,
    'must_correct_remaining_crown_end_root_not_inherit_local_attachment':True,
    'planned_canvas_context_pixels':[1344,1024],
    'native_calls_authorized':0,'planned_native_calls_on_future_root_release':1,'native_calls':0,
    'API_calls':0,'HTTP_calls':0,'automatic_retries':0,'user_quality_preference':'high',
    'native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,'native_size_parameter_exposed':False,
    'fresh_root_Sol_and_photography_required':True,'user_accepted':False,'dynamic_validated':False,
    'created_utc':datetime.now(timezone.utc).isoformat()})

qa=run/'readonly_QA'
viewed=[local/'character_api_original.png',local/'qa_white.png',local/'qa_black.png',source,
        local/'inputs/ref3_APPROVED11_EAR_LOWBEAD_RELATION_ONLY_NO_CAP_EYES.png',
        local/'inputs/ref4_PURE_GRAY_PIGMENT_ONLY.png',refs[1],
        *[qa/n for n in ['READONLY_ROOT_EAR_DIRECTION_white_FULL.png','READONLY_ROOT_EAR_DIRECTION_black_FULL.png',
                        'READONLY_ROOT_EAR_DIRECTION_white_LOCAL_3x.png','READONLY_ROOT_EAR_DIRECTION_black_LOCAL_3x.png',
                        'LOCAL_ALPHA_FULL.png','ORIGINAL507_NATIVE_SAMEEAR_CONTEXT_READONLY_2x.png']]]
actual=save('SOL_KNOWN_LOCAL_AND_ROOT_DIRECTION_ACTUAL_PREPONLY.json',{
    'id':'ART-G07-03','status':'MANDATORY_WHOLE_PREP_ONLY_REMAINING_LOCAL_ROOT_DEFECT_NOT_PASSED',
    'actual_viewed_paths':[str(p) for p in viewed],'actual_viewed_evidence':[ev(p) for p in viewed],
    'input1_and3_copies_exact_bytes_of_actually_viewed_sources':True,
    'observations':['New known local removes the plate face and independent dual rim, preserving visible bob contact and original foreground sleeve/grasp fingers.',
                    'Raw black smoky display comes from alpha0 RGB; actual white/black/alpha confirms the cleared center remains transparent, not a background object.',
                    'Gray front/return/next/C path is now readable, but current root remains at crown-end of visible ear. Red-pixel centroid[305.96,571.84], bbox[281,541,332,601]; larger exposed ear is not a corrected low root.',
                    'Required same-ear nape is toward the inverted jaw/neck, screen-up. Cyan diagnostic region only indicates this direction; not a fixed point or hidden-root certification.',
                    'Current bob/coil still has soft value variation and C-end light spot; whole must flatten gray material while preserving opaque returns and real air.',
                    'Three refs remove original fullplate/redtwin competition: current solepose, small lowear relationship, puregray. Diagrams/source are QA-only.'],
    'current_local_static_pass':False,'current_local_root_repair_remaining':True,
    'hidden_geometry_certified':False,'whole_output_exists':False,'actual_dynamic_playback':False,
    'user_accepted':False,'API_calls':0,'native_calls':0,'central_modified':False})
provenance=save('INPUT_PROVENANCE_PREPONLY.json',{
    'id':'ART-G07-03','references':ip['refs'],'diagnostic_provenance':ev(input_prov),
    'source507_QA_only':ev(source),'PTS_read_from':ev(ledger),'source_timing':timing,
    'known_parent_raw':ev(local/'character_api_original.png'),'known_parent_result':ev(local/'result.json'),
    'known_parent_root_receipt':ev(local/'ROOT_API_EXECUTION_RECEIPT.json'),
    'known_parent_elapsed_seconds':42.236,'parent_call_is_not_this_preparation_call':True,
    'project_consent':ev(auth),'current_requirements':ev(requirements),'defaults':ev(root/'image_defaults.json'),
    'mandatory_full_LEFT_prefix_first':True,'refs_only_three':True,
    'ref2_scope':'41x57 unchanged crop from usercorrect11 context[182,143,223,200]; ear-bead relation only, no eyes/cap/body/pose authority.',
    'ref2_original_context_sha256':'216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528',
    'no_original_fullplate_or_redtwins_in_generation_refs':True,
    'no_annotated_overlay_in_generation_refs':True,
    'diagnostic_draw_operations':'Only readonly QA compositing, rectangular crops, nearest enlargement and labelled boxes/arrows; raw artwork and submitted refs never painted/warped/rotated.',
    'qa_artifacts':[ev(p) for p in qa.glob('*.png')],
    'parent_originals_locks_status_and_failed_versions_preserved':True,
    'API_calls':0,'native_calls':0,'central_JOB_REG_binding_modified':False})
status=save('LOCAL_REPAIR_STATUS_READONLY_FOR_THIS_WHOLE_PREP.json',{
    'id':'ART-G07-03','status':'KNOWN_LOCAL_INTERMEDIATE_ROOT_STILL_WRONG_MANDATORY_WHOLE_PENDING',
    'local_repair_performed':True,'result_unknown':False,'known_raw':ev(local/'character_api_original.png'),
    'local_repair_not_final':True,'remaining_root_defect':True,'parent_API_elapsed_seconds':42.236,
    'mandatory_whole_character_redraw_after_local_repair':True,'mandatory_whole_pending':True,'whole_completed':False,
    'next_whole_PREP':ev(request),'fresh_primary_and_independent_review_pending':True,'asset_selectable':False,
    'old_parent_LOCAL_REPAIR_STATUS_not_rewritten':True,'native_calls_authorized_this_preparation':0,
    'API_calls_this_preparation':0,'native_calls_this_preparation':0,'automatic_retries':0,
    'dynamic_validated':False,'user_accepted':False})
lock=save('REQUEST_LOCK_PREPONLY.json',{
    'id':'ART-G07-03','PREPONLY':True,'root_release_received':False,'request':ev(request),'prompt':ev(prompt),
    'refs':[{**ev(p),'role':role} for p,role in zip(refs,roles)],'provenance':ev(provenance),
    'actual_observations':ev(actual),'local_status_readonly':ev(status),
    'native_calls_authorized':0,'native_calls':0,'API_calls':0,'HTTP_calls':0,
    'compatible_release_helper':str(root/'scripts/Release-RootReviewedWholeImggen.py')})
receipt=save('WHOLE_PREPARATION_RECEIPT_PREPONLY.json',{
    'id':'ART-G07-03','status':'MANDATORY_WHOLE_PREPARED_NOT_RELEASED_NOT_CALLED',
    'request':ev(request),'prompt':ev(prompt),'lock':ev(lock),'references':[ev(p) for p in refs],
    'provenance':ev(provenance),'actual_input_observations':ev(actual),
    'root_actual_priority_QA':[ev(qa/n) for n in ['READONLY_ROOT_EAR_DIRECTION_white_FULL.png',
         'READONLY_ROOT_EAR_DIRECTION_black_FULL.png','READONLY_ROOT_EAR_DIRECTION_white_LOCAL_3x.png',
         'READONLY_ROOT_EAR_DIRECTION_black_LOCAL_3x.png']],
    'known_local_result':ev(local/'result.json'),'known_local_raw_sha256':expected[0],
    'root_next_step':'Actually inspect the three exact refs, full prompt and readonly same-ear root-direction diagrams, then separately release ONE builtin whole if appropriate. Fresh root+Sol whole review required; no automatic call here.',
    'API_calls':0,'native_calls':0,'network_calls':0,'central_JOB_REG_binding_modified':False,
    'static_pass':False,'dynamic_validated':False,'user_accepted':False})
report=run/'README_PREPONLY.md';assert not report.exists()
report.write_text('G07-03 / F507 mandatory whole PREP ONLY。\n\n已实际看 known local b9fbe360 完整raw/白黑、原507完整native、三ref对应原件与耳根白黑图示/alpha。盘面与独立双盘沿已基本清，现有GRAY前→返回→下一转→C可读；但珠根仍在露耳冠端，红像素中心约(306,572)，尚未修复。\n\n新整稿必须沿同一可见耳向图上方颌颈端/nape重接；允许bob藏珠，不强露两珠，不放大耳或用长S接回旧根。图示青框只说明方向，不是固定像素或隐藏几何认证。只读图示不进入工具参考。\n\n三ref：1当前局修完整原字节/唯一整姿；2无眼帽的41×57耳珠关系；3纯GRAY材料。原红双卷/完整盘只作实际QA，不输入。保当前倒悬左右不等眼开度、灰袖、抓指及原裁切；不补隐藏嘴颌颈身，不画盘。统一bob/卷/C无光照灰平涂并保不透明返回。\n\nrequest_imggen.json SHA '+sha(request)+'\nprompt_imggen.txt SHA '+sha(prompt)+'\nREQUEST_LOCK_PREPONLY.json SHA '+sha(lock)+'\nWHOLE_PREPARATION_RECEIPT_PREPONLY.json SHA '+sha(receipt)+'\n\n待ROOT实际三ref/全prompt/readonly_QA/READONLY_ROOT_EAR_DIRECTION_*后单独释放。准备不授权调用；0 API/native/network，未改中央、JOB、REG、绑定，也未重写parent局修状态或旧锁。整稿返回后fresh ROOT+Sol、摄影与动态仍待。\n',encoding='utf-8',newline='\n')
print(json.dumps({'request':ev(request),'prompt':ev(prompt),'lock':ev(lock),'receipt':ev(receipt),'report':ev(report),'root_QA':[ev(qa/n) for n in ['READONLY_ROOT_EAR_DIRECTION_white_FULL.png','READONLY_ROOT_EAR_DIRECTION_black_FULL.png','READONLY_ROOT_EAR_DIRECTION_white_LOCAL_3x.png','READONLY_ROOT_EAR_DIRECTION_black_LOCAL_3x.png']],'API_calls':0,'native_calls':0},ensure_ascii=False,indent=2))
