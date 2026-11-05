# 全片目标 round03 独立复核

**两项均为needs_repair，各有一个明确主要方向。** 未获用户接受，未验动态。仅看图，未生成/改画/改主账。

| 项目 | 源帧 | 主要问题 | 必须保留 |
| --- | ---: | --- | --- |
| ART-G02-03/v01 | F121 | 单钻发在画内过早收尖，较G02-01最终整稿明显跳短/变窄。 | 本帧闭眼、头倾、手势和灰衣折线。 |
| ART-G33-03/v03 | F2314 | 黑瞳仁+浅灰iris环仍是旧双层眼体系，未执行当前单色试验。 | 当前源圆睁眼和视线、抬手/外伸手、交错迈步及服装。 |

G02当前1344×1072，相邻G02-01整稿1387×1134，头肩尺度近似。当前钻发约x1090–1335、y400–905，在y885附近出现完整尖尾；前稿同一珠根的钻发沿肩后继续向右下出画，没有显示尾尖。源只是闭眼和小幅头部变化，不能解释这次长度/体量跳变。只修钻发连续体量，使其随本帧肩部自然延续，不强拉到肩前，也不把旧头/旧发卷贴回来。旧稿画外尾型没有实际显示，不能说其隐藏精确长度已验。

G33双眼问题约x230–342、y140–180：浅灰虹膜环和黑瞳仁区分明确，不能视为轻微色边。改单块深灰主填加小白高光，保留圆睁眼型与当前源神态，不能为了统一画法改半闭。与G33-02实际对照未见G02这种明显钻发骤短；帽/黑双叶、红珠、单钻发、黑服/围裙及手脚主体可保留。整稿重绘仍应带完整三视维持体量，不因旧稿被当参考就沿用旧双色眼。

上述两项如作API局修，之后都必须builtin imagegen整体重绘，再独立审核最终整稿。不能以局修看起来好就跳过整体，也不能回到拼头/拼眼路线。

## 实际看图路径

**ART-G02-03/v01**

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-03/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-03/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-03/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png

**ART-G33-03/v03**

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-03/v03/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-03/v03/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-03/v03/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png

本轮实际查看当前原图、白QA、源及上述相邻参考；没有播放完整曝光序列、验证1080p注册或宣称全片动态通过。原图隐藏RGB暗底/光晕不作可见alpha缺陷，黑底完整检查本轮未做。

