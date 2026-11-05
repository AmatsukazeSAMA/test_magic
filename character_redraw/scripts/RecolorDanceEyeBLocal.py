"""Apply the user-approved B color field to reviewed native iris interiors."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

METHOD = 'approved_dance_B_reference_field'
read = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ev = lambda p: {'path': str(Path(p).resolve()), 'sha256': sha(p)}


def render(root, original, spec):
    policy = read(root/'image_defaults.json')['dance_eye_style_policy']
    assert policy == spec['B_style_acceptance'] and sha(policy['path']) == policy['sha256']
    accepted = read(policy['path'])
    assert spec['id'] in accepted['known_dance_state_ids']
    assert original.mode == 'RGBA' and list(original.size) == spec['input_dimensions']
    assert spec['root_mask_reviewed'] and spec['eyes']
    before = np.asarray(original)
    after = before.copy()
    allowed = np.zeros(before.shape[:2], bool)
    protected = allowed.copy()
    fields = {f['name']: f for f in accepted['color_fields']}
    for eye in spec['eyes']:
        assert eye['mask_reviewed'] and eye['expression_reviewed'] and eye['expression_classification'] == 'normal_open'
        masks = []
        for k in ('interior_mask', 'protected_glint_mask'):
            ref = eye[k]; assert sha(ref['path']) == ref['sha256']
            mask = Image.open(ref['path']); assert mask.mode == 'L' and mask.size == original.size
            a = np.asarray(mask); assert np.isin(a, (0,255)).all()
            masks.append(a == 255)
        m, g = masks
        assert m.any() and not (m & (g | allowed | protected)).any() and not (g & allowed).any()
        allowed |= m; protected |= g
        f = fields[eye['name']]; field_ref = f['image']
        assert sha(field_ref['path']) == field_ref['sha256']
        field = np.asarray(Image.open(field_ref['path']).convert('RGB'), dtype=float)
        y,x = np.where(m); cx,cy = eye['center_xy']; dx,dy = eye['down_unit_xy']
        assert abs(dx*dx+dy*dy-1) < 1e-6
        u=(x-cx)*dy-(y-cy)*dx; v=(x-cx)*dx+(y-cy)*dy
        u0,v0,u1,v1=eye['baseline_adaptation']['own_actual_filled_iris_local_bounds_uv']
        assert u1>u0 and v1>v0
        a0,b0,a1,b1=f['reference_local_bounds_uv']
        a=a0+(u-u0)/(u1-u0)*(a1-a0); b=b0+(v-v0)/(v1-v0)*(b1-b0)
        cx,cy=f['reference_center_xy']; dx,dy=f['reference_down_unit_xy']; x0,y0,*_=f['reference_roi_xyxy']
        rx=np.clip(cx+a*dy+b*dx-x0,0,field.shape[1]-1)
        ry=np.clip(cy-a*dx+b*dy-y0,0,field.shape[0]-1)
        ix=rx.astype(int); iy=ry.astype(int)
        jx=np.minimum(ix+1,field.shape[1]-1); jy=np.minimum(iy+1,field.shape[0]-1)
        fx=(rx-ix)[:,None]; fy=(ry-iy)[:,None]
        after[y,x,:3]=np.rint((1-fx)*(1-fy)*field[iy,ix]+fx*(1-fy)*field[iy,jx]+(1-fx)*fy*field[jy,ix]+fx*fy*field[jy,jx]).astype(np.uint8)
    assert np.array_equal(before[~allowed],after[~allowed])
    assert np.array_equal(before[protected],after[protected])
    assert np.array_equal(before[...,3],after[...,3])
    return after, allowed, protected


def main():
    from EyeLocalPolicy import inherit_passed_art_for_scoped_eye
    p=argparse.ArgumentParser(__doc__);p.add_argument('--spec',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args(); root=Path(__file__).resolve().parent.parent
    spec=read(args.spec);src=Path(spec['input']['path']);assert sha(src)==spec['input']['sha256']
    inherited=inherit_passed_art_for_scoped_eye(root,src,spec)
    im=Image.open(src);after,allowed,protected=render(root,im,spec)
    changed=np.any(np.asarray(im)!=after,axis=2)
    out=args.out.resolve();out.relative_to(src.parent.parent);out.mkdir(exist_ok=False)
    output=out/'character_eye_gray_local.png'; Image.fromarray(after).save(output)
    assert np.array_equal(np.asarray(Image.open(output)),after) and sha(src)==spec['input']['sha256']
    Image.fromarray(changed.astype(np.uint8)*255).save(out/'changed_pixels_mask.png')
    for label in ('white','black'):
        bg=Image.new('RGBA',im.size,label);bg.alpha_composite(Image.fromarray(after));bg.convert('RGB').save(out/f'qa_{label}.png')
    report={'method':METHOD,'source':spec['input'],'output':ev(output),'spec':ev(args.spec),'B_style_acceptance':spec['B_style_acceptance'],
            'inherited_art':inherited,'allowed_pixels':int(allowed.sum()),'protected_glints':int(protected.sum()),'changed_pixels':int(changed.sum()),
            'outside_mask_changed_pixels':0,'alpha_changed_pixels':0,'protected_glint_changed_pixels':0,'API_calls':0,'whole_art_acceptance':False}
    (out/'VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
