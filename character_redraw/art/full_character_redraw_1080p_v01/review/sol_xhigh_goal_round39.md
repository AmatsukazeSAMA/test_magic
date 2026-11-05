# Sol xhigh 第39轮独立静态复核

创建前已查：`sol_xhigh_goal_round39.json/.md` 和 `round39.json/.md` 均不存在，没有覆盖旧报告。实际看12个图像路径及2份JOB，**两项均保留静态候选，无必须主体修复项**。用户接受、摄影注册和动态验证均为false。

| 当前稿 | 精确raw SHA256 | 结论 |
|---|---|---|
| ART-G32-01/v01 | `2cda9d63646caaf5f6c8cb3c9a61094f2be96e106b14b425ba1bcdbeb5158877` | retained_static_candidate |
| ART-G48-01/v01 | `3e6cc82079e090798f93e7da11739cce7a03b9ad2e614f17265d888aab8c8043` | retained_static_candidate |

## G32-01

- 当前原图 `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/character_api_original.png`，1632×1072。已实际看当前guide与原尺寸F2283。
- 保留原近脸大睁眼、偏向一侧的眼神、小粉色O口、头倾及顶/左侧真实裁切；单色深灰瞳和小白高光、暖桃肤色合理，没有双色虹膜环。
- 灰bob、两红珠及一股足量连续灰薄荷卷连接自然；帽源顶裁、两黑叶、细颈/黑领和源可见白肩褶保留，两底无明显必须修接缝/残渣/透明缺口。
- 仅核F2283单实例静态近景；后续多实例前后顺序、viewport及摄影注册未核，不称已合成。

## G48-01

- 当前原图 `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/character_api_original.png`，1680×576。已实际看当前guide与F4337原片。
- 大O口、下颌细颈和红立领保留。源只显示下半脸，没有擅加眼睛、帽饰、胸结或裁外身体。灰bob/两红珠/单灰薄荷完整卷及头颈连接合理，暖桃肤色；白黑底没有实体背景/残渣/拼缝。
- 卡窗黑边、白卡底、花瓣和歌词独立。新人物灰卷在独立层留到guide卡窗下界之外，**最终必须按原非直线窗口上下边裁切**（guide约上y42..62、下y520..535，仅定位非alpha）。本轮没有做/验证此合成，也不要求缩卷塞窗。

## 实际看图与哈希

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

JOB记录：

- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G32-01/v01/JOB.json` — `92db84a4fa113e7c9004044a88cdf11a4d6ddeb5c48085d37e1fa23a8d516219`
- `D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G48-01/v01/JOB.json` — `d1340f86606b44dbfa925e48687500763a36d5c0f5f33d155000ae4a277fdab2`

旧舞蹈pilot已暂停，现有诊断保留为待按新视频/F0944证据复查；没有继续用固定长度比值压制原片弹跳，也没有在这轮非舞蹈静态审核里宣称任何动态通过。未改图片、公共注册或曝光账，未调用生成。

## 后续用户平涂反馈补记（原结论保留为历史）

原文写完后，用户明确要求bob和钻发统一无光照平涂：灰底+薄荷绿结构条带+墨线，无白亮/高光/体积渐变/暗面/发光绿边。基于本轮已实际打开的大图和白黑底，**两张在新门槛下均应记 repair_required，仅修钻发上色**：

- G32：卷上段白亮片/浅亮带及中下卷较深内面、明暗分层；大致ROI `[764,692,1031,1066]`（1632×1072）。保留源脸/眼/口、裁切、帽珠和卷几何。
- G48：浅亮前面/较深内面及表面渐层与bob不统一；大致ROI `[1172,208,1401,575]`（1680×576）。保留大O口、红领、两珠和原卡窗裁切要求。

原 entries 的初审保留状态是历史；最新有效状态见 JSON 的 `post_review_addenda` 与 `latest_effective_review_status`。当前按用户最新优先级暂停非舞蹈扩展，不发修绘调用、不改中央选择。此补记也不构成动态通过。


