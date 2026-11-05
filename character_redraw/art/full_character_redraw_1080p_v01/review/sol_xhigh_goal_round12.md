# Sol xhigh 第12轮独立静态复核

四张完整返回图均已实际查看原图、白黑QA、当前源与列明参考。**两张静态候选、两张须修**；未获用户接受，未验动态。G12-32尚未返回修稿，未预审。

| ID / 版本 | 源帧 | 结论 | 说明 |
|---|---:|---|---|
| ART-G21-01 / v04 | 1647 | retained_static_candidate | 保留前次结论：按源无眼，后脑/背向与帽叶合理，完整双珠单钻发接合；旧侧眼whole不沿用。 |
| ART-G12-32 / v01 | 936 | needs_repair | 保留前次结论：只修钻发中段x520..591/y374..483的扁带直折/窄连接，再mandatory whole；O嘴/眼/交叠手/衣帽保留。 |
| ART-G11-02 / v01 | 787 | needs_repair | 靠颊弯指相对脸右移约55、下移约100px，下方原可见弯曲指额外落出画布。仅修手位/原可见裁切；脸眼嘴、无帽裸颈和发型保留。 |
| ART-G25-01 / v01 | 1796 | retained_static_candidate | 斜向张臂/张指、完整腿鞋、衣帽与圆厚单钻发合理；鸭独立后期，未验最终注册。 |

G11手位依据：同为1680×1072的sourceguide与返图，嘴/下巴位置接近；源最高弯指尖约x381..424/y712..737，返图约x435..489/y814..837。源下方三根弯曲指在y885..1071仍占明显可见面积，返图大部在下界外。已实际看F787原尺寸及同坐标并排ROI x100..699/y650..1071，不能用全图定位同时补回脸与手的相对关系。建议定向局修原手位及可见指形后，按规则整体builtin imggen；不要求重做当前脸或补出画外完整手腕。

G12-32钻发连续，没有实际断开。G12-29也有扁带式简化，不能说它完全圆柱或把当前头姿/手势判失败；修正依据是本张明显直折角/薄接头。

未生成、未改图/alpha、未改主账。精确image/hash、全部实际看图路径和保留点见同名JSON。保留原报告名称sol_xhigh_goal_round12，未新增其他当前入口。

- ART-G21-01：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-01/v04/character_api_original.png`
  SHA256 `ffea98fdb67ea6de59eb9821906b7cc6c0975122d8cb065fea16f0d74648d00f`
- ART-G12-32：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-32/v01/character_api_original.png`
  SHA256 `c955214821b17bfc5f041fcd09e67e75e4e97594140a7d93a9d257b1f11bf2eb`
- ART-G11-02：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-02/v01/character_api_original.png`
  SHA256 `c15d457ef91a321183adbffb97cb15b9fa2b64b730a2ee9dc8e0aa6c90b8ffcb`
- ART-G25-01：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G25-01/v01/character_api_original.png`
  SHA256 `22888ff838d5362467e57aba66002ccaad4552aa5c6b6d8bbbac593bd72dd82e`

