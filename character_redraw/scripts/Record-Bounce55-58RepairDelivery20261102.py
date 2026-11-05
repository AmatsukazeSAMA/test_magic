"""Publish current local review pointers after the two user-rejected cels were repaired."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root = Path(__file__).resolve().parents[1]
base = root / 'art/full_character_redraw_1080p_v01'
proof = base / 'review/firstdance_bounce55_58_repair_delivery_20261102_v02'
assert not proof.exists()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
ev = lambda p: {'path': str(p.relative_to(root)), 'sha256': sha(p)}
save = lambda p, q: p.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
archive = root / 'art/20261102_first_dance_66states_review_v02.zip'
assert sha(archive) == '7f1bae1235184aa91eb61dd620db1c34337f3dd590c4b2bd35d8943f9a7a4229'
receipt = archive.with_suffix('') / 'DELIVERY_RECEIPT.json'
q = read(receipt)
assert q['exposures'] == 300 and q['unique_artworks'] == 66 and q['all_bindings_current']
assert q['actual_continuous_playback_validated'] is False
registry = read(base / 'ASSET_REGISTRY.json')
expected = {'ART-G12-55': 'e64ff52de791e318279b7d34bed005b301db06ce9fe14f4787d055292d04e22d',
            'ART-G12-58': 'b65d6600a743d36a03a883d698cab9cb54527efe4d8a139720bee52f315d14be'}
art = {r['id']: r for r in q['artworks']}
for work_id, digest in expected.items():
    assert registry[work_id]['sha256'] == art[work_id]['raw_sha256'] == digest
    assert sha(Path(registry[work_id]['image'])) == digest
progress = read(base / 'dance_first10_reference_redraw_v01/PROGRESS.json')
assert progress['current_policy_static_reviewed_states'] == 66
assert progress['current_policy_asset_bound_exposures'] == progress['actual_render_binding_verified_exposures'] == 300
preview = root / 'art/20261102_dance_curl_updown_current_v05'
assert read(preview / 'MANIFEST.json')['input_video_package_receipt_sha256'] == sha(receipt)
proof.mkdir()
paths = {'CURRENT_SELECTION': root / 'CURRENT_SELECTION.json',
         'GOAL_EXECUTION': base / 'GOAL_EXECUTION.json'}
for name, p in paths.items():
    shutil.copyfile(p, proof / (name + '_BEFORE.json'))
for name, p in [('README', root / 'README.md'), ('BASE_README', base / 'README.md')]:
    shutil.copyfile(p, proof / (name + '_BEFORE.md'))
delivery = {'archive': ev(archive), 'bytes': archive.stat().st_size,
    'receipt': ev(receipt), 'source_frame_range': [834, 1133],
    'static_reviewed_drawings': 66, 'bound_and_render_readback_verified_exposures': 300,
    'repaired_source_frames': [1058, 1071], 'current_repaired_whole_sha256': expected,
    'production_static_candidate_package': True,
    'continuous_visual_playback_validated': False, 'user_accepted': False, 'goal_complete': False}
sequence = {'comparison': ev(preview / 'curl_updown_original_current_detail.png'),
    'quarter_speed_video': ev(preview / 'F1053-F1074_original_vs_current_quarter_speed.mp4'),
    'display_frames': [1054, 1058, 1066, 1070, 1071],
    'root_actual_observation': 'Root actually viewed current five-column original/current/detail board. New55 has continuous gray front-return-next/taperedC, same lowroot and moderate starting out/up movement; new58 has continuous compact returns rather than old closed caps/graybean and keeps foreground hand/frill occlusion. All columns use the same camera crop/scale. 56-to57 visible coil compaction and57-to58 expansion still require actual continuous playback; board/encoded timing do not certify smoothness.',
    'actual_continuous_playback_validated': False, 'new_generation_calls': 0,
    'artwork_modified_by_presentation': False, 'user_accepted': False}
save(preview / 'ROOT_SEQUENCE_PRESENTATION_REVIEW.json', sequence)
now = datetime.now(timezone.utc).isoformat()
for name, path in paths.items():
    value = read(path)
    if value.get('latest_first_dance_review_delivery'):
        save(proof / (name + '_PREVIOUS_DELIVERY_POINTER.json'), value['latest_first_dance_review_delivery'])
    value.update({'updated_utc': now, 'latest_first_dance_review_delivery': delivery,
                  'latest_curl_updown_review_preview': sequence,
                  'latest_user_curl_repair': {'source_frames': [1058, 1071],
                      'rebound_exposures': [1058, 1059, 1060, 1061, 1071, 1072, 1073, 1074],
                      'old_user_rejected_art_preserved': True,
                      'art_reviews': [ev(base / 'review/sol_xhigh_round190.json'), ev(base / 'review/sol_xhigh_round187.json')],
                      'status': 'fresh_static_art_and_uniform_placement_candidates_bound',
                      'user_accepted': False, 'dynamic_validated': False}})
    save(path, value)
readme = root / 'README.md'
text = readme.read_text(encoding='utf-8-sig')
marker = '当前 **全片人物绘制 GOAL 正在执行**'
assert marker in text
intro = ('# 魔术之心 · PV 人物重绘\n\n'
    'F1058、F1071 已按最新复看重绘钻发，完成新主审、Sol xhigh 静态复核及对应8曝光重新定位绑定。'
    '首段 F834–1133 当前66稿静态候选、300曝光绑定及渲染回读；'
    '[新版审阅包](art/20261102_first_dance_66states_review_v02.zip)、'
    '[相邻五稿与原PV对照](art/20261102_dance_curl_updown_current_v05/curl_updown_original_current_detail.png)、'
    '[四分之一速度对照](art/20261102_dance_curl_updown_current_v05/F1053-F1074_original_vs_current_quarter_speed.mp4)。'
    '实际连续播放检查、相邻稿动态平顺及用户艺术验收仍待完成，全片GOAL未完成。\n\n'
    '旧v01审阅包、用户否决稿和各轮失败返图完整保留为历史；旧状态见'
    '[修复交接记录](art/full_character_redraw_1080p_v01/review/firstdance_bounce55_58_repair_delivery_20261102_v02/DELIVERY_REGISTRATION.json)。\n\n')
readme.write_text(intro + text[text.index(marker):], encoding='utf-8')
base_readme = base / 'README.md'
text = base_readme.read_text(encoding='utf-8-sig')
text = text.replace('原清单仍有 1929 个未确认复用身份的曝光帧，保留在 `UNRESOLVED_EXPOSURES.json`，不能仅凭任务清单宣称作者全部原画和所有曝光已证明完整。',
                    '最初1929个未归属曝光已完成归属核查，当前未解决归属数为0；这仅证明曝光分类已核清，不代表307项绘制、自评、实际绑定及全片播放均已完成。当前状态以 `PROGRESS.json` 和逐帧台账为准。')
base_readme.write_text(text, encoding='utf-8')
for version, reason in [('v03', 'PNG serialization differs from production-render PNG'),
                         ('v04', 'RGBA hidden RGB differs after transparent rendering; visible pixels and alpha agree')]:
    folder = root / ('art/20261102_dance_curl_updown_current_' + version)
    if folder.exists():
        save(folder / 'PREVIEW_VALIDATION_STOP_NOT_ART_REJECTION.json',
             {'reason': reason, 'artwork_changed': False, 'generation_calls': 0,
              'canonical_preview': str(preview), 'video_not_exported_in_this_failed_preview': True})
save(proof / 'DELIVERY_REGISTRATION.json', {'recorded_utc': now, 'delivery': delivery,
    'sequence': sequence, 'generation_calls_in_this_registration': 0,
    'goal_complete': False, 'user_accepted': False})
print(json.dumps({'delivery': str(archive), 'preview': str(preview),
                  'registration': str(proof), 'goal_complete': False}, ensure_ascii=False))
