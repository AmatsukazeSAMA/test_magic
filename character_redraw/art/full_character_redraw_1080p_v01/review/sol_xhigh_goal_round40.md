# Sol xhigh 第40轮：G12-34/v04 独立静态复核

**retained_static_candidate**，无本轮必须修复项。仅本姿态静态结论；用户接受、摄影注册和动态验证均为false。

- 当前raw：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/character_api_original.png`，880×1008。
- 精确raw SHA256：`f09cce8adb87e3afa8770064503848b0647ae12397582d0baf9902ab3eec150a`。
- 原F944 PTS=503968，31.498s；已实际打开guide及原尺寸源、R88原图/头肩crop、邻帧页、v02两底前史和无光照palette。

## 实际发现

- 源半睁微笑、横过胸前再向右上弯的双前臂、叠袖口和可见摊掌/指形保留。单色深灰瞳/小白点、暖桃肤色、源帽双叶/黑领红结/白围裙及后带合理，头颈/衣领连贯。
- 卷根在耳颈侧，可见上卷约 `[460,330,553,416]` 连续；下卷藏在白肩褶及前景黑袖后。约y445..520的横袖表面没有旧v01长灰尾，符合实际看过的R86/88/90附近遮挡。
- 外红珠完整，内珠在bob后只露局部（约外537,312、内516,331），不当旧红楔、不强露隐藏珠/尾。手臂后低卷不可见，本轮不虚构其形状或量全长。
- v02的白色反光纵线/亮斑在v04已去。实际全图及x4同ROI比较，当前灰底/薄荷材料条带/墨线读法更统一于bob，未见明显白高光、体积暗面或发光绿边。palette是材质标准，不以精绘身份图打光为上色依据。
- 正常白黑底无需拦截的实体背景/碎块、明显透明缺口或拼缝；不将raw隐藏RGB判为可见残渣。

## 边界

音频记录给参考t0=原PV27.828s，F944候选R88约3.67s；实际可见姿势已另看，不以相关系数代替姿态/发卷判断。没有审图无返回的v03；仅读取其目录下的palette输入资产。

这是新v04独立静态候选，不继承v02。尚未按真实PTS连播、核各曝光1080注册或用户接受；不称弹跳动态通过，不用固定根尾比压掉动作，不为露全尾把它画到前臂表面。

## 实际看图与哈希

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/inputs/source_pose_guide.png` — `10a5dd146f41d1145393ddd6af2be780f765e05790b308228b03f77bee46da45`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/character_api_original.png` — `f09cce8adb87e3afa8770064503848b0647ae12397582d0baf9902ab3eec150a`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/qa_white.png` — `222726982a50e62e060d1ee938e7015f4e69ae9c669e35815ce2cd8fa5ddb85b`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/qa_black.png` — `b21c4aa273764c7e40e42d67980da72a453ba6bf7e6ce735f6f7dac1c60e8d14`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v02/qa_white.png` — `564fd300a64dadc8301697f75b8ca599cf4e9cfd94c1ba0b5f91db9c3a6eaff9`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v02/qa_black.png` — `613b4196aab7a59d3b10fbd1bf809422e471082103ab88feceb2e26c14f01275`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000088.png` — `3ab879ad3f11b67e9cb8b6e9bd40554a1349dfca14f99ee64dc9b065c78e61c7`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/nearest_reference_hair_arm_crop.png` — `4833207fc06870d1451130f41d6abbd0a5efe635cd224c71544a003bf2bbfee5`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/reference_neighbors.png` — `2b794db5cb3f7035c5a044cc818ee6faa8199d5f3104c10c8270d45f25274276`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png` — `6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png` — `d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-34/source.png` — `5a998c172e07fc556093ba578367b6d9954ce768cd174fe5be51f1859cf2340b`

读取元数据（不代替看图）：

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/JOB.json` — `05e1fe0070a49e659d02d96c8cddd29a701971d80cbe6e75d2d29458a1fa194f`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v04/request_manifest.json` — `e27875c5611eeb44dd31c48ef8a4edf24a816d5657f680867900b148dbeb999e`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json` — `d74f632c3d824878892060e48790ed3928efb44a856476e82339b9a0a0513383`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/F0944_diagnostic/AUDIO_ALIGNMENT.json` — `303abec7f3fe89550af918e09b44b835373959419891a3a5e19d0fe23ae78f5a`

只写独立报告，未改中央registry/曝光账、图像或alpha，未调用生成。

