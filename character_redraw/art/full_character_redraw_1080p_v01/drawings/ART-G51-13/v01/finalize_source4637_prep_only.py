from pathlib import Path
import json, hashlib, datetime, sys, subprocess
P=Path(r'D:\CODEX\魔术之心');B=P/'art/full_character_redraw_1080p_v01';C=B/'drawings/ART-G51-13/v01'
R=C/'prep_first_api_source4637_roundeyes_tinyneutralmouth_outward_unequal_gloves_crossedlegs_fullshoes_graygreen_v06'
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
f=lambda p:dict(path=str(Path(p).resolve()),sha256=sha(p))
def save(p,x):
 p=Path(p);assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
q=read(R/'API_PREPARED_REQUEST.json');d=read(R/'DRAFT_API_REQUEST.json');defaults=read(P/'image_defaults.json')
prefix=defaults['generation_prompt_prefix']['text'];pf=Path(q['PromptFile']);prompt=pf.read_text('utf-8-sig')
assert prompt.startswith(prefix) and prompt.count(prefix)==1
assert len(q)==8 and len(q['InputImages'])==5 and q['OutputDirectory']==str(R.resolve())
assert all(int(x)%16==0 for x in q['Size'].split('x'))
assert sha(P/'scripts/Invoke-ReferenceImage.ps1')=='f6aefc1c428e0edb99c7280e78b44b640364a1f281577623f19e25dc4feb7ab6'
timeline=Path(r'D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\data\original_timeline.json')
row=next(x for x in read(timeline) if x['frame']==4637);assert row['pts']==2476080
prev=B/'drawings/ART-G51-12/v01/prep_first_api_source4634_closed_smile_horizontal_outward_gloves_fullshoes_graygreen_v06'
source=Path(read(C/'JOB.json')['source_image'])
actual=[source,C/'inputs/source_pose_guide.png',prev/'character_api_original.png',prev/'qa_white.png',prev/'qa_black.png',*map(Path,q['InputImages']),R/'OWN4637_GLOVES_READONLY_2x.png',R/'OWN4637_CROSSED_LEGS_BOTH_SHOES_READONLY_2x.png']
save(R/'ACTUAL_REFERENCE_REVIEW_PREPONLY.json',dict(id='ART-G51-13',reviewer='xhigh_pending_artist, not ROOT release',recorded_utc=now(),actual_images=[f(x) for x in actual],actual_view_method='functions.view_image fresh individually; no prior-maker view claim inherited',source_frame=4637,source_pts=2476080,original_timeline=f(timeline),original_timeline_row=row,
 observations=['较圆睁且不等眼、极小中性闭口，不复制前12笑弧。','双臂屈肘向外，画左手套上长指和下折分指/画右近水平长指组不同；两手完整。','交叉小腿与两鞋前后重叠，本源双鞋都完整，不继承前态腿势或底裁。','画右两MAIN帽叶、源白围裙/肩褶/后带与右扬裙摆；ending主布灰绿。','粉瓣紧邻肩后/右卷/右腕，只是独立背景，不作手/发/衣结构。','Ref2是纯衣内灰绿颜料小矩形，实看无动作、脸、根卷或身体轮廓。','Ref3是curl画法ONLY：2large之后须一个有自身灰前/opaque返回的真smallturn再C；不可用第二大hook充数。'],
 source_pixel_copy_or_rectangle_only=True,art_pixels_edited=False,source_occluded_microcontours_not_certified=True,PREPONLY=True,root_release=False,api_calls=0,native_calls=0))
lock=dict(id='ART-G51-13',operation_kind='first_drawing',first_drawing=True,planned_logical_requests=1,
 prepared_request=f(R/'API_PREPARED_REQUEST.json'),draft=f(R/'DRAFT_API_REQUEST.json'),prompt=f(pf),wrapper=f(P/'scripts/Invoke-ReferenceImage.ps1'),authorization=f(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),JOB=f(C/'JOB.json'),REGISTRATION_PLAN=f(C/'REGISTRATION_PLAN.json'),predecessor_gate=f(R/'PREDECESSOR_ROOT_RELEASE_GATE.json'),references=[f(x) for x in q['InputImages']],mandatory_prefix=prefix,retry=1,n=1,PREPONLY=True,submitted=False,
 requirements=f(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),curl_baseline=f(B/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'),eye_tolerance=f(B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'),user_missing_turn_record=f(B/'review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json'),actual_reference_review=f(R/'ACTUAL_REFERENCE_REVIEW_PREPONLY.json'),provenance=f(R/'REFERENCE_PROVENANCE.json'),api_request_policy=f(B/'API_REQUEST_POLICY_20261103_v01.json'),API_calls=0,native_calls=0,root_release_required=True)
assert lock['requirements']['sha256']=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
assert lock['authorization']['sha256']=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
save(R/'REQUEST_LOCK.json',lock)
script='''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCKSHA__'){throw 'PREP lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'PREP payload changed'}
}
$q=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne 5 -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected PREP parameters'}
& $l.wrapper.path @q -Preview
'''
sp=R/'Preview-PreparedFirstOnly.ps1';assert not sp.exists();sp.write_text(script.replace('__LOCKSHA__',sha(R/'REQUEST_LOCK.json')),'utf-8')
preview=subprocess.run(['pwsh','-NoProfile','-File',str(sp)],capture_output=True,check=False)
assert preview.returncode==0,preview.stderr.decode('utf-8','replace')
(R/'PREVIEW_STDOUT.txt').write_bytes(preview.stdout);(R/'PREVIEW_STDERR.txt').write_bytes(preview.stderr)
v=json.loads(preview.stdout.decode('utf-8-sig'));assert not v['submitted'] and v['retry']==1 and v['n']==1 and v['input_count']==5 and v['size']=='720x944'
assert v['effective_prompt_characters']==len(prompt)
save(R/'API_PREVIEW_PROOF_PREPONLY.json',v)
helper=P/'scripts/Release-RootReviewedFirstApi.py';code=helper.read_text('utf-8-sig');guard=code.split("release = run / 'ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json'",1)[0]
sys.argv=[str(helper),str(R),'--observation','PREP compatibility check only; never creates ROOT release']
exec(compile(guard,str(helper),'exec'),{'__name__':'__prep_guard__','__file__':str(helper)})
assert not (R/'ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json').exists()
save(R/'FIRST_HELPER_COMPATIBILITY_PREPONLY.json',dict(id='ART-G51-13',helper=f(helper),executed_guard_prefix_sha256=hashlib.sha256(guard.encode('utf-8')).hexdigest(),all_original_assertions_before_first_ROOT_write_passed=True,formal_exact_eight_fields=True,Windows_native_OutputDirectory_exact_str_resolve=True,real_preview=f(R/'API_PREVIEW_PROOF_PREPONLY.json'),mandatory_prefix_occurrences=1,effective_prompt_characters_match=True,root_release_created=False,attempt_created=False,API_native_network_calls=0))
live=read(B/'ASSET_REGISTRY.json').get('ART-G51-12')
save(R/'PREP_HANDOFF.json',dict(id='ART-G51-13',recorded_utc=now(),source_frame=4637,source_pts=2476080,source=f(source),formal=f(R/'API_PREPARED_REQUEST.json'),prompt=f(pf),references=[f(x) for x in q['InputImages']],lock=f(R/'REQUEST_LOCK.json'),real_preview=f(R/'API_PREVIEW_PROOF_PREPONLY.json'),compatibility=f(R/'FIRST_HELPER_COMPATIBILITY_PREPONLY.json'),provenance=f(R/'REFERENCE_PROVENANCE.json'),actual_reference_review=f(R/'ACTUAL_REFERENCE_REVIEW_PREPONLY.json'),current_predecessor_registry_readback=live,root_must_confirm_previous12_candidate_before_network=True,output_size='720x944',quality='high',n=1,retry=1,submitted=False,api_calls=0,native_calls=0,root_release=False,central_modified=False,own_difference='Round unequal eyes/tiny neutral closedmouth; own unequal outward folded glove groups and crossed legs with two complete overlapping shoes. No previous12 smile/pose/coil transfer.'))
print(json.dumps(read(R/'PREP_HANDOFF.json'),ensure_ascii=False,indent=2))
