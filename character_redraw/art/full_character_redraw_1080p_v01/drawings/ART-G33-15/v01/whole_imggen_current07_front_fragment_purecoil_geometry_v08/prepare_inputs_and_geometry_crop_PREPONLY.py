from pathlib import Path
from PIL import Image
import json,hashlib,shutil
P=Path(__file__).resolve().parent
B=P.parents[3];CEL=P.parent
V07=CEL/'whole_imggen_source2365_farLEFT_hiddenroot_frontedge_body580_v07'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rec(p):return dict(path=str(p),sha256=sha(p),bytes=Path(p).stat().st_size)
(P/'inputs').mkdir(exist_ok=True)
target=V07/'character_imggen_original.png'
assert sha(target)=='6edee7360ef5b4cb000e0083980e6ef7d7fbc5ed3caa6a3ba6024a704e40df55'
ref1=P/'inputs/ref1_KNOWN_V07_6edee736_COMPLETE_NO_REAR_CROSSING_BUT_MISSING_CURL.png';shutil.copyfile(target,ref1)
source11=B/'drawings/ART-G33-11/v01/character_api_original.png'
assert sha(source11)=='c6599b9dce03e6bfea8c5773d49c0bd0606dad0a3fdb9c22b019b1955923a487'
src=Image.open(source11).convert('RGBA')
# Candidate technical source-only crop: central turns/return, no face/root.
roi=(301,266,328,329)
candidate=P/'CANDIDATE_USER_CORRECT11_CENTRAL_TURNS_ONLY_27x63_READONLY.png';crop=src.crop(roi);crop.save(candidate)
qas=[]
for name,bg in [('white',(255,255,255,255)),('black',(0,0,0,255))]:
 comp=Image.alpha_composite(Image.new('RGBA',crop.size,bg),crop).convert('RGB')
 out=P/f'CANDIDATE_USER_CORRECT11_CENTRAL_TURNS_ONLY_{name}_10x_READONLY.png';comp.resize((270,630),Image.Resampling.NEAREST).save(out);qas.append(rec(out))
source=V07/'inputs/ref1_ORIGINAL2365_COMPLETE_UNMASKED_POSE_ONLY.png'
assert sha(source)=='0d3a358c1df91c5a9edcc00e9964163be86deea8021bb159fb344dfa4565543c'
ref3=P/'inputs/ref3_ORIGINAL2365_COMPLETE_UNMASKED_POSE_ONLY.png';shutil.copyfile(source,ref3)
dump(P/'INPUT_PROVENANCE_INITIAL_CROP_INSPECTION_PREPONLY.json',dict(id='ART-G33-15',target=rec(ref1),target_original=rec(target),target_size=Image.open(target).size,candidate_geometry=rec(candidate),candidate_geometry_original=rec(source11),candidate_crop_xyxy=roi,candidate_size=crop.size,qa=qas,ref3=rec(ref3),geometry_approval_source='User explicitly accepted oldG33-11 c659 shape; candidate is only internalturn fragment and cannot specify root/placement/mass.',art_pixels_modified=False,PREPONLY=True,native_calls=0,API_calls=0,HTTP_calls=0))
print(json.dumps(dict(run=str(P),candidate=rec(candidate),qa=qas),ensure_ascii=False))
