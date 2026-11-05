# Sol xhigh 第13轮独立静态复核

实际查看五张新返回图及G33-04前候选原图、白黑QA和当前源。**四张静态候选、两张须修**，其中G33-04是第11轮遗漏的更正。未获用户接受，未验动态；未预审尚未完成whole的G33-04局修中间稿。

| ID / 版本 | 源帧 | 结论 | 实际证据与保留点 |
|---|---:|---|---|
| ART-G12-32 / v01/whole_imggen_v01 | 936 | retained_static_candidate | 新whole卷段圆厚连续，原扁带薄接头已修；O嘴/圆睁/交叠手/衣帽保留。 |
| ART-G21-03 / v01 | 1652 | retained_static_candidate | 本态源已露双眼，当前圆睁及转正合理；不把前两态遮眼强加。帽/领结/完整单钻发自然。 |
| ART-G33-05 / v03 | 2322 | needs_repair | 三个真实独立黑尖叶，源双叶；只修帽饰，手姿/腿鞋/衣服与连续钻发保留。 |
| ART-G33-04 / v03 | 2319 | needs_repair（更正） | 本轮再次看raw/白黑/源确认同样三叶、源双叶。撤回第11轮静态保留，完整双腿/O嘴/拳姿保留。 |
| ART-G11-02 / v01/whole_imggen_v01 | 787 | retained_static_candidate | 新整稿重新看：最高内弯指回到略高于嘴线、靠颊高度；下方三弯指恢复明显可见，底缘正常掌腕裁切。 |
| ART-G01-02 / v01 | 52 | retained_static_candidate | 第二重描眼脸/抓灰肩手/领口/衣褶合理；大单钻发在肩后向右/下自然出画，不为露tip缩短。 |

G11新whole为1570×1002，源guide为1680×1072，按脸嘴与手的相对位置核。旧API手右下移和额外裁指问题已在此新whole修正；不让新结论覆盖旧图失败历史。当前圆睁小张嘴、无帽裸颈、双珠大钻发保留，白黑QA未见必须修复的可见残片。

G01-02维持本态独立ID；源F52与F13第二重描共用已经M01源审证实，但不等于与G01-01第一稿alias。肩后发卷被遮挡及尾端出画符合此近景，不认作断发或短尾。

G33-05帽饰约x337..406/y14..96，G33-04约x288..364/y30..100。05发根/手/钻发ROI显示两珠之一部分被bob遮，钻发在手后连续，不扩大改手姿或强拉到肩前。两项仅定向还原双叶，局修后mandatory whole；先04完成整体返图和双审，再05。

第11轮G33-04漏查叶数是我的审核遗漏，本报告明确更正，历史round11不覆盖。未生成、未改图/alpha或主账。精确image/hash和全部实际查看路径见同名JSON。

- ART-G12-32：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-32/v01/whole_imggen_v01/character_imggen_original.png`
  SHA256 `01f613ade86c7951f59440e5f0cd7abf658a18569579d732c713d12e27ade798`
- ART-G21-03：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G21-03/v01/character_api_original.png`
  SHA256 `80fb7fa5f3d8ece3f6f8be7c23b50db61cf14105bd0bd29f8dad4f22eeaa115c`
- ART-G33-05：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/character_api_original.png`
  SHA256 `383431784f0ecf95684fb9e03501da914f3df2f188dcb338c6e9bf17a057db9a`
- ART-G33-04：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-04/v03/character_api_original.png`
  SHA256 `f2055c824f25bf663538cbbcebbb0d602ec2e33dea3b61e5c1f1c8ec56607429`
- ART-G11-02：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G11-02/v01/whole_imggen_v01/character_imggen_original.png`
  SHA256 `6a2899b44594e72be0ffcd979fc7aba1f7518e411973b61944b6f4ac0b51e939`
- ART-G01-02：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G01-02/v01/character_api_original.png`
  SHA256 `eb66716eac76b1a86d4e5db57e9afddef47d878ef9f620ce842a900126d670df`

