from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib,shutil

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
CEL=B/'drawings/ART-G33-17/v01'
RUN=Path(__file__).resolve().parent
OLD=CEL/'draft_first_api_unmasked_source17_user11_graydetail_v01'
INP=RUN/'inputs';INP.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,v):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 try:
  with Image.open(p) as im:v.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return v
now=datetime.now(timezone.utc).isoformat()
old=read(OLD/'DRAFT_API_REQUEST.json')
assert sha(OLD/'DRAFT_API_REQUEST.json')=='4488ec135b6e9b23876be38ee641951752bb870102b646b5fd6425a03b42909f'
assert not list(CEL.rglob('attempt.json')) and not list(CEL.rglob('character_api_original.png'))
assert read(B/'ASSET_REGISTRY.json').get('ART-G33-17') is None
assert read(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json')['automatic_reset_permitted'] is False
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
ctx=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
assert sha(ctx)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
srcs=[Path(x) for x in old['InputImages']]
srcs[2]=ctx
names=['ref1_ORIGINAL2374_UNMASKED_FULLBODY_BOTH_SHOES.png','ref2_R050_HAIR_PHASE_ONLY_NO_VOLUME_ROOT.png','ref3_USER_CORRECT11_COMPLETE_HEAD_SPIRAL_VOLUME_CONTEXT.png','ref4_USER_BROAD_GRAY_RETURNS_THIN_MINT_DETAIL.png','ref5_G02_MONO_METHOD_SOURCE2374_EYE_OPENING.png','ref6_UNLIT_GRAY_MINT_PIGMENTS.png']
roles=[
 '唯一原PV2374完整未挖头构图；原guide624x1072整幅trim[64,0,560,1072]为496x1072。右向正面三分之四、双圆睁眼、小闭弧笑、两手腰后、裙围裙/后带/腿与两只完整鞋、帽两黑叶原位。不能复制原红双卷/高根；不得因首段半身曝光裁去canonical双鞋。',
 'R50 hair-only ROI[539,222,549,239]10x17，仅头发压紧近肩回弹相位，无AI脸/动作/根/总发量权威。不能把小可见边当整卷应缩小，也不能照其固体画法或肩后整藏。',
 '用户认可旧11完整头帽bob低珠及完整螺旋同坐标体量上下文，SHA216fd；只身份/宽灰发带连续前返/渐尖末C/相对头肩发量。不是新表演/头向/衣身/固定竖轴模板；原17眼口和姿态优先，不重复送37ad同图。',
 '最新用户灰卷detail无脸根crop；宽GRAY前面与真实不透明返回面为主体，mutedmint只较薄材料条，连续螺旋渐尖C。剔除精修高光/暗体积，不取校服/位置。',
 'G02仅一种charcoal平涂虹膜+普通小圆白点；源2374两眼开度、视线、眼形及小闭弧笑拥有最高权威，不抄半睑/心形白点。',
 '纯颜料gray#B6B4B2/mint#B0C8BA/ink#171717；bob和全部gray前内背返回面同灰平涂。色卡不改变灰主面/薄mint的材料分区，无方向影/暗底/银白高光/渐变。']
refs=[]
for i,(src,name,role) in enumerate(zip(srcs,names,roles)):
 dest=INP/name
 assert not dest.exists()
 shutil.copyfile(src,dest)
 refs.append({**ev(dest),'source':ev(src),'role':role,'original_crop_xyxy':old['source_commonlayout']['compact_crop_xyxy'] if i==0 else ([539,222,549,239] if i==1 else None)})
assert refs[0]['sha256']=='ca902e310d2fccd63f9c2e2cd8883d781c1caaa7b6eeed53290e92f544fcad15'
assert refs[3]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
release={
 'recorded_utc':now,'id':'ART-G33-17','source':'Parent specific task conveying current explicit user parallel completion instruction',
 'user_latest_verbatim':'按照要求，并行把缺的绘制帧补齐，注意钻发形态和大小2',
 'root_specific_release':'优先G33-17首图，1个API在途槽；可更新draft生成v01子目录。configured official API high/透明/n1，不自动重试。17返回立即actual view并交接停等root release18。前20待front修，不声称动态连贯通过。不得碰07/15/20/53/54/63。',
 'authorized_calls':1,'authorized_cel':'ART-G33-17','endpoint':'https://api.openai.com/v1/images/edits',
 'quality':'high','background':'transparent','n':1,'retry':0,'new_output_subrun':str(RUN),
 'project_authorization':ev(auth),'quota_reset_revocation':ev(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json'),
 'previous_repair_does_not_claim_pass':'Root explicitly releases this missing state while previous20 front-shoulder repair pending; no inherited previous-art pass or dynamic certification.',
 '18_not_released':True,'max_artist_inflight':1,'other_root_slot_untouched':True}
save(RUN/'ROOT_SPECIFIC_RELEASE.json',release)
preserved=[ev(CEL/'JOB.json'),ev(CEL/'inputs/source_pose_guide.png'),ev(CEL/'REGISTRATION_PLAN.json'),ev(OLD/'DRAFT_API_REQUEST.json'),ev(OLD/'DRAFT_prompt.txt')]
obs={
 'id':'ART-G33-17','reviewer':'xhigh_pending_artist','reviewed_utc':now,
 'actual_source_viewed':[ev(CEL/'inputs/source_pose_guide.png'),ev(Path(read(CEL/'JOB.json')['source_image'])),ev(B/'coverage/source_frames/F000895.png'),ev(B/'coverage/source_frames/F000898.png'),ev(B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000050.png')],
 'original_source_observation':'原2374为朝画右的正面三分之四，非全背；两圆睁眼/小闭弧笑，两手置腰后，画左外肘弯与白袖口后带，画右手被腰身遮。完整不同行腿和两只黑色踝带鞋均在源画内，必须全见。白maidcap和两黑叶、黑长袖红bow金扣白frill围裙保原。',
 'root_projection':'源头向画右，画左可见近耳不是人物LEFT根；唯一解剖LEFT根在远侧低耳后/nape，可被bob/下颌局部遮。不可搬到画左近耳/上抬太阳穴；卷按同侧颈肩转向自然承接肩前走向，不把整卷无脑挂到可见背面。',
 'continuity_boundary':'时间前态G12-20 F892..894仍front修待actual，G33同族15亦repair。源17和phase可绘；前态连接/发量/路径动态未认证，后续必须actual按PTS核对，不用任何v10/v11/v12作完整正参。',
 'reference_choice':'对照216fd完整head和37ad去眼口版后仅选216fd完整context进API，为相对体量/上端连续回折提供上下文；源17独占表演/转向。两者不重复占槽。',
 'coil_checks':'上端也必须连续宽gray前/返回绕行，下端渐尖正常C；不得封口椭圆片堆/实心柱外绕绿装饰。头肩上下文和初设足量但不过粗大，不微型挂件；不套全片固定比例。',
 'actual_reference_viewed_evidence':refs,'originals_preserved':preserved,
 'new_art_pass':False,'dynamic_validated':False,'user_accepted':False,'central_write':False}
save(RUN/'ARTIST_REFERENCE_REVIEW.json',obs)
prompt='''重绘一张ART-G33-17完整可见人物，透明RGBA，560x1216，简洁手书墨线+无光照平涂。原PV参考1是唯一动作、头向、头身、眼口、手、衣装、腿鞋及画面裁切依据；整个人物一次连贯完成，不拼部件。

参考1保留原2374完整未挖头的同画布构图：朝画面右侧的正面三分之四，双眼圆睁、原视线、小小闭弧笑。两手置腰后，画左外肘弯、白袖口与后腰带的接触照源，画右手依源遮挡；不添加前伸手/改姿势。黑长袖、红bow金扣、白肩frill/袖口/围裙/腰后带、裙摆轮廓与内线、不同方向交错的两腿和两只完整黑踝带鞋全部保留；不能只画首段半身或裁掉任何一只鞋。白maidcap及恰好两片黑叶原位完整存在。原红双高卷只需替换为短灰bob和一束罗马卷，红衣结不换色。源496x1072紧凑画布仅整体等比适配输出，不局部改头身或拉腿。

固定人物解剖LEFT的低耳后/下bob-nape双红珠根。当前头向右，可见画左近耳不是根所属侧；LEFT根位于远侧低颈侧，可有bob/下颌自然遮挡，不为两珠全露搬到近耳、升到眼旁或镜像身体。按此转向从同侧颈肩自然承接肩前/胸侧走向，局部按真实bob/肩frill互遮；不能把一整束无脑挂在可见后背，也不能强露整卷尾或改衣形挡错。头、颈领、低珠和卷连贯接合，不悬空或贴片。前一actual稿仍在修复，不能凭空复制其姿势或宣称已连续。

参考2只有R50很小的可见发丝边，仅提供近肩压紧、收回再弹的相位，不取AI脸、身体动作、根位、固有发量、旧密实造型或肩后全藏。小ROI不意味着整卷缩小。

参考3是用户认可的正确旧11完整头帽bob与整束卷上下文，只取身份、发量相对头肩的自然读法和连续螺旋，不抄其正脸表演、举臂、帽位或固定垂直轴/长度。参考4补宽GRAY主面和真实不透明返回面、较薄mutedmint沿卷绕行。必须是一束连续宽灰发带，从上端就有前面/返回面交错螺旋，逐圈收细接正常末C；不是封口椭圆圆盘堆、实心圆柱外绕绿饰、分节绿挂件或细S。上端和下端同样连通，按当前透视自然互遮；真实露空才透明，灰返回面不能挖为空气。不规定洞数/圈数/轴向或全片固定头卷比，大小既不粗大压肩也不微型挂件，先按完整头肩和正确11判断体量。不可照搬参考4精修亮暗。

参考5仅G02眼法：单一深charcoal平填虹膜和普通小圆白点；保持源17当前圆睁的开度/视线/小笑，不抄G02半睑、心形点或双色虹膜。暖桃肤。参考6只颜料：bob和所有灰前面/内面/背面/返回面同无光照gray#B6B4B2，mutedmint#B0C8BA仅材料条，墨线#171717。宽灰为主体，不整束绿、不添加重复深灰体积内底/渐变/高光/银白边，靠线和互遮画回折。

只输出一张连贯完整人物透明层，不带原粉背景/字幕/色卡/棋盘格/独立道具。保证两只鞋完整在画内及原maidcap双黑叶、源腰后手和开眼小笑；自然隐藏的根段不凭空补到近耳。
'''
pp=RUN/'prompt.txt';assert not pp.exists();pp.write_text(prompt,encoding='utf-8')
draft={**old,'created_utc':now,'state':'ROOT_RELEASED_ONE_FIRST_API_PREPARED','dispatchable':True,
 'PromptFile':str(pp),'prompt_sha256':sha(pp),'InputImages':[r['path'] for r in refs],
 'reference_sha256':[r['sha256'] for r in refs],'reference_roles':roles,'OutputDirectory':str(RUN),
 'Stage':'first_API_source2374_complete_unmasked_correct11_fullhead_volume_gray_returns_R50phase',
 'previous_repair_actualview_pass_gate_overridden_by_specific_missing_state_release':True,
 'requires_repaired_previous_actualview_and_live_bothreviews':False,
 'ROOT_SPECIFIC_RELEASE':ev(RUN/'ROOT_SPECIFIC_RELEASE.json'),'originals_preserved':preserved,
 'REGPLAN_central_changed':False,'new_subrun_private_compact_plan_only':old['REGPLAN_expected_compact_private_not_applied'],
 'reference_provenance':{'refs':refs,'correct11_origin_raw_sha256':'c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'},
 'artist_reference_review':ev(RUN/'ARTIST_REFERENCE_REVIEW.json'),'formal_API_PREPARED_REQUEST_written':True,
 'quota_reset_used':False,'quota_reset_revocation':ev(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json')}
save(RUN/'DRAFT_API_REQUEST_v02.json',draft)
formal={k:draft[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']}
save(RUN/'API_PREPARED_REQUEST.json',formal)
provider=Path('D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1')
save(RUN/'PROJECT_SCOPE_REFERENCE_RELEASE.json',{'project_authorization':ev(auth),'specific_release':ev(RUN/'ROOT_SPECIFIC_RELEASE.json'),'references':refs,'prompt':ev(pp),'provider_script':ev(provider),'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','quality':'high','size':'560x1216','background':'transparent','n':1,'retry':0,'one_cel_only':'ART-G33-17','no18release':True})
lock={'id':'ART-G33-17','cel':str(CEL),'formal_request':ev(RUN/'API_PREPARED_REQUEST.json'),'draft':ev(RUN/'DRAFT_API_REQUEST_v02.json'),'prompt':ev(pp),'root_release':ev(RUN/'ROOT_SPECIFIC_RELEASE.json'),'project_release':ev(RUN/'PROJECT_SCOPE_REFERENCE_RELEASE.json'),'project_authorization':ev(auth),'provider_script':ev(provider),'references':refs,'Size':'560x1216','reference_count':6,'preserved_originals':preserved,'calls_permitted':1,'retry':0}
save(RUN/'AUTHORIZED_CALL_LOCK.json',lock)
locksha=sha(RUN/'AUTHORIZED_CALL_LOCK.json')
wrapper=r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$runDirectory=$PSScriptRoot
$lockPath=Join-Path $runDirectory 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCKSHA__'){throw 'Immutable call lock changed.'}
$lock=Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
foreach($r in @($lock.formal_request,$lock.draft,$lock.prompt,$lock.root_release,$lock.project_release,$lock.project_authorization,$lock.provider_script)+@($lock.references)+@($lock.preserved_originals)){
 if((Get-FileHash -LiteralPath $r.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Released input/evidence bytes changed.'}
}
$formal=Get-Content -LiteralPath $lock.formal_request.path -Raw | ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.Size -ne '560x1216' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.InputImages.Count -ne 6 -or $formal.OutputDirectory -ne $runDirectory){throw 'Unexpected exact8field request.'}
for($i=0;$i -lt 6;$i++){if($formal.InputImages[$i] -ne $lock.references[$i].path){throw 'Reference order changed.'}}
$config=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
if(@(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'attempt.json').Count -gt 0){throw 'Existing attempt under cel; no retry.'}
if(@(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'character_api_original.png').Count -gt 0){throw 'Existing cel raw; no duplicate first API.'}
$registry=Get-Content -LiteralPath 'D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/ASSET_REGISTRY.json' -Raw | ConvertFrom-Json
if($null -ne $registry.($lock.id)){throw 'Cel already centrally registered; stop duplicate.'}
$provider=$lock.provider_script.path
if($Preview){& $provider @formal -Preview;return}
$receiptPath=Join-Path $runDirectory 'ARTIST_API_EXECUTION_RECEIPT.json'
if(Test-Path -LiteralPath $receiptPath){throw 'Invocation already recorded; no second call.'}
$started=[DateTime]::UtcNow
$receipt=@{id=$lock.id;status='authorized_invocation_started';started_utc=$started.ToString('o');formal_request_sha256=$lock.formal_request.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;root_release_sha256=$lock.root_release.sha256;project_authorization_sha256=$lock.project_authorization.sha256}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt | ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @formal;$receipt.status='provider_script_returned';$receipt.provider_result=Get-Content -LiteralPath (Join-Path $runDirectory 'result.json') -Raw | ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$started).TotalSeconds,3);Save-Receipt}
'''.replace('__LOCKSHA__',locksha)
wp=RUN/'Invoke-AuthorizedFirstOnce.ps1';assert not wp.exists();wp.write_text(wrapper,encoding='utf-8')
print(json.dumps({'run':str(RUN),'draft':ev(RUN/'DRAFT_API_REQUEST_v02.json'),'formal':ev(RUN/'API_PREPARED_REQUEST.json'),'prompt':ev(pp),'lock':ev(RUN/'AUTHORIZED_CALL_LOCK.json'),'wrapper':ev(wp),'refs':[{'path':r['path'],'sha256':r['sha256']} for r in refs]},ensure_ascii=False,indent=2))
