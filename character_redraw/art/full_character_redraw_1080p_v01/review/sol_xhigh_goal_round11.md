# Sol xhigh 第11轮独立静态复核

实际查看四张原图、白黑QA、源姿势与指定邻稿，四张均可保留为 **retained_static_candidate**。未获用户接受，未验最终合成或动态；没有生成、改图、改alpha或主账。

| ID / 版本 | 源帧 | 结论 | 主要证据及后续 |
|---|---:|---|---|
| ART-G24-01 / v01 | 1763 | 静态候选 | 低头视线、帽叶、双手/指头、完整单钻发与服装合理。原鸭须独立遮回，鸭后白围裙补画仅为余量，不能当源已显示。 |
| ART-G27-01 / v01 | 1865 | 静态候选 | 灰宽领短袖/被前手、无帽与源合理。珠根近看是两颗红珠；下左珠被bob斜遮露两段红弧，不是额外旧红发楔。床被独立遮挡。 |
| ART-G26-04 / v01 | 1849 | 静态候选 | 大睁眼/小闭口、脸眼位置、灰家居领口保留，真实上/左右特写裁切成立。钻发可自然出画，不强塞全头；字幕/黑线独立。 |
| ART-G33-04 / v03 | 2319 | 静态候选 | 举拳/抬脚/O嘴、双腿和鞋完整，帽/服装/单钻发合理；对照G33-03当前whole无明显静态翻边。已否决v02裁腿稿不选。 |

四张白黑QA未见必须修复的明显接缝、旧红双钻残片、漂浮帽叶或空区实体碎屑。没有提出局修或整图重画；道具/摄影注册仍须在最终1080合成验证。

G27额外实际近看：qa_white ROI x430..519、y320..409，内存JPEG放大只判断轮廓/遮挡，没有写诊断图。完整实际查看路径、各项详细观察及精确image SHA256见同名JSON。

- ART-G24-01: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G24-01/v01/character_api_original.png`
  SHA256 `a52de6961bb29c2d4c9be49293fc8f602e04167230d17e7f19e346fc8d1dc8a9`
- ART-G27-01: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G27-01/v01/character_api_original.png`
  SHA256 `eda0b9ae8f0822b637fdd9845981aa39911245329efa0aaf299fe2ec8ad8ef99`
- ART-G26-04: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G26-04/v01/character_api_original.png`
  SHA256 `23917750e0622df68edfe9899b377e400b1e225020eef310a2b4700800d5f697`
- ART-G33-04: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/character_api_original.png`
  SHA256 `f2055c824f25bf663538cbbcebbb0d602ec2e33dea3b61e5c1f1c8ec56607429`

