from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
R=Path(__file__).resolve().parent;CEL=R.parent;B=R.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,o):
 p=R/n;assert not p.exists();p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
raw=R/'character_imggen_original.png';expected='b314f6174667d73a66ea23514934490e96719d49cdb7bb7db97524b8683020d2'
assert sha(raw)==expected
request=read(R/'request_imggen.json');prov=read(R/'INPUT_PROVENANCE.json');tech=read(R/'TECHNICAL_CHECK.json')
for p in request['reference_inputs']:assert sha(p['path'])==p['sha256']
assert sha(CEL/'JOB.json')==prov['source_JOB_SHA']
assert sha(CEL/'REGISTRATION_PLAN.json')==prov['source_REGPLAN_SHA']
now=datetime.now(timezone.utc).isoformat()
src=Path('C:/Users/11515/.codex/generated_images/01a19353-0ba4-7303-865c-fe3c2a74b81f/exec-d6377151-4e22-4719-b56c-4afed2fc01b4.png')
assert sha(src)==expected
receipt=put('PRIVATE_NATIVE_CALL_RECEIPT.json',{
 'id':'ART-G33-20','created_utc':now,'tool':'image_gen.imagegen built-in',
 'functions_exec_cell_id':'814','status':'known_completed',
 'started_utc_clock':'2026-11-01 18:15:23 UTC','finished_utc_clock':'2026-11-01 18:15:54 UTC',
 'elapsed_seconds_clock_1s_resolution':31,'native_calls':1,'API_calls_this_version':0,'automatic_retries':0,
 'request':rec(R/'request_imggen.json'),'actual_prompt':rec(R/'prompt_imggen.txt'),
 'prompt_submission_expression':'request.prompt + trailing newline; equal to prompt_imggen.txt bytes',
 'referenced_images':request['reference_inputs'],'ref_count':5,
 'transparent_background_requested':True,'native_quality_parameter_exposed':False,
 'model':'not exposed by built-in tool','user_quality_preference':'high',
 'source_generated_file':rec(src),'preserved_project_raw':rec(raw),
 'dimensions':[957,1644],'source_generated_bytes_preserved':src.read_bytes()==raw.read_bytes(),
 'BUILTIN_GENERATION':rec(R/'BUILTIN_GENERATION.json'),'technical_check':rec(R/'TECHNICAL_CHECK.json'),
 'generated_result_output_hint':'Generated image saved at '+str(src)+'; original retained and copied byte-identically into own run.',
 'operation_kind':'whole_character_redraw','one_coherent_visible_person_one_call':True,
 'local_mask_or_art_patch_used':False,'art_accepted':False,
})
view=[raw,R/'qa_white.png',R/'qa_black.png']+[Path(p) for p in request['refs']]
view += [R/'diagnostics'/n for n in ['ROOT_COIL_white_1x.png','ROOT_COIL_white_3x.png','ROOT_COIL_black_3x.png','SOURCE2385_vs_NATIVE20_FULL_READONLY.png','EYES_MOUTH_white_3x.png','SKIRT_GRIP_HAND_white_3x.png']]
review=put('DRAFT_PRIMARY_REVIEW.json',{
 'id':'ART-G33-20','created_utc':now,'reviewer':'xhigh_pending_artist private visual draft; not root or Sol',
 'image':str(raw),'exact_raw_sha256':expected,'actual_viewed':[rec(p) for p in view],
 'decision':'HOLD_UPPER_RETURN_READ_AND_FLAT_MATERIAL_AFTER_ONE_WHOLE',
 'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
 'whole_subject_observation':'完整白/黑和原2385对照：当前闭合双睫弧/小闭笑、近正面轻倾、暖肤、低画右LEFT双珠与bob/nape连接、白cap+恰好2黑叶、髋侧曲指抓裙及腰后臂、围裙斜摆/腰后bow、两腿不同倾角和完整踝带鞋均保住；不认为已有摄影对齐或源线逐像素通过。',
 'curl_observation':{
  'preserved':'宽gray正面与相对头肩体量保留，mint边仍较薄；末C清楚，低根没有换侧。没有缩为薄绿小挂件。',
  'upper_return':'normal/3x可见较大的灰正面与其间斜向gray返回连接，但最上仍有圆帽/封口片的读感，前面如何翻回下一圈仍不够清楚。不能仅凭末C或整体螺旋轮廓批准上端。',
  'boundary':'不把所有opaquegray返回面等同封死孔，不要求固定孔数；被返回面/衣/bob遮挡内部不可认证。上端HOLD是可见连接读法的复核请求，不是隐藏拓扑已被代码证明。',
  'material':'bob/卷gray面仍有softgray明暗，返回处灰片相对主面较深；未形成全部gray面同一无光照色的稳定读法，暂HOLD。黑裙也保留轻soft渐色。',
 },
 'source_authority':'原2385fullguide拥有眼闭合、手抓点、衣与完整两鞋；本轮没有AI bitmap、G02或18眼环输入；只有已观察R60压紧近肩的文字相位，没有新动作。',
 'assessment':'保持私有HOLD并交freshroot/Sol，不能将该native返包/技术完整性或gray主色当艺术pass；不作为curl master。',
 'issues':[{'priority':'P1_review_requested','part':'upper coil front-return connection','description':'上端仍偏圆帽片读感，gray返回连接需要fresh审。'},{'priority':'P1_review_requested','part':'gray flat material','description':'gray明暗与return较深灰片仍可见，未清楚满足无独立打光。'}],
 'transparent_edges':'完整两底未见独立背景/字幕，原字节保留；边缘艺术接受仍由freshroot/Sol实际查看。',
 'temporal':'未按真实907..909曝光与23/25播放，不认证动态连续/固定根稳定或隐藏卷形。',
 'native_calls':1,'API_calls_this_version':0,'automatic_retries':0,
 'art_accepted':False,'dynamic_validated':False,'central_registry_modified':False,'bindings_modified':False,
 'next_action':'一图后停交root；不自动第二次、局修、API或下一稿。',
})
handoff=put('ARTIST_HANDOFF.json',{
 'id':'ART-G33-20','created_utc':now,'state':'ONE_NATIVE_WHOLE_KNOWN_RETURN_PRIVATE_HOLD',
 'run':str(R),'raw':rec(raw),'actual_size':[957,1644],'native_calls':1,'API_calls_this_version':0,'inflight':0,'automatic_retries':0,
 'elapsed_seconds_clock_1s_resolution':31,'quality_parameter_exposed':False,
 'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),
 'normal_root_coil':rec(R/'diagnostics/ROOT_COIL_white_1x.png'),'root_coil_3x_white':rec(R/'diagnostics/ROOT_COIL_white_3x.png'),'root_coil_3x_black':rec(R/'diagnostics/ROOT_COIL_black_3x.png'),
 'source_comparison':rec(R/'diagnostics/SOURCE2385_vs_NATIVE20_FULL_READONLY.png'),
 'private_review':review,'native_receipt':receipt,'request':rec(R/'request_imggen.json'),'technical':rec(R/'TECHNICAL_CHECK.json'),
 'observation_summary':'原闭眼小笑/root/2叶/手衣/完整两鞋保留；widegray和末C保留，上端圆帽片读感与gray明暗/return暗片仍HOLD。',
 'JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'bindings_modified':False,'progress_modified':False,
 'old_API_raw_and_review_preserved':True,'quota_resets':0,'no_following_cel_started':True,
 'fresh_root_and_Sol_required':True,'art_accepted':False,'dynamic_validated':False,
})
print(json.dumps({'raw':rec(raw),'receipt':receipt,'private_review':review,'handoff':handoff,'native_calls':1,'inflight':0},ensure_ascii=False,indent=2))
