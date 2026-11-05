Sol xhigh 第44轮独立静态复核（2026-11-01）

ART-G12-20 / whole_imggen_flat_motion_v02：repair_required。
当前raw：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/whole_imggen_flat_motion_v02/character_imggen_original.png
SHA256：e3acba7d0273b66b822d22f94e0bd62dd59459534de61a704f5c7357dd87c8a7
984×1599；原PV F892 / PTS476208。

侧别与退修理由分开记录。实际看三视、原PV完整source/guide、新raw/白黑及本次flat身份/palette，共8张；另读JOB/request，并将白黑耳颈ROI [330,500,320,250] 在内存中放大2倍。未依据root HOLD或提示词直接判图。

侧别：新版可以合理读作远侧LEFT遮挡。此右向profile的近侧是RIGHT；本图近侧脸颊/颈旁没有外露挂接珠对。红珠仅在后脑后缘约[359..383,544..570]露小片；根/上卷由bob遮住，可见卷前缘被颈/黑领挡住，下缘又在白肩frill后结束，故不是单纯藏珠而没有深度关系。没有看见必须再次改根位的明确近侧挂接，不建议强拉出隐藏双珠或尾尖。隐藏几何与珠数仍不能由单帧证明。

当前退修为平涂问题：卷区约x350..491/y550..676的薄荷面仍由左浅转右暗，折回处有低对比暗面体积感。普通白黑底和耳颈放大均能读到，非隐藏RGB；没有白高光并不等于没有打光。与bob及用户要求的无光照灰/薄荷平涂不一致。
辅助正常白底样本同一可见薄荷面：[395,610]=[163,184,165]、[415,610]=[160,177,162]、[435,610]=[151,168,154]；数值只辅助已实际看见的现象，没有设像素阈值判艺术。

原片右向闭眼/闭口、后弯臂/隐藏手、服装和下裁保留。帽两叶、头颈黑领与肩褶连接未见明显接缝；白黑底未见raw透明区彩噪成为实体。建议保持当前远侧几何和PV表演，只在下一次内置整体重绘中去卷面渐变/暗面，不扩大改身体或把卷再拉到近侧。新whole必须重新审图。

实际查看路径与SHA：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/inputs/source_pose_guide.png
  ba4e8146acfd47df063a0a050d25b27dacfbd54ae1add3accd46581a425e1ea0
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/whole_imggen_flat_motion_v02/character_imggen_original.png
  e3acba7d0273b66b822d22f94e0bd62dd59459534de61a704f5c7357dd87c8a7
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/whole_imggen_flat_motion_v02/qa_white.png
  dc2ac772dcf51b043293a073e797f0e72f1bc7df8cd724f38573861726b898bd
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/whole_imggen_flat_motion_v02/qa_black.png
  99f7bb3fccfe408b75049a93c3580faf3d35a3a36d6a06f40e1ef5b412851f6f
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
  c580f9ffe8d93ca121eccdae6f82d67fadcce18cfa72bd5322d8e9859380eaa1
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/whole_imggen_flat_motion_v01/reviewed_flat_identity_only.png
  2b0bf38c148628dac23b4f76940d6a5d4b2964c95382d2ede5eba7392a6fe5b2
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png
  d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0
- D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G12-20/source.png
  db612b00e75459adcf3aa23c93e8a9589fd0afb8b4872707cc8f1975e7a9ca92

读取文档：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/JOB.json
  81d12270be4eeaadb9a47d1469b162c302d875c34260434f4e7519952df99857
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-20/v01/whole_imggen_flat_motion_v02/request_imggen.json
  b3e6fce61afde6dfb109814740ad97562e7e03d8fed8ad2e75ec253725528999

用户接受、摄影位置、连续播放和发丝动态均false。本报告未改图、alpha、公共注册或选择，未调用任何生成。

