# Sol xhigh 第18轮独立静态美术复核

**3张静态候选，1张需要返修。用户接受/动态验证均为false。**

|项|当前版本|结论|
|---|---|---|
|ART-G06-02|v01/whole_imggen_v02|retained_static_candidate|
|ART-G12-34|v01|retained_static_candidate|
|ART-G29-01|v01/whole_imggen_v01|needs_repair|
|ART-G33-06|v01|retained_static_candidate|

## ART-G06-02

- 当前原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v02/character_imggen_original.png`
- SHA256：`e3e1b45d677196fe6cdd99f2802d77f8bb08a34ca6a2995674f9db4551a1f7d9`

- 本次重新实际打开987×1593 whole v02的原图、白黑QA和640×1040原源guide，并将旧whole v01、新v02白底/黑底握持手ROI实际放大对照，不继承旧v01结论。
- 握持手上缘现为连续圆桃色皮肤与黑描线，旧版上方灰白三角/尖片消失；下方指间空隙仅剩合理手指内轮廓，没有新挂出的盘沿灰条。新图(678,916)实际RGBA(0,0,0,0)，圆手内(718,949)RGBA(252,206,181,253)。
- 独立圆盘保持透明；盘孔负空间没有补隐藏躯干/腿。上方可见腿的弧形遮挡截口和另一侧源灰衣/短裤轮廓仍保留，不将源灰衣边误删为盘线。
- 源倒置闭眼、两条裸腿/裸足、展掌和握持手、宽灰T保留；头滚转后的解剖左根在image LEFT，恰两红珠接完整连续灰薄荷单钻发，卷段没有断开。
- 白黑QA未见必须修的实体红发残楔/新接缝/圆盘弧线。raw显示的部分彩噪/隐藏RGB不按实体残渣判；不宣称所有低alpha编码噪声已清零。


- 实看证据：旧whole v01及新v02握手ROI x650..779,y890..1079内存2倍放大；新v02白黑两底均看。

- 边界：尚未验独立圆盘重新合成后的实际1080p手指接触/裁切注册；新稿手与原源仍可能有小幅注册差异，需合成检查。
- 边界：仅静态人物复核，未验连续曝光、旋转/摄影与动态。

实际打开路径：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v02/character_imggen_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v02/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v02/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G06-02/v01/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png

## ART-G12-34

- 当前原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v01/character_api_original.png`
- SHA256：`ac996f8aa5001849530d82c958ebb57ceaae35ce45ad86cc34692a506d251a5d`

- 实际打开本次完整API raw、白/黑QA、当前source guide，并对完整钻发身份/当前单色眼参考，未借主代理结论。
- 本态三分之四头势、半开眼的微笑小闭嘴、抬掌与穿过胸前的黑袖、白袖口/红结/黑白女仆服和围裙裁切保留；不强套眼参考的半闭角度，开合按当前源。
- 白帽贴头、黑结只有源角度下露出的两叶。珠根ROI x475..584,y300..559实际放大，后面较大红珠完整、前/下方一珠被bob局部盖住；这是恰两珠的自然遮挡，不是第三颗珠或旧红发楔。
- 单条灰薄荷钻发从根部到末卷连续、卷体圆厚，垂于当前肩/胸前袖交叠处自然。没有旧版折纸/锯齿灰带式断接，也未为露全tip把长度缩成小尾。
- 眼内为单一深灰近黑面与小白高光，肤色暖桃；颈与黑领衔接、双袖/手缘和透明边缘在正常白黑QA下无明显必须修的新问题。


- 实看证据：白底珠根/完整钻发ROI x475..584,y300..559内存2倍放大。

- 边界：尚未验本态与前后G12动态连续性及1080p字幕/摄影裁切；轻微柔色阴影与更顺描线为风格局限，不单独触发返修。

实际打开路径：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G12-34/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G29-01

- 当前原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/whole_imggen_v01/character_imggen_original.png`
- SHA256：`30e4e19801321cc2d28e78638af22c42971b008b789ddf7773f4a3e19b9de687`

- 实际打开1273×1236 whole原图、白黑QA与1104×1072当前source。粉箱及其字/金件确已从人物层去掉，中央真实透明；无帽、灰bob、两珠、粗连续灰薄荷单钻发，源圆睁单色眼和视线可保留。
- 但是中央alpha截口过高：新whole按画布尺寸归一到源后，鼻下截口约y636..644，原箱上沿/原可见皮肤下缘在y719..723附近。眼位归一后大致重合，不能用整体下移去补这个缺口。
- 已实际查看原源脸部ROI与新whole归一后粉底诊断ROI：当前在原本可见的鼻下/下颊位置留出明显粉色空带。这是alpha为0的实际缺失，不是隐藏RGB或不可见低alpha点。
- 底部两侧三角灰衣是原箱外局部可见衣料的剩余形态，不把这些本来应分离的可见片当游离噪声删掉；缺口修复不能顺手补箱后嘴/下颌/颈。

- **P1 必须修**：去独立箱时过度清除了原箱顶以上本来可见的下颊/鼻下皮肤，实际合成会在眼脸与箱顶之间漏背景。 唯一修正方向：按当前原源的箱上沿恢复这一条可见暖桃皮肤至源遮挡线；保留眼睛、bob、两珠完整钻发及无帽；粉箱/箱后嘴/下颌/颈继续不绘。完成API定向局修后按用户规则再做一次builtin imggen整体重绘，并重新检查截口。

- 实看证据：source原尺寸ROI x300..849,y400..799与new whole按画布尺寸归一到1104×1072后同ROI、粉底诊断实际并看；诊断仅内存，不改画稿。
- 实看证据：source (550,660),(550,680),(550,700) 均RGBA(254,222,214,255)；对应whole (634,761),(634,784),(634,807)均RGBA(0,0,0,0)。

- 边界：粉箱后隐藏脸部不推断；不能通过补完整下脸/颈再称源可见原画。
- 边界：旧带粉箱API稿不作为候选；本条needs_repair只锁定当前whole精确SHA。

实际打开路径：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/whole_imggen_v01/character_imggen_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G29-01/v01/whole_imggen_v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

## ART-G33-06

- 当前原图：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-06/v01/character_api_original.png`
- SHA256：`fc0ba0cd4acf45527533b606f94c7df4e533aaa025771cc9c64fac47f6176fec`

- 重新实际打开本次API raw、白/黑QA、原源guide，与G33-05当前whole白QA、完整身份/单色眼参考对照；另把三张帽根ROI近看。
- 帽黑饰为两片大叶共同安装根，下方短尖片收在bob上缘，结构与G33-05已保留whole的短joint同构。新稿短根约x373..397,y80..106，不把所有短安装片都算第三叶；未见旧三片大叶/长垂尾复发，帽沿贴头。
- 源斜头收眼小闭嘴、近胸弯手及另一侧手指、抬屈一腿/另一腿下伸、完整鞋、黑白女仆服/红结/腰围裙保留。手势、裙褶和双腿无明显新增丢失。
- 灰短bob、两红珠、解剖左侧一条灰薄荷钻发根到尖连续、自然在肩前；眼内单色深灰近黑与小白高光，保留当前源的眼形/视线。
- 正常白黑QA未见明显头颈拼缝、旧红发实体、额外肢体或游离可见alpha残片。短共根作为实看说明记录，不要求因此局修或扩大改手姿。


- 实看证据：当前source帽结ROI x350..449,y20..139、当前白QA x350..449,y0..119，及G33-05whole白QA x515..629,y0..159均内存放大实际对照。

- 边界：未验05→06在实际1080p摄影中的帽根/钻发体量动态连续性；静态保留不代表该动态已通过。

实际打开路径：

- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-06/v01/inputs/source_pose_guide.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-06/v01/character_api_original.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-06/v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-06/v01/qa_black.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-05/v03/whole_imggen_v01/qa_white.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png
- D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G02-01/v02/whole_imggen_v01/qa_white.png

G29只有恢复源箱沿以上可见皮肤一个修正方向；不要补箱后嘴/颈。G06旧v01手尖三角没有因新v02静态保留而恢复通过；G33-06短共根按与05相同的判据保留。

精确QA/source哈希、G06 alpha点、G29缺口alpha样本/截口列位置均在JSON。未改素材、主账或计划，未生成。

