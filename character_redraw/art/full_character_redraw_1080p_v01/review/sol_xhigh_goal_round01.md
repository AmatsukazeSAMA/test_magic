# 全片目标 round01 静态独立复核

Sol xhigh 实际查看两项各自原图、白底QA和源姿势引导，共6张。只审核，未生成、未改画、未改registry。静态候选不等于用户验收或动态通过。

| 项目 | 结论 | 主要意见 |
| --- | --- | --- |
| ART-G08-01/v02 · F728 | retained_static_candidate | 裸手弯指、张开拇指、腕部下沿切口基本随源。旧凭空袖口已去掉，未加红蝴蝶结/金件/字幕。 |
| ART-G34-01/v01 · F2665 | needs_repair | 源为较圆睁开的眼睛，新稿再次变成偏半闭神态。仅此明确P1，先恢复当前源眼态。 |

G08的柔渐变略多，手部描线更整齐，作为PV风格连续性观察项，不据此否决。还未在1080p合成中检查腕部出画和尺度注册。

G34其余整体结构可保留：灰bob、两红珠、完整连续的单钻发；白maid帽和黑双叶贴合；黑服、红蝴蝶结/金色中心、白围裙及腰后白蝴蝶结；左手支腰右手近脸、完整双腿/黑鞋。没有把原红双钻改灰bob本身列为错误，也没有要求制服改初始三视的校服。

G34双眼问题约在原图x377–495、y133–177。源眼更圆更睁开，新稿低上眼皮压缩了眼高。唯一修正方向是恢复本帧源的开合及注视方向，保留单色深灰虹膜和小白高光，其它当前结构不再扩散改动。可用明确眼部局修候选；只要作API局修，后续仍必须builtin imagegen整体重绘，再审核最终整稿，不拼贴眼睛或头。

原图透明区域隐藏RGB显示暗底光晕，QA白底可正常判读alpha。只读抽查外部点alpha均为0，未把隐藏RGB误认为可见光晕；这个技术事实不是艺术通过。

实际看图路径：

**ART-G08-01/v02**

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G08-01/v02/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G08-01/v02/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G08-01/v02/inputs/source_pose_guide.png

**ART-G34-01/v01**

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G34-01/v01/inputs/source_pose_guide.png

两张均未获用户接受；未验证新稿动态、全片连续性或最终1080p注册。

