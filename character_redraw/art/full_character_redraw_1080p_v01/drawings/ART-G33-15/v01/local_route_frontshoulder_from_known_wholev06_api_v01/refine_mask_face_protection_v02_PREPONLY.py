from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
base=P/'build_route_mask_PREPONLY.py'
script=base.read_text(encoding='utf-8')
fix="""# Preserve original visible face/chin and its outline. This is a technical
# mask correction following the v01 rectangular face-protection assertion;
# all v01 mask and QA outputs remain preserved.
faceprotect=Image.new('L',(w,h))
ImageDraw.Draw(faceprotect).polygon([(516,318),(528,324),(556,323),(566,311),(580,280),(600,280),(600,334),(516,334)],fill=255)
protected_face=np.array(faceprotect)>0
oldarr[protected_face]=False
newarr[protected_face]=False
edit=oldarr|newarr
"""
assert script.count('edit=oldarr|newarr')==1
script=script.replace('edit=oldarr|newarr',fix)
script=script.replace('FRONT_EXPOSURE_v01.png','FRONT_EXPOSURE_v02.png')
script=script.replace("f'PREP_PRIOR_CANDIDATE_c03c252b_MASK_OVERLAY_", "f'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_OVERLAY_")
script=script.replace("'PREP_PRIOR_CANDIDATE_c03c252b_MASK_ALPHA_", "'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_ALPHA_")
script=script.replace("'PREP_PRIOR_CANDIDATE_c03c252b_PROTECTED_HEAD_BODY_FULL_QA.png'", "'PREP_PRIOR_CANDIDATE_c03c252b_MASKv02_PROTECTED_HEAD_BODY_FULL_QA.png'")
script=script.replace("'QA_OLD_ROUTE_EDIT_REGION_ONLY_NOT_ART.png'", "'QA_OLD_ROUTE_EDIT_REGION_ONLY_NOT_ART_v02.png'")
script=script.replace("'QA_FRONT_CAPACITY_REGION_ONLY_NOT_ART.png'", "'QA_FRONT_CAPACITY_REGION_ONLY_NOT_ART_v02.png'")
script=script.replace("assert not np.any(edit[285:330,520:580]) # visible face/chin remains protected", "assert not np.any(edit[protected_face]) # actual visible face/chin protection polygon")
script=script.replace("'MASK_PROVENANCE_PREPONLY_v01.json'", "'MASK_PROVENANCE_PREPONLY_v02.json'")
# Earlier v01 files were mask/QA inputs only, never artist-output pixels.
(P/'MASK_v01_TECHNICAL_VALIDATION_FAILURE_PRESERVED.json').write_text(json.dumps(dict(status='v01_mask_only_face_rectangle_assertion_failed',source_builder=str(base),source_builder_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),network_calls=0,api_calls=0,native_calls=0,art_pixels_changed=False,preserved_v01_mask='mask_V06_OLD_REAR_ROUTE_REMOVE_NEW_FRONT_EXPOSURE_v01.png',v02_change='Explicit unchanged-face polygon protection; no final art edits.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v2=P/'build_route_mask_v02_EXPANDED_SOURCE_PREPONLY.py'
assert not v2.exists()
v2.write_text(script,encoding='utf-8')
exec(compile(script,str(v2),'exec'))
