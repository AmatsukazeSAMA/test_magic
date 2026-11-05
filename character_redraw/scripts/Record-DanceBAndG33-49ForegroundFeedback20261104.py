"""Record exact user decisions, preserve policies/receipts, prepare one repair."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import numpy as np
from PIL import Image
import importlib.util

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'art/full_character_redraw_1080p_v01'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(p,obj):
    Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

review=BASE/'review/USER_DANCE_B_LOW_SATURATION_EYES_20261104_v04'
review.mkdir(exist_ok=False)
before=review/'BEFORE';before.mkdir()
defaults_path=ROOT/'image_defaults.json';goal_path=BASE/'GOAL_EXECUTION.json'
for p in [defaults_path,goal_path]:shutil.copyfile(p,before/p.name)
defaults=read(defaults_path);old_pointer=defaults['eye_color_policy'];old=read(old_pointer['path'])
assert sha(old_pointer['path'])==old_pointer['sha256']
trial=BASE/'drawings/ART-X01-14/v01/py_user_reference_B_eye_style_trial_v01/character_eye_style_trial.png'
assert sha(trial)=='14bdcf08bb3a075a3f3523911757709d3b911d43a4b350c1030587965993f7c9'
ref=BASE/'review/USER_X01_14_EYE_STYLE_TWO_REFERENCES_20261104_v01/USER_REFERENCE_B.png'
assert sha(ref)=='80e10642029b2259a139268484becf8cd78f40716f8f4d91366da202e1fc8cac'
module_spec=importlib.util.spec_from_file_location('eye_style_trial',ROOT/'scripts/Trial-X01-14-UserReferenceEyeStyles20261104.py')
module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
fields=[]
for name,roi in [('viewer_left',(370,347,455,426)),('viewer_right',(553,409,635,492))]:
    field,center,bounds,detail=module.style_field(np.asarray(Image.open(ref)),roi,(-.32,float(np.sqrt(1-.32**2))))
    p=review/f'B_{name}_IRIS_INTERIOR_COLOR_FIELD_NO_GLINT_OR_OUTLINE.png'
    Image.fromarray(np.rint(field).astype(np.uint8)).save(p)
    fields.append({'name':name,'image':ev(p),'reference_center_xy':center,'reference_local_bounds_uv':bounds,
                   'reference_roi_xyxy':roi,'reference_down_unit_xy':[-.32,float(np.sqrt(1-.32**2))],
                   'measurement':detail})
priority=read(BASE/'dance_first10_reference_redraw_v01/PROGRESS.json')
first_ids=[r['id'] for r in priority['states']]
jobs=read(BASE/'REDRAW_PLAN.json')['jobs']
known=sorted(set(first_ids+[j['id'] for j in jobs if j.get('group') in ['G33','X01'] and j.get('kind')=='body_pose']))
acceptance={'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'user_statement_verbatim':'B吧，后续的跳舞镜头都使用这种低饱和度的瞳孔',
 'accepted_scope':'B trial iris interior low-saturation two-gray palette, softer lower-light region; all subsequent dance shots.',
 'accepted_trial':ev(trial),'original_reference':ev(ref),'color_fields':fields,
 'known_dance_state_ids':known,'first_dance_state_ids':first_ids,
 'scope_resolution':'All subsequent original-PV dance shots. Explicit first66 and G33/X01 body-pose dance families are listed; any other shot needs actual source classification, not a blanket recolor of non-dance inserts.',
 'protected':'Own eye outer silhouette/opening/gaze/sclera/lid/lashes, native glints+AA, all alpha and all non-iris pixels.',
 'normal_open_only':True,'squint_closed_fully_hidden_exempt_per_eye':True,
 'art_pass_before_separate_Python':True,'whole_character_or_hair_accepted':False,
 'existing_all_previous_eye_passes_retroactively_rejected':False,'API_calls':0}
acceptance_path=review/'USER_EYE_STYLE_ACCEPTANCE.json';save(acceptance_path,acceptance)
policy=dict(old)
policy.update({'policy_id':'post_pass_normal_open_eye_dance_B_override_20261104_v04',
 'recorded_utc':datetime.now(timezone.utc).isoformat(),'supersedes':old_pointer,
 'dance_B_style_override':ev(acceptance_path),
 'reference_field_method':'Adapt approved B iris-interior color fields to each native iris local coordinates; no eye geometry/glint/face transfer. Exact mask/outside/glint/alpha verification and fresh scoped visual review required.',
 'legacy_fixed_palette_scope':'Existing historical checks and non-dance shots retain v03 palette. These constants do not override the later user-selected B style for new dance eye passes.',
 'generation_prompt_prefix':'最新眼睛工作流：跳舞镜头使用用户已选B版低饱和深灰主体、较柔和低反差的底部浅灰弧面，无中央独立黑瞳孔；跳舞眼色不硬套旧72/69/67和129/128/128的强反差。只能参考B眼内颜色/分界画法，不复制B眼形、眼白、头角、开合、视线或高光。非跳舞镜头沿用已确认两灰圆弧基线。原PV决定自身眼形/开合/眼白/睫线/视线及原小白glint。返图人物先实际通过主代理和Sol审核，再另用Python局部处理正常睁眼的眼内RGB/色界；眯眼、闭眼、完全遮眼按单眼实际检查跳过，不能强睁或补虹膜。全部alpha和眼外像素原样保留，眼色不调用API/整图重绘。',
 'latest_user_statements_verbatim':old['latest_user_statements_verbatim']+[acceptance['user_statement_verbatim']]})
policy_path=review/'POLICY.json';save(policy_path,policy)
defaults['eye_color_policy']=ev(policy_path)
defaults['dance_eye_style_policy']=ev(acceptance_path)
defaults['eye_style_baseline']['dance_override']=ev(acceptance_path)
defaults['eye_style_baseline']['drawing_rule']='Own original PV eye geometry and expression. After art pass, local Python normal-open iris style: latest user-selected B low-saturation reference for dance shots; retained two-gray round-cap baseline for non-dance inserts. Closed/squint/hidden exempt per eye.'
save(defaults_path,defaults)
goal=read(goal_path)
goal['repair']['eye_local_RGB_and_internal_light_cap_exception']=ev(policy_path)
goal['latest_dance_eye_policy']=ev(acceptance_path)
goal['current_priority_description']+=' 最新用户选择：后续跳舞镜头统一B版低饱和眼内画法，人物过审后Python局部实施；保眼形、原glint及眼外像素，闭/眯/遮眼豁免。非跳舞插入保持其已确认规则。'
save(goal_path,goal)
save(review/'POLICY_UPDATE_RECEIPT.json',{'new_policy':ev(policy_path),'acceptance':ev(acceptance_path),
 'old_policy_preserved':old_pointer,'before_defaults':ev(before/'image_defaults.json'),
 'new_defaults':ev(defaults_path),'goal':ev(goal_path),'new_generation_calls':0})

feedback=BASE/'review/USER_G33_49_COIL_FOREGROUND_FUSION_20261104_v01'
feedback.mkdir(exist_ok=True)
parent=BASE/'drawings/ART-G33-49/v01'
target=parent/'whole_imggen_restore_far_left_root_shoulderfront_v01/character_imggen_original.png'
selection=read(BASE/'ASSET_REGISTRY.json')['ART-G33-49']
save(feedback/'USER_REJECTION.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'user_statement_verbatim':'钻发和前景融合了','attached_original':ev(target),
 'selected_same_art_eye_derivative':selection,'current_contact_diagnostic':ev(feedback/'CURRENT_FOREGROUND_CONTACT_4x.png'),
 'root_actual_observation':'Lower gray/mint ribbon and taper touch the chest fingers, white cuff edge and shoulder frill ambiguously; keep correct lowfarLEFT2beads, reconstruct actual foreground occlusion instead of showing all turns.',
 'latest_decision':'reopen_art_for_repair','old_reviews_preserved':True,'whole_art_accepted':False})
run=parent/'whole_imggen_clear_foreground_occlusion_no_fused_tail_v02';run.mkdir(exist_ok=False)
coil=BASE/'drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png'
prompt='''Edit image1 as one coherent whole visible character on true transparent alpha. Image2 is this same frame original PV and exclusively owns its gesture/head/body/costume/crop. Image3 supplies the intrinsic continuous wide-gray coil construction, not a requirement to expose every turn.
The user rejected image1 because the lower drill lock FUSES with foreground fingers, white cuff and white shoulder-frill folds. Repair this material/layer contact, retaining the CORRECT anatomicalLEFT low far-side bob→exactly two red beads connection on imageRIGHT. Do not move the root back to imageLEFT exposed nearRIGHT ear, raise it to cap, or shrink the main coil diameter.
Establish simple, unambiguous front-to-back layers: the chest hand's fingers and the other raised hand/wrist stay entirely in FRONT of the hair wherever they overlap; the original white cuff and crossing black sleeve are also solid foreground. Their silhouettes, black contours, finger separations and cuff corner must remain continuous, never dissolve into gray ribbon or mint edge. Gray/mint contours STOP at those occluders; they do not run through fingers/cuff, turn into white cloth strips, join a frill point or emerge as a white C-shaped hair end. The shoulder frill behind the lock keeps separate white fabric edges where actually visible. Avoid long tangencies that make the two materials one continuous surface.
Keep the normal broad gray coil front at neck/chest over the inner shoulder frill. Route the lower part NATURALLY BEHIND the own chest hand and solid white cuff/crossed sleeve. Its tiny C tip may be completely hidden there: do NOT pull the whole coil sideways or downward merely to display a C, and do not invent a new exposed mini-coil below the sleeve. Hidden material counts toward the one intrinsic total of exactly 2Large+independent trueSmall gray front/opaque return+continuous C. Preserve opaque gray returns; only genuine air transparent, mint thin material edge. No extra turns, sealed cylinder/solid cone/stacked plates.
Keep image1 and own image2: head yaw gently imageRIGHT with eyes looking camera, unequal normal-open iris shapes and tiny original white glints, small closed mouth; high hand long index points diagonally UP-LEFT, other fingers fold; chest hand long fingers lie diagonally DOWN-LEFT with own thumb side, white cuff angles/crossed black sleeves unchanged. Do not copy a neighboring more-horizontal finger pose. Same black/red/white long maid dress, red bow/gold clasp, apron and skirt direction, rear waist ribbons, crossed/close ankle stance and both complete strap shoes. No mirrored body, new hands, changed face or extra cloth strip hiding a defect.
Retain original handdrawn sparse black contours with variable thickness and gray/mint simple fills; no metallic silver highlight, dense polished hair or extra clothing folds. Current eye outline/glints remain; after this art passes, local Python applies user-selected B low-saturation iris interiors separately. Output whole same-frame visible character, true transparent background, no text, collage or diagram.'''
pf=run/'prompt_imggen.txt';pf.write_text(prompt+'\n',encoding='utf-8')
save(run/'REQUEST.json',{'id':'ART-G33-49','provider':'built-in imagegen','calls_authorized':1,
 'prompt':ev(pf),'references':[ev(target),ev(parent/'inputs/source_pose_guide.png'),ev(coil)],
 'transparent_background':True,'feedback':ev(feedback/'USER_REJECTION.json'),
 'changed_hypothesis':'Do not force-expose lower tip. Rebuild true source-foreground occlusion, with lower Small/C allowed fully hidden; remove ambiguous gray/mint/white cloth bridges.',
 'user_accepted':False,'created_utc':datetime.now(timezone.utc).isoformat()})
hold=BASE/'drawings/ART-G33-50/v01/whole_imggen_restore_far_left_root_with_reviewed_neighbor_context_v01'
save(hold/'HOLD_REJECTED_REFERENCE_BEFORE_CALL.json',{'reason':'User rejected the G33-49 whole used as side context for fused foreground. Preserve prepared request; do not call with this input. Wait for own previous-family repair actual pass or use an independently justified replacement reference.',
 'calls':0,'rejected_reference':ev(target),'user_feedback':ev(feedback/'USER_REJECTION.json')})
print(json.dumps({'dance_B_policy':ev(policy_path),'accepted_eyes_only':ev(acceptance_path),
 'G33_49_repair_request':ev(run/'REQUEST.json'),'G33_50_prepared_call_held':True,'generation_calls':0},ensure_ascii=False))
