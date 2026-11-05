# PV 制作依赖盘点

工作区 D:\CODEX\魔术之心。扫描至 2026-11-05T13:52:16.324354+00:00。

工作区快照含 78,694 个文件，逻辑体量 21.056 GiB。排除本审计两文件。包括正在生成的 handoff 发布副本，快照非原子，逻辑体量含重复内容。

## 原工程与发布副本

| 分区 | 文件数 | 逻辑体量 |
| --- | ---: | ---: |
| original_workspace_tree_excluding_handoff_staging | 33,676 | 9.887 GiB |
| handoff_reports_outside_publish_copy | 5 | 0.001 GiB |
| git_database_inside_handoff_staging | 32 | 0.001 GiB |
| handoff_publish_repo_staging_copy | 44,981 | 11.167 GiB |

## 最新交接要求

- G33-16 红珠按原 bob、耳后与头颈投影自然遮住，不为露珠而抬高或外移。
- 两颗红珠横向并列，允许自然透视小错位。明显竖叠列 HOLD。
- 两大卷后须有独立小灰卷正面及实际返回，随后接短 C。C 自身不能充作小卷。

## 收集优先级

原 PV、原 handoff 分镜原画、PTS、音频、遮罩及合成输入是制作入口。已找到原片与参考片、284 个 C 盘生成原图、桌面360视频和运动参考视频的工作区内容镜像。原 source tree 的 JSON 等元数据也按内容校验是否已镜像。

仅以下已存在媒体尚未找到工作区镜像。它属于 G33-12 分辨率诊断历史参考，接手时保留即可。

- C:\Users\11515\AppData\Local\Temp\codex-clipboard-0629419d-5b54-4a87-ade6-d12178d95d30.png，475,503 bytes。

被引用 Codex 会话日志合计约8.1GB，仅供历史记录引用，不是渲染入口或 PV 生产素材，不因 JSON 指向它们就要求上传。动态计算路径仍需接手环境解析。

## 文件类型

| 扩展名 | 文件数 | 逻辑体量 |
| --- | ---: | ---: |
| .png | 45,547 | 15.884 GiB |
| .json | 23,980 | 2.443 GiB |
| .zip | 24 | 1.654 GiB |
| .mp4 | 157 | 0.706 GiB |
| .jpg | 1,003 | 0.265 GiB |
| .jsonl | 564 | 0.053 GiB |
| .html | 18 | 0.016 GiB |
| .py | 1,314 | 0.009 GiB |
| .txt | 3,730 | 0.008 GiB |
| .before | 68 | 0.003 GiB |
| .md | 1,326 | 0.003 GiB |
| .gif | 2 | 0.002 GiB |
| .log | 262 | 0.002 GiB |
| .csv | 22 | 0.002 GiB |
| .ps1 | 602 | 0.002 GiB |
| <none> | 19 | 0.001 GiB |
| .js | 2 | 0.001 GiB |
| .ffconcat | 8 | 0.000 GiB |
| .pyc | 13 | 0.000 GiB |
| .sample | 14 | 0.000 GiB |
| .cjs | 4 | 0.000 GiB |
| .before_entries_unwrap | 2 | 0.000 GiB |
| .cs | 6 | 0.000 GiB |
| .css | 1 | 0.000 GiB |
| .sha256 | 6 | 0.000 GiB |

## 超过 50 MiB 的文件

- D:\CODEX\魔术之心\art\20261102_first_dance_66states_review_v01.zip，342,890,238 bytes。
- D:\CODEX\魔术之心\deliverables\handoff_20261105\publish_repo\character_redraw\art\20261102_first_dance_66states_review_v01.zip，342,890,238 bytes。
- D:\CODEX\魔术之心\art\20261102_first_dance_66states_review_v02.zip，342,545,393 bytes。
- D:\CODEX\魔术之心\deliverables\handoff_20261105\publish_repo\character_redraw\art\20261102_first_dance_66states_review_v02.zip，342,545,393 bytes。
- D:\CODEX\魔术之心\deliverables\handoff_20261105\publish_repo\character_redraw\deliverables\舞蹈原片与替换帧_20261031_v01.zip，99,884,019 bytes。
- D:\CODEX\魔术之心\deliverables\舞蹈原片与替换帧_20261031_v01.zip，99,884,019 bytes。
- D:\CODEX\魔术之心\deliverables\handoff_20261105\publish_repo\magic_maid_20261029\overlay_sequences\subtitles_s06.zip，87,790,317 bytes。

## 外目录收集入口

- D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029。原片、参考片、cels、timing/PTS、data、音频、overlays、overlay_sequences 与合成资产。若 publish_repo 内已按同 SHA 汇集，保留路径映射。
- D:/CODEX/手书素材/magic_maid_20261029 与 D:/downloads。原视频来源，已有27MB/39MB镜像可复用。
- C:/Users/11515/.codex/generated_images。284 个被引用生成 PNG 均有经过内容校验的工作区镜像。
- C:/Users/11515/AppData/Local/Temp。被引用20个临时 PNG，19个已有镜像，上列剩余1个可归档。
- C:/Users/11515/Desktop 与 .codex/attachments。桌面360、用户运动参考均有工作区镜像。
- 外目录逐项文件路径、存在性、大小、引用来源和对应工作区镜像见 JSON，目录体量只累计被引用文件。

## 外部引用分类

| 类别 | 引用路径数 | 现存文件 | 缺失路径 | 已验证镜像 |
| --- | ---: | ---: | ---: | ---: |
| temporary_user_attachment | 20 | 20 | 0 | 19 |
| PV_original_handoff_source_tree | 476 | 473 | 0 | 436 |
| tool_or_runtime | 23 | 19 | 2 | 0 |
| other_production_media | 5 | 5 | 0 | 5 |
| generated_original_external | 285 | 284 | 0 | 284 |
| desktop_media_reference | 1 | 1 | 0 | 1 |
| external_metadata_code_or_record | 12 | 5 | 1 | 0 |
| Codex_conversation_history_not_PV_entry | 3 | 3 | 0 | 0 |

## 环境与文档差异

- ffmpeg/ffprobe 的绝对路径包括 GPT-SoVITS runtime 和 D:/Program Files/oopz，字体指向 Windows Fonts。归入环境依赖，不归为待收集 PV 素材。
- 当前 README 的肩前表述与最新用户要求有差异，以当前用户补充和最新 HOLD 为准。审计未修改 README。
- DPAPI 密钥和私人配置不纳入素材上传。只写本审计两个文件，没有联网、复制媒体、修图、生图或修改中央登记。
- JSON 解析失败计数保留在 extraction，部分一次性 dispatch 标记并非有效 JSON。原始 base64 API 响应和超35MiB文本已跳过。
