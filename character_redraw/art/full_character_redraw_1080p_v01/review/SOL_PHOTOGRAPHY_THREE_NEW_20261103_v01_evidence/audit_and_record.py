"""Independent read-only pixel/PTS audit; writes only this review's evidence/report."""
from pathlib import Path
from PIL import Image
import json, hashlib, datetime, math

B = Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
E = Path(__file__).parent
OUT = B / 'review/SOL_PHOTOGRAPHY_THREE_NEW_CURRENT_STATIC_20261103_v01.json'
MAN = B / 'review/PHOTOGRAPHY_PREP_THREE_NEW_STATIC_CANDIDATES_20261103_v01/FINAL_PHOTOGRAPHY_PREP_MANIFEST.json'
TIME = Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\data\original_timeline.json')

def read(p):
    return json.loads(Path(p).read_text('utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def item(p):
    p = Path(p)
    return {'path': str(p), 'sha256': sha(p)}

def save(p, obj):
    assert not Path(p).exists(), f'Refuse to overwrite {p}'
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', 'utf-8')

assert sha(MAN) == 'bb76210f03793a3b19c0c68bededf4a9463db265213ea569f9ac42e8c9b67197'
m = read(MAN)
registry = read(B / 'ASSET_REGISTRY.json')
timeline = {r['frame']: r for r in read(TIME)}
evidence = {}
actual = {}
checks = []
entries = []

def verify(f, role):
    p = f['path']; digest = sha(p)
    assert digest == f['sha256'], (role, p, digest, f['sha256'])
    if p not in evidence:
        evidence[p] = {**item(p), 'roles': []}
    if role not in evidence[p]['roles']:
        evidence[p]['roles'].append(role)
    return read(p) if Path(p).suffix.lower() == '.json' else None

def seen(p, role, key):
    p = str(Path(p))
    if p not in actual:
        actual[p] = {**item(p), 'roles': [], 'case_keys': [], 'actually_viewed_in_this_review': True,
                     'view_method': 'functions.view_image; not inherited from PREP maker'}
    if role not in actual[p]['roles']:
        actual[p]['roles'].append(role)
    if key not in actual[p]['case_keys']:
        actual[p]['case_keys'].append(key)

observations = [
 dict(joint='wider3731独立v02：不等圆睁/pinkO、两侧不同横折指组与腕袖、肩领红结金扣、腰线共同保住；相较initial整体+10/+10后上下更接近自己的原片，非套canonical相机。',
      p2=['帽/bob轮廓及双腕/腰有约5–15px局部视觉残差；本稿身份轮廓变化不能用原红发边缘硬匹配。','原卷softgray与规则返线的艺术P2保留；肩前深度不由摄影证明。'],
      extent='原半身无腿鞋。真实实体底切raw1013→1091.018在1080画外；canvas1024不作切口依据，无画内悬浮横切。'),
 dict(joint='canonical1281采用独立v02的1.245倍近镜：头脸/眼口、肩金扣、双手腕到画底腰上缘共同贴近；initial明显过小已改善，未将wider源的手尖完整范围强塞入近镜。',
      p2=['画右指尖/折指外形及帽顶、袖口有轻微视觉残差（部分约10–20px）；未见需立即局部变形或补画的摄影P1。','原卷材质和肩前深度P2保留。'],
      extent='真实实体底切raw1013→1234.185出1080。画左长指尖与下折指按本近镜源自然出画，不补画外手/裙腿。'),
 dict(joint='own4617：更放松的不等弧睁眼/极小闭口、唯一斜跨裙前低手套、远手隐藏、倾头身与肩腕腰膝踝双鞋能同一整体变换保住。',
      p2=['帽顶约高10px，腕位/裙缘/后带有小残差；腰膝踝与鞋更近。','既有softgray/轻薄边缘alpha、规则灰返线与肩前深度P2不由摄影解除。'],
      extent='两鞋完整在画内，强实体末像素投影约1015.516，无新增腿鞋/漂浮裙切线。源花瓣全部独立未带入，遮住的极细原轮廓不由此认证。'),
 dict(joint='own4625采用nestedv02：较圆不等眼/小闭口、两只不同高度低手套、直垂近臂和侧方远手保持，头肩腕腰膝踝及双鞋共同贴近；较initial偏大且上部高、鞋更低已改善。',
      p2=['帽眼、肩外缘与手套/裙外缘仍有小差异，未见新的明显摄影P1。','肩前深度、softgray/规则返线和原低alpha边缘P2保留；4cab79所准眼角紧邻短笔不机械退修。'],
      extent='两完整鞋均在画内，强实体末行投影约1026.595，留约53px；真实鞋尖而非透明画布作extent核查。'),
]

for i, c in enumerate(m['cases']):
    key = c['case_key']
    for name in ['raw','source','own_guide','JOB','original_REGISTRATION_PLAN','proposed_geometry_not_selected','preserved_initial_proposal','transparent_unselected_layer','same_native_comparison']:
        verify(c[name], key + ':' + name)
    for name, f in c['surfaces'].items():
        verify(f, key + ':1080_' + name)
    for name, f in c['retained_artistic_static_review'].items():
        verify(f, key + ':current_art_' + name)
    p = read(c['proposed_geometry_not_selected']['path'])
    init = read(c['preserved_initial_proposal']['path'])
    job = read(c['JOB']['path']); reg = read(c['original_REGISTRATION_PLAN']['path'])
    live = registry[c['id']]
    assert live['sha256'] == c['raw']['sha256'] == sha(live['image'])
    assert live['primary_static_pass'] and live['independent_static_pass']
    for name, regkey in [('primary','primary_review'), ('independent','independent_review')]:
        assert sha(live[regkey]) == c['retained_artistic_static_review'][name]['sha256']
    assert p['raw'] == c['raw'] and p['unselected_layer'] == c['transparent_unselected_layer']
    assert p['primary_static_review'] == c['retained_artistic_static_review']['primary']
    assert p['independent_static_review'] == c['retained_artistic_static_review']['independent']
    assert p['registry_selected_raw_sha256'] == c['raw']['sha256']
    assert p['source_frame'] == c['source_frame'] and p['source_pts'] == c['source_pts']
    row = timeline[c['source_frame']]
    assert row['pts'] == c['source_pts'] and c['timebase'] == '1/16000'
    basis = job if job['source_frame'] == c['source_frame'] else job['production_reference']
    assert basis['source_frame'] == c['source_frame'] and basis['source_pts'] == c['source_pts']
    assert basis['source_image_sha256'] == c['source']['sha256']
    s = float(c['scale']); tx, ty = c['translation']
    assert s > 0 and math.isfinite(s) and all(math.isfinite(x) for x in [tx,ty])
    assert p['scale'] == s and p['translation'] == [tx,ty]
    raw = Image.open(c['raw']['path']).convert('RGBA')
    assert list(raw.size) == c['raw_dimensions']
    expected = raw.transform((1920,1080), Image.Transform.AFFINE,
                             (1/s,0,-tx/s,0,1/s,-ty/s), resample=Image.Resampling.BICUBIC)
    layer = Image.open(c['transparent_unselected_layer']['path']).convert('RGBA')
    assert layer.size == (1920,1080) and expected.tobytes() == layer.tobytes(), key
    for name, color in [('white',(255,255,255)),('black',(0,0,0)),('pink',(213,167,169))]:
        surface = Image.new('RGBA', (1920,1080), color + (255,))
        surface.alpha_composite(expected)
        actual_surface = Image.open(c['surfaces'][name]['path']).convert('RGB')
        assert surface.convert('RGB').tobytes() == actual_surface.tobytes(), (key,name)
    box = tuple(c['comparison_native_crop_xyxy']); w = box[2]-box[0]
    native = Image.open(c['source']['path']).convert('RGB')
    assert native.size == (1920,1080)
    pair = Image.new('RGB',(w*2,1080),'white')
    pair.paste(native.crop(box),(0,0))
    pair.paste(Image.open(c['surfaces']['pink']['path']).convert('RGB').crop(box),(w,0))
    assert pair.tobytes() == Image.open(c['same_native_comparison']['path']).convert('RGB').tobytes()
    bbox = raw.getchannel('A').point(lambda a: 255 if a >= 200 else 0).getbbox()
    last = (bbox[3]-1)*s+ty
    assert abs(last-c['strong_art_last_pixel_row_projects_y']) < 1e-7
    cut = c['entity_cut_raw_y']
    projected_cut = cut*s+ty if cut is not None else None
    assert projected_cut == c['entity_cut_projects_y'] or (projected_cut is not None and abs(projected_cut-c['entity_cut_projects_y'])<1e-7)
    # QA were actually viewed. This records their source, not a new claim from pixel statistics.
    paths = [(c['raw']['path'],'current_raw'),
             (Path(c['raw']['path']).parent/'qa_white.png','current_raw_white'),
             (Path(c['raw']['path']).parent/'qa_black.png','current_raw_black'),
             (c['source']['path'],'own_native_source'),
             (c['own_guide']['path'],'own_pose_guide'),
             *[(f['path'],'final_1080_'+name) for name,f in c['surfaces'].items()],
             (c['same_native_comparison']['path'],'final_same_native_pair')]
    if i in [0,1,3]:
        paths.append((init['same_native_comparison']['path'],'preserved_initial_pair'))
        verify(init['same_native_comparison'], key + ':preserved_initial_pair')
    for path, role in paths:
        seen(path, role, key)
    for n, box in [(0,(640,395,865,655)),(2,(630,335,830,600)),(3,(592,274,770,520))]:
        if c['id'] == m['cases'][n]['id']:
            for tone in ['white','black']:
                qpath=E/(c['id']+'_EXACT_CURRENT_COIL_'+c['raw']['sha256'][:8]+'_'+tone+'_3x_READONLY.png')
                seen(qpath,'fresh_exact_current_coil_'+tone+'_3x',key)
                evidence[str(qpath)]={**item(qpath),'roles':['read-only current coil 3x, actual viewed'],
                    'source_image':c['raw'],'crop_xyxy':list(box),'resampling':'NEAREST 3x from exact raw QA composite; no art edit'}
    check = dict(case_key=key, raw_sha256=c['raw']['sha256'], source_frame=c['source_frame'],
                 source_pts=c['source_pts'], exact_manifest_hashes=True, current_registry_raw_and_reviews_match=True,
                 original_PTS_row=row, JOB_own_source_basis=basis,
                 single_whole_uniform_transform_pixel_exact=True, alpha_pixel_exact=True,
                 three_backings_pixel_exact=True, same_native_pair_pixel_exact=True,
                 raw_alpha200_bbox=list(bbox), strong_art_last_pixel_row_projects_y=last,
                 entity_cut_raw_y=cut, entity_cut_projects_y=projected_cut,
                 initial_preserved=True, source_pixels_and_art_raw_not_modified=True)
    checks.append(check)
    o = observations[i]; conditional = o.get('conditional',False)
    entries.append(dict(id=c['id'],case_key=key,source_frame=c['source_frame'],source_pts=c['source_pts'],
        decision='conditional' if conditional else 'candidate',
        review_status='conditional_static_registration_candidate' if conditional else 'retained_static_registration_candidate',
        registration_candidate=not conditional,conditional_registration_candidate=conditional,
        static_registration_review_passed=not conditional,
        scope='Only this exact raw/proposal/unselected layer at this single own native source; not all exposures, playback or user approval.',
        raw=c['raw'],raw_sha256=c['raw']['sha256'],raw_dimensions=c['raw_dimensions'],
        proposal=c['proposed_geometry_not_selected'],proposal_sha256=c['proposed_geometry_not_selected']['sha256'],
        preserved_initial_proposal=c['preserved_initial_proposal'],
        layer=c['transparent_unselected_layer'],reviewed_unselected_layer_sha256=c['transparent_unselected_layer']['sha256'],
        layer_dimensions=[1920,1080],layer_mode='RGBA',
        source={**c['source'],'frame':c['source_frame'],'pts':c['source_pts'],'timebase':c['timebase']},
        original_PTS_basis=dict(timeline=item(TIME),row=row,actual_table_read=True),
        geometry=dict(transform_kind='single whole uniform positive scale and translation',scale=s,translation=[tx,ty],
                      single_transform_pixel_exact_reproduces_layer=True,all_three_backings_pixel_exact=True,
                      same_native_comparison_pixel_exact=True,raw_alpha200_bbox=list(bbox),
                      strong_art_last_pixel_row_projected_y=last,entity_cut_raw_y=cut,entity_cut_projects_y=projected_cut,
                      no_partwise_warp=True,no_art_painting_or_alpha_cleanup=True),
        current_registry_target_readback=dict(selected_image_sha256=live['sha256'],primary_static_pass=True,
             independent_static_pass=True,matches_exact_target=True,proposal_current_review_SHA_matches=True,
             **c['retained_artistic_static_review']),
        documents_actually_read=dict(JOB=c['JOB'],REGISTRATION_PLAN=c['original_REGISTRATION_PLAN']),
        visual_findings=dict(joint_head_shoulders_wrists_waist_knees_ankles_shoes=o['joint'],
             extent_and_physical_cut=o['extent'],P1=[],P2=o['p2'],
             source_action_eyes_hands_costume_and_extent_checked=True,
             root_does_not_become_verified_by_prompt=True),
        P1=[],P2=o['p2'],front_shoulder_route_certified=False,
        existing_art_P2_not_cleared=True,X01_baseline_scope='curl drawing only; not size/axis/body/photography/user acceptance',
        actual_viewed_paths=[str(Path(x[0])) for x in paths],
        root_action='Explicit ROOT visual disposition of upper/lower proportion residual before adoption; no part warp.' if conditional else 'ROOT actual review then unselected single-source static disposition only.',
        production_selected=False,production_binding=False,exposure_bindings_changed=False,
        all_exposures_reviewed=False,actual_playback=False,dynamic_validated=False,user_accepted=False))

req=item(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json')
assert req['sha256']=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
tol=item(B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json')
assert tol['sha256']=='4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7'
read(req['path']);read(tol['path'])
for entry in entries:
 entry['policy']=dict(requirements=req,eye_corner_tolerance=tol,
     curl_scope='X01 only curl drawing, not body/size/axis/camera or user whole acceptance.',
     unrelated_G13_19_rejection_not_automatically_propagated=True)
 entry['visual_findings']['visible_curl_observation']='本次新3x白黑实看：可辨两大灰前面及更小下转灰面/不透明返回、再接C；未因G13-19少卷拒绝自动撤回别稿。细mint与soft/规则返线按原P2保留，摄影不升级卷大小/路线或用户验收。'
tech = dict(report='INDEPENDENT_PIXEL_PTS_READBACK_THREE_NEW_20261103_v01',
            recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest=item(MAN),
            checks=checks,artifact_evidence=list(evidence.values()),
            generation_calls=0,network_calls=0,central_modified=False,
            caution='Exact pixel reproduction checks photography operations only; it is not an artistic judgement or runtime playback.')
save(E/'TECHNICAL_READBACK.json', tech)
report = dict(report='SOL_PHOTOGRAPHY_THREE_NEW_CURRENT_STATIC_20261103_v01',
    reviewer='xhigh_pending_artist fresh independent photography reviewer; not PREP producer or ROOT PRIMARY',
    recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),prepared_manifest=item(MAN),
    scope='Three art states, four exact single-source static registration proposals. All own native/raw/WB/guide and final1080WB/pink/pair independently actually viewed; three revised initial pairs and six current-coil3x composites also actual viewed. G13-18 same raw shared by two independently judged cameras. No maker view claim inherited.',
    summary=dict(distinct_art_states=3,source_proposals=4,registration_candidates=4,
        conditional_registration_candidates=0,repair_required=0,P1_total=0,
        actual_viewed_unique_image_count=len(actual),all_raw_layer_proposal_review_and_source_PTS_verified=True,
        unselected_layers_only=True,existing_art_P2_retained=True),
    entries=entries,actual_viewed_evidence=list(actual.values()),
    technical_readback=item(E/'TECHNICAL_READBACK.json'),
    method_readback=dict(source_PTS_timeline=item(TIME),
        expected_layer='PIL RGBA original raw -> single BICUBIC AFFINE (1/s,0,-tx/s,0,1/s,-ty/s) ->1920x1080, exact pixels incl alpha.',
        backings='white255/black0/pink213,167,169 exact alpha-composite; same-native pair crop exact.',
        actual_image_review_separate_from_technical=True),
    generation_calls=0,api_calls=0,native_calls=0,network_calls=0,
    central_JOB_REG_registry_or_binding_modified=False,art_pixels_modified=False,alpha_cleanup_applied=False,
    production_selected=False,production_binding=False,exposure_bindings_changed=False,
    all_exposures_reviewed=False,actual_playback=False,dynamic_validated=False,user_accepted=False,not_ROOT_PRIMARY=True)
save(OUT,report)
lines=['# 独立摄影静态审查：3状态 / 4源', '',
       '4个精确单源静态摄影候选可保，未见新增摄影P1。所有方案未选择、未绑定，未认证全曝光、动态或用户接受。', '',
       '|候选|自己的原片 / PTS|结论|共同定位与保留问题|', '|---|---|---|---|']
for e,o in zip(entries,observations):
    lines.append(f"|{e['id']} {e['case_key']}|F{e['source_frame']} / {e['source_pts']}|{e['decision']}|{o['joint']} {'；'.join(o['p2'])} {o['extent']}|")
lines += ['', 'G13-18：raw实体底切1013，wider3731投影1091.018，canonical1281投影1234.185；两个独立相机均出1080。canvas高1024不能代替真实实体切口。', '',
          'G51-09/10肩前深度、既有软灰与规则返线P2保留；G51-10遵循4cab79眼角短笔容差。实际3x可辨各自灰前/灰返回与更小下转后C，不因另稿G13-19的缺卷用户拒绝自动回写。', '',
          f'本轮实际查看{len(actual)}个不同图像路径；完整路径/SHA/角色在JSON。4层均由原RGBA单一uniform变换逐像素复现，含alpha；三底与同坐标对照也一致。技术一致不等于美术验收。', '',
          f'技术证据：{E / "TECHNICAL_READBACK.json"}', f'主报告 SHA256：{sha(OUT)}', '',
          '0生成、0网络、0中央/索引/绑定修改。']
md=OUT.with_suffix('.md'); assert not md.exists(); md.write_text('\n'.join(lines)+'\n','utf-8')
print(json.dumps(dict(report=item(OUT),md=item(md),technical=item(E/'TECHNICAL_READBACK.json'),
                     summary=report['summary']),ensure_ascii=False,indent=2))
