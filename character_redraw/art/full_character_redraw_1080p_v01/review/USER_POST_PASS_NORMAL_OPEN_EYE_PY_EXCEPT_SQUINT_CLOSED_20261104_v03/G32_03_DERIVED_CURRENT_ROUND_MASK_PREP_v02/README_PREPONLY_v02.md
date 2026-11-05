G32-03 exact418d 派生viewport四虹膜 PREP v02，未正式改色。

- 实看完整2295原源、当前crop白黑底，逐只native/8x及新许可域/高光/圆弧叠图。四眼正常睁开；左中各一眼有前景bob遮挡，仅许可已露出虹膜。右前头双闭睫无虹膜，完全不处理。
- 复用与418d精确绑定且本轮逐边实看的旧完整iris/glint二值蒙版：许可4530+1882+4685+3858=14955，原glintAA264+0+284+267=815。高光未见的遮眼不补高光，发线不当iris黑边涂色。
- 内部cap全部重适配已确认cdf0圆弧baseline，沿各自原轴/可见域，native1.5px过渡。加权light约34.11/38.96/34.25/35.50%，只测量、不作为用户固定比例；旧cap不继承。
- 保globalv03深灰72,69,67/浅灰129,128,128，G32三头插入不套后续跳舞B配色。新叠图cyan=许可、magenta=原高光AA、yellow=新圆cap界线；纯coverage图为诊断，并非输出艺术图。
- source418d原字节不动。ROOT需先实际看mask/spec再apply，之后另独立人审最终结果；本mask准备者不兼任其最终独审。无API/imggen/正式Py/中央/摄影绑定/动态或整人用户通过。

精确路径、各图SHA、原轴/新cap参数见同目录G32_03_FOUR_VISIBLE_IRIS_CURRENT_ROUND_SPEC_PREPONLY_v02.json及MASK_PREP_CURRENT_ROUND_RECEIPT_v02.json。
