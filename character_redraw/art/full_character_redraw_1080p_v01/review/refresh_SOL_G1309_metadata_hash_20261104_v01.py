from pathlib import Path
import json,hashlib
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
F=B/'review/SOL_WHOLE_G13_09_UNLIT_RETURNS_20261104_v01.json'
R=B/'drawings/ART-G13-09/v01/whole_imggen_unlit_samegray_returns_preserve_hands_v04'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads(F.read_text(encoding='utf8'))
for p in [R/'NATIVE_CALL_RECEIPT.json',R/'BUILTIN_GENERATION.json']:
 d['evidence_sha256'][str(p)]=sha(p)
d['receipt']={'provider':'built-in imagegen','logical_builtin_calls':1,'official_API_calls':0,'orchestration_elapsed_ms':70174,'orchestration_timing_basis':'Includes begin-marker-to-actual-tool gap; not image compute time','tool_reported_wall_seconds':62.6,'image_compute_seconds_exposed':False,'quality_preference':'high','quality_parameter_exposed':False,'model_parameter_exposed':False}
d['metadata_readback_note']='Root appended timing/actual-prompt verification only; raw/WB unchanged. Receipt and generation metadata SHA refreshed after reread.'
F.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'report_sha256':sha(F),'md_sha256':sha(F.with_suffix('.md')),'raw_sha256':sha(R/'character_imggen_original.png')},indent=2))
