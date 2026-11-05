from pathlib import Path
from PIL import Image
import hashlib, json
from datetime import datetime, timezone

BASE = Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
OUT = Path(__file__).parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
specs = [
    ('USER_PHOTO1', Path(r'C:\Users\11515\.codex\codex-remote-attachments\01a18c9e-c795-7c41-9eed-612ceab2f81f\1789DC91-0C1D-4479-9E59-B5BFD568BC63\1-照片-1.jpg'), [280,252,345,377]),
    ('OLD3311_API', BASE/'drawings/ART-G33-11/v01/character_api_original.png', [280,252,345,377]),
    ('OLD3311_WHITE', BASE/'drawings/ART-G33-11/v01/qa_white.png', [280,252,345,377]),
    ('OLD3311_BLACK', BASE/'drawings/ART-G33-11/v01/qa_black.png', [280,252,345,377]),
    ('REJECTED_NEW3311_RAW', BASE/'drawings/ART-G33-11/v01/whole_imggen_source_layout_09lowroot_unlit_v01/character_imggen_original.png', [458,420,550,518]),
    ('REJECTED_NEW3311_WHITE', BASE/'drawings/ART-G33-11/v01/whole_imggen_source_layout_09lowroot_unlit_v01/qa_white.png', [458,420,550,518]),
    ('REJECTED_NEW3311_BLACK', BASE/'drawings/ART-G33-11/v01/whole_imggen_source_layout_09lowroot_unlit_v01/qa_black.png', [458,420,550,518]),
]
rows=[]
for label, src, xyxy in specs:
    im=Image.open(src)
    crop=im.crop(xyxy)
    paths=[]
    for factor in (1,4):
        target=OUT/f'{label}_COIL_TURNS_ONLY_{factor}x.png'
        if target.exists(): raise FileExistsError(target)
        (crop if factor==1 else crop.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST)).save(target)
        paths.append({'path':str(target),'sha256':sha(target),'scale':factor,'interpolation':'none' if factor==1 else 'nearest-neighbor diagnostic only'})
    rows.append({'label':label,'source':str(src),'source_sha256':sha(src),'source_size':list(im.size),'source_mode':im.mode,'crop_xyxy':xyxy,'crop_role':'Read-only comparison; root/head/body deliberately excluded. Not a submitted image reference or accepted material master.','outputs':paths})
record={'created_at_utc':datetime.now(timezone.utc).isoformat(),'operation':'read_only_source_crop_and_diagnostic_enlargement','art_generation_calls':0,'final_art_pixels_changed':False,'geometry_lock_source':'User explicitly selected Photo1; visible old3311 spiral geometry only.','rows':rows,'not_submission':True,'not_default_reference':True}
target=OUT/'DIAGNOSTIC_PROVENANCE.json'
if target.exists(): raise FileExistsError(target)
target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'diagnostics':str(target),'sha256':sha(target),'crops':len(rows)*2},ensure_ascii=False))
