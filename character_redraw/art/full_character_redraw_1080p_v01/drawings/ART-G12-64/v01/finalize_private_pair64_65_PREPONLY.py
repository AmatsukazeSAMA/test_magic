from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(__file__).resolve().parents[3];PROJECT=B.parents[1]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p),'sha256':sha(p)}
auth=B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json';assert sha(auth)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
wrapper=PROJECT/'scripts/Invoke-ReferenceImage.ps1';defaults=PROJECT/'image_defaults.json';prefix=read(defaults)['generation_prompt_prefix']['text'];out=[]
template=B/'drawings/ART-G33-58/v01/prep_first_api_source2564_graybob_sourcecutoff_v01/Preview-PreparedOnly.ps1'
assert read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model']=='gpt-image-2.5-sunburst'
for n,f,v,m in [(64,1098,2,213),(65,1103,3,216)]:
 aid=f'ART-G12-{n}';CEL=B/'drawings'/aid/'v01';R=CEL/f'prep_first_api_source{f}_graybob_sourcehands_v{v:02d}'
 d=read(R/'DRAFT_API_REQUEST.json');p=read(R/'INPUT_PROVENANCE.json');now=datetime.now(timezone.utc).isoformat()
 def put(name,data):
  q=R/name;assert not q.exists();q.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return rec(q)
 assert len(d['InputImages'])==6 and not any(CEL.rglob('attempt.json')) and not any(CEL.rglob('character_api_original.png'))
 assert Path(d['PromptFile']).read_text(encoding='utf-8').startswith(prefix) and sha(d['PromptFile'])==d['prompt_sha256']
 refs=[{'path':x,'sha256':h} for x,h in zip(d['InputImages'],d['reference_sha256'])]
 for x in refs:assert sha(x['path'])==x['sha256']
 seen=refs+[p['source_full'],p['source_guide'],p['first_scene_source'],p['refs'][1]['source'],rec(CEL/f'private_source_diagnostics/R{m}_NAPE_PHASE_READONLY_6x.png')]
 put('ARTIST_REFERENCE_REVIEW.json',{'id':aid,'created_utc':now,'reviewer':'xhigh_pending_artist private actual source/ref view','actual_viewed':seen,'observations':{
  'canonical':f'JOB/PROVENANCE/catalog/PRIORITY一致{f}/PTS{d["source_pts"]}，首{d["first_case_frames"]}、PTS{d["first_case_pts"]}；无IDraw/attempt/unknown，registry无ID。',
  'identity':'LEFT首前缀后明确中性灰短圆润bob女孩/自然gray刘海贴颊侧发/低LEFT双珠，图1red尖额发侧刺不是目标且非仅改色。图1只本眼口不同双手/衣body；图3不改表演。',
  'source_action':p['frame_specific_action'],
  'source_body_and_cutoff':p['frame_specific_body'],
  'root':'当前近正面或轻画左转，唯一低LEFT仍viewerRIGHT耳后/nape/bob下，不追露脸抬根换近耳、不镜像；部分真bob/衣领遮珠不代表移根。',
  'phase':p['frame_specific_phase'],
  'AI_visibility_limit':('R213灰卷部分肩边遮，v02纯发段[608,205,646,224]38x19已实际看，排除初裁肩白褶。' if n==64 else 'R216卷大部被原白褶遮，v01/v02裁含白褶保失败历史；v03只留[610,201,646,208]36x7灰发小段，actual看无脸/眼/手/红珠。phase信息受限，不认证隐藏摆幅/内部构造。')+' tiny可见量不是固有发量，不micro，不由AI肩后遮挡硬冻结root/路线。',
  'continuity':'用户63肩前是前态要求，不能无依据整束跳回背后；64/65仍逐本源真实肩手遮挡/自然相位。63未fresh完成时只待核，不宣称实际相邻动态pass。未送63或彼此body/眼口art bitmap。',
  'geometry_material':'exact6refs全actual看；216fd整头graybob/coil给身份与合理相对头肩量/宽gray连续前内后返回+C，0b88舍高光暗底，d142纯gray全端同色+较薄mutedmint材料，不实心盖盘/巨粗/micro/固定孔轴圈长。',
  'cap_canvas':'原白cap两主黑叶+自然短公共基部P2；同JOB画布完整未挖头，保全部源掌尖/肩/半身底裁，无新trim/单部位warp/artpatch/补隐藏腿鞋，REGPLAN/JOB未改。',
 },'API_calls':0,'HTTP_calls':0,'native_calls':0,'dispatchable_by_artist':False,'root_only_actual_network_submission':True,'art_accepted':False,'dynamic_validated':False})
 fp=put('API_PREPARED_REQUEST.json',{k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']})
 lk=put('REQUEST_LOCK.json',{'id':aid,'created_utc':now,'prepared_request':fp,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'prompt_sha256':d['prompt_sha256'],'references':refs,'wrapper':rec(wrapper),'authorization':rec(auth),'JOB':p['source_JOB'],'REGISTRATION_PLAN':p['source_REGPLAN'],'size':d['Size'],'quality':'high','background':'transparent','model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits','n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,'root_must_actual_view_and_personally_send':True,'no_execution_lock_or_attempt_created':True,'mandatory_prefix':prefix,'project_defaults_path':str(defaults)})
 put('PARENT_PREPONLY_SCOPE.json',{'id':aid,'recorded_utc':now,'parent_instruction':'63保持PREPONLY。继续PREPONLY缺稿G12-64 first1098..1101及65 first1102..1105，分目录逐稿actual源和exact6refs，母帧/PTS/catalog/底裁核清。显式中性gray短bob身份，源眼口/不同手非63，固定人物LEFT低根viewerRIGHT当前转向，灰宽ribbon返回不实心/巨粗micro，跟原相位/自然肩手遮挡，AI仅purehairsecondary。6refs/high透明n1retry0/formal8/Preview/immutablelock，0execution/attempt/API/native/中央，不扩66或63network，不改旧请求。','formal':fp,'request_lock':lk,'generation_release':False,'artist_network_calls_authorized':0})
 versions=[]
 for ov in range(1,v):
  old=R.with_name(f'prep_first_api_source{f}_graybob_sourcehands_v{ov:02d}');versions.append({'old_draft':rec(old/'DRAFT_API_REQUEST.json'),'old_hair':rec(old/f'inputs/ref2_R{m}_PURE_HAIR_SECONDARY_ONLY.png')})
 put('PURE_HAIR_ROI_REFINEMENT_HISTORY.json',{'id':aid,'previous_immutable_versions':versions,'current_hair':refs[1],'current_source_crop_xyxy':p['refs'][1]['source_crop_xyxy'],'source_diagnostic':rec(CEL/f'private_source_diagnostics/R{m}_NAPE_PHASE_READONLY_6x.png'),'reason':'初裁含肩frill/boundary，收紧到纯gray发段；不把白肩当hair构造或照AI改身体。少量可见不能缩固有发量。','no_old_art_or_request_overwrite':True,'API_calls':0})
 sp=R/'Preview-PreparedOnly.ps1';assert not sp.exists();sp.write_text(template.read_text(encoding='utf-8-sig').replace('624x1072',d['Size']),encoding='utf-8')
 out.append({'id':aid,'run':str(R),'formal':fp,'lock':lk,'draft':rec(R/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),'calls':0})
print(json.dumps(out,ensure_ascii=False,indent=2))
