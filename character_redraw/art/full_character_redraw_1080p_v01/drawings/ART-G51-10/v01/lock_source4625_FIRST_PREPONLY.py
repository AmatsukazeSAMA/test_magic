from pathlib import Path
from datetime import datetime,timezone
import json,hashlib

JOBROOT=Path(__file__).resolve().parent
BASE=JOBROOT.parents[2];ROOT=BASE.parent.parent
RUN=(JOBROOT/'prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06').resolve()
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
def save(p,v):
 assert not p.exists(),p
 p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
defaults=read(ROOT/'image_defaults.json');prefix=defaults['generation_prompt_prefix']['text']
assert defaults['api_request_policy']['retry']==1
wrapper=ROOT/'scripts/Invoke-ReferenceImage.ps1'
assert sha(wrapper)=='f6aefc1c428e0edb99c7280e78b44b640364a1f281577623f19e25dc4feb7ab6'
prov=read(RUN/'INPUT_COPY_AND_CROP_PROVENANCE_LOCKED.json');refs=prov['references'];assert len(refs)==5
job=read(JOBROOT/'JOB.json');assert job['source_frame']==4625 and job['source_pts']==2469664
timeline=read(Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json'));assert timeline[4625]['pts']==2469664
body='''绘制 ART-G51-10 首次透明人物稿，原F4625/PTS2469664。图1完整原PV唯一决定本帧头身、眼口、肩袖肘腕、两只手套、裙后带腿鞋和共同相对布局；不要抄上一4617的低斜跨单手、侧倚姿态或相机。原红尖发和两高红卷都是要替换的身份，不是染灰就保留。图4仅中性灰圆润短bob、上刘海与帽的材料/身份片段，不负责本帧头倾、比例、表情或帽叶投影。

本帧头较正、近正面微转并略偏斜，双眼按自身不等圆睁的白眼轮廓/开度、上外眼线和视线，不套09放松半睑或其它帧闭眼。图5只保本源上段眼白/上外眼线：其下边是安全参考裁界，绝不能把双眼画成被横切的上半眼；完整眼开度以图1为准。口是图1的极小中性闭口短点/短线，不是O嘴或笑弧。虹膜各单块均匀charcoal，普通小白点，无黑芯灰环、多灰带或渐变。删除与眼线分离的独立眼下圆点/痣，即使原PV旧画法有点也不复制；保有方向且与真实外眼线相接的短睫、小鼻点，不把它们当饰点全部删光。

本帧两只黑手套都可见而且高度、指形不同。画右近臂从短袖向下较直地垂到裙侧，保长前臂与近手腕角度；较低手套在裙边/大腿外侧，外拇指向画右上折，其余错层指端向下，保源简笔角折，不改成张掌或新拳。画左远上臂/大段前臂由身体裙腰遮住，只留腰外短肤色连接和向画左下斜伸的黑手套，较长下向指与收折分指照本源；不要因另一帧只露一手而藏掉它，也不补被藏的上臂。头、两肩、近垂腕、远腰旁腕、围裙斜折、腰、膝踝鞋的相对坐标按图1共同保留。

保本裙向画左较外展、围裙偏斜前折/下缘，画右白腰后结与短长后带，较直画左腿及画右腿微斜的不同膝踝方向。两鞋都完整，画左鞋斜向画左伸、画右鞋更近竖直朝前；按源实际角度/脚底，不补隐藏身体、不用上一09的两腿斜摆。帽和两完整鞋留小透明余量，不能截手尖、帽黑叶、鞋底。

白maidcap与画右两片MAIN黑叶、白肩褶/袖口/围裙腰带后带裙边、黑胸结/手套袜鞋、金扣暖桃肤及两红珠保身份和源衣结构。原红领、短泡袖、衣身和裙主布改低饱和灰绿色ending；图2只是上一09安全衣内灰绿和一条稀疏墨线，不含脸手身体外轮廓或卷，不能转移其pose、窄紧程度、旧肩前深度或低alpha残留。不要把白袖褶/围裙或黑结一起染绿。

按本近正面头颈与肩的实际透视，固定人物自身LEFT低耳后/nape根投影在画右bob与同侧颈肩交界；可由bob遮住一珠或部分根，不抬至帽旁/太阳穴、换画左耳或镜像。同侧单束经肩前/胸侧自然落下，白肩褶与近侧泡袖可真实遮根或下段，但露出的灰正面→实际灰返回→下转要可读；不能把全束贴肩外后背再凭文字声称前绕，也不能为露全2+1强移肩、伸脖或让卷穿衣。依本头肩和垂臂空间取合理体量/摆角，不冻结上一稿coil。

图3用户仅认可钻发绘法，不是整幅人物、人设、固定大小/轴线/姿势的接受。一条连续宽GRAY带，两大转接一个渐细小末转/C：宽灰正面翻回真实不透明GRAY内后返回，再连续斜接下一大转和小C；真实露空才alpha透明。不数绿箍、不封口成灰盘/叠碗/实心柱锥、不出现断灰囊、多个额外尾环或加主圈，不挖掉实体灰返回。bob与全部灰面/返回/C同类无打光中性灰平涂，mint只窄细柔和材料边，无宽绿主面、独立暗底、渐变、银白闪片或金属光。

保原PV手书简笔的不规则轮廓、粗细起伏与稀疏线量，不向量化/平滑精修/加密发丝。真正透明RGBA只含本帧人物与衣装；去粉底粉瓣、淡导框、字幕和独立道具。原PV中的周围花瓣不属于人物，不把裁切粉背景当不透明画布。不生成源外手腿或第二束钻发。
'''
prompt=RUN/'prompt_api.txt';assert not prompt.exists();prompt.write_bytes((prefix+'\n\n'+body).encode('utf-8'))
assert prompt.read_text(encoding='utf-8').count(prefix)==1
observation='Own4625 nearlyfront head/unequal roundopen eyes/tinyclosedmouth. TWO unequalheight gloves:viewerRIGHT neararm hanging almostvertically to lower skirt/thigh with outwardupthumb and staggereddown fingers; viewerLEFT farupperarm hidden,smallwaistconnection then longdownwardglove. Ownleftflaredskirt/obliqueapron/rightbackties/twocomplete differentlyangledshoes. Unlike09 diagonal singlevisibleglove/sidelean. Under-eye separated points excluded from ref5 upper-only eye slice; mouth solely fullguide/text.'
gate=RUN/'PREDECESSOR_DUAL_REVIEW_AND_ROOT_RELEASE_GATE.json'
draft={'id':job['id'],'operation_kind':'first_drawing','first_drawing':True,'PREPONLY':True,'dispatchable':False,'source_frame':4625,'source_pts':2469664,'timebase':'1/16000','source':ev(job['source_image']),'JOB':ev(JOBROOT/'JOB.json'),'REGISTRATION_PLAN':ev(JOBROOT/'REGISTRATION_PLAN.json'),'local_unstarted_audit':ev(RUN/'PRE_FIRST_LOCAL_STATE_AUDIT.json'),'references':refs,'provenance':ev(RUN/'INPUT_COPY_AND_CROP_PROVENANCE_LOCKED.json'),'prompt':ev(prompt),'output_size':'624x1072','quality':'high','n':1,'retry':1,'background':'transparent','predecessor_gate':ev(gate),'requirements':ev(BASE/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),'curl_scope':ev(BASE/'USER_APPROVED_X01_01_CURL_RENDERING_BASELINE_20261103_v01.json'),'actual_source_observation':observation,'planned_logical_requests':1,'API_calls':0,'native_calls':0,'network_calls':0,'root_release_received':False,'central_JOB_REG_unchanged':True,'photography_validated':False,'dynamic_validated':False,'user_accepted':False}
save(RUN/'DRAFT_API_REQUEST.json',draft)
formal={'InputImages':[str(Path(x['path']).resolve()) for x in refs],'PromptFile':str(prompt.resolve()),'OutputDirectory':str(RUN.resolve()),'OutputFileName':'character_api_original.png','Size':'624x1072','Quality':'high','Background':'transparent','Stage':'FIRST_ART_G51_10_SOURCE4625_ROUNDEYES_TWO_UNEQUAL_LOW_GLOVES_ENDING_GRAYGREEN'}
assert len(formal)==8 and '\\' in formal['OutputDirectory']
save(RUN/'API_PREPARED_REQUEST.json',formal)
lock={'id':job['id'],'operation_kind':'first_drawing','first_drawing':True,'prepared_request':ev(RUN/'API_PREPARED_REQUEST.json'),'draft':ev(RUN/'DRAFT_API_REQUEST.json'),'prompt':ev(prompt),'wrapper':ev(wrapper),'authorization':ev(BASE/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),'JOB':ev(JOBROOT/'JOB.json'),'REGISTRATION_PLAN':ev(JOBROOT/'REGISTRATION_PLAN.json'),'predecessor_gate':ev(gate),'references':[{k:x[k] for k in ['path','sha256']} for x in refs],'mandatory_prefix':prefix,'retry':1,'PREPONLY':True,'submitted':False,'n':1,'planned_logical_requests':1,'API_calls':0,'native_calls':0,'root_release_required':True}
save(RUN/'REQUEST_LOCK.json',lock)
oldpreview=BASE/'drawings/ART-G51-08/v01/prep_first_api_source4613_relaxedeyes_bentforearm_single_glove_fullshoes_graygreen_v06/Invoke-PreparedPreviewOnly.ps1'
script=oldpreview.read_text(encoding='utf-8-sig').replace('6b35456c9687104fcf65573a3c76641d9fee205d54995ed6772871aea02f8d9f',sha(RUN/'REQUEST_LOCK.json'))
assert sha(RUN/'REQUEST_LOCK.json') in script
runner=RUN/'Invoke-PreparedPreviewOnly.ps1';assert not runner.exists();runner.write_bytes(script.encode('utf-8'))
print(json.dumps({'run':str(RUN),'formal':ev(RUN/'API_PREPARED_REQUEST.json'),'prompt':ev(prompt),'lock':ev(RUN/'REQUEST_LOCK.json'),'preview_only_runner':ev(runner)},ensure_ascii=False,indent=2))
