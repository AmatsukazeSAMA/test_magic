"""Record the user's explicit acceptance of this eye detail; keep prior reviews."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

root=Path(__file__).resolve().parent.parent
base=root/'art/full_character_redraw_1080p_v01'
folder=base/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01'
folder.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p.resolve()),'sha256':sha(p)}
def create(p,obj):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
goalp=base/'GOAL_EXECUTION.json'; dp=root/'image_defaults.json'; mp=base/'GOAL_CURRENT_REQUIREMENTS.md'
for p,n in [(goalp,'GOAL_EXECUTION_BEFORE.json'),(dp,'image_defaults.before.json'),(mp,'GOAL_CURRENT_REQUIREMENTS.before.md')]:
    with (folder/n).open('xb') as f:f.write(p.read_bytes())
run=base/'drawings/ART-G51-10/v01/whole_imggen_remove_isolated_under_eye_dots_source4625_v01'
raw=run/'character_imggen_original.png'
crop=base/'review/ROOT_WHOLE_G51_10_20261103_v01_evidence/EYES_white_5x.png'
assert sha(raw)=='6ab6d9b3dd82a020b9244f23b451095dcdca7c5559bb7e9853be6e5547365918'
old_sol=base/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01.json'
assert sha(old_sol)=='8a44b66322e453ee9b04f0414faa418be1b6e06a2e903757db93c993edfd68f0'
rule='用户指定G51-10 whole眼部5x图并明确“这种没事”：同类紧邻外眼角的细小短笔/小短点可以保留，即使与主眼线有少量像素间隔，也不单凭分离判P1或要求再次生图。仍按本帧原PV眼开度、视线及单色虹膜核查；本容差不等于整张人物、钻发、摄影或动态验收，也不全面撤销明显独立装饰痣的既有去除要求。'
rec={'recorded_utc':datetime.now(timezone.utc).isoformat(),'user_statement_verbatim':'这种没事',
 'user_attached_evidence':ev(crop),'exact_current_artwork':ev(raw),'id':'ART-G51-10',
 'approved_scope':'small_eye_corner_short_marks_as_shown','eye_detail_user_accepted':True,
 'interpretation':rule,'override':'This exact current whole image two small outer-eye short marks are permitted. Do not continue dot-only generation or retain P1 solely for these marks.',
 'old_independent_report_preserved':ev(old_sol),'originals_and_prior_rejections_preserved':True,
 'curl_policy_unchanged':'hollow_two_large_one_small_20261102_v04',
 'X01_approval_still_curl_drawing_only':True,'user_accepted_whole_art':False,
 'photography_validated':False,'dynamic_validated':False,'new_generation_calls':0}
rp=folder/'USER_TOLERANCE.json';create(rp,rec)
goal=read(goalp)
goal['latest_user_eye_corner_tolerance']={**ev(rp),'user_statement_verbatim':'这种没事','approved_scope':rec['approved_scope'],'exact_artwork':ev(raw),'not_whole_art_acceptance':True,'precedence':'Latest explicit user permission overrides generic isolated-point rule for shown small corner marks.'}
save(goalp,goal)
d=read(dp)
d['eye_style_baseline']['isolated_under_eye_dot']='Remove obvious isolated decorative cheek/under-eye moles. User permits tiny eye-corner short marks like approved G51-10 whole EYES_white_5x, even with a small pixel gap; do not reject solely for separation. Preserve real lashes/liner, own source expression and tiny nose/mouth marks.'
d['latest_user_eye_corner_tolerance']=ev(rp)
d['handdrawn_line_preservation_requirement']='高清化保留原手书粗细起伏、不规则简笔轮廓及相对线宽；不向量化/平滑精修/添密发丝。按最新眼角容差，示例同类紧邻外眼角细小短笔/小短点可保，不单凭微小分离退修；仍去明显独立装饰痣，保真实睫毛/眼线/鼻点，眼开度、视线、嘴型依本原PV。'
save(dp,d)
txt=mp.read_text(encoding='utf-8-sig')
txt=txt.replace('高清保持原手书线宽起伏与简笔轮廓；去掉眼下独立装饰点，保留眼线和睫毛。','高清保持原手书线宽起伏与简笔轮廓；明显独立装饰痣仍去除。按最新用户确认，示例同类紧邻眼角的细小短笔/小短点可以保留，不单凭微小像素间隔退修；保留眼线和睫毛。')
txt+='\n最新眼部容差：用户指向 G51-10 whole 的 EYES_white_5x 说“这种没事”。该图两处眼角小短点获准，停止仅为这些点重复重绘；其余人物、钻发、摄影和动态仍各自核查。正式证据：review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json。旧评审按当时要求保留，新评审引用本次更正。\n'
mp.write_text(txt,encoding='utf-8')
print(json.dumps({'user_tolerance':ev(rp),'requirements':ev(mp),'defaults':ev(dp),'new_generation_calls':0},ensure_ascii=False))
