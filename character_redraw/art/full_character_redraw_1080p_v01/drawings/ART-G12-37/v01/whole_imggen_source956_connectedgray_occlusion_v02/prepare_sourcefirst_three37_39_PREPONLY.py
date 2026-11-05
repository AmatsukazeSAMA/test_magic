from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json
import hashlib
import shutil

HERE = Path(__file__).resolve().parent
B = HERE.parents[3]
PROJECT = B.parents[1]
H = Path(r'D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p = Path(p)
    d = {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower() == '.png':
        with Image.open(p) as im: d.update(size=list(im.size),mode=im.mode)
    return d
def put(r,name,d):
    f=r/name;assert not f.exists(),f
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rec(f)

now=datetime.now(timezone.utc).isoformat()
registry_path=B/'ASSET_REGISTRY.json';registry=read(registry_path)
scope_path=B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json';states=read(scope_path)['states']
prefix=read(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
identity=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
detail=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png'
palette=B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png'
policy=B/'USER_DANCE_CURL_CORRECTIONS_20261102_v01.json'
requirements=B/'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
assert sha(identity)=='216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528'
assert sha(detail)=='4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'
assert sha(palette)=='d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0'

rows=[{'id': 'ART-G12-37',
  'source': 956,
  'pts': 510384,
  'first': [956, 961],
  'first_pts': [510384, 513584],
  'run': 'whole_imggen_source956_connectedgray_occlusion_v02',
  'selected_sha': 'dbfde3c6be11e813575cf65cf7e739fdd3f3ae4e43dd4ae6fdcc0c673f83c35f',
  'first_API_sha': '904d3217bb183792270d681bbb03d9f50f1b550ef3786f0f601e495dbc23320b',
  'fifth_crop': [238, 322, 425, 449],
  'fifth_name': 'ref5_ORIGINAL956_OWN_UNEQUAL_OPEN_EYES_CATLIKE_CLOSED_MOUTH.png',
  'fifth_role': '仅本956斜向不对称睁眼弧、虹膜露出/视线和浅双弧猫形闭口。图2身份眼/AI半睑笑不拥有开度，不贴原艺术像素。',
  'evidence_frames': [956, 961],
  'root_projection': '本956头轻向画左倾、前侧三分之四投影。画左可见近耳不是LEFT根；唯一人物LEFT低根在画右远耳后/低bob-nape，按bob与颈肩自然遮挡。不得在画左近耳加双珠，不能为了露全两珠抬到外眼/上耳；不镜像头身或双手。',
  'action': '原956头倾画左，双眼睁开但斜弧与虹膜露出不对称，画左眼比身份模板更压，浅双弧猫形闭口，不换单弧大笑。双掌抬到画右近并、近竖直，前掌较宽且独立拇指横伸，后掌手指部分藏于前掌后；保各自指端/掌线和不同袖口，不是合成一只手或通用合十。两black长袖交叉横过胸前，原肘角/白袖口折线与红bow被袖遮挡的关系保持。白肩fan和竖frill、黑领、红bow金扣、白cap两黑叶、腰带后bow与apron/black裙可见底段依原图。',
  'extent': '800x1072完整原guide保本头/两只高手/交叉袖/腰与下apron共同比例及原1080底裁。本源只见半身到apron黑裙，底边原本截断；不添加未见腿鞋，不缩躯干或移手以露全卷尾。',
  'motion': '已实际看R100全图，颈肩侧卷上部压紧回折、先向肩侧外弯再下收，末端靠白frill/前black袖遮挡；仅用本相位文字，不提交AI完整头身/半睑笑或小封闭卷位图。小可见段不定义固有发量缩小，也不强拉完整C到袖前。',
  'repair': '用户明确点名母956钻发形态错误，current registry repair_required覆盖旧PRIMARY/Sol88 '
            'retained。Sol88当时没有可见结构P1；旧软gray/暗局部与R100相位P2保持历史，不伪称旧Sol已否决。本轮可见珠下灰斜椭圆前面接数段mint斜弧，起卷向内后返回的入口/出口未清楚形成连续绕行；下灰返回/末端被白frill和black前袖遮挡，不能证明隐藏全卷，也不能仅因零洞判实心。低LEFT远根/原手身有可保依据，体量应以整头肩判断，不沿旧卷几何或孤立小ROI冻结。',
  'hypothesis': '完整未挖头原956 guide独占本表演/布局，排除旧37完整头与封闭斜弧卷，不重复旧whole作edit '
                'target。正确11整头卷给OCgray短bob/低根与相对体量，latestgraydetail给宽gray前内后返回连接，purekey统一同灰，第五本源眼口防身份/AI改开度。检验拿掉旧卷构造锚的source-first假设，非已证明模型内部原因；保真实肩褶/交叉袖遮挡。',
  'specific_prompt': '低LEFT双红珠下同一宽GRAY发带由前面翻向内/后返回并接下一圈，画清本态露出的起卷入口出口，不独立椭圆盖面接薄荷封口片。发带近肩压紧但保头肩相对发量，宽gray返回不挖空、不全mint。真实白frill/前black袖会遮住后段，隐藏C不硬露；可见返回仍连续朝渐细末C方向，不把遮挡当作缩成小饰品。图5只956不对称斜睁眼与双弧闭口，双高手指接触和交叉袖全听图1。',
  'neighbor': 'actual956/961为同一PRIORITY原画态，头倾与近并竖掌、交叉袖不随曝光机械另造item；后962..965转更分叉的双高手，966..969再分为高低掌。只当前源态准备，不认证相邻曝光或动态连续。'},
 {'id': 'ART-G12-38',
  'source': 963,
  'pts': 514112,
  'first': [962, 965],
  'first_pts': [513584, 515712],
  'run': 'whole_imggen_source963_connectedgray_occlusion_v02',
  'selected_sha': 'cc57c106e719e7a706485eb72147519c0dc7409476e72e69158eb41134e38528',
  'first_API_sha': '283b34ec727b0c854eb8798e4fdcd3073444bdcece7d87cd5e49d150ddacdd58',
  'fifth_crop': [195, 237, 390, 374],
  'fifth_name': 'ref5_ORIGINAL963_OWN_UNEQUAL_ROUND_OPEN_EYES_ARC_CLOSED_SMILE.png',
  'fifth_role': '仅本963左右不同圆睁眼弧/iris露出视线、单弧小闭笑。不得沿37双弧口或身份/AI半睑，原像素仅只读参考。',
  'evidence_frames': [962, 965],
  'root_projection': '本963前侧三分之四且头更倾画左，画左可见近耳不接珠；人物LEFT远耳后低bob-nape根投影在画右。按bob/颈肩自然遮挡可少露珠，但不能抬到太阳穴/上耳或换近耳，不镜像身体/掌。',
  'action': '原963头比37更倾画左，双眼不对称圆睁、单弧小闭笑，不能复制37双弧口或AI半睑。两手仍抬画右但比37分开，前掌斜伸、后掌较竖，分叉指扇/独立拇指/掌内线及前后袖口方向分别保留，不是套用37近并长指或合成通用合十。前black袖横胸、后臂折高，原肘点和红bow被横袖挡住关系保持。原黑长袖白袖口、白肩fan竖frill、黑领红bow金扣、白cap两黑叶、腰带后bow和apron黑裙依本source。',
  'extent': '800x992完整原963 guide，真实母963不同首曝光962；头、两高手、交叉袖、腰、后bow和下apron/黑裙原底裁同共同构图，不加未见腿鞋、不沿37尺寸伸短身体。',
  'motion': '已实际看R104全图，低耳颈卷比R100更朝下展开/回收，灰带下端靠白frill；只用相位文字，不输入AIbody/微笑/小卷实体。压紧与展开是次运动，不因头发ROI小就缩固有发量，末端自然被肩褶遮挡不强拉到交叉前袖前。',
  'repair': '用户明确母963卷形错误重开current '
            'repair_required；旧PRIMARY和Sol88当时retained/无P1，不能篡改旧审。当前珠下灰前面与mint斜弧交替成近封闭渐尖体，入口→内后返回接下一圈读法仍不足；下灰钩较钝且与白frill相接。下端是封口还是被frill遮挡不能只凭零洞认证，隐藏C不补想象；gray软变化和R104相位原P2仍待fresh看。低LEFT根/现源体型与手势可保，不拿当前完整头卷作正确几何母参。',
  'hypothesis': '换完整未挖头963 '
                'source-first而非旧38整头edit锚；correct11整头给OC灰短bob/低根及合理体量，latestgraydetail提供宽灰实际前返/渐细C，key仅同灰无光，本源眼口为第五张。测试移除封闭渐尖几何竞争，不保证成功；本态更下收的相位及原肩frill遮挡都保留，不强露整尾。',
  'specific_prompt': '同一宽GRAY发带从低双珠下翻成前面，再向内/后返回接下圈；上中下连成连续绕行，不是灰椭圆盖盘加一串薄荷封口盘。本态卷更朝颈肩下收，宽gray返回仍不透明，不删成洞、不全mint；渐细C可被原白frill真实挡住，不能为了露C抬根或拉到袖前。保本源单弧闭笑和不对称圆睁眼，前斜掌/后竖掌分叉指扇及各袖口不能借37。',
  'neighbor': 'actual962/965同属963源态的首末曝光，不能用首962代母963/PTS514112；前956..961双掌近并更竖，后966..969拆成高低掌。本态须保自己双手、倾头和底裁，非动态验收。'},
 {'id': 'ART-G12-39',
  'source': 966,
  'pts': 515712,
  'first': [966, 969],
  'first_pts': [515712, 517856],
  'run': 'whole_imggen_source966_connectedgray_occlusion_v02',
  'selected_sha': 'b95b9e21a92e3769fbb5d73d91565d2d358cd26435b72c3f9adbdb9e9525cd16',
  'first_API_sha': '135684d23039206f133de2d76ae8d9d33f8e583ad90ffde5ec5db731bab3a8b8',
  'fifth_crop': [254, 246, 444, 394],
  'fifth_name': 'ref5_ORIGINAL966_OWN_UNEQUAL_OPEN_EYES_ARC_CLOSED_SMILE.png',
  'fifth_role': '只本966圆睁但不对称的睫弧/视线与单弧小闭笑，不沿身份模板/G02半睑或37双弧口，不贴入艺术像素。',
  'evidence_frames': [966, 969],
  'root_projection': '本966更近正面、头倾画左，唯一人物LEFT根仍在画右同侧低耳后/bob-nape，不能接眼侧高根或换到画左近耳。bob与白肩褶可自然挡住部分低珠/后段，不能为露全珠抬根，不镜像头身/高低掌。',
  'action': '原966头倾画左、不对称圆睁眼，单弧小闭笑。两臂已分开：画左低摊掌朝前、拇指上立，原不规则三段外分指轮廓/掌纹保留；画右高竖掌侧斜向上，长并指与拇指边、白袖口折线和臂肘角分别照原。不是37/38胸前交叉双高手，也不自动改成对称摊手。红bow金扣此态完整露出，白肩fan与竖frill/袖口、black长袖黑领、白cap两黑叶、腰带后bow与apron黑裙可见段听966。',
  'extent': '880x976完整原966 guide保头身/高低两掌/腰与下apron共同比例和原底裁；本源没有腿鞋，不补隐藏下肢或改成前全身舞步，不为卷尾拉躯干移腰/手。',
  'motion': '已实际看R107全图，低颈侧卷朝下伸展，比R100压紧段更明显、接近肩frill后回收；这里只用hair相位文字，不送AIbody/眼口或实体螺纹卷。发量依完整头肩/正确11，不把露出长短误作固有大小或固定圈轴；自然肩褶遮挡仍保。',
  'repair': '用户明确母966钻发形态错误使current repair_required；旧PRIMARY/Sol92 '
            'retained当时没有P1，保留其历史。当前珠下灰椭圆面与mint斜弧构成压紧柱形，上段前面→内后返回→下圈连接需更明确，而非独立封口盖/实心芯贴螺线。下段真实被白肩frill挡住，不能据零孔判实心或伪认证隐藏根/完整C；softgray/mint和R107相位旧P2待新实看。低LEFT根、高低两掌与本源表演可保，当前整头不作为正确卷几何锚。',
  'hypothesis': '由完整未挖头966 '
                'source-first统一重画可见人物，排除旧39封闭斜弧整头，不借37/38动作或当前body比例。correct11只OC灰短bob低根/相对体量，latestgraydetail只宽灰前内后返回，key定同灰，本源眼口第五张防表演漂移。这是移除旧几何竞争的待验假设，不宣称内部原因已证实；保更下伸相位及原肩褶遮挡，不强拉完整C到前面。',
  'specific_prompt': '珠下起卷必须同一宽GRAY发带前面翻回内后并实际连接下一圈，不独立灰帽片盖在实心螺纹柱上。上中下宽gray前返连续渐细到C方向，真正可见空隙才透明，opaquegray返回不能挖掉。本态向下伸后在白肩frill后自然遮挡，不强露全C/全珠；保整头肩合理体量，避免巨粗或微型绿挂件。图5只966不对称睁眼与单弧闭笑，两掌一低一高、红bow完整露出全听图1。',
  'neighbor': 'actual966/969同一个PRIORITY源态；前962..965胸前交叉双高手在本态已拆成画左低摊掌/画右高竖掌。只核本母966与首末曝光，不扩其他项、不机械新增曝光item或假认证动态。'}]

for row in rows:
    id=row['id'];C=B/'drawings'/id/'v01';R=C/row['run'];selected=registry[id];old=Path(selected['selected_run'])
    jobp=C/'JOB.json';regp=C/'REGISTRATION_PLAN.json';job=read(jobp);state=next(x for x in states if x['id']==id)
    assert job['source_frame']==state['existing_source_canonical_frame']==row['source'] and job['source_pts']==row['pts']
    assert [state['first_frame'],state['last_frame']]==row['first']
    assert [state['first_pts'],state['end_pts']]==row['first_pts']
    assert selected['status']=='repair_required' and selected['sha256']==row['selected_sha'] and sha(selected['image'])==row['selected_sha']
    first_raw=C/'character_api_original.png';receipt=C/'result.json';assert sha(first_raw)==row['first_API_sha']==read(receipt)['output_sha256']
    assert not (R/'character_imggen_original.png').exists() and not (R/'BUILTIN_GENERATION.json').exists()
    source=Path(job['source_image']);guide=C/'inputs/source_pose_guide.png'
    assert sha(source)==job['source_image_sha256']
    refs=[]
    def cp(name,p,role,xy=None):
        out=R/'inputs'/name;assert not out.exists()
        if xy is None:shutil.copyfile(p,out)
        else:
            with Image.open(p) as im:im.crop(xy).save(out)
        item={**rec(out),'source':rec(p),'role':role}
        if xy is not None:item['source_crop_xyxy']=xy
        refs.append(item)
    cp(f"ref1_ORIGINAL{row['source']}_COMPLETE_UNMASKED_POSE_GUIDE.png",guide,'唯一原PV当前动作、共同头身构图、眼口、不同手臂掌/衣腰与实际可见apron黑裙和真实底裁，不补隐藏腿鞋。全guide不挖头不移部位；红角色/尖长额发/双高卷不作为本OC身份。')
    cp('ref2_USER_CORRECT11_GRAY_BOB_COMPLETE_HEAD_COIL_VOLUME_CONTEXT.png',identity,'OC中性灰短圆润bob/自然灰刘海贴颊侧发及唯一低LEFT双珠身份；完整头卷仅合理相对发量与宽灰前返/渐细C，不复制原眼口/头姿/手body或固定卷轴。')
    cp('ref3_LATEST_USER_BROAD_GRAY_FRONT_RETURN_DETAIL_NO_FACE_ROOT.png',detail,'仅宽GRAY主面/内后返回实际连接/渐细C，薄mutedmint材料带。舍原精修高光暗体积面，不定本root/孤立大小/轴向。',[35,58,146,260])
    assert refs[2]['sha256']=='0b88fd6ba273c659797b709b7a967005f6cf3a2bed0878bd2b7fecd5bb9a97a7'
    cp('ref4_PURE_UNLIT_GRAY_MINT_KEY.png',palette,'所有bob与灰发带前内背返回统一同gray平涂，mint独立材料条；不作方向打光/体积构造。')
    fifth_source=old/'qa_white.png' if id=='ART-G33-07' else guide
    cp(row['fifth_name'],fifth_source,row['fifth_role'],row['fifth_crop'])
    assert len(refs)==5
    source_prov=H/'cels'/id.removeprefix('ART-')/'PROVENANCE.json'
    assert read(source_prov)['source_frame']==row['source'] and read(source_prov)['source_pts']==row['pts']
    locals_before=[]
    for p in C.glob('*/LOCAL_REPAIR_STATUS.json'):
        snapname='ANCESTOR_BEFORE_'+p.parent.name+'.json'
        locals_before.append({'status_file':rec(p),'status_exact_before':read(p),'private_copy':put(R,snapname,read(p))})
    local_parent=C/'local_hollow_return_gray_api_v01' if id=='ART-G33-07' else None
    evidence_paths=[source,guide,old/'qa_white.png',old/'qa_black.png']
    frame_nums=row['evidence_frames']
    evidence_paths += [B/'coverage/source_frames'/f'F{n:06d}.png' for n in frame_nums]
    motion_path=Path(state['motion_reference_path']);evidence_paths.append(motion_path)
    prov={
        'id':id,'created_utc':now,'refs':refs,'source_full':rec(source),'source_guide':rec(guide),
        'JOB':rec(jobp),'REGISTRATION_PLAN':rec(regp),'source_PROVENANCE':rec(source_prov),
        'canonical_source_frame':row['source'],'canonical_pts':row['pts'],'source_time_base':'1/16000',
        'first_frames':row['first'],'first_pts':row['first_pts'],'PRIORITY_SCOPE':rec(scope_path),'priority_exact_row':state,
        'selected_registry_exact_snapshot':selected,'selected_image':rec(selected['image']),
        'current_PRIMARY':rec(selected['primary_review']),'current_independent_report':rec(selected['independent_review']),
        'user_correction_policy':rec(policy),'assessment_requirements':rec(requirements),
        'saved_first_API':rec(first_raw),'known_first_API_receipt':rec(receipt),'known_API_elapsed_seconds':read(receipt)['elapsed_seconds'],
        'local_ancestors_before':locals_before,'direct_historical_local_repair_parent':str(local_parent) if local_parent else None,
        'actual_read_only_source_selected_neighbor_motion_paths':[rec(p) for p in evidence_paths],
        'source_action':row['action'],'visible_extent':row['extent'],'phase_observation_text_only':row['motion'],
        'source_neighbors_and_no_duplicate_item':row['neighbor'],'repair_reason':row['repair'],'changed_reference_hypothesis':row['hypothesis'],
        'source_original_JOB_REGPLAN_and_policies_not_modified':True,'new_art_pixels_created_or_patched':False,
    }
    put(R,'INPUT_PROVENANCE_AND_REPAIR_CONTEXT.json',prov)
    put(R,'CURRENT_SELECTED_STATUS_SNAPSHOT.json',{'registry_exact_entry':selected,'PRIMARY_exact':read(selected['primary_review']),'snapshot_only_no_central_write':True,'legacy_review_is_not_current_user_acceptance':True})
    prompt='\n\n'.join([
        prefix,
        '人物身份采用图2中性灰短圆润bob女孩：自然灰刘海、贴颊短侧发、唯一人物LEFT低耳后双红珠。图1红发角色/尖长额发侧刺和双高卷不是目标，不只是改色；图1只拥有本帧头身动作、眼口、手衣和实际可见下apron与原裁切，图2不得改本动作/眼口。',
        f"这是已有API保存稿{id}的一次完整当前可见人物连贯重绘修复；图1原{row['source']}完整source-first构图为动作唯一依据。"+row['action'],
        row['root_projection']+' bob、低根红珠、颈领、cap和肩褶自然衔接，实际遮挡可隐部分根，不能为露全珠或尾尖抬根/拉卷到前臂前。',
        row['specific_prompt']+' 图2整头与肩部上下文核相对体量：不巨粗、不小挂件，也不以孤立局部crop尺寸定发量。图3只宽灰返回连接，不复制高光/暗底。不要固定洞数/圈数/全片轴长，也不能把不透明灰返回面一律挖成洞；真正露出的空气才透明。',
        row['motion'],
        '所有gray短bob与卷的正面/内面/背面/返回都同一无打光灰#B6B4B2，较薄mutedmint#B0C8BA只材料带，墨线#171717；用线与互遮表达绕行，不画重复深灰体积内底/银白亮边/渐变。暖桃肤、原黑白女仆衣/红bow金扣、白cap与两主要黑叶保持，普通小共同帽根不另长第三垂叶。眼睛一种charcoal实色iris+普通小圆白点，开度/视线仅本source，禁止G02半睑模板/黑中心灰环。',
        row['extent']+' 整个人物一次重新画连贯，不局部贴辫子/贴眼/拼衣或代码补底。只输出真实透明可见人物，无粉色背景、字幕、棋盘格、色表或独立物件。'
    ])+'\n'
    prompt_path=R/'prompt_imggen.txt';assert not prompt_path.exists();prompt_path.write_text(prompt,encoding='utf-8')
    request={
        'id':id,'run':str(R),'operation_kind':'whole_character_redraw','existing_saved_API_repair_not_new_FIRST':True,
        'source_first':True,'refs':[x['path'] for x in refs],'reference_sha256':[x['sha256'] for x in refs],
        'prompt_file':str(prompt_path),'prompt_sha256':sha(prompt_path),'prompt':prompt,
        'tool_arguments':{'prompt':prompt,'referenced_image_paths':[x['path'] for x in refs],'transparent_background':True},
        'transparent_background':True,'whole_character_one_generation':True,'source_frame':row['source'],'source_pts':row['pts'],
        'first_case_frames':row['first'],'source_canvas_guidance':job['output_size'],
        'rejected_current_image':rec(selected['image']),'repair_reason':row['repair'],'changed_reference_hypothesis':row['hypothesis'],
        'local_repair_parent':str(local_parent) if local_parent else None,
        'historical_local_ancestors_whole_done_not_fresh_pass':bool(local_parent),
        'mandatory_whole_redraw_after_local_repair':bool(local_parent),'whole_character_imggen_completed_for_this_request':False,
        'fresh_root_Sol_and_placement_required':True,'user_quality_preference':'high','native_quality_parameter_exposed':False,'native_model_parameter_exposed':False,
        'submitted':False,'PREPONLY':True,'dispatchable_by_artist':False,'native_calls_authorized_this_record':0,
        'planned_native_n_on_future_root_release':1,'API_calls':0,'native_calls':0,'automatic_retries':0,
        'whole_image_not_a_patch':True,'user_accepted':False,'dynamic_validated':False,
    }
    request_record=put(R,'request_imggen.json',request)
    put(R,'LOCAL_ANCESTRY_BEFORE_AND_FRESH_WHOLE_PENDING.json',{
        'id':id,'historical_local_parent':str(local_parent) if local_parent else None,'ancestor_before':locals_before,
        'no_new_local_patch_this_turn':True,'mandatory_visible_whole_requested':True,
        'historical_whole_completion_not_inherited_for_this_candidate':True,'new_whole_completed':False,
        'fresh_review_pending_after_future_whole_return':True,'eligible_for_final_selection':False,
        'no_parent_status_modified':True,'API_calls':0,'native_calls':0,
    })
    print(json.dumps({'id':id,'request':request_record,'prompt':rec(prompt_path),'refs':[{k:x[k] for k in ['path','sha256','size']} for x in refs],'calls':0},ensure_ascii=False))
