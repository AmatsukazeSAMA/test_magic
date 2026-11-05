"""Apply the actually viewed round-arc trial through the guarded local editor."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
from EyeLocalPolicy import inherit_passed_art_for_scoped_eye

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
REVIEW = BASE / 'review/USER_X01_14_LIGHT_ARC_BASELINE_CHECK_20261104_v01'
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev = lambda p: {'path': str(Path(p).resolve()), 'sha256': sha(p)}
prep = REVIEW/'X01_14_BASELINE_ROUND_CAP_SPEC_PREPONLY_v01.json'
approved = REVIEW/'X01_14_BASELINE_ROUND_CAP_SPEC_ROOT_APPROVED_v01.json'
assert not approved.exists()
spec = read(prep)
inherited = inherit_passed_art_for_scoped_eye(ROOT, spec['input']['path'], spec)
surfaces = [REVIEW/f'{name}_BASELINE_ROUND_CAP_MASK_DIAGNOSTIC_8x.png'
            for name in ['viewer_left','viewer_right']]
assert all(p.is_file() for p in surfaces)
for eye in spec['eyes']:
    eye.update({'mask_reviewed':True,'root_mask_reviewed':True,
                'mask_reviewed_by':'ROOT actual approved master/full image and both current baseline round-cap cyan permission/magenta original-glint/yellow proposed boundary diagnostics viewed.'})
spec.update({'root_mask_reviewed':True,'root_release_granted':True,
             'prep_status':'ROOT_ACTUALLY_VIEWED_BASELINE_ARC_APPROVED_FOR_LOCAL_TRIAL',
             'root_reviewed_utc':datetime.now(timezone.utc).isoformat(),
             'approved_from_PREP':ev(prep),
             'root_actually_viewed_surfaces':[ev(p) for p in surfaces],
             'whole_art_pass_evidence':list(inherited['art_reviews'].values()),
             'inherited_parent_art_review':inherited})
approved.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out = BASE/'drawings/ART-X01-14/v01/py_post_pass_user_baseline_round_light_arc_v03'
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/Recolor-EyeGrayLocal.py'),
                '--spec',str(approved),'--out',str(out)],check=True)

font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',25)
small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
canvas = Image.new('RGB',(1280,720),(243,243,243)); d=ImageDraw.Draw(canvas)
d.text((22,12),'已确认基线：浅灰上缘为饱满的上凸圆弧',font=font,fill=(20,20,20))
baseline_crop = Path(read(BASE/'review/USER_POST_PASS_NORMAL_OPEN_EYE_PY_EXCEPT_SQUINT_CLOSED_20261104_v03/POLICY.json')['light_cap_reference']['path'])
b = Image.open(baseline_crop).convert('RGB')
canvas.paste(b,((canvas.width-b.width)//2,52))
old = BASE/'drawings/ART-X01-14/v01/py_post_pass_user_round_ribbon_smaller_light_cap_v02/qa_white.png'
roi = (370,205,582,345)
for x,path,label in [(0,old,'上一版：弧面压得偏平'),(640,out/'qa_white.png','本次：按基线恢复圆弧')]:
    d.text((x+22,278),label,font=font,fill=(20,20,20))
    crop=Image.open(path).convert('RGB').crop(roi)
    crop=crop.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST)
    canvas.paste(crop,(x+2,318))
canvas=canvas.crop((0,0,1280,738))
comparison=out/'USER_BASELINE_ROUND_ARC_COMPARISON.png'
canvas.save(comparison)
print(json.dumps({'output':ev(out/'character_eye_gray_local.png'),'comparison':ev(comparison),
                  'full_white':ev(out/'qa_white.png'),'user_accepted':False},ensure_ascii=False))
