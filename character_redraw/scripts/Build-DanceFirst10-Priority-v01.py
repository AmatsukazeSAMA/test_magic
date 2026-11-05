"""Scope the user-prioritized clip against existing true-PTS source states."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
DEST = BASE / 'dance_first10_reference_redraw_v01'


def main():
    DEST.mkdir(exist_ok=True)
    load = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
    ledger = load(BASE / 'coverage/EXPOSURE_LEDGER.json')
    plan = load(BASE / 'REDRAW_PLAN.json')
    registry = load(BASE / 'ASSET_REGISTRY.json')
    ref = BASE / 'inputs/motion_reference_upright_first10_20261031_v01'
    alignment = load(ref / 'F0944_diagnostic/AUDIO_ALIGNMENT.json')
    offset = alignment['reference_video_t0_at_pv_audio_seconds']
    clip_start_pts = round(offset * 16000)
    clip_end_pts = clip_start_pts + 10 * 16000
    frames = [f for f in ledger['frames'] if offset <= f['pts'] / 16000 < offset + 10]
    states = []
    for frame in frames:
        ids = frame.get('resolved_canonical_ids', frame.get('proposed_canonical_ids', []))
        if len(ids) != 1:
            raise RuntimeError(f'Expected separately reviewed single visible drawing binding at {frame["frame"]}: {ids}')
        if not states or states[-1]['id'] != ids[0]:
            states.append({'id': ids[0], 'first_frame': frame['frame'], 'last_frame': frame['frame'],
                           'first_pts': frame['pts'], 'end_pts': min(frame['end_pts'], clip_end_pts),
                           'original_end_pts': frame['end_pts']})
        else:
            states[-1]['last_frame'] = frame['frame']
            states[-1]['end_pts'] = min(frame['end_pts'], clip_end_pts)
            states[-1]['original_end_pts'] = frame['end_pts']
    jobs = {j['id']: j for j in plan['jobs']}
    for n, state in enumerate(states, 1):
        job = jobs[state['id']]
        middle = ((state['first_pts'] + state['end_pts']) / 2) / 16000 - offset
        r = max(0, min(239, int(round(middle * 24))))
        current = registry.get(state['id'], {})
        state.update({
            'order': n, 'existing_source_canonical_frame': job['source_frame'],
            'source_master_kind': job['kind'],
            'current_run': job['run_relative'],
            'motion_reference_frame_proposal': r,
            'motion_reference_path': str(ref / f'frames/R{r:06d}.png'),
            'original_first_scene_frame': str(BASE / f'coverage/source_frames/F{state["first_frame"]:06d}.png'),
            'original_source_master': job['source_image'],
            'legacy_static_status': current.get('status', 'not_drawn'),
            'legacy_selected_image': current.get('image'),
            'latest_flat_hair_and_motion_review': 'pending_actual_per_state_review',
            'motion_reference_frame_proposal_actual_pose_checked': False,
            'placement_for_this_clip_actual_reviewed': False,
            'dynamic_validated': False,
            'reuse_boundary': 'Existing source ID is preserved. A shared full-body source master may serve a zoomed/cropped first-scene appearance only after actual per-appearance scale/crop registration. Do not show hidden legs in the clip or call canonical output placement the first-scene placement.',
        })
    obj = {
        'schema': 'magic-maid.dance-first10-priority/1',
        'updated_utc': datetime.now(timezone.utc).isoformat(),
        'user_instruction': '先完成对提供视频舞蹈生成帧的重新绘制',
        'preserved_user_reference': str(ref / 'REFERENCE_MANIFEST.json'),
        'audio_alignment': str(ref / 'F0944_diagnostic/AUDIO_ALIGNMENT.json'),
        'reference_video_frames': 240, 'reference_fps': '24/1',
        'clip_start_pts': clip_start_pts, 'clip_end_pts_exclusive': clip_end_pts,
        'clip_duration_ticks': 160000,
        'end_trim_rule': 'Preserve true source PTS, but trim the last included exposure at exactly 10 seconds. The final source frame is not automatically its full original duration.',
        'original_pv_frame_range_inclusive': [frames[0]['frame'], frames[-1]['frame']],
        'original_pv_frame_count': len(frames), 'original_time_base': '1/16000',
        'existing_visible_drawing_states': len(states),
        'scope_basis': 'Original PV exclusively controls exact action, head/body/hand pose, expression, costume, framing and true exposure/PTS. The AI video is ONLY a secondary reference for hair sway, bounce and rebound retargeted to that original pose. Never copy its character motion or add actions from it. Any justified extra hair-motion variant preserves the original body pose and is reviewed explicitly. Encoder noise and 240 unique PNG hashes are not 240 proven drawings.',
        'generation_provider_policy': 'First image of each new visible state: configured API high, hair swing considered before submission. Redraw/repair existing images: built-in imggen whole-visible-character, then fresh root and Sol xhigh actual image review.',
        'rendering': 'Unlit flat bob AND drill: one ash-gray fill, one muted mint material stripe, black ink. No specular highlight, white reflective line, gradient, shaded coil underside or green glow.',
        'same_group_order': 'Sequential actual primary and Sol xhigh image review before another neighboring source state; at most two independent action groups in flight.',
        'other_shots': 'No new unrelated drawing submissions while this clip is the priority; already submitted returns preserved.',
        'completion': 'All visible states redrawn or actually retained under the new rules, source-based per-appearance registrations, real exposure layer bindings, 1080P transparent outputs and actual temporal review. No final background/subtitle/effect composite.',
        'complete': False, 'user_accepted': False,
        'exposure_proposals': [{'source_frame': f['frame'], 'source_pts': f['pts'],
                               'original_end_pts': f['end_pts'], 'clip_end_pts': min(f['end_pts'], clip_end_pts),
                               'clip_relative_pts': f['pts'] - clip_start_pts,
                               'clip_duration_ticks': min(f['end_pts'], clip_end_pts) - f['pts'],
                               'source_ids': f.get('resolved_canonical_ids', f.get('proposed_canonical_ids', [])),
                               'actual_selected_asset_binding': None,
                               'actual_render_binding_verified': False}
                              for f in frames],
        'states': states,
    }
    path = DEST / 'PRIORITY_SCOPE.json'
    if path.exists():
        # Keep human per-state decisions in a separate review file, not this generated manifest.
        obj['previous_scope_preserved'] = True
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    goal_path = BASE / 'GOAL_EXECUTION.json'
    goal = load(goal_path)
    goal['current_priority'] = str(path)
    goal['current_priority_description'] = 'Complete uploaded first10 dance character redraws using reference hair movement and uniformly unlit flat hair before other new shots.'
    goal_path.write_text(json.dumps(goal, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'scope': str(path), 'original_frames': len(frames), 'visible_states': len(states),
                      'legacy_statuses_requiring_new_criterion_review': dict(Counter(s['legacy_static_status'] for s in states))}, ensure_ascii=False))


if __name__ == '__main__':
    main()
