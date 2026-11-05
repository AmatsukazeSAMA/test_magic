from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib,shutil

B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
C=B/'drawings/ART-G33-17/v01'
R=Path(__file__).resolve().parent
P=C/'first_api_source2374_user11_fullcontext_v02'
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
assert read(P/'attempt.json')['status']=='completed'
assert sha(P/'character_api_original.png')=='3bd6d12bef111c96b0b0d81d3eb049a13237d4780f52b7960260b7e940ac8e84'
assert not (R/'attempt.json').exists() and not (R/'character_api_original.png').exists()
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
assert read(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json')['automatic_reset_permitted'] is False
screen=Path('C:/Users/11515/AppData/Local/Temp/codex-clipboard-70b459ea-05b0-443d-b548-d3cfc9855570.png')
screen_copy=R/'USER_DIRECTED_CURRENT17_WHITE_SCREENSHOT.png'
assert not screen_copy.exists();shutil.copyfile(screen,screen_copy)
with Image.open(screen) as a,Image.open(P/'qa_white.png') as b:
 screenshot_same_pixels=a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
release={
 'recorded_utc':now,'id':'ART-G33-17','authorization_source':'Actual user directed API repair conveyed by root specific release',
 'user_verbatim':['重新发给API修复一下','能不能在绘图的时候加一句，辫子在人物左侧？','人物的左侧，一般为画面的右侧'],
 'current_user_screenshot':ev(screen_copy),'screenshot_source':ev(screen),
 'screenshot_pixels_equal_current17_qa_white':screenshot_same_pixels,
 'actual_view_confirmation':'用户截图与当前17同构图/错侧近耳珠卷/第三黑帽尖；已实际查看。截图仅定向记录，不上传作绘画参考，绘画用原透明raw。',
 'specific_root_release':'One official API high whole coherent character redraw repair, 560x1216 transparent n1 no automatic retry. Remove wrong screen-left bead/curl; low anatomicalLEFT root projects screen-right far neck, adapt source turn/nape/frill, preserve source performance/body/hands/full two shoes, delete third black pointed leaf. No local mask, no patch. Return actual-view then stop; no18.',
 'operation_kind':'whole_character_redraw','known_parent':ev(P/'character_api_original.png'),
 'known_parent_attempt':ev(P/'attempt.json'),'known_parent_status':'completed HTTP200',
 'not_unknown_retry':True,'authorized_new_calls':1,'n':1,'quality':'high','size':'560x1216','background':'transparent','retry':0,
 'project_authorization':ev(auth),'quota_reset_revocation':ev(B/'TASK_QUOTA_RESET_REVOCATION_20261102_v01.json'),
 'quota_reset_used':False,'API_slots':1,'18_released':False}
save(R/'USER_DIRECTED_API_REPAIR_RELEASE.json',release)
oldrefs=read(P/'API_PREPARED_REQUEST.json')['InputImages']
srcs=[P/'character_api_original.png',C/'inputs/source_pose_guide.png',Path(oldrefs[2]),Path(oldrefs[3]),Path(oldrefs[5])]
names=['ref1_CURRENT17_TRANSPARENT_ORIGINAL_EDIT_TARGET_WRONG_LEFTSCREEN_ROOT.png','ref2_ORIGINAL2374_COMPLETE_GUIDE_ACTION_BOTH_SHOES.png','ref3_USER_CORRECT11_FULL_HEAD_SPIRAL_VOLUME_ONLY.png','ref4_USER_BROAD_GRAY_THIN_MINT_RETURNS_DETAIL.png','ref5_UNLIT_PIGMENTS_ONLY.png']
roles=[
 '当前17已知原透明返图，唯一编辑目标；保整体头身、原睁眼小笑、腰后手/服装/腿双完整鞋。明确其画左近耳下珠卷错误必须移除并重画正确LEFT远侧根；帽有第三小黑尖需删。原alpha0隐藏RGB不画成背景。',
 '原PV2374完整未挖头guide624x1072，唯一动作/头向/眼口/掌腕/衣身/腿鞋/裁切依据；原红双高卷不复制。不能因参考2与目标画布宽度不同单部位变换，当前目标构图整体连贯保留。',
 '用户正确11完整head/bob/低珠/整卷相对体量上下文216fd，只提供足量连续宽灰前返回/上端也绕行/逐圈收尖C，不复制正脸表演、帽叶位置、举臂或固定竖轴。',
 '最新灰卷detail0b88无脸根：宽GRAY正面与不透明返回面、薄mutedmint材料条带与连续尖C。无打光/深内底/精修高光，非封口椭圆片堆或实心柱外绕绿装饰。',
 'gray#B6B4B2/mint#B0C8BA/ink#171717仅颜料。bob与gray前/内/背/返回全部同灰无光照，保灰宽面与薄mint分区；不渐变/高光/深灰内底。']
refs=[]
for src,name,role in zip(srcs,names,roles):
 dst=I/name;assert not dst.exists();shutil.copyfile(src,dst)
 refs.append({**ev(dst),'source':ev(src),'role':role})
assert refs[2]['sha256']=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
assert refs[3]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
preserved=[ev(C/'JOB.json'),ev(C/'REGISTRATION_PLAN.json'),ev(C/'inputs/source_pose_guide.png'),ev(P/'character_api_original.png'),ev(P/'artist_return_diagnostics_v01/ARTIST_PRIVATE_RETURN_REVIEW.json')]
save(R/'ARTIST_REFERENCE_REVIEW.json',{
 'id':'ART-G33-17','reviewer':'xhigh_pending_artist','reviewed_utc':now,
 'actual_viewed':'本轮已实际看用户白底截图、当前透明raw/完整白黑、原2374guide+native full、895/898full、216fd与37ad对照、0b88细图和palette；仅采用下面5张raw refs，不上传白底截图/G02/AI或15错误稿。',
 'refs':refs,'projection':'源是头向画右的正面3/4，画左可见近耳不属于LEFT根；修复至画右远耳低nape，允许bob自然挡珠；原表演不镜像。',
 'changed_hypothesis':'首图是source-first新绘却wrong-near-ear。本轮以已知完整17原raw作明确整人修复目标，用户显式自身左侧/画右远根第一句；除旧画左珠卷和第三叶外保表演身体；不是unknown重试。',
 'preserved_originals':preserved,'local_mask_used':False,'parts_spliced':False,'operation_kind':'whole_character_redraw',
 'new_static_pass':False,'dynamic_validated':False,'user_accepted':False,'central_write':False})
prompt='''辫子固定在人物自身的左侧，不是画面左侧；正面一般在画面右侧。本稿头向画面右的正面三分之四，人物LEFT低根在画面右侧远耳/低颈侧，不能在现在画左的可见近耳下。

对参考1这张已知完整透明人物作一次连贯整人重绘修复，输出560x1216透明RGBA。保持整个人物头身、右向头姿、睁眼视线/单色charcoal虹膜/普通小圆白点、小闭弧笑、腰后双手、身体方向、黑长袖红蝴蝶结金扣白袖口肩frill围裙腰后带、交错双腿与画内完整两鞋，不镜像身体/脸/手脚，不换表演，不分件拼贴、不局部贴辫子。

明确清除参考1画左可见近耳下的错误两红珠和整束卷，那里恢复正常短灰bob/颈肩及原衣边。唯一卷接在人物自身LEFT的远侧低耳后/下bob-nape，即本稿画右远耳低颈侧，与bob/红珠/卷连续接通；根不能上抬到眼或太阳穴。根可由bob、下颌真实遮挡，根侧优先于两珠全部露出，绝不为了露珠移到近耳。正确同侧卷自然延至肩前胸侧，并按原白frill/颈领空间自然互遮，不能为避错抹掉整束或缩为小挂件，也不能把整卷摆到可见背面当外挂。人物、颈、衣领和卷在一次整人重绘中连贯。

帽白褶保留，恰好两片黑叶；删除现在多出的第三片小黑尖瓣，不能加新叶或双帽。参考2原PV2374完整guide唯一决定动作/头向/原开眼小笑/腰后两手/衣结构/腿鞋及裁切，其原红双高卷不可复制。源两只鞋全见，不能截断任何鞋尖或换脚姿；只整体适配输出，不能改局部比例。

参考3用户正确11完整头帽/整卷上下文只决定卷形和自然相对体量，不复制其正脸、举臂或固定竖直轴。参考4决定宽GRAY发带前面和真实不透明返回面、较薄mutedmint条沿卷绕行：从上端起就是同一发带的连续螺旋前返绕折，逐圈收细接正常下C。上端不能是封口椭圆帽/圆盘堆或实心锥、实心圆柱外缠绿装饰，也不能变分节绿小柱或细S。按当前透视自然互遮，不固定圈数/洞数/轴长；真实空气才透明，不把返回灰发面挖掉。大小按完整头、肩和正确11核，既不巨粗压肩也不微型挂件，保持原本足量卷体，不借远侧遮挡改掉固有发量。

参考5仅平涂颜料：bob和灰正面/内面/背面/返回面都同无光照gray#B6B4B2，mutedmint#B0C8BA只较薄材料条，墨线#171717。保持宽灰主体，不全mint、不深灰体积内底、不渐变、高光、银白亮边；靠线和互遮画回折。暖桃肤。所有实际可见人物一次整体连贯重画，输出只有透明人物层及真实空气；参考1透明区域隐藏RGB不是背景，不画灰黑光斑、粉底、字幕、棋盘格或色卡。
'''
pp=R/'prompt.txt';assert not pp.exists();pp.write_text(prompt,encoding='utf-8')
formal={'PromptFile':str(pp),'InputImages':[x['path'] for x in refs],'OutputDirectory':str(R),'Size':'560x1216','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'user_directed_known17_whole_redraw_correct_anatomicalLEFT_far_nape_remove_third_cap_leaf'}
save(R/'API_PREPARED_REQUEST.json',formal)
provider=Path('D:/CODEX/魔术之心/scripts/Invoke-ReferenceImage.ps1')
save(R/'WHOLE_CHARACTER_REPAIR_REQUEST.json',{'id':'ART-G33-17','created_utc':now,'operation_kind':'whole_character_redraw','whole_character_redraw':True,'local_mask_used':False,'parts_spliced':False,'mandatory_followup_imggen_whole':False,'mandatory_note':'此次自身即官方API完整人物重绘，未局修/贴图；若实际改为局修或拼接则必须另记mandatory imggen whole，不可省略。','known_parent':ev(P/'character_api_original.png'),'user_directed_release':ev(R/'USER_DIRECTED_API_REPAIR_RELEASE.json'),'formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(pp),'refs':refs,'output_size':[560,1216],'n':1,'retry':0,'endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','Quality':'high','Background':'transparent','previous_failed_version_preserved':True,'dynamic_validated':False,'user_accepted':False,'central_write':False,'quota_reset_used':False})
lock={'id':'ART-G33-17','formal':ev(R/'API_PREPARED_REQUEST.json'),'request':ev(R/'WHOLE_CHARACTER_REPAIR_REQUEST.json'),'prompt':ev(pp),'release':ev(R/'USER_DIRECTED_API_REPAIR_RELEASE.json'),'project_authorization':ev(auth),'provider':ev(provider),'references':refs,'preserved_originals':preserved,'parent_attempt':ev(P/'attempt.json'),'parent_attempt_path':str(P/'attempt.json')}
save(R/'AUTHORIZED_CALL_LOCK.json',lock)
wrapper=r'''#Requires -Version 7.0
param([switch]$Preview)
$ErrorActionPreference='Stop'
$lockFile=Join-Path $PSScriptRoot 'AUTHORIZED_CALL_LOCK.json'
if((Get-FileHash -LiteralPath $lockFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCKSHA__'){throw 'Immutable repair lock changed.'}
$lock=Get-Content -LiteralPath $lockFile -Raw | ConvertFrom-Json
foreach($r in @($lock.formal,$lock.request,$lock.prompt,$lock.release,$lock.project_authorization,$lock.provider,$lock.parent_attempt)+@($lock.references)+@($lock.preserved_originals)){
 if((Get-FileHash -LiteralPath $r.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Repair input/evidence changed.'}
}
$previous=Get-Content -LiteralPath $lock.parent_attempt_path -Raw | ConvertFrom-Json
if($previous.status -ne 'completed' -or $previous.http_status -ne '200'){throw 'Parent result not known completed.'}
$formal=Get-Content -LiteralPath $lock.formal.path -Raw | ConvertFrom-Json -AsHashtable
if($formal.Count -ne 8 -or $formal.InputImages.Count -ne 5 -or $formal.Size -ne '560x1216' -or $formal.Quality -ne 'high' -or $formal.Background -ne 'transparent' -or $formal.OutputDirectory -ne $PSScriptRoot){throw 'Unexpected whole-repair exact request.'}
for($i=0;$i -lt 5;$i++){if($formal.InputImages[$i] -ne $lock.references[$i].path){throw 'Reference order changed.'}}
$config=Get-Content -LiteralPath 'C:/Users/11515/.agents/skills/openai-api/api/connection.json' -Raw | ConvertFrom-Json
if($config.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured model changed.'}
$provider=$lock.provider.path
if($Preview){& $provider @formal -Preview;return}
foreach($name in @('attempt.json','character_api_original.png','ARTIST_API_EXECUTION_RECEIPT.json')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'This repair already attempted; no retry.'}}
$receiptPath=Join-Path $PSScriptRoot 'ARTIST_API_EXECUTION_RECEIPT.json'
$start=[DateTime]::UtcNow
$receipt=@{id='ART-G33-17';status='authorized_known_parent_whole_repair_invocation_started';started_utc=$start.ToString('o');operation_kind='whole_character_redraw';formal_sha256=$lock.formal.sha256;release_sha256=$lock.release.sha256;endpoint='https://api.openai.com/v1/images/edits';n=1;automatic_retries=0;local_mask_used=$false;parts_spliced=$false}
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Receipt{[IO.File]::WriteAllText($receiptPath,($receipt|ConvertTo-Json -Depth 20),$utf8)}
Save-Receipt
try{& $provider @formal;$receipt.status='provider_script_returned';$receipt.result=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'result.json') -Raw|ConvertFrom-Json}
catch{$receipt.status='failed_or_unknown_no_retry';$receipt.error=$_.Exception.Message -replace 'sk-[A-Za-z0-9_-]+','[REDACTED]';throw}
finally{$receipt.finished_utc=[DateTime]::UtcNow.ToString('o');$receipt.elapsed_seconds=[Math]::Round(([DateTime]::UtcNow-$start).TotalSeconds,3);Save-Receipt}
'''.replace('__LOCKSHA__',sha(R/'AUTHORIZED_CALL_LOCK.json'))
wp=R/'Invoke-AuthorizedWholeRepairOnce.ps1';assert not wp.exists();wp.write_text(wrapper,encoding='utf-8')
print(json.dumps({'request':ev(R/'WHOLE_CHARACTER_REPAIR_REQUEST.json'),'formal':ev(R/'API_PREPARED_REQUEST.json'),'prompt':ev(pp),'lock':ev(R/'AUTHORIZED_CALL_LOCK.json'),'release':ev(R/'USER_DIRECTED_API_REPAIR_RELEASE.json'),'refs':refs,'screenshot_exact_pixels_equal_qa_white':screenshot_same_pixels},ensure_ascii=False,indent=2))
