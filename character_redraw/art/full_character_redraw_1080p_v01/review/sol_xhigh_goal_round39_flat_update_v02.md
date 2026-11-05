# Round39 平涂反馈完整有效更新 v02

**两项 entries 均为 `repair_required`。** 本报告用于最新状态附件，不再让旧 `retained_static_candidate` 被误读。原始Round39及补记保留不变。

- 旧报告：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/sol_xhigh_goal_round39.json`，SHA256 `cc446bd7a1668b893e3aeeb30da79ff5030bfb3332dec1ab6a606400f43a4037`。
- 旧MD：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/review/sol_xhigh_goal_round39.md`，SHA256 `95cafe8fbb1d834031d4b8b690479a6e64958cd78c9e7d00812c00f0e7c6f2e1`。

最新门槛：**钻发与bob统一灰底+薄荷绿结构条带+墨线；无白亮斑/高光、体积渐变/暗面或发光绿边。**

## ART-G32-01/v01

- 精确raw：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/character_api_original.png`。
- SHA256：`2cda9d63646caaf5f6c8cb3c9a61094f2be96e106b14b425ba1bcdbeb5158877`。
- 状态：`repair_required`。
- 已实际看的卷上段有白亮色片/偏浅亮带，中下卷有较深内面与明暗分层；与bob的简色灰底不一致。新门槛下只应修平涂上色，不更改已可保留的源脸/眼/口、裁切、珠根、帽及卷几何。
- 定位ROI：`[764,692,1031,1066]`，1632x1072 current raw。
- 仅统一钻发上色：灰底+薄荷结构条带+墨线，去白亮斑/高光、体积渐变/暗面和发光绿边；保留当前结构及源动作服装裁切。当前按用户最新优先级暂停非舞蹈修绘，本报告不启动API。

## ART-G48-01/v01

- 精确raw：`D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/character_api_original.png`。
- SHA256：`3e6cc82079e090798f93e7da11739cce7a03b9ad2e614f17265d888aab8c8043`。
- 状态：`repair_required`。
- 已实际看的灰薄荷卷存在浅亮前面/较深内面及表面渐层，bob相对简平；按新门槛不应沿用原静态保留。只修钻发为统一无光照灰底+薄荷结构条带，保留当前O口、红立领、两珠及卡窗合成边界要求。
- 定位ROI：`[1172,208,1401,575]`，1680x576 current raw。
- 仅统一钻发上色：灰底+薄荷结构条带+墨线，去白亮斑/高光、体积渐变/暗面和发光绿边；保留当前结构及源动作服装裁切。当前按用户最新优先级暂停非舞蹈修绘，本报告不启动API。

原片可见脸/嘴/衣服、身份几何、珠根和裁切的初审观察仍可作历史证据，不能覆盖此新上色否决；G48卡窗合成边界仍未验证。当前只保存完整有效评测，不修改中央选择，不调用修绘。

## 本次沿用的实际看图证据

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/inputs/source_pose_guide.png` — `b3210a8fa602673ec9fa6d949881733183a40d022e310fc76bad999a41d8dcd5`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/character_api_original.png` — `2cda9d63646caaf5f6c8cb3c9a61094f2be96e106b14b425ba1bcdbeb5158877`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/qa_white.png` — `10386fe37c43ce2bd507615adf9ae28d20e2b6178a7eec624d0541317f888658`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/qa_black.png` — `d21bdfbdc41401d81ffae5e35caf0953fe09c627ee329838d5f48d8962d30f9a`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/inputs/source_pose_guide.png` — `b465916ec6db075d6121b2868eec9651a85a93a55a0c0caa0338b48c715736f1`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/character_api_original.png` — `3e6cc82079e090798f93e7da11739cce7a03b9ad2e614f17265d888aab8c8043`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/qa_white.png` — `4c1e23fb8b0072b73107a3f17e2074336940afe9d43feb9f8ff2eae1ed776401`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/qa_black.png` — `ce7c3d3d563e0134cd19aa8efec188e00e5ae0c017ff1ea95088bba9f233a45b`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/identity_full_drill_three_views.png` — `c580f9ffe8d93ca121eccdae6f82d67fadcce18cfa72bd5322d8e9859380eaa1`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/inputs/eye_G02-01_F100.png` — `6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G32-01/source.png` — `fe6738f21e5fc001fcd2f0d47a2ce6ca1e3c9c86a21b7edd205056979b0c9ded`
- `D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G48-01/source.png` — `d61e7ea35db17c797a291123635ddb28bcc210a9779035b9aa4cb4811a8a80c7`

上述12张已实际打开；此更新只按最新明示规则复查已看的原图与白黑底，不新增非舞蹈素材。用户接受、摄影注册、动态均false。

