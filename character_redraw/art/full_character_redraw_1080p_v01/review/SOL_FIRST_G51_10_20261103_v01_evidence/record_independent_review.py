from pathlib import Path
from PIL import Image
import json, hashlib, datetime

B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
R=B/'drawings/ART-G51-10/v01/prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
E=Path(__file__).parent
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(p):return dict(path=str(p),sha256=sha(p))
res=read(R/'result.json');q=read(R/'API_PREPARED_REQUEST.json');job=read(R.parent/'JOB.json')
raw=R/'character_api_original.png';req=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'
assert sha(raw)==res['output_sha256']=='794a7d5de1d5c72acef640f5297f7d04c1085b7499bc576ab39d40eb4122fde9'
assert job['source_frame']==4625 and job['source_pts']==2469664
source=Path(job['source_image']);assert sha(source)==job['source_image_sha256']
assert sha(req)=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
for i,x in enumerate(res['inputs']):
    assert x['path']==q['InputImages'][i] and sha(x['path'])==x['sha256']
metrics=read(R/'curl_transport_metrics.json')
assert metrics['http_code']==200 and metrics['num_retries']==0 and res['transport_attempt_count']==1
prefix=read(B.parents[1]/'image_defaults.json')['generation_prompt_prefix']['text'].replace('\r\n','\n').strip()
prompt=(R/'prompt_effective.txt').read_text('utf-8-sig').replace('\r\n','\n')
assert prompt.startswith(prefix) and prompt.count(prefix)==1
assert sha(R/'prompt_effective.txt')==res['prompt_sha256']
timeline=Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\data\original_timeline.json')
row=next(x for x in read(timeline) if x['frame']==4625);assert row['pts']==2469664
paths=[raw,R/'qa_white.png',R/'qa_black.png',source,R.parent/'inputs/source_pose_guide.png',
       *map(Path,q['InputImages']),
       E/'CURRENT_EYES_MOUTH_white_5x.png',E/'CURRENT_ROOT_GRAY_RETURNS_C_white_5x.png',
       E/'CURRENT_ROOT_GRAY_RETURNS_C_black_5x.png',E/'CURRENT_TWO_UNEQUAL_GLOVES_white_2x.png',
       E/'CURRENT_VIEWER_LEFT_OUTER_LOWER_DETACHED_POINT_10x.png',
       R/'OWN4625_EYES_MOUTH_POINTS_READONLY_4x.png',E/'CURRENT_VIEWER_RIGHT_OUTER_EYE_EDGE_10x.png']
evidence=[{**f(p),'actual_viewed':True,'view_method':'functions.view_image in this independent review, not PREP claims'} for p in paths]
evidencehash=hashlib.sha256(json.dumps(evidence,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest()
p1=[dict(code='ISOLATED_UNDER_EYE_POINTS_REMAIN',severity='P1',
         finding='画左眼外下仍有一枚分离圆点；画右外下还有较小竖圆点，两者与上外眼线/方向睫毛之间有浅色间隔。源有这些旧点不能覆盖本次用户要求删除。',
         approximate_raw_xyxy=[[291,165,297,171],[397,149,402,155]],
         actual_evidence=[str(E/'CURRENT_VIEWER_LEFT_OUTER_LOWER_DETACHED_POINT_10x.png'),str(E/'CURRENT_VIEWER_RIGHT_OUTER_EYE_EDGE_10x.png')],
         required_change='去两侧离散点，保连接的上外眼线/真实方向短睫和小鼻/闭口；不改本帧较圆睁不等开度、视线或单色虹膜。')]
p2=['大部分coil位于肩外，只有根/肩白褶局部遮挡，缺足够胸侧T形互遮；肩前深度未证，不能因prompt称肩前而认证。',
    'bob/灰卷有softgray及返回内部较暗短带、规整返线；当前未见大面积独立深暗体积底或银白闪片，严格纯平色未认证。',
    '帽bob/手套指缘、腰裙后带与鞋轮廓有细差，原动作可保但摄影未审；单帧不认证相邻卷摆/大小与动态。']
entry=dict(id='ART-G51-10',review_status='repair_required',status='repair_required',repair_required=True,
    independent_static_pass=False,independent=True,image=str(raw),image_sha256=sha(raw),dimensions=list(Image.open(raw).size),
    canonical_source_frame=4625,canonical_source_pts=2469664,actual_viewed=True,actual_viewed_paths=[str(p) for p in paths],
    evidencehash=evidencehash,curl_structure_policy_id='hollow_two_large_one_small_20261102_v04',requirements_revision='goal_curl_assessment_20261103_v06',
    P1=p1,P2_open=p2,
    source_eyes_pose_costume_extent_conclusions=[
        'own4625 native/guide、source眼口与当前5x/10x实看：较圆睁不等弧眼、tiny中性闭口、略偏斜头保留；虹膜视觉为各一块深charcoal配普通小白点，未见明确黑芯灰环/月牙双色P1。唯两侧眼下分离点仍留，需退修。',
        '两只低手套都露且不同：画右近长臂较直下垂、低手外拇指上折/错层下指；画左远臂被腰裙遮住后短连接、远手斜向左下分指。未套09单斜跨手或添隐藏上臂。',
        '自己的斜围裙、外展裙、白后结/短长后带、不同腿向和两只完整鞋均保。白maidcap/画右2 MAIN黑叶、黑胸结/手套袜鞋、金扣白衣饰、暖肤与片尾灰绿保留；没有粉瓣字幕实体。线宽有粗细起伏，未明显向量化。'],
    curl_visible_conclusions=[
        '近正面头颈的解剖LEFT低耳后/nape根在画右bob与同侧肩颈之间，两珠局部被bob挡，未抬至帽/太阳穴、换画左近耳或长第二束。',
        '白黑5x可沿宽GRAY正面翻回opaqueGRAY内后返回，连续斜接第二大转再下渐细小C；thinmint沿带缘，真实露空随白黑底变化。未见明确独立封盖/断灰囊/额外主圈或实心柱贴绿线。',
        '完整头肩中卷体量中等，非micro或巨粗；用户76bd仅curl画法，不把其尺寸、轴向、服装或whole接受移植。实际肩前深度保P2未证。'],
    front_shoulder_route_assessment=dict(front_shoulder_route_certified=False,
        reason='Most visible coil lies outside shoulder silhouette; limited root/frill T cue does not prove full chest-front passage.',
        visible_root_low_LEFT_projection_retained=True,visible_cross_back_or_root_swap_observed=False,
        occluded_connection_geometry_certified=False,classification='P2_depth_route_unconfirmed'),
    X01_baseline_scope=dict(reference_sha256='76bd9b5cc147fa98a9d9bdf6b68ef703ebdf5a9ca96d8b5b4fb291fc37c6c44b',
                           use='curl_rendering_only',whole_art_acceptance_transferred=False,fixed_size_or_axis_transferred=False),
    photographic_registration_validated=False,dynamic_validated=False,hidden_geometry_certified=False,
    strict_flat_material_certified=False,user_accepted=False,whole_art_user_accepted=False,
    reviewer_API_calls=0,reviewer_native_calls=0,central_or_binding_modified=False)
docpaths=[R/'result.json',R/'API_PREPARED_REQUEST.json',R/'prompt_effective.txt',R/'curl_transport_metrics.json',
          R.parent/'JOB.json',req,B/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json',timeline]
report=dict(report='SOL_FIRST_G51_10_CURLBASELINE_20261103_v01',
    reviewer='xhigh_pending_artist fresh independent actual-image review; not FIRST PREP maker or ROOT PRIMARY',
    reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    scope='Own4625 source/guide, exact current raw/WB, all5 refs/effective prompt and fresh eye/coil/glove diagnostics actually viewed. Static art only.',
    entries=[entry],actual_viewed_evidence=evidence,
    call_technical_readback=dict(known_result='saved_original',provider=res['provider'],endpoint=res['endpoint'],model=res['model'],
        quality=res['quality'],size=res['size'],n=res['n'],elapsed_seconds=res['elapsed_seconds'],
        configured_retry=res['retry'],actual_automatic_retries=metrics['num_retries'],transport_attempt_count=res['transport_attempt_count'],
        effective_prompt_sha256=res['prompt_sha256'],normalized_full_mandatory_prefix_count=1,starts_with_mandatory_prefix=True,
        technical_success_not_artistic_pass=True),
    source_pts_readback=dict(timeline=f(timeline),row=row),requirements=f(req),
    diagnostic_provenance=f(E/'DIAGNOSTIC_PROVENANCE.json'),documents_read=[f(p) for p in docpaths],
    generation_calls=0,network_calls=0,central_modified=False)
out=B/'review/SOL_FIRST_G51_10_CURLBASELINE_20261103_v01.json'
assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
md=out.with_suffix('.md');assert not md.exists()
md.write_text('\n'.join(['# G51-10 首图独立实看：退修', '',
    f'当前raw：{sha(raw)}；624×1072；ownF4625 / PTS2469664。', '',
    'P1：两眼外下分离点仍留。画左较圆点约[291,165,297,171]，画右较小竖圆点约[397,149,402,155]，10x实际可见与眼线分隔；即使源有点也应删。保真实连接的睫线/鼻点，不改较圆睁开度与tiny闭口。', '',
    '可保：单charcoal虹膜和普通白点；两不等低手套/自己的姿腿与完整双鞋；2MAIN帽叶/ending灰绿；画右低LEFT根与连续宽灰2大+小C及thinmint。', '',
    'P2：肩前深度未证；softgray与规则返线/暗短带保留。摄影、动态、隐藏结构及用户验收均未认证。', '',
    f'17路径逐张actual；精确SHA在JSON。官方high n1/configretry1、actualretry0、25.624s、完整prefix一次，仅是已知技术回执。', '',
    f'报告 SHA256：{sha(out)}', '本轮0生成/0网络/0中央与绑定修改。'])+'\n','utf-8')
print(json.dumps(dict(report=f(out),md=f(md),evidence_count=len(evidence),decision='repair_required',P1='two isolated under-eye points'),ensure_ascii=False,indent=2))
