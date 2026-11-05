from pathlib import Path
from PIL import Image
import hashlib, json
from datetime import datetime, timezone

BASE=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
OUT=Path(__file__).parent
RUN12=OUT.parent
RUN48=BASE/'drawings/ART-G12-48/v01/preflight_source_layout_hair_only_HOLD_v01'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, data):
    if p.exists(): raise FileExistsError(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'path':str(p),'sha256':sha(p)}

sources={
 'user_photo1':Path(r'C:\Users\11515\.codex\codex-remote-attachments\01a18c9e-c795-7c41-9eed-612ceab2f81f\1789DC91-0C1D-4479-9E59-B5BFD568BC63\1-照片-1.jpg'),
 'old_raw':BASE/'drawings/ART-G33-11/v01/character_api_original.png',
 'old_white':BASE/'drawings/ART-G33-11/v01/qa_white.png',
 'old_black':BASE/'drawings/ART-G33-11/v01/qa_black.png',
 'rejected_new_raw':BASE/'drawings/ART-G33-11/v01/whole_imggen_source_layout_09lowroot_unlit_v01/character_imggen_original.png',
 'rejected_new_white':BASE/'drawings/ART-G33-11/v01/whole_imggen_source_layout_09lowroot_unlit_v01/qa_white.png',
 'rejected_new_black':BASE/'drawings/ART-G33-11/v01/whole_imggen_source_layout_09lowroot_unlit_v01/qa_black.png'}
assert sha(sources['old_raw'])=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'
assert sha(sources['rejected_new_raw'])=='ade931130d241385efbe7df2b5df1c206b311f577ddc9da38d63f5cd92ec33da'
assert sha(RUN12/'request_imggen.json')=='3deb46ea94ab5f47ba519e5d5e9a8d8237c97feb648e2d31981ddbf95e07472d'

crops=[]
for label in ['user_photo1','old_raw','old_white','old_black']:
    src=sources[label]; xyxy=[280,260,345,377]
    im=Image.open(src).crop(xyxy)
    outputs=[]
    for factor in (1,4):
        p=OUT/f'{label.upper()}_STRICT_NO_BEADS_NO_HEAD_TURNS_CURL_{factor}x.png'
        if p.exists(): raise FileExistsError(p)
        (im if factor==1 else im.resize((im.width*factor,im.height*factor),Image.Resampling.NEAREST)).save(p)
        outputs.append({'path':str(p),'sha256':sha(p),'scale':factor})
    crops.append({'source':str(src),'source_sha256':sha(src),'crop_xyxy':xyxy,'role':'Read-only candidate comparison: visible continuous tapering spiral and terminal curl only, no root/head/body authority; not submitted/default reference. Material appearance not adopted as unlit pigment authority.','outputs':outputs})

prov=write(OUT/'STRICT_TURNS_ONLY_CANDIDATE_PROVENANCE.json',{
 'created_at_utc':datetime.now(timezone.utc).isoformat(),'crops':crops,'pixel_operation':'Exact source crop; 4x nearest-neighbor diagnostic only; no painting, alpha edits, recolor or final-art change.',
 'earlier_diagnostic_crop_boundary_caveat':'The initial comparison xyxy[280,252,345,377] (and new3311 xyxy[458,420,550,518]) retains a small red bead fragment at top. It is contextual diagnostic only and must not be submitted as a no-root reference. These strict candidate crops move old3311 top edge to260. Earlier files preserved, not overwritten.',
 'reference_status':'UNREVIEWED_PRIVATE_CANDIDATE_NOT_SUBMITTED','calls':0})
print(json.dumps({'strict_candidate_provenance':prov,'awaiting_actual_strict_crop_view_before_addendum':True},ensure_ascii=False))
