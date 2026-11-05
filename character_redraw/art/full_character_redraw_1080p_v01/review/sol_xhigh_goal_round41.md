# Sol xhigh 第41轮：G33-01/v03 独立静态复核

创建前确认同名JSON/MD不存在。**retained_static_candidate**，无本轮必须修复项。用户接受、动态和摄影注册均为false。

- 当前raw：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/character_api_original.png`，640×1024。
- SHA256：`18827fffbbd64165746babfedf262ffa89d140769b6f0e837a8f89083f9ae958`。
- 已实际看9张图：当前guide/raw/白黑、原F2306、首段F834、R0、无光照palette及G02眼参考。

## 原片表演与人物结构

原PV的闭眼、小直闭嘴、低头正向、垂臂、源可见手/另一手遮藏、交错腿与完整鞋均保留。黑立领红结/金件、黑长袖、白肩褶/袖口、长围裙/后飘带与黑长裙合理，头颈/衣领连贯，帽两叶贴头；两底未见需退修的实体残渣、透明缺口或拼接边。没有把R0简化动作/面部漂移、偏白肤色或画幅当作人物依据。

当前源闭眼，不强加虹膜/白点；最新单色眼画法不意味着所有帧都应睁眼。

## 头发与新参考的使用边界

灰bob、两珠、一股解剖左灰薄荷卷根部和可见卷段相连，画面右侧约 `[360,204,409,274]` 与白肩褶自然遮挡。可见灰底/薄荷材质条带/墨线未见明显白亮反光、体积暗面或发光绿边。R0只看头发相位，不用其人物动作/表情/肤色/构图。未强迫隐藏尾部露全，也未固定根尾比验运动。

这里没有相邻新稿的真实PTS连播，不能称摇晃/弹跳动态通过或隐蔽卷长已看见。

## F834..840 首段必须另行注册

F2306是完整全身母稿，F834实际是另行放大的半身用法；本轮实际打开F834，确认闭眼/小口/衣身等可见内容，而首段下裁遮去手下段和腿。**母稿当前全身位置不等于F834位置**。需要按原PV独立核缩放/平移/裁切及各曝光，不让母稿腿部露进首段，不能套R0画幅。835..840本轮未重新逐帧打开，不宣称已验证。

## 实际看图及哈希

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/inputs/source_pose_guide.png` — `c14ff1346354603764e1275555621d411ad9f15f53f0e5ee85220b651744ac8e`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/character_api_original.png` — `18827fffbbd64165746babfedf262ffa89d140769b6f0e837a8f89083f9ae958`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/qa_white.png` — `d4e396df8e97978aef6477e3fa00b8684167a27c9a99723b6cd463f17dfb3f2d`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/qa_black.png` — `a10ea0382a47ae2eae8505a4fbe1eca0e0bee6f78fcce47c07fc91419dedbf6e`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-01/source.png` — `5fd791de77c4871b4795b00d33fca6cdef41cdc68c3495027526317ae9a7f50c`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000834.png` — `8932bd2c964d5442f3b986f9eb285c7eb61069ff66b02cfe6950a12964ee9e72`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/motion_reference_upright_first10_20261031_v01/frames/R000000.png` — `8df21c4e4a3ae83ce7e79993842ee36c04787a34c396fb16beba7cc3588e65f3`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png` — `d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png` — `6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0`

JOB：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-01/v03/JOB.json` — `7b62de68c84c3511c6e875fe4fa47200f124892f3468c2d58634f7ed76d205b4`。API耗时、字节成功及主审candidate没有作为艺术结论依据。

当前只写报告，无生成/图像/alpha/公共registry或曝光账更改。用户最新规则允许已有API稿修复时内置imggen整体绘制，本代理不启动该流程。

