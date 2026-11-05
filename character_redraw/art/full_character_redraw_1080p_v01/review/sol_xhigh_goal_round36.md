# Sol xhigh 第36轮独立静态复核

实际查看15个图像路径，读取4份JOB/请求记录。两项均为 `retained_static_candidate`；无本轮必须修复项。用户艺术验收、摄影注册和动态验证均为 false。

| 当前精确稿件 | 原图SHA256 | 独立结论 |
|---|---|---|
| ART-G13-06 / v01 | `dc8229f8b42b187ccb5e4155ab4fc81faf5c792a12e62c05de986d479e92e2e2` | 保留静态候选 |
| ART-G12-40 / v01/whole_imggen_v02 | `2fc8ebce3da7001b3152c5f90003b2b75c6a5355eb35d35d1290769a9199be5e` | 保留静态候选 |

## ART-G13-06 / v01

- 当前原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/character_api_original.png`（944×1072）。canonical仍为F1185；本次实际结构参考为较宽F3634，已打开当前guide和1920×1080原帧。没有把canonical采样时间改成新首次曝光。
- 本态头倾、左上弯指/白袖口、左肘边裁和另一袖/围裙下裁保留。眼睛保持当前源较睁开的开合、单色深灰瞳及小白点，小弯闭嘴未被误改。
- 两红珠、灰bob及足量一股完整灰薄荷卷连接自然。与05完整稿实看卷根约y480/474、尾约y790/788，头高相近，无明显邻长跳变；这些坐标仅辅助定位。
- 白帽贴头、两黑叶、黑立领/红胸结/金件、白肩褶/围裙均保留。暖桃肤色和头颈连续；原图与白黑底未见需退修的实体残渣或拼缝。

## ART-G12-40 / v01/whole_imggen_v02

- 当前原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/character_imggen_original.png`（1423×1105）。本次只评新v02；已否决v01不再作为当前候选。
- 当前源的左低横摊掌、右高斜掌、头倾、睁眼及小弯笑口保留，没有照搬39的动作。黑立领/红胸结、白肩褶/袖口、围裙/后腰结与裁切保留，帽双叶/头颈连接无明显问题。
- 两红珠下是宽上卷、连续中下回旋和细尾。与39完整稿及本次preceding完整卷参考实看，旧稿明显拉长的中下尾已收回；视觉头高归一约0.60对0.64，相容，未见中段删失或缩成小弹簧。比例是辅助证据，实际圆厚卷形和连续性才是结论依据。
- 完整读取request与CHANGED_HYPOTHESIS：新请求唯一输入为完整API局修稿，撤掉多参考/15px延长假设。局修master raw本轮没有另开，不继承其PASS；本次新whole已从原图及两底重新判断。
- 原始透明RGB外部彩色表现未在正常白黑QA形成可见实体，不列为必须重绘问题；不宣称编码低alpha点已清零。

## 实际查看路径与证据

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/inputs/source_pose_guide.png` — `2d817cbd0193a98b81c9ae5e6246dba0878110517933bb9e6651b6e6e9da194a`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/character_api_original.png` — `dc8229f8b42b187ccb5e4155ab4fc81faf5c792a12e62c05de986d479e92e2e2`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/qa_white.png` — `4ac9ba40bda6eaa626610f22abe32af2e0f0383f27f448befb85e93416d348d9`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/qa_black.png` — `fb66b0a10284a6dab62869661486764aa10f9a7d9fd5395e3cbeb2fc84ea40c3`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/inputs/previous_head_continuity.png` — `ca64aa40b743b2616db36c814ed9c5315a3d85205058a609644a656bdbe0fc0e`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/inputs/source_pose_guide.png` — `2038d8c4e5a9f72670356e287b68c2ec56ad59005a6fa4350fdeaf2f7bfb84b7`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/character_imggen_original.png` — `2fc8ebce3da7001b3152c5f90003b2b75c6a5355eb35d35d1290769a9199be5e`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/qa_white.png` — `e14c151534de57477bed0eb58ecdea5da2e78cc2ca813682e675d2e34a95775c`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/qa_black.png` — `c884884835b3f3333ccb7e44b4d5d6ccea035e460bbb63ba0f6ba6d7ff8cadf3`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/local_coil_continuity_v01/preceding_complete_coil_reference.png` — `ca337fa2c8036e28fb77872c93818c378a25807666b8752665b9fa7c17346c4c`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-05/v01/qa_white.png` — `3d5069f5c3eeb4c36377883dc164a3d3489d13089a9267775722c05501587f41`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-39/v01/qa_white.png` — `f2df5e244b407ceb0c2731c0c89c5309d2b73c66b68d19ab6c390e7a5db20f68`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png` — `c580f9ffe8d93ca121eccdae6f82d67fadcce18cfa72bd5322d8e9859380eaa1`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png` — `6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F003634.png` — `93f349180ed789c6ef364d230993f52e218b95b1ebec7addf501fbbaca4a9d47`

读取的元数据/请求（不以文字代替看图）：

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/JOB.json` — `e0589a5da2ca1431e06ccd5a54ee0b59ee35a6994baeda348817f98948b96407`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/JOB.json` — `4a8a7f8b1c4751665895f5cf5338fd2494133e06db565d1457202f1637169d36`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/request_imggen.json` — `c37bc4564ccfab2ecc5bee50126edb0c3704337f1ad02ae0efaed6907889762b`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/CHANGED_HYPOTHESIS.json` — `adab238af768ae4087e77b0863d3fa161fb5c231f7027054facf545e5ddfd25a`

canonical源路径及JOB内源哈希在JSON逐项保留；本轮未另开canonical完整源图，已明确区分其记录证据与实际打开的current guide/native/reference。

这里只保留两张静态候选。未改中央注册、曝光账、生成图或alpha，未调用生成；1080摄影注册、特效接触、连续播放及用户接受均待后续。

