"""Independent read-only pixel/PTS audit; writes only this review's evidence/report."""
from pathlib import Path
from PIL import Image
import json, hashlib, datetime, math

B = Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
E = Path(__file__).parent
OUT = B / 'review/SOL_PHOTOGRAPHY_EIGHT_MORE_CURRENT_STATIC_20261103_v01.json'
MAN = B / 'review/PHOTOGRAPHY_PREP_EIGHT_MORE_STATIC_CANDIDATES_20261103_v01/FINAL_PHOTOGRAPHY_PREP_MANIFEST.json'
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

assert sha(MAN) == '29366fe550cd269817c25616c1c0e7da244faa57c3389acac413dbb297129270'
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
    dict(joint='高竖食指与另一低平掌、眼口、肩腕腰膝踝及两鞋能由同一整体变换共同保住；帽顶和高手略高，未见须立即退修的新摄影P1。',
         p2=['帽顶/高手约5–15px高的视觉残差；头型身份变化不等于相机点位全部相同。'],
         extent='双鞋完整在画内，无半身实体横切或新增腿鞋。'),
    dict(joint='本帧向左转头、上手弯食指与拇指/下手平展仍保；帽发顶约25–35px高，眼/高手约10–17px高，但腰踝更近。整体下移不能同时改善上下，需ROOT对该比例残差显式取舍。',
         p2=['上部与下部不具有同一最佳平移：条件候选，未签无条件摄影通过；不可局部warp头/手。'],
         extent='前景鞋源本有底裁，raw1056边界投影1099.64在画外；后鞋全见。没有认证前鞋为完整鞋。', conditional=True),
    dict(joint='自己的腹前交叠/摊开手、tiny O、头肩腕腰膝踝及双鞋共同保住，未串前07高指或前鞋裁法。',
         p2=['帽/手/腰与鞋轮廓仍有小残差；源粉瓣遮住的细裙缘不由摄影认证或补画。'],
         extent='两鞋完整在画内，裙/白后带未出现悬浮实体截边。'),
    dict(joint='采用nested v02：放松偏右视线、小闭口、两只不同高度低手套及倾头、腰裙、双鞋共同贴近本4599源；相较initial上部偏高已缓解。',
         p2=['膝腕及服装外轮廓轻微差异、既有soft gray等艺术P2保留。'],
         extent='完整双鞋在画内；initial保留但本结论只对应v02。'),
    dict(joint='采用nested v02：近手内折/远手长分指两组区别仍保，倾头与裙腿到双鞋共同定位；较initial整体略大偏高已改善。',
         p2=['指尖、眼线及鞋缘余量有轻微差异；不是把单点fit当所有关节完全重合。'],
         extent='双鞋完整，无源外隐藏身体增绘；initial保留但本结论只对应v02。'),
    dict(joint='闭睫低俯侧倾、唯一斜跨裙前低手套、隐藏远手、长后带、裙腿全鞋均保，头肩腕腰膝踝共同位置可保。',
         p2=['帽顶约10px高、鞋约7px低的轻微残差。', '卷大部分投影肩外，单帧不足以证明肩前路线；原深度P2保留。'],
         extent='两鞋完整在画内，不添隐藏远手。', depth=False),
    dict(joint='自己的放松不等半开眼、弯近臂唯一低手套、远手隐藏、肩腰裙膝踝与双鞋仍保。',
         p2=['头/眼/帽较源约10–15px高而腕腰更近，作为小比例残差保留。', '肩前深度未得到单帧遮挡证明，摄影不认证该路线。'],
         extent='双鞋在画内，无明显漂浮实体切线或附加手。', depth=False),
    dict(joint='wider3726采用独立nested v02；帽脸、交叉裸手/腕、红结金扣和腰部共同保住。initial可见悬浮底切，v02已将真实实体切口放到画外；不将canonical机位套入本源。',
         p2=['头轴/眼鼻位置及手腕袖口外形仍有小残差；艺术卷材质等P2未由摄影解除。'],
         extent='raw实体底切1347→1118.026，低于1080；没有补隐藏腿或裙。画布高1381不是实体切口。'),
    dict(joint='canonical1277采用另一独立nested v02；近镜帽脸/金扣/交叉手与局部腰共同可保，未借wider坐标冒充本源。initial底切在画内，v02实体切口已出画。',
         p2=['头轴/眼鼻及袖口形状与源有轻微差异；不认证另一镜头或全曝光。'],
         extent='raw实体底切1347→1270.322，低于1080；本近镜自身下裁不等于漂浮横截，不添腿鞋。'),
]

for i, c in enumerate(m['cases']):
    key = c['case_key']
    for name in ['raw','source','JOB','original_REGISTRATION_PLAN','proposed_geometry_not_selected','preserved_initial_proposal','transparent_unselected_layer','same_native_comparison']:
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
             *[(f['path'],'final_1080_'+name) for name,f in c['surfaces'].items()],
             (c['same_native_comparison']['path'],'final_same_native_pair')]
    if i in [3,4,7,8]:
        paths.append((init['same_native_comparison']['path'],'preserved_initial_pair'))
        verify(init['same_native_comparison'], key + ':preserved_initial_pair')
    for path, role in paths:
        seen(path, role, key)
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

tech = dict(report='INDEPENDENT_PIXEL_PTS_READBACK_EIGHT_MORE_20261103_v01',
            recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest=item(MAN),
            checks=checks,artifact_evidence=list(evidence.values()),
            generation_calls=0,network_calls=0,central_modified=False,
            caution='Exact pixel reproduction checks photography operations only; it is not an artistic judgement or runtime playback.')
save(E/'TECHNICAL_READBACK.json', tech)
report = dict(report='SOL_PHOTOGRAPHY_EIGHT_MORE_CURRENT_STATIC_20261103_v01',
    reviewer='xhigh_pending_artist fresh independent photography reviewer; not PREP producer or ROOT PRIMARY',
    recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),prepared_manifest=item(MAN),
    scope='Eight art states, nine exact single-source static registration proposals. Each mandatory raw/WB, own native and final 1080 white/black/pink/pair independently actually viewed; initial four revised pairs also viewed. No maker actual-view claim inherited.',
    summary=dict(distinct_art_states=8,source_proposals=9,registration_candidates=8,
        conditional_registration_candidates=1,repair_required=0,P1_total=0,
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
lines=['# 独立摄影静态审查：8状态 / 9源', '',
       '8个单源静态候选可保；X01-07为条件候选。没有新明确P1。所有方案仍未选择、未绑定，未认证全曝光/动态/用户接受。', '',
       '|候选|自己的原片 / PTS|结论|共同定位与保留问题|', '|---|---|---|---|']
for e,o in zip(entries,observations):
    lines.append(f"|{e['id']} {e['case_key']}|F{e['source_frame']} / {e['source_pts']}|{e['decision']}|{o['joint']} {'；'.join(o['p2'])} {o['extent']}|")
lines += ['', 'X01-07：帽发顶约高25–35px，眼/高手约高10–17px，腰踝更近；需要ROOT显式处置，不能局部变形消差。前鞋是原底裁，非完整鞋。', '',
          'G13-17：raw实体底切是1347，wider3726投影1118.026，canonical1277投影1270.322，均在1080画外。两种镜头独立，initial仍保留。', '',
          'G51-07/08肩前层次P2未证；摄影不认证路线。X01只卷画法基线，不是整身、尺寸、轴向认可。', '',
          f'本轮实际查看{len(actual)}个不同图像路径；完整SHA/角色表在JSON中。9层均从原RGBA以单一uniform变换逐像素复现，含alpha；三底与同坐标对照亦一致。技术一致不等于美术验收。', '',
          f'技术证据：{E / "TECHNICAL_READBACK.json"}',
          f'主报告 SHA256：{sha(OUT)}', '', '本轮0生成、0网络、0中央/索引/绑定修改。']
md=OUT.with_suffix('.md'); assert not md.exists(); md.write_text('\n'.join(lines)+'\n','utf-8')
print(json.dumps(dict(report=item(OUT),md=item(md),technical=item(E/'TECHNICAL_READBACK.json'),
                     summary=report['summary']),ensure_ascii=False,indent=2))
