# Sol xhigh 现有候选重新审核 v04

2026-10-31 03:26（Asia/Hong_Kong）。本轮重新实际查看 PROGRESS.json 中指定的 11 张 reviewed_candidate 当前原返图、各自白底 QA 和原 PV，另查看 G18-01。每张均重新看图，没有沿用旧 review 代替观察。只写本审核文件，没有改画稿、计划或 PROGRESS，没有调用生图接口。

用户最新要求已纳入：**G02-01/F100 的眼形、眼线、神态优先于此前 F858；后续尝试单色深灰虹膜并保留小白高光。眼睛开合、朝向和表情仍随每帧原动作，不全改半闭眼。** 用户只指出这张眼神较好，同时明确否定其偏小钻发；G02 整稿未获接受，不能充当完整母稿。单色眼仍是后续试验，尚未被用户选定为新成稿。三视人设与用户侧后脑图负责钻发体量和结构，原 PV 负责该帧服装、动作、头饰和裁切。

本轮指定 11 张中：6 张可保留为静态候选，5 张 needs_repair；额外 G18 也 needs_repair。**这些不是用户验收数量，也不是动态通过数量。**

| 稿件 | 本轮当前目录 | 判断 | 实际发现 | 建议 |
|---|---|---|---|---|
| ART-G01-01 / F9 | drawings/ART-G01-01/v02 | needs_repair | 近景钻发被缩成细短的两三卷小尾巴，灰 bob 与钻发的体量关系明显小于最初三视图；不能以完整收进画面替代正常发量。 | 保留脸、手和原灰衣构图，用 API 局修把钻发上部体量恢复到人设比例；允许下段被肩衣遮住或出画。失败再整体重画，不手工拼头。 |
| ART-G02-01 / F100 | drawings/ART-G02-01/v01 | needs_repair | 用户已明确指出本张钻发太小。眼睛偏好仅针对眼形、眼线和神态，整张画稿与小钻发均未被认可。 | 按主代理安排用 API high 整体试绘：保留 G02 的眼形/眼线/神态，以单色深灰虹膜和小白高光试验，同时恢复三视图的正常钻发体量；不推广半闭眼到其它帧。 |
| ART-G09-01 / F752 | drawings/ART-G09-01/v01 | needs_repair | 钻发有连接和卷尖，但整体相对大头偏小、偏短，珠下很快收成小尾，未保持最初人设的长钻发体量。 | 仅针对灰/薄荷钻发恢复较宽上卷和较长连续中段；保持本帧圆睁眼、嘴形与灰衣，不改成女仆服。 |
| ART-G11-01 / F784 | drawings/ART-G11-01/v01 | needs_repair | 返图在下缘增加黑高领和红胸结，盖掉源帧本应可见的裸颈；右上新增黑双叶饰也无本帧源依据。已直接核对 source_pose_guide 与 source_character_crop，不能把通用女仆参考套入该近景。 | 先用 API 局修去掉无依据的黑领/红结与新增黑饰，恢复源裸颈和该近景裁切；若局修使头颈不连贯，再整体重画。 |
| ART-G12-10 / F858 | drawings/ART-G12-10/v01 | retained_static_candidate | 半闭眼是本源帧真实表情；女仆服、胸结、双手、头饰、两珠及连续单钻发成立，颈领未见明显接缝。 | 保留静态候选；F858 只作为此前眼睛基准，后续眼样试验优先按新 G02 要求。不得把 F858 的半闭眼复制到其它动作。 |
| ART-G13-01 / F1175 | drawings/ART-G13-01/v01 | needs_repair | 钻发相对头部偏细短，中段过快变细并在肩上收尖，体量不足；双珠和侧向虽正确，不应沿用为正常发量母型。 | API 局修钻发的宽上卷与连续中段长度，保持头部、衣服、手势和源眼态；若带坏肩/发根连接，再整体重画。 |
| ART-G15-01 / F1417 | drawings/ART-G15-01/v01 | retained_static_candidate | 坐姿上身、微笑、托颊手和握杯柄手势与源基本一致；黑白女仆服和红胸结正确。帽饰贴合，两珠侧向正确，单钻发连续。茶杯、桌椅单独合成不属于人物漏画。 | 保留静态候选，后续核手与独立杯柄的实际接触和遮挡，不为缺少独立道具否决人物层。 |
| ART-G33-01 / F2306 | drawings/ART-G33-01/v01 | retained_static_candidate | 闭眼符合源，不能为套新眼样强制睁眼。黑白长袖女仆服、白围裙、下垂可见手、略错开的双脚关系均与源相容；帽、颈领和单钻发完整。 | 保留这张 v01 静态候选，不与此前缺腿的 G33-03/04/05 v02 混淆；后续按真实曝光检验相邻手足动作。 |
| ART-G33-02 / F2312 | drawings/ART-G33-02/v01 | retained_static_candidate | 睁眼、向左伸的弯肘前臂及另一手下垂、双脚位置、黑白女仆服和围裙均与源基本一致；两珠和完整单钻发位于正面画面右，头饰贴合。 | 保留静态候选；未来单色虹膜试验保留本帧睁眼状态，不能借机冻结为其它 G33 动作。 |
| ART-G36-01 / F2751 | drawings/ART-G36-01/v01 | retained_static_candidate | 向左侧脸、双手在身后、白围裙及背后系带、露肤腿与黑系带鞋符合源；灰 bob、双珠与单钻发在侧后方，帽和颈领连贯。 | 保留静态候选。侧眼很窄，按源透视保留，不把正面 G02 虹膜宽度硬塞入侧眼。 |
| ART-G51-01 / F4584 | drawings/ART-G51-01/v01 | retained_static_candidate | 本源是红色短袖女仆服、黑胸结、白短围裙与黑长袜/鞋，返图保留了这些差异；不得统一改成长袖黑裙。双手与腿的前后关系基本相容，灰 bob、双珠和单钻发侧向正确，帽领连贯。 | 保留静态候选，后续按源红制服组做时序检查；钻发体量母型仍用最初三视图，不能反向用本远景小图定尺寸。 |
| ART-G18-01 / F1549 | drawings/ART-G18-01/v01 | needs_repair | 钻发在双珠之后很快收成短小的几卷，明显比最初三视图的长钻发细短，应随本轮正常发量方向修正。 | 保持源脸/服装/动作，用 API 局修恢复钻发较宽上部与完整长中段；若破坏头肩整体再整图重画。原 returned_needs_review 状态不能当作用户已接受。 |

近景钻发问题要按正常人设发量修：不要为了在画布内露出完整卷尖而把整条钻发缩小。可以按真实头肩遮挡留下画外段或被衣物遮住的段；不应移动脸、手或源构图来勉强塞发。G01/G09/G13/G18 的修复可先做 API 局部重绘候选；G02 按主代理最新安排做 API high 完整试绘。G11 是本源近景不该出现的女仆领／胸结／黑饰，先局修这些无依据部位，失败再完整重画。这里的局修指真实绘图编辑，不是把独立头部、帽子、身体重新拼接。

源帧已经闭眼的 G33-01 保持闭眼；G09、G11 等圆睁眼帧保持圆睁眼；G36 保持狭窄侧眼。新的 G02 眼样不能覆盖这些真实动作差异。G51 的红短袖制服与长袜是该源正确信息，不能为了统一母型改成黑长袖裙。G15 不带茶杯/桌椅是人物与道具分层，不属于漏画；实际杯柄接触仍待后期验证。

本轮实际看过的逐项输入路径如下（每项另共同对照新旧眼样和最初人设）：

- **ART-G01-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G01-01/v02/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G01-01/v02/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G01-01/source.png`。
- **ART-G02-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G02-01/source.png`。
- **ART-G09-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G09-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G09-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G09-01/source.png`。
- **ART-G11-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G11-01/source.png`；另看：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-01/v01/inputs/source_pose_guide.png`、`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-01/v01/inputs/source_character_crop.png`。
- **ART-G12-10**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-10/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-10/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-10/source.png`。
- **ART-G13-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G13-01/source.png`。
- **ART-G15-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G15-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G15-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G15-01/source.png`。
- **ART-G33-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-01/source.png`。
- **ART-G33-02**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-02/source.png`。
- **ART-G36-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G36-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G36-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G36-01/source.png`。
- **ART-G51-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G51-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G51-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G51-01/source.png`。
- **ART-G18-01**：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G18-01/v01/character_api_original.png`；`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G18-01/v01/qa_white.png`；`D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G18-01/source.png`。

共同实际查看的参考：

- 新眼睛优先参考：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v01/qa_white.png`。
- 此前眼睛参考：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-10/v01/qa_white.png`（原返图也已查看）。
- 钻发体量：`D:/CODEX/魔术之心/art/20261030_maid_turnaround_v01/inputs/identity_turnaround.png`。
- 侧后脑构造：`D:/CODEX/魔术之心/art/20261030_braid_revision_refs/user_side_back_hair.png`。

F1501 v02、F1647 和 F1666 的完整新稿沿用 v03 已记下的静态候选结论，本轮没有重新查看它们，也没有选回被否决的拼接稿。未来单色眼试验若获选择，再评估其余候选是否需要眼部统一；本报告没有仅因旧稿有多层灰虹膜就全部判坏。

本轮未检查相邻曝光播放、全片动态、1080p 最终注册及道具接触。没有把技术检查、HTTP 状态或哈希当作艺术通过。PROGRESS 原有状态只是本次输入定位信息，所有候选均未由本报告获得用户接受或正式采用。

