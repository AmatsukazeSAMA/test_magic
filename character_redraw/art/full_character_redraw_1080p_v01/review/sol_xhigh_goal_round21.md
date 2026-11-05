# Sol xhigh round21 独立静态艺术复核

2026-10-31。四项raw、白黑QA和各自source均实际打开；另外看指定三邻稿、完整钻发三视、G02单色眼参考及G38根部放大。3张可留静态候选，G29 whole v03需修。用户/艺术验收及动态均为false。

|项目|当前完整图|SHA256|结论|
|---|---|---|---|
|ART-G12-35|D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-35/v01/character_api_original.png|e81774c84aac6754f256634b1b91e087e8627665f060695663eb37d25941395b|retained_static_candidate|
|ART-G41-02|D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G41-02/v01/character_api_original.png|d590a60ecc35288b6480b974ff58e559ca2582f69397701c9187ab9cf7fc5708|retained_static_candidate|
|ART-G38-01|D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-01/v01/character_api_original.png|486e6b677b3b741972f6a97f2ceb5da41a5655bd134ac1c824b13e989dcaf9ff|retained_static_candidate|
|ART-G29-01|D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/whole_imggen_v03/character_imggen_original.png|3c19f052068860f3fd99b64365e0f254c9ce9b0015228f79e4683415d4719937|needs_repair|

## G12-35

源F949的斜头半睁、小闭嘴笑及并抬双前臂/竖掌已保留。胸前袖/双白袖三角、原黑白服红结/围裙背结合理。与34相比，两珠根侧、卷量和完整根至尖长度相近；灰薄荷卷圆厚连续，无小尾跳变。帽两短黑叶贴合。静态可留。

## G41-02

原片越顶折指手与右侧裁断的另一掌、圆睁小闭口、袖/胸白褶/红结/腰带重描保留。与01相比图右双珠接粗完整单卷，未见明显跳长或翻边。帽沿被手遮住部分仍贴头，两黑叶。没有枝叶/字幕或裁外腿混入，静态可留。

## G38-01

倒置解剖左根在图左，两珠与灰薄荷卷可见，第二珠部分被灰发遮挡。实际放大当前白黑QA与G37-02：卷从珠向图上延伸，若干卷弧被源前臂/白肩/黑领自然遮住，未见暴露断口或提前尖尾；不强拉隐藏tip到肩前，不声称已看到遮挡全长。源睁眼、小闭口、跨胸袖/双白袖口/腰带/红结保留，顶部裁外手掌未补。静态可留。

## G29 whole_imggen_v03：P1需修

新稿确实画回整个粉箱及白搭扣/提手、黑轮廓，约x225..1070/y820..1218，白黑QA都清楚可见。原图(650,1000)RGBA=[241,131,129,249]，(500,900)=[251,132,130,253]，白提手(650,845)A253：是实体道具，不能交人物透明层。

只去掉独立粉箱及白金件/黑边，保留原箱沿上方可见脸颊、箱外灰衣、无帽灰bob、两珠和完整卷；不补箱后嘴/下颌/颈。去箱后须重核截口，不能再用v01/v02的高cut。若局修则按规则再次builtin imggen整体重绘并独立复审。当前因明确道具错误即拦截，未假称已清除旧截口问题。

轻柔阴影/较顺描线记录为风格局限。前三图未见正常白黑底必须修的透明碎片；不等于编码alpha清零或1080输出定位通过。全部精确路径、hash、查看记录和G38 ROI/G29 alpha见同名JSON。未改原图、计划、账本或中央注册，未生图。

