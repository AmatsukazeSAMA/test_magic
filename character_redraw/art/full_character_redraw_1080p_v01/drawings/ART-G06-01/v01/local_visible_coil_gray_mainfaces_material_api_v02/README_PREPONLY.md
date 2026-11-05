# G06-01 材料局修准备（未释放、未发送）

本轮 actual 查看当前完整 raw/白黑、原476完整及guide、两个精确输入、卷坐标白黑、完整蒙版/完整白黑overlay、局部4倍白黑overlay及alpha。可见三片宽前面到末端C偏mint绿，只开放这些材料内部。

640×1040 RGBA蒙版 alpha0=可编辑，alpha255=保护；2616像素，bbox [177,873,243,1014]。原alpha<250、黑结构及空气孔均0像素开放。黑线与轮廓留一像素内部余量，可能留下合理细mint边；细到不能安全开放的钩尖/返回仍保护。此蒙版不是新轮廓、输出通过或隐藏结构认证。

两参考顺序：当前完整78b8374d原字节target；pureGRAY颜料249d62ac。原476只实际核动作，不发送，避免红双尾入材料局修。完整强制LEFT前缀保留，prompt明确倒悬时根在画左下而非镜像根、保盘真透明区域/双裸足/灰袖/张掌抓沿。

八字段formal、引用/蒙版/provenance锁及仅Preview脚本已核。Preview实跑：官方edits / configured gpt-image-2.5-sunburst / high / 640x1040 / transparent / n1 / mask true / 2refs / submitted false。无执行分支、无key读取、无网络、无attempt。

root需actual以上精确refs、白黑完整/局部overlay、alpha和prompt后，另建正式release才可提交。返回只能是intermediate；future_mandatory_whole_PREPONLY只是未填返回SHA的非执行模板，必须known返回实看→整人builtin→fresh root/Sol，不能直接adopt或自动调用。0API/0native/0中央/JOB/REG/绑定。

精确hash见ARTIST_HANDOFF_PREPONLY.json。
