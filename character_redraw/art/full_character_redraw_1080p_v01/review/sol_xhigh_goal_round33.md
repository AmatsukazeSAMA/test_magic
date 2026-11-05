# Sol xhigh Round33 独立静态复核

2026-10-31。实际查看24个图像路径，另作只读内存放大/相邻头高并排。1项静态候选、3项需修；不沿用主审或旧baseline结论。

## ART-G12-40 — repair_required

[当前原图](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/character_api_original.png)，1216×944；run `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01`。

SHA256：`38b9c5758cf5bbb3f21b301edda6a2f890c6c48fe7e39173ffd791cb813c1bee`。

- 本态左低平摊掌、右高斜掌、微笑睁眼、源黑白女仆服保留；灰bob/双珠根位/两黑叶贴帽及头颈连接没有明显问题。
- 独立单图看主体可留，但与39按相近头高实际并排后，中下卷距及细尾明显拉长。两稿都完整露卷，前稿下段没有手臂/衣肩遮挡；两源头倾相近，不能以摄影画布尺寸差直接解释。
- 这里未证实新增一整圈，问题是同一单卷的下段长度/卷距跳变；保留当前表情双掌与服装，只修中下卷连续性。

- **P1 图右钻发中下段/细尾，current约x720..807/y392..554**：相邻39→40卷长明显增加，完整露卷情况下不能靠遮挡解释。 维持40根位、双珠、上卷体积和源双掌，仅统一中下卷距及尾端长度到完整身份与已审39的相邻比例；局修后重新整体imggen并新审。

范围：本报告更正前面尚未落盘的初步candidate；未用静态单图掩盖相邻长度问题。 手工头高标点只作近似比较，不是最终摄影锚点；未看真实连续播放。

## ART-G47-04 — retained_static_candidate

[当前原图](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01/character_api_original.png)，1024×736；run `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01`。

SHA256：`4395efe0586f4a2ce86fcf35d3ef0d7e82f1cc1b6c44cbd15b1fae148db8c2e2`。

- F4287本态半睁眼、小直嘴与红立领保留；不是把03闭眼复制进来。当前单色深灰虹膜和小白点、简洁上睫合理。
- 单个TOP头像，灰bob/两红珠/足量单灰薄荷卷在图右连续出底；未画卡框、字幕、多头像。帽贴头且两片黑叶，未见明显接缝/旧红发实体。
- 与03完整邻稿核根位/粗卷连续性，未见需要局修的明显长度变化；卡片实际顶/底viewport仍需生产定位裁切。

无本轮必须修正项。

范围：采样F4287保留；TOP crop [730,20,1205,358]是guide证据，不是alpha。 多卡复制实例注册、卡片裁切和03→04连续播放未核。

## OPT-BROOCH-PORTRAIT — repair_required

[当前原图](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/OPT-BROOCH-PORTRAIT/v01/character_api_original.png)，736×912；run `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/OPT-BROOCH-PORTRAIT/v01`。

SHA256：`9f6dcd5e7933b60c810924971be1615ca0ebbf8dbeda081b05584062d819e6dc`。

- 当前guide与nativeF2154明确只见印刷头部、细颈和窄浅色领口，原人物没有女仆帽或黑叶。金色外框、网点及巨大红bow是独立道具/效果。
- 当前返图擅加白maidcap与黑叶，还在下部画出大片红披肩/红领结、白翻领和宽肩服装；这是源可见服装/范围误判，不能由透明边技术PASS代替修正。
- 灰bob/两红珠/单卷、原源睁眼/小直嘴方向可保留；不应把独立大红bow转换成人物穿着，也不补源未显示的整肩胸。

- **P1 额顶/图右头饰，approx x125..725/y28..280**：源无帽/黑叶，返图明确添加。 移除帽和黑叶，恢复无头饰灰bob，保持当前源脸态。
- **P1 下部约x50..718/y672..900**：误画红披肩、大领结与白翻领/宽肩；源仅细颈与窄浅领口。 以原源可见头/细颈/窄浅领口为范围，去掉凭空服装；金框、网点、大红bow保持独立。局修后整图重绘再审。

范围：未合成真实金框/网点/高光，未证明人物alpha可直接放入胸针。 灰钻发可随最终正确人物范围自然遮挡/裁切，不为塞进金框缩成小卷。

## ART-G51-01 — repair_required

[当前原图](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G51-01/v01/character_api_original.png)，624×1072；run `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G51-01/v01`。

SHA256：`e3db83d02ad56bf9ad51836d603255744496f90d562101e5aec3792428823cf8`。

- 这是旧selected精确raw的最新标准复核；当前白黑诊断QA从同一alpha合成，未覆盖旧run白图，未改原图。历史baseline_v04通过保留，不继承为当前标准通过。
- 实际看既有x6眼部诊断，并独立用原QA再作x5只读放大：双眼均有独立灰虹膜外环与黑色瞳芯，和G02单色深灰不一致。当前圆睁、小闭口神态应保持。
- 钻发根与各卷段是连续的，但完整可见下段过早收尖、灰色发量偏薄且空隙偏大，呈较短的带状弹簧；图右完整tip约到y286，并非被肩或手遮住。完整身份参考是圆厚连续灰卷。
- 红短袖/红立领、黑胸bow/金扣、白围裙、黑手套、长黑袜与双鞋、全身站姿及当前暖桃肤色可保留。内侧珠被bob分隔的局部红色不机械认作第三珠。

- **P1 双眼，approx x257..366/y150..188**：独立灰虹膜环+黑瞳芯，违反当前单色眼标准。 合为单色深灰虹膜，留小白高光；原圆睁/视线/表情和位置不变。
- **P1 图右单钻发，approx x355..422/y196..291**：连续但偏短偏薄，下卷收尖急；本态完整露tip，不能以遮挡解释不足体量。 按完整身份恢复圆厚中下卷及自然细尾，保持当前根位双珠/人体与服装，不额外加第二条卷或强拉肩前；与眼修后一起whole新审。

范围：此次只撤回当前精确旧raw对最新标准的静态候选判断，不回写/删除历史v04报告。 全身生产注册、实际播放、效果遮挡及用户验收仍未验证。

## G12 相邻比对

39/40两稿均露完整下卷、两源头倾相近。人工近似灰bob头高278/266；灰卷起端至tip约179/218，约0.64/0.82头高。数字不是硬摄影锚点，但只读并排可见中下卷距/尾端明显变长；这是本轮将40由未落盘初步candidate更正为repair的原因，不声称增加一整圈。

## 实际看图路径

- [drawings/ART-G12-40/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/inputs/source_pose_guide.png)
- [drawings/ART-G12-40/v01/character_api_original.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/character_api_original.png)
- [drawings/ART-G12-40/v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/qa_white.png)
- [drawings/ART-G12-40/v01/qa_black.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/qa_black.png)
- [drawings/ART-G47-04/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01/inputs/source_pose_guide.png)
- [drawings/ART-G47-04/v01/character_api_original.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01/character_api_original.png)
- [drawings/ART-G47-04/v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01/qa_white.png)
- [drawings/ART-G47-04/v01/qa_black.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01/qa_black.png)
- [drawings/OPT-BROOCH-PORTRAIT/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/OPT-BROOCH-PORTRAIT/v01/inputs/source_pose_guide.png)
- [drawings/OPT-BROOCH-PORTRAIT/v01/character_api_original.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/OPT-BROOCH-PORTRAIT/v01/character_api_original.png)
- [drawings/OPT-BROOCH-PORTRAIT/v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/OPT-BROOCH-PORTRAIT/v01/qa_white.png)
- [drawings/OPT-BROOCH-PORTRAIT/v01/qa_black.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/OPT-BROOCH-PORTRAIT/v01/qa_black.png)
- [drawings/ART-G51-01/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G51-01/v01/inputs/source_pose_guide.png)
- [drawings/ART-G51-01/v01/character_api_original.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G51-01/v01/character_api_original.png)
- [review/G51_01_latest_baseline/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/G51_01_latest_baseline/qa_white.png)
- [review/G51_01_latest_baseline/qa_black.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/G51_01_latest_baseline/qa_black.png)
- [drawings/ART-G12-39/v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-39/v01/qa_white.png)
- [drawings/ART-G47-03/v01/qa_white.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-03/v01/qa_white.png)
- [inputs/identity_full_drill_three_views.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png)
- [inputs/eye_G02-01_F100.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png)
- [review/G51_01_latest_baseline/eyes_diagnostic_x6.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/G51_01_latest_baseline/eyes_diagnostic_x6.png)
- [coverage/source_frames/F002154.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002154.png)
- [coverage/source_frames/F004584.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004584.png)
- [drawings/ART-G12-39/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-39/v01/inputs/source_pose_guide.png)

所有当前原图/QA/source/参考与JOB的精确SHA见JSON。G51使用review/G51_01_latest_baseline白黑QA，raw不变；历史v04报告不覆盖。取消双色试验未查看/采用。只写报告，没有生图、改画、中央账修改。当前实际摄影、道具接触、连续播放及用户/艺术验收均未验证。

