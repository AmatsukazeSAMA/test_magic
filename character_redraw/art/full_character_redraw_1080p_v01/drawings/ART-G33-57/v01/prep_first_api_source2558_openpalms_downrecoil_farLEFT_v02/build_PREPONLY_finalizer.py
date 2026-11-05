from pathlib import Path
import re
R=Path(__file__).resolve().parent;B=R.parents[3]
src=B/'drawings/ART-G12-60/v01/prep_first_api_source1082_downswing_farLEFT_v01/finalize_PREPONLY.py'
s=src.read_text(encoding='utf-8').replace('ART-G12-60','ART-G33-57').replace('736x1072','624x1072')
obs={
 'canonical':'JOB/PROVENANCE/catalog/PRIORITY一致2558/PTS1365632；首1084..1087/PTS578720..580848。全ID无返图/attempt/unknown，registry无ID。',
 'eyes_mouth':'原圆睁眼/虹膜露出/普通点与张开笑粉内口，不沿60半睑、11neutral或AI闭笑。图5当前source positive；没有G02bitmap或18灰环。',
 'hands_body':'双掌全在画右脸旁斜外上展开交叠，前景大掌/长指与后掌只实际可见指保持，后掌部分被大白袖口/前掌遮住不补全。原交叉前臂/腕角/衣领结/后bow长带、长apron锯齿下摆和黑裙均保，不沿60OK或AI左右低手。',
 'fullbody_crop':'canonical2558完整两腿两踝带鞋：靠近异角，两鞋端均有原像素，不能照首1084半身裁掉。实际first1084与canonical动作同态摄影不同，body不alias别稿。',
 'root_projection':'比60更转正的右向视角，唯一LEFT仍画右低耳后/nape/bob下，画左近耳无双珠；不追露脸抬/换根或镜像。部分根卷可自然被bob/原肩/袖掌挡。',
 'phase':'原2558与1084近侧红卷向外斜下，Sol audit57核下摆与远侧大部头遮。仅转译摆动stage到LEFT，不能机械镜像近红卷/root，不能用隐藏解释可见实心封口。',
 'AI_limit':'actualR202full完全不同双手低分开/闭笑，body脸不发。v01crop顶端含少量红珠边，留历史不发送；v02[594,222,633,255]39x33只颈侧gray段/少量白frill邻界，排眼手珠root。只次级下回收/压缩，不定根/固有发量/实体构造。',
 'geometry_material':'exact6refs均actualview。correct11整头卷216fd只相对头肩合理发量/宽gray连续前内后返回/C；graydetail0b88舍高光暗底，keyd142所有gray面同色、较薄mutedmint材料边。非micro/巨粗、无固定孔轴圈长。',
 'cap_occlusion':'原白cap+两黑叶在源头顶透视位置，非11正面侧翼位；正常短共同基部P2。按原bob/肩/交袖掌自然遮挡，不强露尾、不微缩发假遮挡。',
 'canvas':'完整未挖头6241072guide原坐标不改，REGPLAN/JOB无修改；无新trim或单部位warp/artpatch，实际摄影另审。',
}
start=s.index(" 'observations':");end=s.index("'API_calls':0",start)
s=s[:start]+" 'observations':"+repr(obs)+",\n"+s[end:]
parent='请PREPONLY下一从未绘制ART-G33-57（first1084..1087，清单实际canonical核对），延续60向下/回收阶段但动作眼口双手必须本原PV；唯一低napeLEFT根透视，灰宽ribbon返回真实连通，不能附盖盘/实心锥或micro。6refs同来源类型，Preview/8字段formal/hashlock，无execution/attempt/HTTP/native，root会亲自view/send。按用户首图API/high透明；不动59/60文件。'
s=re.sub(r"'parent_instruction':'.*?','project_user_broad_scope'",repr('parent_instruction')+':'+repr(parent)+','+repr('project_user_broad_scope'),s,count=1)
p=R/'finalize_PREPONLY.py';assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf-8');print(p)
