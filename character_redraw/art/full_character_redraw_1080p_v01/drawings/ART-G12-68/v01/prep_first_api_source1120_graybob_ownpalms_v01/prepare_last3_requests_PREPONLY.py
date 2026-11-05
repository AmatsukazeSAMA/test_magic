from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
B = HERE.parents[3]
PROJECT = B.parents[1]
H = Path(r'D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def rec(p):
    p = Path(p)
    d = {'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
    if p.suffix.lower() == '.png':
        with Image.open(p) as im:
            d.update(size=list(im.size), mode=im.mode)
    return d

def put(r, name, obj):
    p = r/name
    assert not p.exists(), p
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return rec(p)

now = datetime.now(timezone.utc).isoformat()
scope_path = B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json'
queue_path = B/'dance_first10_reference_redraw_v01/NEW40_ARTIST_QUEUE_v01.json'
registry_path = B/'ASSET_REGISTRY.json'
scope = read(scope_path)['states']
queue = read(queue_path)['rows']
registry = read(registry_path)
catalog_path = H/'data/panel_catalog.json'
catalog = read(catalog_path)
prefix = read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
auth = B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
assert read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model'] == 'gpt-image-2.5-sunburst'

identity = B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
detail = B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
key = B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
assert sha(identity) == '216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
assert sha(detail) == '4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'
assert sha(key) == 'd1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'

sentinels = []
for id in ['ART-G12-63', 'ART-G12-64', 'ART-G12-65', 'ART-G12-66', 'ART-G33-63']:
    cel = B/'drawings'/id/'v01'
    sentinels.extend(rec(p) for p in cel.glob('prep*/REQUEST_LOCK.json'))
    sentinels.extend(rec(cel/name) for name in ['JOB.json', 'REGISTRATION_PLAN.json'])

rows = [{'id': 'ART-G12-68',
  'source': 1120,
  'pts': 597936,
  'first': [1118, 1122],
  'first_pts': [596864, 599536],
  'size': '1280x944',
  'motion': 229,
  'motion_roi': [533, 237, 565, 261],
  'eyes_roi': [530, 224, 748, 350],
  'run': 'prep_first_api_source1120_graybob_ownpalms_v01',
  'source_sha': '85cf798a573a8ac9448708eaa2947e2425b6c2fe50a126edea99ab43cd920963',
  'action': '原1120头仍较直、圆睁眼、短浅弧闭笑。两臂外伸、两腕已转为近竖向外掌：画左长指并拢斜上偏左、掌根接较高白袖口；画右长指并拢斜上偏右、腕与掌更低且线角不同。保原拇指与指间线、两腕袖口/弯肘高低差，不沿66横向掌心朝上或借AI手势。当前黑长袖/红领结金扣、两肩白fan及竖褶、白袖口、腰带折角、画右腰后bow和围裙到画底全部按1120。',
  'canvas': '完整1280x944未挖头原guide；头、cap两黑叶、不同竖掌和腰裙均保原共同坐标。原source为半身，apron/黑裙在1080底边被切断，guide对应底裁保留，不加隐藏腿鞋，不把原底裙缩短留白。无新trim/单部位挪移。',
  'difference': '68不同于66：双腕由横摊转成近竖外掌、长指斜上且并拢；左掌更高、右袖口更低，头/腰/肩褶和红bow描线也不同。first1118与canonical1120同状态曝光来源均实际核，母帧不是1118。不得用G33-63全身构图替代当前半身源。',
  'motion_observation': 'actual '
                        'R229全图卷下段在肩侧比前状态有更长下伸/回弹读法，尾邻白frill，自身构造仍非母参。purehair[533,237,565,261]32x24仅灰发段，排脸眼、红珠/root和白肩饰。只给局部回弹/压缩相位；不能用小ROI证明隐藏长度或缩小固有发量，不复制AI竖掌/头脸。',
  'source_expression': '本1120双眼圆睁、左右睫弧/虹膜露出不对称，短浅弧闭笑。图1/5唯一开度和口形，不能套69/70半睑、图3中性小口或AI眼形。',
  'root_continuity': '唯一人物LEFT低耳后/nape双红珠根，当前正面投影在画右同侧bob下；低头时根随耳后/后颈一起倾转下降，不能沿用站直时的屏幕高度、抬到太阳穴/帽边，不能加画左近耳双珠或镜像身体。保从前63–66转正后同侧肩前/胸侧的自然路线，当前肩手/bob实际遮住才遮局部，不能无原因把整束转到背后或为躲根侧错误缩成小挂件，也不强拉尾尖穿到手臂前。前后新稿尚未逐曝光核实，本次只记录待核连续性意图，不宣称动态或家族通过。本帧仍较直，按源原卷及R229读到的回弹转译到同一低LEFT卷；卷可在自然肩侧伸展，不能为完整露尾换根或冻结成前66压紧小柱。'},
 {'id': 'ART-G12-69',
  'source': 1123,
  'pts': 599536,
  'first': [1123, 1128],
  'first_pts': [599536, 602736],
  'size': '1360x848',
  'motion': 234,
  'motion_roi': [529, 291, 557, 312],
  'eyes_roi': [560, 284, 766, 398],
  'run': 'prep_first_api_source1123_graybob_ownpalms_v01',
  'source_sha': 'bfc47ddf1466f342a481372e32c2fbe7ee63fc976efccbb25b591a50b5febe79',
  'action': '原1123向前鞠躬低头，头顶/cap前后层次可见，半睑向下视线、短小闭弧笑。两肘下沉且双前臂近水平伸向两侧；画左指尖斜左上并拢、拇指独立向左下分开，画右长指较平斜右上、拇指在下侧分出。两手在腰旁外侧，不是68近竖掌或合十。当前肩白褶、black长袖、两种白袖口线、红bow金扣、腰带/后bow/底apron原形全部保1123。',
  'canvas': '完整1360x848未挖头guide，低头、双手、颈肩腰和下围裙保持当前共同坐标；source1080本就只半身/apron下端切出，不能补腿鞋、把身体立直或拉长躯干去凑前帧头高。无新trim或单部位移动，较矮画布来自当前源裁框，不代表任意压扁人物。',
  'difference': '69首次1123恰是canonical1123；由68直头圆睁/高竖掌转为俯头半睑/两低外手，并可见更多头顶而下巴收近领口。图3站直全头只身份/体量，不能把头扶正、眼撑圆或掌抬回。两手原拇指分叉、袖口斜线与70的再次重画不同。',
  'motion_observation': 'actual '
                        'R234全图随俯头，卷在同侧肩颈下降/紧收，局部灰带斜向回折；AI半睑也不能拥有本source开度。purehair[529,291,557,312]28x21排眼脸、珠/root、白frill，仅局部弹性相位。不由这段裁图推整卷长度/固定轴或微缩固有发量，不复制AI头身/手腕。',
  'source_expression': '本1123双眼半睑、上睑较平且左右不对称，露出压低的charcoal虹膜，视线向下，短小弧闭笑。半睑是此原PV本态真实表演，不是G02模板；图1/5控制，不能复制图3圆睁。',
  'root_continuity': '唯一人物LEFT低耳后/nape双红珠根，当前正面投影在画右同侧bob下；低头时根随耳后/后颈一起倾转下降，不能沿用站直时的屏幕高度、抬到太阳穴/帽边，不能加画左近耳双珠或镜像身体。保从前63–66转正后同侧肩前/胸侧的自然路线，当前肩手/bob实际遮住才遮局部，不能无原因把整束转到背后或为躲根侧错误缩成小挂件，也不强拉尾尖穿到手臂前。前后新稿尚未逐曝光核实，本次只记录待核连续性意图，不宣称动态或家族通过。本态俯头投影会改变卷根与bob/肩的遮挡；允许根段部分藏在同侧bob/nape，保持完整发量读法与自然肩前路线，不把source高红双卷的上举根当新低root。'},
 {'id': 'ART-G12-70',
  'source': 1129,
  'pts': 602736,
  'first': [1129, 1133],
  'first_pts': [602736, 605248],
  'size': '1360x800',
  'motion': 238,
  'motion_roi': [528, 329, 555, 352],
  'eyes_roi': [570, 295, 785, 404],
  'run': 'prep_first_api_source1129_graybob_ownpalms_v01',
  'source_sha': 'ab2ddffc164b2db86f6dcaa047ee02a58256ab6f33495f2aba012c8713140d75',
  'action': '原1129头/肩进一步俯低，冠顶与cap前缘可见，半睑下视、极小闭弧笑。双肘仍下沉、两臂低向外伸；画左并拢指尖斜左上，拇指呈清楚弯钩向左下，画右长指斜右上较低、下侧拇指分出，掌根/指间线与69再重画。画左袖口下缘弯折、画右袖口接近竖边且掌腕更低，肩褶/红bow金扣/腰后带和原半身底裙独占1129。',
  'canvas': '完整1360x800未挖头原guide，仍是原1129共同构图，双手所有可见指端和apron黑裙底裁保留。不能复制69的头高/手腕或借图3直立头，不能补隐藏腿鞋/缩人留底。无新增trim或单部位变形。首段末曝光1129..1133在scope '
            'endPTS605248结束，原状态endPTS605408仅历史，不能越过10秒边界。',
  'difference': '70不同69：俯头/肩更低、cap和头顶透视略变，眼虹膜与睑弧重新描绘；画左拇指更弯、掌边与右侧分指/两袖口线也不是69重复。输出1360x800而69为1360x848，依各自真实source裁框保比例，不能把69机械压扁成70。',
  'motion_observation': 'actual '
                        'R238全图卷随更低俯头下移，末段在肩侧伸展/回收而非站直冻结；purehair[528,329,555,352]27x23排眼脸、珠/root和白frill，仅局部灰带相位。小ROI不能定整卷固有大小/隐藏圈或把回弹缩成装饰，不复制AI半睑/双手/较圆笑口。',
  'source_expression': '本1129半睑仍睁开、目光向下，左右眼弧和iris露出按本帧，极小弧闭笑；不可变闭眼或图3圆睁，不复制69像素眼口或G02半睑bitmap。图1/5唯一表演。',
  'root_continuity': '唯一人物LEFT低耳后/nape双红珠根，当前正面投影在画右同侧bob下；低头时根随耳后/后颈一起倾转下降，不能沿用站直时的屏幕高度、抬到太阳穴/帽边，不能加画左近耳双珠或镜像身体。保从前63–66转正后同侧肩前/胸侧的自然路线，当前肩手/bob实际遮住才遮局部，不能无原因把整束转到背后或为躲根侧错误缩成小挂件，也不强拉尾尖穿到手臂前。前后新稿尚未逐曝光核实，本次只记录待核连续性意图，不宣称动态或家族通过。本态是俯头收尾相位，低LEFT根仍随本耳后/nape低下，回折和C可随弹性变化、自然遮挡，但不许冻结同69整卷或把整束改成实心柱/封口盘。'}]

def find_catalog(x, name):
    if isinstance(x, dict):
        if x.get('id') == name:
            return x
        for value in x.values():
            found = find_catalog(value, name)
            if found: return found
    elif isinstance(x, list):
        for value in x:
            found = find_catalog(value, name)
            if found: return found

for row in rows:
    id = row['id']; cel = B/'drawings'/id/'v01'; r = cel/row['run']
    assert r.is_dir() and (r/'inputs').is_dir()
    assert registry.get(id) is None
    forbidden = ['character_api_original.png', 'character_imggen_original.png', 'attempt.json', 'result.json']
    assert not any(list(cel.rglob(name)) for name in forbidden)
    state = next(x for x in scope if x['id'] == id)
    q = next(x for x in queue if x['id'] == id)
    job_path = cel/'JOB.json'; reg_path = cel/'REGISTRATION_PLAN.json'
    job = read(job_path); reg = read(reg_path)
    pr_path = H/'cels'/id.removeprefix('ART-')/'PROVENANCE.json'
    pr = read(pr_path); cat = find_catalog(catalog, id.removeprefix('ART-'))
    assert job['source_frame'] == pr['source_frame'] == cat['source_frame'] == state['existing_source_canonical_frame'] == row['source']
    assert job['source_pts'] == pr['source_pts'] == cat['source_pts'] == row['pts']
    assert [state['first_frame'], state['last_frame']] == row['first']
    assert [state['first_pts'], state['end_pts']] == row['first_pts']
    assert state['motion_reference_frame_proposal'] == row['motion']
    assert job['output_size_string'] == row['size']
    source = Path(job['source_image']); guide = cel/'inputs/source_pose_guide.png'
    first = Path(state['original_first_scene_frame']); motion = Path(state['motion_reference_path'])
    assert sha(source) == job['source_image_sha256'] == pr['source_png_sha256'] == row['source_sha']
    assert list(Image.open(guide).size) == job['output_size'] == reg['guide_dimensions']
    refs = []
    def copy_ref(name, src, role, crop=None):
        dest = r/'inputs'/name
        assert not dest.exists()
        if crop is None:
            shutil.copyfile(src, dest)
        else:
            with Image.open(src) as im: im.crop(crop).save(dest)
        item = {**rec(dest), 'source': rec(src), 'role': role}
        if crop is not None: item['source_crop_xyxy'] = crop
        refs.append(item)
    copy_ref(f"ref1_ORIGINAL{row['source']}_COMPLETE_UNMASKED_GUIDE.png", guide,
             '唯一当前动作/头身原共同坐标/眼口/双手/衣腰裙及真实下裁；保完整源像素不挖头不移部位。原红身份/尖长额发/双高卷非目标。')
    copy_ref(f"ref2_R{row['motion']}_PURE_HAIR_SECONDARY_ONLY.png", motion,
             row['motion_observation'], row['motion_roi'])
    copy_ref('ref3_USER_CORRECT11_GRAYBOB_IDENTITY_HEAD_COIL_VOLUME.png', identity,
             '本OC中性灰短圆润bob/自然灰刘海贴颊侧发及低LEFT双珠身份，整头卷只给合理相对体量、宽灰前内后返回和渐收C；不改当前源眼口/双手/body/帽位，不固定轴长孔数，不复制图中手臂。')
    copy_ref('ref4_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png', detail,
             '只宽GRAY主面/内后返回实际连通与渐收末C，薄mutedmint材料边；舍精修高光暗内底。无脸root，不定新位置或孤立放大尺寸。', [35,58,146,260])
    assert refs[3]['sha256'] == '0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
    copy_ref(f"ref5_ORIGINAL{row['source']}_OPEN_EYES_CLOSED_SMILE.png", guide,
             row['source_expression']+' 仅只读源眼口，不贴艺术像素。不发送G02半睑bitmap。', row['eyes_roi'])
    copy_ref('ref6_PURE_UNLIT_GRAY_MINT_KEY.png', key,
             '所有bob及gray前/内/后/返回同一无打光灰，较薄mutedmint只为独立材料边；不是高光阴影构造图。')
    assert len(refs) == 6
    provenance = {
        'id': id, 'created_utc': now, 'refs': refs,
        'source_full': rec(source), 'source_guide': rec(guide), 'first_scene_source': rec(first),
        'source_JOB': rec(job_path), 'source_REGPLAN': rec(reg_path),
        'source_PROVENANCE': rec(pr_path), 'catalog': rec(catalog_path), 'catalog_exact_record': cat,
        'PRIORITY_SCOPE': rec(scope_path), 'scope_exact_record': state,
        'NEW40_QUEUE': rec(queue_path), 'original_40_exact_row': q,
        'canonical_frame': row['source'], 'canonical_pts': row['pts'], 'time_base': '1/16000',
        'first_case_frames': row['first'], 'first_case_pts': row['first_pts'],
        'motion_reference': rec(motion), 'REGPLAN_unchanged_expected': reg,
        'no_compact_override': True, 'source_guide_preserved_unmasked': True,
        'read_only_63_64_65_sentinels': sentinels,
        'no_prior_known_generation': {'registry_record': None, 'ID_attempt_result_raw_files': [],
            'project_target_result_attempt_BUILTIN_RELEASE_search': 'rg no matches; exit1; no evidence of prior known/unknown request'},
        'original_art_pixels_edited': False, 'source_crop_only': True,
    }
    put(r, 'INPUT_PROVENANCE.json', provenance)
    continuity = row['root_continuity']
    prompt = '\n\n'.join([
        prefix,
        '主角换成图3的中性灰短圆润bob女孩身份；图1红发和原尖长额发/侧刺不是目标，不仅改色，要本OC短bob、自然灰刘海、贴颊侧发与唯一人物LEFT低耳后双红珠。图1只决定本动作、当前眼口、不同双手/衣身与原裁切；图3不得改变本源眼口/手势/身体。',
        f"为{id}绘制一张完整当前可见人物透明层，图1是原PV{row['source']}唯一表演与共同构图基准，整个人物一次连贯重画。{row['action']}",
        row['source_expression']+' 眼睛只一种深charcoal实色虹膜与普通小圆白点，源白眼/iris露出程度和视线不变；不画黑中心灰环、不套横半睑或夸张瞪圆。暖桃肤、原黑白女仆服/红结金扣、白cap和恰好两片主要黑叶保留。',
        continuity,
        '卷是宽、不透明的GRAY头发带连续绕行：上端宽灰前面向内/后翻回接入下一圈，下端逐圈渐细至正常C，前面与内后返回之间有真实遮挡/露空；不能画独立封口椭圆帽片叠盘、实心锥/柱外贴绿色螺线、薄S线或微型绿挂件，也不做巨粗整束。图3整头肩部上下文给合理相对发量，图4只给宽灰回折连通细节；不套固定孔数/圈数/长轴/全片比例，绝不把不透明灰返回面一律挖成空气。',
        '图2只本时段hair次运动，'+row['motion_observation']+' 不复制AI脸、眼、手、肩体动作或根位。',
        '无独立打光平涂：所有短bob与钻发gray前面/内面/背面/返回都同一灰#B6B4B2，薄mutedmint#B0C8BA只是绕行材料边。用线与互遮表达结构，不用重复深灰内底、银白边、渐变或发光；图4原精修光影不复制。',
        row['canvas']+f" 输出{row['size']}，仅真实透明人物，实际空气为alpha0、灰发带与白裙黑衣仍不透明。无背景/粉色字幕/独立道具/棋盘格。"
    ])+'\n'
    prompt_path = r/'prompt_api.txt'
    assert not prompt_path.exists(); prompt_path.write_text(prompt, encoding='utf-8')
    draft = {
        'id': id, 'operation_kind': f"FIRST_API_whole_visible_character_source{row['source']}_PREPONLY",
        'InputImages': [x['path'] for x in refs], 'reference_sha256': [x['sha256'] for x in refs],
        'PromptFile': str(prompt_path), 'prompt_sha256': sha(prompt_path),
        'OutputDirectory': str(r), 'OutputFileName': 'character_api_original.png',
        'Stage': f"{id} FIRST source{row['source']} explicit graybob source own palms candidate",
        'Size': row['size'], 'Quality': 'high', 'Background': 'transparent', 'n': 1, 'automatic_retries': 0,
        'source_frame': row['source'], 'source_pts': row['pts'], 'first_case_frames': row['first'], 'first_case_pts': row['first_pts'],
        'dispatchable_by_artist': False, 'root_must_personally_release_and_send': True,
        'identity_change_explicit': True, 'API_calls_before': 0, 'native_calls': 0,
        'central_writes': False, 'art_accepted': False, 'dynamic_validated': False,
    }
    dr = put(r, 'DRAFT_API_REQUEST.json', draft)
    put(r, 'SOURCE_OBSERVATION_PRIVATE_PREPONLY.json', {
        'id': id, 'created_utc': now, 'canonical': [row['source'],row['pts']],
        'first': row['first'], 'first_pts': row['first_pts'],
        'action': row['action'], 'eyes_mouth': row['source_expression'],
        'source_difference': row['difference'], 'source_canvas_cutoff': row['canvas'],
        'LEFT_root_and_continuity': continuity, 'AI_hair_only_observation': row['motion_observation'],
        'source_reuse_not_alias': job.get('source_reuse_scope'),
        'source_review_paths': [str(source),str(guide),str(first),str(motion)],
        'actual_viewed_reference_review_to_follow': True,
        'prior_known_candidate': False, 'root_send_release': False,
        'generation_calls': 0, 'dynamic_validated': False,
    })
    put(r, 'NO_PRIOR_REQUEST_KNOWN_PREPONLY.json', {
        'id':id, 'checked_utc':now,'original_40_member':True,'central_registry_record':None,
        'target_raw_result_attempt_files': [],'project_result_attempt_BUILTIN_RELEASE_search_no_matches':True,
        'new_private_prep_only':True,'no_existing_unknown_to_retry':True,
        'no_HTTP_execution_or_attempt_created':True,'no_claim_of_API_art_result':True,
    })
    print(json.dumps({'id':id,'run':str(r),'draft':dr,'prompt':rec(prompt_path),'refs':[rec(x['path']) for x in refs]}, ensure_ascii=False))
