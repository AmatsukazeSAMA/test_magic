"""Create G49-01 v02 inputs and prompt only. Never lock, Preview, release or send."""
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib
import json
import shutil

run = Path(__file__).resolve().parent
root = next(p for p in run.parents if (p / 'image_defaults.json').is_file())
base = root / 'art/full_character_redraw_1080p_v01'
jobrun = run.parent
old = jobrun / 'prep_first_api_source4401_rearLEFT_graybob_endingclothes_v01'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
ev = lambda p: {'path': str(Path(p).resolve()), 'sha256': sha(p), 'bytes': Path(p).stat().st_size}

def save(name, value):
    p = run / name
    assert not p.exists(), f'Preserve existing evidence: {p}'
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

assert not (run / 'inputs').exists(), 'Preparation is immutable after creation.'
defaults = read(root / 'image_defaults.json')
prefix = defaults['generation_prompt_prefix']['text']
policy = base / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v04.json'
requirements = read(policy)
assert requirements['turn_construction']['large_turns'] == 2
assert requirements['turn_construction']['small_terminal_turns'] == 1
job = read(jobrun / 'JOB.json')
source = Path(job['source_image'])
assert job['source_frame'] == 4401 and job['source_pts'] == 2350080
assert sha(source) == job['source_image_sha256'] == '53fd205a873707fdfc5aa4acc42b7a2b4d129aa8a1906adce79813ca4d8b367d'
auth = base / 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
flat = base / 'inputs/user_curl_two_large_one_small_flat_20261102_v04.png'
identity = base / 'inputs/user_curl_two_large_one_small_identity_20261102_v04.png'
assert sha(flat) == 'ceebb6d5b7968f6a8774c39b0a70cda040b20d2aa8536386071490fe2ed2c6c2'
assert sha(identity) == '7be0a65fe0396300223c599b71bf18ddd2d4a17d7ea85240ef3db81542725bf0'
spec = [
    ('ref1_ORIGINAL4401_POSE_AND_VISIBLE_CROP_ONLY.png', jobrun / 'inputs/source_pose_guide.png', 'Only pose, side-back head angle, shared head-neck-shoulder layout, visible face extent, frill/garment cut and crop. Original high red twin curls, background, text and petals excluded.'),
    ('ref2_REVIEWED14_BACK_BOB_ONLY_NO_BEADS_COIL_CLOTHING.png', old / 'inputs/ref2_REVIEWED14_BACK_BOB_ONLY_NO_BEADS_COIL_CLOTHING.png', 'Back-bob identity and simple line grouping only. No old coil, beads or clothes; no transfer of straight-back angle, cap placement or soft shading.'),
    ('ref3_LATEST_USER_FLAT_TWO_LARGE_ONE_SMALL_STRUCTURE.png', flat, 'Primary latest 2-large + 1-small hollow ribbon construction, continuous opaque gray return and taper. No source face, eye-under dots, hands, clothing, root projection or universal hanging direction.'),
    ('ref4_USER_SELECTED_ENDING_CLOTHING_COLOR_ONLY.png', base / 'inputs/ending_gray_green_clothing_palette_only_v01.png', 'User-selected ENDING clothing color only; preserve actual original4401 garment cut and whites.'),
    ('ref5_PURE_GRAY_HAIR_PIGMENT_ONLY.png', old / 'inputs/ref5_PURE_GRAY_HAIR_PIGMENT_ONLY.png', 'Flat neutral gray hair pigment only, including inner/back returns and small terminal turn. Mint remains a narrow muted material stripe.'),
]
(run / 'inputs').mkdir()
for name, p, role in spec:
    shutil.copyfile(p, run / 'inputs' / name)

prompt = prefix + '''

以参考图1原PV第4401帧为唯一动作、镜头和裁切依据，画当前可见人物，1024×1072透明RGBA。背向身体、头朝画面左侧的侧背头肩大特写；保持原后脑—少量侧脸—颌颈—高领—两肩白褶的共同位置、比例及转向。没有可见眼睛，不新增眼睛、眉睫、正面鼻嘴表情或眼下独立点；没有手，不补手臂手掌、腰腿鞋。原帽顶、黑色两主叶和白帽已经穿过上边界，保持此裁切，不补完整帽，不缩成远景。下方衣身继续原裁切。去掉粉色背景、字幕白字、漂浮花瓣与非人物元素。

把原红双高卷换成短灰bob和唯一一束解剖LEFT低耳后/nape双红珠根的灰宽带卷。图2只控制短灰bob身份及简洁分束线，不控制本镜头后脑角度或帽叶侧别。头颌转向跟图1；LEFT根按本侧背角度的近远与bob遮挡投影，不能照正面固定画右，不能把远侧根移到近耳，也不能镜像人物。根珠可以被bob遮住，不抬到帽边或头冠，不为露珠补出原不可见耳朵。只留同一束单卷，原画两边高根大红卷的形状和体量都不复刻。

图3是最新用户认可的平涂钻发结构，优先于旧参考：固有结构为两个大卷加一个小末卷，不是三个等大卷，也不增加第四圈。整个卷是一条连续宽GRAY发带绕空心轴翻回：宽灰正面沿实际不透明灰内/背返回，斜向接下一大转，再连到小末卷自然收尖卷钩。灰色返回是实体，实际露空处才透明；必须读出同一条束的前后回折，不能实心柱锥、封口灰片、叠碗盘盖、断卷，或绿线绕着灰柱。小卷与上方连续，不能拆成独立尾环。整体体量适合当前完整头肩，既不巨大粗柱也不小饰品。当前侧背角度、bob和肩褶可隐藏部分卷面，不为凑三个可见孔移动遮挡、拉长卷或补画隐藏段。图3的脸、眼下独立点、手、衣服和正面悬挂方向都不使用。

bob、两大卷的全部主面和内后返回、小末卷均按图5中性灰同类平涂。薄荷挑染仅窄柔和材料条，不占宽正面、宽返回或整块末卷。无大绿面、独立深灰底板、银白闪片、渐变、金属光和第二光源。保持原PV手书黑线的粗细起伏、简笔轮廓和相对线宽，不向量化平滑，不添密发丝或精修插画光泽。

图4仅提供用户选择的ENDING低饱和灰绿色衣服色样。把图1可见红立领、肩下红衣片和下边所露红主布料改为这款灰绿，立领折线、白肩褶和服装cut仍按图1；白帽/白褶保持白，黑主叶保持黑，皮肤暖浅色，若红珠可见仍为红。衣服灰绿不移到头发；不从图4新增胸结、围裙、完整身体或双手。输出只含可见人物，空气与非人物区域透明。
'''
prompt_path = run / 'prompt_api.txt'
assert not prompt_path.exists()
prompt_path.write_text(prompt, encoding='utf-8')
refs = [run / 'inputs' / x[0] for x in spec]
draft = {'PromptFile': str(prompt_path), 'InputImages': [str(p) for p in refs], 'OutputDirectory': str(run), 'Size': '1024x1072', 'Quality': 'high', 'Background': 'transparent', 'OutputFileName': 'character_api_original.png', 'Stage': 'ART-G49-01 FIRST source4401 rearLEFT cropped headshoulders latest hollow two-large-one-small ENDING graygreen'}
save('DRAFT_API_REQUEST.json', draft)
save('INPUT_PROVENANCE_PREPONLY.json', {
    'id': 'ART-G49-01', 'created_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'INPUTS_PROMPT_DRAFT_READY_AWAIT_PROVIDER_UPDATE_BEFORE_FORMAL_LOCK_PREVIEW',
    'source': ev(source), 'source_frame': 4401, 'source_pts': 2350080, 'timebase': '1/16000',
    'JOB': ev(jobrun / 'JOB.json'), 'REGISTRATION_PLAN': ev(jobrun / 'REGISTRATION_PLAN.json'),
    'reference_records': [{**ev(p), 'dimensions': list(Image.open(p).size), 'role': item[2]} for p, item in zip(refs, spec)],
    'identity_geometry_readonly_QA_not_sent': {**ev(identity), 'role': 'Actually viewed corroboration of latest 2+1 identity construction. Excluded from API inputs to prevent polished lighting, face and school costume transfer.'},
    'latest_curl_policy': ev(policy), 'project_consent': ev(auth),
    'bob_crop_provenance': {'origin': str(base / 'drawings/ART-G33-14/v01/whole_imggen_rear_left_cap_neutral_gray_preserve_geometry_v01/qa_white.png'), 'origin_raw_sha256': 'dcbaa05b8546b0887e6e0dba9af9dbb5223c0f5ddc87087ef8a13cdbfcd10b4c', 'crop_xyxy': [215,135,580,295], 'no_coil_policy_pass_inherited': True},
    'actual_viewed_source_reference_paths': [str(p) for p in [jobrun / 'inputs/source_pose_guide.png', *[x[1] for x in spec[1:]], identity]],
    'source_root_projection_observations': ['4401 shows a back/side head turned viewerLEFT, only a narrow face/jaw edge and no visible eye; top cap/leaves and lower shoulder fabric are cropped.', 'Original red twin high roots and plate-like coils do not establish the replacement gray root. Same anatomicalLEFT lowear/nape is projected from this head/jaw orientation; bob may obscure root/beads.', 'ViewerLEFT jaw/shoulder-side exposure is consistent with this back/side turn, but no hidden root connection or invisible turn count is certified. Do not mirror or use a universal screen-side rule.'],
    'transport_directive_pending_provider': {'latest_parent_relayed_user_setting': {'quality': 'high', 'n': 1, 'retry': 1}, 'old_policy_text_retry0_is_not_the_new_transport_authority': True, 'do_not_freeze_old_provider_or_retry0': True},
    'planned_first_api_calls': 1, 'network_calls': 0, 'native_calls_authorized': 0,
    'formal_request_locked': False, 'guarded_preview_executed': False, 'root_release': False,
    'v01_preserved': True, 'central_registry_JOB_REG_binding_modified': False,
    'dynamic_validated': False, 'user_accepted': False,
    'future_review': 'Fresh root and Sol actual source/whole-white-black checks under v04, including 2+1 hollow construction; original-policy static approval is not inherited.'
})
(run / 'README_PREP_ONLY.md').write_text('G49-01 v02: inputs/prompt/draft only.\n\nLatest flat 2-large + 1-small reference replaces old11. The original4401 alone controls back/side pose and visible crop; ENDING clothing remains user graygreen. Identity2+1 actually viewed as corroboration but not sent because its polished material/face/clothes are unnecessary.\n\nParent is updating provider/release helpers for latest user high,n1,retry1. REQUEST_LOCK / API_PREPARED_REQUEST / Preview proof are intentionally not created before that update notification. No Preview, release, attempt, credential access or network. Root must actual-review all inputs and release later.\n', encoding='utf-8')
print(json.dumps({'run': str(run), 'prompt': ev(prompt_path), 'draft': ev(run / 'DRAFT_API_REQUEST.json'), 'provenance': ev(run / 'INPUT_PROVENANCE_PREPONLY.json'), 'network_calls': 0, 'awaiting': 'Parent provider update notification before formal lock/Preview'}, ensure_ascii=False, indent=2))
