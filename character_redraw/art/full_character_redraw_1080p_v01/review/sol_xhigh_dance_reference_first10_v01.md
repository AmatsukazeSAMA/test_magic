# 10秒舞蹈参考：Sol xhigh 可见关系与交付笔记

**按原PV绘制态与真实曝光组织交付，不能把240个压缩帧当240张应付费重画稿。AI视频仅供头发摇晃。** 当前只是实际有序静帧/放大笔记，未连播、未验全240帧、未判动态通过。

- 实际看3页overview、R80..96邻帧页、R88原图/头肩crop、原F944crop与旧v01，以及R106/109/113；另看F834和R0。概览31时刻，加邻帧及额外样本共40个独立R时刻。
- F944旧v01把长卷盖在横过胸前的黑袖面前；R86/88/90附近可见灰卷位于耳颈侧，下部在白肩褶/黑前臂之后。这是前后遮挡问题，不能仅按固定长度比或收短尾巴来修。
- 概览有侧后转身、回正、手臂越胸等阶段，发束可见段和摆向随之变化。画到各态时须有原动作依据的藏入/再显露、压缩/回弹；不能每张都竖直挂胸前，也不能随机加长冒充弹跳。
- R106/109/113附近灰卷同样更贴耳颈/肩褶，旧39/40/41前置下垂的画法须按新基准复核；旧pilot和Round38比值仅保留历史，不作新终验门槛。

## 所有表演只服从原PV

头/身体/手的动作、姿态、表情、视线、服装、构图、曝光全部原PV权威。不可把AI手指、简化动作、面部漂移或偏白肤色补到源上。参考仅用于灰发的摇晃与遮挡关系，不能据此改演员。两珠、单股连续卷/自然隐藏要留，bob和卷统一无光照灰底+薄荷材质带+墨线。

## 资产与时序

规划元数据实际读取并数核为66行/66个stableID、300个不重叠源曝光帧，覆盖F834..1133；这不是66稿新画法的艺术验收。以这些源绘制态作为资产基础，确认同身体态中仍独立变化的发束相位后再登记变体；压缩/摄影/插值不自动新增画。原canonical采样/ID全部保留。共享全身G33母稿的首段半身放大使用必须独立注册，不能把全身位置或裁外腿带进首段。

新态首张仍API high，已有API稿按用户允许可内置imggen整体重绘；本代理不生成、不改registry。必须在真实源PTS上做1080人物层的实际时序/相邻发束验证后才谈动态。

## 时间证据边界

读取的音频对齐记录：参考t0≈PV27.828s，相关系数0.9969869594。F944=31.498s，对应候选R88=3.666667s；可见姿势另已实际检查。相关值不是本代理重新测量，也不保证所有生成视频帧都逐帧表演一致。R106/109/113是F966/970/975的音频邻近候选，不能按文件编号绑定。

若严格交付10.000s，原区间应为PTS `[445248,605248)`；F1133从604864开始，最后曝光保留24ms。若保留完整300源帧约10.010s。这里只记录时间算术，没有改ledger或导出。

## 实际看图与哈希

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/overview_01.png` — `408c5608ad16b23e37a03666a4bde21bd3fda5813010851d12cb6fcfbc5d7d73`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/overview_02.png` — `1494039f5284d4be4fb0af8f5a518215e3fa133399fdbac8b156b30a8653608a`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/overview_03.png` — `0f79f320b1e9b9439ea13d4c18c9bb52270a7ff5f89a6e6ede818f25589550f6`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/reference_neighbors.png` — `2b794db5cb3f7035c5a044cc818ee6faa8199d5f3104c10c8270d45f25274276`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000088.png` — `3ab879ad3f11b67e9cb8b6e9bd40554a1349dfca14f99ee64dc9b065c78e61c7`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/nearest_reference_hair_arm_crop.png` — `4833207fc06870d1451130f41d6abbd0a5efe635cd224c71544a003bf2bbfee5`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/original_PV_F0944_crop.png` — `896e13857c30d29a2298c71a43db2f3dad90bbfbc36ecaacda7212f5495c4fa5`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v01/qa_white.png` — `633c364bc1f8631f9a071ddfe01f5210897d0f2fbd5bc4a35fee2b28d4c09a32`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000106.png` — `738516587443e1f90323b424a013774a49658c0a16f30723820c79561f57b3e1`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000109.png` — `39c0cdf6eb485526a2da7b5535515dff9ea74d907fc8d98355aa552018681f5d`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000113.png` — `3761dc248abc978ec2e416a6dd098b29eeda62b2906d0919aeb6ff43ec22afca`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000834.png` — `8932bd2c964d5442f3b986f9eb285c7eb61069ff66b02cfe6950a12964ee9e72`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000000.png` — `8df21c4e4a3ae83ce7e79993842ee36c04787a34c396fb16beba7cc3588e65f3`

元数据：

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/REFERENCE_MANIFEST.json` — `b5298ca6cdec4f99f62a04bcd90d1b31acac4b1922804341e6681dde9ee71590`（核验期间主代理更新了role；已实际重读hair-only/PV-authority/time-boundary，旧记录哈希 `e085934328cf357107f2a6358c4cd6cd70b0fda2f227f89445ed48cc91653f62` 在JSON保留）
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/AUDIO_ALIGNMENT.json` — `303abec7f3fe89550af918e09b44b835373959419891a3a5e19d0fe23ae78f5a`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/FRAME_PTS.json` — `1a4bee66be83d1320830a354c4ac7c835a9a1b8d5d76b5fd3422017d31f9836f`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/data/original_timeline.json` — `07e94b9efda9e38d60b7812c6404ebfbe6acdc285f85b08d32f5204c75829698`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json` — `69eb6a739c2d1204e7d510ebf03860ff7ea54c37c39207a216d1e7f62facafe0`

所有结论保留静态/时序边界：用户接受、动态、逐曝光注册均未在此笔记中通过。

