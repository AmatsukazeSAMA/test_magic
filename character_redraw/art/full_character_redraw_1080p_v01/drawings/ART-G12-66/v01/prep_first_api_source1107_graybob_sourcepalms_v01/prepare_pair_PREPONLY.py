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
for id in ['ART-G12-63', 'ART-G12-64', 'ART-G12-65']:
    cel = B/'drawings'/id/'v01'
    sentinels.extend(rec(p) for p in cel.glob('prep*/REQUEST_LOCK.json'))
    sentinels.extend(rec(cel/name) for name in ['JOB.json', 'REGISTRATION_PLAN.json'])

rows = [
    {
        'id': 'ART-G12-66', 'source': 1107, 'pts': 590992,
        'first': [1106, 1109], 'first_pts': [590464, 592592],
        'size': '1440x1072', 'motion': 219, 'motion_roi': [584,188,626,216],
        'eyes_roi': [635,235,850,378],
        'run': 'prep_first_api_source1107_graybob_sourcepalms_v01',
        'source_sha': '8c004174d9cf659bdd7d7223fd140ceb3af9c58ac96fbb2cbc6b636066f4ff3a',
        'action': '原1107近正面直立圆睁眼、小弧闭笑。两臂外摊且画左掌更高，左侧四长指几乎水平向左、拇指独立上竖；画右掌较低，拇指斜上、横向指端轻弯向下。保两手不同掌纹/指间线/腕角与白袖口，不能套65画右斜上分指或图3抬臂。黑长袖、红领结金扣、两侧白肩fan/竖褶、原腰带/腰后两侧白bow与apron到画底的长度，均只取本1107。',
        'canvas': '完整1440x1072原guide、无新trim/无头部挖除/无单部位移动。原1107为半身，围裙黑裙穿过底边，没有可见腿鞋；不能补全隐藏腿鞋或缩短apron留白。双掌极左/极右指端原来都可见，必须完整保留。',
        'difference': '相较65源，66头更直、两摊掌更平更低，画右不再是65向右上分开的长指；画左拇指更直立，袖口/弯肘/腰bow与裙褶均不相同。与后续G33-63也非整人alias，当前66半身底裁而后者canonical全身且手/cuff/腰裙不同。',
        'motion_observation': 'actual R219全帧颈侧卷压紧、局部斜带有回收读法，肩白褶遮住下段。纯hair [584,188,626,216]42x28，排脸眼、红珠/root、白肩饰。小ROI只能给局部回弹压缩，不能证明隐藏圈长/整束轴，也不能据它缩小固有发量或把整卷硬藏肩后。',
        'source_expression': '本1107原圆睁不对称眼弧/虹膜露出、普通小白点、小弧闭笑，以图1与图5为准，不复制图3中性小口或AI眼形。',
    },
    {
        'id': 'ART-G33-63', 'source': 2589, 'pts': 1382176,
        'first': [1110, 1117], 'first_pts': [592592, 596864],
        'size': '832x1072', 'motion': 224, 'motion_roi': [558,204,597,225],
        'eyes_roi': [365,145,500,235],
        'run': 'prep_first_api_source2589_graybob_fullshoes_v01',
        'source_sha': 'eb10ce8881c9ded73c842bc42f094275756ffcadd2f3fcbbadaab4e0d127d306',
        'action': '原2589近正面、头与身体轻侧倾，圆睁眼、短浅折弧闭笑。两臂外伸掌心朝上：画左掌较高，四长指左伸并稍分开、长拇指斜上；画右掌较低，指尖向右、拇指上斜，两侧腕/cuff角度不同。黑长袖红领结金扣、白肩竖褶/袖口、腰白带、画右腰后大bow与下垂带、长apron原锯齿白边/黑裙摆、不同倾角的两小腿和踝带鞋均保。画右鞋尖更低，两鞋都完整可见，不能镜像成同脚或补改重心。',
        'canvas': '完整832x1072未挖头原guide，保canonical2589全裙腿和两只完整踝带鞋；first1110是本状态放大的半身曝光，不能拿它裁掉canonical腿鞋。首次clip摄影缩放/裁边另审，不把全身输出直接称为已定位或动态通过。无新trim、无单部位移动。',
        'difference': 'first1110实际半身眼口/两掌/腰后bow可见，canonical2589是同状态全身来源但摄影尺度与可见下身不同。与前66的画左袖口刻线、右腕/指间线、后bow只向画右、长apron与裙摆都不同，不整人alias；不能拿66半身裁切生成本完整master。',
        'motion_observation': 'actual R224全帧近颈灰卷仍紧凑、局部带稍斜向回收，下端接近白肩frill；纯hair [558,204,597,225]39x21排除眼脸、红珠/root与白frill。AI只有半身不得提供本全身腿鞋/手式。小发段不决定隐藏卷长或固有发量，不能变微型挂件。',
        'source_expression': '本2589圆睁眼、带轻微折角的短闭笑，以图1/5为准；不借66更圆滑笑线/AI表情或正确11中性嘴。',
    },
]

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
    continuity = ('唯一人物LEFT低耳后/nape双红珠根，当前近正面投影在画右同侧bob下，不抬到眼侧/帽边，不镜像身体或把双珠移画左。'
                  '承接63用户指定肩前与64/65转正时的同侧路线：原根不跳边，卷向同侧肩前/胸侧自然延伸，bob/肩褶/手的真实遮挡可盖局部，但不可无理由把整束转到背后或微缩隐藏。'
                  '前63–65当前未有已审新稿，当前仅待核连续性意图，不宣称曝光/动态已通过；本动作仍只按当前source，不复制前稿手眼或固定卷轴。')
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
