from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
import hashlib,json,shutil

RUN=Path(__file__).resolve().parent
CEL=RUN.parent
BASE=RUN.parents[3]
PROJECT=BASE.parent.parent
WRAPPER=PROJECT/'scripts/Invoke-ReferenceImage.ps1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p)
    x={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        with Image.open(p) as im:x.update(dimensions=list(im.size),mode=im.mode)
    return x
def dump(p,x):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

assert not (RUN/'API_PREPARED_REQUEST.json').exists()
prior_request_artifacts=[]
for p in (BASE/'drawings/ART-G12-71').rglob('*'):
    if p.is_file() and (p.name in ['attempt.json','result.json','character_api_original.png','character_imggen_original.png','api_response.raw.json'] or 'UNKNOWN' in p.name.upper()):prior_request_artifacts.append(str(p))
assert not prior_request_artifacts,prior_request_artifacts
registry=json.loads((BASE/'ASSET_REGISTRY.json').read_text(encoding='utf-8-sig'))
assert 'ART-G12-71' not in registry
prev=registry['ART-G12-70']
assert prev['primary_static_pass'] and prev['independent_static_pass']
assert sha(prev['image'])==prev['sha256']=='018ee408b3e209e3a39ad9b305781f031776945433646fa96dfcbb34758d6690'
job=json.loads((CEL/'JOB.json').read_text(encoding='utf-8-sig'))
assert job['source_frame']==1135 and job['source_pts']==605936
native=BASE/'coverage/source_frames/F001135.png'
assert sha(native)==job['source_image_sha256']=='cc0618609c67a91d4d2e96ddda5cadb6a38a7c12bf8d51404156fd8839df4586'
AUTH=BASE/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
assert sha(AUTH)=='f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
(RUN/'inputs').mkdir(exist_ok=True)
refs=[]
def copyref(source,name,role):
    p=RUN/'inputs'/name
    shutil.copyfile(source,p)
    refs.append({**rec(p),'source_image':str(source),'source_sha256':sha(source),'role':role,'copied_without_pixel_change':True})
def cropref(source,roi,name,role):
    p=RUN/'inputs'/name
    with Image.open(source) as im:im.crop(roi).save(p)
    refs.append({**rec(p),'source_image':str(source),'source_sha256':sha(source),'crop_xyxy':roi,'role':role,'readonly_original_rectangle_no_paint_or_warp':True})
copyref(CEL/'inputs/source_pose_guide.png','ref1_ORIGINAL1135_COMPLETE_UNMASKED_ACTION_GUIDE.png','Complete original1135 sole pose/eyes/gaze/mouth/hands/cloth/cap/sourcebottom authority; redtwinhighcoil/redfringe are not OC identity/root.')
cropref(Path(prev['image']),[465,10,915,325],'ref2_REVIEWED70_BOB_CAP_IDENTITY_ONLY_NO_OLD_COIL.png','Current bothreviewed70 head/cap/roundgraybob identity/ink only, oldcoil excluded. Partialface/eyelid not current1135 aperture or pose. Lowerbob cropped, not outputedge.')
context=BASE/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
assert sha(context)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
copyref(context,'ref3_USER_CORRECT11_HEAD_COIL_RELATIVE_VOLUME_AND_CONTINUOUS_TAPER.png','User-correct11 croppedhead+completecoil relative volume/continuousgrayfront-return-nextturn-taperC only. Not source1135 eyes/mouth/raisedarm/body/axis or lighting. Context not isolatedtinycoil scale.')
cropref(CEL/'inputs/source_pose_guide.png',[550,260,765,390],'ref4_ORIGINAL1135_OWN_HALFOPEN_DOWNGAZE_SMALL_CLOSED_SMILE.png','Ownsource1135 eyelid aperture/asymmetry/downgaze/smallclosedsmile only. No original highredcoil. All iris interior onecharcoal by text/card, not blackcentergrayring.')
gray=BASE/'drawings/ART-G12-55/v01/local_v05_lowroot_continuous_gray_upturn_api_v01/inputs/ref4_PURE_UNLIT_GRAY_PIGMENT_ONLY_B6B4B2.png'
assert sha(gray)=='249d62ac2fc1c97ca652f040859d0be4296304207dc7b2641855ea33ae964751'
copyref(gray,'ref5_PURE_UNLIT_GRAY_PIGMENT_ONLY.png','PureflatGRAY#B6B4B2 only, overrides all context lighting; thinmint#B0C8BA text only.')
charcoal=RUN/'inputs/ref6_IRIS_UNIFORM_CHARCOAL_METHOD_ONLY_NO_EYE_APERTURE.png'
Image.new('RGB',(192,128),(36,35,35)).save(charcoal)
refs.append({**rec(charcoal),'role':'Uniformcharcoal#242323 methodcard only. Illustrative inputkey implements G02 single-solid-fill rule, not sampledG02pixels/eyeoutline or finalart. Whiteglints remain sourceordinaryshape.','technical_reference_colorcard_not_character_art':True})
prefix=json.loads((PROJECT/'image_defaults.json').read_text(encoding='utf-8-sig'))['generation_prompt_prefix']['text']
prompt=prefix+'\n\n'+'''绘制一张ART-G12-71/F1135完整当前可见人物，1312×784真实透明PNG，整个人物一次连贯重绘。图1是原PV唯一动作和相对比例基准：正面略低头，两眼不对称半开向下看、小闭弧笑；双臂在两侧低伸，两手各按原指形，画左指组斜向左上且拇指下分，画右指组较平向右且拇指下弯，不镜像成同手、不改成OK或祈祷。保双腕袖口、肘肩、下颌衣领、红结金扣、黑长袖、白肩褶/腰后带/围裙与原半身底裁的共同位置比例；不加源外腿鞋。图4仅放大本源眼口，不能借前后1133或1140眼开度替代。

主角换成中性灰短圆润bob女孩，不是原红尖长额发仅换灰。图2只给前邻70的bob/帽与墨线身份，不复制它的脸表演/手/旧卷；图3只给用户正确11整颗头与整束卷的相对体量、连续宽带回折/收尖C，不复制它圆眼、抬手、身体、竖直轴或明暗。完整白maidcap上仅两片MAIN黑叶按当前源投影，公共小根自然连接，没有另垂第三瓣。

本正面低头，唯一人物LEFT低耳后/nape根在画右，双红珠可由bob自然部分遮。卷从这个同侧低根向前肩/胸侧自然回收垂落；不在画左近耳长第二束，不把根升到原红高卷位置。保持与图3整头肩部相称的中等发量，不能小薄绿挂件或巨粗囊。上端宽GRAY前面连续翻回不透明同GRAY内后返回、接下一转，沿同一路径渐细为灰C；入口出口能追踪，不封口椭圆盘堆/实心锥外缠绿线，不分叉成毛束或独立灰袋。肩白褶/手臂按原真实轮廓自然遮挡，允许隐藏尾段，不强露全C、不固定洞数/圈数。

图5将bob与全部灰前/内/后返回/C统一无光照GRAY #B6B4B2平色，mint #B0C8BA只窄材料边；无深灰体积内底、银亮或渐变。图6只是虹膜均匀charcoal颜料法：每眼可见虹膜整片一色，不黑中心配灰环/月牙，保本源开度/视线和普通白点，不心形高光。肤色暖桃，原黑白长袖女仆服/红结金扣不变。全帽/bob/两掌都在画内且上左右留透明边，原可见围裙底裁保持供后续整幅定位；只输出人物，不画粉底、字幕、独立道具、色卡或alpha0隐藏RGB。'''
pp=RUN/'prompt_api.txt'
pp.write_text(prompt+'\n',encoding='utf-8')
formal={'InputImages':[r['path'] for r in refs],'PromptFile':str(pp),'OutputDirectory':str(RUN),'OutputFileName':'character_api_original.png','Size':'1312x784','Quality':'high','Background':'transparent','Stage':'GOAL ART-G12-71 F1135 FIRST sourcepose grayLEFT continuousribbon; PREPONLY root release pending'}
assert len(formal)==8
dump(RUN/'API_PREPARED_REQUEST.json',formal)
draft={'id':'ART-G12-71','PREPONLY':True,'dispatchable':False,'root_release_received':False,'API_calls_authorized':0,'API_calls':0,'HTTP_calls':0,'native_calls':0,'automatic_retries':0,'n':1,'provider':'OpenAI API','endpoint':'https://api.openai.com/v1/images/edits','model':'gpt-image-2.5-sunburst','quality':'high','size':'1312x784','background':'transparent','formal':rec(RUN/'API_PREPARED_REQUEST.json'),'prompt':rec(pp),'refs':refs,'source_frame':1135,'source_pts':605936,'JOB':rec(CEL/'JOB.json'),'REGISTRATION_PLAN':rec(CEL/'REGISTRATION_PLAN.json'),'guide_trim_xyxy':[0,0,1312,784],'guide_no_trim_or_part_transform':True,'AI_hair_reference_not_submitted':'No newly verified matching userAI phase beyond original first10 scope; native original1133/1135/1140 only phase observations, no invented AI/body reference.','source_native':rec(native),'original_next1140':rec(BASE/'coverage/source_frames/F001140.png'),'previous70_source1133':rec(BASE/'coverage/source_frames/F001133.png'),'current_previous_reviewed_asset':prev,'previousPRIMARY':rec(Path(prev['primary_review'])),'auth':rec(AUTH),'wrapper':rec(WRAPPER),'prefix_sha256':hashlib.sha256(prefix.encode('utf-8')).hexdigest(),'first_preflight_prior_artifacts':prior_request_artifacts,'source_observation':'1135 frontbow unequal halfopen downgaze smallclosedsmile, different lowoutstretched palms/longblack sleeves/whitecuffs/frills/redbowgold/waist/apronbottom.1133 rounder eyes and1140 lower closedlids not current performance. Entire guide already compact for full visiblehands.','created_utc':datetime.now(timezone.utc).isoformat()}
dump(RUN/'DRAFT_API_REQUEST.json',draft)
dump(RUN/'REQUEST_LOCK_PREPONLY.json',{'id':'ART-G12-71','PREPONLY':True,'dispatchable':False,'root_release_received':False,'formal':rec(RUN/'API_PREPARED_REQUEST.json'),'draft':rec(RUN/'DRAFT_API_REQUEST.json'),'prompt':rec(pp),'refs':refs,'wrapper':rec(WRAPPER),'auth':rec(AUTH),'n':1,'retry':0,'API_calls':0,'HTTP_calls':0,'native_calls':0})
dump(RUN/'NO_PRIOR_REQUEST_PREFLIGHT.json',{'id':'ART-G12-71','scope':'all directories beneath drawings/ART-G12-71 and live registry','prior_attempt_result_raw_unknown_files':prior_request_artifacts,'registry_entry_present':False,'known_FIRST_return':False,'paid_result_unknown':False,'new_network_or_generation_performed':False})
print(json.dumps({'formal':rec(RUN/'API_PREPARED_REQUEST.json'),'draft':rec(RUN/'DRAFT_API_REQUEST.json'),'prompt':rec(pp),'lock':rec(RUN/'REQUEST_LOCK_PREPONLY.json'),'input_paths':[r['path'] for r in refs]},ensure_ascii=False,indent=2))
