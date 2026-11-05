from pathlib import Path
from PIL import Image
import json, hashlib, shutil, datetime, subprocess, sys

P=Path(r'D:\CODEX\魔术之心'); B=P/'art/full_character_redraw_1080p_v01'
C=B/'drawings/ART-G51-13/v01'
R=C/'prep_first_api_source4637_roundeyes_tinyneutralmouth_outward_unequal_gloves_crossedlegs_fullshoes_graygreen_v06'
PREV=B/'drawings/ART-G51-12/v01/prep_first_api_source4634_closed_smile_horizontal_outward_gloves_fullshoes_graygreen_v06'
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
f=lambda p:dict(path=str(Path(p).resolve()),sha256=sha(p))
def save(p,x):
 p=Path(p); assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')

def inputs():
 assert not R.exists()
 job=read(C/'JOB.json');registry=read(B/'ASSET_REGISTRY.json')
 assert job['source_frame']==4637 and job['source_pts']==2476080
 assert sha(job['source_image'])==job['source_image_sha256']
 assert 'ART-G51-13' not in registry
 prior_files=[str(p) for p in C.rglob('*') if p.is_file()]
 forbidden={'attempt.json','result.json','character_api_original.png','character_imggen_original.png','BUILTIN_GENERATION.json','ROOT_API_EXECUTION_RECEIPT.json'}
 assert not [p for p in C.rglob('*') if p.is_file() and (p.name in forbidden or 'unknown' in p.name.lower())]
 (R/'inputs').mkdir(parents=True)
 specs=[(C/'inputs/source_pose_guide.png','ref1_OWN4637_COMPLETE_UNMASKED_POSE_OUTWARD_GLOVES_CROSSEDLEGS_FULLSHOES.png',None),
 (PREV/'character_api_original.png','ref2_PREVIOUS12_SAFE_INTERIOR_GRAYGREEN_CLOTH_PIGMENT_ONLY.png',[257,484,294,516]),
 (B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png','ref3_USER_APPROVED_X01_CURL_DRAWING_ONLY.png',None),
 (PREV/'inputs/ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png','ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png',None),
 (C/'inputs/source_pose_guide.png','ref5_OWN4637_UNEQUAL_ROUND_EYES_TINY_NEUTRAL_CLOSEDMOUTH.png',[283,126,411,222])]
 refs=[];prov=[]
 for src,name,box in specs:
  dst=R/'inputs'/name
  if box: Image.open(src).crop(box).save(dst)
  else: shutil.copyfile(src,dst); assert src.read_bytes()==dst.read_bytes()
  refs.append(str(dst.resolve()));prov.append(dict(reference=f(dst),source=f(src),crop_xyxy=box,operation='readonly rectangle original pixels' if box else 'exact unchanged byte copy',scale=1,art_paint_or_alpha_cleanup=False))
 roles=['Own4637 complete unmasked guide alone owns pose, eyes, tiny mouth, each glove finger group, crossed legs and complete shoe extent. Original red hair/curls/background/petals are not target identity.',
 'Previous12 safe interior graygreen cloth pigment only. No contour, face, hand, root or coil; not a pose or proportion reference.',
 'User original X01 curl DRAWING ONLY: two large turns and a real smaller turn with its own gray front/opaque gray return, then C; no fixed size/axis or whole acceptance.',
 'Neutral gray short rounded bob/fringe/cap identity only. Own source determines head angle, cap placement, eyes and body; no old coil.',
 'Own4637 unequal round eye aperture/gaze and tiny neutral closed mouth; not previous12 smile or a generic half-lid template.']
 prefix=read(P/'image_defaults.json')['generation_prompt_prefix']['text']
 prompt=prefix+'''

绘制ART-G51-13首次完整透明人物，原F4637/PTS2476080。图1是本帧唯一整体动作、眼口、两只手套指组、肩肘腕腰裙腿鞋及真实裁切权威，不复制上一12的笑弧、手形或腿。主角换成图4中性灰短圆润bob、自然灰刘海及贴颊短侧发；图1红尖额发和左右高红卷须完整替换，不是只染色再加灰卷。图4只短bob身份，不能移植其表情、头倾、帽位置、比例或身体。

眼睛依图1/5较圆睁、两眼开度略不等及原视线；嘴为极小中性闭口短线/点折，不画O或上一态笑弧。两iris分别为一块均匀深charcoal配普通白点，不留黑芯灰环/月牙、双色或渐色。保真实方向睫毛和外眼线；紧邻眼角的小短笔即使有几像素间隙也允许，不添加明显独立大痣或远离眼角的装饰圆点。

两臂向左右外展开且肘低、前臂回抬，两只手都可见但不可做成对称同形。画左黑手套的长指向画左伸、其余折指层叠收拢向左下，拇指与掌的角折按图1；画右黑手套近水平向右、长指组叠向右端，拇指和折指边界按图1，保两腕不同角度和简笔形，不变拳或竖食指。自己两膝/小腿交叉，画左腿斜折到内侧、两鞋前后交叠但源可见的两只鞋都完整；前鞋更低，后鞋短露于其左上，不能冻结前12并腿姿，也不凭空画出被另一腿/鞋挡住的细节。

保图1头肩、双腕、腰、围裙中心、右扬裙摆/白下边与两白后带原相对位置。白maidcap及本投影画右两MAIN黑叶、暖桃肤、黑胸结/手套/长袜鞋、金扣、白肩褶袖口围裙腰带后带保源；红领、泡袖、衣身和裙主布改低饱和灰绿ending。图2只是前12衣内灰绿颜料，不含完整身体/姿势/脸手/卷，不能带入上一态相机或动作。

按本近正面头颈，唯一人物LEFT低耳后/nape双红珠根在画右同侧bob颈肩，依实际遮挡可隐藏部分，不抬到帽/太阳穴、不换近耳、不镜像身体。卷沿同侧肩前胸侧自然互遮，中等体量按本整头肩部判断，不小挂件不巨粗。图3用户仅认可卷的绘法，不是尺寸/轴向/整个人物认可：连续宽GRAY前面翻回不透明GRAY内后返回、接下一大转；两大转之后还有一个真正较小末转，它自身有GRAY前面和不透明GRAY返回，再收成C尖。不能拿第二大转末端hook充小卷，不能封口圆盘堆、实心柱锥或独立灰囊；不固定空气孔数，不将灰返回挖成空气。mint仅窄细材料边，bob和所有灰前/内后返/C均无独立打光平涂，不深暗体积底、银白亮边或渐变。原肩褶/手臂可自然挡部分卷，不为露全强拉到手前。

保原手书粗细起伏、不规则轮廓和稀疏简笔，不向量化精修、密添发丝。真正透明RGBA只画当前可见完整人物，帽/两手套/双鞋均留在画内；图1粉背景、细导框及独立粉花瓣全部排除。肩后、右卷后及右手腕旁粉瓣不是衣/手/发结构；源被瓣遮处的极细轮廓不能假称已看全，不烘焙背景或补隐藏肢体。
'''
 pf=R/'prompt_api.txt';pf.write_text(prompt,'utf-8')
 q=dict(InputImages=refs,PromptFile=str(pf.resolve()),OutputDirectory=str(R.resolve()),OutputFileName='character_api_original.png',Size='720x944',Quality='high',Background='transparent',Stage='FIRST_ART_G51_13_SOURCE4637_ROUNDEYES_TINYNEUTRALMOUTH_OUTWARD_UNEQUAL_GLOVES_CROSSEDLEGS_FULLSHOES_ENDING_GRAYGREEN')
 save(R/'API_PREPARED_REQUEST.json',q)
 save(R/'REFERENCE_PROVENANCE.json',dict(id=job['id'],references=prov,roles=roles,source_pixels_unchanged=True,art_pixels_edited=False))
 save(R/'DRAFT_API_REQUEST.json',dict(id=job['id'],PREPONLY=True,formal=q,references=[f(x) for x in refs],reference_roles=roles,source_frame=4637,source_pts=2476080,timebase='1/16000',quality='high',n=1,retry=1,submitted=False,root_release_required=True,api_calls=0,native_calls=0))
 for name,box in [('OWN4637_GLOVES_READONLY_2x',(32,290,692,402)),('OWN4637_CROSSED_LEGS_BOTH_SHOES_READONLY_2x',(270,568,416,906))]:
  im=Image.open(C/'inputs/source_pose_guide.png').crop(box);im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(R/(name+'.png'))
 save(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json',dict(id=job['id'],registry_entry_absent=True,prior_files=prior_files,no_known_attempt_result_raw_or_unknown=True,source=f(job['source_image']),JOB=f(C/'JOB.json'),REG=f(C/'REGISTRATION_PLAN.json'),source_guide=f(C/'inputs/source_pose_guide.png'),old_unknown_reopened=False))
 sol=B/'review/SOL_FIRST_G51_12_CURLBASELINE_20261103_v01.json'
 save(R/'PREDECESSOR_ROOT_RELEASE_GATE.json',dict(id=job['id'],previous_id='ART-G51-12',known_previous_raw=f(PREV/'character_api_original.png'),fresh_independent=f(sol),current_registry_entry=registry.get('ART-G51-12'),status='PREP_ONLY root currentcandidate readback required before network; fresh Sol can retain, ROOT finishing its own source/curl review and registry',ROOTrelease=False,continue_family_not_inferred=True))
 print(json.dumps(dict(run=str(R),formal=f(R/'API_PREPARED_REQUEST.json'),prompt=f(pf),refs=[f(x) for x in refs]),ensure_ascii=False,indent=2))

if __name__=='__main__':inputs()
