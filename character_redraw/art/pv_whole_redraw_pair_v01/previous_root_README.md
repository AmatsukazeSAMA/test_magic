# 魔术之心 · PV 人物重绘

当前阶段：正面 F2306、侧面 F2751、背面 F2362 的原 PV 换头合成已完成，并已评审为我满意的静帧预览候选。身体、肩宽、制服和动作沿用附件1；头部由 API `high` 绘制，再做显式平涂调色，裸露肤色按最初人物设定统一。尚无用户验收和动态验证。

![当前三向合成](art/20261030_pv_three_angles_v01/three_angles_character_overview.png)

当前选择见 `CURRENT_SELECTION.json`，完整文件、尺寸说明和[画风评估](art/20261030_pv_three_angles_v01/REVIEW.md)位于 `art/20261030_pv_three_angles_v01/`。各角度均有原尺寸整帧、4K 查看版、透明头层、原片底层与对照。4K 查看版的原片身体/背景由 1080P 放大，新头部直接使用 API 原始大图合成。

以下为过程中保留的旧候选和记录，当前预览以三向合成为准。

![当前正面合成](art/20261030_pv_F002306_head_composite_v01/pv_F002306_head_composited_1920x1080.png)

本轮一次 API 新生成原稿为 1536×2304、`high` 质量，原始返回保存在 `art/20261030_pv_F002306_v02/`。仅抽取头部合入原片，原身体和字幕保留；肩部排除新增卷发遮挡区后像素差异为 0。当前交付及[画风评估](art/20261030_pv_F002306_head_composite_v01/STYLE_REVIEW.md)位于 `art/20261030_pv_F002306_head_composite_v01/`。4K 查看版中的身体、背景和字幕由原片 1080P 放大，头部直接由本轮高分辨率 API 原稿合成。

![三视图候选 v01](art/20261030_maid_turnaround_v01/maid_turnaround_v01.png)

输入、提示词、请求参数、API 返回和视觉核对保留在 `art/20261030_maid_turnaround_v01/`。本轮使用已配置 OpenAI API，模型 `gpt-image-2.5-sunburst`，质量 `high`，共一次绘画请求。共享及本项目默认质量均设为 `high`。

原 PV 单帧试稿使用同一 API 和 `high` 质量，实际一次请求；候选、透明人物层、原字幕合成图和[画风评估报告](art/20261030_pv_F002306_v01/STYLE_REVIEW.md)保存在 `art/20261030_pv_F002306_v01/`。该用户授权意味着可进入单帧试验，不代替对人设、画风或批量制作的正式验收。

![原片与描改全身对照](art/20261030_pv_F002306_v01/comparison_character.png)

PV 服装参考来自 `D:\CODEX\手书素材\github_moshuzhixin_handoff\magic_maid_20261029\references\maid_outfit`，全部属于附件1原片；完整分段/字幕/特效交付在该交接仓库中。
