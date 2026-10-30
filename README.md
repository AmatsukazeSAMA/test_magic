# 《魔法女仆》PV 拆解交接（2026-10-29）

## 最新重点：字幕、特效与 S 工作分包

用户明确优先需要**抠出字幕和特效，供后期合成**。本轮新增独立的软 alpha PNG 素材、全片逐帧时序与复用索引，并按连贯动作组织为 **15 个 s 工作包**；黑裙舞蹈及回归镜头统一在 **s06**，不是将 37 个 M 镜头机械改名。

- [字幕特效与绘制计划](magic_maid_20261029/字幕特效与绘制计划.md)：素材用法、导出、层序、工作量和限制。
- [字幕特效与复用工作台](magic_maid_20261029/字幕特效与复用工作台.html)：离线切换浅底/深底/棋盘格，查看每帧字幕、FX、来源与复用状态。
- [15 个 S 工作包](magic_maid_20261029/work_sections/README.md)：各包绘制任务、局部/原片帧、旧 M/G、复用曝光和素材索引。
- [复用与绘制任务说明](magic_maid_20261029/复用与绘制任务说明.md)：当前 **306 项制作任务 = 302 项线稿/局部改线 + 4 项仅校色**，含半身、头/手/嘴局部，**不是 302 张全身图**；可选胸针肖像另加 1。
- [原片裁切复用实证](magic_maid_20261029/data/crop_reuse_report.json)：49 对全部完成原片复核，**25 对纯裁切复用、4 对仅颜色差、9 对局部线差、11 对手势/姿态差**。只有25对整稿纯裁切从旧331项清单扣除；另22个未配对半身任务保留。附[独立抽查](magic_maid_20261029/data/CROP_REUSE_INDEPENDENT_REVIEW.json)、[未配对复核](magic_maid_20261029/data/crop_reuse_unpaired_review.json)、[其他全身编号候选复核](magic_maid_20261029/data/crop_reuse_gesture_alternatives_review.json)与[附件2说明核对](magic_maid_20261029/data/REFERENCE_REUSE_INSTRUCTION_CHECK.json)。
- [全片 alpha 清单](magic_maid_20261029/data/overlay_manifest.json)、[复用清单](magic_maid_20261029/data/reuse_manifest.json)、[独立最终检查](magic_maid_20261029/data/OVERLAY_DELIVERY_VERIFICATION.json)。

新的 `overlays/` 是从扁平原片估计的 straight-alpha 合成素材，**与下方上一版 `layers/` 的二值可逆像素分区不同**。请使用新版视觉报告和逐帧限制，不要用旧回合成一致性证明新素材语义正确。未恢复作者原始 alpha，未补画隐藏人物；两份源视频和旧交付保留。

[下载 16 个普通 PNG 序列包](magic_maid_20261029/overlay_sequences/README.md)（179.34 MB）与[独立棋盘格查看视频](magic_maid_20261029/renders/overlays_checker_preview.mp4)（6.39 MB）。全片两轨各 4763 帧，去重透明母资产共 2183 张；精确时序和部分缺字/遮挡限制随清单交接。

字幕按 **15 个语义 S 包**交付 ZIP，每包小于95 MB，完整黑裙舞蹈仍保留在一个 s06 包；特效另为全片 ZIP。包内文件与精确原片/局部 PTS 映射、实际文件清单和查看版说明见[字幕特效与绘制计划](magic_maid_20261029/字幕特效与绘制计划.md)。S 包的局部顺接只服务分工，不是改剪原片。原片字幕遮挡、部分投影和同色接触仍有明确限制。

## 项目背景与上一版可逆分区

用户要求基于附件1分段、拆绘制帧，以附件2中的逐帧示例和文字提醒为参考，后续将人物重绘并重新合成。**用户明确纠正：人物必须从附件1提取；附件2只用于参考拆帧和提醒。最终必须按附件1的时序把人物、字幕、特效和背景等合成回去。**

在原交接快照上，现新增 **411 个参考构图的可逆透明分层、全片逐帧分区/精确 PTS 回合成工具，以及独立的绘制态漏项审计**。结果和检查入口见下方及[本轮处理报告](magic_maid_20261029/分层与补帧报告.md)。

**这不是已经找回的干净原画。** 图层只保存附件1中实际可见的原像素；语义分界仍有待修项，遮挡下的身体/背景、原始半透明边缘未恢复，人物没有重绘。`source.png` 仍是原片完整合成画面。全层叠加与原片相同只证明没有改坏或遗漏像素，不能证明人物抠图正确。

此前助手曾提出从附件2提取人物，该方案已被用户明确纠正，不应继续执行。两份原视频和原有 `cels/` 均保持不变。

## 新增成果与复核入口

- [分层工作台](magic_maid_20261029/分层工作台.html)：下载/克隆后离线打开；411 个参考构图、1,398 张非空 RGBA 图层，可开关各层、对照原图、查看帧号/PTS/遮挡说明。原目录中的代表帧分布在31个工作段，**并非仅凭此页覆盖了37段全部曝光**。
- [代表构图分层清单](magic_maid_20261029/data/layer_manifest.json) 与 [独立像素完整性检查](magic_maid_20261029/data/LAYER_INTEGRITY.json)：原尺寸、原坐标、不重采样，图层有逐文件哈希与来源。
- [逐帧分区清单](magic_maid_20261029/data/frame_layer_manifest.json) 与 [逐帧绑定](magic_maid_20261029/data/frame_bindings.json)：每个原视频帧单独处理，不拿最近参考图或估计持帧替代原画。`frame_labels/` 是紧凑索引蒙版；恢复原片PNG后可导出任意帧的透明层。
- [独立语义视觉检查](magic_maid_20261029/data/layer_visual_audit.json)：覆盖37段实际原帧及高风险回归样本，列出残余遮挡、道具/人物混合、淡出及复杂排版问题；不以回合成测试代替语义验收。
- [补帧与候选查看页](magic_maid_20261029/drawing_candidates/index.html) 与 [绘制态覆盖审计](magic_maid_20261029/data/drawing_coverage_audit.json)：独立检查原片而非只数411张参考图；保留83张新增原尺寸源帧（3个确证漏态、2个边界样本、78个复用/遮挡未决候选），不把候选数当作新原画数。
- [补审完整性验证](magic_maid_20261029/data/DRAWING_COVERAGE_VERIFICATION.json)：重新从原视频解码，核对全部4763个RGB指纹、PTS、83张补审原图和关联证据；通过不等于证明所有作者原画已捕获。
- [全片查看副本](magic_maid_20261029/renders/all_frames_preview.mp4)：原PTS及原音频的回合成查看副本；有损H.264，不声称其RGB无损。[无损母版检查](magic_maid_20261029/renders/all_frames_lossless.verification.json) 和 [查看副本检查](magic_maid_20261029/renders/all_frames_preview.verification.json) 分别记录实际核验结果。大型无损母版不进入Git，可用下述命令重建。
- [最终聚合检查](magic_maid_20261029/data/PIPELINE_VERIFICATION.json) 与 [原生播放器检查](magic_maid_20261029/data/NATIVE_PLAYBACK_CHECK.json)：46项单元/集成测试、9项工作台自检和最终资产哈希通过；修正查看版BT.709标签后连续播放至尾帧。仍不代替语义美术验收。

## 先看哪里

下载或克隆本仓库后，打开 [`magic_maid_20261029/打开参考库.html`](magic_maid_20261029/打开参考库.html) 本地查看。页面包含两份视频的查看副本、37个分段、411个参考构图、教程文字提醒和开场曝光表。查看单个原片完整帧时，可在人物/参考图上打开原尺寸图。

- [拆解报告](magic_maid_20261029/拆解报告.md)：全片工作段、组别、教程提醒、复用与已知限制。
- [分段表](magic_maid_20261029/分段表.csv)：37段，按附件1的PTS；区间在CSV/JSON中采用左闭右开。
- [绘制参考清单](magic_maid_20261029/绘制参考清单.csv)：附件2参考340张，原片补充71张，共411个**参考构图**，不是411张独立人物原画。
- [素材索引和来源记录](magic_maid_20261029/data/panel_catalog.json)：每张参考的原片帧号、PTS、文件、哈希及匹配说明；`cels/<编号>/source.png` 来自附件1，`reference.png` 来自附件2。
- [原片逐帧时间表](magic_maid_20261029/data/original_timeline.json) 与 [逐帧索引](magic_maid_20261029/data/frame_index.csv)：视频帧0–4762，时序以原PTS为准。像素曝光可逐帧回放，但不能据此宣称已确定全片作者原画身份。
- [开场曝光核对](magic_maid_20261029/开场曝光核对.csv)：F9–F169，共5个可见人物态、26段连续曝光；不能将这一段的持帧数推广到全片。
- [分段视频](magic_maid_20261029/clips/)：M00–M36，720p、带原声；全数加起来4763视频帧。
- [原始视频副本](magic_maid_20261029/source/)：`original.mp4` 是附件1，`reference.mp4` 是附件2；保持输入文件的字节副本。
- [参考总览](magic_maid_20261029/sheets/) 与 [分段总览](magic_maid_20261029/sheets/分段总览_01.jpg)：用于快速定位。F4021只持续1个视频帧，但与F4022腿和裙摆不同，保留为 X01-01。

## 制作边界与后续工作

1. 以附件1为唯一人物像素来源。当前分区已分开可辨认的人物、字幕、特效、背景/道具，并单列 `unresolved_visible`；仍须依据视觉审计修正复杂接触和遮挡，不能把剩余像素随意称作干净背景。附件2仅用于核对动作编号与提醒。
2. 字幕、花瓣、幽灵线、橙色转场等遮住人物时，优先检查附件1中同一人物态是否在其他时刻露出相应位置；只有能确认同一画稿时才用作补足。无法在附件1证实的部分标记为遮挡/待修，不能称作找回了原稿。
3. 根据用户**后续提供的人设要求**重绘；本轮不擅自采用其他项目的人设，也没有重绘人物。同一原画的重复曝光只在证据足够时复用，确实不同的动作或重描分别保留；人物、道具和镜头变化不要混算。
4. 当前回合成是原像素/时间轴诊断，不是重绘后的成片。替换人物后仍须重新检查首尾、快速切换、复用、文字/花瓣遮挡、转场和声音同步，不能沿用本轮完整性通过记录当成新稿验收。

## 便携处理与复现

新工具不依赖原电脑的绝对路径。需要 Python 3.11+、FFmpeg/ffprobe（HEVC解码、libx264及libx264rgb编码），并安装固定版本依赖；本轮实测 Python 3.12.14、FFmpeg 7.1.5。以下均在仓库根目录执行：

```sh
python -m pip install -r requirements-layers.txt
python scripts/magic_maid_timeline.py validate
python scripts/magic_maid_timeline.py extract
python scripts/verify_layers.py
python scripts/magic_maid_drawing_audit.py verify
python scripts/magic_maid_layer_viewer.py
python -m unittest discover -s tests -v
python scripts/magic_maid_layer_viewer.py --self-test
```

恢复 `frames/` 后，导出指定视频帧（输出必须是新目录；示例 F4021 是原片仅出现1帧的独立姿态）：

```sh
python scripts/magic_maid_frame_layers.py export-frame 4021 --output magic_maid_20261029/exports/F004021
```

只需要某个未决绘制候选的原尺寸完整帧时，可以直接从保留的原视频取出并核对RGB，不必先解码全部帧：

```sh
python scripts/magic_maid_drawing_audit.py materialize 1247 --output magic_maid_20261029/exports/original_F001247
```

从已提交的逐帧分区重建无损诊断母版，再生成查看副本（已有同名输出时会拒绝覆盖，先另选路径或保留旧版）：

```sh
python scripts/magic_maid_timeline.py render --layers magic_maid_20261029/data/layer_manifest.json --frame-layers magic_maid_20261029/data/frame_layer_manifest.json --output magic_maid_20261029/renders/all_frames_lossless.mp4
python scripts/magic_maid_timeline.py preview magic_maid_20261029/renders/all_frames_lossless.mp4 --output magic_maid_20261029/renders/rebuilt_preview.mp4
```

若要重新运行分区算法而不改动交付图层，请使用新输出目录/清单：

```sh
python scripts/magic_maid_layers.py --output layers_rebuilt --manifest data/layer_manifest_rebuilt.json
python scripts/magic_maid_frame_layers.py build --output frame_labels_rebuilt --manifest data/frame_layer_manifest_rebuilt.json --workers 4
```

生成失败留下匹配的 `.partial.json` 时，可在**输入、算法、路由及输出目录未改动**的前提下加 `--resume` 继续；检查点逐文件校验，不会把旧算法的蒙版冒充新结果。

## 仓库范围和恢复

仓库包含两份原视频、411组对应的原片截图（以及有附件2参考时的参考图）、37段查看视频、6张教程提醒、分层图像、索引蒙版、补帧证据、清单和脚本。全套原尺寸附件1视频帧 `frames/F000000.png`–`F004762.png`、完整附件2抽帧、大型 `.npy` 缓存和大型无损诊断母版不上传；用已保留的原视频和新工具重新生成。历史文档中的 `D:\CODEX\手书素材\magic_maid_20261029` 只是原交接环境，不是新工具的必需路径。

`打开参考库.html` 使用仓库包含的精选原帧；没有上传全部逐帧图时，它会跳到最近的可用参考帧。`index.html` 是完整版工作台，需先恢复全部附件1原尺寸逐帧图。报告和旧校验记录描述的是本机完整工作目录，并非宣称仓库已经包含所有缓存或逐帧图。

恢复全部附件1原尺寸帧的一种方式（将 `ffmpeg` 换成实际可用、支持HEVC的可执行文件；在仓库根目录执行）：

```powershell
New-Item -ItemType Directory -Force -Path .\magic_maid_20261029\frames | Out-Null
ffmpeg -i .\magic_maid_20261029\source\original.mp4 -map 0:v:0 -an -vsync 0 -start_number 0 -compression_level 3 .\magic_maid_20261029\frames\F%06d.png
```

应得到4763张1920×1080 PNG；更推荐上面的 `extract` 命令，它先核验源视频且拒绝覆盖不完整旧缓存。历史整理脚本仍可能包含原电脑绝对路径并重写旧索引，请勿与新便携工具混淆。原交接快照可从Git历史恢复；本轮没有改写原视频或原有参考PNG。

## 核验与边界

本机完整工作目录的 [验证结果](magic_maid_20261029/data/VERIFICATION.json) 记录两份源文件哈希、4763帧、751张原尺寸参考图、37段视频帧数和音频等检查；[浏览器检查](magic_maid_20261029/data/BROWSER_CHECK.json) 验证过分段、参考检索、预览播放与便携页。两份记录是该次本机验证结果，不能替代对新分层与回合成结果的检查。尚未恢复作者工程或透明原始图层，没有生成或补画人物，也未取得用户对绘画成品的验收。

输入校验 SHA-256：

```text
original.mp4  ec5e207ae3ef97da5a7866bfcaed3b23216dcc828bc87be72668e66533038cc1
reference.mp4 fe3031cd98c5488949f26194e503d41ba966e8261e1c8a280686e90651aad498
```
