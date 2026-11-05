"""Two independent first-image requests; local hashes and Preview only. No dispatch."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from PIL import Image

ROOT=Path("D:/CODEX/魔术之心")
BASE=ROOT/"art/full_character_redraw_1080p_v01"
TASK=BASE/"review/prep_s04_pending_source476507_20261102_v01"
WRAPPER=ROOT/"scripts/Invoke-ReferenceImage.ps1"
CFG=Path("C:/Users/11515/.agents/skills/openai-api/api/connection.json")
DEFAULTS=ROOT/"image_defaults.json"
AUTH=BASE/"API_PROJECT_SCOPE_AUTHORIZATION_20261101.json"
REQ=BASE/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json"
now=datetime.now(timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text("utf-8-sig"))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{"path":str(p),"sha256":sha(p)}
def textnew(p,t):
    assert not p.exists(),f"Preserve existing evidence: {p}"
    p.write_text(t,encoding="utf-8")
def save(p,obj):textnew(p,json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
def image_ev(p):
    o=ev(p);o["dimensions"]=list(Image.open(p).size);o["actual_viewed"]=True;return o
prefix=read(DEFAULTS)["generation_prompt_prefix"]["text"]
cfg=read(CFG)
assert cfg["model"]=="gpt-image-2.5-sunburst" and cfg["defaults"]["quality"]=="high"
assert sha(REQ)=="b06daa9a9a043cbd26d3af8bab5125969faf05154a93bf2f9249defc69d06e4a"
entries=read(TASK/"REFERENCE_PREPARATION_INDEX.json")
viewlog=read(TASK/"ACTUAL_VIEW_LOG_PREPONLY.json")["actual_viewed_paths"]
viewset=set(str(Path(p)) for p in viewlog)
p=read(BASE/"PROGRESS.json");reg=read(BASE/"ASSET_REGISTRY.json")
ledger=read(BASE/"coverage/EXPOSURE_LEDGER.json")
allview=[image_ev(Path(x)) for x in viewlog]
wr=WRAPPER.read_text("utf-8-sig")
assert wr.index("if ($Preview)") < wr.index("Get-OpenAIKey.ps1")
assert wr.index("return",wr.index("if ($Preview)")) < wr.index("Get-OpenAIKey.ps1")

common = """
这是手书PV逐态换人物的 FIRST 整张人物原画。只参考第1张原PV的当前动作、表情、身体比例、服装和可见裁切，输出单个人物当前真实可见部分的透明PNG。保持倒悬，不能站直、旋转转正或镜像身体。换成短灰bob、暖桃肤、同一个人物自身LEFT低耳后/颈后双红珠连接唯一连续钻发；原红色双马尾、尖红刘海和第二侧辫不能保留。

本镜源人物裸头，没有白女仆帽，也没有黑帽叶。不得从其它参考添加maidcap/两黑叶、红领结、白围裙、女仆泡袖或其它整套普通站立服装。当前原图的松灰袖、深色衣边及实际裸露皮肤才是本镜服装。参考2仅裸bob身份/倒悬发型上下文，旧眼色、旧明暗、旧卷和旧艺术通过均不继承。参考3只提供用户已认可的连续宽灰发带回绕、逐渐收尖与末C结构，不复制它的正立轴向、肩位、光斑、衣服或固定圈数。参考4唯一用于无光灰颜料；参考5唯一用于当前原表情和盘沿遮挡。五图职责不互换。

圆盘和独立道具、盘的黑边、白线幽灵/旁白/文字/背景全部由后期单独合成，本人物PNG不画。源圆盘挡住的胸、腹、躯干以及盘沿挡住的下颌口部仍是不可见区域：这些位置透明，不补一个隐藏的完整身体、不画灰白实体圆片来代替透明。严格保留实际在盘前的手掌/前臂和露在盘外的衣袖、脸、头发、皮肤，它们不因为在盘区域内就被删除；以原盘边和原人体交接处作可见轮廓边界，不出现凭空切断裸露手臂。

LEFT是人物解剖侧，不是屏幕口诀。本图是原正面偏转的倒悬姿态，相同LEFT低耳后根投影到画面偏左一侧；相对颌耳/颈后是低根，相对屏幕可能在眼线上方。按原头部滚转和真实前后层次画，不用镜像/抬根解决倒悬。双珠可被bob或原前景遮一部分，不强露两珠；只有一组红珠接一束卷，不在另一侧添加第二束。短bob保圆短轮廓，卷从同耳后低根自然接出，不像贴上的小挂件。倒悬重力使松开的发带向画面下方落并随当前头轴侧偏，不能把正立参考僵硬倒贴或把整人旋转回正。体量以完整头/颈上下文判断为中等合理发量，既不是巨大粗卷也不是tiny挂件；不规定长度、圈数、孔数或固定轴比。确实受遮挡的末段按原可见范围隐藏，不强补完整尾，也不认证隐藏数学结构。

钻发是同一条宽发带连续绕卷：宽GRAY前面接向可见GRAY内侧/返回面，再连接下一个收细转折和末端回钩；可见连接要连贯，不画独立椭圆封口盖片、互不连接的叠盘、实心锥段、接缝或重复暗块。返回面本身是实体灰发面，应不透明；只有真正露空处alpha透明，不为了挖规定数量孔而删掉灰返回面。宽面和返回面均用参考4的中性浅灰平涂，mint只是窄而柔和的材料条/边，不把整宽面涂mint绿，不画银白高光、亮边、暗体积返回面、渐变或独立光照。黑线轻简，皮肤暖桃平涂；普通眼白/很小白点按当前源可见，不复制参考旧灰环/黑中央芯或华丽反光。保持源人体手指/拇指/接触、袖口和头身比例，不美化成新立绘。

画布外及原道具遮挡的人体缺口均为真实透明alpha，不以白底假装透明；不生成背景、道具、说明字、版号、水印、分镜、光效、接触表或多个角色。只交一张同源布局的当前可见人物PNG。图1/图5的原动作和可见边界优先于所有身份/结构参考。
""".strip()

details={
"ART-G06-01":{
 "source_text":"母帧F476，PTS254128（time_base 1/16000），原可见同态最早源提名F425。输出640×1040，与图1共同原坐标。",
 "pose":"原图头在下、两条腿斜伸向画面右上；两只不同角度的脚都是裸足，保实际踝和脚趾，不加袜、踝带鞋或鞋。灰松袖位于画左下/盘旁，一只前臂横跨盘面，手掌张指向画右；另一只手在画右抓盘沿，仅重画其实际露出的手指/袖，不把盘或白线幽灵画入人物。源双眼是闭睫线、没有可见iris；保这一闭眼开度，不从旧邻稿/正确11移入睁眼。口/下颌紧邻盘沿，只有原真正露出的细线能保，盘沿挡住部分不补新张口或笑形。保原深色衣边和实际身体可见截断。",
 "observation":"倒悬偏正面；闭睫无iris。两裸足与不同脚趾角度完整可见；松灰袖、盘前横臂张掌与另一侧抓沿手可见。大圆盘遮胸腹。无maidcap/帽叶/普通女仆装；白线幽灵覆盖局部抓沿，不能认证被遮手指。",
 "source_frames":[424,425,426,475,476,477],
 "first":425,
 "aliases":["ART-G06-06"],
 "ref2_note":"保留此前G06-02裸bob部分脸上下文的闭眼；这不是当前动作/材质通过，不复制旧柔灰体积。",
},
"ART-G07-03":{
 "source_text":"母帧/本态最早源提名F507，PTS270672（time_base 1/16000）。输出1344×1024，与图1共同原坐标。",
 "pose":"原图是倒悬近景大头：脸在盘的下方，画左上有松灰衣袖/前臂截断，画右上只有抓沿手的一部分。下颌与嘴在图1/图5圆盘黑边附近被遮，不能画出一张完整的笑嘴、O口、全下巴或隐藏胸身。保原左右不等的睁眼开度与斜眼轴、普通小白点，单charcoal实色iris，无黑中心加灰外环/下月牙，不把旧邻稿的双层灰眼复制过来。此镜原图没有腿鞋，不添加完整身体或裸足来凑全身。保顶部袖/手的原画幅切断，不扩大构图露出原来没有的肢体。",
 "observation":"倒悬近景偏正面；两眼可见且不等开度，单色原瞳配普通白点；嘴/下颌被盘沿遮。顶部松灰袖、另一侧抓沿部分手指可见，腿鞋均画外。裸头无帽。与此前506在表情/裁切上有关，但当前507像素独占动作。",
 "source_frames":[506,507,508,509],
 "first":507,
 "aliases":["ART-G07-08","ART-G07-15"],
 "ref2_note":"原试选邻稿面部有旧灰月牙，已排除出正式输入；改同一原始字节的纯矩形hair-only crop，不含眼、珠卷或身体。旧试选不删除。",
}}
outputs=[]
for en in entries:
    aid=en["id"];d=details[aid];run=Path(en["run"]);parent=run.parent
    refs=en["references"].copy()
    excluded=[]
    if aid=="ART-G07-03":
        excluded=[refs[1]]
        refs[1]=read(run/"FINAL_REF2_HAIR_ONLY_PROVENANCE_PREPONLY.json")
    for i in refs:
        assert sha(Path(i["path"]))==i["sha256"]
        assert str(Path(i["path"])) in viewset
        i["path"]=str(Path(i["path"]))
    assert not list((BASE/"drawings"/aid).rglob("character*original*.png"))
    row=next(x for x in p["records"] if x["id"]==aid)
    assert row["status"]=="pending" and not row.get("image") and aid not in reg
    assert not [x for x in p["calls"] if aid in str(x.get("run",""))]
    assert sha(parent/"JOB.json")==en["job_before_sha256"]
    assert sha(parent/"REGISTRATION_PLAN.json")==en["registration_plan_before_sha256"]
    src=Path(en["source_image"]);assert sha(src)==en["source_image_sha256"]
    prompt=prefix+"\n\n"+d["source_text"]+"\n\n"+d["pose"]+"\n\n"+common+"\n"
    prompt_path=run/"prompt_api.txt";textnew(prompt_path,prompt)
    q={"PromptFile":str(prompt_path),"InputImages":[x["path"] for x in refs],
       "OutputDirectory":str(run),"Size":en["proposed_request_size"],"Quality":"high",
       "Background":"transparent","OutputFileName":"character_api_original.png",
       "Stage":aid+" FIRST original inverted visible character only; independent prop composited later; PREPONLY no dispatch"}
    formal=run/"API_PREPARED_REQUEST.json";save(formal,q)
    draft={
     "schema":"magic-maid.first-api-visible-only-preparation/1","id":aid,"created_utc":now,
     "PREPONLY":True,"submitted":False,"provider":"OpenAI official API","model":cfg["model"],
     "endpoint":"https://api.openai.com/v1/images/edits","quality":"high","n":1,
     "output_format":"png","background":"transparent","size":q["Size"],
     "first_drawing":True,"local_repair_if_later_requires_mandatory_whole":True,
     "source":ev(src),"canonical_source_frame":en["source_frame"],"source_pts":en["source_pts"],
     "first_nominated_source_frame":d["first"],"time_base":ledger["time_base"],
     "full_prefix_in_prompt":prefix,"references":refs,"excluded_input_considerations_preserved":excluded,
     "source_only_action_costume_crop":True,"ordinary_character_not_ending_palette":True,
     "disc_and_ghosts_postproduction_only":True,"hidden_torso_not_generated":True,
     "bareheaded_no_maidcap_or_blackleaves":True,"anatomical_LEFT_not_screen_mnemonic":True,
     "requirements":ev(REQ),"construction_policy_id":"open_hollow_ribbon_20261101_v01",
     "requirements_revision":"goal_curl_assessment_20261102_v03",
     "authority_scope":"Preparation only; parent root must actually view and release a new exact locked payload. Historical project API consent is not this run release.",
     "network_calls":0,"api_calls":0,"native_calls":0,"automatic_retries":0,
     "art_review_passed":False,"static_review_passed":False,"photography_review_passed":False,
     "dynamic_validated":False,"hidden_geometry_validated":False,"user_accepted":False,
    }
    draft_path=run/"FIRST_DRAFT_PREPONLY.json";save(draft_path,draft)
    source_actual=[x for x in allview if str(Path(x["path"]))==str(src) or
       any(Path(x["path"]).name==f"F{f:06d}.png" for f in d["source_frames"])]
    audit={
     "schema":"magic-maid.source-visible-scope-prep-audit/1","id":aid,"created_utc":now,
     "reviewer":"Sol xhigh actual source/input inspection; this is PREP, no art output exists",
     "status":"prepared_not_submitted","canonical":{**ev(src),"frame":en["source_frame"],"pts":en["source_pts"],"time_base":ledger["time_base"]},
     "first_nominated_source_frame":d["first"],"visible_observations":d["observation"],
     "source_visible_exposure_nominations":en["source_visible_exposure_nominations"],
     "nominations_not_bindings_or_certified_author_cel_identity":True,
     "not_all_nominated_repeats_actually_viewed":True,
     "actual_source_and_adjacent_views":source_actual,
     "own_guide":refs[0],"own_expression_disc_boundary":refs[4],
     "body_hidden_by_disc":"Keep unobserved torso transparent; preserve visible foreground hands/forearms even inside disc footprint. Do not infer missing neck/jaw/mouth.",
     "postproduction_layers":["disc surface","black disc rim","white-line ghosts","lyrics","background"],
     "inverted_LEFT_projection_hypothesis":"Same anatomical LEFT low ear/nape root; frontal inversion puts it toward viewerLEFT, screen-up relative to eye is not anatomical high root. Source head roll and occlusion control final placement; no upright rotation or person mirror.",
     "gravity_hypothesis_not_dynamic_certification":"Loose hair falls toward screen down around inverted head; no fixed turn count/length/axis. Current static source is insufficient for exact hidden 3D or playback.",
     "costume_source_exclusive":"Barehead, source loose gray sleeves/dark cloth edge; G06 source bare feet; G07 legs/feet offscreen. No imported maid costume/cap/leaves/shoes.",
     "duplicate_audit":{"progress_snapshot_utc":p.get("updated_utc"),"status":row["status"],"selected_asset_existed":False,
       "actual_return_files":[],"own_API_calls":[],"source_panel_aliases_checked_without_returns":d["aliases"],
       "excludes_known_unknown_or_already_returned_states":True},
     "independent_groups":["G06","G07"],"can_prepare_independently":True,
     "future_submission_scheduling":"Root only; not released. Independent groups may be scheduled subject to current global max2 and user/project approval.",
     "unchanged_source_job_and_registration_plan":[ev(parent/"JOB.json"),ev(parent/"REGISTRATION_PLAN.json")],
     "api_calls":0,"network_calls":0,"dynamic_validated":False,"user_accepted":False,
    }
    audit_path=run/"SOURCE_VISIBLE_SCOPE_AUDIT_PREPONLY.json";save(audit_path,audit)
    inputreview={
     "schema":"magic-maid.artist-input-review-prep/1","id":aid,"status":"prepared_not_submitted",
     "actual_viewed_references":refs,"prompt_actually_written_and_read":ev(prompt_path),
     "actual_viewed_context_only":[x for x in allview if x not in source_actual and Path(x["path"]).name not in [Path(z["path"]).name for z in refs]],
     "observation":d["ref2_note"],
     "full_correct11_head_with_maidcap_excluded_from_input":True,
     "correct11_coil_only_contains_no_cap":"77x154 approved coil geometry crop; small adjacent cloth is context, not costume",
     "gray_detail_gloss_and_equal_mint_palette_excluded":True,
     "reference_count_reason":"Five relevant references; no unrelated sixth image added to satisfy an old helper count.",
     "current_helper_release_not_invoked":"Old Release-RootReviewedFirstApi.py hardcodes six; root must deliberately update allowed relevant input count before later release.",
     "old_neighbor_art_pass_material_and_eyes_not_inherited":True,
     "source_action_or_expression_not_transferred_from_neighbors":True,
     "output_art_review_passed":False,"generation_calls":0,
    }
    review_path=run/"ARTIST_REFERENCE_REVIEW_PREPONLY.json";save(review_path,inputreview)
    lock={
     "id":aid,"created_utc":now,"status":"PREPONLY_no_generation_authorization",
     "prepared_request":ev(formal),"draft":ev(draft_path),"prompt":ev(prompt_path),
     "wrapper":ev(WRAPPER),"authorization":ev(AUTH),
     "authorization_note":"Historical project-scope consent record only; this PREP carries zero calls and root has not released this payload.",
     "JOB":ev(parent/"JOB.json"),"REGISTRATION_PLAN":ev(parent/"REGISTRATION_PLAN.json"),
     "references":[ev(Path(x["path"])) for x in refs],
     "mandatory_prefix":prefix,"model":cfg["model"],"size":q["Size"],"quality":"high","n":1,
     "background":"transparent","output_format":"png","input_count":5,
     "source_audit":ev(audit_path),"input_review":ev(review_path),"requirements":ev(REQ),
     "configured_connection_public":ev(CFG),"project_defaults_path":str(DEFAULTS),
     "generation_calls_authorized_by_this_PREP":0,"submitted":False,"network_calls":0,
     "selection_modified":False,"bind_modified":False,"dynamic_validated":False,"user_accepted":False,
    }
    lock_path=run/"REQUEST_LOCK.json";save(lock_path,lock)
    guard=r'''#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
if(-not $Preview){throw 'PREPONLY: Preview is required. This script has no dispatch branch and cannot submit.'}
$lp=Join-Path $PSScriptRoot 'REQUEST_LOCK.json'
if((Get-FileHash -LiteralPath $lp -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCK_SHA__'){throw 'PREP lock changed'}
$l=Get-Content -LiteralPath $lp -Raw|ConvertFrom-Json
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN,$l.source_audit,$l.input_review,$l.requirements,$l.configured_connection_public)+@($l.references)){
 if((Get-FileHash -LiteralPath $x.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $x.sha256){throw "Changed PREP evidence: $($x.path)"}
}
if($l.generation_calls_authorized_by_this_PREP -ne 0 -or $l.submitted){throw 'PREP scope changed'}
$q=Get-Content -LiteralPath $l.prepared_request.path -Raw|ConvertFrom-Json -AsHashtable
if($q.Count -ne 8 -or $q.InputImages.Count -ne $l.input_count -or $q.Quality -ne 'high' -or $q.Background -ne 'transparent' -or $q.Size -ne $l.size -or $q.OutputDirectory -ne $PSScriptRoot){throw 'Prepared parameters changed'}
for($i=0;$i -lt $l.input_count;$i++){if($q.InputImages[$i] -ne $l.references[$i].path){throw 'Reference order changed'}}
$defs=Get-Content -LiteralPath $l.project_defaults_path -Raw|ConvertFrom-Json
if([string]$defs.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'Configured LEFT prefix changed'}
$pt=[IO.File]::ReadAllText($l.prompt.path)
if(-not $pt.StartsWith([string]$l.mandatory_prefix,[StringComparison]::Ordinal)){throw 'Prompt lacks exact full configured prefix'}
foreach($name in @('attempt.json','result.json','character_api_original.png','ROOT_API_EXECUTION_RECEIPT.json')){
 if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw 'A prior attempt/return exists; preserve and recover. Never dispatch or retry here.'}
}
# Only Preview is passed, unconditionally. Wrapper returns before credentials/network/attempt writes.
& $l.wrapper.path @q -Preview
return
'''
    runner=run/"Preview-PreparedFirstOnly.ps1"
    textnew(runner,guard.replace("__LOCK_SHA__",sha(lock_path)))
    handoff={
     "id":aid,"created_utc":now,"PREPONLY":True,"status":"prepared_pending_root_actual_input_review",
     "request":ev(formal),"request_lock":ev(lock_path),"preview_only_runner":ev(runner),
     "prompt":ev(prompt_path),"source_audit":ev(audit_path),"input_review":ev(review_path),
     "not_generated":True,"not_static_art_pass":True,"root_release_exists":False,
     "api_calls":0,"native_calls":0,"network_calls":0,"automatic_retries":0,
     "provider":"OpenAI official API planned, not invoked","expected_quality":"high","expected_n":1,
     "after_future_return":"Preserve raw/white-black QA and exact receipt; root+independent actual art review; if local repair used, mandatory whole before adoption; photography and dynamics separately pending.",
     "release_helper_note":"Relevant count=5. Do not run old hard-six helper unchanged or invent a sixth input.",
    }
    hp=run/"ARTIST_HANDOFF_PREPONLY.json";save(hp,handoff)
    md=f"""# {aid} — FIRST PREPONLY

本次只准备，API/native/network 均0；没有艺术返图，也没有静态/摄影/动态/用户通过。未改中央表或绑定。

- 原PV母帧 F{en['source_frame']} / PTS {en['source_pts']}，time_base 1/16000；最早同态提名 F{d['first']}。提名不等于已确认绑定。
- {d['observation']}
- 请求：官方 API 参考图编辑端点，{cfg['model']} / high / n1 / transparent PNG / {q['Size']}。
- 五个正式输入见 API_PREPARED_REQUEST.json；全部已实际查看。{d['ref2_note']}
- 不输入正确11的maidcap全头，只输入卷-only；不输入带光灰细图或灰mint等面积色卡。
- 保原倒悬与真实解剖LEFT低根；不转正或镜像求侧别。盘/盘沿/幽灵/字是后期层；盘挡躯干与下颌口部不补，盘前露出的手臂掌指保留。
- preview guard 只有 -Preview 分支；不传 -Preview 会在调用wrapper前拒绝。根代理之后需实际看图/完整prompt并另行release，旧6图helper不适用于本5图准备包。
- 只可运行 Preview-PreparedFirstOnly.ps1 -Preview 检查本地锁定参数。它不会读取密钥、联网或生成。
"""
    textnew(run/"README_PREPONLY.md",md)
    outputs.append({"id":aid,"run":str(run),"request":ev(formal),"lock":ev(lock_path),"prompt":ev(prompt_path),"preview_only_runner":ev(runner),"source_audit":ev(audit_path),"handoff":ev(hp),"size":q["Size"],"reference_count":5,"submitted":False,"api_calls":0})
save(TASK/"FINAL_PREPARED_INDEX.json",{"created_utc":now,"entries":outputs,"actual_viewed_evidence":allview,"no_art_output_or_art_pass":True,"network_calls":0,"generation_calls":0})
print(json.dumps(outputs,ensure_ascii=False,indent=2))

