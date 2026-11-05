# Sol xhigh 第38轮独立静态复核

实际看16张路径、读取2份JOB。**G12-41需修中下卷；G13-07保留静态候选。** 用户接受、摄影注册和动态验证均为false。

| 当前图 | 精确raw SHA256 | 结论 |
|---|---|---|
| ART-G12-41/v01 | `2b907a3cd8e466e55fc455936d92015623c93fb5e3750f449cd02370cfa164d3` | repair_required |
| ART-G13-07/v01 | `58771edeef1dd5992b60263eb7e4e13d6e0e61eda6381485b43acced2ff89d67` | retained_static_candidate |

## G12-41：P1，相邻中下卷拉长

- 当前raw：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/character_api_original.png`，1216×944；已实际打开当前guide及原尺寸F975 canonical。
- 本态转正头、右上眼神、波形闭笑、左低/右高双摊掌及当前指形、黑领红结/白围裙均保留。单色瞳/暖桃肤、两珠/两叶、头颈和两底边缘未发现另一个必须修的问题。
- 退修区约 **x734..826/y324..538**，重点中下段 **x740..812/y390..538**。已将40 whole_v02和41实际QA按近同头高并排：41根尾约326..535、bob顶88至下颊379，根尾/头高约0.72；40约401..594、bob顶165至下颊490，约0.59。尾低于下颊约0.54对0.32。
- 不是只用数字否决：实际图中41下段更拉开，细尾更垂向胸结中部，两稿都无臂/手遮尾。考虑珠根随转头移动后，仍存在可见的中下段长度/螺距不相容。未宣称多出某固定整圈或存在断段。
- 只修41当前中下卷/细尾，使其与40完整卷长度和体量相容；保留当前珠根位置、两珠、完整连续中段及细尾，不缩成小卷。不改当前脸/眼/口、双手和服装。按API局修→mandatory builtin whole→新双审。

## G13-07：保留静态候选

- 当前raw：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/character_api_original.png`，1040×1040。canonical仍为F1187，本次production为较宽F3637，已实际打开当前guide及native。
- 本态较正面头、睁眼短直闭嘴、左脸旁/右胸前两只摊指手及衣服/下裁保留，单色深灰瞳和暖桃肤合理。两红珠、一股足量灰薄荷卷、两叶帽与头颈连接自然。
- 实际看x695..875/y600..840的源/白/黑放大对照，约(746,668)处食指在前，肤色指尖/前缘完整，卷尾从其后进入遮挡，没有把手指接成头发或穿过手。不可用被挡的可见长度与06无遮挡全尾硬比，也不为露尖缩卷。手后隐藏尾形本轮不可见，不虚构或宣称已测定。
- 当前可见卷段/体量与06相容，原图及两底未见必须修复的实体残渣、透明缺损或拼缝。

## 实际看图与哈希

两份只读诊断仅在内存显示：G12近同头高并排（40 crop `[470,150,1020,700]`、41 crop `[435,80,933,578]`，各显示550×550）；G13手/卷源白黑ROI `[695,600,875,840]` ×2。不改图、不另存PNG。

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/inputs/source_pose_guide.png` — `a0806b5b1c068ca6e2a9cace32d1e6fb12db3ce63f8148316f4e61cc896c5263`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/character_api_original.png` — `2b907a3cd8e466e55fc455936d92015623c93fb5e3750f449cd02370cfa164d3`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/qa_white.png` — `fdb4033f3430854d79df0f6d947803322a61796b8f866acd9561bdae733c5b22`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/qa_black.png` — `c7cbed3365ee91c5bc498e9dd57e44667cf9896bed2ee53b0f2c3381fe24e02b`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/inputs/previous_head_continuity.png` — `f4b06140c079c8c2be9a52a830bb1716b7f607937e8eae5274306557c2dcc250`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/inputs/source_pose_guide.png` — `0c7d00846832c8413d4d1d8e2bb9eced896d5507d4097f6ef080eb4fb1fb2a87`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/character_api_original.png` — `58771edeef1dd5992b60263eb7e4e13d6e0e61eda6381485b43acced2ff89d67`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/qa_white.png` — `ee587f17dcf26f95b0b7ad6f8e2532bb2304b09673f1ae9da767a43f8bdcba7d`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/qa_black.png` — `ad00e287967c19859d3ef764384fe2ae9e2b1da8d450d0b47e3934528462628d`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/inputs/previous_head_continuity.png` — `4d35e9f8e7f498fe9f931b087e8eb966c0324cf8e02dc8f58df9b9b9cb0b94d5`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-40/v01/whole_imggen_v02/qa_white.png` — `e14c151534de57477bed0eb58ecdea5da2e78cc2ca813682e675d2e34a95775c`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-06/v01/qa_white.png` — `4ac9ba40bda6eaa626610f22abe32af2e0f0383f27f448befb85e93416d348d9`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png` — `c580f9ffe8d93ca121eccdae6f82d67fadcce18cfa72bd5322d8e9859380eaa1`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png` — `6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-41/source.png` — `ce76b95b9918360b1ccefac4abc868ca5755e7411f6decf0af494423f087d96a`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F003637.png` — `36228bf08d41cce0fc1fc8cee78b80c7da99e228238ec009d5aad379d563659f`

读取JOB：

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-41/v01/JOB.json` — `1cc65e9093bae9a553d530ab504b46c11b376400c96b932ce56a0c05bd526454`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G13-07/v01/JOB.json` — `7d01b2f2519ef59c6212677d8cc443362d1c8376e73372891bdfd3033c4b102b`

未把API成功/耗时或主审candidate当美术结论。只改本独立报告，未生成、未改素材/alpha/中央账；注册、连续播放和用户艺术验收均未验证。

