from pathlib import Path
import pprint
import hashlib

R = Path(__file__).resolve().parent
B = R.parents[3]
template = B/'drawings/ART-G12-66/v01/prep_first_api_source1107_graybob_sourcepalms_v01'

common_root = (
    '唯一人物LEFT低耳后/nape双红珠根，当前正面投影在画右同侧bob下；低头时根随耳后/后颈一起倾转下降，'
    '不能沿用站直时的屏幕高度、抬到太阳穴/帽边，不能加画左近耳双珠或镜像身体。'
    '保从前63–66转正后同侧肩前/胸侧的自然路线，当前肩手/bob实际遮住才遮局部，'
    '不能无原因把整束转到背后或为躲根侧错误缩成小挂件，也不强拉尾尖穿到手臂前。'
    '前后新稿尚未逐曝光核实，本次只记录待核连续性意图，不宣称动态或家族通过。'
)

rows = [
    {
        'id':'ART-G12-68','source':1120,'pts':597936,
        'first':[1118,1122],'first_pts':[596864,599536],
        'size':'1280x944','motion':229,'motion_roi':[533,237,565,261],
        'eyes_roi':[530,224,748,350],
        'run':'prep_first_api_source1120_graybob_ownpalms_v01',
        'source_sha':'85cf798a573a8ac9448708eaa2947e2425b6c2fe50a126edea99ab43cd920963',
        'action':(
            '原1120头仍较直、圆睁眼、短浅弧闭笑。两臂外伸、两腕已转为近竖向外掌：'
            '画左长指并拢斜上偏左、掌根接较高白袖口；画右长指并拢斜上偏右、腕与掌更低且线角不同。'
            '保原拇指与指间线、两腕袖口/弯肘高低差，不沿66横向掌心朝上或借AI手势。'
            '当前黑长袖/红领结金扣、两肩白fan及竖褶、白袖口、腰带折角、画右腰后bow和围裙到画底全部按1120。'
        ),
        'canvas':(
            '完整1280x944未挖头原guide；头、cap两黑叶、不同竖掌和腰裙均保原共同坐标。'
            '原source为半身，apron/黑裙在1080底边被切断，guide对应底裁保留，不加隐藏腿鞋，'
            '不把原底裙缩短留白。无新trim/单部位挪移。'
        ),
        'difference':(
            '68不同于66：双腕由横摊转成近竖外掌、长指斜上且并拢；左掌更高、右袖口更低，'
            '头/腰/肩褶和红bow描线也不同。first1118与canonical1120同状态曝光来源均实际核，母帧不是1118。'
            '不得用G33-63全身构图替代当前半身源。'
        ),
        'motion_observation':(
            'actual R229全图卷下段在肩侧比前状态有更长下伸/回弹读法，尾邻白frill，自身构造仍非母参。'
            'purehair[533,237,565,261]32x24仅灰发段，排脸眼、红珠/root和白肩饰。'
            '只给局部回弹/压缩相位；不能用小ROI证明隐藏长度或缩小固有发量，不复制AI竖掌/头脸。'
        ),
        'source_expression':(
            '本1120双眼圆睁、左右睫弧/虹膜露出不对称，短浅弧闭笑。图1/5唯一开度和口形，'
            '不能套69/70半睑、图3中性小口或AI眼形。'
        ),
        'root_continuity':common_root+(
            '本帧仍较直，按源原卷及R229读到的回弹转译到同一低LEFT卷；'
            '卷可在自然肩侧伸展，不能为完整露尾换根或冻结成前66压紧小柱。'
        ),
    },
    {
        'id':'ART-G12-69','source':1123,'pts':599536,
        'first':[1123,1128],'first_pts':[599536,602736],
        'size':'1360x848','motion':234,'motion_roi':[529,291,557,312],
        'eyes_roi':[560,284,766,398],
        'run':'prep_first_api_source1123_graybob_ownpalms_v01',
        'source_sha':'bfc47ddf1466f342a481372e32c2fbe7ee63fc976efccbb25b591a50b5febe79',
        'action':(
            '原1123向前鞠躬低头，头顶/cap前后层次可见，半睑向下视线、短小闭弧笑。'
            '两肘下沉且双前臂近水平伸向两侧；画左指尖斜左上并拢、拇指独立向左下分开，'
            '画右长指较平斜右上、拇指在下侧分出。两手在腰旁外侧，不是68近竖掌或合十。'
            '当前肩白褶、black长袖、两种白袖口线、红bow金扣、腰带/后bow/底apron原形全部保1123。'
        ),
        'canvas':(
            '完整1360x848未挖头guide，低头、双手、颈肩腰和下围裙保持当前共同坐标；'
            'source1080本就只半身/apron下端切出，不能补腿鞋、把身体立直或拉长躯干去凑前帧头高。'
            '无新trim或单部位移动，较矮画布来自当前源裁框，不代表任意压扁人物。'
        ),
        'difference':(
            '69首次1123恰是canonical1123；由68直头圆睁/高竖掌转为俯头半睑/两低外手，'
            '并可见更多头顶而下巴收近领口。图3站直全头只身份/体量，不能把头扶正、眼撑圆或掌抬回。'
            '两手原拇指分叉、袖口斜线与70的再次重画不同。'
        ),
        'motion_observation':(
            'actual R234全图随俯头，卷在同侧肩颈下降/紧收，局部灰带斜向回折；AI半睑也不能拥有本source开度。'
            'purehair[529,291,557,312]28x21排眼脸、珠/root、白frill，仅局部弹性相位。'
            '不由这段裁图推整卷长度/固定轴或微缩固有发量，不复制AI头身/手腕。'
        ),
        'source_expression':(
            '本1123双眼半睑、上睑较平且左右不对称，露出压低的charcoal虹膜，视线向下，'
            '短小弧闭笑。半睑是此原PV本态真实表演，不是G02模板；图1/5控制，不能复制图3圆睁。'
        ),
        'root_continuity':common_root+(
            '本态俯头投影会改变卷根与bob/肩的遮挡；允许根段部分藏在同侧bob/nape，'
            '保持完整发量读法与自然肩前路线，不把source高红双卷的上举根当新低root。'
        ),
    },
    {
        'id':'ART-G12-70','source':1129,'pts':602736,
        'first':[1129,1133],'first_pts':[602736,605248],
        'size':'1360x800','motion':238,'motion_roi':[528,329,555,352],
        'eyes_roi':[570,295,785,404],
        'run':'prep_first_api_source1129_graybob_ownpalms_v01',
        'source_sha':'ab2ddffc164b2db86f6dcaa047ee02a58256ab6f33495f2aba012c8713140d75',
        'action':(
            '原1129头/肩进一步俯低，冠顶与cap前缘可见，半睑下视、极小闭弧笑。'
            '双肘仍下沉、两臂低向外伸；画左并拢指尖斜左上，拇指呈清楚弯钩向左下，'
            '画右长指斜右上较低、下侧拇指分出，掌根/指间线与69再重画。'
            '画左袖口下缘弯折、画右袖口接近竖边且掌腕更低，肩褶/红bow金扣/腰后带和原半身底裙独占1129。'
        ),
        'canvas':(
            '完整1360x800未挖头原guide，仍是原1129共同构图，双手所有可见指端和apron黑裙底裁保留。'
            '不能复制69的头高/手腕或借图3直立头，不能补隐藏腿鞋/缩人留底。无新增trim或单部位变形。'
            '首段末曝光1129..1133在scope endPTS605248结束，原状态endPTS605408仅历史，不能越过10秒边界。'
        ),
        'difference':(
            '70不同69：俯头/肩更低、cap和头顶透视略变，眼虹膜与睑弧重新描绘；'
            '画左拇指更弯、掌边与右侧分指/两袖口线也不是69重复。输出1360x800而69为1360x848，'
            '依各自真实source裁框保比例，不能把69机械压扁成70。'
        ),
        'motion_observation':(
            'actual R238全图卷随更低俯头下移，末段在肩侧伸展/回收而非站直冻结；'
            'purehair[528,329,555,352]27x23排眼脸、珠/root和白frill，仅局部灰带相位。'
            '小ROI不能定整卷固有大小/隐藏圈或把回弹缩成装饰，不复制AI半睑/双手/较圆笑口。'
        ),
        'source_expression':(
            '本1129半睑仍睁开、目光向下，左右眼弧和iris露出按本帧，极小弧闭笑；'
            '不可变闭眼或图3圆睁，不复制69像素眼口或G02半睑bitmap。图1/5唯一表演。'
        ),
        'root_continuity':common_root+(
            '本态是俯头收尾相位，低LEFT根仍随本耳后/nape低下，回折和C可随弹性变化、自然遮挡，'
            '但不许冻结同69整卷或把整束改成实心柱/封口盘。'
        ),
    },
]

src = (template/'prepare_pair_PREPONLY.py').read_text(encoding='utf-8')
start = src.index('rows = [')
end = src.index('\ndef find_catalog', start)
src = src[:start]+'rows = '+pprint.pformat(rows, width=120, sort_dicts=False)+'\n'+src[end:]
src = src.replace("for id in ['ART-G12-63', 'ART-G12-64', 'ART-G12-65']:",
                  "for id in ['ART-G12-63', 'ART-G12-64', 'ART-G12-65', 'ART-G12-66', 'ART-G33-63']:")
start = src.index('    continuity = (')
end = src.index('\n    prompt = ', start)
src = src[:start]+"    continuity = row['root_continuity']"+src[end:]
dest = R/'prepare_last3_requests_PREPONLY.py'
assert not dest.exists()
dest.write_text(src, encoding='utf-8')

src = (template/'finalize_pair_PREPONLY.py').read_text(encoding='utf-8')
start = src.index('runs = [')
end = src.index('\nauth = ', start)
run_paths = [str(B/'drawings'/row['id']/'v01'/row['run']) for row in rows]
src = src[:start]+'runs = [Path(p) for p in '+repr(run_paths)+']\n'+src[end:]
src = src.replace("'predecessor_current_images_not_yet_available_no_dynamic_pass': True,",
                  "'predecessor_current_images_not_verified_for_this_turn_no_dynamic_pass': True,")
src = src.replace("'PREPONLY G12-66 and G33-63; verify actual canonical/first PTS/current status and source action; do not duplicate known candidate. Fresh private missing-first preparation only. Actual own full source and eye/mouth/hands plus all6 refs. high/transparent/n1/retry0/formal8/lock/Preview only. Explicit gray short bob identity, fixed anatomical LEFT low nape root, 63-65 turn/front-shoulder continuity pending actual preceding states. No API/imggen/network/attempt/execution/central/JOB/REG/63-65 lock changes, do not expand another item.'",
                  "'PREPONLY last3 ART-G12-68/69/70 only. Verify actual canonical/first PTS/status. Fresh private directories only, source-specific eyes/mouth and different palm phases. Actual original full source and exact6refs. Explicit gray short rounded bob identity, anatomical LEFT low nape beads following current bow, natural front-shoulder route/rebound/occlusion, wide gray connected front/returns/taper C and relative head volume, uniformly unlit bob/coil. high transparent n1 retry0 formal8 immutable lock and Preview only. No API/native/HTTP/execution/attempt/central/JOB/REG or existing63..66/G33-63 changes; do not expand range.'")
dest2 = R/'finalize_last3_PREPONLY.py'
assert not dest2.exists()
dest2.write_text(src, encoding='utf-8')

log = R/'READONLY_TEMPLATE_DERIVATION.txt'
assert not log.exists()
log.write_text(
    'Private helpers derived from read-only prior pair preparation code; no old helper executed or modified.\n'
    +str(template/'prepare_pair_PREPONLY.py')+' SHA256 '+hashlib.sha256((template/'prepare_pair_PREPONLY.py').read_bytes()).hexdigest()+'\n'
    +str(template/'finalize_pair_PREPONLY.py')+' SHA256 '+hashlib.sha256((template/'finalize_pair_PREPONLY.py').read_bytes()).hexdigest()+'\n'
    +'Rows/source-specific actions/own eye state/root bow projection/current allowed IDs and PARENT scope replaced for68/69/70.\n',encoding='utf-8')
print(dest)
print(dest2)
