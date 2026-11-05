from pathlib import Path
from PIL import Image
B=Path(__file__).resolve().parents[3]
for n,m in [(64,213),(65,216)]:
 d=B/f'drawings/ART-G12-{n}/v01/private_source_diagnostics';d.mkdir(exist_ok=False)
 Image.open(B/f'inputs/motion_reference_upright_first10_20261031_v01/frames/R{m:06d}.png').crop([592,180,660,252]).resize((408,432),Image.Resampling.NEAREST).save(d/f'R{m}_NAPE_PHASE_READONLY_6x.png')
