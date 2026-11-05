# Sol xhigh 第14轮独立静态美术复核

2026-10-31。实际重开四项当前原图、白黑QA、当前源与指定对照。结果：3项静态候选，1项需局修后整体重绘。未生成、未改图/alpha或主账；不是用户接受，未验证动态/最终1080注册。

| 项目 | 当前返回 | 结论 |
|---|---|---|
| ART-G33-04 | v03/whole_imggen_v01，957×1644 | retained_static_candidate；双黑叶修正成立。尾卷/白肩褶交叠为P2观察。 |
| ART-G06-02 | v01 API，640×1040 | needs_repair；夹盘手后两截独立盘沿仍可见。 |
| ART-G21-04 | v01 API，944×1056 | retained_static_candidate；源转正双眼、两叶帽、双珠单卷合理。 |
| ART-G28-01 | v01 API，624×1072 | retained_static_candidate；箱体孔留空、抓握手及便服短裤保留。 |

## G33-04：双叶修正可保留

这是新whole的重新独立审查，不沿用旧v03三叶稿。帽上确为两片黑叶，根部贴帽；当前睁眼/O嘴、两处拳、抬脚、完整腿鞋、女仆服/红结金件保留。两珠与单条灰薄荷卷连续，没有明显旧红双钻或头颈缝。

P2：新whole约x530..567、y474..537，末端细卷与白肩褶折线拥挤，形成局部菱形/折角线团；未证实真正断发。记录到后续1080/同组连续性检查，不据此单独再付费重画。

## G06-02：只清夹盘手后的短盘沿

源、白QA、黑QA同坐标放大后，上端x417..428/y568..592灰白尖片及黑边，和下方x412..428/y644..666指间短灰白条/并行黑线，均沿源独立圆盘的rim穿到手后。它们不是肤色指尖，也不是alpha0隐藏RGB：样点(421,579) A245、(420,652) A111、(424,657) A252；道具性质仍由源/白黑QA形状对照判断。

两处为同一局修方向：去掉手后盘沿填充/内线，完整保留肤色手指、手背、贴盘接触边和遮挡。随后按用户规则mandatory whole imggen，再复核新整稿。闭眼倒置头、image LEFT两珠完整灰薄荷单卷、灰衣、裸足、双腿及张开手均可保留。大盘孔已空且无贯穿孔长弧，但不能据此说所有盘边已分离；未来可能被道具遮住不等于已验证。

## G21-04与G28-01：静态候选

G21-04按F1657转正并露双眼、小闭口；白帽黑双叶、耳颈/黑领、白肩褶与红结金件合理。与G21-03实际对照，珠根/体量随转向自然，没有明显翻边或突然短尾。单色眼控制画法，开合仍随当前原片。

G28-01的粉箱区域实际白黑QA留空，未补隐藏嘴颈/中央上身；灰短袖、斜长衣摆、黑抽绳短裤、两侧手与大腿下裁切保留。后珠被bob遮成两段红弧，仍只有两珠，未发现第三珠/旧红发楔。粗单卷在箱侧连续。孔内(310,420)/(310,550)/(250,340)三点A0，仅为抽查，不声称全部alpha清零。后续须检查独立箱的覆盖、手前后层级和最终相机注册。

## 精确审核图与实际打开路径

### ART-G33-04 / v03/whole_imggen_v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/whole_imggen_v01/character_imggen_original.png`
- SHA256: `2206df8ed20bd140795bf0c957d7b6a6323706c405b5ab139c56b59bc7882eab`
- 实际看图：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/whole_imggen_v01/character_imggen_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/whole_imggen_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/whole_imggen_v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/local_two_leaf_cap_v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`

### ART-G06-02 / v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/character_api_original.png`
- SHA256: `7bdffebcb07b87fbe36a9ea7a43536489df4aa74cfd9b7995f818b6caf12b6be`
- 实际看图：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/character_api_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-05/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`

### ART-G21-04 / v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-04/v01/character_api_original.png`
- SHA256: `7c62c96bb053b0372a5ef4373d15349d3a83ef1225378074fe0efdbe8a2e5b13`
- 实际看图：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-04/v01/character_api_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-04/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-04/v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-04/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-03/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`

### ART-G28-01 / v01

- image: `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G28-01/v01/character_api_original.png`
- SHA256: `d9404fead61f0a66d6b237d278f05fd05f638d5e99ab3f4064d17f612531eca3`
- 实际看图：
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G28-01/v01/qa_white.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G28-01/v01/character_api_original.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G28-01/v01/qa_black.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G28-01/v01/inputs/source_pose_guide.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png`
  - `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png`

所有ROI均为内存诊断裁切，未修改/保存艺术图。JSON记录逐项观察、问题区域、alpha证据和局限。白黑QA实际显示优先于raw透明显示的隐藏RGB；哈希仅绑定意见对象。

