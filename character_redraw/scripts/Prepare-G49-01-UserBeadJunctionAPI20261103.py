"""Prepare exactly one new user-requested official API edit; no submission here."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent.parent
base = root / 'art/full_character_redraw_1080p_v01'
run = base / 'drawings/ART-G49-01/v01/api_user_originalref_bead_junction_open_coil_v08'
run.mkdir(parents=True, exist_ok=True)
assert not (run / 'DIRECT_REQUEST.json').exists(), 'Existing request must be preserved.'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def ev(p):
    return {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

temp_reference = Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-47d3df1c-1312-4025-97aa-cc8270b21f99.png')
reference = base / 'inputs/user_original_twoLarge_oneSmall_bead_junction_20261103_v01.png'
if not reference.exists():
    shutil.copyfile(temp_reference, reference)
assert ev(reference)['sha256'] == ev(temp_reference)['sha256']
target = base / 'drawings/ART-G49-01/v01/whole_imggen_user_video_smooth_backbob_v07/character_imggen_original.png'
source = base / 'drawings/ART-G49-01/v01/inputs/source_pose_guide.png'
head = base / 'inputs/user_upper_body_360_hair_structure_20261103_v01/HEAD_R036_GEOMETRY_ONLY.png'
refs = [target, source, head, reference]
prompt = '''Edit image 1 as ONE coherent full-character PV cel. The user specifically rejects the detached bead/side-drill assembly and the solid-looking coil in image 1. Preserve its exact rear-left camera, head turn and cheek sliver, crop, maid cap, black leaves, shoulders, white frills, gray-green costume and compact rounded gray bob. Correct the hairstyle construction using the ORIGINAL DESIGN references 3 and 4.

MOST IMPORTANT, ACTUAL PHYSICAL ROOT: This is one attached side lock from the character's own anatomical LEFT low-ear/nape hair, tied at its base by the TWO RED BEADS, then continuing directly into the gray drill braid. The material sequence is GRAY BOB/SIDE LOCK -> RED BEAD TIE AT THE JUNCTION -> GRAY CURL BRAID. Both beads must touch and straddle the gathered gray hair where the lock leaves the bob. Show a short continuous gray gathered root emerging from the side/nape bob into the bead tie, and the first gray curl beginning immediately below that tie. No transparent/skin/air slit separating the bob from the gathered root or beads. The beads are a hair tie at the junction, not earrings on bare ear skin, separate floating balls, or beads attached only to the end of a detached spring. Use image 3's low bob-to-bead relationship and image 4's actual original-design junction and curl ribbon construction. Preserve a natural short bob edge around this attached root; do not grow long loose nape spikes to bridge it.

HOLLOW OPEN RIBBON COIL: The braid is one broad neutral-gray flat ribbon twisting around an open air core, with a thin pale mint edging. Model the underlying whole braid as TWO LARGE complete loops plus ONE distinctly SMALLER complete loop, then its curled C tip. Each turn has a real gray back/return surface; the interior is an open mouth with the background or naturally underlying surface visible between front ribbon and gray return. In the exposed top loop, make an unmistakable open elliptical mouth with a visible gray inner return surface. Preserve substantial normal gray ribbon width and natural coil diameter, rather than a tiny coil or green wire. Do not fill the center with a solid gray cap, corkscrew cone, stacked gray sausages or opaque slab. Do not erase the real gray return merely to make a gap. Image 4 is the correct two-large/one-small hollow-ribbon drawing reference, not a pose or costume source.

SHOULDER-FRONT ROUTE: This left-side braid hangs in FRONT of her anatomical LEFT shoulder toward the front chest, as in the user's design. In this rear-left view the white foreground shoulder frill and body may naturally hide the lower loops and C tip. Do not force all loops into view or hang the whole coil on the green BACK collar. Keep the exposed loop normally sized and attached at the low root. The back collar remains clean. Correct actual attachment and visible hollow structure rather than hiding the defect or replacing it with a small detached ornament.

REFERENCE ROLES: Image 1 is the full target and exact visible layout. Image 2 is its original PV frame guide, pose/camera/crop only: ignore its old red hair, high bilateral drill shapes, pink background and guide marks. Image 3 is the user's original-design 360 side/rear hair reference, posterior-bob volume and attached low bead junction only: do not copy its realistic shading, mint crown shine, shirt or vest. Image 4 is the user's original flat drawing of the bead junction and hollow two-large/one-small coil only. Keep the target's simple black hand-drawn PV outlines and flat colors. No new face, eyes, hands, extra hair accessories, mirrored laterality, extra body or changed camera. Render a transparent PNG with the same clean lower crop. One output only.'''
defaults = read(root / 'image_defaults.json')
prefix = defaults.get('generation_prompt_prefix', {})
if prefix.get('enabled') and prefix.get('text'):
    prompt = prefix['text'] + '\n\n' + prompt
prompt_path = run / 'prompt_api.txt'
prompt_path.write_text(prompt + '\n', encoding='utf-8')
policy_path = run / 'USER_BEAD_JUNCTION_REQUIREMENT.json'
policy = {
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'user_verbatim': ['钻发和本体头发分离，且偏向实心，使用API对照原图再试一次', '注意红珠子是接在头发和辫子之间的'],
    'material_sequence': '本体灰发/侧发根 -> 双红珠扎结 -> 空心灰色钻发辫',
    'requirements': ['红珠连接在本体头发与辫根之间，灰发根连续进入扎结，不得悬空、贴裸耳作耳饰或与本体分离。', '空心开放卷带，两大完整卷加一小完整卷及C形末梢；可见开口有真实灰色回转面，不得实心灰帽。', '保持低位解剖左侧及左肩前路由；背面允许正常遮挡，但露出部分大小正常。', '保留新视频确定的圆润大分束后发与后颈内收。'],
    'scope': 'Hair junction/open ribbon requirement applies throughout the GOAL; this new edit authorization is one G49-01 logical official API request, high n1 retry1.',
    'rejected_run': ev(target), 'original_design_reference': ev(reference),
    'user_artistic_acceptance': False
}
save(policy_path, policy)
params = {
    'PromptFile': str(prompt_path), 'InputImages': [str(p) for p in refs],
    'OutputDirectory': str(run), 'Size': '1024x1072', 'Quality': 'high',
    'Background': 'transparent', 'OutputFileName': 'character_api_original.png',
    'Stage': 'USER_NEW_ONCE_G49_01_ORIGINALREF_ATTACHED_BEAD_JUNCTION_HOLLOW_COIL'
}
request = {
    'id': 'ART-G49-01', 'source_frame': 4401, 'operation_kind': 'whole_character_redraw',
    'first_drawing': False, 'planned_logical_requests': 1, 'n': 1, 'quality': 'high', 'retry': 1,
    'new_user_authorization': policy['user_verbatim'], 'requirement': ev(policy_path),
    'parameters': params, 'prompt': ev(prompt_path),
    'references': [ev(p) for p in refs], 'actual_viewed_paths': [str(p) for p in refs],
    'same_goal_upload_consent': ev(base / 'review/USER_GOAL_OFFICIAL_API_SCOPE_CONFIRMATION_20261103_v02.json'),
    'provider': ev(root / 'scripts/Invoke-ReferenceImage.ps1'),
    'user_accepted': False, 'dynamic_validated': False
}
save(run / 'DIRECT_REQUEST.json', request)
launcher = '''#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
$request = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'DIRECT_REQUEST.json') -Raw | ConvertFrom-Json -AsHashtable
$apiParameters = $request.parameters
& 'D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1' @apiParameters
'''
(run / 'Submit-Once.ps1').write_text(launcher, encoding='utf-8')
goal_path = base / 'GOAL_EXECUTION.json'
goal = read(goal_path)
save(run / 'GOAL_BEFORE_USER_JUNCTION_REQUIREMENT.json', goal)
old = goal.get('latest_posterior_bob_representative')
if old:
    goal.setdefault('posterior_bob_representative_history', []).append(old)
    old['status'] = 'user_rejected_requires_repair'
    old['user_rejection'] = policy['user_verbatim']
goal['latest_user_bead_junction_requirement'] = ev(policy_path)
goal['review']['mandatory_bead_junction_requirement'] = ev(policy_path)
goal['current_user_turn_scope'] = 'One user-requested official API G49-01 correction against original design: attached bead junction and hollow curl.'
goal['updated_utc'] = policy['recorded_utc']
save(goal_path, goal)
defaults['bead_junction_rule'] = {**ev(policy_path), 'rule': policy['material_sequence']}
save(root / 'image_defaults.json', defaults)
with (base / 'GOAL_CURRENT_REQUIREMENTS.md').open('a', encoding='utf-8') as f:
    f.write('\n红珠连接最新补充：本体灰发/侧发根 → 双红珠扎结 → 空心钻发辫，灰发根须连续进入红珠扎结；红珠不是悬空饰物或耳饰。G49-01 v07已被用户指出与本体分离且偏实心，列为待修。本次新授权官方API一次对照原图修正，high/n=1/retry=1，保留肩前遮挡、正常体量和视频后发结构要求。\n')
print(json.dumps({'request': ev(run / 'DIRECT_REQUEST.json'), 'logical_requests': 1, 'submitted': False}, ensure_ascii=False))
