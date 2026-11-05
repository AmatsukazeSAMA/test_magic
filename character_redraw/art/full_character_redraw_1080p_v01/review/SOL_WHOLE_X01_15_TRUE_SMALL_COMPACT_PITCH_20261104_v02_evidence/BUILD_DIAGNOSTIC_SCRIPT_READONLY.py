from pathlib import Path
import json
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
p=B/"review/SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01_evidence/PREPARE_READONLY_DIAGNOSTICS.py"
s=p.read_text(encoding="utf-8")
s=s.replace("whole_imggen_restore_normal_large_turn_volume_keep_thin_band_v01","whole_imggen_restore_true_small_keep_normal_volume_compact_pitch_v02").replace("SOL_WHOLE_X01_15_NORMAL_VOLUME_THIN_RIBBON_20261104_v01","SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02").replace("f55ac32a894b384697e37f677f3580219b6282d91fcbb42abfceb49a78fc0392","fa114462dad743a35cc4a36a1d3ab980076fd7d199041914beb38fdb98736f9c")
D=B/"review/SOL_WHOLE_X01_15_TRUE_SMALL_COMPACT_PITCH_20261104_v02_evidence";D.mkdir(parents=True,exist_ok=True)
(D/"PREPARE_READONLY_DIAGNOSTICS.py").write_text(s,encoding="utf-8")

