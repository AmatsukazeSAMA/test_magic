# G02 F100 最终整体重绘独立复核 v06

**结论：retained_static_candidate，可保留为静态候选。未获用户接受，未验动态。**

实际查看了以下五张，原图与QA均为1387×1134：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/character_imggen_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png

本张保留了用户偏好的v01眼形、上眼线和回望神态。当前源本来半睁，本张没有错误扩成全睁；深灰主色虹膜及小白高光方向成立。本轮没有做虹膜像素纯色检测，不把视觉单色方向说成严格色值验证。

绿色bob高光带已去掉。双红珠、单条灰/薄荷绿钻发位于画面右、人物自身左侧。钻发从珠下连接，沿肩后连续向右下延续出画，可见中段没有断卷，也不再像v01那样很快收成小尾巴。当前发尾超出构图，不能据此证明画外尾型或精确长度。头发比例依据补齐的完整三视参照，不把“一整头高”或旧裁掉下段的头部参考作为统一硬阈值。

灰衣、肩部、双手与回望构图保留，脸颈和钻发接合没有明显拼接缝。源本帧没有maid帽/黑双叶，不能为统一女仆造型添加。肤色视觉为浅暖桃色，没有明显苍白；未做#FCE8DC定量取样。

柔和脸部/衣服渐变、较整齐描线仍偏精修，白高光略呈心形，列为P2风格局限，不据此要求再生成本张。没有发现需要再次重绘的明显服装、发型、头颈或源姿势错误。

后续仍需在1080p注册和相邻动作播放中检查钻发出画、人物尺度与眼睛/阴影连续性；本轮没有做该动态验证。本报告不追认此前API试稿，不覆盖v05历史，也不代表用户选定母稿。未来若再作任何API局修，仍应按用户规则随后进行builtin imagegen整体重绘；本轮只审核，没有调用生成。

