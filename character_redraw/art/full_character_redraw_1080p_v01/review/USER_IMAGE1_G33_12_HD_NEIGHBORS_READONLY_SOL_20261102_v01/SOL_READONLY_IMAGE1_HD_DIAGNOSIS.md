图1精确匹配 ART-G33-12 / v02，first878–881，母2351（PTS1255120/16000）。截图无法区分同一hold内具体哪一帧。

当前raw：D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01\drawings\ART-G33-12\v02\character_api_original.png
SHA：44c4d543d1eaa1606d0009b8fd33bad0789032487047a7c51b0d3aaf5b2d9be5
原PV母图：D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\cels\G33-12\source.png
源SHA：2b65ad9dfe9c349e87d99b544f64b24c56fa102847856f76ed3fefec0cc378db
首曝光：D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01\coverage\source_frames\F000878.png

当前66包v02、boardv07、registry/currentpolicy和绑定均匹配。五态package renderer与原proposal在可见RGBA像素完全相同；没有发现装错版本。

| 相对态 | ID / first | raw尺寸 | 当前摄影倍率 | 解析风险 |
|---|---|---:|---:|---|
| 前2 | ART-G33-10 / 871–873 | 964×1632 | 1.128339× | 较低，轻放大 |
| 前1 | ART-G33-11 / 874–877 | 624×1072 | 1.818947× | 同档较高 |
| 图1 | ART-G33-12 / 878–881 | 624×1072 | 1.719088× | 本次目标 |
| 后1 | ART-G33-13 / 882–885 | 624×1072 | 1.869940× | 同档较高 |
| 后2 | ART-G33-14 / 886–888 | 839×1875 | 0.967194× | 较低，略缩小 |

图1原稿624×1072但当前摄影s=1.7190884359、t=(444.92493244,83.61969204)，只有顶端约580行投到半身1080画面。实际完整1080和头手卷2x只读局部可见帽沿、指线和发丝抗锯齿被放宽，细返线存在采样上限；不能因输出canvas为1920×1080就称原画细节已足。11/13同为624×1072且放大更大，应作为相邻解析风险并看。10/14没有同档大放大条件。

原动作顺序：10正面折腕高臂→11正面斜高摊掌→12左侧单圆眼/闭口、耳上掌→13背3/4闭眼低前手/后腰手→14纯背无脸。高清稿不能把相邻表情、手式或屏幕根侧冻结过来。母2351是完整全身，first878是半身摄影，不为露鞋缩小人物。

同构图若要让当前摄影接近1:1，12的数学尺寸约1073×1843；这只是解析诊断，不是强制输出规格，改变尺寸或DPI不会自动补回线条。新IMGGEN高清稿应保现有动作/卷体后fresh实审，再重新统一定位。11有用户正确卷形政策，不能以高清化顺带改坏轮廓、返回接合和C。

只读证据：

- SCREENSHOT_VS_CURRENT_BOUND_MATCH_READONLY.png
- NEIGHBOR_5STATE_SOURCE_RAW_BOUND_READONLY.png（5行已实际核看）
- G33_12_CURRENT_REGISTERED_HEAD_HAND_COIL_NEAREST_2x.png（仅已有输出像素2x诊断）

本任务0生成/API/网络，未改中央/registry/绑定或艺术像素；没有新增静态艺术通过，也未实际播放，不认证动态。

JSON SHA：3c53900363d7852758270ae9591ab94a4da006367883a3ba3f08cb63987c9e34
