"""Explicit visual curation of the reference's numbered demonstrations and source shots."""
from magic_maid_inspect import *

holds=json.loads((OUT/'data/reference_matches_initial.json').read_text('utf-8'))
byid={int(h['id'][1:]):h for h in holds}
timeline=json.loads((OUT/'data/original_timeline.json').read_text('utf-8'))
summary=json.loads((OUT/'data/original_summary.json').read_text('utf-8'))
metrics=json.loads((OUT/'data/original_metrics.json').read_text('utf-8'))

def tm(f):return timeline[f]['time_s'] if f<len(timeline) else summary['video_duration_s']
def span(a,b,exclude=()):return [i for i in range(a,b+1) if i not in exclude]

# A numbered reference panel is a composited state, not necessarily a new character cel.
# Repeated static runs caused by codec refreshes are explicitly removed below.
specs=[
 ('G01','抱膝：睁眼重描',[1,2],9,97,'人物','2个姿势相同的描线态；按原片曝光交替，不逐视频帧重画。'),
 ('G02','抱膝：闭眼过程',[4,5,6],97,170,'人物','1个半闭眼过渡，随后闭眼描线态；与G01接续。'),
 ('G03','横向花边字框',[9],170,257,'背景','参考片给出空框单帧；源片F170也可见空白框，后续内部换字另作文字层。'),
 ('G04','桌面衣装盒',[10,11],257,340,'道具/背景','两态桌面重描：盒、蝴蝶结、瓶罐、书；全景素材优先分开安排文字。'),
 ('G05','圆盘出现',span(13,17),340,422,'合成','5个编号含入场缩放和盘缘变化，不能直接计为5张独立人物稿。'),
 ('G06','倒悬远景与幽灵线',span(20,30),422,504,'人物/特效','11个合成参考，人物、圆盘与白色幽灵线分别核对；幽灵位置变化不增加人物张数。'),
 ('G07','倒悬近景与幽灵线',span(31,48,[47]),504,679,'人物/特效','编号1–17；原片多次重复，歌词与幽灵独立变化。H047是同一编号16的编码刷新拆分。'),
 ('G08','伸手触碰衣装盒',[49],679,751,'人物/道具','参考标单帧；长持帧时主要是镜头和歌词变化。'),
 ('G09','拿盒正面',[50],751,767,'人物','参考标单帧；后续散发拿盒是另一套头发/构图，不能直接替代。'),
 ('G10','手离开蝴蝶结',span(51,56),767,784,'人物/特效','编号1–6，手指动作与金色闪光分别做；H057与H056均为编号6。'),
 ('G11','变装前面部与橙色飞溅',span(60,68),784,818,'人物/特效','9个编号包括表情、头发与飞溅覆盖；橙色单独成层。'),
 ('G12','黑裙半身舞蹈',span(71,147,[109,139]),834,1175,'人物/特效','编号1–75。参考原文：这部分后面有全身动作。先对照G37全身版；编号含起始橙色揭幕，不相加宣称143张独立人物原画。'),
 ('G13','黑条歌词近景手势',span(150,179,[151]),1175,1328,'人物','编号1–29。参考原文：重复动作未计入。原片仍应保留重复的曝光，后段M25再次使用。'),
 ('G14','纵向花边字框',[183],1328,1404,'背景','空框单帧参考；H182/H183为同一素材的相邻静态段。后段钟表版另有背景布置。'),
 ('G15','坐桌喝茶',[184],1404,1489,'人物/道具','参考标单帧；人物、杯、壶、桌面和椅背可在制作时分层，当前文件仍是成片。'),
 ('G16','茶具俯视',[185],1489,1498,'道具','仅9个原片视频帧，约0.300秒；不能按参考片的展示停留长度使用。'),
 ('G17','拎篮全身定格',[186],1498,1542,'人物/道具','单帧姿势；人物与篮子接触需一起核对。'),
 ('G18','回望半身定格',[187],1542,1582,'人物','单帧姿势。'),
 ('G19','倒置法棍定格',[188],1582,1622,'人物/道具','单帧姿势；倒置构图和握持按源保留。'),
 ('G20','侧后站姿定格',[189],1622,1643,'人物','单帧姿势；与接下来的头肩近景分别保留。'),
 ('G21','黑裙回头近景',span(190,193),1643,1666,'人物','4个编号：背面两态、回头两态。'),
 ('G22','侧坐定格',[194],1666,1706,'人物','单帧姿势。'),
 ('G23','扫帚全身定格',[195],1706,1747,'人物/道具','单帧姿势，手与扫帚的接触点是主要描绘依据。'),
 ('G24','捧鸭定格',[196],1747,1786,'人物/道具','单帧姿势。'),
 ('G25','漂浮与鸭子定格',[197],1786,1821,'人物/道具','单帧姿势；整体斜放不等于逐帧翻滚重画。'),
 ('G26','睁眼黑色划线揭幕',span(198,201),1821,1852,'合成','4个编号主要是同一脸稿的黑色划线遮罩逐步撤开；遮罩不并入人物原画数。'),
 ('G27','床上房间全景',[204],1852,1908,'人物/背景','单帧参考；床、柜、枕头、画框、人物分别列作制作对象，黑字块与后期震动独立。'),
 ('G28','散发拿盒全身',[205],1976,2059,'人物','单帧参考；散发、灰衣、短裤与盒子。'),
 ('G29','散发拿盒近景',[206],2059,2153,'人物','单帧参考；可与G28做构图复用核对，不凭成片假定同一张高分辨率源图。'),
 ('G30','蝴蝶结与肖像胸针',span(207,216,[208]),2153,2221,'道具/特效','编号1–9，胸针高光/流动和蝴蝶结轮廓变化分开判断；H208是编号1的静态拆分。'),
 ('G31','蝴蝶结橙色放射转场',span(218,226),2221,2278,'特效/道具','9个编号含歌词和放射线。以已有蝴蝶结为底，单列放射特效。'),
 ('G32','三脸横向叠加',span(228,230),2278,2306,'合成','3个构图状态；分成三个头部姿态与复制/排版，不将每个合成阶段都画整个人物。'),
 ('G33','黑裙全身舞蹈',span(232,301,[256,292]),2306,2633,'人物','编号1–68；G12提醒对应的全身参考。转身、重心、鞋、裙摆与腰后蝴蝶结一并看。'),
 ('G34','房间站姿',[304],2633,2671,'人物/背景','参考标单帧；背景含椅、灯、画框和藤蔓。后续有淡出，不是新增姿势。'),
 ('G35','房间坐姿',[305],2671,2719,'人物/背景','参考标单帧；坐姿与椅子接触关系单独绘制。'),
 ('G36','房间侧向站姿',[306],2719,2801,'人物/背景','参考标单帧；人物与字块淡出仍属后期。'),
 ('G37','间奏倒悬：手扶腰',span(307,308),2959,3015,'人物','2个描线态；同一姿态交替。'),
 ('G38','间奏倒悬：手靠脸',span(309,310),3015,3053,'人物','2个描线态；沿原曝光复用。'),
 ('G39','间奏倒悬：单手外伸',span(311,312),3053,3094,'人物','2个描线态；画面保持倒置。'),
 ('G40','间奏倒悬：闭眼托脸',span(313,314),3094,3136,'人物','2个描线态；H315是编号2的编码刷新拆分。'),
 ('G41','间奏正向：双手举起',span(316,317),3136,3174,'人物','2个描线态。'),
 ('G42','间奏正向：手靠唇',span(318,319),3174,3214,'人物','2个描线态。'),
 ('G43','间奏正向：双手展开',span(320,321),3214,3254,'人物','2个描线态。'),
 ('G44','间奏正向：托腮',span(322,323),3254,3288,'人物','2个描线态。'),
 ('G45','漂浮面包篮',span(324,326),3288,3361,'人物/特效','3个合成参考，人物/面包篮与金色星芒分别核对。'),
 ('G46','大星芒遮场',span(329,331),3361,3373,'特效','3个编号，主体沿用G45；大星芒扩大到橙色满屏。'),
 ('G47','三格头像叠加',span(334,341),4280,4310,'合成','8个编号含头像姿态和格子数量变化；先画头部态，再做复制与排版。H342是编号8的静态拆分。'),
 ('G48','嘴部横条特写',span(345,350),4337,4355,'局部人物','6个嘴部/局部描线态；其余脸部被遮住，不能从这一段推算完整头部。'),
 ('G49','红裙回头落泪',span(353,358),4401,4431,'人物','6个编号：背面、转头、泪光。与黑裙G21动作相近，服装/领结/表情已有变化。'),
 ('G50','红裙托手眨眼',span(360,362),4511,4584,'人物','3个编号，眨眼与描线变化；花瓣独立。'),
 ('G51','红裙全身收束',span(363,382,[374]),4584,4763,'人物','编号1–19；末态长持，花瓣仍动。H374与H373同为编号11。'),
]

# Correct cross references use the stable group identifiers above.
specs=[(*s[:6],s[6].replace('G37全身版','G33全身版')) for s in specs]
groups=[];panels=[]
for gid,title,hids,lo,hi,kind,note in specs:
    g={'id':gid,'title':title,'hold_ids':[f'H{i:03d}' for i in hids],
       'reference_panel_count':len(hids),'source_search_range':[lo,hi],
       'kind':kind,'note':note,'count_unit':'numbered reference compositions; not unique character drawings'}
    groups.append(g)
    for number,hid in enumerate(hids,1):
        h=byid[hid]
        item={'id':f'{gid}-{number:02d}','group':gid,'title':title,
            'reference_number':number,'reference_hold_id':h['id'],
            'reference_frame':h['rep'],'reference_time_s':h['rep']/30,
            'reference_hold_start_frame':h['start_frame'],'reference_hold_end_frame_exclusive':h['end_frame_exclusive'],
            'source_search_range':[lo,hi],'source_frame':h['source_best_frame'],
            'source_time_s':h['source_best_s'],'initial_masked_rgb_mse':h['match_score'],
            'kind':kind,'note':note,'origin':'attachment_2_numbered_or_single_frame_reference',
            'status':'reference_panel; source_frame_candidate_pending_restricted_match',
            'unique_author_cel_claimed':False}
        panels.append(item)

# Reminder cards retain separate identities; they do not add drawings.
notes=[
 {'id':'N01','text':'连起来！循环','hold_id':'H003','frame':87,'meaning':'同一组作画按源片时序循环；参考片连播仅用于理解。'},
 {'id':'N02','text':'再来一次！','hold_id':'H008','frame':236,'meaning':'重复演示，新增作画数为0。'},
 {'id':'N03','text':'单帧素材','hold_id':'H009','frame':261,'meaning':'静态素材；镜头、透明度或内部文字可另动。'},
 {'id':'N04','text':'这部分后面有全身动作','hold_id':'H071','frame':2062,'meaning':'先核对G33全身参考与G12半身参考，再安排描绘复用。'},
 {'id':'N05','text':'重复动作未计入','hold_id':'H150','frame':4644,'meaning':'参考编号剔除了动作重复，原片曝光表仍需要把复现的时段记回。'},
 {'id':'N06','text':'1（单帧）','hold_id':'H185','frame':5773,'meaning':'参考展示停留不等于原片曝光；茶具俯视原片只持续约0.3秒。'},
]
for n in notes:n['reference_time_s']=n['frame']/30

chapter_specs=[
 (0,9,'粉色起拍','背景','开头9帧没有人物。'),
 (9,170,'抱膝与闭眼','G01 G02','先睁眼两态，再半闭眼过渡和闭眼描线态；歌词独立。'),
 (170,257,'横向花边字卡','G03','同一花边框内换字。'),
 (257,340,'衣装盒桌面','G04','桌面两态循环。'),
 (340,422,'圆盘入场','G05','入场缩放与盘缘变化分开。'),
 (422,504,'倒悬远景','G06','人物和白色幽灵线独立。'),
 (504,679,'倒悬近景','G07','重复主体，换歌词和幽灵线。'),
 (679,751,'手触衣装盒','G08','单稿长持，镜头推进。'),
 (751,834,'拿盒与首次变装','G09 G10 G11','快速切人物、手和飞溅，末尾橙色满屏。'),
 (834,1175,'黑裙半身舞蹈','G12','优先对照后面的全身动作；开场还有橙色揭幕。'),
 (1175,1328,'黑条歌词近景','G13','29个非重复编号，原片有回用。'),
 (1328,1404,'纵向花边字卡','G14','静态花边框与文字。'),
 (1404,1498,'喝茶与俯视茶具','G15 G16','喝茶长持，最后9帧切俯视。'),
 (1498,1821,'署名姿势蒙太奇','G17 G18 G19 G20 G21 G22 G23 G24 G25','拎篮、回望、法棍、后背、回头、侧坐、扫帚、捧鸭和漂浮。'),
 (1821,1908,'睁眼揭幕与卧室','G26 G27','黑线遮罩撤开，切房间后黑字块与画面震动。'),
 (1908,1976,'黑白字块与白色圆环','X03','参考片没有逐张编号；按特效拆分。'),
 (1976,2153,'散发拿盒','G28 G29','全身到近景；按两种构图参考。'),
 (2153,2278,'肖像胸针与放射转场','G30 G31','蝴蝶结底、胸针效果、橙色放射分别做。'),
 (2278,2306,'三个头部叠加','G32','三种头部与复制排版。'),
 (2306,2633,'黑裙全身舞蹈','G33','68个编号，重点看腿、重心、裙摆和转身。'),
 (2633,2801,'藤蔓房间站坐','G34 G35 G36','三个单稿构图，人物淡出和字块独立。'),
 (2801,2948,'近景舞蹈复现','G12（局部）','既有动作放大、歌词改变；不因构图变化自动增加人物稿。'),
 (2948,3288,'藤蔓间奏八组动作','G37 G38 G39 G40 G41 G42 G43 G44','开场先见背景，再倒悬四姿、正向四姿，各两态。'),
 (3288,3373,'面包篮漂浮与星芒','G45 G46','人物/篮子与星芒遮场独立。'),
 (3373,3625,'黑裙半身舞蹈复现','G12（后半）','复现已有动作序列，保持原片的删节与曝光。'),
 (3625,3778,'黑条歌词近景复现','G13','相同动作在新时间再次出现，不按整段新增。'),
 (3778,3945,'钟表与藤蔓字卡','X04','钟表、画框、藤蔓、竖框与文字分别列对象。'),
 (3945,4021,'短句与花瓣','X05','花瓣开始，文字单独渐显；无可见人物。'),
 (4021,4103,'红裙全身过门','X01','参考片未逐张编号，补入原片姿态；红裙、长手套与黑裙版不同。'),
 (4103,4261,'红裙半身舞蹈','X02','参考片略过的变装动作：保留手套、袖形、领结等新绘制内容。'),
 (4261,4337,'字句与三格头像','G47 X05','字句、头像三格和心形符号的排版变化分开。'),
 (4337,4355,'嘴部横条特写','G48','6个局部人物态，单独拆嘴型。'),
 (4355,4401,'藤蔓空房间复现','G34 G35 G36（背景）','既有背景再用，字块与花瓣独立。'),
 (4401,4431,'红裙回头与落泪','G49','6个参考态；有新的服装和泪光。'),
 (4431,4511,'末尾花边字卡','G03（框体）','花边横框复现，文字与花瓣独立。'),
 (4511,4584,'红裙托手眨眼','G50','3个编号态；右手托起，眼睑和描线切换。'),
 (4584,4763,'红裙全身谢幕','G51','19个编号，末态长持；花瓣继续独立移动至尾帧。'),
]
chapters=[]
for i,(a,b,title,refs,note) in enumerate(chapter_specs):
    chapters.append({'id':f'M{i:02d}','start_frame':a,'end_frame_exclusive':b,
        'frame_count':b-a,'start_s':tm(a),'end_s':tm(b),'duration_s':tm(b)-tm(a),
        'title':title,'groups':refs,'note':note,'representative_frame':(a+b)//2,
        'boundary_status':'visually reviewed analytical work partition; not author production shot list'})
assert chapters[0]['start_frame']==0 and chapters[-1]['end_frame_exclusive']==len(timeline)
assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(chapters,chapters[1:]))

# Supplemental source states omitted from the tutorial's numbering. A frame-change
# proposal is visually inspected before inclusion; it is not called an author cel.
full=[r['frame'] for r in metrics[4021:4103] if r['adjacent_mae']>1.5]
close=[r['frame'] for r in metrics[4103:4261] if r['adjacent_mae']>3]
extras=[
 {'id':'X01','title':'红裙全身过门：原片补充','frames':full,'kind':'人物','range':[4021,4103],
  'note':'参考片没有编号的红裙动作，共19个合成姿态。F4021只持续1个视频帧，但腿和裙摆确与F4022不同，按独立可见姿态保留；尚非作者原图去重数。'},
 {'id':'X02','title':'红裙半身舞蹈：原片补充','frames':close,'kind':'人物','range':[4103,4261],
  'note':'30个合成姿态；黑裙动作可参照运动，红袖、长手套、领结和裙身需按本段处理。花瓣不并入人物。'},
 {'id':'X03','title':'黑白字块与白环：原片补充','frames':[1908,1916,1927,1936,1941,1949,1956,1963],
  'kind':'特效','range':[1908,1976],'note':'8个关键合成参考；字块/墨迹与白环按效果组织，未将其称为8张人物稿。'},
 {'id':'X04','title':'钟表藤蔓背景：原片补充','frames':[3778,3810,3845,3878,3915,3941],
  'kind':'背景','range':[3778,3945],'note':'6个构图/指针/字卡阶段参考；背景元素复用，画面推进不逐帧整张重画。'},
 {'id':'X05','title':'短句、心形与花瓣：原片补充','frames':[3945,3980,4010,4261,4270,4315,4320,4329],
  'kind':'特效/文字','range':[3945,4337],'note':'8个代表构图；文字和心形符号可独立做，花瓣单列。'},
]
for g in extras:
    g['reference_panel_count']=len(g['frames'])
    g['count_unit']='supplemental source composition states, not unique character drawings'
    for i,f in enumerate(g['frames'],1):
        end=(g['frames'][i] if i<len(g['frames']) else g['range'][1]) if g['id'] in ('X01','X02') else None
        panels.append({'id':f"{g['id']}-{i:02d}",'group':g['id'],'title':g['title'],'reference_number':None,
            'reference_frame':None,'reference_time_s':None,'source_frame':f,'source_time_s':tm(f),
            'source_exposure_end_frame_exclusive':end,'kind':g['kind'],'note':g['note'],
            'origin':'attachment_1_supplement_not_numbered_in_attachment_2',
            'status':'source_visible_composition_candidate','unique_author_cel_claimed':False})

write(OUT/'data/reference_groups.json',groups)
write(OUT/'data/reference_notes.json',notes)
write(OUT/'data/supplemental_groups.json',extras)
write(OUT/'data/chapters.json',chapters)
write(OUT/'data/panels_curated.json',panels)
write(OUT/'data/curation_decisions.json',{
    'reference_holds_reviewed':382,'review_method':'all 16 contact sheets, 384px wide images; selected native reminders exported separately',
    'duplicate_holds_removed':['H047','H057','H109','H139','H151','H182','H208','H256','H292','H315','H342','H374'],
    'reference_loop_and_replay_cards_add_drawings':False,
    'all_reference_panel_counts_are_author_cel_counts':False,
    'source_frames_4021_4022':'Native inspection confirms different leg/skirt poses. F4021 is a one-video-frame visible pose and is retained as X01-01, rather than discarded as a reveal.',
    'full_movie_layers_restored':False,'image_generation_calls':0})
for j,g in enumerate(extras):
    for page,off in enumerate(range(0,len(g['frames']),24),1):
        batch=g['frames'][off:off+24]
        sheet('original',batch,f"supplement_{g['id']}_{page:02d}.jpg",4,384,
            labels=[f"{g['id']}-{off+i+1:02d}" for i in range(len(batch))])
# Boundary pairs make every chosen chapter edge reviewable.
boundaryframes=[];labels=[]
for c in chapters[1:]:
    for f,tag in [(c['start_frame']-1,'before'),(c['start_frame'],'after')]:
        boundaryframes.append(f);labels.append(c['id']+' '+tag+' '+c['title'])
for page,off in enumerate(range(0,len(boundaryframes),24),1):
    sheet('original',boundaryframes[off:off+24],f'chapter_boundaries_{page:02d}.jpg',4,384,labels=labels[off:off+24])
print(json.dumps({'chapters':len(chapters),'reference_groups':len(groups),
    'reference_panels':sum(g['reference_panel_count'] for g in groups),
    'supplemental_panels':sum(len(g['frames']) for g in extras),'all_panels':len(panels)},ensure_ascii=False),flush=True)
