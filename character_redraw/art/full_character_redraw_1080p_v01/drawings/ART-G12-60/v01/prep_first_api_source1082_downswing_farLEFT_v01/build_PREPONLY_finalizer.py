from pathlib import Path
import re
R=Path(__file__).resolve().parent;B=R.parents[3]
src=B/'drawings/ART-G12-59/v01/prep_first_api_source1078_horizontal_rebound_farLEFT_v02/finalize_PREPONLY.py'
s=src.read_text(encoding='utf-8').replace('ART-G12-59','ART-G12-60').replace('816x1040','736x1072')
obs={
 'canonical':'JOB/PROVENANCE/catalog/PRIORITY一致1082/PTS577648；首1079..1083/PTS576048..578720。无ID返图/attempt/unknown、registry无ID。',
 'eyes_mouth':'当前不对称半睁弧/原虹膜露出与普通圆白点；小U形张开笑口粉内口。图5原轮廓不沿59大开笑口或55闭波口；没有G02半睑bitmap/18灰环。',
 'hands_body':'高画右角形OKthumbindex保持闭合空；余指钩角与间隙依1082。胸前另一手仅当前可见垂指，部分被高前臂/袖口遮住不补全。原交叉臂/肩fanfrill、领结金扣/腰褶后bow/半身底裁全依源，不套55..59 body或手。',
 'root_projection':'本右向3quarter远侧LEFT低root在画右bob/nape；画左清楚可见近耳下没有双珠。不为露根移近侧或镜像；自然bob/肩/高袖遮挡可藏部分根卷。',
 'phase':'原1082近侧红卷尖低于根，首1079同态。Sol只读audit60核再次下摆，不能继续59横甩或55上提；只转译摆动阶段到远LEFT，不机械镜像原近红卷/root。',
 'AI_limit':'实际看R198full，crop[553,202,585,230]32x28只近颈灰发段/少量背景，无眼/手/root。只次级回收压缩弹性，不定source动作或固有发量；不复制实体封口构造。',
 'geometry_material':'exact6refs全actual看。correct11完整headcoil216fd只相对头肩合理发量+宽gray连续正内后返回+C，detail0b88舍精修光/暗体积，keyd142所有gray同flat。既非微型挂件非粗巨大，不固定孔轴圈长。',
 'cap_occlusion':'本源白cap与2叶在头顶透视位置，不能沿correct11正面右边翼形位。短共同基部P2。胸前手/高袖/肩白褶在远侧路径前，自然遮挡不强露尾/缩发假遮挡。',
 'canvas':'原JOB/sourceguide736x1072保持，无新compact/trim/单部位变换或artpatch；REGPLAN原样，摄影root另审，不宣称Sunburst硬尺寸界限。',
}
start=s.index(" 'observations':{");end=s.index(" },'API_calls'",start)
s=s[:start]+" 'observations':"+repr(obs)+",\n"+s[end+3:]
parent='之后PREPONLY准备下个从未绘制G12-60：必须据清单实际母帧/原图，原PV动作唯一/AI仅hairsecondary；趋势59水平外摆之后60向下，固定低耳后LEFT根，不追露脸加珠。项目6参考，Preview high/n1/transparent/retry0，准备8字段锁文件+exactformal+prompt并实际全看。PREPONLY无execution/attempt/网络，root自己看并发。59已准备root接手，不动其文件。'
s=re.sub(r"'parent_instruction':'.*?','project_user_broad_scope'",repr('parent_instruction')+':'+repr(parent)+','+repr('project_user_broad_scope'),s,count=1)
a=s.index('old=R.with_name(');b=s.index("script='''",a);s=s[:a]+s[b:]
p=R/'finalize_PREPONLY.py';assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf-8')
print(p)
