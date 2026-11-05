from pathlib import Path
from PIL import Image
import json
import hashlib

R=Path(__file__).resolve().parent
B=R.parents[3]
rows=[('ART-G12-37','whole_imggen_source956_connectedgray_occlusion_v02',[565,470,710,700]),('ART-G12-38','whole_imggen_source963_connectedgray_occlusion_v02',[535,410,695,625]),('ART-G12-39','whole_imggen_source966_connectedgray_occlusion_v02',[605,375,755,610])]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for id,run,xy in rows:
    dest=B/'drawings'/id/'v01'/run
    source=dest.parent/'whole_imggen_flat_motion_v01'
    records=[]
    for bg in ['white','black']:
        original=source/f'qa_{bg}.png'
        with Image.open(original) as im:
            crop=im.crop(xy)
        for scale in [1,3]:
            out=dest/f'READONLY_CURRENT_COIL_{bg}_{scale}x.png'
            assert not out.exists()
            (crop if scale==1 else crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST)).save(out)
            records.append({'path':str(out),'sha256':sha(out),'source_path':str(original),'source_sha256':sha(original),'source_crop_xyxy':xy,'scale':scale,'read_only_diagnostic_not_generation_reference':True})
    f=dest/'READONLY_COIL_DIAGNOSTIC_PROVENANCE.json';assert not f.exists()
    f.write_text(json.dumps({'id':id,'diagnostics':records,'no_character_art_pixels_modified':True,'calls':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(id,sha(f))
