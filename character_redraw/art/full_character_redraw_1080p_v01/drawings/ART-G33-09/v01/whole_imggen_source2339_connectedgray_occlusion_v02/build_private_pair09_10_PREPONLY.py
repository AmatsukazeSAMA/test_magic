from pathlib import Path
import pprint
import hashlib

R=Path(__file__).resolve().parent
B=R.parents[3]
template=B/'drawings/ART-G33-07/v01/whole_imggen_source2333_upperreturn_lowerC_v13/prepare_sourcefirst_pair_PREPONLY.py'
rows=[
    {
        'id':'ART-G33-09','source':2339,'pts':1248720,'first':[867,870],'first_pts':[462864,464992],
        'run':'whole_imggen_source2339_connectedgray_occlusion_v02',
        'selected_sha':'a425cc873b2a8ce69707a3b7fff7ab8a75ad1c5245b2ef05f51adfc2201ce1fc',
        'first_API_sha':'2d576fc092c80d5ba70508b983fd6bb06d96f16eabb91135d08c5405330c2c7a',
        'fifth_crop':[134,154,269,242],
        'fifth_name':'ref5_ORIGINAL2339_OWN_OPEN_EYES_TINY_NEUTRAL_MOUTH.png',
        'fifth_role':'仅本2339圆睁不对称眼弧/虹膜露出、视线及极小中性闭口。不是G02半睑模板，不贴艺术像素，不借身份图或AI小笑。',
        'evidence_frames':[866,867,870,871],
        'action':(
            '原2339头近正面略侧倾，双眼圆睁且左右睫弧/视线略不对称，极小中性短闭口，不加笑。'
            '画左臂向腰后弯折、手真实被身体挡住，不凭空补出；另一长臂从画右肩斜向右下伸出，'
            '低摊掌朝前外、独立拇指指向右上，四分指向右下，保原不规则指形/掌纹与白袖口斜角。'
            '不是前08近竖下掌，也不是下一10高伸臂折腕垂指。'
            '原black长袖/白肩fan和竖褶/白袖口、红bow金扣、腰带与后bow、长apron锯齿边黑裙、'
            '交错前腿/屈膝抬后腿及踝带鞋的原可见段保留，不拉直站姿。'
        ),
        'extent':(
            'canonical2339原前景鞋尖贴1080底边截断，后抬鞋可见；624x1072完整guide保原共同构图与底裁，'
            '不沿当前native补圆完整toe，也不缩人/上移以露全原未见鞋端。'
            'first867..870是放大半身曝光，不能拿其未露脚豁免canonical原见裙腿，摄影定位另审。'
        ),
        'motion':(
            '已实际看R28全帧：低耳颈侧卷仍向肩侧下收、局部紧压回弹，白frill遮住下端；'
            '只有发丝次运动文字，不输入AI小实体卷/完整头眼/低臂身体位图。'
            '小可见段和自然遮挡不能定义固有发量变小，不能复制AI微笑或沿08旧外展固定轴。'
        ),
        'repair':(
            'current registry repair_required来自用户明确点名母2339钻发形态错误；PRIMARY与Sol95当时为retained，'
            '没有把其旧issues空列表篡改成Sol当时已判P1。用户后来否决覆盖旧静态保留。'
            '当前可见上端灰椭圆盖面接数片宽mint闭合弧带，宽灰前→内后返回的入口/出口仍不清，'
            '下端被白肩饰遮住，隐藏拓扑不可认证，也不能单凭没有洞判实心。'
            '低LEFT根、源眼口手body有可保范围；softgray/mint材料与投影原为P2，后续fresh实看，不能伪当已满足当前无打光要求。'
        ),
        'hypothesis':(
            '改用完整未挖头2339 guide独占所有表演和比例，完全排除当前09整头/闭合卷与旧08/09低根head模板。'
            '用用户正确11完整head-coil上下文给OC中性灰bob和合理整头体量，最新graydetail只给宽灰连续前/返回，'
            'unlitkey给同灰材料，本source眼口第5张防身份/AI改表演。'
            '检验拿掉旧闭合弧带几何竞争的source-first假设，非已证实内部原因；保实际肩frill遮挡，不强拉全C。'
        ),
        'specific_prompt':(
            '低LEFT双红珠下是同一条宽GRAY发带：上端灰前面翻向内/后、实际接回下一圈，不能独立椭圆盖片接一串封闭薄荷盘。'
            '沿本态颈肩回收时仍有宽灰主面和返回，不是只有一条薄荷装饰绕实心体。'
            '逐圈渐细C可部分被原白肩frill真实挡住，遮挡不是缩小发量，也不能为了证明结构硬拉整尾到肩褶前。'
            '图5只本源眼口，严守源圆睁/极小中性闭口、低斜摊掌与腰后隐藏手。'
        ),
        'neighbor':(
            'actual866前08仍近竖下垂臂，867/870本2339改成斜向右下外伸摊掌；'
            'actual871后10将该臂抬高、手腕折下，不能把后态手套给09。'
            'first867..870属一个PRIORITY状态，其首末PNG有微小RGB差异，不自动逐像素alias，也不机械新增人物项；'
            '本source与first放大构图只用于当前源态，非曝光定位或动态认证。'
        ),
    },
    {
        'id':'ART-G33-10','source':2342,'pts':1250320,'first':[871,873],'first_pts':[464992,466608],
        'run':'whole_imggen_source2342_connectedgray_sleeveocclusion_v02',
        'selected_sha':'07c70b582c6b4401dc84d8b85dc6c1483dad2fdf7d0e692e7ab35462a462863d',
        'first_API_sha':'54cb01abe717c8df495248aa8965f51d5b59b9d1c8999bfa45d7c45ab79acc28',
        'fifth_crop':[119,132,244,215],
        'fifth_name':'ref5_ORIGINAL2342_OWN_OPEN_EYES_TINY_NEUTRAL_MOUTH.png',
        'fifth_role':'仅本2342原圆睁不对称眼开度/iris露出、视线及tiny中性闭口。不可抄AI小笑/身份图表情，不送G02半睑图，不贴艺术像素。',
        'evidence_frames':[870,871,873,874],
        'action':(
            '原2342头近正面略向画左倾，双眼圆睁、视线和两侧眼弧不对称，tiny中性短闭口。'
            '画右长臂高斜外伸、白袖口接折腕，原拇指向上、指尖水平/垂下的风格化轮廓分别保留，'
            '不是09低斜摊掌，也不是后874向上摊开的高掌。画左肘折回、手真实藏在腰后，不补隐藏手。'
            '高臂black袖下原本有锯齿轮廓，按source齿深/齿尖画，既不误当新破洞抹平，也不沿当前旧稿进一步夸大。'
            '原black领/长裙长袖、红bow金扣、白肩frill竖带/袖口、腰带后bow和apron、交错弯腿/后抬鞋均按2342。'
        ),
        'extent':(
            '完整624x1056原guide而非09的624x1072，头/高折腕手/腰/长apron/黑裙/双腿鞋共同比例保持。'
            'canonical2342前鞋尖在1080边界贴底截断，后抬鞋可见；不沿当前native完整额外toe认作源已见几何，'
            '不能缩人抬人去露未见鞋尖。first871..873放大半身的摄影另审，不裁掉canonical原见裙腿或假称已绑定。'
        ),
        'motion':(
            '已实际看R31全帧：低颈侧卷更压紧，随高袖/肩frill自然遮挡，只见少量回折灰发带；'
            '不发送AI完整头身/微笑和卷bitmap，仅相位文字。'
            '自然挡住不等于可以画成实心盖盘/微型挂件，也不强制拉出隐藏尖C或把根抬到上耳。'
        ),
        'repair':(
            'current registry repair_required由用户明确点名母2342钻发形态错误覆盖旧PRIMARY/Sol103 retained。'
            'Sol103当时没有可见结构P1，只保留softgray/mint色阶/相位等P2，不能伪说其当时已否决。'
            '本轮实际可见珠下上端仍似独立灰椭圆盖面与几片mint弧带，前面→内后返回路径需重建；'
            '后续被白肩frill/高black袖挡住，不认证隐藏完整卷/轴/C，也不能把真实遮挡当成必须露出整束。'
            '当前低LEFT根和主要源表演可保；原袖锯齿不是新服装破损，当前较深尖的袖廓应回依source。'
        ),
        'hypothesis':(
            '排除曾喂入的09完整头/压紧闭合卷模板，也不以当前10整头作保持锚；完整未挖头2342 guide独占本帧动作与布局。'
            'correct11完整头卷只本OC graybob/低根身份与整头相对体量，graydetail只连通宽灰前返，palette只无打光同灰，'
            '第五本源眼口防表演漂移。以不同参考假设重建当前可见起卷的真实连通，仍遵原高袖/肩frill遮挡，不靠堆洞词或强露全C。'
        ),
        'specific_prompt':(
            '低LEFT根双红珠下的起卷同一宽GRAY发带前面向内/后翻回进入下一圈，画清当前露出的连接，'
            '不是椭圆灰盖面后排一串封口mint片。该束在本态压紧于原肩frill和高black袖后，'
            '这些真实衣物遮挡继续不透明；被挡的整尾/C不强拉出来，也不挖空gray返回去强造洞。'
            '头肩上下文保固有发量，不巨粗、不微型。图5只本源眼口，高折腕手指/原袖齿深全听图1。'
        ),
        'neighbor':(
            'actual870前09是较低斜伸摊掌；871/873本2342抬臂到高位并折腕垂指；'
            'actual874下一态改为更高斜臂与向上摊掌，不能借下一态手或把09动作照搬。'
            'first871..873属同一个PRIORITY状态，首末图像即使微小RGB不同也不机械另造新item，不作整层像素alias/摄影通过。'
        ),
    },
]

src=template.read_text(encoding='utf-8')
start=src.index('rows=[');end=src.index('\nfor row in rows:',start)
src=src[:start]+'rows='+pprint.pformat(rows,width=120,sort_dicts=False)+'\n'+src[end:]
old="frame_nums=[860,861,862,863,866] if id=='ART-G33-07' else [861,862,863,866,867]"
assert old in src;src=src.replace(old,"frame_nums=row['evidence_frames']")
out=R/'prepare_sourcefirst_pair09_10_PREPONLY.py';assert not out.exists();out.write_text(src,encoding='utf-8')
record=R/'READONLY_TEMPLATE_DERIVATION.txt';assert not record.exists()
record.write_text('Read-only template: '+str(template)+'\nSHA256 '+hashlib.sha256(template.read_bytes()).hexdigest()+'\nOnly new09/10 rows and source-specific neighbor list substituted. No existing07/08 files modified or executed. No drawing/HTTP call.\n',encoding='utf-8')
print(out)
