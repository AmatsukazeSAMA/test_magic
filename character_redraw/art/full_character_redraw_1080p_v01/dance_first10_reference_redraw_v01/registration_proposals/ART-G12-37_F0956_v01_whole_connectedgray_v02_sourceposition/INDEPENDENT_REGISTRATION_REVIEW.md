# ART-G12-37 — 新v01摄影拒绝

结论：`repair_required`。当前master `cb56b7a6a8c39fd0db2bcc698932d6e171798a0dffef397f5a4df2fe91625e27`，首曝光956..961共6帧，母956 / PTS510384，范围[510384,513584) / 1/16000。

- 新当前cb56...原图按原956→同first956的source-face几何生成初版；没有继承旧37定位或旧whole通过。
- 完整四面实际看：人物整层偏高，最高帽叶顶触/截于1080上边；源帽叶完整入画且更低。眼/下巴、金扣和腰也联合偏高，双掌高位随之上浮。
- 原保存衣底约raw1428映射1077.65，画内仍留约2px直切/底条；不能把初版直接绑定。该摄影失败不等同cb56艺术静态失败。
- 同一摄影任务重新实看956..961全部六native及母956/currentraw；此拒绝针对新v01位置，原源动作/当前灰卷结构不需为摄影重画。
- 仅建议整层uniform调整；不改原稿，不局部warp，不写ROOT_PRIMARY或中央。

- Proposal SHA256：`977f5e318de18751d4bf7e40e144474ea25fbd7153aa701b6164ed94006276de`
- 1080 layer SHA256：`778f209688a2cc1e2beb0ba2a0b29b83af28c1846b40124fe4dd46257a1e4a72`
- 本轮12张实际图路径/SHA及uniform几何见JSON；完整六源native与四摄影面均已看。
- exact-current-raw只读整层uniform重建与proposed RGBA一致；它只证明变换范围，不替代实际美术检查。

0生成/网络，0原稿修图/局部warp，0中央/ROOT_PRIMARY/绑定修改。静态摄影结论不代表动态、隐藏几何或用户验收。

