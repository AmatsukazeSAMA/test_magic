from pathlib import Path
from PIL import Image
import json,hashlib,shutil,datetime,sys

P=Path(r'D:\CODEX\魔术之心');B=P/'art/full_character_redraw_1080p_v01';CEL=B/'drawings/ART-G51-11/v01'
R=CEL/'prep_first_api_source4630_roundeyes_asymmetric_outward_low_gloves_fullshoes_graygreen_v06'
PR=B/'drawings/ART-G51-10/v01/whole_imggen_remove_isolated_under_eye_dots_source4625_v01'
OLD=B/'drawings/ART-G51-10/v01/prep_first_api_source4625_roundeyes_unequal_low_gloves_fullshoes_graygreen_v06'
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(p):return dict(path=str(Path(p).resolve()),sha256=sha(p))
def save(p,x):
    p=Path(p);assert not p.exists(),f'Preserve existing {p}';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def make_inputs():
    assert not R.exists();(R/'inputs').mkdir(parents=True)
    job=read(CEL/'JOB.json');reg=read(B/'ASSET_REGISTRY.json')
    assert job['source_frame']==4630 and job['source_pts']==2472336
    assert sha(job['source_image'])==job['source_image_sha256']
    assert 'ART-G51-11' not in reg
    known_names={'attempt.json','result.json','character_api_original.png','character_imggen_original.png','NATIVE_CALL_RECEIPT.json','ROOT_API_EXECUTION_RECEIPT.json','BUILTIN_GENERATION.json'}
    found=[str(p) for p in CEL.rglob('*') if p.is_file() and (p.name in known_names or 'unknown' in p.name.lower())]
    assert not found,found
    previous=reg['ART-G51-10'];primary=read(previous['primary_review'])
    assert previous['sha256']=='6ab6d9b3dd82a020b9244f23b451095dcdca7c5559bb7e9853be6e5547365918'
    assert sha(previous['image'])==previous['sha256']
    assert previous['primary_static_pass'] and previous['independent_static_pass'] and primary['continue_family']
    tol=B/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
    assert sha(tol)=='4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7'
    specs=[(CEL/'inputs/source_pose_guide.png','ref1_OWN4630_FULL_UNMASKED_POSE_TWO_OUTWARD_LOW_GLOVES_FULLSHOES.png',None),
           (Path(previous['image']),'ref2_PREVIOUS10_SAFE_INTERIOR_GRAYGREEN_SLEEVE_LINE_NO_BODY.png',[623,440,651,466]),
           (B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png','ref3_USER_APPROVED_X01_CURL_DRAWING_ONLY.png',None),
           (OLD/'inputs/ref4_SAFE_GRAY_UPPER_BOB_CAP_FRINGE_NO_EYES_DOTS_COIL.png','ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png',None),
           (CEL/'inputs/source_pose_guide.png','ref5_OWN4630_ROUND_UNEQUAL_EYES_TINY_NEUTRAL_MOUTH.png',[257,134,379,222])]
    refs=[];provenance=[]
    for src,name,box in specs:
        dst=R/'inputs'/name
        if box:Image.open(src).crop(box).save(dst)
        else:shutil.copyfile(src,dst);assert src.read_bytes()==dst.read_bytes()
        refs.append(str(dst.resolve()));provenance.append(dict(reference=f(dst),source=f(src),crop_xyxy=box,scale=1,operation='readonly original rectangle; no paint/alpha cleanup/part warp' if box else 'unchanged byte copy'))
    for name,box in [('OWN4630_TWO_DIFFERENT_OUTWARD_GLOVES_READONLY_2x',[35,365,628,525]),('OWN4630_COMPLETE_BOTH_SHOES_READONLY_2x',[195,845,410,975])]:
        im=Image.open(CEL/'inputs/source_pose_guide.png').crop(box);im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(R/(name+'.png'))
    prefix=read(P/'image_defaults.json')['generation_prompt_prefix']['text']
    prompt=prefix+'''

绘制ART-G51-11首次透明人物，原F4630/PTS2472336。图1是本帧唯一整体动作/眼口/手套/肩肘腕腰裙腿鞋与裁切权威，不复制前10垂臂和身姿。主角必须换成图4的中性灰短圆润bob、自然灰刘海和贴颊短侧发；图1红尖额发、左右高红卷是要完整替换的旧身份，不仅染灰，不保旧红双卷再添灰卷。图4只身份，不移植它的头倾、帽投影、表情、比例或动作。

自己的眼睛较圆睁且不等高/开度，瞳位按图1/5，小口是极小中性闭口短线/点，不是O或笑弧，勿套前10脸。两iris各一块均匀深charcoal配普通白点，无黑芯灰环/月牙或渐色。保真实方向睫毛与上外眼线，紧邻眼角的细小短笔/小短点允许少量像素间隙，不要机械抹掉；仍不新添明显独立大痣或远离眼角的装饰点。图5只负责本4630眼口，保持完整开度而非把裁图边当眼睑。

本帧双臂向两侧展开、两手套都在低位但指形/方向不同。画左上臂向下后屈肘，前臂近水平伸向画左，手腕下折，黑手套的长指/收折分指斜向左下，保简笔角折；不是上一态远臂被腰裙完全藏住。画右臂由短袖斜向右下展开，另一手套分指斜向右下，拇指独立下分，不能改成直垂近臂/拳/上指或复制画左手。两肩、肘、腕、腰和裙的相对位置严格依图1，不把左右手抬成对称同高掌。

身体较正、头轻偏，保本圆睁视线、短领、腰带位置、前围裙折线/白下边、两侧白后结带与裙形。画左腿膝有折势、鞋斜向左下，画右腿更直、鞋近竖向前，双鞋都完整且须留小透明余量，不能继承前镜底裁或添隐藏腿。白maidcap与本投影画右两MAIN黑叶、暖桃肤、黑胸结/手套袜鞋、金扣、白肩褶袖口围裙腰带后带保留；红领/泡袖/衣身/裙主布改低饱和灰绿ending。图2仅前10安全衣内灰绿颜料与一条稀疏墨线，不含完整脸手/轮廓/卷，不传前10pose、眼嘴或肩前深度。

按本近正面头颈肩，唯一人物LEFT低耳后/nape双红珠根投影在画右低bob与同侧颈肩，可自然挡住部分珠根，不抬到帽/太阳穴、不换耳或镜像。卷沿肩前胸侧自然互遮，按本头肩取中等体量；白肩褶和袖可挡根或下段，不为露全强穿肩/手、不随意缩micro。图3用户只认可curl绘法，不是整个人物、固定尺寸或轴向接受：一条宽GRAY前面翻回实际不透明GRAY内后返回，连续接第二大转与一个渐细小末C，两大加一小；真实空气透明，实体灰返回不能挖掉。mint只窄细材料边，全部bob/gray前返/C同类无打光平涂；不封口盘堆/实心柱锥、不加圈或独立灰囊，不大绿面/独立暗底/银白高光/渐变。

保手书粗细起伏、不规则简笔与疏线，不向量化精修/密添发丝。真正透明RGBA只含本帧可见人物；图1粉背景、导框及独立粉瓣不画，画左颈肩附近花瓣不变成皮肤/衣/卷，不将源遮住的细轮廓假称已观察。不烘焙背景、不加道具或额外手，完整帽/两手套/双鞋在画内。
'''
    pf=R/'prompt_api.txt';pf.write_bytes(prompt.encode('utf-8'))
    formal=dict(InputImages=refs,PromptFile=str(pf.resolve()),OutputDirectory=str(R.resolve()),OutputFileName='character_api_original.png',Size='656x1008',Quality='high',Background='transparent',Stage='FIRST_ART_G51_11_SOURCE4630_ROUNDEYES_TWO_ASYMMETRIC_OUTWARD_LOW_GLOVES_ENDING_GRAYGREEN')
    save(R/'API_PREPARED_REQUEST.json',formal)
    roles=['Own4630 complete unmasked guide: sole pose/face/eyes/hand groups/camera/extent, no original redhair identity or background/petals.',
           'Previous10 safe interior sleeve pigment/line only [623,440,651,466]; no pose/face/hands/coil/outline or shoulder-depth transfer.',
           'User original X01 CURL DRAWING ONLY; continuous gray2large+smallC opaque returns/thinmint, no fixed size/axis or whole acceptance.',
           'Only neutral gray rounded shortbob/fringe/cap identity; own4630 owns cap projection/headtilt/body/eyes, no old coil transfer.',
           'Own4630 round unequal eyes/pupil direction/tinyneutral closedmouth method; not previous10 face or generic half-lid template.']
    save(R/'REFERENCE_PROVENANCE.json',dict(id=job['id'],refs=provenance,reference_roles=roles,art_pixels_modified=False))
    save(R/'DRAFT_API_REQUEST.json',dict(id=job['id'],PREPONLY=True,formal=formal,refs=[f(p) for p in refs],reference_roles=roles,source_frame=4630,source_pts=2472336,output_size=[656,1008],original_guide_unchanged=f(CEL/'inputs/source_pose_guide.png'),REG_unchanged=f(CEL/'REGISTRATION_PLAN.json'),actual_reference_review_pending=True,eye_tolerance=f(tol),curl_baseline_scope='drawing only, not size axis wholeart',quality='high',n=1,retry=1,submitted=False,root_release_required=True,api_calls=0,native_calls=0))
    save(R/'PRE_FIRST_LOCAL_STATE_AUDIT.json',dict(id=job['id'],registry_entry_absent=True,existing_attempt_raw_result_unknown_files=found,known_names_checked=sorted(known_names),searched=str(CEL),OLD_UNKNOWN_reopened=False,source=f(job['source_image']),JOB=f(CEL/'JOB.json'),REG=f(CEL/'REGISTRATION_PLAN.json'),generation_calls=0))
    save(R/'PREDECESSOR_DUAL_REVIEW_AND_ROOT_RELEASE_GATE.json',dict(id=job['id'],predecessor=previous,primary=f(previous['primary_review']),independent=f(previous['independent_review']),continue_family_readback=True,eye_tolerance=f(tol),root_current_input_actual_review_required=True,ROOTrelease=False,all_exposure_or_dynamic_pass=False))
    print(json.dumps(dict(run=str(R),refs=refs,prompt=f(pf),formal=f(R/'API_PREPARED_REQUEST.json'),diagnostics=[str(R/'OWN4630_TWO_DIFFERENT_OUTWARD_GLOVES_READONLY_2x.png'),str(R/'OWN4630_COMPLETE_BOTH_SHOES_READONLY_2x.png')]),ensure_ascii=False))

if __name__=='__main__':make_inputs()
