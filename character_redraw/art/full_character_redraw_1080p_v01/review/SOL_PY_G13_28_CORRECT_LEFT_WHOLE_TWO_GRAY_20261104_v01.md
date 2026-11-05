# G13-28 correct-LEFT whole 眼部局部独审

结论：**retained_scoped_eye_candidate**；`secondary_eye_local_passed=true`，`scoped_edit_review_passed=true`。

- 独立NumPy：6994许可/6990实际变化（左3579/3579，右3415/3411）。眼外RGBA0、全部alpha0、560个glint保护像素RGBA0变化。正式结果与独立双色ellipse公式逐像素差异0；白黑QA与原RGBA合成差异0。
- 实际看完整白黑与每眼原生、原/最终8x、批准mask叠层：dark(72,69,67)+light(129,128,128)宽上凸下cap，1.5nativepx内部AA，未见centralblack。原glint/AA、原不等眼形、视线、上眼线/睫毛/眼白保持，侧下iris连续残黑环已去；真实眼线短笔保留。
- 仅局部通过。继承80e106新whole的exact PRIMARY及独审，眼域外全等；不重新批准全人、摄影、动态、隐藏卷/C或用户验收。

Output SHA：`b4723b7dfca8b02a9f9e68f93c12c804e214748db0ef57cfd08130490d656233`。Parent SHA：`80e10642029b2259a139268484becf8cd78f40716f8f4d91366da202e1fc8cac`。

完整actual路径/SHA、approvedspec、独立数组审计与母稿指针见同名JSON。0apply/API/生成/中央修改。
