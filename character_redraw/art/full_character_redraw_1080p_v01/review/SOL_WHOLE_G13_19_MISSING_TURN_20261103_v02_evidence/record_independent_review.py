from pathlib import Path
from PIL import Image
import json,hashlib,datetime,collections
B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
R=B/'drawings/ART-G13-19/v01/whole_imggen_restore_missing_turn_visibleunion_twoleaves_v02'
E=Path(__file__).parent
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(p):return dict(path=str(Path(p)),sha256=sha(p))
q=read(R/'request_imggen_ROOT_AUTHORIZED.json');g=read(R/'BUILTIN_GENERATION.json');receipt=read(R/'NATIVE_CALL_RECEIPT.json')
raw=R/'character_imggen_original.png';digest=sha(raw)
assert digest==g['output_sha256']==receipt['raw_sha256']=='a37e83a3e6cfadcb323bc61efa993123c14c411a8148c231f2cee161ab266319'
assert g['dimensions']==[1433,1098] and Image.open(raw).mode=='RGBA'
assert receipt['known_result_saved'] and not receipt['result_unknown'] and receipt['native_calls']==1 and receipt['api_calls']==0
for p,s in zip(q['refs'],q['reference_sha256'],strict=True):assert sha(p)==s
assert Path(q['prompt_file']).read_text('utf-8')==q['prompt']
req=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json';tol=B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json';reject=B/'review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json'
assert sha(req)=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
assert sha(tol)=='4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7'
source_audit=B/'review/SOURCE_G13_19_HAND_VISIBLE_RANGE_20261103_v01.json';audit=read(source_audit)
scope=B/'drawings/ART-G13-19/v01/prep_first_api_canonical1284_wider3734_outward_partialhands_blackred_v07_visibleunion/PER_EXPOSURE_VISIBLE_UNION_CONSTRAINTS.json';six=read(scope)
for x in six['exposures']:assert sha(x['source']['path'])==x['source']['sha256']
source1=B/'coverage/source_frames/F001284.png';source2=B/'coverage/source_frames/F003734.png'
assert sha(source1)=='7f30e3b08128f9f63c855aeb787d80f9d880ad8051062aba82e671124bd5b19c'
assert sha(source2)=='96873978becd3f8cf2dc510bafe0cc0bcdef80bf23a8a070390ea934ee69fa0a'
timeline=Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\data\original_timeline.json');rows={x['frame']:x for x in read(timeline)}
assert rows[1284]['pts']==685488 and rows[3734]['pts']==1994000
diags=read(E/'DIAGNOSTIC_PROVENANCE.json')
pair=B/'review/SOURCE_G13_19_HAND_VISIBLE_RANGE_20261103_v01_evidence/RIGHT_INDEX_SAME_WIDER_COORDS_CANONICAL_LEFT_WIDER_RIGHT_3x.png'
paths=[raw,R/'qa_white.png',R/'qa_black.png',source1,source2,*map(Path,q['refs']),*[Path(x['path']) for x in diags],pair]
assert len(paths)==19
ev=[dict(**f(p),actual_viewed=True,method='functions.view_image in this fresh review; not PREP actual-view inheritance') for p in paths]
# Pixel facts supplement, never replace, visual judgement: the upper index is a solid palm-connected component.
a=Image.open(raw).getchannel('A');pts=[(1265,748),(1300,706),(1330,673),(1360,642),(1380,619)]
samples=[dict(x=x,y=y,alpha=a.getpixel((x,y))) for x,y in pts]
start=(1265,748);end=(1380,619);queue=collections.deque([start]);visited={start}
while queue:
    x,y=queue.popleft()
    for u,v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
        if 1215<=u<1425 and 580<=v<825 and (u,v) not in visited and a.getpixel((u,v))>=200:
            visited.add((u,v));queue.append((u,v))
connected=end in visited
assert connected
pixel=dict(raw=f(raw),read_only=True,ROI=[1215,580,1425,825],threshold=200,
           palm_start=list(start),upper_index_distal_point=list(end),same_opaque_connected_component=connected,
           sample_alpha=samples,does_not_solve_source_to_art_production_registration=True,
           interpretation='Visual WB plus alpha confirm uninterrupted palm-to-upper-index. Lower folded-finger gap is not the missing upper shaft bridge in source audit.')
(E/'UPPER_INDEX_ALPHA_FACTS_READONLY.json').write_text(json.dumps(pixel,ensure_ascii=False,indent=2),'utf-8')
p1=[dict(code='UNSUPPORTED_COMMON_UPPER_INDEX_BRIDGE_STILL_CONNECTED',severity='P1',
    region_raw_xyxy=[1235,600,1400,809],
    description='画右上方长index从掌部到tip仍连续实色/轮廓；新透明缺口仅将下方折指片段切离。源1284+3734共同未知的是上长指近段与远端tip之间的shaft桥，不能用折指下方任意缺口替代。',
    source_basis='Own1284 shows distal upper tip outside first caption bar; own3734 shows proximal palm/index left of its bar. Both hide a common upper-finger strip, approximately wider-native x1243..1252. Uniform source coverage fit is diagnostic, not a solved production mask.',
    evidence=[str(E/'CURRENT_RIGHT_UPPER_INDEX_CONTINUOUS_FOLDED_PIECES_white_3x.png'),str(E/'CURRENT_RIGHT_UPPER_INDEX_CONTINUOUS_FOLDED_PIECES_black_3x.png'),str(E/'CURRENT_RIGHT_UPPER_INDEX_ALPHA_3x.png'),str(pair)],
    required_change='保真实已见远端tip/下方折指片段及源掌腕；上长index共同未见桥段保持透明中断，不补肉色/墨线桥、不把已见tip一并删掉。不得靠后期字幕遮住来宣称人物未知桥已合法补齐。')]
p2=['肩前深度仍未由本单帧充分证明：coil多在肩外，根/白肩褶有限遮挡可读，不把prompt或未知动态当成front-route证据。',
    'GRAY面/返回有softgray与规则分界和稍暗细带，未见本次需要另立大暗底/银白高光P1；严格纯平色与隐藏完整拓扑不认证。',
    '原手书/手肘袖口/脸帽比例与本源有细差；右手碎段形状/定位也仍待桥修后fresh实看和逐曝光摄影，不能由任意透明洞放行。']
entry=dict(id='ART-G13-19',version='whole_imggen_restore_missing_turn_visibleunion_twoleaves_v02',
    review_status='repair_required',status='repair_required',repair_required=True,independent_static_pass=False,independent=True,
    image=str(raw),image_sha256=digest,dimensions=[1433,1098],
    canonical_source_frame=1284,canonical_source_pts=685488,production_reference_source_frame=3734,production_reference_source_pts=1994000,
    actual_viewed=True,actual_viewed_paths=[str(p) for p in paths],
    evidencehash=hashlib.sha256(json.dumps(ev,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest(),
    requirements_revision='goal_curl_assessment_20261103_v06',curl_structure_policy_id='hollow_two_large_one_small_20261102_v04',
    P1=p1,P2_open=p2,
    repaired_visible_findings=[
       '相比用户否决96c899两大转直接钩尾，本新4x白黑能跟踪两较大宽灰前面/opaque返回后，另有较小末转自己的GRAY正面与后返，再渐细C；不是只多绿线/孔或第二大转hook充数。小末转缺失本次可见已修，尺寸/轴向未因此成为新master。',
       '新帽4x只余两片向上展开MAIN黑叶与很短公共根；原向右下第三独立长叶已消。公共根微锯齿不判新增第三叶。',
       '灰短bob已取代红尖头/双高红卷，唯一画右低LEFT双珠/nape根与自然bob遮挡保留；未见换耳/高根/第二束。',
       '本源不等圆睁/瞳位、单charcoal普通白点、小窄粉O与黑长袖红结金扣白肩袖围裙腰后结上缘保留，半身不补腿鞋，画左长指仍依源左边裁出。',
       '眼角紧邻小短笔仍见，但依据4cab79用户容差可保；本次不将其单独判P1或声称成功删净，不扩张为整稿/所有大痣接受。'],
    right_hand_source_union_assessment=dict(common_unknown_upper_bridge_fixed=False,
       current_upper_index_palm_to_tip_continuous=True,only_lower_folded_pieces_detached=True,
       observed_tip_and_fold_fragments_present=True,correct_shape_and_placement_of_all_fragments_certified=False,
       generic_transparent_gap_is_not_source_bridge_proof=True,
       approximate_common_source_strip_wider_native_xyxy=[1243.0,96.31543708780481,1252.1325581588071,704.9410175540169],
       diagnostic_strip_not_applied_as_art_mask=True,
       known_source_audit=f(source_audit),alpha_pixel_facts=f(E/'UPPER_INDEX_ALPHA_FACTS_READONLY.json')),
    curl_visible_assessment=dict(two_large_plus_genuine_small_turn_then_C_visible=True,
       small_turn_has_own_gray_front_and_opaque_return=True,user_missing_turn_rejection_applied=True,
       apparent_missing_turn_fixed_relative_to_rejected_parent=True,not_whole_art_pass=True),
    main_cap_leaves_count=2,third_independent_lower_leaf_visible=False,
    eye_corner_tolerance=f(tol),front_shoulder_route_certified=False,
    X01_baseline_scope='curl rendering only, not fixed size/axis/wholecharacter acceptance',
    photographic_registration_validated=False,all_exposures_reviewed=False,dynamic_validated=False,
    hidden_geometry_certified=False,strict_flat_material_certified=False,user_accepted=False,
    reviewer_API_calls=0,reviewer_native_calls=0,central_or_binding_modified=False)
report=dict(report='SOL_WHOLE_G13_19_MISSING_TURN_VISIBLEUNION_20261103_v02',
    reviewer='xhigh_pending_artist fresh independent review; not v02 PREP author and not ROOT PRIMARY',
    reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    scope='Exact known v02 raw/WB, all5refs/prompt, own canonical1284+wider3734 full source and source-union audit actually reviewed. Fresh19 image paths, no inherited PREP actual-view declarations.',
    entries=[entry],actual_viewed_evidence=ev,requirements=f(req),user_missing_turn_rejection=f(reject),eye_tolerance=f(tol),
    source_evidence=dict(canonical=dict(**f(source1),frame=1284,pts=685488),wider=dict(**f(source2),frame=3734,pts=1994000),
      audit=f(source_audit),constraints=f(scope),six_exposure_PTS_evidence_from_audit=True,fresh_full_native_views_this_review=[1284,3734],
      all6_fresh_native_images_claimed=False,source_timeline=f(timeline)),
    known_native_technical=dict(receipt=f(R/'NATIVE_CALL_RECEIPT.json'),record=f(R/'BUILTIN_GENERATION.json'),
      known_saved=True,native_calls_in_execution_receipt=1,api_calls=0,elapsed_wall_seconds=receipt['elapsed_wall_ms']/1000,
      generation_seconds_not_separately_exposed=True,quality_parameter_exposed=False,automatic_retry=False,technical_success_not_art_pass=True),
    diagnostic_provenance=f(E/'DIAGNOSTIC_PROVENANCE.json'),
    documents_read=[f(R/'request_imggen_ROOT_AUTHORIZED.json'),f(R/'prompt_imggen.txt'),f(R/'SOURCE_EXTENT_PROOF_PREPONLY.json'),f(req),f(reject),f(tol),f(source_audit),f(scope)],
    generation_calls=0,network_calls=0,central_modified=False,photography_validated=False,dynamic_validated=False,user_accepted=False)
out=B/'review/SOL_WHOLE_G13_19_MISSING_TURN_VISIBLEUNION_20261103_v02.json';assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
md=out.with_suffix('.md');assert not md.exists();md.write_text('\n'.join(['# G13-19 v02 独立实看：退修','',
    f'当前raw：{digest}，1433×1098 RGBA。一次known builtin，68.863s为回执墙钟，非单独曝光生成耗时。','',
    'P1：上长index从掌部到tip仍连续，透明只将下方折指分开；共同未知桥位于上长指shaft，位置/拓扑未修。源1284与3734联合也未观察到该桥，不能凭有洞放行。保真实tip和折指片段，不补未知桥。','',
    '已修：两大后新增真实小末转的灰正面/不透明灰返回，再C；第三独立下帽叶消，只2 MAIN加短公共根。灰bob、低LEFT画右根、本不等圆睁/窄粉O/黑红白衣及半身裁切可保。','',
    '4cab79眼角小短笔容差适用，未再据tiny分离判P1；不扩大为整稿认可。肩前深度、softgray/规则返线等P2未认证。','',
    '19图实际查看，精确paths/SHA在JSON。源相机实际查看1284/3734，六曝光scope依据保留文档，不冒称本轮全6摄影/播放。','',
    f'报告SHA256：{sha(out)}','本轮0调用/0中央/0摄影绑定，建议桥修前不续本家族。'])+'\n','utf-8')
print(json.dumps(dict(report=f(out),md=f(md),decision='repair_required',actual_images=len(ev),P1='upper-index common unknown bridge still opaque/continuous',curl_missing_turn_fixed=True,two_main_cap_leaves=True,alpha_samples=samples),ensure_ascii=False,indent=2))
