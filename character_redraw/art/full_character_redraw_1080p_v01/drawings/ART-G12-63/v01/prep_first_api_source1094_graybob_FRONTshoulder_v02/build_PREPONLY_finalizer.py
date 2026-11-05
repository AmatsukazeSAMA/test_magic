from pathlib import Path
import re
R=Path(__file__).resolve().parent;B=R.parents[3]
src=B/'drawings/ART-G33-58/v01/prep_first_api_source2564_graybob_sourcecutoff_v01/finalize_PREPONLY.py'
s=src.read_text(encoding='utf-8').replace('ART-G33-58','ART-G12-63').replace('624x1072','1328x992')
obs={
 'canonical_queue':'JOB/PROVENANCE/catalog/PRIORITY一致1094/PTS584048，first1093..1097/583520..586192；原40queue rows含本ID。无IDraw/attempt/unknown，ASSET无ID。旧source-only v01不覆写。',
 'identity':'LEFT首前缀后明确图3中性灰短圆润bob/自然灰刘海/贴颊侧发与唯一低LEFT双珠；源红角色尖长额发双高卷不是目标，不仅改色。图1只当前圆睁弧闭笑/双摊掌/衣body。',
 'eyes_mouth':'原正面双眼圆睁弧/虹膜露出/视线与简单弧形闭口笑，当前source5positive；不沿58波口、57开笑或11neutral。新稿不送旧G02半睑bitmap，单charcoal和普通圆点仅文字。',
 'hands_body':'双肘外展/两掌朝上不同高低：画左掌更高长指左/拇指斜上，画右低掌长指右/拇指上，原指形间隙腕袖不同。黑长袖redbowgold、肩fan/白竖带、腰后bow/apron半身底裁全源1094独占，非58body或原JOBrecoloralias自动复用。',
 'root_and_FRONT_user_override':'用户原文F1094钻发回到肩膀前/根据上一张需要连贯。此正面LEFT仍画右低耳后/nape，不换边/抬根/镜像；从同低根自然绕到画右肩前胸侧低垂，不能整束又藏frill后或背面。局部bob/真实衣领接合可遮，不改肩手，不用巨型/micro解决位置。旧SOURCE_OBSERVATION behind-white-shoulder为历史被本指令覆盖。',
 'phase_continuity':'原1094/1093/1097均近正面双肘展开，原两红卷低垂外下，未见新高上冲。只转译phase，非双卷身份。前时间态58F1088..1092与JOBfamily前60不同，前58未fresh完成时只留待实际邻曝光核，不假称连贯pass。',
 'AI_limit':'actualR209full，复用已排珠的purehair[608,222,651,249]43x27 SHA97269443，当前exact6actual看。仅局部压缩弹性，不定root/前后/体量，不能据tinyROI缩发或沿AI肩后遮挡覆盖用户前肩。',
 'geometry_material':'图3完整整头卷216fd只身份与合理相对头肩量/宽gray连续前内后返回/C，图4 0b88舍高光暗底，keyd142所有gray面同flat、较薄mutedmint材料边。无附盖盘堆/实心锥/细S，不一律挖opaquegray返回，不固定孔轴圈长。',
 'cap_canvas':'原白cap2黑叶/正常短共同基部P2。原1328992完整未挖头guide保所有掌尖和apron底，足够紧凑不新trim/warp/patch，REGPLAN/JOB未改，不声称Sunburst硬尺寸界限。',
}
start=s.index(" 'observations':");end=s.index("'API_calls':0",start)
s=s[:start]+" 'observations':"+repr(obs)+",\n"+s[end:]
parent='请PREPONLY只准备G12-63（用户F1094明确钻发回到肩膀前，固定原低LEFT根不换边/不巨型/不实心），first1093..1097，实际母帧/源眼口/动作按catalog核。现头身转正后画右LEFT根在前肩路线，参考前58当前阶段，但不要复制其body或source眼口。灰短bob身份必须显式，图3只人设/卷体量，不沿红源尖刘海。六项目图/ownsourceeye/purehair与最新graydetail/无打光键，Preview high透明n1retry0、8fieldsformal、新锁和实际全部看。0execution/attempt/network/native，不再继续64或改中央。'
s=re.sub(r"'parent_instruction':'.*?','project_user_broad_scope'",repr('parent_instruction')+':'+repr(parent)+','+repr('project_user_broad_scope'),s,count=1)
p=R/'finalize_PREPONLY.py';assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf-8');print(p)
