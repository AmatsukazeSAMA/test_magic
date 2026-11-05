# Sol xhigh 独立美术复核 Round06

已实际看四张API完整返图、各自白黑QA和当前源；G02另对当前G02-03整稿，G07另对F515清晰alias参考与其JSON说明。审核器生成调用0，未修改画稿、计划或主账。

| 当前稿 | 结论 | 必须修正 |
| --- | --- | --- |
| G02-02 / F154 / v01 | retained_static_candidate | 无 |
| G10-01 / F767 / v02 | retained_static_candidate | 无 |
| G06-03 / F429 / v03 | needs_repair | 人物层仍有独立圆盘弧边 |
| G07-02 / F506 / v03 | needs_repair | 人物层仍有大盘弧及窄白盘沿 |

## 前两张

G02-02保持当前闭眼、眉口、缩肩抓灰衣和双手动作。双珠与钻发卷段连续到肩后出画，对照G02-03没有重新缩成小尾巴。G10-01已是纯裸手，当前展开长指、指间轮廓和腕切口随源；没有袖口、红结、金扣、盒沿或字幕。两张白黑QA未见必须修正的明显残渣。轻渐变及规整描线列P2风格局限；未经局修的完整API原稿不必仅为流程追加imggen。

## 倒置两张：只修独立圆盘残留

G06（640×1040）上盘弧约 **x90–360,y455–560**，左沿约x95–120,y515–727，下弧约 **x195–350,y768–793**，握盘手下尖弧约x414–435,y689–725仍真实可见。白QA能够追踪圆形盘沿，盘心透明不等于道具已经从人物层移除。原图(220,461) alpha=240，(260,787) alpha=217，佐证并非alpha=0隐藏RGB。

G07（1408×992）额头上方大弧约 **x510–1215,y145–316**；右上握盘手下的双弧/窄白盘沿约 **x1090–1285,y60–215** 仍可见。原图(900,302) alpha=248，(1190,140) alpha=218。窄白片在黑QA也可见。这些几何与原片圆盘吻合，不能当作头发或灰衣轮廓保留。

两张的180度倒置动作、图左双珠根部/完整单钻发、G06闭眼和G07半开单色眼、灰衣及手脚可保留。修正方向仅为**清除盘沿及夹带的窄填充**，逐线保住灰袖自身外缘、掌缘指缝与颈部/发线，不能矩形抹除，也无需补盘后隐藏身体。按用户规则，任何这类艺术局修之后都须交builtin imggen整体绘制，再看完整新稿白黑QA。

## 实际查看路径

### ART-G02-02

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-02/v01/character_api_original.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-02/v01/qa_white.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-02/v01/qa_black.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-02/v01/inputs/source_pose_guide.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-03/v01/whole_imggen_v01/qa_white.png`

### ART-G10-01

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G10-01/v02/character_api_original.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G10-01/v02/qa_white.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G10-01/v02/qa_black.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G10-01/v02/inputs/source_pose_guide.png`

### ART-G06-03

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-03/v03/character_api_original.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-03/v03/qa_white.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-03/v03/qa_black.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-03/v03/inputs/source_pose_guide.png`

### ART-G07-02

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-02/v03/character_api_original.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-02/v03/qa_white.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-02/v03/qa_black.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-02/v03/inputs/source_pose_guide.png`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-02/v03/inputs/source_clear_F515_alias_guide.png`

另读取：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G07-02/v03/inputs/CLEAR_ALIAS_GUIDE.json`

坐标为当前原返图像素近似区间；alpha仅用于说明已见线条的可见性。所有结论为静态复核，未获用户接受、未验最终1080p注册/独立道具合成或全片动态。

