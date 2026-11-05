# 全片目标 round02 独立复核

**G23可留静态候选；G34主体与圆睁眼修复可留，但当前文件仍需清理颈后透明空隙残线。** 未获用户接受，未验动态。只读审核，没有调用生成或改主账。

| 项目 | 实际图像尺寸 | review_status | 主要意见 |
| --- | --- | --- | --- |
| ART-G23-01 · F1706 · v01/whole_imggen_v01 | 1133×1388 | retained_static_candidate | 白帽/黑叶恢复贴合，钻发完整且体量正常，当前半睁眼随源，服装/双手/双腿可留。 |
| ART-G34-01 · F2665 · v01/whole_imggen_v01 | 1004×1567 | needs_repair | 此前错半闭眼已恢复源的圆睁。主体可保留；颈后与手之间约x552–586、y329–365有可见浅灰碎线，需清理alpha空隙。 |

G23虹膜内仍有轻微灰阶/瞳仁层次，不能称严格单块纯色；柔渐变也多于原PV，列为P2风格局限，不为此要求本轮再生成。扫帚缺席是prompt明确安排：人物与道具独立。当前两手保留斜握杆姿势，最终合成需让独立扫帚对齐两手，本轮没有审核道具层。

G34较圆睁开的眼睛已恢复，深色主填和小白高光可留。帽/黑叶、灰bob、双红珠、连续单钻发及完整尾尖、黑服/红结/白围裙、左手支腰右手近脸和完整双腿均未见新增明显结构错误。不能为统一眼画法再次改成G02半闭神态。

G34的P2透明层缺陷不是原图隐藏RGB彩点：我把真实qa_white和qa_black的x530–630、y285–395区域作4倍并排，浅灰悬空碎线在两者里都可见。建议只清理这块背景空隙的alpha残片，保护真实bob边缘、颈线和手指，重出白黑QA复核。主体不必因此重新设计；若另作API艺术局修，仍须按用户规则随后builtin imagegen整体重绘，不能转回拼头拼眼。

## 实际看图

**ART-G23-01**

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G23-01/v01/whole_imggen_v01/character_imggen_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G23-01/v01/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G23-01/v01/whole_imggen_v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G23-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png

**ART-G34-01**

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/whole_imggen_v01/character_imggen_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/whole_imggen_v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png

本轮没有做最终1080p摄影注册、G23道具接触或相邻帧动态验证，也没有把透明通道存在/技术检查当作艺术通过。G34清理建议尚未执行，主账和艺术文件均未改。

