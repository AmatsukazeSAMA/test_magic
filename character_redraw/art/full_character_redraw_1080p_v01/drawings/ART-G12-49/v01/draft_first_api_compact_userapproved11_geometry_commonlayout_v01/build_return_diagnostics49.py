from pathlib import Path
from PIL import Image
import hashlib,json
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;OUT=CEL/'artist_return_diagnostics_v01';OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows=[]
specs=[
 ('RETURN_LOW_EAR_ROOT_COMPACT_SPIRAL','qa_white.png',[450,315,575,500]),
 ('RETURN_LOW_EAR_ROOT_COMPACT_SPIRAL_BLACK','qa_black.png',[450,315,575,500]),
 ('RETURN_OPEN_EYES_TINY_O','qa_white.png',[294,204,497,361]),
 ('RETURN_DISTINCT_LOWLEFT_HANDS','qa_white.png',[16,376,293,590]),
 ('SOURCE49_DISTINCT_LOWLEFT_HANDS','inputs/source_pose_guide.png',[32,376,309,590]),
 ('SOURCE49_FACE_EYES_TINY_O','inputs/source_pose_guide.png',[280,184,535,405])]
for label,name,xyxy in specs:
    src=CEL/name;crop=Image.open(src).crop(xyxy)
    for factor in (1,3):
        dest=OUT/f'{label}_{factor}x.png'
        (crop if factor==1 else crop.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST)).save(dest)
        rows.append({'path':str(dest),'sha256':sha(dest),'source':str(src),'source_sha256':sha(src),'crop_xyxy':xyxy,'scale':factor,'operation':'read-only diagnostic crop; no art edit or partalignment'})
src=CEL/'inputs/source_pose_guide.png';dest=OUT/'SOURCE49_ORIGINAL_GUIDE_COMPACT_WINDOW_1x.png';Image.open(src).crop([16,0,672,1040]).save(dest)
rows.append({'path':str(dest),'sha256':sha(dest),'source':str(src),'source_sha256':sha(src),'crop_xyxy':[16,0,672,1040],'scale':1,'operation':'read-only samecompactwindow forsourcecomparison, oldredhead remains diagnostic only'})
record={'id':'ART-G12-49','created_at_utc':datetime.now(timezone.utc).isoformat(),'raw_sha256':sha(CEL/'character_api_original.png'),'rows':rows,'art_generation_calls':0,'final_art_modified':False}
dest=OUT/'DIAGNOSTIC_PROVENANCE.json';dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(dest),'sha256':sha(dest)},ensure_ascii=False))
