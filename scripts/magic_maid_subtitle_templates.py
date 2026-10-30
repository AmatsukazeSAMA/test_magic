#!/usr/bin/env python3
"""Bounded, source-observed refinements for the subtitle template manifest.

Run AFTER magic_maid_subtitle_overlays.py --template-plan.  This uses original
pixels and existing source-observed glyph supports, never renders a font.
It creates a new directory and marks results pending fresh native-image QA.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import magic_maid_subtitle_overlays as sub

RECIPE_VERSION = "observed-caption-timing-and-contact-support-v1"


def styled_flat_observation(rgb, box=(110,460,1840,650)):
    """Solve observed white glyph + black shadow over a verified flat plate.

    Pixel = w_white*white + w_plate*plate + w_black*black.  The two independent
    RGB coefficients determine an equivalent straight-alpha grayscale overlay.
    This is an explicit black-shadow model, not recovered author alpha.
    """
    x0,y0,x1,y1 = box
    patch = rgb[y0:y1,x0:x1]
    background = sub._modal_color(patch[::3,::3].reshape(-1,3))
    matrix = np.stack((np.ones(3), background / 255), axis=1)
    weights = (patch.astype(np.float32)/255) @ np.linalg.pinv(matrix).T
    white, plate = weights[...,0], weights[...,1]
    predicted = weights @ matrix.T
    residual = np.max(np.abs(predicted*255-patch), axis=-1)
    valid = ((white >= -.02) & (plate >= -.02) & (white+plate <= 1.03) & (residual < 9))
    white, plate = np.clip(white,0,1), np.clip(plate,0,1)
    alpha = np.clip(1-plate,0,1)
    core = sub._remove_tiny(np.min(patch,axis=-1) > 247, minimum=6)
    support = ndi.binary_dilation(core, iterations=14)
    alpha[(~valid)|(~support)|(alpha<.025)] = 0
    intensity = np.divide(white,alpha,out=np.zeros_like(alpha),where=alpha>0)
    out = np.zeros((*sub.CANVAS,4),np.uint8)
    out[y0:y1,x0:x1,3] = np.rint(alpha*255).astype(np.uint8)
    gray = np.rint(np.clip(intensity,0,1)*255).astype(np.uint8)
    out[y0:y1,x0:x1,:3] = gray[...,None]
    out[out[...,3]==0] = 0
    a=out[y0:y1,x0:x1,3:4].astype(float)/255
    recomposed=out[y0:y1,x0:x1,:3]*a+background*(1-a)
    return out, {"observed_plate_rgb":background.astype(int).tolist(),
                 "recomposition_mae_rgb":float(np.abs(recomposed-patch).mean()),
                 "style_alpha_model":"equivalent_white_and_black_shadow_over_observed_flat_plate"}


def m35_observed_constraint(stage_alpha, current_observed_alpha, source_rgb):
    """Keep source-visible M35 pixels only inside matched source-glyph support."""
    support=np.zeros(sub.CANVAS,np.uint8)
    transforms=[]
    for index in range(5):
        crop=Image.fromarray(stage_alpha[:320,index*256:(index+1)*256])
        resized=np.array(crop.resize((205,256),Image.Resampling.LANCZOS))
        x,y=8+index*256,12
        support[y:y+256,x:x+205]=np.maximum(support[y:y+256,x:x+205],resized)
        transforms.append({"source_box":[index*256,0,(index+1)*256,320],
                           "scale":[205/256,0.8],"target_xy":[x,y]})
    target=(np.max(np.abs(source_rgb.astype(np.int16)-237),axis=-1)<=5)
    a=(support[:270,:240]>128);b=target[:270,:240]
    iou=float(np.count_nonzero(a&b)/max(1,np.count_nonzero(a|b)))
    if iou < .87:
        raise ValueError(f"M35 source-glyph geometric correspondence failed: IoU={iou}")
    out=np.zeros(sub.CANVAS,np.uint8)
    keep=ndi.binary_dilation(support>24,iterations=2)
    out[:280]=np.where(keep[:280],current_observed_alpha[:280],0)
    # The large lower-left shoulder is not text.  The white collar is identical
    # in color to several strokes; exclude that source-observed contact region
    # rather than calling the entire connected garment a glyph.
    out[850:,900:]=current_observed_alpha[850:,900:]
    collar=[(1020,780),(1235,780),(1195,872),(1252,941),(1286,1004),
            (1340,1050),(1315,1080),(1200,1080),(1143,1000),(1088,921),(1046,872)]
    mask=Image.new('1',(1920,1080));ImageDraw.Draw(mask).polygon(collar,fill=1)
    out[np.array(mask,dtype=bool)]=0
    out[~sub._remove_tiny(out>0,minimum=40)]=0
    return out, {"same_glyph_source":"stage", "first_glyph_visible_core_iou":iou,
                 "transforms":transforms,"support_only_not_font_redrawing":True,
                 "collar_exclusion_polygon":collar,
                 "limitations":["Top glyphs are constrained by a geometrically matched original-source caption; white-on-white contacts are not independently identifiable.",
                                "Lower 晴/れ strokes intersect the identical-gray collar; the contact is excluded, not reconstructed."]}


def refine(project: Path, candidate_relative: str, output_relative: str):
    project=project.resolve()
    source=sub._safe_path(project,"source/original.mp4")
    if sub.sha256(source)!=sub.SOURCE_VIDEO_SHA256:
        raise ValueError("Wrong original video")
    manifest_path=sub._safe_path(project,candidate_relative+"/manifest.json")
    manifest=json.loads(manifest_path.read_text())
    if manifest.get('schema')!=sub.TEMPLATE_SCHEMA:
        raise ValueError("Wrong candidate schema")
    destination=sub._safe_path(project,output_relative,must_exist=False)
    if not output_relative.startswith('data/subtitle_templates') or destination.exists():
        raise ValueError("Refinement requires a new dedicated template directory")
    alpha={e['id']:np.array(Image.open(sub._safe_path(project,e['alpha_path']))) for e in manifest['templates']}
    for e in manifest['templates']:
        if sub.sha256(sub._safe_path(project,e['alpha_path']))!=e['alpha_sha256']:
            raise ValueError("Candidate alpha changed")
    temporary=Path(tempfile.mkdtemp(prefix='.subtitle-refine-',dir=destination.parent))
    limitations={
      'today':([[640,805,1185,1080]],"Middle of lower caption remains occluded/unrecovered in these observations."),
      'special':([[500,0,1120,300],[100,805,800,1080]],"Some contacts in 言 and お remain unresolved; not a complete reconstructed sentence."),
      'stage':([[850,805,1150,1080]],"Lower 晴 is not recovered from the behind-subject observations."),
      'm23':([[650,430,1160,650]],"Central に/か strokes contact the identical-gray apron; only supported portions are retained."),
      'red_a':([[480,0,1200,300],[750,805,1500,1080]],"Large source-caption portions remain behind the character; no unseen strokes generated."),
      'red_b':([[850,805,1650,1080]],"Lower caption remains partly hidden behind the character and petals."),
      'm35':([[1035,780,1340,1080]],"晴/れ contact the identical-gray collar; excluded contact is incomplete.")}
    try:
        for entry in manifest['templates']:
            identifier=entry['id'];a=alpha[identifier]
            entry['limitations']=["Straight alpha is estimated from compressed original RGB; author alpha was not recovered."]
            entry['glyph_completeness']='incomplete_observed_glyph' if identifier in limitations else 'observed_visible_glyphs'
            entry['visual_review_status']='pending_fresh_refinement_png_review'
            entry['style_components']=['glyph_fill']
            if identifier in {'m07','m16'}:
                entry['omitted_style_components']=['dark_drop_shadow']
                entry['limitations'].append("Original dark drop shadow is not in this glyph-only track; retain the original reference when adding a replacement shadow during compositing.")
            if identifier in limitations:
                boxes,note=limitations[identifier]
                entry['known_unobservable_regions']=boxes
                entry['limitations'].append(note)
            if identifier=='m08':
                frame=820
                path=sub._safe_path(project,f'frames/F{frame:06d}.png')
                rgb=np.array(Image.open(path).convert('RGB'))
                rgba,stats=styled_flat_observation(rgb)
                a=rgba[...,3]
                rgba_name=identifier+'_styled.png';Image.fromarray(rgba).save(temporary/rgba_name)
                entry.update({'frame_ranges':[[752,834]],'source_frames':[frame],
                              'source_rgb_sha256':{str(frame):hashlib.sha256(rgb.tobytes()).hexdigest()},
                              'source_png_sha256':{str(frame):sub.sha256(path)},
                              'observation_plan':[{'frame_index':frame,'chapter':'M08','group':'G11'}],
                              'minimum_observations_per_pixel':1,'source_kind':'flat_plate_styled_observation',
                              'style_components':['glyph_fill','observed_dark_shadow'],
                              'rgba_path':f'{output_relative}/{rgba_name}','rgba_sha256':sub.sha256(temporary/rgba_name),
                              'flat_plate_observation':stats})
                entry['limitations'].append("Black-shadow equivalent-alpha model; validated on the original orange plate, not a recovery of the author's shadow settings.")
            if identifier=='m33':
                entry['visibility_regions']=[{'box':[i*640,0,(i+1)*640,1080],
                                              'start_frame':start,'end_frame_exclusive':4431}
                                             for i,start in enumerate([4401,4410,4418])]
                entry['visibility_evidence_frames']=[4409,4410,4417,4418]
            if identifier in {'m16','m23'}:
                entry['mask_observed_orange_occlusion']=True
            if identifier=='m16':
                a=a.copy();labels,_=ndi.label(a>0)
                for label,region in enumerate(ndi.find_objects(labels),1):
                    if region[0].start<840:a[labels==label]=0
                entry['excluded_nontext_box_corner_above_y']=840
            if identifier=='m23':
                # A white glove touches に and a detached white ribbon lies
                # beneath the text. These are observed costume, not glyphs.
                garment_polygons=[[(730,445),(772,450),(896,476),(913,528),(882,542),(815,525),(747,500)],
                                  [(992,515),(1028,518),(1048,535),(1033,578),(998,560),(990,540)],
                                  [(1112,570),(1180,561),(1255,578),(1260,633),(1190,654),(1112,617)]]
                garment=Image.new('1',(1920,1080));draw=ImageDraw.Draw(garment)
                for polygon in garment_polygons:draw.polygon(polygon,fill=1)
                a=a.copy();a[np.array(garment,dtype=bool)]=0
                a[430:600,730:920]=0
                a[~sub._remove_tiny(a>0,minimum=200)]=0
                entry['source_contact_exclusion_polygons']=garment_polygons
                entry['conservative_unresolved_contact_box']=[730,430,920,600]
                entry['limitations'].append("Source-observed white glove/ribbon contacts are excluded rather than falsely exported as text.")
            if identifier=='m35':
                rgb=np.array(Image.open(sub._safe_path(project,'frames/F004547.png')).convert('RGB'))
                a,evidence=m35_observed_constraint(alpha['stage'],a,rgb)
                entry['source_glyph_geometry_constraint']=evidence
                entry['limitations'].extend(evidence['limitations'])
            name=identifier+'_alpha.png';Image.fromarray(a).save(temporary/name,compress_level=9)
            entry.update({'alpha_path':f'{output_relative}/{name}','alpha_sha256':sub.sha256(temporary/name),
                          'pixel_count':int(np.count_nonzero(a))})
        # M30 repeats the identical observed バイ glyphs at the same coordinates.
        # The middle portrait's white backing hides portions of the word, but
        # the same original-source word is observable in M33. Validate against
        # M30's unobstructed left pair before permitting this narrow reuse.
        m33=next(e for e in manifest['templates'] if e['id']=='m33')
        target_path=sub._safe_path(project,'frames/F004284.png')
        target=np.array(Image.open(target_path).convert('RGB'))
        target_core=np.max(np.abs(target.astype(np.int16)-237),axis=-1)<=5
        observed=alpha['m33'][420:680,:640]>128;actual=target_core[420:680,:640]
        iou=float(np.count_nonzero(observed&actual)/max(1,np.count_nonzero(observed|actual)))
        if iou<.90:raise ValueError(f'M30/M33 observed-glyph match failed: {iou}')
        m30=copy.deepcopy(m33);m30['id']='m30_observed_m33_reuse';m30['frame_ranges']=[[4280,4304]]
        m30['visibility_regions']=[{'box':[i*640,0,(i+1)*640,1080],
                                   'start_frame':start,'end_frame_exclusive':4304}
                                  for i,start in enumerate([4280,4286,4294])]
        m30['visibility_evidence_frames']=[4285,4286,4293,4294,4303,4304]
        m30['same_glyph_reuse_evidence']={'observed_source_template':'m33','target_frame':4284,
                                        'target_rgb_sha256':hashlib.sha256(target.tobytes()).hexdigest(),
                                        'visible_left_pair_iou':iou,'scale':1,'translation_xy':[0,0]}
        m30['limitations'].append('Identical original-source caption glyphs reused from M33 after a visible-pixel geometric match; this is not typography rendered from a font.')
        manifest['templates'].append(m30)
        manifest['refinement']={'recipe':RECIPE_VERSION,'script_sha256':sub.sha256(Path(__file__)),
                                'candidate_manifest_sha256':sub.sha256(manifest_path),
                                'new_source_review_required':True}
        (temporary/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        if destination.exists():raise ValueError("Output appeared during refinement; nothing overwritten")
        temporary.rename(destination)
        return manifest
    finally:
        if temporary.exists():shutil.rmtree(temporary)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--candidate',default='data/subtitle_templates_candidate')
    parser.add_argument('--output',default='data/subtitle_templates')
    args=parser.parse_args();result=refine(args.project,args.candidate,args.output)
    print(json.dumps({'templates':len(result['templates']),'output':args.output,'review':'pending'}))
