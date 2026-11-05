# Sol xhigh 第23轮独立静态审核

六项新API整人返图均实际打开raw、白底QA、黑底QA、当前sourceguide，并查看列出的邻稿及完整钻发/单色眼参照。4项保留静态候选，2项需修；另补G29静态接触诊断意见。未生成、未改图、未改中央registry。全部用户/艺术验收、动态验证为 false。

| 项目 | 当前结论 | 必要处理 |
| --- | --- | --- |
| ART-G12-36/v01 | needs_repair（P1） | 恢复当前36更圆睁的眼态，以及横向翻腕/掌指方向，不能继承35半睑与斜上并掌 |
| ART-G38-02/v01 | retained_static_candidate | 倒置左根双珠/粗连续卷被领肩褶遮住较多，有自然依据 |
| ART-G39-01/v01 | retained_static_candidate | 倒置摊掌、顶裁及衣线保留，未补裁外手/腿 |
| ART-G40-01/v01 | retained_static_candidate | 当前闭眼、掌贴红结、倒置左根双珠粗卷保留 |
| ART-G42-01/v01 | retained_static_candidate | 当前转身靠脸蜷指、开眼/小闭口及原衣褶保留 |
| ART-G45-01/v01 | needs_repair（P1） | 恢复篮遮挡负空间与原露出握指，不能补篮后胸腹或以泛化悬掌替代 |

## ART-G12-36

当前返图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-36/v01/character_api_original.png
SHA256：`d7b3c7e492ac7884d543de8cb967601041e1a29293dd8f46e9e06f9c6f7a0a35`；736×1008；源F954。

- 灰bob、两红珠、画面右较粗连续灰薄荷钻发，帽贴头且两黑叶、原黑长袖/白肩褶/红结/围裙主体可保留。
- 已额外实际打开35自己的sourceguide。36新稿双眼与双掌仍非常接近已审35，当前36源自身则改变眼开合与翻腕方向；API声称open不作为证据。
- **P1 必修**：当前源36双眼更圆睁、上睑弧度与瞳位不同；新稿仍为35式较平低的上睑/半睑侧瞥，抹掉当前动作表情变化。 区域（约）：{"image_xyxy_approx":[240,245,430,340],"source_guide_xyxy_approx":[240,230,410,315]}。 以36当前sourceguide的开合/视线恢复圆睁，保留单色深灰虹膜+小白点/经济上睫，不复制35半睑。
- **P1 必修**：新双掌继续35式斜上并掌，当前36原源为更横向翻腕、指尖向画面右展开；前臂终点/腕角与源态不一致，不能仅修眼睛后当36通过。 区域（约）：{"image_xyxy_approx":[560,185,728,405],"source_guide_xyxy_approx":[485,190,705,380]}。 同次按36源恢复两腕相对位置、横向掌指方向与当前前臂角度，保持原衣袖与身体主姿。

以当前36源为动作结构，定向恢复圆睁眼及本态翻腕/掌指；API局修后必须builtin imggen整个人物再独审。保留灰bob/双珠/粗连续钻发/帽与服装身份，不手工拼眼或挖改手形。

实际查看：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-36/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-36/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-36/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-36/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-35/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-35/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G38-02

当前返图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-02/v01/character_api_original.png
SHA256：`be905a6b3da571114757a10d4cb9b50508f93fbe14f7633215681a9e5a862c32`；640×1040；源F3025。

- 倒置image LEFT两红珠根自然接单条较宽钻发；沿珠向上可见连续卷段进入白领肩褶/前臂遮挡，第二态露出较少符合源领肩位置，没有明确悬空/断段。
- 与38-01比较粗卷体量及灰bob同体系，未把隐藏卷尾强拉到肩前；未声称已看见被遮完整长度。
- 当前源开眼/小嘴、倒置黑白女仆衣、横跨前臂与顶部真实袖口/皮肤裁切保留；没有补屏外手掌、腿或独立枝叶/文字。
- 白黑QA未见明显旧红发实体、帽漂浮、头颈接缝或空隙残线；两黑叶贴帽。

保留静态候选。完整动作摄影注册/被遮头发与袖肩连续性在后续动态核查。

实际查看：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-02/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-02/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-02/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-02/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G39-01

当前返图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G39-01/v01/character_api_original.png
SHA256：`73f2df830f72ac08b64ac12f180252d55d9b987a64da8577fa285e6bab1941c4`；800×912；源F3053。

- 倒置根位仍在image LEFT，恰两红珠与宽连续灰薄荷卷，珠根到卷段自然连入白肩褶/手臂遮挡；灰bob/两叶帽饰同系列。
- 当前源画面左上摊掌的简化指轮廓、直袖/袖口与顶裁保留，另侧手臂出画不补隐藏手掌；白围裙/腰带/红结及衣线可对应源。
- 当前倒置圆睁与小闭口保留，虹膜单色小白高光；没有强抄38的另一动作。
- 白黑QA未见新的必须修透明实体/接缝；柔阴影与较顺描线记风格局限，不据此单独否决。

保留静态候选；顶裁由源摄影控制，不为展示手/卷尾扩大隐藏部分。

实际查看：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G39-01/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G39-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G39-01/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G39-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G40-01

当前返图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G40-01/v01/character_api_original.png
SHA256：`7de5fab092c3a13ec5a3cf483e8aa64ecdbffad149446e422d04cae1eff4d8cf`；656×1008；源F3094。

- 倒置闭眼与源手掌贴红结的接触关系、手指方向基本保留；未增加虹膜、睁眼或改为相邻摊掌态。
- 黑长袖/白袖口、红结、腰带围裙及顶部真实手腕裁切对应源，不补裁外肢体。
- image LEFT双珠自然接足量连续灰薄荷钻发，再被白领褶/袖口遮挡；帽两叶贴头，无明显旧红钻发实体。
- 白黑QA中颈/领连接和手边未见必须修的漂浮残片或断缝。

保留静态候选；闭眼简笔体系保持，后续核倒置组摄影与动态。

实际查看：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G40-01/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G40-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G40-01/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G40-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G38-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G42-01

当前返图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G42-01/v01/character_api_original.png
SHA256：`e58c5c8f4415edd4400d9e8e963067204f74f189abf6fa0926413f1ff90ad72c`；672×992；源F3187。

- 当前转身、近脸蜷指、另一臂垂下及原下沿皮肤裁切保留；源小闭口和睁眼侧看没有复制41的过头手势。
- 灰bob、image RIGHT双红珠与足量单钻发，卷段连续下收尖，和41-02仅做人设体量连贯比较。
- 帽贴头且两黑叶、原黑袖/立领红结/白肩褶/围裙腰褶/后腰白结对应源；衣服未换款。
- 白黑QA未见明显头颈接缝、第三黑叶或游离高不透明碎片；一般柔阴影不作为P1。

保留静态候选。源当前手势/视线优先，独立枝叶与字幕后期；未核动态摄影。

实际查看：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G42-01/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G42-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G42-01/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G42-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G41-02/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G45-01

当前返图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/character_api_original.png
SHA256：`d87988484a4c82bc6477694236637f916b46ad110439342c44232b4a8943e379`；816×832；源F3288。

- 灰bob/双珠/连续单卷、贴帽两叶、当前低头睁眼笑和双腿/鞋的大体源姿势可保留。
- 原源前景为独立面包篮，面包及篮遮住中央胸腹/部分红结，只有外露握指与袖腕可见；当前返图虽然省了篮，却补出了被篮遮挡的人体并把手换成泛化悬掌。
- 这不是透明RGB误显示：正常白黑QA都显示新增黑衣/红结和两掌，原raw采样A245..253，见alpha_observation。
- **P1 必修**：没有保留原篮/面包遮挡的真实负空间，填回未知胸腹/红结/部分颈前与臂侧；可见范围与用户只画原片可见人的要求冲突，不能直接交付透明人物。 区域（约）：{"source_guide_prop_xyxy_approx":[295,170,568,435],"current_body_xyxy_approx":[430,275,585,430]}。 以原源篮和面包的遮挡边界控制人物可见范围，独立前景区域保持透明；只保留源确实露出的皮肤/衣服，不重建篮后躯干。
- **P1 必修**：原贴篮握指/袖腕的接触姿态被画成胸前两只展开悬掌，原有支撑/抓握关系丢失；仅覆盖篮或单纯定位不能修回可见指形。 区域（约）：{"source_guide_xyxy_approx":[345,340,431,416],"image_xyxy_approx":[323,333,435,418]}。 按原源露出的指弯、拇指与袖腕轮廓重建握持；不补被篮/字幕遮住的整手。

应按当前原源的篮遮挡负空间和真实握持关系重新整人绘制；保留已合理的头发/帽/脸/裙腿身份。若先API局修，仍必须再builtin imggen整人并重审；不能靠手工挖洞或临时叠篮把泛化悬掌冒充源握指。

实际查看：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G45-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## G29 静态接触补充

当前锁定whole_v04 SHA256：`6f09bee94cf8abc0571740338b161f8a9a2072c0eeada8c1b859eec8d1233fde`。
1080人物层SHA256：`11a777b05550ed311f339c9f7951a82f415193cd7a63fbaffd15c461e92d3909`（本轮只复核哈希，未单独查看整幅人物层）。

结论：`retained_static_contact_candidate`。实际看 comparison.png 与 native_contact_strip.png 后，整体下移约15 guide像素的中央脸沿/case顶未见明显贯通粉底裂缝。没有旧高截口造成的大空带，不要求为该处再次主体重绘。

两角少量旧红角和字幕属于临时原前景mask；QA_PROVENANCE明确它不是干净生产道具，也不是最终场景。不得将其归咎当前人物raw，亦不得把这次局部接触候选称为交付前景或动态通过。

- 实际看图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G29_prop_occlusion_placement_v02/comparison.png
- 实际看图：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G29_prop_occlusion_placement_v02/native_contact_strip.png
- 已读来源：D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/diagnostics/G29_prop_occlusion_placement_v02/QA_PROVENANCE.json；SHA256 `a71397c1fc59cd8794c6ad6a0a79e9a49d324513389e717212eb5c1a4fbc51bc`

本轮精确raw/QA/source/邻稿路径与SHA256、逐项问题区域和G45实际alpha采样均保存在同名JSON。柔和简色阴影/较顺描线不单独作为必须重画依据；透明区隐藏RGB不代替白黑QA视觉判断。所有候选仍待摄影注册、道具/字幕遮挡及动态核查。

