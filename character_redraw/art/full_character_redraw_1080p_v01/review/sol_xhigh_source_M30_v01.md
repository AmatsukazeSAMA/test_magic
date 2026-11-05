# M30 原片可见态独立复核

2026-10-31；Sol xhigh。已实际看全部5页逐帧联系图、8张canonical原图及9张native原尺寸，另看3张当前生产guide。只写本审核，未改主账/计划/registry/素材，未生成。

76帧中，24帧有人物、52帧无人；保留G47的8个既有状态，0新增、0待近看。11段包括同06态在F4294新增第三实例的边界。上/中/下框可共用各自当前状态资产，逐实例注册；8态之间不机械合并。

**生产输入须先隔离**：8个canonical均是PV整帧。实开01/04/07的guide分别含大空白/字幕、2个或3个头像。不要把它们当单个人物或干净alpha输入。另提取每态上框较无遮挡人物参考；保留原source、旧guide和采样证据。白卡、黑框、字幕、花瓣独立，按卡框裁切，不补框外身体或缩小钻发来露尖。

## 逐段区间（首尾均包含）

| 区间 | 帧数 | 结论 | canonical | 实例数 | 实际观察 |
|---|---:|---|---|---:|---|
| 4261..4279 | 19 | confirmed_no_visible_character | — | 0 | 粉色底、纵排文字/花瓣，未见人物；不能将字幕或花瓣视为待绘人物。 |
| 4280..4280 | 1 | confirmed_binding | ART-G47-01 | 1 | 单上框，闭眼；刘海与两侧发梢为01态。 |
| 4281..4284 | 4 | confirmed_binding | ART-G47-02 | 1 | 单上框，闭眼；刘海偏转和耳侧/卷轮廓较01重描。 |
| 4285..4285 | 1 | confirmed_binding | ART-G47-03 | 1 | 单上框，闭眼；斜刘海、颊旁长尖发梢与前两态不同。 |
| 4286..4288 | 3 | confirmed_binding | ART-G47-04 | 2 | 第二框F4286已出现；上下为同一04半开眼态，中框字幕遮挡独立。 |
| 4289..4292 | 4 | confirmed_binding | ART-G47-05 | 2 | 上/中两框同为05；不是将04的摄影位移另列。 |
| 4293..4293 | 1 | confirmed_binding | ART-G47-06 | 2 | 06圆睁眼首次出现，仅上/中两框。 |
| 4294..4294 | 1 | confirmed_binding | ART-G47-06 | 3 | 第三框首次出现，三框同为06；实例数增加，不新增绘制ID。 |
| 4295..4299 | 5 | confirmed_binding | ART-G47-07 | 3 | 三框同为07圆睁眼；首次4295，比canonical4296早1帧。 |
| 4300..4303 | 4 | confirmed_binding | ART-G47-08 | 3 | 三框同为08圆睁眼；首次4300，比canonical4301早1帧。 |
| 4304..4336 | 33 | confirmed_no_visible_character | — | 0 | 仅红色心形图标的转动/缩放、白色文字和花瓣，未见人物；心形不是人物。 |

## 采样与首次可见分列

| ID | canonical采样帧 | 本章首次可见 | 可见态依据 |
|---|---:|---:|---|
| ART-G47-01 | 4280 | 4280 | 单上框，闭眼；刘海与两侧发梢为01态。 |
| ART-G47-02 | 4281 | 4281 | 单上框，闭眼；刘海偏转和耳侧/卷轮廓较01重描。 |
| ART-G47-03 | 4285 | 4285 | 单上框，闭眼；斜刘海、颊旁长尖发梢与前两态不同。 |
| ART-G47-04 | 4287 | 4286 | 半开眼，沿03的斜刘海/颊旁发梢构型；与03闭眼分开。 |
| ART-G47-05 | 4289 | 4289 | 半开眼，刘海、耳侧及帽黑叶倾角较04改变；保留独立05。 |
| ART-G47-06 | 4293 | 4293 | 圆睁眼，头发构型近05但眼开合明显改变；与05分开。 |
| ART-G47-07 | 4296 | 4295 | 圆睁眼，刘海回到接近01的构型；不能与闭眼01合并。 |
| ART-G47-08 | 4301 | 4300 | 圆睁眼，刘海偏转至接近02的构型；不能与闭眼02合并。 |

## 实例和原尺寸定位

| 实例 | 可见区间 | 曝光帧数 | 近似ROI（xyxy） |
|---|---|---:|---|
| M30.card.top | 4280..4303 | 24 | 728,24,1205,356 |
| M30.card.middle | 4286..4303 | 18 | 728,380,1205,713 |
| M30.card.bottom | 4294..4303 | 10 | 728,730,1205,1062 |

24+18+10=52次头部实例曝光，不是52份画稿。原尺寸逐框对照眼、刘海、耳侧、红领和白肩，同帧各框共用当前态。中框的白「バイ」跨脸/发，下面框偶有花瓣遮挡；这些是前景。ROI为近似定位参考，不是精确mask或已验证变换。04首次4286（canonical4287），07首次4295（canonical4296），08首次4300（canonical4301）；canonical来源全保留。

F4261..4279仅文字/花瓣。F4304..4336只有红心图标、文字与花瓣，红心旋转/缩放不算人物。

## 实际打开的图及SHA256

以下逐项均实际调用view_image打开。其余章节native在联系页逐格看过，没有声称全部单张原尺寸打开。全部indexed源文件、INDEX和计划的精确SHA另在同名JSON的evidence_files中。

**联系页**

- [coverage/review/M30_all/page_01.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M30_all/page_01.png) — `3cba4f02b7a70d158151826928051f85b7c6736091d6b10bf9c5cae06170441f`
- [coverage/review/M30_all/page_02.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M30_all/page_02.png) — `750f47929c0891929a83c761cd9b1c2255c640951a37e93d37f4be25db399bab`
- [coverage/review/M30_all/page_03.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M30_all/page_03.png) — `c4d1a918a85ffd63662db600a4a8455be9c238a5116dde28873e1de865030c27`
- [coverage/review/M30_all/page_04.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M30_all/page_04.png) — `7078727dd75407dc55d2671799add459c4fddbd66c3d1be47b4081b0179ca999`
- [coverage/review/M30_all/page_05.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M30_all/page_05.png) — `62028814d66d9577bcef5e9c618722396292f28a9dee23bb501b45ee7f6e6ddb`

**canonical原图**

- [magic_maid_20261029/cels/G47-01/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-01/source.png) — `9ba9dc1afdc25b60891f97c18c8bb5d2a6e0b6a93ab37635ba651374853ec4ee`
- [magic_maid_20261029/cels/G47-02/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-02/source.png) — `dc2819faa0ba4655adfcb1da5c7a350a4d3d4ea751c75ea2732cf90138ae1ceb`
- [magic_maid_20261029/cels/G47-03/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-03/source.png) — `cb821b96437a3c7b84428d0b711aa0ce2a936c81b4f0d8df71170fcb7da1e063`
- [magic_maid_20261029/cels/G47-04/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-04/source.png) — `3ddafb621667688b650dc6e88d2356a387b862483f7b688070da9eb7838ca5fc`
- [magic_maid_20261029/cels/G47-05/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-05/source.png) — `3117cdb870509a3aef2819880546c4bc5ad0c966c30195475b797879e7d32354`
- [magic_maid_20261029/cels/G47-06/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-06/source.png) — `4e2aef1060427c3f5e2d25cf45a21e6a7447ec743464607684f50c9179bf9181`
- [magic_maid_20261029/cels/G47-07/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-07/source.png) — `f8547d62f42a08c157663bf6f54420692ec9bf4d79510b6aee06b84301b65392`
- [magic_maid_20261029/cels/G47-08/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G47-08/source.png) — `a4bfc0eda2f90fb042eb840b96c797cb8c567c23260d4dc5a10b3a91ec18b1ec`

**native原尺寸**

- [full_character_redraw_1080p_v01/coverage/source_frames/F004286.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004286.png) — `268cb7d6b2f8c2a7e68e3380cc8eb2f3fa814a3f153d5ef4a19e9386f4116bec`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004294.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004294.png) — `544b3c7eaf24adf358c77f599571215c6eccced7bf7bc5b50195fd25786eb184`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004295.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004295.png) — `9d171804e5b840b13293dd312406bade892da89794b326cbdc810c3ffbc149d1`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004300.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004300.png) — `e6346dc51e144e854d3accaebf1d611de89571f2e4733f0a9fa306823a7e8965`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004279.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004279.png) — `76286620b83ce51dda2a835a8cc716669d118b0ad167b471d1c192e64849a4a4`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004303.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004303.png) — `b4e343ba2471a4d521964fbd6746b6c73f66373efb50530083b2792e2052fc61`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004304.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004304.png) — `5dd10b72f5becbd00a44a8a05619acaac48caa15dc5de49dde7383624ab800b1`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004336.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004336.png) — `caae8c8b29902eeffeef5386ea1808abf435367f205559cb1f94b5b12053945f`
- [full_character_redraw_1080p_v01/coverage/source_frames/F004280.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F004280.png) — `9ba9dc1afdc25b60891f97c18c8bb5d2a6e0b6a93ab37635ba651374853ec4ee`

**当前guide**

- [ART-G47-01/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-01/v01/inputs/source_pose_guide.png) — `3f70c65de350c27b794f7b6146d829d2463283c5c2ad1607567a34e17ce380aa`
- [ART-G47-04/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-04/v01/inputs/source_pose_guide.png) — `e044815f8583a28adc3fdc611ed9939b860f01c67eb29ae21124923c15293a2c`
- [ART-G47-07/v01/inputs/source_pose_guide.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G47-07/v01/inputs/source_pose_guide.png) — `1d42f7d38930ce32abe0819eaf7288f15d20cc87224e51ebc2e9b2f9f1e088f4`

## 范围与未验证内容

本结论只覆盖本章原片可见态归属，不考古隐藏cel。没有精制字幕/花瓣/卡框mask；没有验证生成图、最终摄影注册、动态、道具接触或用户艺术验收。`dynamic_validated=false`、`user_accepted=false`、`generated_artwork_passed=false`。

待生产处理：隔离G47单框人物参考和多实例注册；这不是源状态不明，也没有为实例数增加而申请新绘制ID。

