"""Record scoped user curl approval and one explicit extra G49 API operation."""
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib
import json
import shutil

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{'path':str(p.resolve()),'sha256':sha(p)}
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proof=base/'review/user_X01_curl_only_G49_extra_once_20261103_v01'
proof.mkdir(exist_ok=False)
for p in [root/'image_defaults.json',base/'GOAL_EXECUTION.json',root/'CURRENT_SELECTION.json']:
    shutil.copyfile(p,proof/(p.name+'.before'))
now=datetime.now(timezone.utc).isoformat()
x=base/'drawings/ART-X01-01/v01/prep_first_api_source4021_ending_graygreen_two_large_one_small_v01/character_api_original.png'
g=base/'drawings/ART-G49-01/v01/prep_first_api_source4401_rearLEFT_graybob_twoLargeOneSmall_v03_LFprefix/character_api_original.png'
assert sha(x)=='3d9730933e488cd05bbf39a678cecc89f8ed0e09c91d8d7fb9378360c4883a0a'
assert sha(g)=='d4f403acc25ecccad41c9f065832ca718c5e280c4ab2427be596218234c8bdb4'
crop=base/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png'
assert not crop.exists()
box=[350,225,460,375]
with Image.open(x) as im:im.crop(box).save(crop)
baseline_path=base/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'
baseline={'recorded_utc':now,'id':'ART-X01-01','original':ev(x),'curl_reference_crop':ev(crop),
 'crop_xyxy':box,'crop_operation':'Readonly rectangular crop of unchanged API original for scoped reference; no art retouch.',
 'user_statements_verbatim':['这张可以，能当基线','我是说钻发的绘制可以当基线'],
 'approved_scope':'curl_rendering_only','whole_character_user_accepted':False,
 'role':'Primary user-approved drill drawing method: hollow continuous gray ribbon, two large turns and one small terminal turn, opaque gray returns and thin mint edge.',
 'not_approved_by_this_statement':['whole character','face/eyes/expression','bob identity','clothing','whole-body proportions','placement/binding','temporal playback'],
 'transfer_rule':'Use only the curl drawing method. Each original PV pose controls anatomical root projection/occlusion and the current whole-head/shoulder context controls scale; do not transfer the frontal screen-right position to rear profiles.',
 'generation_calls':0,'dynamic_validated':False}
save(baseline_path,baseline)
extra_path=base/'API_EXTRA_G49_01_HAIR_REDRAW_ONCE_AUTHORIZATION_20261103_v01.json'
extra={'recorded_utc':now,'id':'ART-G49-01','user_statements_verbatim':['钻发小了','建议把钻发放在肩膀前','调整发型，额外api重绘机会一次'],
 'operation_kind':'whole_character_redraw','first_drawing':False,'maximum_new_logical_requests':1,
 'current_rejected_image':ev(g),'curl_baseline':ev(baseline_path),
 'changes':'Adjust hairstyle coherently; larger curl at anatomical LEFT low ear/nape and route it around the LEFT shoulder front with real occlusion. Preserve original4401 head/neck/torso/crop and ending clothing.',
 'endpoint':'https://api.openai.com/v1/images/edits','quality':'high','n':1,'retry':1,
 'maximum_transport_attempts_per_authorized_operation':2,
 'retry_budget_is_not_an_additional_new_redraw_operation':True,
 'consumed_by_run':None,'generation_calls_by_this_record':0}
save(extra_path,extra)
prior=base/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v05.json'
req=read(prior);req['requirements_revision']='goal_curl_assessment_20261103_v06';req['recorded_utc']=now
req['user_statements_verbatim']+=baseline['user_statements_verbatim']+extra['user_statements_verbatim']
req['curl_rendering_baseline']=ev(baseline_path)
entry={**ev(crop),'role':baseline['role'],'approved_scope':'curl_rendering_only','root_actually_viewed':True}
req['reference_priority'].insert(0,entry)
req['G49_specific_user_correction']={**ev(extra_path),'baseline_scope':'curl rendering only; not whole X01 artwork'}
req['supersedes']={**ev(prior),'conflicts_superseded':['Any inference that the X01 user curl selection accepted the whole character'], 'two_large_one_small_and_retry1_unchanged':True}
req_path=base/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json';save(req_path,req)
d=read(root/'image_defaults.json');d['drill_structure_rule']['requirements']=ev(req_path)
d['drill_structure_rule']['reference_priority']=req['reference_priority']
d['drill_structure_rule']['user_approved_rendering_baseline']={**ev(baseline_path),'approved_scope':'curl_rendering_only'}
save(root/'image_defaults.json',d)
gp=base/'GOAL_EXECUTION.json';goal=read(gp)
goal.setdefault('curl_assessment_pointer_history',[]).append(goal['review']['mandatory_curl_requirements'])
pointer={**ev(req_path),'requirements_revision':req['requirements_revision'],'construction_policy_id':req['construction_policy_id'],'recorded_utc':now,'old_reports_preserved':True,'no_automatic_reacceptance':True}
goal['review']['mandatory_curl_requirements']=pointer;goal['latest_curl_assessment_requirements']=pointer
goal['latest_hollow_drill_policy']['requirements']=pointer;goal['latest_hollow_drill_policy']['reference_priority']=req['reference_priority']
goal['latest_user_approved_curl_rendering_baseline']=ev(baseline_path)
goal['latest_G49_extra_hair_redraw_authorization']=ev(extra_path)
goal['updated_utc']=now;goal['complete']=False;save(gp,goal)
sp=root/'CURRENT_SELECTION.json';s=read(sp);s.update({'latest_curl_requirements':pointer,'latest_user_approved_curl_rendering_baseline':ev(baseline_path),'latest_G49_extra_hair_redraw_authorization':ev(extra_path)})
save(sp,s)
doc=base/'GOAL_CURRENT_REQUIREMENTS.md'
with doc.open('a',encoding='utf-8') as out:out.write('\n最新基线：X01-01 仅钻发画法获用户认可，不能扩为整张人物通过。G49-01 钻发增量并改左肩前方，已授权额外一次官方API全人物发型重绘；high/n=1/retry=1。\n')
save(proof/'RECEIPT.json',{'baseline':ev(baseline_path),'extra_authorization':ev(extra_path),'requirements':ev(req_path),'goal':ev(gp),'defaults':ev(root/'image_defaults.json'),'originals_changed':False,'generation_calls':0})
print(json.dumps({'baseline':str(baseline_path),'approved_scope':'curl_rendering_only','extra_authorization':str(extra_path),'maximum_extra_logical_requests':1,'generation_calls':0},ensure_ascii=False))
