# 普通字幕 / 特效 PNG 序列下载包

字幕按 15 个语义 S 工作包分发，特效为一个完整全片包。所有 ZIP 含普通 PNG、精确 PTS 映射及说明。
S 内顺接仅是工作索引，不是新的成片；回合成按 source_frame/source_pts。s06 完整保留全部黑裙舞蹈。
素材为扁平原片估计的可见 straight alpha，不是作者原始 alpha；空帧及复杂遮挡仍须人工审阅。

| 文件 | 轨 | 原片帧数 | 字节 |
|---|---|---:|---:|
| [effects_png.zip](effects_png.zip) | effects | 4763 | 28792142 |
| [subtitles_s01.zip](subtitles_s01.zip) | subtitles | 170 | 3062000 |
| [subtitles_s02.zip](subtitles_s02.zip) | subtitles | 486 | 4724123 |
| [subtitles_s03.zip](subtitles_s03.zip) | subtitles | 165 | 2036942 |
| [subtitles_s04.zip](subtitles_s04.zip) | subtitles | 257 | 3583615 |
| [subtitles_s05.zip](subtitles_s05.zip) | subtitles | 155 | 14476879 |
| [subtitles_s06.zip](subtitles_s06.zip) | subtitles | 1384 | 87790317 |
| [subtitles_s07.zip](subtitles_s07.zip) | subtitles | 417 | 4502492 |
| [subtitles_s08.zip](subtitles_s08.zip) | subtitles | 155 | 1813361 |
| [subtitles_s09.zip](subtitles_s09.zip) | subtitles | 177 | 3566475 |
| [subtitles_s10.zip](subtitles_s10.zip) | subtitles | 153 | 1608272 |
| [subtitles_s11.zip](subtitles_s11.zip) | subtitles | 214 | 4289268 |
| [subtitles_s12.zip](subtitles_s12.zip) | subtitles | 329 | 2622091 |
| [subtitles_s13.zip](subtitles_s13.zip) | subtitles | 85 | 2703608 |
| [subtitles_s14.zip](subtitles_s14.zip) | subtitles | 522 | 12109145 |
| [subtitles_s15.zip](subtitles_s15.zip) | subtitles | 94 | 1656632 |

逐包哈希、CRC/字节验证与覆盖范围见 [index.json](index.json)。

## 复现到新路径

先用仓库工具导出普通双轨序列，再运行：
```sh
python scripts/magic_maid_overlays.py export-sequence --category both --output magic_maid_20261029/overlay_exports/full
python scripts/magic_maid_package_overlay_sequences.py --project magic_maid_20261029 --export magic_maid_20261029/overlay_exports/full --output overlay_sequences_rebuilt --report-prefix data/OVERLAY_SEQUENCE_REBUILT
```
已有输出拒绝覆盖；完整普通导出目录属于可再生缓存，不入仓库。
