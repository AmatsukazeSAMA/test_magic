from pathlib import Path
from PIL import Image
import hashlib,json
from datetime import datetime,timezone
BASE=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
tasks=[
 ('ART-G12-50',[
 ('RETURN_OK_LOOP_THREE_UPRIGHT_FINGERS','qa_white.png',[45,103,213,295]),
 ('RETURN_OK_LOOP_THREE_UPRIGHT_FINGERS_BLACK','qa_black.png',[45,103,213,295]),
 ('RETURN_LOW_DROOP_HAND','qa_white.png',[206,469,438,587]),
 ('RETURN_LOW_EAR_ROOT_SPIRAL','qa_white.png',[530,265,627,497]),
 ('RETURN_LOW_EAR_ROOT_SPIRAL_BLACK','qa_black.png',[530,265,627,497]),
 ('RETURN_OPEN_EYES_TINY_O','qa_white.png',[350,174,565,332]),
 ('SOURCE50_OK_LOOP','inputs/source_pose_guide.png',[61,103,229,295]),
 ('SOURCE50_LOW_HAND','inputs/source_pose_guide.png',[222,469,454,587])]),
 ('ART-G33-13',[
 ('RETURN_BACK_PROFILE_EAR_HIGH_BEAD_ROOT','qa_white.png',[210,113,364,265]),
 ('RETURN_BACK_PROFILE_EAR_HIGH_BEAD_ROOT_BLACK','qa_black.png',[210,113,364,265]),
 ('RETURN_COMPLETE_CALVES_ANKLES_SHOES','qa_white.png',[192,791,491,1042]),
 ('RETURN_COMPLETE_CALVES_ANKLES_SHOES_BLACK','qa_black.png',[192,791,491,1042]),
 ('RETURN_FOLDED_HAND','qa_white.png',[103,294,185,395]),
 ('RETURN_WAIST_HAND_BOW_CONTACT','qa_white.png',[332,384,415,520]),
 ('SOURCE13_PROFILE_EAR_NAPE','inputs/source_pose_guide.png',[210,137,364,265]),
 ('SOURCE13_COMPLETE_CALVES_ANKLES_SHOES','inputs/source_pose_guide.png',[192,791,491,1042])])]
for asset,specs in tasks:
    cel=BASE/'drawings'/asset/'v01';out=cel/'artist_return_diagnostics_v01';out.mkdir(exist_ok=False);rows=[]
    for label,name,xyxy in specs:
        src=cel/name;crop=Image.open(src).crop(xyxy)
        for factor in (1,3):
            dest=out/f'{label}_{factor}x.png';(crop if factor==1 else crop.resize((crop.width*factor,crop.height*factor),Image.Resampling.NEAREST)).save(dest)
            rows.append({'path':str(dest),'sha256':sha(dest),'source':str(src),'source_sha256':sha(src),'crop_xyxy':xyxy,'scale':factor,'operation':'readonlydiagnostic crop andnearest enlargement; no finalart paint/warp'})
    record={'id':asset,'created_at_utc':datetime.now(timezone.utc).isoformat(),'raw_sha256':sha(cel/'character_api_original.png'),'rows':rows,'new_generation_calls':0,'art_modified':False}
    dest=out/'DIAGNOSTIC_PROVENANCE.json';dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'id':asset,'path':str(dest),'sha256':sha(dest)},ensure_ascii=False))
