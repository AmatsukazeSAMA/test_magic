from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(r'D:\CODEX\魔术之心');B=P/'art/full_character_redraw_1080p_v01';C=B/'drawings/ART-G07-01/v01'
R=C/'prep_first_api_source532_inverted_halfeyes_gray_sleeve_visible_disc_occlusion_v06'
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(p):return dict(path=str(Path(p).resolve()),sha256=sha(p))
def save(p,x):p=Path(p);assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
assert not R.exists();(R/'inputs').mkdir(parents=True)
j=read(C/'JOB.json');reg=read(B/'ASSET_REGISTRY.json');progress=read(B/'PROGRESS.json')
assert j['source_frame']==532 and j['source_pts']==284016 and sha(j['source_image'])==j['source_image_sha256']
assert 'ART-G07-01' not in reg
names={'attempt.json','result.json','character_api_original.png','character_imggen_original.png','ROOT_API_EXECUTION_RECEIPT.json','NATIVE_CALL_RECEIPT.json'}
found=[str(p) for p in C.rglob('*') if p.is_file() and (p.name in names or 'unknown' in p.name.lower())];assert not found,found
prev=reg['ART-G07-14'];primary=read(prev['primary_review'])
assert prev['sha256']=='7b68bfaf3f6cc39f8075fad614d90b9c7af45a84baee30ad7b3a1898df104f07' and sha(prev['image'])==prev['sha256']
assert prev['primary_static_pass'] and prev['independent_static_pass'] and primary['continue_family']
spec=[(C/'inputs/source_pose_guide.png','ref1_OWN532_COMPLETE_INVERTED_SOURCE_POSE_OCCLUSION_ONLY.png',None),
      (Path(prev['image']),'ref2_PREVIOUS14_SAFE_INTERIOR_GRAY_SLEEVE_PIGMENT_ONLY.png',[280,125,350,175]),
      (B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png','ref3_USER_APPROVED_CURL_DRAWING_ONLY_NOT_UPRIGHT_AXIS.png',None),
      (Path(prev['image']),'ref4_SAFE_INVERTED_GRAY_BOB_INTERIOR_ONLY_NO_EYES_COIL_CAP.png',[650,650,970,825]),
      (Path(j['source_image']),'ref5_OWN532_INVERTED_HALFOPEN_EYES_ONLY_NO_HIDDEN_MOUTH.png',[504,349,915,505])]
refs=[];prov=[]
for src,name,box in spec:
    dst=R/'inputs'/name
    if box:Image.open(src).crop(box).save(dst)
    else:shutil.copyfile(src,dst);assert src.read_bytes()==dst.read_bytes()
    refs.append(str(dst.resolve()));prov.append(dict(reference=f(dst),source=f(src),crop_xyxy=box,scale=1,operation='read-only original rectangular selection, no painting/mask/warp' if box else 'unchanged byte copy'))
prefix=read(P/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=prefix+'''

绘制ART-G07-01首次透明可见人物，原F532/PTS284016，保持图1倒置的头/灰松袖/局部裸手，不转正、不镜像。图1独占当前头倾/眼开合视线、皮肤/衣袖/手指、实际裁边和盘遮挡；图2/4只给灰衣颜料与灰短bob画法，不复制前态表情/手型/根位或旧卷形。不是片尾女仆灰绿衣，不添加maidcap/黑帽叶、胸结、裙腿鞋等本镜看不见的部件。

主角完整换成中性灰短圆润bob，保本脸/头的相对位置与倒置投影，重建自然短灰刘海和贴颊短侧发；图1红尖额发和双高红卷不是目标，全部替换，不能只染灰或留红发再加第三束卷。图4仅本身graybob内部稀疏发线/色面，不是整头轮廓或眼睛、旧卷模板。图5本倒置半开眼负责两眼各自不等开度/上外睑方向和瞳位，勿抄直立正脸圆睁/闭眼；iris各单一均匀深charcoal和普通白点，不黑芯灰环/月牙/渐变。紧邻眼角的细小短笔容许少量像素间隔，保真实睫毛/眼线，不添明显独立装饰痣。源嘴/下颌中央被盘遮住，不新画完整嘴、隐藏颈胸或补成完整正脸。

本镜近正面倒置，人物自身LEFT仍是同一个耳后/nape：此投影落在画面左侧可见耳与bob颈侧，不能机械套直立正面画右，更不能将全人翻镜。低耳后是人物解剖位置，不是画面向下；可由bob/灰袖/盘的真实遮挡隐藏珠根，不为露全两珠将根抬到太阳穴/头顶或绕到另一耳。只保同侧单束双红珠，不复制源双高卷，也不把上一14旧root/轴当本帧已证。

图3只提供用户认可的curl绘法，绝非整个人物、固定大小/轴向或正立方向接受。按本倒置头颈体量、重力与实际可见空间画合理中量：连续宽GRAY前面翻回不透明GRAY内后返回，接第二大转后还要有自己灰前/灰返回的真实小末转，再渐细C尖；不能仅把第二大转末端钩一下冒充小卷，不能加主圈、封口盘堆/实心锥柱/独立灰囊或绿线缠柱。真实露空透明，实体灰返回保不透明；被bob/盘/袖挡的段不强露。所有bob/GRAY前返/小卷/C无打光同类灰平涂，mint仅细窄材料边，无大绿面、独立暗底、银白亮片/渐变。不把小尺寸参考像素当整束大小。

只输出本源实际可见人物RGBA：画面上方的灰宽松袖及真实露出的皮肤段、右上裁出画面的几根裸指按图1原弯折与接点保留，不能补完整隐藏掌腕/手臂或改成手套。大白圆盘及其外沿/窄弧是独立道具，不属于人物，整个盘面与盘遮住的人体中心必须真透明；保原手指与灰袖实见边界，不把盘下圆弧封成袖口/颈线，不加盘、硬环/连接楔片。粉背景、白描边粉圈、字幕/独立特效都不画，也不当发卷或手；特效遮住的细边不宣称已见。源画外裁到的袖/手不要补全，未见躯干腿鞋不画。

保原手书简笔粗细起伏/稀疏线、不规则轮廓与相对线宽，不向量化精修/密添发丝。图1只管本动作与遮挡，图2灰袖内部不提供新动作，图4无旧实心卷/眼法，不将任何旧稿非当前curl规则通过当新卷合格。人物各可见部分一次连贯画，独立props/字幕特效留后期。
'''
pf=R/'prompt_api.txt';pf.write_bytes(prompt.encode('utf-8'))
q=dict(InputImages=refs,PromptFile=str(pf.resolve()),OutputDirectory=str(R.resolve()),OutputFileName='character_api_original.png',Size='1408x992',Quality='high',Background='transparent',Stage='FIRST_ART_G07_01_SOURCE532_INVERTED_HALFOPEN_EYES_GRAY_SLEEVE_VISIBLE_ONLY_NO_DISC')
save(R/'API_PREPARED_REQUEST.json',q)
roles=['Own532 complete guide ONLY pose, inverted eyes/face, actual gray sleeve/visible bare fingers/cut/prop occlusion. Red double drills and disc/caption/FX are not output.',
       'Previous14 safe gray sleeve interior pigment only, no character outline/face/hands/coil or action transfer. Old candidate is not current curl-policy approved.',
       'User X01 CURL DRAWING ONLY continuous broadgray/opaquegrayreturns 2large+one real smallturn then C/thinmint; no upright axis/whole art/size transfer.',
       'Gray bob interior rectangle only; no eyes, root, oldcoil, cap, body or full-head proportions. Own532 controls inverted head.',
       'Own532 original inverted half-open eye aperture/gaze/liner only. No G02 half-lid bitmap, no hidden mouth reconstruction.']
tol=B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
save(R/'DRAFT_API_REQUEST.json',dict(id=j['id'],PREPONLY=True,formal=q,refs=[f(p) for p in refs],reference_roles=roles,source_frame=532,source_pts=284016,source=f(j['source_image']),guide_unchanged=f(C/'inputs/source_pose_guide.png'),REG_unchanged=f(C/'REGISTRATION_PLAN.json'),quality='high',n=1,retry=1,eye_tolerance=f(tol),predecessor_oldrule_only=True,root_actual_inputs_review_required=True,submitted=False,API_calls=0,native_calls=0))
save(R/'REFERENCE_PROVENANCE.json',dict(id=j['id'],refs=prov,roles=roles,art_pixels_modified=False,no_local_mask_or_art_paste=True))
save(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json',dict(id=j['id'],progress_record=[x for x in progress['records'] if x.get('id')==j['id']],progress=f(B/'PROGRESS.json'),registry_entry_absent=True,no_attempt_result_unknown_in_own_cel=True,checked_known_files=sorted(names),found=found,source=f(j['source_image']),JOB=f(C/'JOB.json'),REG=f(C/'REGISTRATION_PLAN.json'),generation_calls=0))
save(R/'PREDECESSOR_DUAL_REVIEW_AND_ROOT_RELEASE_GATE.json',dict(id=j['id'],previous_id='ART-G07-14',registry_readback=prev,primary=f(prev['primary_review']),independent=f(prev['independent_review']),continue_family_readback=True,old_static_pass_is_not_current_curl_pass=True,oldcurl_not_input=True,predecessor_source_JOB=f(B/'drawings/ART-G07-14/v01/JOB.json'),root_actual_new_refs_required=True,ROOTrelease=False,photography_or_dynamic_certified=False))
save(R/'PENDING_GROUP_SELECTION_READONLY.json',dict(id=j['id'],selection='Earliest missing FIRST with existing actually viewed current predecessor and no own attempt; group family_order0 firsts already have artifacts/registry.',status_counts=progress['status_counts'],other_scope=[dict(group='G33',candidate='ART-G33-19',predecessor='ART-G33-18',status='next possible no-attempt candidate, not prepared this task'),dict(group='G33',candidate='ART-G33-16',status='prior attempt; not reopened'),dict(group='G13/X01/X02/G49',status='explicit root gates/extra budget respected; not touched'),dict(group='G51',candidate='ART-G51-11',status='parent owns submitted lane; not duplicated')],source_checked=True,network_calls=0,generation_calls=0,central_modified=False))
print(json.dumps(dict(run=str(R),refs=refs,formal=f(R/'API_PREPARED_REQUEST.json'),prompt=f(pf)),ensure_ascii=False))
