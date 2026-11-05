G33-41 深灰上接合 PREP v02（未应用）

实看诊断：原v01左眼最顶 y139:x378..382 是5px横段，右眼 y147:x438..449 是12px横段，右眼平顶更明显；本问题与底浅灰cap不同。

候选保原661许可像素与glint mask原SHA，仅另加L灰度 upper_dark_coverage。左眼 y139..141共10px，右眼 y147..149共25px使用32x32 SSAA椭圆冠覆盖；所有改动坐标和0..255权重见spec/receipt。上下眼线、眼白、小白glint、底浅cap、alpha和所有艺术文件未改。

图 ORIGINAL_CURRENT_PROPOSED_MASK_native_1x/10x 从左至右为：原图、当前Py、拟蒙版叠图（非调色返图）。V01_V02_MASK_OVERLAY_10x 左旧右拟；洋红为许可覆盖，青为小白点保护。

这只柔化深灰顶缘native阶梯，不能保证不动原上眼线就得到完整规则圆弧。0值恢复原source RGB，部分权重仅作source↔深灰AA；精确验证必须限制到这些上缘像素，不能把中心黑点/侧下黑rim也当例外。

已通过EyeLocalPolicy零应用source guard及两coverage结构检查。root_mask_reviewed=false/root_release=false，ROOT须看后才应用，并另交fresh实际结果审核。本PREP不是艺术接受或通过。
