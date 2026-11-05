# GOAL 当前补充要求

全片目标与4763帧真实PTS、307项绘制及确需新增项的范围保持；GOAL继续进行。

- 钻发绘制以用户指定的 X01-01 钻发局部为基线，并结合两张圈数参考：空心、两大卷加一个小卷；宽灰发带连续翻回，绿色挑染为细材料边。
- 一条宽灰发带的正面、实际不透明灰返回、下一卷与小卷连续连接；不画封口盘、实心柱，不挖掉实体返回制造孔。
- bob与卷统一无打光灰色平涂，绿色挑染可细化为窄材料边。固定人物LEFT低耳后发根，侧背按真实遮挡，邻帧体量与摆动连贯。
- 用户指出的闭眼正面帧应垂直下垂；其他帧仍依原PV动作和摆动阶段。
- 高清保持原手书线宽起伏与简笔轮廓；明显独立装饰痣仍去除。按最新用户确认，示例同类紧邻眼角的细小短笔/小短点可以保留，不单凭微小像素间隔退修；保留眼线和睫毛。
- 所有已绘制稿的钻发先列待修改；旧图、旧评审及旧绑定保留，不自动沿用为新标准通过。
- **优先补未出首图**：官方API high，n=1，retry=1，新稿直接采用新钻发规则。旧稿核查和新绘并行。
- 现有图可imggen整体修复；任何局修或拼接后必须整体imggen，再由root与Sol xhigh实际看图。
- 静态复核、真实PTS绑定、原速慢速实际播放和用户艺术验收分别记录。默认不推送GitHub，不合成最终字幕、背景和特效。

此前“圈数不固定”及临时“三个等大圈”解释已被最新“两大卷加一小卷”更正取代。

官方API最新参数：**high，n=1，retry=1**；单个新请求最多追加一次临时错误重试，实际次数与响应证据逐次保留。

最新基线：用户明确“我是说钻发的绘制可以当基线”。X01-01 仅钻发画法获用户认可：统一空心两大卷加一个小末卷、连续宽灰发带的翻转连接与细绿色挑染。脸、眼睛、服装、整身比例和动作仍逐帧按各自原 PV 检查；当前头肩、透视和动作阶段决定钻发大小、方向、遮挡及上下摆动，不固定参考图的像素尺寸或轴角。该认可不包含整张人物、摄影或动态验收。

G49-01 钻发增量并改左肩前方的额外一次官方API全人物发型重绘已使用，返图保留为待修；根侧、肩前遮挡与体量仍未解决。本次额外授权已耗用，不追加该 API 重绘。

已定位的垂直下垂修正：G33-01，母帧2306，首舞曝光834–840；不套用到全片弹跳帧。

最新眼部容差：用户指向 G51-10 whole 的 EYES_white_5x 说“这种没事”。该图两处眼角小短点获准，停止仅为这些点重复重绘；其余人物、钻发、摄影和动态仍各自核查。正式证据：review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json。旧评审按当时要求保留，新评审引用本次更正。

最新少卷修正：用户对G13-19 whole（96c8998a）明确“少了一卷”，升级为待修P1。两大卷之后，必须还有具有自身灰正面与实际不透明灰返回的小末转，再收细为C形尖端；不能第二大转直接接一个钩就当作两大加一小，不按绿色边线或透明孔数计圈。各段是一条连续灰发带，实体返回不得挖空。补缺首图与本项修正并行。证据：review/USER_G13_19_MISSING_TURN_20261103_v01/USER_REJECTION.json。

最新直接API流程：用户明确无前后动作联系的新场景可以直接API绘制。先看本原PV及最少必要的人设/卷参考，即提交official high、n=1、retry=1；独立稿并行，返图后实际双审。无需等前一场景旧稿通过或先制作大份PREP/邻帧审计；连续动作帧才核必要前后衔接。已有缺陷保待修，继续补缺首图，不反复重绘阻塞其他独立新稿。未知旧调用仍先恢复，原图与自动回执保留。

最新背面肩前补充：用户明确“肩膀前，可以被遮住看不见一部分，但露出的部分大小得正常”。G49-01至G49-06保持解剖左侧低根，钻发位于左肩前；允许被头发或肩膀自然遮住一部分，无须强露全部两大加一小。露出的灰发带宽度、卷径和头肩比例必须正常，不能把整束缩小来藏住，也不能把整束挂在背面领布上来展示圈数。本次仅补充验收标准，不增加API次数；G49-01本轮新授权仍仅一次。证据：review/USER_REAR_FRONTSHOULDER_NORMAL_VISIBLE_SIZE_20261103_v01/POLICY.json。

最新正面肩前纠正：用户指出G48-06“说了这种纯正面的，钻发和原人设一样，放在正面前的肩膀上”。纯正面、无风场景的钻发像原人设一样垂在人物自身左肩的正面前方，按本镜头正常体量与发带宽度、卷径绘制。条带或近景裁掉肩部也不豁免：钻发应向颈侧和上胸内侧下行，超出画面下边缘的卷自然出画，允许只看见部分；不能为了展示两大一小把整束悬在脸侧外空白，不能缩小整束塞进裁切，也不能凭空扩出可见肩身。 G48-01至G48-06全部列肩前路线待核/待修改，旧静态评审保留历史且不自动沿用；G48-06当前外悬首图按用户否决退修。证据：review/USER_G48_FRONTAL_SHOULDER_ROUTE_REJECTION_20261103_v01/POLICY.json。

最新后发修正：用户提供upper_body_360_720p24.mp4和背面截图，明确“后发太乱，参考该视频”。后发以新360视频及后背截图为结构参考：短bob整体圆润紧凑，少量清楚的大弧形发束沿后脑下垂并向后颈内收；末缘仅少量自然短尖和轻薄短后颈层。去掉当前后脑/后颈多层交错长三角尖、锯齿链和炸毛外扩，不画成光滑硬头盔。转向按各自原PV头部投影保持，不镜像。该视频只新增后bob轮廓、发束分区、体量、后颈收束的几何依据；不借视频衣服、人体动作、曝光时轴、精修渐变或绿色高光。 当前先修G49-01代表稿；保留所有旧稿与评审，不自动将旧后发判为新结构通过。证据：review/USER_POSTERIOR_BOB_360_REFERENCE_20261103_v01/POLICY.json。

红珠连接最新补充：本体灰发/侧发根 → 双红珠扎结 → 空心钻发辫，灰发根须连续进入红珠扎结；红珠不是悬空饰物或耳饰。G49-01 v07已被用户指出与本体分离且偏实心，列为待修。本次新授权官方API一次对照原图修正，high/n=1/retry=1，保留肩前遮挡、正常体量和视频后发结构要求。

G49-01 v08用户返图否决：“首圈太小了”“并且画风似乎有偏离”。首圈恢复原人设正常大卷体量；保持本体灰发→双红珠扎结→空心灰辫连续。画风以原PV简笔黑线、平涂为准，减少连续渐变与规整发束弧线；新360视频仅供后发几何。v08列为待修改，当前一次官方API已返回，本轮没有追加调用。后续修正草案仅保存未提交。

最新参考图否决：用户指出731d95a9图“多了几个圈”。该图钻发列为卷数错误参考，不能整图进入后续绘制输入。若借用其简笔平涂/灰bob身份，须裁去整段旧钻发；钻发继续按空心两大完整卷＋一小完整卷再C，红珠连接本体灰发和辫根。本条不增加API调用。

2026-11-04最新用户范围：G26-04、G27-01、G28-01、G29-01保持各自原PV散发刘海/长度/轮廓/波浪/遮挡，仅参考图4灰色和薄荷绿配色；脸型、五官、原服装不变，不加bob/钻发/扎珠。白裙换衣试验已取消，保留弃用原图，不作新服装或胸针复用源。OPT-BROOCH-PORTRAIT从一张完成且核查合格的散发稿裁取复用，不是复用原PV红发头像，不单独绘制；复用源和实际绑定尚待完成。原307项/4763真实PTS范围保留，不把遮罩摄影阶段另生人物态。

### 2026-11-04 G33-32 head direction and gaze

User rejects whole v03: original PV head is oblique with eyes slightly toward the camera, not a front-facing head. Restore source head yaw/tilt, jaw-ear-nape, neck and collar relation with torso; preserve eye gaze separately. Current raw remains repair, not a baseline. G33-30/31 are adjacent checks, not automatically rejected for this new issue. Loose-hair sleep previews take priority. Evidence: D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01\review\USER_G33_32_HEAD_YAW_GAZE_CORRECTION_20261104_v01\USER_REJECTION.json

### 2026-11-04 Latest brooch and eye trial override

User: 还是尝试重绘吧. Brooch now gets one original-PV portrait redraw trial, preserving own face/gaze/loose shape/gray clothes with gray+mint palette. This supersedes reuse-only; G27 reuse crop diagnostics remain history. Four other loose recolor rules unchanged; no white dress. User eye reference is the LAST 96cc4117 image: palette only, no new center black dot or eye shape; one built-in trial, no official API for that last trial.

### 2026-11-04 All eye-black palette, exact protected shapes

Latest accepted eaa5a7f6 color only: dark-gray body/lighter lower gray, no central black dot. Every eye shape, opening, gaze, white glint, black eyelash/liner and non-eye-black area stays as the original drawing. Missing FIRST API drawings have this color from the start; no later API recoloring. Existing drawings color-only changes use no API, are queued after missing FIRSTs, and must preserve exact eye mask and every outside RGBA pixel. Reference: D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01\review\USER_ALL_EYE_BLACK_GRAY_PALETTE_ONLY_20261104_v01\POLICY.json

### 2026-11-04 Skin calibration after drawing work

User selects ART-G29-01 api_user_original_loose_graymint_visible_alpha_v05 skin colors only. Current API drawings need not match this skin color. Continue missing FIRST and required drawing work; only after all drawing work is done unify skin colors against the exact baseline. No global color edits now, no single HEX inferred, no whole-art acceptance. Evidence: D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01\review\USER_SKIN_BASELINE_G29_01_DEFERRED_CALIBRATION_20261104_v01\POLICY.json

### 2026-11-04 G06-04 inverted curl side

User rejects v05 viewer-right curl. This upside-down near-front source needs viewer LEFT while anatomical LEFT low-ear/nape root stays fixed. Do not mirror the body; do not reuse upright front-right mnemonic for an inverted head. Root-side repair queued; missing FIRST remains primary.

### 2026-11-04 G12-72 extra bead

User rejects the third small red bead/fragment above the two main beads. Keep exactly TWO joining main hair and drill at the same low anatomical LEFT root; no extra red/white fragment. Structural repair queued; do not use a color-only API call.
