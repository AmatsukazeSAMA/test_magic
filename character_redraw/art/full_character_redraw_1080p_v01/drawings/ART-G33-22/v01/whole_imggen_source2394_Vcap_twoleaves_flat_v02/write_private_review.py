from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def put(n,d):
 p=R/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(p)
raw=R/'character_imggen_original.png';expected='87b6e8fb9c2efbf0beab8a959a1a343334f38ce7873998dfdc5a47267c7cc994'
assert sha(raw)==expected
src=Path('C:/Users/11515/.codex/generated_images/01a19353-0ba4-7303-865c-fe3c2a74b81f/exec-6574ae71-ad29-4385-81d5-78b80bf30e44.png');assert sha(src)==expected
req=read(R/'request_imggen.json');prov=read(R/'INPUT_PROVENANCE.json')
for x in req['reference_inputs']:assert sha(x['path'])==x['sha256']
for key in ['source_JOB','source_REGPLAN']:assert sha(prov[key]['path'])==prov[key]['sha256']
now=datetime.now(timezone.utc).isoformat()
receipt=put('PRIVATE_NATIVE_CALL_RECEIPT.json',{
 'id':'ART-G33-22','created_utc':now,'tool':'image_gen.imagegen built-in',
 'functions_exec_cell_id':'841','status':'known_completed',
 'started_utc_clock':'2026-11-01 18:38:18 UTC','finished_utc_clock':'2026-11-01 18:38:52 UTC',
 'elapsed_seconds_clock_1s_resolution':34,'native_calls':1,'API_calls_this_version':0,'automatic_retries':0,
 'request':rec(R/'request_imggen.json'),'actual_prompt':rec(R/'prompt_imggen.txt'),
 'prompt_submission':'request.prompt + trailing newline; byte-equivalent to prompt_imggen.txt',
 'referenced_images':req['reference_inputs'],'ref_count':5,'transparent_background_requested':True,
 'user_quality_preference':'high','quality_parameter_exposed':False,'model':'not exposed by built-in tool',
 'source_generated_file':rec(src),'project_raw':rec(raw),'raw_bytes_preserved':src.read_bytes()==raw.read_bytes(),
 'dimensions':[957,1644],'operation_kind':'whole_character_redraw','whole_visible_person_one_generation':True,
 'local_patch_or_mask_used':False,'technical_record':rec(R/'BUILTIN_GENERATION.json'),'technical_check':rec(R/'TECHNICAL_CHECK.json'),
 'technical_success_not_art_acceptance':True,
})
view=[raw,R/'qa_white.png',R/'qa_black.png']+[Path(x['path']) for x in req['reference_inputs']]
view += [R/'diagnostics'/n for n in ['CAP_V_ATTACHMENT_white_3x.png','ROOT_COIL_white_1x.png','ROOT_COIL_white_3x.png','ROOT_COIL_black_3x.png','SOURCE2394_vs_NATIVE22_FULL_READONLY.png','EYES_MOUTH_white_3x.png','SKIRT_GRIP_HAND_white_3x.png','BOTH_SHOES_white_1x.png']]
review=put('DRAFT_PRIMARY_REVIEW.json',{
 'id':'ART-G33-22','created_utc':now,'reviewer':'xhigh_pending_artist private visual draft; not root or Sol',
 'image':str(raw),'exact_raw_sha256':expected,'actual_viewed':[rec(p) for p in view],
 'decision':'REPAIR_REQUIRED_CAP_LOWER_EXTRA_TAIL_PERSISTS_AFTER_ONE_NATIVE',
 'primary_static_pass':False,'independent_static_pass':False,'continue_family':False,
 'cap_target_result':{'observation':'当前两片长黑叶之下，共同小底仍另接一片朝下较长尖瓣，轮廓与first API相似；不是只剩自然厚连接底。源ref3为两叶V形，无这片下垂叶。完整white/black及cap3x确认，本次修复目标未消除。','priority':'P1','repair_succeeded':False,'hypothesis_result':'新增原V局部并去掉正确11整头ref，仍未压过完整target里的旧尾形；这是观察，不声称工具内部原因已证实。'},
 'body_eye_root':{'observation':'原睁开眼的弧和单charcoal普通白点/小闭口笑、近正面头身、画右LEFT低耳nape珠、下握黑裙曲指+腰后臂、黑褶向画左、白apron/腰后bow、不同腿角和两完整踝带鞋保留。','boundary':'没有摄影对齐或逐像素原线认可。'},
 'curl_material':{'observation':'coil体量未微缩，仍gray宽前面、斜返回/末C与正确低根；但mint/gray前面仍有混色和柔和明暗，返回连接也有深浅差，未形成同色无光照的稳定读法。上端仍是帽片样front加斜返回，不能只因末C正确判全卷通过。','assessment':'HOLD fresh root/Sol；不作为geometry/materialmaster。','boundary':'不要求固定孔数，也不把不透明gray返回面全挖空。遮挡内部没有认证。'},
 'transparent_layer':'完整两底没有独立背景/字幕；原字节保留，技术alpha解码不能代替艺术通过。',
 'temporal':'未真实曝光播放914..916与25/23，动态连续及隐藏几何不认证。',
 'native_calls':1,'API_calls_this_version':0,'automatic_retries':0,'result_unknown':False,
 'JOB_REGPLAN_unchanged':True,'central_registry_modified':False,'binding_modified':False,'progress_modified':False,
 'user_accepted':False,'dynamic_validated':False,
 'next_action':'停止本参考假设，交root具体失败证据；不自动第二次native/API/蒙版或下一项。',
})
handoff=put('ARTIST_HANDOFF.json',{
 'id':'ART-G33-22','created_utc':now,'state':'ONE_NATIVE_KNOWN_RETURN_REPAIR_REQUIRED_PRIVATE_DRAFT',
 'run':str(R),'raw':rec(raw),'actual_size':[957,1644],'native_calls':1,'API_calls_this_version':0,'automatic_retries':0,'inflight':0,
 'elapsed_seconds_clock_1s_resolution':34,'quality_parameter_exposed':False,
 'full_white':rec(R/'qa_white.png'),'full_black':rec(R/'qa_black.png'),'cap3x':rec(R/'diagnostics/CAP_V_ATTACHMENT_white_3x.png'),
 'source_V_ref':rec(R/'inputs/ref3_ORIGINAL2394_V_TWO_BLACK_LEAVES_ATTACHMENT_ONLY.png'),
 'normal_coil':rec(R/'diagnostics/ROOT_COIL_white_1x.png'),'coil3x_white':rec(R/'diagnostics/ROOT_COIL_white_3x.png'),'coil3x_black':rec(R/'diagnostics/ROOT_COIL_black_3x.png'),
 'source_comparison':rec(R/'diagnostics/SOURCE2394_vs_NATIVE22_FULL_READONLY.png'),
 'private_review':review,'native_receipt':receipt,'technical':rec(R/'TECHNICAL_CHECK.json'),
 'observation_summary':'sourceV两叶假设仍未删除帽下独立尖尾，目标修复失败；原睁眼小笑/低根/手衣/完整鞋保留，卷材质与上端仍HOLD。',
 'old_API_and_failure_records_preserved':True,'central_registry_modified':False,'binding_modified':False,'progress_modified':False,'JOB_REGPLAN_modified':False,
 'no_automatic_second_call':True,'no_following_item_started':True,'quota_resets':0,'fresh_root_and_Sol_required':True,
})
print(json.dumps({'raw':rec(raw),'review':review,'receipt':receipt,'handoff':handoff,'native_calls':1,'inflight':0},ensure_ascii=False,indent=2))
