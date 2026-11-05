sol_xhigh_registration_G33-03_F0845_v02 — Sol xhigh独立静态摄影复核（2026-11-01）

结论：retained_static_registration_candidate，保留当前uniform transform，无继续整层调整建议。
范围F845..848（inclusive）；canonical F2314。
当前原画：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-03/v03/whole_imggen_flat_motion_v01/character_imggen_original.png
原画SHA256：48ddbb5425c5f71f7e88dd1b4f92f279e1fb6904cc07e18e0277422ec0a2e1c2
当前1080候选：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v02/character_1920x1080_proposed.png
候选SHA256：1f6e110bc1f7afe732c899eaa50bd7aec5aec2e3fdfbd4bd918d9e1679a8a73a
提案SHA256：8900e11be29259f5490ebc1aa36f623722caaf3ec3d27027945b1a03e8eff8b9
当前scale=1.0876735577072985；translation=[435.3005937355424, 116.85961302672172]。

- 实际打开新v02源并列图、1920×1080粉底/透明人物、全部四帧联系页，另原尺寸看F845/F848和当前raw；检查脸之外的两手、袖口、腰和下裁，没有沿用root候选。
- 当前口/金件/腰、帽顶及身幅在原片相近位置，视口下缘保留原半身裙/飘带截面；没有把全身母稿腿鞋放回首段，也没有出现画布内身体直截线。
- 两侧手势和相对高低保留，但余差并非零：图左最高指尖约右移20px、下移26px，图右最高指尖约下移34px；腕/袖口局部约低10..20px。此差别须保留记录，不能只核脸后忽略手。
- 口/金件几乎已齐，而腰上缘略高，整体上移25..35px追指尖会破坏头身对齐；当前不建议再用统一位移/缩放追所有内部点，也不建议分件warp。
- 四帧原片联系页中人物可见态/位置未见要求更改本transform的摄影变化；主要变化为背景和文字/FX。这里只逐张静态看，不称连续播放通过。

手部余差明确保留为P2：最高指尖约低25..35px、腕/袖口约低10..20px，图左手另偏右约20px。不能称完全对齐，也不能只看脸。

实际本轮打开7张图（4新定位图、native首尾两帧、当前原画），全部原曝光也在联系页看过；其余native不冒称逐张原尺寸打开。读取2份参数文档。人工锚点为近似读图，详见JSON，不是自动检测PASS。

实际查看路径/SHA：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v02/source_comparison.png
  9bb94f8b1aa441656c6e82ce41439c5c6b5c8d2175b848eb510b12eb9e170120
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v02/pink_position_proposed.png
  99680bff841131beb0afcd35d4d69bf4418635f61e9bb249275a38981034e5c6
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v02/character_1920x1080_proposed.png
  1f6e110bc1f7afe732c899eaa50bd7aec5aec2e3fdfbd4bd918d9e1679a8a73a
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v02/all_first_hold_source_frames.png
  0e61202b09fc0889c0b8ce6b06e8dbc158aaae348c5869a52d5e30f49e21f36d
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000845.png
  2ddadef2e9e5d2a4dafed570308f2c2ffb0498c8a0cdcec8e31a27ecb4158b7a
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000848.png
  959f7d0a5e1b8ce98f51d2118811f30b2078e08194c3a8a0afbb21ce6e7aafae
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-03/v03/whole_imggen_flat_motion_v01/character_imggen_original.png
  48ddbb5425c5f71f7e88dd1b4f92f279e1fb6904cc07e18e0277422ec0a2e1c2

参数文档：
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v02/REGISTRATION_PROPOSAL.json
  8900e11be29259f5490ebc1aa36f623722caaf3ec3d27027945b1a03e8eff8b9
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-03_F0845_v01/REGISTRATION_PROPOSAL.json
  942b9ae0d6f851d8b09532c4a7fd34cfa7e19aaac6dd55ef6d1a11509ad854a7

保留当前v02 scale/translation，无下一次整层调整建议；后续独立应用绑定并真实连播，关注两手P2余差。
未改素材、alpha、公共注册/曝光、提案；未生成。原速连接、头发动态、FX合成和用户接受均false。

