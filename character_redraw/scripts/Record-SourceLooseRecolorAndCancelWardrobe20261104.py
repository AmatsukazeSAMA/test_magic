"""Record the user's exact loose-hair, reuse and withdrawn-clothing scope."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

root = Path(__file__).resolve().parent.parent
b = root / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.resolve()), 'sha256': sha(p)}
def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

old = b / 'review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v01/POLICY.json'
folder = b / 'review/USER_SOURCE_LOOSE_RECOLOR_ONLY_20261104_v02'
folder.mkdir(parents=True, exist_ok=True)
policy_path = folder / 'POLICY.json'
assert not policy_path.exists(), 'Preserve existing policy version.'
policy = read(old)
policy.update(policy_id='source_loose_recolor_only_20261104_v02', recorded_utc=datetime.now(timezone.utc).isoformat(),
              supersedes=ev(old), recorded_by='root current user clarification',
              user_latest_statements_verbatim=['只需要参考图4的配色', '发型维持原PV散发换色即可',
                  '这里面的也是散发，可以复用不用绘制，注意', '不要换衣服了',
                  '不是按原PV复用，是使用一张散发图复用'],
              prompt_prefix='本稿按原PV散发处理：刘海、发长、分缝、外轮廓、波浪、发梢及遮挡均保持本原片，只参考图4的灰色与薄荷绿配色。脸型、五官、表情、姿势和服装仍按原PV；不改成图4的发型，不加短bob、钻发、扎珠或新发饰。换衣试验已经取消，不采用白裙。',
              wardrobe_rule='Original PV clothing and face must be preserved. The white sleeveless dress trial is withdrawn, not a new costume policy.',
              portrait_reuse_rule='Reuse pixels from one corrected loose-hair artwork, not the original PV red/amber portrait and not the withdrawn white-dress trial. No separate portrait generation.',
              reused_artwork_available_or_bound=False)
for ident, row in policy['states'].items():
    row['source_hairstyle_policy_id'] = policy['policy_id']
    row['generation_allowed'] = ident != 'OPT-BROOCH-PORTRAIT'
    row['preserve_original_PV_clothing_and_face'] = True
    row['render_strategy'] = 'existing_loose_art_reuse' if ident == 'OPT-BROOCH-PORTRAIT' else 'original_PV_loose_shape_recolor_only'
portrait = policy['states']['OPT-BROOCH-PORTRAIT']
portrait['reuse_source_candidates'] = ['ART-G27-01', 'ART-G26-04', 'ART-G28-01']
portrait['reuse_selected_source'] = None
portrait['reuse_dependency'] = 'A corrected source-loose recolor artwork with original PV face/clothing must be available and reviewed before clipping/fitting into the existing brooch aperture.'
portrait['not_author_cel_identity_or_reuse_approval'] = False
portrait['user_authorizes_loose_art_pixel_reuse'] = True
portrait['original_source_role'] = 'Brooch aperture, printed-image framing and exposure context only; not the replacement portrait pixels.'
save(policy_path, policy)

trial = b / 'drawings/ART-G27-01/v01/whole_imggen_user_white_dress_original_loose_recolor_v02'
withdrawal = trial / 'USER_WITHDRAWAL.json'
assert not withdrawal.exists()
save(withdrawal, {'recorded_utc': policy['recorded_utc'], 'id': 'ART-G27-01',
     'user_statement_verbatim': '不要换衣服了', 'status': 'user_withdrawn_wardrobe_trial',
     'trial': ev(trial / 'character_imggen_original.png'),
     'original_PV_clothing_required': True, 'future_white_dress_calls': False,
     'not_a_reuse_source_for_brooch': True, 'user_accepted': False,
     'face_feedback': '是不是脸型变了，实在不行API吧',
     'face_requirement': 'Preserve source face shape, expression and feature arrangement; do not borrow reference4 face.'})

defaults_path, goal_path = root / 'image_defaults.json', b / 'GOAL_EXECUTION.json'
defaults, goal = read(defaults_path), read(goal_path)
save(folder / 'IMAGE_DEFAULTS_BEFORE.json', defaults)
save(folder / 'GOAL_EXECUTION_BEFORE.json', goal)
defaults['source_hairstyle_policy'] = ev(policy_path)
defaults['latest_wardrobe_trial_cancellation'] = ev(withdrawal)
save(defaults_path, defaults)
previous_req = Path(goal['review']['mandatory_curl_requirements']['path'])
req = read(previous_req)
req.update(requirements_revision='goal_curl_assessment_20261104_v07',
           supersedes=ev(previous_req), recorded_utc=policy['recorded_utc'],
           source_hairstyle_scope=ev(policy_path),
           scope_precedence='Curl/bob construction rules apply to tied-drill source scenes. The five exact source-loose entries override them: four original-shape recolors, one portrait reuse from corrected loose artwork.',
           wardrobe_trial_withdrawal=ev(withdrawal))
req['production_priority']['primary'] = '先补未出首图，official API high/n1/retry1；依据本原PV发型模式。散发四项保持原轮廓只换灰mint，胸针头像复用一张合格散发稿而不单独生成。'
req_path = b / 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v07.json'
assert not req_path.exists()
save(req_path, req)
goal.setdefault('source_hairstyle_policy_history', []).append(goal.get('latest_source_hairstyle_policy')) if goal.get('latest_source_hairstyle_policy') else None
goal['latest_source_hairstyle_policy'] = ev(policy_path)
goal['latest_user_wardrobe_cancellation'] = ev(withdrawal)
goal['review']['mandatory_curl_requirements'] = ev(req_path)
goal['latest_curl_assessment_requirements'] = {**ev(req_path), 'requirements_revision': req['requirements_revision'], 'construction_policy_id': req['construction_policy_id']}
goal['updated_utc'] = policy['recorded_utc']
save(goal_path, goal)
with (b / 'GOAL_CURRENT_REQUIREMENTS.md').open('a', encoding='utf-8') as f:
    f.write('\n2026-11-04最新用户范围：G26-04、G27-01、G28-01、G29-01保持各自原PV散发刘海/长度/轮廓/波浪/遮挡，仅参考图4灰色和薄荷绿配色；脸型、五官、原服装不变，不加bob/钻发/扎珠。白裙换衣试验已取消，保留弃用原图，不作新服装或胸针复用源。OPT-BROOCH-PORTRAIT从一张完成且核查合格的散发稿裁取复用，不是复用原PV红发头像，不单独绘制；复用源和实际绑定尚待完成。原307项/4763真实PTS范围保留，不把遮罩摄影阶段另生人物态。\n')
print(json.dumps({'policy': ev(policy_path), 'requirements': ev(req_path), 'withdrawal': ev(withdrawal), 'loose_recolors': 4, 'portrait_reuse_only': 1, 'network_calls': 0}, ensure_ascii=False))
