# Sol xhigh 第15轮独立静态美术复核

2026-10-31。三项当前真实返图已实际打开raw、白黑QA、source及指定对照。1项静态候选，2项需修。未生成、改图/alpha或主账；不是用户接受，未验证动态/最终1080合成。

| 项目 | 精确当前返回 | 结论 |
|---|---|---|
| G11-03 | v01 API 1632×1008 | needs_repair：手相对脸仍右移约110–130px。 |
| G12-33 | v01/whole_imggen_v01 1193×1319 | retained_static_candidate：双叶/贴帽/闭眼笑及双手、完整大卷可留。 |
| G06-02 | v01/whole_imggen_v01 984×1599 | needs_repair：握盘手上端小尖回归，透明负形/源腿截线主体可留。 |

## G11-03：保留首审需修结论

当前收眼、小闭嘴略皱、最高弯指高度符合本态；灰bob、双珠连续大卷和无头饰可保留。手与脸的水平关系不符：同1632×1008 guide源最高弯指帽约x280..394/y676..783，当前约x401..526/y668..768，嘴都约x815/y710。手约右移110–130px，下方三指/拇指同步偏右，不能用全人物定位修好。仅还原手的水平位置/弯曲及实际下裁切后mandatory whole，保留脸眼嘴和发型。SOURCE_COVERAGE_CORRECTION把旧底999延到源1080本身正确，不撤回。已看native F791/F795，黄色飞溅独立，不补隐藏腕/躯干。

## G12-33：新whole可作静态候选

新帽为两片黑叶，白帽贴头，闭眼笑/抬起的简笔双手、女仆服/红结金件及领口接合符合源。双珠/粗圆连续单钻发进入前臂遮挡后，未强拉尾端到手前。正常白黑QA没有必须修的明显实体残片。

P2非阻断技术观察：裁切线下全宽y1287..1318抽查，5214个非零alpha像素，最高A6，非零范围x37..854/y1287..1318；raw工具缩略图的异色/白形在正常白黑QA实际不可见。保留原图，不把它当高不透明碎片/接缝，不为不可见编码噪声重复付费；最终1080真实背景可见性仍待验证。

## G06-02：空负形保持，但上端盘沿小尖重现

新whole未继承局修整图错误补出的隐藏腿。空盘负形、腿被盘挡住的截线、灰宽T/裸足双腿、张开手、闭眼倒置头和image LEFT双珠足量连续卷均可保留。

但握盘手上端x674..689/y907..930有小黑边/灰白三角尖。实际与corrected_grip_only_reference并排放大，该参考顶部圆弯干净，whole又带回向上伸出的旧盘沿尖形；白黑QA均显示，样点(678,916)/(678,922)均A251。仅清这一处，保留肤色指/手背圆弯接触轮廓；下方指间窄黑边与接触边重合，本轮不扩大到全删。继续用源/prelocal主体+干净握手参考，不能用已拒绝的local_full隐藏身体。按规则局修后whole再审。

## 精确审核图与实际查看路径

### ART-G11-03 / v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/character_api_original.png`
- SHA256: `5c87c3c23e411140b5a80e2cd3c2f3f42abe465e292244107895151808b5a55e`
- 实际打开的图片：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/character_api_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000791.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/coverage/source_frames/F000795.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-02/v01/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`
- 实际读取工程证据：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/SOURCE_COVERAGE_CORRECTION.json`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-03/v01/REGISTRATION_PLAN.json`

### ART-G12-33 / v01/whole_imggen_v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-33/v01/whole_imggen_v01/character_imggen_original.png`
- SHA256: `f88026fad526a97ef5010eaf9eccc6730959d247732fa6c47b6b22dd07fd615a`
- 实际打开的图片：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-33/v01/whole_imggen_v01/character_imggen_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-33/v01/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-33/v01/whole_imggen_v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-33/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-32/v01/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`

### ART-G06-02 / v01/whole_imggen_v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v01/character_imggen_original.png`
- SHA256: `14d9c972921071d40a2fd70f817da5999e5bd82f2af2930839cf3426cbc08640`
- 实际打开的图片：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v01/character_imggen_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/local_disc_rim_removal_v01/corrected_grip_only_reference.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`

ROI均为内存诊断，没有修改/保存画稿。哈希绑定意见对象，不代表用户接受或动态/技术艺术PASS。

