"""Record latest explicit user GOAL requirements and revision queues. No art edits."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

root=Path(__file__).resolve().parents[1]
base=root/'art/full_character_redraw_1080p_v01'
proof=base/'review/goal_two_large_one_small_update_20261102_v04'
proof.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ev(p):
    return {'path':str(p.resolve()),'sha256':sha(p)}
now=datetime.now(timezone.utc).isoformat()
for p in [root/'image_defaults.json',base/'GOAL_EXECUTION.json',base/'ASSET_REGISTRY.json',base/'PROGRESS.json',root/'CURRENT_SELECTION.json']:
    shutil.copyfile(p,proof/(p.name+'.before'))
refs=[]
for name,source,role in [
 ('user_curl_two_large_one_small_flat_20261102_v04.png','codex-clipboard-47d3df1c-1312-4025-97aa-cc8270b21f99.png','Primary latest user flat curl construction: two large turns plus one small terminal turn; not this face, hand, costume or pose.'),
 ('user_curl_two_large_one_small_identity_20261102_v04.png','codex-clipboard-80a4a8bc-05ae-47fd-b5c3-8c465a24755a.png','Latest original identity confirming two large turns plus a small turn. Geometry only; do not copy its polished lighting.')]:
    src=Path('C:/Users/11515/AppData/Local/Temp')/source
    dst=base/'inputs'/name
    assert src.is_file() and not dst.exists()
    shutil.copyfile(src,dst)
    refs.append({**ev(dst),'original_user_attachment':str(src),'role':role,'root_actually_viewed':True})
policy_id='hollow_two_large_one_small_20261102_v04'
reqpath=base/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v04.json'
prior=base/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
requirements={
 'requirements_revision':'goal_curl_assessment_20261102_v04','construction_policy_id':policy_id,'recorded_utc':now,
 'user_statements_verbatim':[
  '已绘制的图的核查和新图绘制一并进行',
  '其实·应该是两卷加一个小卷，更正',
  '所有图的钻发，可能都要列为修改。先列为待修改项，先进行未绘制的绘制，新绘制的要求为新的钻发要求',
  '以上列为goal','高清化需要保留线条风格','眼睛下的小点去了'],
 'reference_priority':refs,
 'turn_construction':{'large_turns':2,'small_terminal_turns':1,
  'requirement':'空心，两大卷加一个小卷，按最新用户参考的前后回折与收尖统一画法；不是三个等大卷，不额外堆叠主圈。',
  'terminal_tip':'小卷自然收尖并连续卷钩，不另加第四个大圈，不拆成独立尾环。',
  'visibility':'固有结构为两大一小；透视、压缩、弹跳及bob/肩/手臂遮挡会隐藏部分圈面，不能为凑三个可见孔而移开遮挡或补画隐藏段。'},
 'hollow_ribbon':'一条连续宽灰色发带绕空心轴翻回。宽正面、实际不透明灰内后返回、下一转和小卷连通；不可实心柱/锥、封口圆片、叠碗、断卷或仅绿线绕柱。真实露空才alpha透明，不能把实体灰返回挖掉。',
 'material':'短bob与全部卷面/返回/小卷同类无打光中性灰平涂；绿色挑染允许细化，保持窄柔和材料边。无大绿主面、独立暗底、银白闪片、渐变或第二光源。',
 'root_side':'固定人物自身LEFT低耳后/nape双红珠根。正面通常画右，背面通常画左；侧背按真实头颌近远侧和遮挡推导，可隐藏根珠。不得镜像、改耳或把远根移到近耳。',
 'mass_and_motion':'整体体量依完整头肩与相邻实际稿，不是微型挂件或巨大粗卷；每帧同一种两大一小结构。按原PV动作与真实PTS连续摆动/压缩/回弹，不换边、跳长、跳粗或断接；AI视频仅发摆参考。',
 'specific_vertical_correction':{'user_statement':'这一帧应该为垂直向下的钻发','attachment':'codex-clipboard-c71a9a39-0b74-48f8-9c6e-d39a56c0ec01.png','id_mapping':'pending_actual_lookup','requirement':'该帧改为自然垂直下垂；不把这一帧的方向强制套到全片弹跳帧。'},
 'line_and_face':'高清化保留原手书粗细起伏、不规则简笔轮廓及相对线宽；不向量化/平滑精修/添密发丝。去掉眼下独立装饰点或痣，保留真实睫毛/眼线/鼻点；眼开度、视线、嘴型依本原PV。',
 'original_authority':'原PV唯一控制人物动作、姿态、服装裁切、实际可见范围、曝光/PTS；独立字幕/背景/特效/道具留后期，不补隐藏身体。',
 'production_priority':{'primary':'先补未出首图，全部新首图使用已配置官方API high、n1、retry0并采用本规则。','parallel':'已绘制稿钻发核查与新图制作同时进行；不以完成全部旧图修复作为新首图的前置。','repair':'现有图可使用内置imggen整体修复；局修/拼接后必须整体imggen并fresh root和Sol xhigh实际复核。','concurrency':'独立镜头最多两个真实请求在途；同动作组逐张返图实际查看后继续。'},
 'existing_drawings':'所有已绘制人物稿先进入钻发待修改队列，保留旧原图/候选/评审/绑定。无可见钻发的图也须核清源遮挡或无头部依据才可标不适用，不能自动通过。',
 'reviews':'root和Sol xhigh按最新参考实际查看原图、源PV、完整白黑QA与相邻稿；旧静态通过不等于本规则通过。两大一小、空心和统一画法均需明确结论。真实PTS原速/慢速实际播放另外验证；技术hash/alpha/编码成功不是美术或动态通过。',
 'supersedes':{**ev(prior),'conflicts_superseded':['Earlier no-fixed-turn-count allowance','Earlier three-equal-large-turn interpretation','Earlier whole-art approvals used as universal curl style templates']},
 'all_existing_policy_checks_pending':True,'user_artistic_acceptance_separate':True,'goal_complete':False}
save(reqpath,requirements)
defaults=read(root/'image_defaults.json')
left=defaults['generation_prompt_prefix']['text'].split('\n')[0]
curl_sentence='罗马卷采用最新统一画法：空心，两大卷加一个小卷；宽灰正面与不透明灰返回连续接合，绿色挑染为窄细材料边。按本帧透视、摆动与遮挡绘制，不能加圈、封口成柱、换侧或强挖实体返回。'
defaults['generation_prompt_prefix']['text']=left+'\n'+curl_sentence
defaults['drill_size_rule']='Keep the latest user reference intrinsic two LARGE turns plus one SMALL terminal turn, with hollow continuous gray hair ribbon and reasonable whole-head/shoulder volume. Projection/occlusion/motion may hide surfaces, not change intrinsic construction. No universal pixel scale or forced visible-hole count.'
defaults['drill_structure_rule']={'policy_id':policy_id,'requirements':ev(reqpath),'rule':requirements['turn_construction']['requirement'],
 'construction':requirements['hollow_ribbon'],'reference_priority':refs,'material_rule':requirements['material'],
 'existing_drawings_pending_revision':True,'historical_examples_are_not_current_approval':True}
defaults['eye_style_baseline']['isolated_under_eye_dot']='Remove isolated decorative cheek/under-eye mole/dot; retain actual eyelashes, eyelid lines, source expression and small nose mark.'
defaults['handdrawn_line_preservation_requirement']=requirements['line_and_face']
save(root/'image_defaults.json',defaults)
progress=read(base/'PROGRESS.json')
registry=read(base/'ASSET_REGISTRY.json')
entries=[]
for r in progress['records']:
    image=Path(r['image']) if r.get('image') else None
    entries.append({'id':r['id'],'source_frame':r['source_frame'],'existing_image':str(image) if image else None,
      'existing_image_sha256':sha(image) if image else None,'prior_status':r['status'],
      'revision_status':'pending_curl_revision' if image else 'pending_first_image',
      'requirements_revision':requirements['requirements_revision'],'policy_id':policy_id,
      'visible_curl_or_NA_evidence':'pending actual source/full-image inspection' if image else 'new first image must follow latest requirement',
      'user_accepted':False,'dynamic_validated':False})
    if r['id'] in registry:
        registry[r['id']]['latest_curl_revision_status']='pending_curl_revision'
        registry[r['id']]['required_curl_policy_id']=policy_id
        registry[r['id']]['previous_static_approval_is_not_latest_curl_approval']=True
queuepath=base/'CURL_REVISION_QUEUE_20261102_v04.json'
save(queuepath,{'created_utc':now,'policy':ev(reqpath),'all_existing_drawings_queued':True,
 'counts':{'planned':len(entries),'existing_pending_curl_revision':sum(bool(r['existing_image']) for r in entries),'pending_first_image':sum(not r['existing_image'] for r in entries)},
 'do_not_delay_new_FIRST_for_old_repairs':True,'records':entries,'goal_complete':False})
save(base/'ASSET_REGISTRY.json',registry)
goal=read(base/'GOAL_EXECUTION.json')
goal.setdefault('curl_assessment_pointer_history',[]).append(goal['review']['mandatory_curl_requirements'])
pointer={**ev(reqpath),'requirements_revision':requirements['requirements_revision'],'construction_policy_id':policy_id,'recorded_utc':now,'old_reports_preserved':True,'no_automatic_reacceptance':True}
goal['review']['mandatory_curl_requirements']=pointer
goal['latest_hollow_drill_policy']={'policy_id':policy_id,'requirements':pointer,'reference_priority':refs,'construction':requirements['turn_construction']['requirement'],'current_rule_supersedes_history':True}
goal['existing_curl_revision_queue']=ev(queuepath)
goal['current_priority']=str(queuepath)
goal['current_priority_description']='优先未绘制首图，采用最新空心两大卷加一小卷；已绘稿钻发先列待修改，核查与新首图并行。'
goal['latest_user_production_priority']=requirements['production_priority']
goal['latest_user_line_and_face_rule']=requirements['line_and_face']
goal['updated_utc']=now
goal['complete']=False
if goal.get('latest_first_dance_review_delivery'):
    goal['latest_first_dance_review_delivery']['latest_curl_rule_eligibility']='Historical package before v04; not automatically approved under two-large-one-small requirement.'
save(base/'GOAL_EXECUTION.json',goal)
selection=read(root/'CURRENT_SELECTION.json')
selection.update({'latest_curl_requirements':pointer,'existing_curl_revision_queue':ev(queuepath),
 'current_priority':str(queuepath),'current_priority_description':goal['current_priority_description'],'latest_curl_rule_complete':False})
if selection.get('latest_first_dance_review_delivery'):
    selection['latest_first_dance_review_delivery']['latest_curl_rule_eligibility']='Historical pre-v04 package; all curl styles pending latest revision review.'
save(root/'CURRENT_SELECTION.json',selection)
md='''# GOAL 当前补充要求\n\n全片目标与4763帧真实PTS、307项绘制及确需新增项的范围保持；GOAL继续进行。\n\n- 钻发以最新两张参考为准：空心、两大卷加一个小卷；不是三个等大卷，不额外加圈。\n- 一条宽灰发带的正面、实际不透明灰返回、下一卷与小卷连续连接；不画封口盘、实心柱，不挖掉实体返回制造孔。\n- bob与卷统一无打光灰色平涂，绿色挑染可细化为窄材料边。固定人物LEFT低耳后发根，侧背按真实遮挡，邻帧体量与摆动连贯。\n- 用户指出的闭眼正面帧应垂直下垂；其他帧仍依原PV动作和摆动阶段。\n- 高清保持原手书线宽起伏与简笔轮廓；去掉眼下独立装饰点，保留眼线和睫毛。\n- 所有已绘制稿的钻发先列待修改；旧图、旧评审及旧绑定保留，不自动沿用为新标准通过。\n- **优先补未出首图**：官方API high，n=1，retry=0，新稿直接采用新钻发规则。旧稿核查和新绘并行。\n- 现有图可imggen整体修复；任何局修或拼接后必须整体imggen，再由root与Sol xhigh实际看图。\n- 静态复核、真实PTS绑定、原速慢速实际播放和用户艺术验收分别记录。默认不推送GitHub，不合成最终字幕、背景和特效。\n\n此前“圈数不固定”及临时“三个等大圈”解释已被最新“两大卷加一小卷”更正取代。\n'''
(base/'GOAL_CURRENT_REQUIREMENTS.md').write_text(md,encoding='utf-8')
save(proof/'UPDATE_RECEIPT.json',{'recorded_utc':now,'requirements':ev(reqpath),'queue':ev(queuepath),'goal':ev(base/'GOAL_EXECUTION.json'),'defaults':ev(root/'image_defaults.json'),
 'counts':read(queuepath)['counts'],'original_images_modified':False,'generation_calls':0,'old_reviews_preserved':True,'goal_active_incomplete':True})
print(json.dumps({'policy_id':policy_id,'requirements':str(reqpath),'queue_counts':read(queuepath)['counts'],'goal_updated':True,'generation_calls':0},ensure_ascii=False))
