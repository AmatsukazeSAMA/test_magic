# 魔术之心 · PV 人物重绘

当前入口为 **F1501、F1647、F1666 三张完整人物重绘候选**。F1647 使用已配置 OpenAI API、质量 `high`；F1501 和 F1666 按用户要求使用内置 imagegen。内置工具没有公开模型及质量参数，工程记录保留这一区别。

**眼睛画法以 F858（ART-G12-10/v01）为基准**：黑色上眼线、深灰虹膜、简洁灰色下缘和小白高光。只沿用画法，各帧的睁眼程度、表情及视线仍取自相应原 PV 帧。基准及后续默认规则见 [image_defaults.json](image_defaults.json)。

| 帧 | 透明生成原图 | 1080P 人物层 | 定位预览 |
|---|---|---|---|
| F1501 | [imagegen v02](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1501_character_original.png) | [RGBA](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1501_character_1920x1080.png) | [预览](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1501_1080P_position.png) |
| F1647 | [API high](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1647_character_original.png) | [RGBA](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1647_character_1920x1080.png) | [预览](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1647_1080P_position.png) |
| F1666 | [imagegen](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1666_character_original.png) | [RGBA](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1666_character_1920x1080.png) | [预览](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/F1666_1080P_position.png) |

![三张整体重绘对照](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/whole_character_review.png)

三张均为一次生成的完整人物，交付原图保持生成文件字节；1080P 人物层仅对整个人物统一缩放、平移。原片字幕、特效、背景及独立道具留待后期合成；粉色定位图用于查看人物位置，不是完整 PV 合成成片。

已按要求由 **Sol xhigh** 独立静态复查。F1501 v02 已恢复原帧较睁开的回望眼神；三张当前未见需要再次整体重画的明显服装、发型、头饰漂浮或头颈接缝问题。当前结论是静态候选，相邻曝光连续性及最终场景注册尚未验收。详见[独立复核记录](art/full_character_redraw_1080p_v01/review/sol_xhigh_whole_redraw_v03.md)。

全片任务仍在进行：已知工作计划共 307 项，其中主要人物工作 306 项、附加肖像 1 项；另有 1929 个原片曝光帧的归属尚未解决。任务及逐次调用记录见 [PROGRESS.json](art/full_character_redraw_1080p_v01/PROGRESS.json)。这三张返修不代表全片完成，当前未记录用户对新稿的艺术验收。

先前被否决的拼头、头饰补丁和旧候选保留为历史，不再作为这三帧的当前版本。最新文件入口见 [CURRENT_SELECTION.json](CURRENT_SELECTION.json)，本轮原图哈希、提供方及定位方法见[交付索引](art/full_character_redraw_1080p_v01/whole_character_restart_v01/delivery/INDEX.json)。本次更新前的工程入口保存在 `art/full_character_redraw_1080p_v01/whole_character_restart_v01/previous_project_entry_20261031/`。

原 PV 及分段工程位于 `D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029`，属于附件 1；附件 2 仅用于拆解参考。
