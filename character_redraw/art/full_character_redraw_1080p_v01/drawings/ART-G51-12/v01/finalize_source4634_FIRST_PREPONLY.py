from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT = Path(__file__).resolve().parents[5]
B = ROOT / 'art/full_character_redraw_1080p_v01'
CEL = Path(__file__).resolve().parent
R = (CEL/'prep_first_api_source4634_closed_smile_horizontal_outward_gloves_fullshoes_graygreen_v06').resolve()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(p,x):
    assert not p.exists(),p
    p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

defaults=read(ROOT/'image_defaults.json')
prefix=defaults['generation_prompt_prefix']['text']
assert defaults['api_request_policy']['retry']==1 and defaults['api_request_policy']['n']==1
wrapper=ROOT/'scripts/Invoke-ReferenceImage.ps1'
assert sha(wrapper)=='f6aefc1c428e0edb99c7280e78b44b640364a1f281577623f19e25dc4feb7ab6'
prov=read(R/'INPUT_COPY_AND_CROP_PROVENANCE.json'); refs=prov['references']; assert len(refs)==5
audit=read(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json')
for x in audit['files_present_before_PREP']:
    assert sha(x['path'])==x['sha256']
job=read(CEL/'JOB.json')
source_obs='Own4634 nearfront slightheadtilt, unequal roundopen eyes and SMALL CLOSED SMILE rather than previous11 neutralpoint. Both lowforearms extend almosthorizontally outward: viewerLEFT wristfold/downleft curledfinger groups, viewerRIGHT flatter rightward parallelfinger group with separate lowerthumb. Skirt flares viewerRIGHT, apron/frontfold and whitebackties ownframe. ViewerLEFT boot is shorter, nearvertical with flat closedbase; viewerRIGHT leg/shoe reaches lower with angled front and foldlines. Both shoes are complete; no toe/heel added beyond original observed extent. Leftneck pinkpetal excluded.'
actual=[Path(job['source_image']),CEL/'inputs/source_pose_guide.png']+[Path(x['path']) for x in refs]+[Path(x['path']) for x in prov['diagnostics']]
review=R/'ACTUAL_REFERENCE_REVIEW_PREPONLY.json'
save(review,{'id':job['id'],'reviewed_utc':datetime.now(timezone.utc).isoformat(),
    'actual_viewed':[ev(p) for p in dict.fromkeys(actual)],'source_observation':source_obs,
    'reference_boundary_check':'Ref2 rectangle lies entirely inside prior11 skirt cloth, not source outline/face/hands/coil; this is pigment only and does not transfer pose or shoulder depth. Ref4 excludes eyes and oldcoil. Ref5 owns current smallsmile and eyeopenings; rectangle is not a new eyelid boundary.',
    'curl_reference_scope':'X01 curl drawing only; 2adfb1 demands an actual smallthirdfront and opaquegrayreturn before Ctip, not counting mint borders or holes.',
    'generation_API_native_network_calls':0,'root_actual_review_or_release':False,
    'photography_validated':False,'dynamic_validated':False,'user_accepted':False})
registry=read(B/'ASSET_REGISTRY.json');assert job['id'] not in registry
prev=registry.get('ART-G51-11')
sol=B/'review/SOL_FIRST_G51_11_CURLBASELINE_20261103_v01.json'
sr=read(sol);assert sr['review_status']=='retained_static_candidate' and sr['image_sha256']=='124e316dc34866a127f75e66d41023941dc5aaa28fa9e822ad3e00e4a6773f7c'
gate=R/'PREDECESSOR_ROOT_RELEASE_GATE.json'
if prev:
    assert prev['sha256']==sr['image_sha256'] and prev['primary_static_pass'] and prev['independent_static_pass']
    assert read(prev['primary_review'])['continue_family']
save(gate,{'id':job['id'],'previous_id':'ART-G51-11','expected_image':ev(sr['image']),
    'independent_review':ev(sol),'registry_entry_at_PREP':prev,
    'root_registry_record_pending_at_PREP':prev is None,
    'scope':'0call preparation is authorized now. Paid FIRST requires root actual current inputs and predecessor root+Sol candidate confirmation; no automatic dispatch.',
    'front_shoulder_depth_inherited':False,'root_release_received':False,'generation_calls':0})
body='''绘制ART-G51-12首次透明人物，原F4634/PTS2474480。图1完整原PV只负责本帧头身、眼口、肩肘腕、两手套、腰裙后带、双腿双鞋和实际范围，不复制前11动作。必须用图4的中性灰短圆润bob/灰刘海/贴颊短侧发完整替换图1红尖bob与左右两高红卷；不是把原红发染灰，也不是保红双卷再添灰钻。图4只上bob/帽身份，不能移植头倾、脸或整人比例。

本帧双眼自身不等圆睁、瞳位和略偏头按图1/5；小嘴为极小闭合浅笑弧，两端略上，区别前11中性短点口，不改O嘴或张口。各虹膜单块均匀深charcoal配普通小白点，无黑芯灰环/多灰带/渐变。保方向睫毛与外眼线，紧邻外眼角细小短笔/小点容许少量像素间隙；不新添远离眼角的大痣或装饰点。图5是本源完整眼开度/浅闭笑，不把裁边当眼睑或缩小眼白。

本帧两只黑手套都可见，低位向两侧展开，前臂比前11更接近横向，不能套前11右臂长斜垂与大张指。画左上臂斜向左下后屈肘，前臂近水平伸左，手腕下折，简笔长指分组弯向左下；保持原收折指组/间隙，不画新拳或上指。画右前臂向右略下伸，较平的手套长指并行向右，拇指在掌下单独斜分；不改朝下张掌或复制画左手。画左腕接近腰带高、画右略低，肩肘腕和腰的共同关系依图1，不对称化或补隐藏手。

保源身体较正微偏、短领、腰带、围裙前折/下尖与白褶边、原腰后白带。裙摆向画右外展，不复制前11裙形。画左腿/靴较短、近竖且底部平直闭合；画右腿鞋更低，前脚略斜、脚背折线依原，双鞋当前完整，不能把源真实平底改成摄影裁线而补新脚尖/鞋跟。完整帽/两手尖/双鞋保持小透明余量，不新截原可见边。

白maidcap及按本投影画右的两片MAIN黑叶保留，两叶仅短共同根，不多补第三黑叶、长黑梗或悬空饰物。原红立领/短泡袖/衣身/裙主布改低饱和ending灰绿色；黑胸结/手套袜鞋、金扣、白肩褶袖口/围裙腰带后带裙边、暖桃肤和两红珠保。图2只有前11安全衣内灰绿颜料，不含脸手/外轮廓/卷，不移植其动作、相机、比例或肩前深度。

依本近正面头颈和双肩透视，固定人物自身LEFT低耳后/nape根在画右低bob与同侧颈肩，可由bob遮一珠或部分发根，不抬到帽旁/太阳穴、不换画左耳或镜像。单束沿同侧肩前/胸侧自然落下，白肩褶与袖有真实前后遮挡；露出部分应有实际灰返回和合理头肩体量，不把全束挂肩外后背再凭文字宣称前绕，也不为露全卷移动肩颈或让卷穿衣。被bob/肩褶挡住的部分不挖出隐藏几何，不强求全2+1全部露在外面。

图3用户认可仅钻发绘法，不是整个人物、人设、固定大小/轴线或姿势接受。一条连续宽灰发带：两次大转之后，必须另有具有自己灰正面及实际不透明灰内后返回的小末转，再渐细收成C尖。不能第二大转直接接一个钩充数，不能按绿色边线或透明孔数计圈。宽GRAY前面翻回opaqueGRAY内后返回，连续斜接下一大转/小末转；实体返回保留，真实露空才alpha透明。不加圈，不封口灰盘/叠碗/实心柱锥/断灰囊，不多尾。bob与灰front/returns/小转/C用同类无打光中性灰平涂，mint只窄细柔和材料边，无大绿主面、独立暗底、银白闪片或金属光/渐变。

保原PV手书粗细起伏、不规则简笔与稀疏线量，不向量化精修/平滑/密添发丝。真正透明RGBA只含本源可见人物及衣装；不画粉背景、导框、字幕和独立粉瓣，尤其画左颈后粉瓣不是头发/皮肤/衣服。只画实际可见，不补源外手腿或第二束卷。
'''
prompt=R/'prompt_api.txt';assert not prompt.exists();prompt.write_bytes((prefix+'\n\n'+body).encode('utf-8'))
assert prompt.read_text('utf-8').count(prefix)==1
draft={'id':job['id'],'operation_kind':'first_drawing','first_drawing':True,'PREPONLY':True,
    'dispatchable':False,'source_frame':4634,'source_pts':2474480,'timebase':'1/16000','source':ev(job['source_image']),
    'JOB':ev(CEL/'JOB.json'),'REGISTRATION_PLAN':ev(CEL/'REGISTRATION_PLAN.json'),
    'local_unstarted_audit':ev(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json'),'references':refs,
    'provenance':ev(R/'INPUT_COPY_AND_CROP_PROVENANCE.json'),'actual_reference_review':ev(review),
    'prompt':ev(prompt),'output_size':'720x944','quality':'high','n':1,'retry':1,'background':'transparent',
    'predecessor_gate':ev(gate),'requirements':ev(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),
    'curl_scope':ev(B/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'),
    'user_missing_turn':ev(B/'review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json'),
    'eye_tolerance':ev(B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'),
    'actual_source_observation':source_obs,'planned_logical_requests':1,'API_calls':0,'native_calls':0,
    'network_calls':0,'root_release_received':False,'central_JOB_REG_unchanged':True,
    'photography_validated':False,'dynamic_validated':False,'user_accepted':False}
save(R/'DRAFT_API_REQUEST.json',draft)
formal={'InputImages':[str(Path(x['path']).resolve()) for x in refs],'PromptFile':str(prompt.resolve()),
    'OutputDirectory':str(R.resolve()),'OutputFileName':'character_api_original.png','Size':'720x944','Quality':'high',
    'Background':'transparent','Stage':'FIRST_ART_G51_12_SOURCE4634_CLOSED_SMILE_HORIZONTAL_OUTWARD_GLOVES_FULLSHOES_ENDING_GRAYGREEN'}
assert len(formal)==8 and '\\' in formal['OutputDirectory']
save(R/'API_PREPARED_REQUEST.json',formal)
lock={'id':job['id'],'operation_kind':'first_drawing','first_drawing':True,'planned_logical_requests':1,
    'prepared_request':ev(R/'API_PREPARED_REQUEST.json'),'draft':ev(R/'DRAFT_API_REQUEST.json'),'prompt':ev(prompt),
    'wrapper':ev(wrapper),'authorization':ev(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
    'JOB':ev(CEL/'JOB.json'),'REGISTRATION_PLAN':ev(CEL/'REGISTRATION_PLAN.json'),
    'predecessor_gate':ev(gate),'references':[{k:x[k] for k in ('path','sha256')} for x in refs],
    'mandatory_prefix':prefix,'retry':1,'n':1,'PREPONLY':True,'submitted':False,
    'requirements':draft['requirements'],'curl_baseline':draft['curl_scope'],
    'eye_tolerance':draft['eye_tolerance'],'user_missing_turn_record':draft['user_missing_turn'],
    'actual_reference_review':ev(review),'provenance':draft['provenance'],
    'api_request_policy':ev(B/'API_REQUEST_POLICY_20261103_v01.json'),
    'API_calls':0,'native_calls':0,'root_release_required':True}
save(R/'REQUEST_LOCK.json',lock)
old=B/'drawings/ART-G51-10/v01/prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06/Invoke-PreparedPreviewOnly.ps1'
script=old.read_text('utf-8-sig').replace('f43bc9d6c3ad2c5b867e4057a7e85dd1b07e0e8d761b6e7d37e09420dfdcadf3',sha(R/'REQUEST_LOCK.json'))
assert sha(R/'REQUEST_LOCK.json') in script
runner=R/'Invoke-PreparedPreviewOnly.ps1';assert not runner.exists();runner.write_bytes(script.encode('utf-8'))
print(json.dumps({'run':str(R),'formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(prompt),'lock':ev(R/'REQUEST_LOCK.json'),'preview_only_runner':ev(runner),'previous_registry_ready':prev is not None},ensure_ascii=False))
