from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib,shutil

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01');C=B/'drawings/ART-G33-18/v01'
R=Path(__file__).resolve().parent;O=C/'draft_first_api_unmasked_source18_curl_assessment_v02_v01'
I=R/'inputs';I.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 p=Path(p)
 if p.exists():raise FileExistsError(str(p))
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
 except Exception:pass
 return d
now=datetime.now(timezone.utc).isoformat()
assert not list(C.rglob('attempt.json')) and not list(C.rglob('character_api_original.png'))
assert read(B/'ASSET_REGISTRY.json').get('ART-G33-18') is None
old=read(O/'DRAFT_API_REQUEST.json')
assert sha(O/'DRAFT_API_REQUEST.json')=='fef6343bfd055f667f8f904cfe5696c3915e3e24433dbf4af7c8b67c2acf454d'
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
assert read(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json')['automatic_reset_permitted'] is False
defaults=Path('D:/CODEX/魔术之心/image_defaults.json');prefix=read(defaults)['generation_prompt_prefix']
assert prefix['enabled'] is True
ctx=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
assert sha(ctx)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
srcs=[Path(x) for x in old['InputImages']];srcs[2]=ctx
names=['ref1_ORIGINAL2377_UNMASKED_SKIRT_GRIP_SOURCE_SHOE_CUTOFF.png','ref2_R054_HAIR_PHASE_ONLY_NO_AI_EYES_BODY.png','ref3_USER_CORRECT11_COMPLETE_HEAD_SPIRAL_VOLUME_CONTEXT.png','ref4_USER_BROAD_GRAY_RETURNS_THIN_MINT_DETAIL.png','ref5_G02_MONO_METHOD_SOURCE2377_NARROWER_APERTURE.png','ref6_UNLIT_GRAY_MINT_PIGMENTS.png']
roles=[
 '原2377完整未挖头guide624x1072仅整幅trim[32,0,608,1072]，576x1072，独占原较窄睁眼/小闭弧笑/倾头、画右手提裙指尖接触、另一腰后手、裙摆/围裙/后带/腿鞋裁切。原红双高卷不复制；前景鞋在原1080底被切，绝不补隐藏鞋尖/完整鞋底或缩整人塞鞋端。',
 'R54 hair-only ROI[517,231,554,274]37x43，仅读近肩向后外回弹与frill遮挡阶段，不复制AI闭眼/动作/根/密实卷；小可见crop不决定整束发量或固定长度/轴向。',
 '用户认可old11完整头帽bob低珠及整卷上下文216fd，原图c659而非17返图；只足量体积/宽gray上端与下段前返回绕/逐渐收尖C，不抄正脸眼口/举臂/帽位置/固定竖轴。',
 '最新用户灰detail0b88无脸根，宽GRAY前与真实不透明返回面为主体、较薄mutedmint材料条带连续绕行。不得取其方向亮暗/校服/根或封口柱形推断。',
 'G02只一种深charcoal平填iris和普通小圆白点方法；原18较窄睁眼开度/视线/眼形优先，不抄G02表演，也不抄R54全闭眼或身份参圆睁大眼。',
 'gray#B6B4B2/mint#B0C8BA/ink#171717仅无光照颜料：bob与所有gray前内背返回同灰，mint为较薄材料带，保灰主面不全绿；无暗体积内底、渐变、高光/银白亮边。']
refs=[]
for src,name,role in zip(srcs,names,roles):
 dst=I/name;assert not dst.exists();shutil.copyfile(src,dst);refs.append({**ev(dst),'source':ev(src),'role':role})
assert refs[0]['sha256']=='79d628928a1b9bdb328b00feb1c871091b826e87a9f6004edd56644696d21e05'
assert refs[1]['sha256']=='25dca2f27559e61b48eb0a2a4a8e8a443b83a6785a5e97795fb01e441393fea7'
preserved=[ev(C/'JOB.json'),ev(C/'REGISTRATION_PLAN.json'),ev(C/'inputs/source_pose_guide.png'),ev(O/'DRAFT_API_REQUEST.json'),ev(O/'DRAFT_prompt.txt')]
release={'id':'ART-G33-18','recorded_utc':now,'source':'Root specific release in current turn based on explicit user parallel missing-state instruction',
 'user_latest_verbatim':'并行把缺的绘制帧补齐',
 'root_specific_release':'Release18 FIRST API ONE official configuredhigh/n1/transparent, source2377/first899..902/R54haironly. Retain narrower source eye/mouth, skirt-grip hand and other backwaist hand, original foreground shoe cutoff at1080. AnatomicalLEFT low root in current screen-right far neck, not left near ear. 6refs originalunmasked/hairphase/correct11 fullhead216fd/graydetail0b88/G02method/palette. No17/07v11/v12 coil template. Return actualview fullwhiteblack/source and stop pending19. No central changes.',
 'authorized_new_calls':1,'cel':'ART-G33-18','is_retry':False,'Size':'608x1136','Quality':'high','Background':'transparent','n':1,'RetryCount':0,
 'root_artist_inflight_limit':1,'project_authorization':ev(auth),'quota_reset_revocation':ev(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json'),'quota_reset_used':False,
 'previous17_HOLD_not_geometry_master':True,'previous_static_gate_specific_release_override':True,'temporal_actual_playback_still_pending':True,'19_not_released':True}
save(R/'ROOT_SPECIFIC_RELEASE.json',release)
source_paths=[C/'inputs/source_pose_guide.png',Path(read(C/'JOB.json')['source_image']),B/'coverage/source_frames/F000899.png',B/'coverage/source_frames/F000902.png',B/'inputs/motion_reference_upright_first10_20261031_v01/frames/R000054.png']
save(R/'ARTIST_REFERENCE_REVIEW.json',{'id':'ART-G33-18','reviewed_utc':now,'reviewer':'xhigh_pending_artist','actual_source_viewed':[ev(x) for x in source_paths],
 'observations':{'source_performance':'原2377完整full与guide是略朝画右/轻倾头，原眼较窄但仍睁开、小闭弧笑；画右手抓裙指尖接裙折，另一手腰后，不同前后腿。不能复制R54闭眼和放手。',
 'source_shoe_cutoff':'native2377前景鞋在1080底被切断，guide底保该截断而非完整闭合鞋尖；后侧鞋可见。不能套17双鞋全见的要求，不补看不到的前鞋端，也不缩全人把鞋端装进画面。',
 'root':'唯一解剖LEFT低nape当前画右远侧，bob可遮部分红珠；不能在画左近耳下。按原转向/颈领/frill自然投影，不整卷外挂背面或拿tinyROI缩发。',
 'coil':'选正确11完整头卷216fd和0b88灰返回细节，上下都同一宽灰发带前返回绕入下一圈，渐尖C，不封口帽堆/实心柱外绕mint。足量但非v10巨大或微型挂件。17HOLD/07v11v12不作输入。',
 'eye_reference':'源较窄open优先；G02只mono/普通圆白点，不复制其心形点/眼型。'},
 'effective_refs':refs,'preserved_originals':preserved,'previous17_not_an_input':True,'new_art_pass':False,'dynamic_validated':False,'user_accepted':False,'central_write':False})
prompt=prefix['text']+'''\n\n本稿原2377头略向画面右、轻倾的正面三分之四，人物LEFT低根在画面右侧远耳/低颈侧，不能在画左可见近耳下。保原头身/身体和手脚不镜像，原红双高卷不是新根位。

为ART-G33-18重画一张完整源可见人物透明层，608x1136，整个人物一次连贯完成，简洁手书墨线与无光照平涂。参考1是原PV2377完整未挖除头像的原画布，仅裁两侧空区，独占动作、头身、头倾、眼口、手与衣装裁切。保持原较窄但仍睁开的两眼、视线与小闭弧笑，不能改为AI闭眼或参考3的大圆睁表演。画右低手抓住黑裙边，原指尖接触/裙折与腕袖方向准确保留，另一手置腰后，不能换成双手后放或放开裙子。原黑长袖、红bow金扣、白maidcap与恰好两黑叶、肩frill/袖口/围裙竖带/腰后带、提起的黑裙摆/围裙底与不同行腿照原，衣装红结不变。

尤其保原鞋裁切：原2377的前景鞋在1080画面底被截掉鞋尖，输出仍只画源可见部分并保留截断边界，不补隐藏鞋尖/完整鞋底，不缩小整个人物把裁外鞋端塞进画内；后侧鞋依源可见部分保留。不能照17“完整两鞋”画；本稿没有17作为输入，原源范围优先。仅整体等比适配当前画布，不单独拉头身、挪腰手或拉腿。

新身份短灰bob，唯一解剖LEFT低耳后/下bob-nape双红珠与卷发连续接合，本视角为画右远侧。允许bob/下颌自然挡一部分根珠，根侧优先于两珠全露；不能上抬到眼旁、换到画左近耳或镜像人。卷从同侧低颈肩自然绕至当前可见肩前胸侧，按原颈领/白frill真实互遮，不悬空/贴片，不为躲错抹掉整束、缩小发量或把全卷挂在可见背面。

参考2只取R54毛发近肩压紧后向外回弹与自然遮挡相位，绝不取AI闭眼、脸、手、身体、根位、固有发量或封口卷造型。37x43只是小可见局部，不能决定整束大小。参考3用户正确11完整头帽/bob及全卷在同坐标上的上下文，只取相对头肩足量体积、低根连接与连续螺旋渐尖C，不拷其正脸表演、头倾/举臂、帽位或固定竖轴长。参考4补宽GRAY前面与真实不透明返回面、较薄mutedmint材料条绕行：从上端第一圈就让宽灰前面向内/后弧连回下一圈，上下同一宽带螺旋，逐圈收细接末C；不能封口椭圆帽/圆盘堆、实心锥或实心柱外贴绿螺线，不分节绿挂件/细S。看完整头肩体积，既不过粗大也不微型，不套全片固定比例/轴向/圈数/洞数。真实空气才透明，灰返回不挖成洞，隐藏段/末端不强行拉出。

参考5只眼法：一种深charcoal平填虹膜配普通小圆白点，开度/眼型/视线与闭口笑仍严格参考1，不复制G02半睑形/心形点或身份参表演。暖桃肤。参考6只颜料：bob与全部灰前/内/背/返回面同gray#B6B4B2，较薄mint条#B0C8BA，墨线#171717；宽灰为主体，不全绿、不深灰体积内底、不渐变/高光/银白亮边，以墨线和互遮画返回。

输出仅连贯完整当前可见人物RGBA，不画粉背景/字幕/色卡/棋盘格/独立道具；白帽黑叶恰2。前态仍待修，连续性后续需真实PTS和actual前稿核查，本次不假称动态通过。
'''
pp=R/'prompt.txt';assert not pp.exists();pp.write_text(prompt,encoding='utf-8')
draft={**old,'created_utc':now,'state':'ROOT_RELEASED_ONE_FIRST_API_PREPARED','dispatchable':True,'requires_actual_previous_current_bothreviews':False,
 'specific_release_overrides_previous_HOLD_dispatch_gate_without_art_pass':True,
 'PromptFile':str(pp),'prompt_sha256':sha(pp),'InputImages':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],'reference_roles':roles,'OutputDirectory':str(R),
 'Stage':'first_API_source2377_original_unmasked_shoecutoff_anatomicalLEFT_correct11_fullvolume',
 'ROOT_SPECIFIC_RELEASE':ev(R/'ROOT_SPECIFIC_RELEASE.json'),'actual_reference_review':ev(R/'ARTIST_REFERENCE_REVIEW.json'),'preserved_originals':preserved,
 'formal_API_PREPARED_REQUEST_written':True,'REGPLAN_central_changed':False,'quota_reset_used':False,'prefix_expected':prefix['text']}
save(R/'DRAFT_API_REQUEST_v02.json',draft)
formal={k:draft[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']};save(R/'API_PREPARED_REQUEST.json',formal)
provider=Path('D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1')
save(R/'PROJECT_SCOPE_REFERENCE_RELEASE.json',{'id':'ART-G33-18','project_authorization':ev(auth),'specific_release':ev(R/'ROOT_SPECIFIC_RELEASE.json'),'refs':refs,'prompt':ev(pp),'provider':ev(provider),'prefix_value':prefix,'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','quality':'high','size':'608x1136','background':'transparent','n':1,'retry':0,'no19release':True})
lock={'id':'ART-G33-18','cel':str(C),'formal':ev(R/'API_PREPARED_REQUEST.json'),'draft':ev(R/'DRAFT_API_REQUEST_v02.json'),'prompt':ev(pp),'release':ev(R/'ROOT_SPECIFIC_RELEASE.json'),'project_release':ev(R/'PROJECT_SCOPE_REFERENCE_RELEASE.json'),'auth':ev(auth),'provider':ev(provider),'refs':refs,'preserved_originals':preserved,'prefix_text':prefix['text']}
save(R/'AUTHORIZED_CALL_LOCK.json',lock)
wrapper=r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lp=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCKSHA__'){throw 'Immutable 18 lock changed.'}
$lock=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($lock.formal,$lock.draft,$lock.prompt,$lock.release,$lock.project_release,$lock.auth,$lock.provider)+@($lock.refs)+@($lock.preserved_originals)){if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw 'Released 18 bytes changed.'}}
$formal=Get-Content -LiteralPath $lock.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.InputImages.Count -ne 6 -or $formal.Size -ne '608x1136' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected exact8field 18 request.'}
for($i=0;$i -lt 6;$i++){if($formal.InputImages[$i] -ne $lock.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $lock.prefix_text){throw 'Released LEFT prefix changed.'}
if(@(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'attempt.json').Count -gt 0 -or @(Get-ChildItem -LiteralPath $lock.cel -Recurse -File -Filter 'character_api_original.png').Count -gt 0){throw 'Existing18 attempt/raw; no duplicate or unknown retry.'}
$reg=Get-Content -LiteralPath 'D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/ASSET_REGISTRY.json' -Raw|ConvertFrom-Json
if($null -ne $reg.($lock.id)){throw '18 already centrally registered; stop duplicate.'}
$provider=$lock.provider.path
if($Preview){& $provider @formal -Preview;return}
$rp=Join-Path $PSScriptRoot 'ARTIST_API_EXECUTION_RECEIPT.json'
if(Test-Path -LiteralPath $rp){throw '18 invocation already recorded; no second call.'}
$start=[DateTime]::UtcNow
$receipt=@{id=$lock.id;status='authorized_FIRST_API_started';started_utc=$start.ToString('o');formal_sha256=$lock.formal.sha256;root_release_sha256=$lock.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($rp,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @formal;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
'''.replace('__LOCKSHA__',sha(R/'AUTHORIZED_CALL_LOCK.json'))
wp=R/'Invoke-AuthorizedFirstOnce.ps1';assert not wp.exists();wp.write_text(wrapper,encoding='utf-8')
print(json.dumps({'run':str(R),'draft':ev(R/'DRAFT_API_REQUEST_v02.json'),'formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(pp),'lock':ev(R/'AUTHORIZED_CALL_LOCK.json'),'refs':[{'path':x['path'],'sha256':x['sha256'],'size':x['size']} for x in refs]},ensure_ascii=False,indent=2))
