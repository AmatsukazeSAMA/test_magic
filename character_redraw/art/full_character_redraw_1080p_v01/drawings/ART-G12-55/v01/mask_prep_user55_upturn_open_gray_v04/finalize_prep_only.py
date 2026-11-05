from pathlib import Path
from PIL import Image
import json, hashlib, shutil
from datetime import datetime, timezone

R = Path(__file__).resolve().parent
B = R.parents[3]
PROJECT = B.parents[1]
CEL = R.parent
I = R / 'inputs'
Q = R / 'readonly_QA'
NOW = datetime.now(timezone.utc).isoformat()

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def put(name, obj):
    p = R / name
    if p.exists():
        raise FileExistsError(p)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'path': str(p), 'sha256': sha(p)}

def proof(p):
    p = Path(p)
    d = {'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}
    if p.suffix.lower() == '.png':
        with Image.open(p) as im:
            d.update(size=list(im.size), mode=im.mode)
    return d

assert B.name == 'full_character_redraw_1080p_v01'
assert PROJECT.name == '魔术之心'
defaults = PROJECT / 'image_defaults.json'
prefix = read(defaults)['generation_prompt_prefix']['text']
mask_prov = read(R / 'MASK_PROVENANCE_v01.json')
mask = Path(mask_prov['mask_path'])
target = CEL / 'whole_imggen_reviewed54_source1058_perspective_occlusion_v03' / 'character_imggen_original.png'
target_expected = '71dca7e1c84330c3543cbed29b4222702e2759c102bc4540fd43f018c8e61d8e'
assert sha(target) == target_expected
assert sha(mask) == 'fbf10b76f6cb2f5cf16611760dd288911ccee63ea23234951b24b30133edd057'

ref_names = [
    'ref1_CURRENT55_RAW_KEEP_LOW_LEFT_ROOT_CAP_HANDS_BODY.png',
    'ref2_ORIGINAL1058_COMPLETE_UNMASKED_GUIDE_ACTION_ONLY.png',
    'ref3_USER_GRAY_RETURN_DETAIL_NO_FACE_ROOT.png',
    'ref4_USER_CORRECT11_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png',
    'ref5_ORIGINAL1054_TO_1058_CURL_MOTION_ONLY_COMPARISON.png',
]
expected = [
    target_expected,
    'e8b00bd54311ba910eebfb77437a798acad8659ae76d5bfd64da8dbc68655e03',
    '0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7',
    '216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528',
    'f9a37caf7c1f16708aae6675e7d513f31b58a3e76c87cdba0053db43373757d5',
]
roles = [
    '当前人物完整编辑目标。正确画右远侧LEFT低耳后根/双珠、两片帽叶、bob/脸/颈、手衣身体和底裁保留；旧卷封口实心及下垂相位明确错误，不是几何模板。透明处的隐藏RGB不当作发面。',
    '原1058完整未挖头像guide，独占头倾、眼开度/视线/波形闭口、OK角形与胸前垂指/腕袖、衣装结构及裁切；原红卷不定新身份、根位或材质。',
    '用户最新灰卷细节的只读无脸/无根裁图，只给宽gray前面与返回面连续绕行、真实露空、渐收与末C；不复制精修打光/衣物/根位。',
    '用户认可旧11完整头卷上下文，只给相对头肩体量、连续灰带回折/收尖/C路径；不复制正面圆眼/嘴/抬手/衣姿/垂直轴或新帧根投影。',
    '原PV1054→1058近侧红卷只读对照，仅给从下斜到趋平上提的当前55运动相位；不复制红色、实心画法、近侧根或轴角，不镜像身体或整条轮廓。',
]
refs = []
for n, h, role in zip(ref_names, expected, roles):
    p = I / n
    assert sha(p) == h
    refs.append({**proof(p), 'role': role})

policy = B / 'USER_CURL_F1058_UPSWING_START_AND_SOLID_REJECTION_20261102_v01.json'
audit = B / 'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json'
assert sha(policy) == '6cb24467787c997a18c393154524db43eb3eaca99e326de5eff160e9ba9e9451'
assert sha(audit) == '2aa92df5a178b3a7c97085cfc277932ce1b00744d2f962376ebb47252e9f0319'
a = read(audit)
source55 = next(s for s in a['states'] if s['id'] == 'ART-G12-55')

prompt = prefix.rstrip() + '\n\n' + '''只在所附蒙版透明编辑区修复图1当前人物的可见灰钻发及其上扬轮廓，其他区域保持。人物身体、头倾、脸眼和波形闭口、画右低耳后双红珠根、白maidcap与恰好两片黑叶、双手及衣装、半身底裁均不变，不镜像。图2原PV1058是这些动作、表情、手势、服装和裁切的唯一依据；原红发不复制。

用户指出本稿“钻发又变成实心的了”，并要求从1058这一帧已经开始上扬。把现在封口分段的灰卷改为一束连续的宽灰发带：上端也由宽正面连贯折回内/后返回面，再绕入下一圈，连续渐收；可见末段自然回成C。不是封口椭圆圆片堆、实心锥/圆柱贴绿螺线，也不是薄绿小挂件。真实露出的空气须透明；真正不透明的灰返回面要保留，不能为造洞挖掉。用遮挡和描线表达回折，不画深灰体积内底、高光或渐变。灰色正/内/背/返回面均为与bob相同的平涂灰#B6B4B2，薄荷#B0C8BA仅沿卷面作较薄材料带。

本帧卷体从固定画右远侧低根向外并开始上翻，允许部分上扬段被bob、肩白褶或前景手臂自然遮住。新增编辑空气只是上扬的活动空间，不必填满；不为了展示卷尖或两珠挪根、挪手衣或强露全尾。只转译图5原1054下斜到1058趋平/上提的相位到本人物远侧透视，不镜像原近侧红卷，也不沿54继续完整下垂。后续上下摆动另按逐帧原PV，不把整段设成单调上扬。

图3只给连续宽灰前/返回折与渐收细节，舍弃其打光；图4只给整头肩上下文中的合理固有发量/连续螺旋，不复制它的正面眼口、动作、轴向或占位。体量应与当前头肩协调，既非粗大重卷也非微型挂件；不固定孔数、圈数、长轴或强制露完整卷。不使用R181下垂模板，不把当前坏上端当正确结构。输出独立透明人物，背景、字幕与参考板标签不画入。'''
prompt_file = R / 'prompt_api_draft.txt'
if prompt_file.exists():
    raise FileExistsError(prompt_file)
prompt_file.write_text(prompt + '\n', encoding='utf-8')

snap = R / 'PREP_BEFORE_SNAPSHOTS'
snap.mkdir(exist_ok=False)
snapshots = []
for p in [CEL / 'JOB.json', CEL / 'REGISTRATION_PLAN.json', target.parent / 'request_imggen.json', R / 'MASK_PROVENANCE_v01.json', R / 'READONLY_INPUT_PROVENANCE_v01.json']:
    q = snap / (p.parent.name + '__' + p.name)
    shutil.copyfile(p, q)
    assert sha(q) == sha(p)
    snapshots.append({'original': proof(p), 'snapshot': proof(q)})

draft = {
    'schema': 'magic-maid.masked-hair-repair-prep-only/1',
    'id': 'ART-G12-55', 'created_utc': NOW,
    'state': 'DRAFT_READY_WITHOUT_SUBMIT', 'dispatchable': False,
    'operation_kind': 'masked_visible_curl_topology_and_current1058_upswing_repair',
    'InputImages': [x['path'] for x in refs],
    'reference_sha256': expected, 'references': refs,
    'PromptFile': str(prompt_file), 'prompt_sha256': sha(prompt_file),
    'MaskFile': str(mask), 'mask_sha256': sha(mask),
    'OutputDirectory': str(R), 'OutputFileName': 'character_api_original.png',
    'Size': '1104x1424', 'Quality': 'high', 'Background': 'transparent',
    'n': 1, 'automatic_retries': 0,
    'provider': 'configured official OpenAI images/edits',
    'model': 'gpt-image-2.5-sunburst',
    'input_size_exact': [1103, 1426], 'mask_size_exact': [1103, 1426],
    'output_size_is_draft_pending_root_review': True,
    'size_note': '输入与蒙版均保持原1103x1426，不缩放或补画艺术像素。拟输出1104x1424仅为待root核的16倍数近同纵横比画布；若获准，后续仅整人物fit处理，不改局部比例，不宣称Sunburst硬尺寸限制已被验证。',
    'original_target': proof(target),
    'source_frame': 1058, 'source_pts': 564832,
    'first_case_frames': [1058, 1061],
    'root_policy_prefix': {'source': str(defaults), 'source_sha256': sha(defaults), 'text': prefix},
    'mask_provenance': proof(R / 'MASK_PROVENANCE_v01.json'),
    'source_observation': source55,
    'source_phase_audit': proof(audit), 'latest_user_policy': proof(policy),
    'assessment_requirements': proof(B / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'),
    'occlusion_motion_policy': proof(B / 'USER_CURL_OCCLUSION_JUMP_CONTINUITY_20261102_v01.json'),
    'project_broad_authorization': proof(B / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
    'authorization_boundary': '本项仅mask/refs/prompt草案。尚待root实际查看并明确release，不调用审批发送或HTTP。广授权不在此草案内被解释为本项可立即dispatch。',
    'changed_hypothesis': '保住正确root和身体，将错误gray可见卷与其原alpha0外上方空气单独开放；用原1054→1058相位+用户完整头卷体量/灰返回细节替代旧R181压紧下垂及当前封口段。人工trace仅API输入mask，不改最终艺术像素。',
    'local_repair_parent': str(R),
    'mandatory_builtin_whole_after_local': True,
    'fresh_root_and_Sol_required_after_whole': True,
    'formal_API_PREPARED_REQUEST_written': False, 'attempt_written': False,
    'HTTP_started': False, 'API_calls': 0, 'native_calls': 0,
    'central_registry_modified': False, 'art_pixels_modified': False,
    'registration_plan_modified': False, 'bindings_modified': False,
    'quota_resets': 0, 'other_items_touched': False,
    'art_accepted': False, 'dynamic_validated': False,
}
request_proof = put('DRAFT_API_REQUEST.json', draft)

status_proof = put('LOCAL_REPAIR_STATUS.json', {
    'id': 'ART-G12-55', 'created_utc': NOW,
    'state': 'PREP_ONLY_NOT_SUBMITTED', 'local_repair': True,
    'local_repair_completed': False, 'local_repair_result': None,
    'mandatory_whole_redraw': True, 'requires_whole_character_redraw': True,
    'whole_character_redraw_completed': False,
    'operation_kind_after_local': 'whole_character_redraw',
    'fresh_root_review_required': True, 'fresh_independent_review_required': True,
    'patch_must_not_be_adopted': True, 'old_static_pass_inherited': False,
    'target_before': proof(target), 'private_before_snapshots': snapshots,
    'API_calls': 0, 'native_calls': 0, 'dispatchable': False,
})

view_paths = [Path(x['path']) for x in refs] + [
    target.parent / 'qa_white.png', target.parent / 'qa_black.png',
    B / 'coverage/source_frames/F001054.png', B / 'coverage/source_frames/F001058.png',
    Q / 'CURRENT55_ROOT_VISIBLE_COIL_1x_white.png',
    Q / 'CURRENT55_ROOT_VISIBLE_COIL_3x_white.png',
    Q / 'CURRENT55_ROOT_COIL_COORDINATE_GRID_3x_READONLY.png',
    Q / 'MASK_OVERLAY_FULL_white.png', Q / 'MASK_OVERLAY_ROOT_AIR_2x_white.png', Q / 'MASK_OVERLAY_ROOT_AIR_2x_black.png',
]
review = {
    'id': 'ART-G12-55', 'reviewer': 'xhigh_pending_artist', 'created_utc': NOW,
    'scope': 'read-only source/reference/mask-preparation review; no generated repair exists',
    'actual_viewed': [proof(p) for p in view_paths],
    'observations': {
        'current_whole': '画右同侧低红珠根与恰好两黑帽叶可保留；卷体可见正面呈封口分段且仍下垂，需修。头倾、收眼波口、高OK角形及胸前垂指、腕袖交叠、原半身下裁由原1058管辖。',
        'source_phase': '实际看原1054与1058全源及同原像素curl对照：近侧红curl从下斜趋平上提。仅转译此55相位，不镜像原近侧投影到新远侧LEFT根，不假称整个后段单调上扬或已证实起跳。',
        'detail_volume': 'ref3能见宽gray面/返回折与内空，含打光须舍弃；ref4含完整bob/珠/卷渐收+C与头肩体量。其眼口动作均无新帧权威，不以孤立小ROI推测固有发量。',
        'mask_old_region': '红色overlay覆盖当前可见coil，低珠/皮肤/白褶和前景手保持保护；被衣手遮住的尾不作隐藏几何重建。',
        'mask_upward_air': '蓝色overlay仅取原alpha0空气，向bob右外上方开放，并避开两手及OK孔。上方走廊受bob和高掌约束，须root复核是否足以在自然遮挡下上扬；不是要求按mask边界填满或把卷缩细。',
        'mask_boundary_limit': 'manual trace是待root实看输入；像素统计不能保证语义分割或API准确服从。低珠边界保守保护，未来返图需核残旧卷边/接合。',
        'existing_edge_limit': 'target原底缘有白色细碎alpha边，当前mask保护不借此改身体；后续mandatory whole需一起实际检查透明边。',
    },
    'mask': mask_prov,
    'future_full_review_checklist': [
        '根侧/低位/双珠连接稳定，帽白褶+恰好两黑叶不丢不增；身体/手不镜像。',
        '1058本帧可见卷体已上提；远侧透视自然，bob/肩白褶/手臂遮挡合理，不强露末端。',
        '上端及下端均连续宽opaquegray前/返回折、渐收+C；不叠封口片、不实心底贴green螺线，不挖掉grayreturn造洞。',
        '整头肩上下文发量合理，不巨大也不微型；不能因编辑走廊较窄缩掉固有发量。',
        'gray/mint材料平涂，无独立暗体积面/银光/渐变，外露空气真alpha透明。',
        '完整raw白黑+原source同时核眼口/OK孔和其余三指/垂指触点/衣和底裁，alpha边实际看。',
        '局修不能批准；必须builtin whole当前可见整个人物，再freshroot+Sol对新raw实看。',
        '相邻相位按实际逐源态/PTS另评，未做实际播放，不认证动态或隐藏卷形。',
    ],
    'decision': 'DRAFT_READY_FOR_ROOT_REFERENCE_AND_MASK_REVIEW_ONLY',
    'art_pass': False, 'dynamic_validated': False, 'dispatchable': False,
    'API_calls': 0, 'native_calls': 0,
}
review_proof = put('ARTIST_SOURCE_MASK_REFERENCE_REVIEW.json', review)

# Byte-preservation and input-only checks; no invocation of API or native tools.
assert sha(target) == target_expected
assert sha(I / ref_names[0]) == target_expected
with Image.open(mask) as m, Image.open(target) as t:
    assert m.mode == 'RGBA' and m.size == t.size == (1103, 1426)
    hist = m.getchannel('A').histogram()
    assert hist[0] == 26585 and hist[255] == 1546293 and sum(hist[1:255]) == 0
assert not (R / 'API_PREPARED_REQUEST.json').exists()
assert not (R / 'character_api_original.png').exists()
ready = {
    'id': 'ART-G12-55', 'created_utc': NOW,
    'state': 'DRAFT_READY_WITHOUT_SUBMIT', 'dispatchable': False,
    'draft_request': request_proof, 'prompt': proof(prompt_file),
    'mask': proof(mask), 'references': refs,
    'overlay_full_white': proof(Q / 'MASK_OVERLAY_FULL_white.png'),
    'overlay_root_air_white': proof(Q / 'MASK_OVERLAY_ROOT_AIR_2x_white.png'),
    'overlay_root_air_black': proof(Q / 'MASK_OVERLAY_ROOT_AIR_2x_black.png'),
    'artist_review': review_proof, 'local_status': status_proof,
    'source_original_bytes_unchanged': True,
    'formal_API_PREPARED_REQUEST_written': False, 'attempt_written': False,
    'HTTP_started': False, 'API_calls': 0, 'native_calls': 0,
    'central_registry_modified': False, 'exposure_or_progress_modified': False,
    'registration_plan_modified': False, '18_accessed_by_this_finalizer': False,
    'quota_resets': 0, 'needs_root_release_before_dispatch': True,
}
ready_proof = put('DRAFT_READY_WITHOUT_SUBMIT.json', ready)
print(json.dumps({'draft': request_proof, 'prompt': proof(prompt_file), 'mask': proof(mask), 'review': review_proof, 'ready': ready_proof, 'API_calls': 0, 'native_calls': 0}, ensure_ascii=False, indent=2))
