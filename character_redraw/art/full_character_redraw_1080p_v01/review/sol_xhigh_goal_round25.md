# Sol xhigh round25 独立静态艺术复核

2026-10-31。实际打开新G45 whole原图、白黑QA、当前sourceguide、青色道具位置注释、native F3288及完整钻发/单色眼参考；另外实际做内存颈部比例近看。

**ART-G45-01 / v01/whole_imggen_v01：needs_repair（P1）**。

- 当前raw：[character_imggen_original.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/whole_imggen_v01/character_imggen_original.png)，1254×1254。
- 精确SHA256：`6e46a68361889b47d92161fb3e7fee138cc3bceb2a1ec381d544bcafc4fdf67d`。

主篮/面包负空间、前景握指、弯腿鞋裙与腰后飘带已大体恢复；灰bob、两珠、连续足量单卷、两黑叶贴头、当前单色睁眼/微笑与肤色可留。没有把独立篮子缺失当身体丢失。

需要修的是**篮缘外原片实际露出的黑立领及少量红衣结边**：sourceguide约x530..573、y276..355，原native同样可见。当前whole颈底到白肩之间却为空；raw(830,455)/(850,475)/(850,485)均A0。源guide(540,290)=R42/G44/B41黑领。新负空间误删了源可见制服，不能仅用道具覆盖解释。

青色注释是粗定位证据，不能当真实道具alpha：黑领(540,290)在注释仍黑；source(548,332)=R175/G0/B5红衣料，但注释同点已被涂cyan。正式修正应回原source区分篮边/衣料，保留注释历史，不盲信粗罩。

只恢复上述实际可见黑领/红小边、连接现有颈底与白肩；保留当前主体/握指/腿裙/飘带/完整钻发及主道具孔，**不补篮后胸腹、整红结或隐藏手**。若API局修，随后按用户规则builtin imggen整体重绘，再对新精确图双审。

## 实际查看与SHA

- [ART-G45-01/v01/whole_imggen_v01/character_imggen_original.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/whole_imggen_v01/character_imggen_original.png) — `6e46a68361889b47d92161fb3e7fee138cc3bceb2a1ec381d544bcafc4fdf67d`
- [ART-G45-01/v01/whole_imggen_v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/whole_imggen_v01/qa_white.png) — `9cc441ff53ddc786ff7e836b124515f01bd8f810c73937fcd6fc625c6dacfb3b`
- [ART-G45-01/v01/whole_imggen_v01/qa_black.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/whole_imggen_v01/qa_black.png) — `542be35b9b859a0a9900c20c8232bf57fecc4fa25a2e8231b14814662da99690`
- [ART-G45-01/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/inputs/source_pose_guide.png) — `cfe956fa4dbbb81902ef70f88858f0a067334867d58471fb0b75a4e6dd2a3c97`
- [review/diagnostics/G45-01_basket_occlusion_source_v01/original_action_cyan_independent_occluder.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G45-01_basket_occlusion_source_v01/original_action_cyan_independent_occluder.png) — `173faa060ca49d30fd31a1896f48c0032a5b18bf7dae06f4f6901799f435fd64`
- [full_character_redraw_1080p_v01/coverage/source_frames/F003288.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F003288.png) — `ec1e9cc115a61f8096e8c49fb6ff4309d758fc53ec6d584a956acac6226db93c`
- [art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png) — `c580f9ffe8d93ca121eccdae6f82d67fadcce18cfa72bd5322d8e9859380eaa1`
- [ART-G02-01/v02/whole_imggen_v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png) — `fcc9f01ffa5b08992106132bdeb2397cd969cbd3ec8140b04fc621885a930f72`

## 局限

局部对照源ROI `[480,245,600,350]`，当前白QA比例ROI `[738,377,923,539]`；只在内存显示，近似比例，不是最终摄影配准。原raw部分彩色细点在正常白黑QA无明显实体，未将透明RGB当新增艺术缺陷，也未声称编码清零。

本轮尚未合篮：握指/篮沿接触、道具alpha、摄影与动态均待验证。`user_accepted=false`、`art_accepted=false`、`dynamic_validated=false`。未修改画稿、注册或曝光账，未生成。

## 已保存的只读诊断

[原源/粗cyan/新whole三列放大对照](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G45-01_visible_collar_round25_v01/comparison.png)，已保存后实际打开；[ROI和来源坐标JSON](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G45-01_visible_collar_round25_v01/ROI_COORDINATES.json)。只写新诊断，没有改动任何原source/返图/QA/注释。

- comparison.png SHA256 `b32004ffa5469cf69e87af17f31ee4b4db4407c48f7994333dfea0f38f82d15e`
- ROI_COORDINATES.json SHA256 `a31a258f3e0af13f80151abc2ae2b9cfb09474a15a13b14115d739d39ece4f6c`


