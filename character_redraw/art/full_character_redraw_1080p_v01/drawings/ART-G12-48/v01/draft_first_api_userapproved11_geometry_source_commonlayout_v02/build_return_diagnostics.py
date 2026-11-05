from pathlib import Path
from PIL import Image
import json,hashlib
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;OUT=CEL/'artist_return_diagnostics_v01';OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows=[]
specs=[
 ('RETURN_HEAD_LOW_EAR_ROOT_COIL','qa_white.png',[380,222,527,451]),
 ('RETURN_HEAD_LOW_EAR_ROOT_COIL_BLACK','qa_black.png',[380,222,527,451]),
 ('RETURN_OPEN_MONO_EYES','qa_white.png',[206,179,427,285]),
 ('RETURN_DISTINCT_MOUTH_COVER_HANDS','qa_white.png',[105,265,372,450]),
 ('SOURCE48_EYES_HANDS','inputs/source_pose_guide.png',[105,215,437,485]),
 ('SOURCE48_WAIST_APRON_BOTTOM','inputs/source_pose_guide.png',[112,622,630,944]),
 ('RETURN48_WAIST_APRON_BOTTOM','qa_white.png',[112,602,630,944])]
for label,name,xyxy in specs:
    src=CEL/name;im=Image.open(src);crop=im.crop(xyxy)
    for factor in (1,3):
        dest=OUT/f'{label}_{factor}x.png'
        (crop if factor==1 else crop.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST)).save(dest)
        rows.append({'path':str(dest),'sha256':sha(dest),'source':str(src),'source_sha256':sha(src),'crop_xyxy':xyxy,'scale':factor,'operation':'read-only diagnostic crop/enlargement, no final art edit or geometric alignment'})
record={'created_at_utc':datetime.now(timezone.utc).isoformat(),'id':'ART-G12-48','raw_image':str(CEL/'character_api_original.png'),'raw_sha256':sha(CEL/'character_api_original.png'),'rows':rows,'new_generations':0,'art_modified':False}
dest=OUT/'DIAGNOSTIC_PROVENANCE.json';dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':str(dest),'sha256':sha(dest),'raw_sha256':record['raw_sha256']},ensure_ascii=False))
