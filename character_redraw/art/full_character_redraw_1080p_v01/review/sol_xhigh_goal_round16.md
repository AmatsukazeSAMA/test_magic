# Sol xhigh 第16轮独立静态美术复核

2026-10-31。两张新whole各自raw、白黑QA、当前source与对照均实际打开，结论均为retained_static_candidate。未获用户接受、未验动态/最终1080合成；未生成、改艺术/alpha或主账。

| 项目 | 当前新whole | 结论 |
|---|---|---|
| ART-G33-05 | v03/whole_imggen_v01，957×1644 | 两片大叶/短根贴帽；完整手/两腿鞋及衣裙保留。 |
| ART-G11-03 | v01/whole_imggen_v01，1596×986 | 明显横向手位错移已修；余约20–30px右下差记P2合成观察。 |

## G33-05

源帽结与当前白QA另原尺寸ROI放大后，现为两片大叶，共根短尖连接收在头顶发面，未见旧第三片独立大叶。白帽贴头。斜头开眼/小闭口、近头弯手/另一侧伸手、一屈一伸腿与完整鞋、黑白衣/红结金件/围裙保留。两珠与一条灰薄荷钻发完整连续，手前发后关系合理，不强拉卷到手前。白黑QA没有必须修的明显缝/实体残红或碎屑。

## G11-03

保留收眼、略皱小闭嘴，无女仆头饰/领结/袖口，灰bob/双珠/大卷自然出画。sourceguide1632×1008与whole1596×986已在内存诊断统一尺度后再比较。源最高弯指帽缩放后约x274..385/y661..766，新稿约x294..410/y685..787，余约20–30px右下差；旧110–130px向脸靠近的大错位已明显消失，低处三弯指/拇指及真实下裁切接近源。

P2：源指帽上端比嘴线高三十余px，新稿较近嘴线；这不是零误差，但本轮静态不因该数十px量级立即再付费整绘。下一步必须在实际1080脸锚注册后叠原黄色飞溅/字幕，检查原本露出的左下指段；若可见区缺指/误露隐藏腕，再定向修。不能靠全人物位移齐手，也不把手掌回填当已证实源人体。

## 精确图与实际看图路径

### ART-G33-05 / v03/whole_imggen_v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/whole_imggen_v01/character_imggen_original.png`
- SHA256: `18d4d8ce3bbc095727a690a7fd2afc1391c43a166a93adb4de9aaa4880b2334f`
- 实际打开：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/whole_imggen_v01/character_imggen_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/whole_imggen_v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`

### ART-G11-03 / v01/whole_imggen_v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/whole_imggen_v01/character_imggen_original.png`
- SHA256: `1aa0f00232793e37451869ce71f736158f9dd5939d99e61a856bfa0b45524833`
- 实际打开：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/whole_imggen_v01/character_imggen_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/whole_imggen_v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000795.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`

G33旧三叶API和G11旧手位错API的needs_repair历史不覆盖；本次意见只针对新whole精确SHA。所有诊断缩放/ROI均在内存，不改艺术文件。

