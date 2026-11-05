from pathlib import Path
import re
R=Path(__file__).resolve().parent;B=R.parents[3]
src=B/'drawings/ART-G33-57/v01/prep_first_api_source2558_openpalms_downrecoil_farLEFT_v02/finalize_PREPONLY.py'
s=src.read_text(encoding='utf-8').replace('ART-G33-57','ART-G33-58')
obs={
 'canonical':'JOB/PROVENANCE/catalog/PRIORITY一致2564/PTS1368832；first1088..1092/PTS580848..583520。无ID返图/attempt/unknown，registry无ID。',
 'identity':'LEFT首前缀之后明确中性灰短圆润bob女孩/自然灰刘海/贴颊侧发和低LEFT双珠，原红角色尖长额发侧刺非目标且非仅改色。图1只本动作眼口衣手body，图3不改本源圆眼波嘴/手/body。',
 'eyes_mouth':'当前圆睁不对称眼弧/单iris露出与小浅波闭口，不复制57张口、AI微笑或11中性口。source5positive不发G02半睑bitmap/18灰环。',
 'hands_body':'两手已分开：画左胸前折腕分指下垂/拇指向左，画右外侧摊掌近横向/拇指向上长指向右。不是57高交叠掌或60OK。原袖腕肩frill/领bow金扣/腰后右扬白bow带/长apron锯齿边黑裙和交叠腿均source2564独占。',
 'source_cutoff_EXCEPTION':'原full2564底1080切掉完整脚鞋，只见小腿、一条踝带和贴底皮肤段，没有完整两鞋。完整sourceguide仍6241072保原截断，不补隐藏鞋尖、不缩短/上移人物凑鞋。first1088半身摄影另审不能覆盖canonical可见裙腿。',
 'root_projection':'已转近正面，LEFT根重新按画右同侧低耳后/nape/bob下投影，不沿57侧面隐藏假设，不画左加双珠第二卷、不抬根/镜像。实际bob/肩遮挡才遮，不追全露尾。',
 'phase':'原两红卷转正均可见，末端主要外下/回收，不是持续升高；只转译相位，不把两红卷身份带入。不按固定轴长/孔数冻结，不为遮挡微缩固有发量。',
 'AI_limit':'actualR205full，hair-only[594,222,633,255]39x33排除脸眼手root，少量白frill邻界。仅近颈压缩回弹，不复制其表情/body/指形/实心卷，不用小ROI缩发。',
 'geometry_material':'exact6refs均actualview。correct11整头216fd给OCgraybob身份及合理头肩发量/宽gray前内后返回/渐收C；detail0b88舍高光暗底，keyd142所有gray面同flat+较薄mutedmint材料边。禁附盖圆盘堆/实心锥/micro，不全挖opaquegray返回。',
 'cap_canvas':'源白cap两黑叶正面原透视/自然短公共基部P2；完整未挖头6241072guide/REGPLAN/JOB不改，无新trim或artpatch，摄影/动态另审。',
}
start=s.index(" 'observations':");end=s.index("'API_calls':0",start)
s=s[:start]+" 'observations':"+repr(obs)+",\n"+s[end:]
parent='在57v03身份明确版之后，PREPONLY准备G33-58(first1088..1092)真canonical按原动作，暂不扩63。后续FIRST均在LEFT固定前缀之后明确图3中性灰短圆润bob女孩身份，图1红发/尖长额发侧刺不是目标、不仅改色，图1仅本动作眼口衣手body，图3不得改变本原表现。六ref/high透明/新Preview/8字段formal及hashlock，0execution/attempt/HTTP/native，由root亲自view/send。'
s=re.sub(r"'parent_instruction':'.*?','project_user_broad_scope'",repr('parent_instruction')+':'+repr(parent)+','+repr('project_user_broad_scope'),s,count=1)
p=R/'finalize_PREPONLY.py';assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf-8');print(p)
