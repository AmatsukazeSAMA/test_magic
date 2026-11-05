"""Apply the user's direct-API workflow for independent new scenes."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
root=Path(__file__).resolve().parent.parent;b=root/'art/full_character_redraw_1080p_v01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=b/'USER_DIRECT_INDEPENDENT_SCENE_API_20261103_v01.json'
assert not p.exists()
rule={'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'user_statement_verbatim':'一张图画了一小时有点变态了，对于新场景前后没联系的的图，可以直接api绘制',
 'scope':'Independent new-scene FIRST drawings with no adjacent-action dependency',
 'workflow':'View own original PV frame and minimal identity/curl references, then submit official API immediately; review returned artwork afterwards.',
 'provider':'OpenAI official API','quality':'high','n':1,'retry':1,
 'minimal_references':'Own PV plus only useful gray character identity and user-approved curl drawing references; no mandatory previous-frame crop.',
 'parallel_independent_requests':True,'wait_for_previous_scene_review_before_FIRST':False,
 'pre_generation_adjacent_frame_audit_required':False,'large_PREP_handoff_required':False,
 'consecutive_action_frames':'Check necessary neighboring action and curl continuity; do not impose this on unrelated scenes.',
 'post_return':'Root actual view and independent actual art review continue. Known P1s stay in repair queue; no automatic chain of redraws before other missing FIRSTs.',
 'originals_and_automatic_provider_receipts_preserved':True,
 'prior_UNKNOWN_calls_must_be_recovered_not_restarted':True,
 'curl_count_side_size_line_style_requirements_unchanged':True,
 'goal_complete':False}
save(p,rule)
e={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
gp=b/'GOAL_EXECUTION.json';g=read(gp);g['latest_user_direct_independent_scene_api_workflow']=e
g['current_priority_description']='优先并行补缺首图；无前后动作联系的新场景直接official API high/n1/retry1，返图后双审；连续动作才核邻帧。旧修复并行，钻发两大加真实小末转。'
save(gp,g)
dp=root/'image_defaults.json';d=read(dp);d['independent_scene_direct_API_workflow']={**e,**{k:rule[k] for k in ['quality','n','retry','parallel_independent_requests','wait_for_previous_scene_review_before_FIRST','large_PREP_handoff_required']}}
save(dp,d)
with (b/'GOAL_CURRENT_REQUIREMENTS.md').open('a',encoding='utf-8') as f:
 f.write('\n最新直接API流程：用户明确无前后动作联系的新场景可以直接API绘制。先看本原PV及最少必要的人设/卷参考，即提交official high、n=1、retry=1；独立稿并行，返图后实际双审。无需等前一场景旧稿通过或先制作大份PREP/邻帧审计；连续动作帧才核必要前后衔接。已有缺陷保待修，继续补缺首图，不反复重绘阻塞其他独立新稿。未知旧调用仍先恢复，原图与自动回执保留。\n')
print(json.dumps({'direct_workflow':e,'generation_calls':0},ensure_ascii=False))
