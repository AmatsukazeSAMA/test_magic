from pathlib import Path
import json,re
R=Path(__file__).resolve().parent;B=R.parents[3]
src=B/'drawings/ART-G33-26/v01/first_api_source2412_raisedindex_lowpalm_user11_v01/finalize_authorized_request.py'
s=src.read_text(encoding='utf-8').replace('ART-G33-26','ART-G33-27').replace('640x1040','624x1072').replace('slot2_independent_of_root56','slot2_independent_of_root58')
obs={
 'canonical':'PROVENANCE/catalog/JOB/PRIORITY一致2416/PTS1289824；首930..932/PTS496496..498096，非猜母帧，无ID返图/attempt/unknown。',
 'eyes_mouth':'本源近正面轻倾，双眼弧睁开及单黑虹膜，极小中性点/短竖口；不沿26斜闭口或AI笑。图5原眼口positive，不送G02半睑bitmap或18灰环。',
 'hands_body':'画左高手单index斜外上，拇指斜右上、三折指前叠，与26竖指不同；画右低手近横侧下、臂更收近身体。原腰后bow/围裙长斜褶/黑裙摆，双腿双鞋靠拢且两个完整踝带黑鞋保。',
 'root_projection':'当前近正面略转倾，LEFT仍投影画右同侧低耳后/nape/bob下，不是近画左耳/高太阳穴。根由bob/肩自然遮挡，不强露两珠尾。',
 'AI_phase':'实际看R78 full，发段[404,240,459,289]仅近肩侧回折/压缩与末梢外弹，少量frill邻界；无眼/手/root。AI不定PV动作/眼口、固有发量或封口结构。',
 'geometry_material':'全部exact六图actual看完。correct11整头卷216fd给合理相对头肩体量/宽gray前内后返回/渐收C，detail0b88舍光照，keyd142仅颜料。不微缩挂件、不粗巨大、不固定孔轴圈长，gray返回不能一律挖洞。',
 'cap_boundary':'原白maidcap和2黑叶，短共同基部按root最新意见P2，不为同类短尖自动整人重画；独立第三长叶/漏帽仍检查。',
 'adjacency_boundary':'前26只是known静态候选送141，未拿它作新表达/动作/卷master；本源独占动作，首段曝光摄影和动态未通过。',
}
start=s.index(" 'observations':{");end=s.index(" },'art_accepted'",start)
s=s[:start]+" 'observations':"+repr(obs)+",\n"+s[end+3:]
release='Root已actual26完整白黑+源2412guide/6ref，源neutral小闭口/睁眼、竖index低摊掌/两全鞋、LEFT画右lowroot均保，灰返回soft/暗线由Sol141 actual判，不即刻新增native。请继续最后一张前半未画G33-27（PRIORITYfirst930..932，核真实母帧而非猜），同26/24六refs首官方API high适合JOB画布透明/n1/0retry，mandatoryLEFT，originalPV手嘴眼衣动作、11 fullheadvolume+graydetail+palette、AIhair-only次运动。不复制上稿表情/手势。你自己refs/source actual完成后可按本消息end-to-end root release一次提交，但必须exec_command sandbox_permissions=require_escalated，不能遗漏成use_default；58曾漏用网络权限本机proxy0ms失败，避免。当前root58v02API live48015我持有1在飞，你27可slot2。若approval拒绝knownunsent，保留exactpayload/用户broadf261+rootrelease交root核查，别绕通道。返回actual白黑/source局部后停，不native/下一项，不中央/REG/bind。'
s=re.sub(r" 'parent_release_verbatim':'.*?',\n",' '+repr('parent_release_verbatim')+':'+repr(release)+',\n',s,count=1)
s=s.replace("'change':'Only own guard expected canvas 624x1072 to actual JOB640x1040; no wrapper change'", "'change':'Own guard exact actual JOB624x1072; no wrapper change'")
target=R/'finalize_authorized_request.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf-8')
print(target)
