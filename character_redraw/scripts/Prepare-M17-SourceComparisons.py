"""Prepare explicit printed-portrait reuse nominations, not binding decisions."""
from pathlib import Path
import json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
frames=[2153,2170,2190,2210,2230,2248,2249,2252]
spec={'chapter':'M17','output_directory':str(base/'coverage/review/M17_portrait_source_comparison_v01'),
 'scope':'Printed brooch portrait is in all-character scope via existing OPT-BROOCH-PORTRAIT. Compare source facial ink, not gold glints/camera/FX. Nominations only.',
 'nominations':[{'canonical_id':'OPT-BROOCH-PORTRAIT','start_frame':f,'end_frame':f,
 'canonical_diagnostic_crop_xyxy':[825,285,1125,660],
 'current_diagnostic_crop_xyxy':[825,285,1125,660],
 'note':'Partial visible printed portrait behind orange FX' if f>=2249 else 'Printed portrait behind locket tint/glints and whole-prop camera'} for f in frames]}
target=base/'coverage/review/M17_PORTRAIT_REUSE_NOMINATIONS_v01.json'
if target.exists(): raise SystemExit('Preserve existing nominations.')
target.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target)
