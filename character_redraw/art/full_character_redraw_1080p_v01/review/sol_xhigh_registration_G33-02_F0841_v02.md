Sol xhigh — G33-02 / F841..844 位置与裁切 v02 独立复核（2026-11-01）

结论：retained_static_registration_candidate。保留当前整层变换，不建议继续移动；静态通过不等于生产绑定、原速连接/头发动势或用户接受通过。

原画：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/whole_imggen_flat_motion_v01/character_imggen_original.png
原画SHA256：83670948a643e2adbee2ca690422c9ec0e0530f6ba92efbd3fb1edd422f477bd
当前1080候选：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v02/character_1920x1080_proposed.png
候选SHA256：293974106083349cacd1b3e76d6a30f6e89c7ee939a617bab4168637a7570876
提案SHA256：6c132dee619dcb5297a60f1228b44fda4de9d9e68d98ba5c73cf2d8a44b61c4e
scale=1.142483529865302；translation=[320.26511239362867, 75.7232150313258]。参数对照v01仅X+32，Y/scale不变；没有局部分件warp建议。

实际新看v02比较、原尺寸粉底/透明层、全部四帧源联系页，另开native F841/F844以及当前whole raw/白黑、canonical F2312与guide，共11张。当前左拳外轮廓/袖口、肩身、腰与脸的横向位置相容，没有继续整层移动的必要。视口下裁与原片相近，没有把全身母稿腿鞋放入首段。

仍有局部画形余量，不能称逐点零误差：人工约读，原/当前口中心约[904,434]/[899,446]，金件[909,545]/[903,553]；腰带上缘[901,744]/[902,741]，左拳上端[430,793]/[430,793]，左袖口上缘[528,787]/[525,791]（各约±5px）。口眼内部低十来像素与已对齐的腰/拳不宜靠同一整层Y消除，亦不建议分件warp；后续原速连接仍要观察是否跳位。

四帧源人物可见态/位置没有要求更改本transform的变化，主要变化为背景、星形和文字。珠根/单卷在前向人物的画面右侧，符合人物LEFT。没有读取PRIMARY结论代替独立看图，也未审尚未返回的其他稿。

实际查看路径与SHA：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v02/source_comparison.png
  e396822fcd1b6a9cb29a7054930a39eabaa54366d021bf08f79a81dedf5828c9
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v02/pink_position_proposed.png
  04c13872f4ce9b3145ed27a8975de6dc34740a113ccf4e990d490c0fbc7ef5fe
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v02/character_1920x1080_proposed.png
  293974106083349cacd1b3e76d6a30f6e89c7ee939a617bab4168637a7570876
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v02/all_first_hold_source_frames.png
  3411473a9a6b348c71b94ec44b781e54e02a9de50631ee853955171e6e563740
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000841.png
  3a0e06b0040e7fc97a2ad4adc9d6ecf191f0c6de0cb8b7bdf4d32141735551e5
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000844.png
  41ea600ddb8d015d6ff8ad204663c8383816aadc7cc22e4a0c6262930f4096c2
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/whole_imggen_flat_motion_v01/character_imggen_original.png
  83670948a643e2adbee2ca690422c9ec0e0530f6ba92efbd3fb1edd422f477bd
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/whole_imggen_flat_motion_v01/qa_white.png
  37d6d0c675ad4e3ecd320464a899b2be64f4f7d4d8b0f264f9b5766e57c4a043
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/whole_imggen_flat_motion_v01/qa_black.png
  0b1ed92c5810983b3cf30e99878793c3ce2bd3e7d2d36087a315ece668f30e6e
- D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-02/source.png
  06d9f4c9785e9e5d652217c43ba2bb02a76e3bcf7fde276f57830fb8e816834f
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-02/v01/inputs/source_pose_guide.png
  77a672bb202f3d8921d56224fbd2f4b95bebd2d47f07ee5d6d979e78a7622343

读取参数文档：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v02/REGISTRATION_PROPOSAL.json
  6c132dee619dcb5297a60f1228b44fda4de9d9e68d98ba5c73cf2d8a44b61c4e
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-02_F0841_v01/REGISTRATION_PROPOSAL.json
  e67766c13e239bc4c5bede6ccb73b940b17c7cb1727a3825b269cec51df4406f

未修改素材、alpha、提案、公共registry或曝光绑定；未连续播放。本结论仅对F841..844当前静态位置候选有效。

