sol_xhigh_registration_G12-10_F0858_v03 — Sol xhigh独立静态摄影复核（2026-11-01）

结论：small_uniform_translation_adjustment_recommended / repair_required，仅需微小摄影修正，原画不用重绘。当前v03不作静态裁切通过。
范围F858..860（inclusive）；canonical F858。
当前原画：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-10/v01/whole_imggen_flat_motion_v02/character_imggen_original.png
原画SHA256：4698546ddfcb3d32228af84ff7155d051ed860a24af21f9cce58d97a260e6ba6
当前1080候选：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v03/character_1920x1080_proposed.png
候选SHA256：ba0d03a36a13adb03855bc07643f91013ec71e1b0c652322ce9603e1d44e1fb4
提案SHA256：01ab30c045f8ed2a604027615bf32e4a1c04b361dae90808b5d9cb809bd20e0b
当前scale=0.6209790209790209；translation=[537.5, 109.16048951048947]。

- 实际打开新v03比较、原尺寸粉底/透明1080、三帧源联系页，另原尺寸看F858/F860及当前raw。头手/身幅总体接近原片，但没有因root candidate而直接给裁切通过。
- 当前口、金件与两手整体横向较源约偏左10..25px；现scale无需再变。原片半睁眼/小闭嘴/倾头和图左双弯指手仍保留。
- 实际粉底底缘2倍近看可见1px背景横线：人物在y1078为半透明，y1079中央黑裙及白围裙多列A=0。因此身体平直裁口仍落在1080最后边缘，不是已经完全移到画布之外；这是实际合成可见性，非A0隐藏RGB误报。
- 不需要重画衣裙或补隐藏腿。保持scale，至少整层Y+2可将AA/直截边推出视口；另整层X+12可减小口/金件/手组的共同横差。
- 只在内存用现人物RGBA试位X+12/Y+2，实际看原源/落盘v03/试位三列。试位底部没有原来的背景横线，横向整体更接近原片。此试位未落盘，不能作为已通过的新production候选。
- 三帧原片联系页人物可见态/位置相同层次，主要变化为字/背景；没有实际连续播放。

底缘关键数值：y1078在中央裙/围裙各列A约167..201，y1079为0；正常pink近看有1px背景横线。建议当前整层X+12/Y+2，scale不变，translation=[549.5,111.16048951048947]。只在内存试位，未落盘/修改提案；实际新版本需复看。

实际本轮打开7张图（4新定位图、native首尾两帧、当前原画），全部原曝光也在联系页看过；其余native不冒称逐张原尺寸打开。读取2份参数文档。人工锚点为近似读图，详见JSON，不是自动检测PASS。

实际查看路径/SHA：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v03/source_comparison.png
  05ec25b755a1823fe31660f3e4696f9e4128d74b254b01f08b3908f67a37ac6f
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v03/pink_position_proposed.png
  446f368e6a687d1d88cb8922c0be5bc51f7766c1a8b1c42a3175fdc73f585a3e
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v03/character_1920x1080_proposed.png
  ba0d03a36a13adb03855bc07643f91013ec71e1b0c652322ce9603e1d44e1fb4
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v03/all_first_hold_source_frames.png
  3625961d71a47b60c6a48532ec25eb9056af4dc21d2685a421e04f1544ff7db6
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000858.png
  991252b2fa2269041ebd01d09eef407b6953415be5e0715246a31c39bf21ce84
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000860.png
  2031cd2416df221d0111727f9606542c5a524374469bb38538f17d7f1c7f37df
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-10/v01/whole_imggen_flat_motion_v02/character_imggen_original.png
  4698546ddfcb3d32228af84ff7155d051ed860a24af21f9cce58d97a260e6ba6

参数文档：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v03/REGISTRATION_PROPOSAL.json
  01ab30c045f8ed2a604027615bf32e4a1c04b361dae90808b5d9cb809bd20e0b
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G12-10_F0858_v01/REGISTRATION_PROPOSAL.json
  93fd6b2547008d8f18660ea143f93ba8aef941ebf3a90e721238be8bde1f82a8

保持现scale=0.6209790209790209；下一摄影候选建议translation=[549.5,111.16048951048947]，即当前整层X+12/Y+2。至少Y+2用于底缘，X+12为整体横向优化；不需要生成或分件warp。
未改素材、alpha、公共注册/曝光、提案；未生成。原速连接、头发动态、FX合成和用户接受均false。

