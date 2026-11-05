# Sol xhigh M17 独立源片审核

2026-10-31。F2153..2277，共125帧。实际看完8张全帧联系页、2张源源放大比较页（8对）、10张native原尺寸和canonical F2154源图。0新增状态、0待近看；未审核生成美术。

| inclusive区间 | 帧数 | 状态 | 归属与依据 |
|---|---:|---|---|
| 2153..2248 | 96 | confirmed_binding | OPT-BROOCH-PORTRAIT；同一印刷头像，金光/网点/歌词/放射橙FX变化不构成新表情。 |
| 2249..2252 | 4 | confirmed_binding | 同OPT；小圆孔仍露刘海/额部，不能整章按道具漏掉。 |
| 2253..2261 | 9 | confirmed_occluded_unobservable | 头像全遮，仅独立红bow尖条可见，不推断隐藏人物。 |
| 2262..2277 | 16 | confirmed_no_visible_character | 全橙底与白歌词，无人物；红bow碎片也已消失。 |

原尺寸更正：独立bow碎片最后在F2261可见，F2262已全橙白字，因此不是F2265才进入该段。头像本身最后可见F2252，F2253即完全被遮。这两个界线须分开记录。

既有OPT-BROOCH-PORTRAIT的canonical采样仍为F2154、source_pts=1149952，章节首可见另记F2153。原canonical SHA256：`a8ca16c5474209e47224508cc6efdc2608912014e0fd2310416823429086447d`。不改采样、计划或主曝光账。

## 实际看图与证据

- [coverage/review/M17_all/page_01.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_01.png) — `11a7748da9bfd2cef13bb264195971c6d18e0181fa76db376f3b249dc3789620`
- [coverage/review/M17_all/page_02.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_02.png) — `2cee17e9f10550378264dc4c5c2be285b630e9a6f09aa384f21a60487a79f3b9`
- [coverage/review/M17_all/page_03.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_03.png) — `3d8cfb6c88eaa418152df1e924f2317732c08cc0e7d14f04a3c1bbd899450dc7`
- [coverage/review/M17_all/page_04.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_04.png) — `c16e31b035e754e54fcf834ddcb1f5cd283ff63a868f1005746e4b3756d01cb1`
- [coverage/review/M17_all/page_05.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_05.png) — `a2ef08e2776d2f5fe3fc788055a886afc1ee2c5d91f193291d3a94b17e3b1dd7`
- [coverage/review/M17_all/page_06.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_06.png) — `6421df5569def7605d3f2f50be2f1009d6f4cdb214719e83316bf160d5a6ed19`
- [coverage/review/M17_all/page_07.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_07.png) — `ca591b9b3bf41466a68f6284dfda3cd3dc04fd3951246b76c0735a090affa33f`
- [coverage/review/M17_all/page_08.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_all/page_08.png) — `dd377c0787983d400db44273b6d53223a1345d01a0a8967d94b21f291bf9bf1d`
- [coverage/review/M17_portrait_source_comparison_v01/page_01.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_portrait_source_comparison_v01/page_01.png) — `93634f372cc445d55464a661ec2f166a2ca6822bbd797648b0df925a3fa71672`
- [coverage/review/M17_portrait_source_comparison_v01/page_02.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/review/M17_portrait_source_comparison_v01/page_02.png) — `69e4273ca567547e80714b15871c6f2c95443f56a846f3b8329262d7a73b8048`
- [coverage/source_frames/F002154.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002154.png) — `a8ca16c5474209e47224508cc6efdc2608912014e0fd2310416823429086447d`
- [coverage/source_frames/F002248.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002248.png) — `efca872618ce618bf6cfef2dd9beddb14d69526b62fcef170e077439e2bb8d23`
- [coverage/source_frames/F002249.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002249.png) — `94f91835a46d37a81ea6ea4292a9d30a21c337beadf032c861cedb27e07891a6`
- [coverage/source_frames/F002252.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002252.png) — `86ff2cfa5f0d3811cf0b3cb61c5302944d6ab058aaae82104c9ab16d4636737d`
- [coverage/source_frames/F002253.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002253.png) — `1263a06a3cb1d9f708cb6ec0dc29c2d29e48f676b55baa60f1dd364535858812`
- [coverage/source_frames/F002255.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002255.png) — `0c54feeadd59132113d9ca9f25a2875834ec9db6c5f9025f8870e5d99b182b76`
- [coverage/source_frames/F002261.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002261.png) — `a78744a6933f2dc31d7a854e8293f8d5ee7b13c620bcfec7a5aeee25fec37cde`
- [coverage/source_frames/F002262.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002262.png) — `204e7c6ca5d0e4cea3eca5ff11694b9ae20253818bab1225b9e846a6380b3904`
- [coverage/source_frames/F002264.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002264.png) — `0fc36982bc4b788f766e3f6ef6169a557dc94ab490f7ab1f100aeb5ee1ecbba6`
- [coverage/source_frames/F002265.png](D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F002265.png) — `c18ffc7c3ee77b66f7f624fc43f2de37c13c38bcaaffb076e60c446a1b5cb11d`
- [canonical G30-01/source.png](D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G30-01/source.png) — `a8ca16c5474209e47224508cc6efdc2608912014e0fd2310416823429086447d`

125张source frame文件及4份元数据的完整SHA记录见JSON；未单独全尺寸打开者明确记录为通过联系页查看，不以技术哈希冒充看图。

人物头像属于当前全人物范围。金框、独立大红bow、玻璃高光、网点与字幕另层处理；真实PTS绑定、生成稿/alpha、1080注册和连续播放均未核，用户与艺术验收均false。

