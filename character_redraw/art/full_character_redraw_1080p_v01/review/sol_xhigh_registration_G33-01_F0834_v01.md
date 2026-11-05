# G33-01 首段F834位置/裁切独立审核

**建议当前提案整层下移约22像素；scale与X不变。** 这不是连续播放/用户接受，也没有修改公共绑定或图片。

- 当前艺术原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/character_api_original.png`，SHA256 `18827fffbbd64165746babfedf262ffa89d140769b6f0e837a8f89083f9ae958`。
- 当前1080位置提案：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-01_F0834_v01/character_F0834_1920x1080_proposed.png`，SHA256 `0bd4e7b5b8f2fb1e88237cc71d5a71dac7db3dd05b9efeff75c368a0bc3d5f91`。
- 提案记录：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-01_F0834_v01/REGISTRATION_PROPOSAL.json`，SHA256 `a80168d013ca3168951ea74874fde912529f6045e70ebced0a57ee4b024f782d`。

实际看完7帧源联系页，另看native834/837/840、F2306、当前guide/raw/白黑、proposal比较/透明1080/粉底。源人物维持闭眼小口/低手的同一位置，背景特效变化；没有据背景拆新人物态。首段是独立放大半身，不能用全身母稿坐标称注册通过。

## 建议的统一调整

- 原scale：`1.809475806451613`，保留。
- 原translation：`[337.6103830645161,51.67590725806447]`。
- 建议translation：`[337.6103830645161,73.67590725806447]`，即当前整层 `(dx,dy)=(0,+22)`，可在+20..24px范围微看。
- 不做局部warp、不移动单独头或手，也不需因此重画当前人物。

当前帽顶约高23px、嘴/下颊高20px、腰带高24px、袖口高28px。内存实际制作了原F834/当前/整层+22三列对照，+22后帽、颊、嘴、胸结、腰和袖口更贴源，源下裁也更自然。新脸闭眼线内部比例略不同，+22后约较源低8..12px；不能为了单独对齐眼线把全身抬回或分块拉伸。数值是人工视觉近似，未当作自动对齐PASS。

## 范围与证据

本次试位只在内存显示，crop `[620,80,1200,1080]` 原尺寸三列；没有另存或覆盖proposal。保持原半身下裁，不露腿；同一候选可供834..840源hold待复核。主代理仍需形成实际落盘新候选并复看后采用，本报告不把未微调旧提案记为注册通过。

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-01_F0834_v01/source_comparison.png` — `1b507aa46d4aa1b5cc7f3afae049f4b48e13dbab828c5ebd44d8e7c1f10edea2`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-01_F0834_v01/all_first_hold_source_frames.png` — `c8e1e1dbb2d21675b6c93bd4f6a22eea968c9d272325c63ca79cfd1cc8a2eebf`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-01_F0834_v01/character_F0834_1920x1080_proposed.png` — `0bd4e7b5b8f2fb1e88237cc71d5a71dac7db3dd05b9efeff75c368a0bc3d5f91`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/dance_first10_reference_redraw_v01/registration_proposals/ART-G33-01_F0834_v01/pink_position_proposed.png` — `95f53fb67b9ee22ed63819c9cae72a5447fecef6fd2f58c7c17da969a583c583`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000834.png` — `8932bd2c964d5442f3b986f9eb285c7eb61069ff66b02cfe6950a12964ee9e72`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000837.png` — `703c436d25c574915eb2798f4c994eda6102aafe0412033cf56731f89defe990`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000840.png` — `814cb5b3ec09ee6c6e8a607d4d14e2c4ad871ea5e37675be2462184c11e6162d`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/character_api_original.png` — `18827fffbbd64165746babfedf262ffa89d140769b6f0e837a8f89083f9ae958`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/qa_white.png` — `d4e396df8e97978aef6477e3fa00b8684167a27c9a99723b6cd463f17dfb3f2d`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/qa_black.png` — `a10ea0382a47ae2eae8505a4fbe1eca0e0bee6f78fcce47c07fc91419dedbf6e`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-01/source.png` — `5fd791de77c4871b4795b00d33fca6cdef41cdc68c3495027526317ae9a7f50c`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/inputs/source_pose_guide.png` — `c14ff1346354603764e1275555621d411ad9f15f53f0e5ee85220b651744ac8e`

源835/836/838/839只通过完整7帧联系页实际看，完整native文件仅记录哈希；834/837/840实际另开原尺寸。JSON逐帧列明，未冒称全部native都另开。

动态、实际连续播放、公共注册采用与用户接受均false；Round41只是母稿静态候选，本次不继承为首段注册通过。

