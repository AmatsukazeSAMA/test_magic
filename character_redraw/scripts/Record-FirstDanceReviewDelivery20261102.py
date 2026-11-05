"""Register a review delivery without granting dynamic or user acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
proof = base / 'review/firstdance_review_delivery_registration_20261102_v01'
assert not proof.exists()
proof.mkdir()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.relative_to(root)), 'sha256': sha(p)}
save = lambda p, q: p.write_text(json.dumps(q, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
archive = root / 'art/20261102_first_dance_66states_review_v01.zip'
assert sha(archive) == 'd76e9885c9a88166d726106eecdb085800644d27f86b648a2d5994672fd58293'
delivery = {'archive': ev(archive), 'bytes': archive.stat().st_size,
    'receipt': ev(archive.with_suffix('')/'DELIVERY_RECEIPT.json'),
    'Sol_technical_audit': ev(base/'review/DELIVERY_TECHNICAL_AUDIT_SOL_FIRST_DANCE_20261102_v01.json'),
    'source_frame_range': [834,1133], 'static_reviewed_drawings':66,
    'bound_and_render_readback_verified_exposures':300,
    'continuous_visual_playback_validated':False, 'user_accepted':False, 'goal_complete':False}
preview = root/'art/20261102_dance_curl_updown_current_v02'
sequence = {'comparison': ev(preview/'curl_updown_original_current_detail.png'),
    'quarter_speed_video': ev(preview/'F1053-F1074_original_vs_current_quarter_speed.mp4'),
    'display_frames':[1054,1058,1066,1070,1071],
    'fresh_Sol_sequence_static_review': ev(base/'review/sol_xhigh_round184.json'),
    'root_actual_observation': 'Root actually viewed full source1058/1066/1070, current55/56/57 white QA, and all five currently bound columns on the v02 original/current/detail board. Static upswing/outward/down stages visible. 56 to57 visible coil compacts markedly;57 to58 reopens. This cannot be excused entirely as occlusion or certified smooth without actual playback. Mint/C edge breadth55/56 remains open P2. No new art/selection changes.',
    'actual_continuous_playback_validated':False, 'new_generation_calls':0,
    'registry_art_selection_changed_by_this_review':False, 'user_accepted':False}
save(preview/'ROOT_SEQUENCE_PRESENTATION_REVIEW.json', sequence)
now = datetime.now(timezone.utc).isoformat()
for name, path in [('CURRENT_SELECTION',root/'CURRENT_SELECTION.json'),
                   ('GOAL_EXECUTION',base/'GOAL_EXECUTION.json')]:
    shutil.copyfile(path, proof/(name+'_BEFORE.json'))
    q=read(path)
    q['updated_utc']=now
    q['latest_first_dance_review_delivery']=delivery
    q['latest_curl_updown_review_preview']=sequence
    save(path,q)
readme=root/'README.md'
shutil.copyfile(readme,proof/'README_BEFORE.md')
text=readme.read_text(encoding='utf-8-sig')
paragraph=('首段舞蹈 F834–1133 的 66 稿已完成主审、Sol xhigh 静态复核及 300 曝光定位绑定，'
    '[审阅压缩包](art/20261102_first_dance_66states_review_v01.zip)含原片截取、人物原速／慢速片、透明层及对照图。'
    '[F1058 上扬至 F1070 回落的现稿对照](art/20261102_dance_curl_updown_current_v02/curl_updown_original_current_detail.png)'
    '另附四分之一速度片；56→57卷束收紧、57→58展开仍需连续播放检查。实际连续播放和用户艺术验收尚未完成，全片 GOAL 保持执行。\n\n')
first=text.index('\n\n')+2
readme.write_text(text[:first]+paragraph+text[first:],encoding='utf-8')
save(proof/'DELIVERY_POINTER_REGISTRATION.json',{'created_utc':now,'delivery':delivery,
    'sequence':sequence,'new_generation_calls':0,'goal_complete':False})
print(json.dumps({'registered':str(proof),'goal_complete':False},ensure_ascii=False))
