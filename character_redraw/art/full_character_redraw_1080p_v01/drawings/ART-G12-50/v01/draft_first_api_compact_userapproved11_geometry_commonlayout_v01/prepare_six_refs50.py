from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
RUN=Path(__file__).parent;CEL=RUN.parent;BASE=RUN.parents[3];INP=RUN/'inputs';INP.mkdir(exist_ok=True)
PREF=CEL/'preflight_source_layout_hair_only_HOLD_v01';prior=BASE/'drawings/ART-G12-49/v01/draft_first_api_compact_userapproved11_geometry_commonlayout_v01/inputs'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(p):return {'path':str(p),'sha256':sha(p)}
specs=[
 (PREF/'inputs/ORIGINAL50_COMMON_LAYOUT_OPEN_EYES_TINY_O_HIGH_OK_LOOP_LOW_DROOP_HAND_READONLY.png','ref1_ORIGINAL50_COMMON_HIGH_OK_LOOP_THREE_FINGERS_LOW_DROOP_HAND.png','9c8e050186ad8d37b6687099079bf35e9357f1761a2b7fdcd1887a86c1673c6f'),
 (PREF/'inputs/R157_HAIR_ONLY_READONLY.png','ref2_R157_HAIR_ONLY_RECOIL_NOT_GEOMETRY.png','c21eeaa362ecc3ccd8f141066159a8dabde9c756bd5cc6aab4a8925680167bec'),
 (prior/'ref3_OLD11_GRAY_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_NO_COIL.png','ref3_OLD11_BOB_CAP_LOW_BEADS_IDENTITY_ONLY_NO_COIL.png','053477b15810b54c1458a56d912c137a6ee1bdbd8a3904044eb0f95ac1e620a3'),
 (BASE/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png','ref4_USER_APPROVED11_CONTINUOUS_SPIRAL_TAPER_TERMINAL_CURL.png','13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959'),
 (BASE/'inputs/eye_G02-01_F100.png','ref5_G02_SINGLE_CHARCOAL_EYE_METHOD_ONLY.png','6019c1afe7863ce6896b78df95004b678a0d6169a8081c8caf9ca367809e19f0'),
 (BASE/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png','ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png','d1428b1355eea47a80be7bb541fd50d85d81ca120715e3b2b2480e2cd72c1ae0')]
rows=[]
for src,name,expected in specs:
    assert sha(src)==expected;dest=INP/name;assert not dest.exists();shutil.copyfile(src,dest)
    rows.append({'source':str(src),'source_sha256':expected,'path':str(dest),'sha256':sha(dest),'operation':'exact bytecopy of reviewedreadonly input'})
record={'id':'ART-G12-50','created_at_utc':datetime.now(timezone.utc).isoformat(),'references':rows,'source_hair_provenance':evidence(PREF/'SOURCE_LAYOUT_HAIR_ONLY_PREFLIGHT_PROVENANCE.json'),'source_actual_review':evidence(PREF/'SOURCE_HAIR_ACTUAL_REVIEW_HOLD.json'),'source_guide_size':[848,976],'compact_crop_xyxy':[16,0,736,976],'source_canvas':[720,976],'trim_transform':{'scale':1,'translation':[-16,0],'per_part_transform':False},'API_calls':0,'native_calls':0,'submitted':False,'central_write':False}
dest=RUN/'SIX_REFERENCE_PROVENANCE.json';assert not dest.exists();dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provenance':evidence(dest),'ref_sha256':[v['sha256'] for v in rows],'calls':0},ensure_ascii=False))
