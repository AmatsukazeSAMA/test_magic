"""Record the exact user rejection and clarify counting without changing old evidence."""
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
root=Path(__file__).resolve().parent.parent
b=root/'art/full_character_redraw_1080p_v01'
f=b/'review/USER_G13_19_MISSING_TURN_20261103_v01';f.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p.resolve()),'sha256':sha(p)}
def create(p,v):
    with p.open('x',encoding='utf-8') as s:s.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
gp=b/'GOAL_EXECUTION.json';dp=root/'image_defaults.json';mp=b/'GOAL_CURRENT_REQUIREMENTS.md'
for p,n in [(gp,'GOAL_EXECUTION_BEFORE.json'),(dp,'image_defaults.before.json'),(mp,'GOAL_CURRENT_REQUIREMENTS.before.md')]:
    with (f/n).open('xb') as s:s.write(p.read_bytes())
raw=b/'drawings/ART-G13-19/v01/whole_imggen_graybob_visibleunion_remove_points_source1284_wider3734_v01/character_imggen_original.png'
assert sha(raw)=='96c8998abde437eb0dbb3f18e5b40ecf6258805691b4923297300674b5a4d381'
attachment=Path('C:/Users/11515/.codex/generated_images/01a18c9e-c795-7c41-9eed-612ceab2f81f/exec-dbb71a16-ac07-477b-84d3-f8436f9881a5.png')
assert sha(attachment)==sha(raw)
rule='两大卷之后，必须还有具有自身灰正面与实际不透明灰返回的小末转，再收细为C形尖端；不能第二大转直接接一个钩就当作两大加一小，不按绿色边线或透明孔数计圈。各段是一条连续灰发带，实体返回不得挖空。'
p=f/'USER_REJECTION.json'
create(p,{'recorded_utc':datetime.now(timezone.utc).isoformat(),'id':'ART-G13-19','user_statement_verbatim':'少了一卷',
 'rejected_artwork':ev(raw),'user_attachment_normalized':ev(attachment),
 'old_primary_review_preserved':ev(raw.parent/'PRIMARY_GOAL_REVIEW.json'),
 'old_independent_review_preserved':ev(b/'review/SOL_WHOLE_G13_19_GRAYBOB_VISIBLEUNION_20261103_v01.json'),
 'decision':'user_P1_missing_turn_not_merely_compressed_P2','counting_clarification':rule,
 'construction_policy_unchanged':'hollow_two_large_one_small_20261102_v04','approved_baseline_scope':'curl_drawing_only',
 'other_P1_still_pending':['unsupported common hidden right index bridge','third independent cap leaf'],
 'eye_corner_tolerance_unchanged':True,'old_images_and_reports_preserved':True,'generation_calls':0,
 'goal_complete':False,'user_accepted_whole_art':False})
g=read(gp);g['latest_user_missing_curl_turn_rejection']={**ev(p),'id':'ART-G13-19','user_statement_verbatim':'少了一卷','priority':'P1 repair; missing FIRST drawings continue in parallel','curl_counting_clarification':rule}
gp.write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read(dp);d['latest_user_missing_curl_turn_rejection']=ev(p);d['curl_small_terminal_turn_counting_rule']=rule
dp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with mp.open('a',encoding='utf-8') as s:s.write('\n最新少卷修正：用户对G13-19 whole（96c8998a）明确“少了一卷”，升级为待修P1。'+rule+'补缺首图与本项修正并行。证据：review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json。\n')
print(json.dumps({'user_rejection':ev(p),'requirements':ev(mp),'defaults':ev(dp),'calls':0},ensure_ascii=False))
