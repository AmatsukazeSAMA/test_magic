"""Readback hashes and manifest for unselected camera PREP, never central writes."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p): return {'path': str(Path(p)), 'sha256': sha(p)}
def save(p, obj):
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))

order = ['ART-X01-06_F004040', 'ART-X01-07_F004045', 'ART-X01-08_F004051',
         'ART-G51-05_F004599', 'ART-G51-06_F004602', 'ART-G51-07_F004606',
         'ART-G51-08_F004613', 'ART-G13-17_F003726_WIDER', 'ART-G13-17_F001277']
revised = {order[i] for i in [3, 4, 7, 8]}
observations = {
order[0]: [
    'Own upright high index, other low flat palm and tiny closed mouth; joint eyes/wrist/waist/knees/shoes broadly follow native4040. Complete shoes remain visible.',
    'Cap/high wrist and some contours remain roughly5-15px above original; identity bob width cannot be expected to match red hair pixelwise. Root and another independent reviewer must judge the residual.'],
order[1]: [
    'Own left-turn bent high index, opposite low flat palm, closed mouth and skirt/backties retained. Original foreground shoe cutoff projects outside1080; rear shoe remains complete. No shoe invented.',
    'Cap/hair crown reads roughly25-35px higher and eyes/high wrist roughly10-17px higher than original, while waist/ankle placement is closer. This is a residual joint-fit concern for root/independent actual review; whole translation cannot remove it without moving the closer waist/shoes.'],
order[2]: [
    'Own crossed waist gloves with outward fingers and tinyO, bent legs, skirt/backties and two complete shoes follow native4051.',
    'Small bob/cap, waist and shoe contour differences remain. This PREP does not clear existing artistic P2.'],
order[3]: [
    'Own relaxed rightward eyes/tiny closed mouth, two unequal-height gloves, skirt/backties and complete feet retained. v02 whole factor.985 about native(935,1030) improves head/eyes/waist together versus initial.',
    'Minor head/hand/cloth contour differences remain; no local geometry changed.'],
order[4]: [
    'Own two gloves near same height with different near inward-folded wrist/fingers versus far long separated fingers, tilted head/body, right-flared skirt and full shoes retained.',
    'Initial whole was too tall with high head and low shoes; v02 whole factor.96 about native(900,480) improves the joint fit. Small fingertip/head contours remain.'],
order[5]: [
    'Own closed lashes, diagonal single visible glove, hidden far hand, leaning body, long white backties and complete shoes retained. Cap about10px high and feet about7px low remain minor fit differences.',
    'Existing shoulder-depth/occluded low-root P2 is preserved: front_shoulder_route_certified=false. Photography does not certify hidden geometry or move the curl.'],
order[6]: [
    'Own relaxed half-open eyes, bent forearm and lowered visible glove, hidden other hand, own skirt/legs and two complete shoes retained.',
    'Head/eye/cap reads about10-15px high while wrist/waist is closer; residual art/camera judgment remains. front_shoulder_route_certified=false is unchanged.'],
order[7]: [
    'Own production wider3726 camera independently fitted using eyes, collar/gold, crossed bare hands/wrists and waist. New whole retains removed isolated left under-eye dots and right directional lashes.',
    'Initial canvas-fit was too small/high with actual entitycut inside1080. v02 fits shared head/hands/waist more closely and puts raw entitycut1347 at1118.026. No hidden legs or apron extension; minor head-axis/cuff/hand differences remain.'],
order[8]: [
    'Own canonical1277 is the closer camera, not copied from wider3726. Larger v02 jointly follows own face/gold/crossed bare hands/wrists and partial waist crop.',
    'Initial canvas-fit was too small/high with entitycut inside1080. v02 physicalcut is1270.322; no hidden legs or stretched clothing. Minor head-axis/hand/cap differences remain.']
}
snapshot = read(OUT/'TARGET_REGISTRY_READONLY_SNAPSHOT.json')
registry = read(BASE/'ASSET_REGISTRY.json')
index_path = BASE/'review/STATIC_1080P_CANDIDATES_INDEX_20261103_v02.json'
existing = read(index_path)
assert not set(snapshot) & {x['id'] for x in existing['entries']}
timeline_path = Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json')
timeline = read(timeline_path)
cases = []
seen_inputs = {}
for key in order:
    init = OUT/key/'UNSELECTED_UNIFORM_PROPOSAL.json'
    final = init.parent/'whole_uniform_joint_extent_revision_v02/UNSELECTED_UNIFORM_PROPOSAL.json' if key in revised else init
    d = read(final)
    cur = registry[d['id']]
    assert cur['sha256'] == snapshot[d['id']]['sha256'] == d['raw']['sha256']
    assert cur['primary_static_pass'] and cur['independent_static_pass']
    assert sha(cur['image']) == d['raw']['sha256']
    assert timeline[d['source_frame']]['frame'] == d['source_frame']
    assert timeline[d['source_frame']]['pts'] == d['source_pts']
    assert d['scale'] > 0 and not d['selected'] and not d['photography_pass']
    for item in d['preserved_inputs']:
        assert sha(item['path']) == item['sha256'], item['path']
        seen_inputs[item['path']] = item
    for item in [d['unselected_layer'], *d['surfaces'].values(), d['same_native_comparison']]:
        assert sha(item['path']) == item['sha256'], item['path']
    with Image.open(d['unselected_layer']['path']) as im:
        assert im.size == (1920,1080) and im.mode == 'RGBA'
    if d['entity_cut_raw_y'] is not None:
        assert d['entity_cut_projects_y'] >= 1082
    rawdir = Path(d['raw']['path']).parent
    # All these files were actually opened at original size in this logical task.
    viewed_paths = [d['raw']['path'], str(rawdir/'qa_white.png'), str(rawdir/'qa_black.png'),
                    d['source']['path'], *[x['path'] for x in d['surfaces'].values()],
                    d['same_native_comparison']['path']]
    if key in revised:
        viewed_paths.append(read(init)['same_native_comparison']['path'])
    actual = [ev(p) for p in dict.fromkeys(viewed_paths)]
    cases.append({
        'id': d['id'], 'case_key': key, 'status': 'UNSELECTED_PHOTOGRAPHY_PREP_ONLY',
        'proposed_geometry_not_selected': ev(final), 'preserved_initial_proposal': ev(init),
        'raw': d['raw'], 'raw_dimensions': d['raw_dimensions'], 'source': d['source'],
        'source_frame': d['source_frame'], 'source_pts': d['source_pts'], 'timebase': '1/16000',
        'scale': d['scale'], 'translation': d['translation'],
        'entity_cut_raw_y': d['entity_cut_raw_y'], 'entity_cut_projects_y': d['entity_cut_projects_y'],
        'strong_art_last_pixel_row_projects_y': d['strong_art_last_pixel_row_projects_y'],
        'transparent_unselected_layer': d['unselected_layer'], 'surfaces': d['surfaces'],
        'same_native_comparison': d['same_native_comparison'],
        'comparison_native_crop_xyxy': d['comparison_native_crop_xyxy'],
        'actual_viewed': actual, 'prep_observation_after_actual_view': observations[key],
        'retained_artistic_static_review': {'primary': d['primary_static_review'], 'independent': d['independent_static_review']},
        'JOB': d['JOB'], 'original_REGISTRATION_PLAN': d['original_REGISTRATION_PLAN'],
        'front_shoulder_route_certified': d['front_shoulder_route_certified'],
        'selected': False, 'photography_pass': False,
        'root_and_another_independent_actual_photography_review_pending': True,
        'production_binding': False, 'all_exposures_reviewed': False,
        'dynamic_validated': False, 'user_accepted': False
    })
manifest = {
    'report': 'EIGHT_MORE_CURRENT_STATIC_STATES_NINE_SOURCEFRAME_UNSELECTED_PHOTOGRAPHY_PREP',
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'prepared_by': 'Sol xhigh camera PREP and actual QA observations; not ROOT PRIMARY or independent photography acceptance',
    'scope': '8 exact current static states,9 separately fitted own-source single-frame camera candidates; no exposure/temporal approval.',
    'method': 'One positive whole uniform RGBA bicubic affine from unchanged raw; no localwarp/painting/alpha cleanup/recolor. Native pair uses identical x-crop,full1080 height and no resize.',
    'cases': cases,
    'target_registry_snapshot': ev(OUT/'TARGET_REGISTRY_READONLY_SNAPSHOT.json'),
    'registry_readback_all_eight_exact_target_raw_sha256_match': True,
    'preserved_inputs_readback': list(seen_inputs.values()),
    'source_pts_readback': ev(timeline_path),
    'existing_eleven_candidates_index_readonly_not_modified_by_this_task': ev(index_path),
    'tooling': [ev(OUT/'build_unselected_uniform_qa.py'),ev(OUT/'revise_whole_joint_extent_only.py'),ev(Path(__file__))],
    'root_attention': [
        'X01-07 crown/eyes/highwrist is above original while waist/ankle is closer; actual independent judgment required, no false numerical/art pass.',
        'G51-05/06 and both G13-17 cases use v02; all initial candidates remain intact.',
        'X01-07 source foreground shoe is originally truncated; cut1099.64 outside1080 is preserved, rear shoe complete.',
        'G13-17 physicalcut1347,notcanvas1381, projects1118.026 wider3726 and1270.322 canonical1277; both cameras remain separate.',
        'G51-07/08 shoulder-depth/hiddenroot P2 and all retained static-art P2 are not cleared by photography.',
        'User X01 baseline is curl drawing only, not wholecharacter/fixedsize/axis/camera acceptance.'
    ],
    'generation_calls': 0, 'network_calls': 0, 'central_JOB_REG_registry_binding_modified': False,
    'selected': False, 'photography_pass': False, 'production_binding': False,
    'root_and_another_independent_actual_photography_review_pending': True,
    'all_exposures_reviewed': False, 'dynamic_validated': False, 'actual_playback': False, 'user_accepted': False
}
mp = OUT/'FINAL_PHOTOGRAPHY_PREP_MANIFEST.json'
save(mp, manifest)
lines = ['8状态 / 9个源帧未选中摄影准备。仅整张正比例缩放和平移；root与另一独立Sol实看摄影审核待完成。', '',
         '| 状态 / own源帧 | PTS(1/16000) | scale | tx,ty | 实体底切/自然末行y |', '|---|---:|---:|---|---:|']
for c in cases:
    bottom = c['entity_cut_projects_y'] if c['entity_cut_projects_y'] is not None else c['strong_art_last_pixel_row_projects_y']
    lines.append(f"| {c['id']} / {c['source_frame']} | {c['source_pts']} | {c['scale']:.12f} | {c['translation'][0]:.6f}, {c['translation'][1]:.6f} | {bottom:.3f} |")
lines += ['', 'G51-05/06、G13-17两摄影使用各自whole_uniform_joint_extent_revision_v02，其余使用初案；初案全部保留。', '',
          '待root关切：X01-07帽发顶比原较高而腰踝更近，需另审画法/比例残差；原前鞋裁线已出1080且不补鞋。G13-17两真实相机分别拟合，实体cut1347已出画，无隐藏腿或拉衣。G51-07/08肩前深度P2仍未认证。', '',
          '所有9份最终完整白黑/pink与同坐标对照、8份current raw白黑、9份own native均已实际打开；各JOB/REG和精确current raw/PTS已读取核对。', '',
          '原图/源/JOB/REG字节hash保持；9层均1920×1080 RGBA。0生成/网络/中央表/绑定修改，无摄影通过、曝光/动态/用户验收。', '',
          f'Manifest SHA256: {sha(mp)}', '']
md = OUT/'PREP_SUMMARY.md'
assert not md.exists()
md.write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'manifest': ev(mp), 'summary': ev(md), 'case_count':len(cases),
                  'target_count':len(snapshot), 'all_target_current_sha_match':True,
                  'preserved_input_count':len(seen_inputs),
                  'geometry':[{k:c[k] for k in ['case_key','source_pts','scale','translation','entity_cut_projects_y']} for c in cases]}, ensure_ascii=False,indent=2))
