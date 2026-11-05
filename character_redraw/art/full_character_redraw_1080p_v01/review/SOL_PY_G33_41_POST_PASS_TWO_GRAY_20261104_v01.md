# G33-41 后处理双灰眼局部独审（2026-11-04）

**retained_scoped_eye_candidate，secondary_eye_local_passed=true。仅限眼内RGB/下部浅灰拱cap。**

当前图SHA256：`2f66e00906f7a4db9edbf35ca1f7308443dd788cda63e7924a2467bdbc1e7695`。父原图：`636b913a402e8619cc352c0af830862a4aca5b5b1aece3a4b923158a201d4aaa`。

实际看完整WB、native/8x眼、处理前眼、own2480原眼、许可mask-overlay及认可cap参考。逐眼均normal_open；原不等开度/眼外形和小白glint保留，主灰与下拱浅灰成立，未见中心黑瞳或独立侧下黑iris环。真实黑上眼线和外缘AA保留；内部1.5px名义过渡在native尺度柔和。

独立重算全图675840像素：仅改661处（左287/右374），许可外675179处RGBA全同；全部alpha变化0，27个glint保护像素变化0，4个实际掩码SHA与ROOT_APPROVED spec吻合，changed-mask不符0。实际精确深灰426、浅灰158、两灰插值77；未使用VERIFICATION的core计数代替独立RGBA审计。

本审核未参与prep/apply；0生成、0中央/艺术像素修改。当前完整WB也实际看过，但不重新批准整个人物、摄影、曝光绑定、隐藏几何、动态或用户验收；这些状态均false。完整路径/20份证据SHA与重算结果见JSON。

