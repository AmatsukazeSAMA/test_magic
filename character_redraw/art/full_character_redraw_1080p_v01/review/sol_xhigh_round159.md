# Sol xhigh round159 — G33-07 v14

**结论：repair_required；independent_static_pass=false。明确P1：卷体量过大。**

原图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-07/v01/whole_imggen_source2333_visible_horizontal_hairphase_v14/character_imggen_original.png

SHA-256：`95ea08e7af8f6c60592cc18131b74c5a8dc3662c3e7e9f6ed29911a07aea051f`（957×1644）。这是已知whole修复，非新FIRST。

实际19张图/五exact refs/完整prompt均查看。源2333 / PTS1245520，first861..862两native均实际看，PTS [459664,460720)，timebase1/16000。逐张路径/SHA和新v14白黑3x源/ROI见JSON，未沿用157旧图作本次证据。

- **P1体量：** 完整头肩中，粗宽卷体从低耳横伸接近一个bob宽、到当前画右边附近，多片厚前面一起明显增加发量。同态v11整体占用更收，正确11全头肩参照也不支持这份额外长度和厚度。不是只把等量发束转横；不能只因轴正确放行。v11仅对照同态收回后体量，不恢复其坏上端。
- **连接：** 新3x可追宽灰前面、灰内/后返回和渐细C，未见明确独立封盘或实心柱P1。实际外部间隙随白黑背景改变，但隐藏轴心不认证；不以opaque灰/固定孔数否决。
- **材料：** 本v14未见v13同等级首返回/C大块深灰体积底重现。首内返、小叠面略深和mint宽度变化记P2，严格平涂仍未认证；不继承157材料P1。
- **方向/根：** 近水平向外主段已恢复，低LEFT画右双珠/短bob连接保住，无第二束/高根。静态方向改善不等于动态通过。
- **人物/cut：** 原圆睁不等眼/tiny中性闭口、斜跨长臂下手/腰后手、衣帽裙apron和交错抬腿保。前鞋保存平切已恢复，仍须与原1080边界摄影对齐；first861..862半身不得露腿鞋。白黑外缘未见明显实体RGB噪点/背景拼接，raw透明RGB不单判实体。

修复应锁原人姿、低根与外甩方向，在同态合理头肩占用内收回长度和厚度，重建连续宽灰前返回/C，不能裁尾、遮尾、缩全身或退成tiny。输入变更与放大返图同时出现不证明模型内部唯一原因。任何后续局修仍须whole后fresh实看。

政策：goal_curl_assessment_20261102_v03 / open_hollow_ribbon_20261101_v01，SHA `b06daa9a9a043cbd26d3af8bab5125969faf05154a93bf2f9249defc69d06e4a`。摄影/动态/隐藏几何/用户验收均false；0生成网络/中央PRIMARY绑定修改。

