from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

R=Path(__file__).resolve().parent
B=R.parents[1]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def put(name,d):
    p=R/name;assert not p.exists(),p
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rec(p)

m=read(R/'READONLY_INPUTS_AND_QA_MANIFEST.json')
corrected=read(R/'COMPLETE_CONTEXT_PANELS_v02.json')['panels']
overview=read(R/'FRESH_SEQUENCE_BOARD_OUTPUTS.json')['boards']
now=datetime.now(timezone.utc).isoformat()
live=read(B/'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json')
liveby={r['source_frame']:r for r in live['frames']}
live_registry=read(B/'ASSET_REGISTRY.json')
for state in m['states']:
    id=state['id'];assert live_registry[id]['sha256']==state['exact_current_bound_master']['sha256']
    assert sha(state['exact_current_bound_master']['path'])==state['exact_current_bound_master']['sha256']
    assert sha(state['exact_current_bound_layer']['path'])==state['exact_current_bound_layer']['sha256']
    for before in state['all_exposure_binding_entries']:
        n=before['source_frame'];a=before['actual_selected_asset_binding'];b=liveby[n]['actual_selected_asset_binding']
        for key in ['id','master_sha256','layer_sha256','layer_1080','scale','translation']:assert a[key]==b[key]
for e in m['all_original_source_frames']:assert sha(e['path'])==e['sha256']
for e in corrected:assert sha(e['panel']['path'])==e['panel']['sha256']

actual=[]
for e in m['new_source_contacts']:
    actual.append({**e,'view_mechanism':'Opened this new original-resolution contact PNG with view_image; every cell inspected. Source fullframe cell640x360 uniform1/3; not all45 native-full1x.'})
for e in corrected:
    actual.append({**e['panel'],'view_mechanism':'Opened exact new v02 source/current comparison; fullframe960x540 uniform0.5 and identical fixed[500,60,1450,760] source/current1x context. No part recenter/warp.'})
for e in m['new_black_context_contacts']:
    actual.append({**e,'view_mechanism':'Opened new black alpha context contact at original resolution; all10 bound-layer head/root/shoulder contexts inspected at file1x.'})
for e in overview:actual.append({**e,'view_mechanism':'Opened new temporal source/current sequence overview; entire1080 layers uniformly thumbnailed, only QA matte.'})
actual.append({**m['prior_5stage_board_reference_only'],'view_mechanism':'Opened independently this turn as historical5stage reference only; did not inherit its prior root actual-view statements.'})
viewlist=put('ACTUAL_VIEW_LIST.json',{
    'reviewer':'xhigh_pending_artist independent new read-only static continuity audit','completed_utc':now,
    'new_actual_viewed_PNGs':actual,'all45_source_frames_inspected_as_contact_cells':m['all_original_source_frames'],
    'all10_exact_bound_layers_inspected_through_verified_derivatives':[s['exact_current_bound_layer'] for s in m['states']],
    'original_fullframe_at_native1x_for_all45_claimed':False,'unseen_canonical_cel_files_not_claimed_actually_viewed':True,
    'no_old_actual_view_claims_reused':True,'video_playback_performed':False,'generation_calls':0
})

findings=[
    {'source_phase':'低位/外下','target':'当前卷从画右远侧低珠向下，后段被前手/白frill挡住。作为54低位前态可读；不把原近侧红卷位置照搬到目标ROOT。','root':'可见双珠在低耳后/下bob，未升到眼侧。','structure':'可见gray宽前返和mint边；下段遮挡，完整C/内部拓扑不认证。','size':'小可见包络主要来自颈肩/手遮挡，未据此认证固有发量。'},
    {'source_phase':'1058已开始近水平外上','target':'当前55灰宽带从低根向画右外上折起，末C外露；相对54的下垂已改变，未等到56才开始上扬。其C钩末端仍可下卷，不能只量C最低点否定整束外上。','root':'根仍贴低bob/nape；抬高的是卷体/返回面而非把双珠推到太阳穴。','structure':'宽灰面向内返、下C与实际露空可读，gray返回仍opaque。','size':'相对54露出更多宽gray面是打开/上提后包络，不见立即可定巨大或tiny的错误。'},
    {'source_phase':'1062..1066继续外甩上提','target':'当前56整卷继续外上打开，主灰带较伸展，末C回钩。不是54垂挂复制，也未改原高手OK/胸前手及收眼波口。','root':'双珠仍在画右低耳颈侧，灰带从此处弯起，不随尾端一起抬根。','structure':'宽前面/侧返回/末C连续可读，不能将opaque灰面挖成洞。','size':'横向包络较55大，56→57包络回收明显，需播放检验弹性体量是否过快收缩。'},
    {'source_phase':'1067..1070转外下摆','target':'当前57由56的外上改为较竖下收、末C回勾；源也明确改为向外下，反向本身不是无依据轴跳。头肩上移与发尾下摆可同时发生。','root':'低远LEFT根仍附下bob/nape，不因body上移误说ROOT上窜。','structure':'上端压紧较规则，gray前返与末C部分可见；上段完整入口出口不认证。','size':'外露包络明显小于56，部分来自投影/压紧；仅静图不足断言固有发量守恒或P1缩水。'},
    {'source_phase':'1071..1074下摆减小/抬回','target':'当前58上段更贴颈肩、前手/白frill挡住下段，保源新张口。与57相比可读为回收/抬回的兼容投影，但下C被挡，不能认证精确发梢升高轨迹。','root':'低珠相对下bob/耳颈位置保持，没有借遮挡换近侧根。','structure':'可见宽灰返回保留；隐去末C不是缺失或实心的充分证据。','size':'57→58露出量变化需实际播放复核，不能把被挡部分等同固有发量消失。'},
    {'source_phase':'1075..1078近水平外甩','target':'当前59从颈侧向外较水平伸展，末C可见，非继续抄58下垂。原张口/不对称双手与body转向保持。','root':'根大部被bob遮住，仅能核颈侧同束连接与画左近耳无新双珠；隐藏根不认证。','structure':'宽gray前返回/C可见，部分返回被自身面挡，不因少孔单独判坏。','size':'横包络比58露出段大，59→60会换回长向下包络，需播放检验惯性过渡，不能以画布横向位移替代发轴判断。'},
    {'source_phase':'1079..1083重新向下回收','target':'当前60宽灰发带向下延到前臂/胸前手后、末C在外侧露出，满足源此态下摆；字幕换页/人物横向位置变化不是新的ROOT换边。','root':'低双珠保持画右下bob；无近侧画左新根。','structure':'宽前返沿原手/袖/frill自然互遮，未以整尾强穿前手。','size':'下向包络比59横向更长；转向/自然露出可解释一部分，未据静态认证逐帧体量守恒。'},
    {'source_phase':'1084..1087向外下/转正，手式改变','target':'本33-57原高OK已松开为向画右展开双掌，圆睁开口。当前发束贴画右颈肩下收，后段被前掌/白cuff/frill挡住，没有冻结60手形。','root':'低远侧根仍在同一LEFT下bob，部分珠被发挡住允许。','structure':'宽gray返回压紧并延到真实遮挡后；隐藏尖C不可认证。','size':'露出段较60少，遮挡/转正投影影响显著；不把ROI小直接评为micro固有发束。'},
    {'source_phase':'1088..1092更正面/外下，改不同双掌与闭口','target':'当前33-58更近正面，保持源一低垂分指/一高摊掌、闭小波口。唯一LEFT卷在画右低耳下沿肩侧下垂，部分在肩frill后，末C外露；没有继续单调上扬。','root':'从前3/4转正后画右低耳珠关系更直接可读，无新高根。','structure':'上中下GRAY连续前返与渐细C存在，部分绕面/空气与白肩布需两底区分；不是全卷几何master。','size':'可见长度较33-57增加但头肩转正/遮挡放开；未见明显巨大扩张，具体包络连续仍待播放。'},
    {'source_phase':'1093..1097低垂，用户F1094肩前','target':'当前63已转正，宽GRAY卷落在画右肩前/胸侧、白肩frill前，逐细到C；保持本源双侧不等高掌与小闭笑。用户F1094肩前要求静态可见。','root':'低LEFT根在画右下bob/耳后，珠可部分互遮，不换根或镜像。','structure':'宽前返与末C可读，softgray和线法仍不是逐像素同灰/隐藏拓扑认证。','size':'与33-58相比外露宽面/长度有变化，但未见一眼可定巨大/微型的突变；前肩路线在实际1092→1093播放仍需核。'},
]
state_findings=[]
for row,f in zip(m['states'],findings):
    state_findings.append({
        'id':row['id'],'frames':[row['first_frame'],row['last_frame']],'canonical_source_frame':row['canonical_source_frame'],
        'first_pts':row['first_pts'],'end_pts':row['end_pts_exclusive'],
        'bound_layer':row['exact_current_bound_layer'],'bound_master':row['exact_current_bound_master'],
        'observed_source_phase':f['source_phase'],'new_current_static_observation':f['target'],
        'low_LEFT_root_assessment':f['root'],'broad_gray_return_and_C_readability':f['structure'],'visible_volume_assessment':f['size'],
        'verdict':'static_observation_only_no_new_artistic_approval','new_P1_asserted':False,'dynamic_validated':False
    })

open_points=[
    {'severity':'OPEN_TEMPORAL_VOLUME','transition':'G12-56→57','observation':'外上展开到下收压紧的可见包络变化较大；原相位明确反向，不能仅凭静图说轴跳/固有发量缩水，也未证明播放平顺。','next_check':'按真实PTS原速/慢放并肩比头肩相对包络及返回路径，不重绘直到root实际判断。'},
    {'severity':'OPEN_OCCLUDED_TIP','transition':'G12-57→58','observation':'58下C被原前手/白褶挡住，静态只能核上段回收/抬回兼容性，不能测隐藏尖端轨迹。','next_check':'播放核相位和遮挡边连续，不强拉全尾前置。'},
    {'severity':'OPEN_TEMPORAL_VOLUME','transition':'G12-59→60','observation':'横向大包络切到下向长包络、body/歌词页面亦变化；原源下摆依据成立，发束内在体量是否跳变仍未动态认证。','next_check':'同一首段真实定位下播放，分离整人平移/头转和局部发摆。'},
    {'severity':'OPEN_ROUTE_CONTINUITY','transition':'G33-58→G12-63','observation':'63肩前要求已可见，之前一态部分在肩frill后；转正遮挡切换是否自然只能动态复核。','next_check':'1092→1093按真实PTS查看，ROOT固定、不能靠加长/换侧解释。'},
    {'severity':'OPEN_STRUCTURAL_MASTER','transition':'54/57/58及33-57遮挡上段','observation':'规则gray回面/自身遮挡不能单凭零孔判坏，但本次不认证完整上端入口出口或全卷master；soft材料逐像素单色也未认证。','next_check':'后续如用户点名具体P1，fresh原样回图与两底局部复核，不能以本报告充当全片卷形通过。'},
]
report={
    'schema':'magic-maid.readonly-bound-static-continuity/1','reviewer':'xhigh_pending_artist independent fresh actual-view','completed_utc':now,
    'scope':{'frames':[1053,1097],'source_frame_count':45,'drawing_state_count':10,'time_base':'1/16000','start_pts':562160,'end_pts_exclusive':586192,'duration_s':1.502},
    'decision':'F1058_upswing_observed_static_no_new_definite_root_phase_P1_temporal_and_volume_certification_open',
    'main_findings':[
        '当前55不是沿54垂挂冻结：F1058已外上回折，56继续外上，57下摆，58回收/抬回兼容投影，59水平，60再下收。不能把全段解释成单调上扬。',
        '可见低LEFT根不随尾部外上抬到眼/太阳穴，转正后仍在画右低耳bob；隐藏根及末C不能认证。',
        '63当前肩前宽GRAY卷/C已可见；未把前一态肩后布遮挡当所有状态固定规则。',
        '未发现本次可立即定为跨态换根/无源轴向跳跃的新P1；这不等于新静态通过、用户接受或体量/播放通过。'
    ],
    'sources_are_action_authority':True,'original_near_red_motion_is_phase_only_not_target_root_or_mirror_template':True,
    'source_exposure_vs_action':{
        'all45_contact_observation':'每状态首/中/末在接触表级未见新增眼手衣动作；不同state有头倾、眼口、手型与发phase变化，非仅统一平移的重复人物。',
        'binding_code_fact':'每state覆盖帧使用相同精确1080层SHA、scale与translation，没有逐帧独立层平移/插值。此事实不证明原片像素逐帧相同。',
        'source_PNGs_pixel_identity_asserted':False,'source_camera_subpixel_translation_solved':False,
        'absolute_root_or_tip_screen_position_not_used_as_intrinsic_volume_proof':True,
        'caption_page_change_not_used_as_ground_or_jump_measure':True,
        'no_physical_takeoff_landing_certified_without_foot_contact':True
    },
    'new_per_state_observations':state_findings,'new_P1_issues':[],'open_playback_and_structural_points':open_points,
    'actual_view_list':viewlist,'input_snapshot':rec(R/'READONLY_INPUTS_AND_QA_MANIFEST.json'),
    'complete_context_panels_v02':rec(R/'COMPLETE_CONTEXT_PANELS_v02.json'),'fresh_temporal_PNGs':overview,
    'legacy5stage_reference_independently_viewed':m['prior_5stage_board_reference_only'],
    'reference_user_policy':m['user_F1058_policy'],'old_source_motion_audit_reference_not_own_actual_claim':m['prior_source_motion_report_reference_only'],
    'live_10_bound_entries_and_raw_layer_hashes_rechecked_before_report':True,
    'current_ENTIRE_binding_file_may_change_due_unrelated_root_work':'Per-frame audited10-state binding payloads were compared exactly; root may update unrelated IDs concurrently.',
    'boundaries':{'static_only':True,'fresh_primary_or_independent_artistic_PASS_written':False,'original_speed_playback_performed':False,'slow_playback_performed':False,'dynamic_validated':False,'renderer_runtime_verified':False,'hidden_geometry_certified':False,'strict_flat_material_certified':False,'intrinsic_volume_conservation_certified':False,'photographic_registration_reapproved':False,'user_accepted':False,'art_pixels_modified':False,'central_registry_modified':False,'exposure_binding_modified':False,'generation_API_native_network_calls':0},
    'QA_correction_boundary':'Original v01 comparison PNGs preserved; v02 extends diagnostic canvas20px to fit complete700px context. Source/current asset pixels and uniform transforms never changed.'
}
record=put('F1053_F1097_STATIC_CONTINUITY_AUDIT_xhigh_v01.json',report)
lines=[
    '本次10态静态核查：55从F1058已开始外上回折，56继续外上，57下摆，58回收，59水平，60再下收；63当前卷已回肩前。',
    '',
    '新看了45源帧接触格、10精确绑定层的整幅0.5缩略与同坐标1x头肩白黑QA。可见LEFT低根没有随尾部上抬；未发现立即可定的新换根/无源phase P1。',
    '',
    '仍未认证动态/固有体量：56→57展开到压紧、57→58隐藏C、59→60横摆到下收、33-58→63肩前切换必须按真实PTS播放复核。未播放、未重绘、未改中央/绑定。',
    '',
    '| state / first | 原相位 | 当前静态观察 |',
    '|---|---|---|',
]
for row,f in zip(m['states'],findings):lines.append(f'| {row["id"]} / F{row["first_frame"]} | {f["source_phase"]} | {f["target"]} |')
lines += ['',f'报告 SHA256: {record["sha256"]}','',f'actual清单 SHA256: {viewlist["sha256"]}','']
md=R/'F1053_F1097_STATIC_CONTINUITY_AUDIT_xhigh_v01.md';assert not md.exists();md.write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'report':record,'actual_views':viewlist,'readable_report':rec(md),'fresh_boards':overview,'generation_calls':0},ensure_ascii=False))
