# M06 源曝光独立复核 v01

审核：Sol xhigh。范围：F504–678，175帧。只读审核，无生成、无画稿/计划/主ledger更改。

**122帧可确认具体canonical；53帧确认有现有画型对应，但01/07或02/14的唯一ID仍待核。未证实额外new_visible_state。** 没有为遮挡或编号未知提出付费补画。

## 实际查看

实际看完M06_all的11页全部175帧，读取INDEX与REDRAW_PLAN group G07，但不采纳页标题candidate为结论。以下8张完整1920×1080源图逐张看过：

| 稳定ID | source_frame | source_image |
| --- | ---: | --- |
| ART-G07-02 | F506 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-02/source.png |
| ART-G07-03 | F507 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-03/source.png |
| ART-G07-04 | F509 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-04/source.png |
| ART-G07-05 | F510 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-05/source.png |
| ART-G07-14 | F525 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-14/source.png |
| ART-G07-01 | F532 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-01/source.png |
| ART-G07-06 | F541 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-06/source.png |
| ART-G07-07 | F542 | D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G07-07/source.png |

另外实际全幅查看F549、611、678；在内存只读并排裁切了F507/516/671、F510/520/568、F532/552/677的眉眼/发尖（2倍最近邻），及F504/532/542、F506/515/525、F510/520/635、F512/541/676的鼓沿/颈部（原尺寸）。没有保存或修改诊断图及画稿。全部175帧看过contact sheet，不等于175张各自全幅原尺寸精读。

固定头、脸、鼓沿、灰袖、手、左侧发块ROI的RGB MAE只帮助定位。未配准、未排净所有幽灵，数值没有绑定/艺术通过阈值。

## 可见区别

不同头态/描线不能全部复用一张。尤其03与04的脸很接近，鼓沿下缘却明显不同；05与06也有不同鼓沿/灰袖相位；07与14之间亦有变化。这些已经由现有8项覆盖，本轮没有证实还要新增人物稿。

01/07和02/14分别高度同形。脸部与鼓沿近看支持相同人物画型，轻微色边/幽灵差不足以证明唯一原始cel编号。保留全部8项，除当前基准及直接连续复用外，其余53帧按对应二选一留待核；不强行归属，不删除所谓重复项。

例如左上小幽灵压住灰袖、画面右侧大幽灵盖住红钻发，都应独立于人物。F546、586、642附近字幕改变也不是新人物动作。新灰bob人物绘制应遵守各个源动作/线稿相位，不重绘幽灵和文字进人物。

## inclusive逐段意见

`canonical_id`使用REDRAW_PLAN稳定ART-G07 ID。待核段JSON的canonical_id为null，并列稳定候选ID；不是默认接受其中一个。

| 首尾帧（inclusive） | 帧数 | 状态 | 已绑定ID或待核ID |
| --- | ---: | --- | --- |
| F504–505 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F506 | 1 | confirmed_binding | ART-G07-02 |
| F507–508 | 2 | confirmed_binding | ART-G07-03 |
| F509 | 1 | confirmed_binding | ART-G07-04 |
| F510–511 | 2 | confirmed_binding | ART-G07-05 |
| F512 | 1 | confirmed_binding | ART-G07-06 |
| F513–514 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F515 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F516–518 | 3 | confirmed_binding | ART-G07-03 |
| F519 | 1 | confirmed_binding | ART-G07-04 |
| F520–521 | 2 | confirmed_binding | ART-G07-05 |
| F522 | 1 | confirmed_binding | ART-G07-06 |
| F523–524 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F525 | 1 | confirmed_binding | ART-G07-14 |
| F526–527 | 2 | confirmed_binding | ART-G07-03 |
| F528 | 1 | confirmed_binding | ART-G07-04 |
| F529–530 | 2 | confirmed_binding | ART-G07-05 |
| F531 | 1 | confirmed_binding | ART-G07-06 |
| F532–534 | 3 | confirmed_binding | ART-G07-01 |
| F535 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F536–537 | 2 | confirmed_binding | ART-G07-03 |
| F538 | 1 | confirmed_binding | ART-G07-04 |
| F539–540 | 2 | confirmed_binding | ART-G07-05 |
| F541 | 1 | confirmed_binding | ART-G07-06 |
| F542–543 | 2 | confirmed_binding | ART-G07-07 |
| F544 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F545–546 | 2 | confirmed_binding | ART-G07-03 |
| F547–548 | 2 | confirmed_binding | ART-G07-04 |
| F549–550 | 2 | confirmed_binding | ART-G07-05 |
| F551 | 1 | confirmed_binding | ART-G07-06 |
| F552–553 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F554 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F555–556 | 2 | confirmed_binding | ART-G07-03 |
| F557 | 1 | confirmed_binding | ART-G07-04 |
| F558–559 | 2 | confirmed_binding | ART-G07-05 |
| F560 | 1 | confirmed_binding | ART-G07-06 |
| F561–563 | 3 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F564 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F565–566 | 2 | confirmed_binding | ART-G07-03 |
| F567 | 1 | confirmed_binding | ART-G07-04 |
| F568–569 | 2 | confirmed_binding | ART-G07-05 |
| F570 | 1 | confirmed_binding | ART-G07-06 |
| F571–572 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F573 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F574–575 | 2 | confirmed_binding | ART-G07-03 |
| F576 | 1 | confirmed_binding | ART-G07-04 |
| F577–579 | 3 | confirmed_binding | ART-G07-05 |
| F580 | 1 | confirmed_binding | ART-G07-06 |
| F581–582 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F583 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F584–585 | 2 | confirmed_binding | ART-G07-03 |
| F586 | 1 | confirmed_binding | ART-G07-04 |
| F587–588 | 2 | confirmed_binding | ART-G07-05 |
| F589 | 1 | confirmed_binding | ART-G07-06 |
| F590–591 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F592 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F593–595 | 3 | confirmed_binding | ART-G07-03 |
| F596 | 1 | confirmed_binding | ART-G07-04 |
| F597–598 | 2 | confirmed_binding | ART-G07-05 |
| F599 | 1 | confirmed_binding | ART-G07-06 |
| F600–601 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F602 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F603–604 | 2 | confirmed_binding | ART-G07-03 |
| F605 | 1 | confirmed_binding | ART-G07-04 |
| F606–607 | 2 | confirmed_binding | ART-G07-05 |
| F608–609 | 2 | confirmed_binding | ART-G07-06 |
| F610 | 1 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F611 | 1 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F612 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F613–614 | 2 | confirmed_binding | ART-G07-03 |
| F615 | 1 | confirmed_binding | ART-G07-04 |
| F616–617 | 2 | confirmed_binding | ART-G07-05 |
| F618 | 1 | confirmed_binding | ART-G07-06 |
| F619–620 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F621 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F622–624 | 3 | confirmed_binding | ART-G07-03 |
| F625 | 1 | confirmed_binding | ART-G07-04 |
| F626–627 | 2 | confirmed_binding | ART-G07-05 |
| F628 | 1 | confirmed_binding | ART-G07-06 |
| F629–630 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F631 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F632–633 | 2 | confirmed_binding | ART-G07-03 |
| F634 | 1 | confirmed_binding | ART-G07-04 |
| F635–636 | 2 | confirmed_binding | ART-G07-05 |
| F637 | 1 | confirmed_binding | ART-G07-06 |
| F638–640 | 3 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F641 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F642–643 | 2 | confirmed_binding | ART-G07-03 |
| F644 | 1 | confirmed_binding | ART-G07-04 |
| F645–646 | 2 | confirmed_binding | ART-G07-05 |
| F647 | 1 | confirmed_binding | ART-G07-06 |
| F648–649 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F650 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F651–652 | 2 | confirmed_binding | ART-G07-03 |
| F653 | 1 | confirmed_binding | ART-G07-04 |
| F654–656 | 3 | confirmed_binding | ART-G07-05 |
| F657 | 1 | confirmed_binding | ART-G07-06 |
| F658–659 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F660 | 1 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F661–662 | 2 | confirmed_binding | ART-G07-03 |
| F663 | 1 | confirmed_binding | ART-G07-04 |
| F664–665 | 2 | confirmed_binding | ART-G07-05 |
| F666 | 1 | confirmed_binding | ART-G07-06 |
| F667–668 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |
| F669–670 | 2 | needs_closer_inspection | ART-G07-02 / ART-G07-14 |
| F671–672 | 2 | confirmed_binding | ART-G07-03 |
| F673 | 1 | confirmed_binding | ART-G07-04 |
| F674–675 | 2 | confirmed_binding | ART-G07-05 |
| F676 | 1 | confirmed_binding | ART-G07-06 |
| F677–678 | 2 | needs_closer_inspection | ART-G07-01 / ART-G07-07 |

## 后续核查与范围

53帧优先查原始人物层、原画索引或排除后期后的稳定描线差，解决01/07和02/14各自编号。已经确认有现有画型对应，不因唯一ID未知就自动新增付费稿。

这不是API新稿美术验收，也未做最终1080p注册、M06新稿动态播放或全片验证。175帧接触表已看、122具体绑定、53待核的边界都保留；不能据此声称1929未归属曝光或全片任务完成。

