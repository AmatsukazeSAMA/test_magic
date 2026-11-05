from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'art/full_character_redraw_1080p_v01';C=Path(__file__).resolve().parent
R=(C/'direct_first_api_source4406_latest_curl_v01').resolve()
assert not R.exists()
read=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev=lambda p:{'path':str(Path(p).resolve()),'sha256':sha(p)}
job=read(C/'JOB.json');assert job['source_frame']==4406 and job['source_pts']==2352752
assert sha(job['source_image'])==job['source_image_sha256']
blocked=[str(p) for p in C.rglob('*') if p.is_file() and (p.name in {'attempt.json','result.json','character_api_original.png','character_imggen_original.png','request_manifest.json'} or 'unknown' in p.name.lower())]
assert not blocked,blocked
assert 'ART-G49-02' not in read(B/'ASSET_REGISTRY.json')
d=read(ROOT/'image_defaults.json');prefix=d['generation_prompt_prefix']['text']
assert d['api_request_policy']['quality']=='high' and d['api_request_policy']['n']==1 and d['api_request_policy']['retry']==1
provider=ROOT/'scripts/Invoke-ReferenceImage.ps1';assert sha(provider)=='f6aefc1c428e0edb99c7280e78b44b640364a1f281577623f19e25dc4feb7ab6'
(R/'inputs').mkdir(parents=True)
palette=B/'inputs/ending_gray_green_clothing_palette_only_v01.png'
patch=R/'inputs/ending_graygreen_PIGMENT_ONLY.png';Image.open(palette).crop((425,398,470,438)).save(patch)
refs=[C/'inputs/source_pose_guide.png',B/'inputs/user_approved_X01_01_curl_rendering_only_20261103_v01.png',
 B/'drawings/ART-G51-13/v01/prep_first_api_source4637_roundeyes_tinyneutralmouth_outward_unequal_gloves_crossedlegs_fullshoes_graygreen_v06/inputs/ref4_SAFE_GRAY_SHORT_ROUNDED_UPPERBOB_CAP_IDENTITY_ONLY.png',patch]
assert sha(refs[1])=='76bd9b5cc147fa98a9d9bdf6b68ef703ebdf5a9ca96d8b5b4fb291fc37c6c44b'
assert sha(refs[2])=='88b8416e41daad64b7bf9b31c878b9f099539469e33e0279bc9698193ca8676f'
body='''绘制ART-G49-02的首次透明人物，唯一原动作F4406/PTS2352752。图1是本侧背近景头颌颈、肩白褶、后立领/衣片与裁幅权威：头朝画左、身背3/4转，脸只露无眼口的小段侧面和下颌；不转正脸，不补眼睛/睫毛/嘴/鼻符号或手臂全身。顶白帽与两片MAIN黑叶原本被上边裁断，继续同源裁幅，不补完整帽或额外第三叶/长梗。下方衣肩也保持本源半身截边，不补背后身体或腿鞋。

源红尖发/长红侧发和左右高红卷都完整替换为图3中性灰短圆润bob、灰刘海与贴颊短侧发；不能只染原高红卷为灰，也不保高卷再加低卷。图3只灰短bob/帽的材料身份，不转移正面脸、眼、头姿或完整帽。整头颌颈、可见耳与身体肩转向保持图1。

本头朝画左的侧背投影，解剖LEFT是当前可见耳/下颌这一侧。唯一低LEFT根接在可见耳的低耳后/nape、靠颌颈与同侧肩的连接，bob可自然遮一珠或部分根；不要把双珠放在画右后脑/后领中央，不让珠穿颈跨背，不把根抬到帽或太阳穴。单束从此低根经人物自身左肩前方自然下落，按本视图在画左可见颈肩/白肩褶的前缘露出合理宽灰卷片段，有真实前后T遮挡；肩褶或bob可遮部分路径，不强露全部，但不能整束仍挂画右后背领面或全藏成单珠/微绿S后声称肩前。保持完整头肩比例下的合理发量，不画成小饰品，也不膨胀巨物。上一01错误后挂卷不作为输入或认可。

图2用户只认可钻发画法，不是整人、固定大小或轴向接受。一条连续宽GRAY发带：两大转之后，另有自己的小GRAY正面和实际不透明GRAY内后返回，再收细成C尖；不能第二大转直接接钩充数，不按mint线/孔数计圈。宽灰前→opaque灰返回→下一转→真正小转→C连续，不加帽高额外圈、第四主转/独立尾环，不封口盘堆/实心柱锥或断灰囊。真实露空透明，实体灰返回不可挖。全部bob/灰正面/返回/C同类无打光灰平涂，mint只细窄材料边，无大绿主面、独立暗底、银白闪片/渐变。

源可见红后立领/肩背衣片改图4小色片低饱和灰绿，仅衣服换色；白肩褶/帽、黑帽叶、暖桃肤、两红珠与灰发薄mint保身份。不补正面胸结/金扣或其它源外衣装。后领原折线/小内部切口和双肩白褶依图1，不复制图4的整身或服装轮廓（图4只有颜料）。

保原PV手书不规则简笔、粗细起伏与稀疏线，不向量化精修/密添发丝。图1字幕白字、粉底和飘瓣全部排除，字幕遮脸部分只延续已见素面与轮廓，不凭参考脸发明眼口。真实透明RGBA只含本帧可见人物，不烘焙背景、不加文字、道具、额外头/手或源外完整身体。'''
pf=R/'prompt_api.txt';pf.write_bytes((prefix+'\n\n'+body).encode('utf-8'))
assert pf.read_text('utf-8').count(prefix)==1
q={'PromptFile':str(pf),'InputImages':list(map(str,refs)),'OutputDirectory':str(R),'Size':'1072x1072','Quality':'high','Background':'transparent','OutputFileName':'character_api_original.png','Stage':'FIRST_ART_G49_02_DIRECT_SOURCE4406_LOWLEFT_FRONTSHOULDER_GRAYGREEN'}
previous=B/'drawings/ART-G49-01/v01/prep_extra_whole_api_source4401_LEFT_frontshoulder_coilbaseline_v04/qa_white.png'
record={'id':'ART-G49-02','source_frame':4406,'source_pts':2352752,'source':ev(job['source_image']),
 'recorded_utc':datetime.now(timezone.utc).isoformat(),'workflow':'User-authorized direct FIRST, one logical request only; root delegated input inspection/submission, no additional release waiting',
 'first_drawing':True,'planned_logical_requests':1,'quality':'high','n':1,'retry':1,
 'same_project_authorization':ev(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),
 'G49_01_extra_grant_used_for_this_request':False,'G49_01_prior_repair_not_retried':True,
 'local_prior_attempt_raw_result_unknown_files':blocked,'parameters':q,'provider':ev(provider),
 'actual_source_observation':'Left-facing side/rear closeup, ear/jaw/neck and shoulders only, no visible eyes/mouth/hands; top cap/leaf and bottom body are cropped. Current LEFT near visible ear resolves toward front shoulder, not rear collar.',
 'previous_actual_viewed_continuity_only':ev(previous),
 'references':[ev(p) for p in refs],
 'reference_roles':['Own4406 complete unchanged guide: sole pose/crop/action','User approved CURL DRAWING ONLY 2large+true small, not pose/size','Gray shortbob upper identity only, not face or viewpoint','Ending cloth pigment only'],
 'palette_crop':{'source':ev(palette),'crop_xyxy':[425,398,470,438],'operation':'readonly rectangle no paint/warp'},
 'requirements':ev(B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261103_v06.json'),
 'photography_validated':False,'dynamic_validated':False,'user_accepted':False}
(R/'DIRECT_REQUEST.json').write_bytes((json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'run':str(R),'request_sha256':sha(R/'DIRECT_REQUEST.json'),'prompt_sha256':sha(pf),'palette_patch':str(patch),'source':record['source'],'size':q['Size'],'references':record['references']},ensure_ascii=False))
