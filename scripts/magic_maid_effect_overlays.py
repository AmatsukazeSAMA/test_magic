#!/usr/bin/env python3
"""Source-palette straight-alpha effects for the attachment-1 PV timeline.

Recovered from the cloud task's recorded implementation after workspace loss.
This is NOT the old frozen visible-pixel partition, and not recovered author
alpha. Native coverage and remaining edge/occlusion limits are recorded in the
separate effect overlay audit; unit tests alone do not approve artistic reuse.

API: extract_overlay(rgb uint8 HxWx3, frame_index, chapter, group) -> RGBA, dict.
The input may be readonly and is never mutated. configure_project(root) selects
a restored project. Only two declared attachment-1 source PNGs are lazily read,
for black transitions. No network, attachment-2, user computer, or source write.

Colour is solved in decoded source RGB, not a claim about the source transfer
function. Unknown underlays, higher overlays, and noise-level faint pixels are
explicit limitations. No full-source RGB fallback and no hidden character art.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

METHOD_VERSION = "observed-effect-palette-matte-v1"
DATA_DEPENDENCIES: tuple[str, ...] = (
    "cels/G26-04/source.png",  # Original F1849, clear same face layout.
    "cels/X03-03/source.png",  # Original F1927, clear same lyric cards.
)
_PROJECT = Path(__file__).resolve().parents[1] / "magic_maid_20261029"
PINK = (213, 167, 169)
WHITE = (237, 237, 237)
GHOST_INK = (238, 235, 232)
PETAL = (175, 48, 93)
ORANGE = (255, 171, 40)
RAY = (245, 138, 8)
RED = (173, 0, 3)
BLACK = (0, 0, 0)
DARK = (46, 46, 46)
STRUCTURE = np.ones((3, 3), dtype=bool)
UNDERLAYS = (PINK, WHITE, (255, 255, 255), RED, DARK, BLACK,
             (255, 219, 207), (254, 222, 214), (218, 207, 210),
             (160, 89, 90), (255, 209, 207))


def configure_project(project):
    """Idempotent root selection for main process / process-pool workers."""
    global _PROJECT
    value = Path(project).resolve()
    if value != _PROJECT:
        _PROJECT = value
        _reference.cache_clear()


@lru_cache(maxsize=2)
def _reference(relative):
    if relative not in DATA_DEPENDENCIES:
        raise ValueError("Undeclared source reference")
    path = _PROJECT / relative
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing/nonregular source reference: {relative}")
    with Image.open(path) as im:
        result = np.array(im.convert("RGB"), dtype=np.float32)
    result.flags.writeable = False
    return result


def _project(c, foreground, background):
    """Least-squares C = a F + (1-a) B in observed decoded RGB."""
    f, b = np.asarray(foreground, np.float32), np.asarray(background, np.float32)
    v = f - b
    denominator = float(np.dot(v, v))
    if denominator < 1:
        return np.zeros(c.shape[:2], np.float32), np.full(c.shape[:2], 999, np.float32)
    alpha = np.sum((c - b) * v, axis=2) / denominator
    residual = np.max(np.abs(c - (b + np.clip(alpha, 0, 1)[..., None] * v)), axis=2)
    return alpha, residual


def _near(c, colour, tolerance=7):
    return np.max(np.abs(c - np.asarray(colour, np.float32)), axis=2) <= tolerance


def _rect(shape, box):
    h, w = shape
    x0, y0, x1, y1 = box
    out = np.zeros(shape, bool)
    out[max(0, int(y0*h)):min(h, int(np.ceil(y1*h))),
        max(0, int(x0*w)):min(w, int(np.ceil(x1*w)))] = True
    return out


def _components_with_seed(mask, seed, minimum=3):
    labels, count = ndi.label(mask, STRUCTURE)
    if not count:
        return np.zeros(mask.shape, bool)
    counts = np.bincount(labels[seed & mask], minlength=count+1)
    keep = counts >= minimum
    keep[0] = False
    return keep[labels]


def _rgba_colour(colour, alpha):
    out = np.zeros((*alpha.shape, 4), np.uint8)
    out[..., 3] = np.clip(np.rint(alpha * 255), 0, 255).astype(np.uint8)
    out[..., :3][out[..., 3] > 0] = colour
    return out


def _over(bottom, top):
    """Straight-alpha over; canonical zero RGB on transparent pixels."""
    a = top[..., 3:4].astype(np.float32) / 255
    b = bottom[..., 3:4].astype(np.float32) / 255
    out_a = a + b * (1-a)
    premult = top[..., :3] * a + bottom[..., :3] * b * (1-a)
    rgb = np.divide(premult, out_a, out=np.zeros_like(premult), where=out_a > 0)
    out = np.zeros_like(top)
    out[..., :3] = np.clip(np.rint(rgb), 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(np.rint(out_a[..., 0] * 255), 0, 255).astype(np.uint8)
    out[..., :3][out[..., 3] == 0] = 0
    return out


def _flat(c, colour, allowed=None, *, backgrounds=UNDERLAYS, radius=7,
          minimum_seed=3, faint=True, residual_limit=8):
    """Flat-colour matte with locally witnessed alternative underlays.

    Only non-core edge samples run the palette fits. A zero-alpha supported
    underlay participates in model selection: otherwise a real grey garment
    can wrongly win a less accurate positive white/pink-alpha explanation.
    """
    shape = c.shape[:2]
    allowed = np.ones(shape, bool) if allowed is None else allowed
    pink_a, pink_r = _project(c, colour, PINK)
    core = _near(c, colour, 8) & allowed
    seed = core.copy()
    if faint:
        seed |= (pink_a >= .075) & (pink_a <= 1.08) & (pink_r <= residual_limit*.6) & allowed
        weak = (pink_a >= .035) & (pink_a < .075) & (pink_r <= 3) & allowed
        seed |= _components_with_seed(weak, weak, 16)
    seed = _components_with_seed(seed, seed, minimum_seed)
    if not seed.any():
        return np.zeros((*shape, 4), np.uint8), {"seed_pixels": 0, "uncertain_edge_pixels": 0}
    candidate = ndi.binary_dilation(seed, STRUCTURE, iterations=radius) & allowed
    alpha = np.zeros(shape, np.float32)
    query = candidate & ~core
    ys, xs = np.nonzero(query)
    values = c[ys, xs]
    edge_a = np.zeros(len(ys), np.float32)
    edge_e = np.full(len(ys), np.inf, np.float32)
    offsets = ((-1,0),(1,0),(0,-1),(0,1),(-3,0),(3,0),(0,-3),(0,3),
               (-radius,0),(radius,0),(0,-radius),(0,radius),
               (-radius,-radius),(-radius,radius),(radius,-radius),(radius,radius))
    neighbours = np.stack([c[np.clip(ys+dy, 0, shape[0]-1),
                              np.clip(xs+dx, 0, shape[1]-1)]
                           for dy, dx in offsets], axis=1)
    for bg in backgrounds:
        b = np.asarray(bg, np.float32)
        v = np.asarray(colour, np.float32) - b
        denominator = float(np.dot(v, v))
        if denominator < 1:
            continue
        a = np.sum((values-b)*v, axis=1) / denominator
        residual = np.max(np.abs(values-(b+np.clip(a,0,1)[:,None]*v)), axis=1)
        support = np.any(np.max(np.abs(neighbours-b), axis=2) <= 8, axis=1)
        if tuple(bg) == PINK:
            support |= (pink_r[ys,xs] < 5) & (pink_a[ys,xs] > 0)
        valid = (support & (a >= -.03) & (a <= 1.10)
                 & (residual <= residual_limit) & (residual < edge_e))
        edge_a[valid] = np.clip(a[valid], 0, 1)
        edge_e[valid] = residual[valid]
    edge_a[edge_a < .022] = 0
    alpha[ys,xs] = edge_a
    underlay_found = np.zeros(shape, bool)
    underlay_found[ys,xs] = np.isfinite(edge_e)
    alpha[core & seed] = 1
    accepted = _components_with_seed(alpha > 0, seed, minimum_seed)
    alpha[~accepted] = 0
    uncertain = candidate & ~underlay_found & ~core & ~_near(c, PINK, 8)
    return _rgba_colour(colour, alpha), {
        "seed_pixels": int(seed.sum()), "uncertain_edge_pixels": int(uncertain.sum()),
        "partial_alpha_pixels": int(((alpha > 0) & (alpha < 1)).sum()),
        "alpha_method": "least_squares_observed_palette_with_local_underlay_support",
    }


def _protect_components(core, protected, *, retain_large=None):
    labels, n = ndi.label(core, STRUCTURE)
    sizes = np.bincount(labels.ravel(), minlength=n+1)
    overlap = np.bincount(labels[protected], minlength=n+1)
    reject = (overlap > 0) & (overlap >= sizes * .55)
    if retain_large is not None:
        reject &= sizes < retain_large
    reject[0] = False
    return reject[labels]


def _outlined(c, colour, allowed=None):
    """Retain observed fill AND dark contour mixtures, not a colour-core cut.

    Strict black keying lost source-subsampled black/orange or black/red edges.
    In a 7px fill-core band, remove the observed backing by minimum feasible
    alpha, explicitly a lower-bound estimate rather than original author alpha.
    """
    shape = c.shape[:2]
    allowed = np.ones(shape, bool) if allowed is None else allowed
    core = _components_with_seed(_near(c, colour, 12) & allowed,
                                 _near(c, colour, 12) & allowed, 3)
    band = ndi.binary_dilation(core, STRUCTURE, iterations=7) & allowed
    possible = band & ~_near(c, PINK, 8) & ((c.min(axis=2) < 155) | core)
    possible = _components_with_seed(possible, core, 3)
    ys, xs = np.nonzero(possible)
    if not len(ys):
        return np.zeros((*shape,4),np.uint8), {"seed_pixels":0,"uncertain_edge_pixels":0}
    values = c[ys,xs]
    backing = np.broadcast_to(np.asarray(PINK,np.float32), values.shape).copy()
    best = np.full(len(ys), np.inf, np.float32)
    for bg in (PINK, WHITE, (255,255,255)):
        b = np.asarray(bg,np.float32)
        av = np.sum((values-b)*(-b),axis=1) / np.dot(b,b)
        error = np.max(np.abs(values-b*(1-np.clip(av,0,1)[:,None])),axis=1)
        supported = np.zeros(len(ys),bool)
        for dy,dx in ((-3,0),(3,0),(0,-3),(0,3),(-6,0),(6,0),(0,-6),(0,6)):
            sample = c[np.clip(ys+dy,0,shape[0]-1),np.clip(xs+dx,0,shape[1]-1)]
            supported |= np.max(np.abs(sample-b),axis=1) < 9
        if bg == PINK:
            supported[:] = True
        take = supported & (error+2 < best)
        backing[take], best[take] = b, error[take]
    low = (backing-values) / np.maximum(backing,1)
    high = (values-backing) / np.maximum(255-backing,1)
    alpha = np.clip(np.maximum(low,high).max(axis=1),0,1)
    alpha[core[ys,xs]] = 1
    alpha[alpha < .025] = 0
    foreground = np.divide(values-(1-alpha[:,None])*backing, alpha[:,None],
                           out=np.zeros_like(values), where=alpha[:,None]>0)
    out = np.zeros((*shape,4),np.uint8)
    out[ys,xs,:3] = np.clip(np.rint(foreground),0,255).astype(np.uint8)
    out[ys,xs,3] = np.rint(alpha*255).astype(np.uint8)
    out[core,:3] = colour
    out[...,:3][out[...,3] == 0] = 0
    return out, {
        "seed_pixels": int(core.sum()),
        "partial_alpha_pixels": int(((out[...,3]>0)&(out[...,3]<255)).sum()),
        "uncertain_edge_pixels": int((band & ~possible & ~_near(c,PINK,8)).sum()),
        "alpha_method": "minimum_feasible_alpha_with_observed_pink_or_nearby_white_backing",
        "contour_colour": "observed_source_black/brown_mix_unmixed_from_backing; not colour-core-only",
    }


def _loop_iou(a, b):
    """IoU for local binary masks with full-frame slice coordinates."""
    sa, ma = a[0], a[1]
    sb, mb = b[0], b[1]
    y0, y1 = max(sa[0].start,sb[0].start), min(sa[0].stop,sb[0].stop)
    x0, x1 = max(sa[1].start,sb[1].start), min(sa[1].stop,sb[1].stop)
    if y1 <= y0 or x1 <= x0:
        return 0.
    aa = ma[y0-sa[0].start:y1-sa[0].start,x0-sa[1].start:x1-sa[1].start]
    bb = mb[y0-sb[0].start:y1-sb[0].start,x0-sb[1].start:x1-sb[1].start]
    intersection = int((aa & bb).sum())
    return intersection / (int(ma.sum()) + int(mb.sum()) - intersection)


def _ghost_composite(stroke, frame_index, observed_rgb=None):
    """Observed loop topology + pink backing, including small hollow eyes.

    Bounded recovery corrections:
      * Save real RAW closed holes before 4px gap-closing; closing alone erased
        the narrow F476 eye. A sealed near-duplicate cannot replace a raw loop.
      * Place backing under the inner half of ink, not ``backing[support]=0``.
        Nesting erodes each contour toward its centre, preserving eye voids.
      * Body and ink share one object opacity. Compositing two partial-opacity
        layers would double the fade and leave dark seams on a new background.

    This infers only a visible effect's bounded shape/alpha, never hidden art.
    """
    shape = stroke.shape[:2]
    support = stroke[...,3] >= 25
    sealed = ndi.binary_closing(np.pad(support,6), STRUCTURE, iterations=4)[6:-6,6:-6]
    loops = []
    raw_count = 0
    for mask, raw in ((support, True), (sealed, False)):
        labels, _ = ndi.label(mask, STRUCTURE)
        for lab, sl in enumerate(ndi.find_objects(labels), 1):
            if sl is None:
                continue
            component = labels[sl] == lab
            if int(component.sum()) < 8:
                continue
            enclosed = ndi.binary_fill_holes(component)
            interior_area = int((enclosed & ~component).sum())
            # A pinhole inside a thick garment-rim fragment is not a ghost
            # loop. Preserve genuinely hollow small eyes, not ink-dominated
            # accidental codec/white-rim components.
            if interior_area < 8 or interior_area < int(enclosed.sum())*.16:
                continue
            values = stroke[...,3][sl][component]
            values = values[values > 0]
            if not len(values):
                continue
            opacity = float(np.quantile(values,.9)) / 255
            distance = ndi.distance_transform_edt(component)
            half_width = int(np.clip(np.rint(np.quantile(distance[component], .7)),1,4))
            item = (sl, enclosed, opacity, half_width, raw)
            if any(_loop_iou(item, known) >= .85 for known in loops):
                continue
            loops.append(item)
            raw_count += int(raw)
    minimum_outer_area = shape[0]*shape[1]*(.003 if frame_index < 504 else .02)
    outer_support = np.zeros(shape,bool)
    for sl,enclosed,opacity,width,raw in loops:
        if int(enclosed.sum()) >= minimum_outer_area:
            outer_support[sl] |= enclosed
    depth = np.zeros(shape,np.uint16)
    opacity_field = np.zeros(shape,np.float32)
    for sl,enclosed,opacity,width,raw in loops:
        if not np.any(enclosed & outer_support[sl]):
            continue
        # Erode EACH polygon before even/odd nesting. Eroding the final parity
        # mask would enlarge eye holes and again remove backing under ink.
        middle = ndi.binary_erosion(np.pad(enclosed,width+1), STRUCTURE,
                                    iterations=width)[width+1:-width-1,width+1:-width-1]
        depth[sl] += middle
        opacity_field[sl] = np.maximum(opacity_field[sl], np.where(middle,opacity,0))
    backing_alpha = np.where((depth % 2) == 1, opacity_field, 0)
    # Remove open garment crumbs, retaining observed loops, their enclosing
    # outer contour, and genuinely canvas-cropped contours.
    centres = [(sl[0].start+(sl[0].stop-sl[0].start)/2,
                sl[1].start+(sl[1].stop-sl[1].start)/2) for sl,*_ in loops]
    labels, _ = ndi.label(sealed, STRUCTURE)
    retained = np.zeros(shape,bool)
    canvas_clipped_components = []
    for lab, sl in enumerate(ndi.find_objects(labels),1):
        if sl is None:
            continue
        y0,y1,x0,x1 = sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
        cropped = y0 <= 1 or x0 <= 1 or y1 >= shape[0]-1 or x1 >= shape[1]-1
        encloses = any(y0 <= cy < y1 and x0 <= cx < x1 for cy,cx in centres)
        if cropped or encloses:
            retained[sl] |= labels[sl] == lab
        if cropped:
            canvas_clipped_components.append((lab,sl))
    # Raw tiny holes might disappear from `sealed`; retain their observed ink.
    for sl,enclosed,opacity,width,raw in loops:
        retained[sl] |= enclosed & support[sl]
    retained = ndi.binary_dilation(retained,STRUCTURE,iterations=4)
    out = stroke.copy()
    out[~retained] = 0
    source_fill = np.zeros(shape,bool)
    source_eye = np.zeros(shape,bool)
    modeled_edge = np.zeros(shape,bool)
    if observed_rgb is not None:
        # In F476 the source pink face is itself a closed 41,782-pixel island,
        # even though protecting the plate opened the KEYED white contour.
        # Use that witnessed island rather than inventing a geometric arc.
        pink = _near(observed_rgb,PINK,10)
        pink_labels,pink_n = ndi.label(pink,STRUCTURE)
        pink_sizes = np.bincount(pink_labels.ravel(),minlength=pink_n+1)
        pink_boxes = ndi.find_objects(pink_labels)
        selected = {}
        for sl in ndi.find_objects(labels):
            if sl is None:
                continue
            y0,y1,x0,x1 = sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
            if (y1-y0)*(x1-x0) < minimum_outer_area:
                continue
            candidates = []
            for number,ps in enumerate(pink_boxes,1):
                if ps is None or pink_sizes[number]<minimum_outer_area*.20:
                    continue
                py0,py1,px0,px1=ps[0].start,ps[0].stop,ps[1].start,ps[1].stop
                if py0==0 or px0==0 or py1==shape[0] or px1==shape[1]:
                    continue  # The actual background plane is not a ghost.
                if y0-4<=py0 and py1<=y1+4 and x0-4<=px0 and px1<=x1+4:
                    candidates.append(number)
            if candidates:
                number=max(candidates,key=lambda z:pink_sizes[z])
                observed=stroke[...,3][sl]
                observed=observed[observed>0]
                if len(observed):
                    selected[number]=max(selected.get(number,0),float(np.quantile(observed,.9))/255)
        for number,opacity in selected.items():
            region=pink_labels==number
            source_fill |= region
            expanded=ndi.binary_dilation(region,STRUCTURE,iterations=2) & ((stroke[...,3]>0)|region)
            modeled_edge |= expanded & ~region
            backing_alpha[expanded]=np.maximum(backing_alpha[expanded],opacity)
            # Smaller enclosed source-pink islands are eye/mouth voids, not a
            # second solid pink face. This preserves F476's observed 97px eye.
            holes=ndi.binary_fill_holes(region) & ~region
            ids=np.unique(pink_labels[holes & pink])
            for eye_id in ids:
                if eye_id and eye_id not in selected and pink_sizes[eye_id]>=8:
                    source_eye |= pink_labels==eye_id
        backing_alpha[source_eye]=0
    inside = backing_alpha > 0
    ink_alpha = out[...,3].astype(np.float32)/255
    total_alpha = np.maximum(backing_alpha, ink_alpha)
    ink_weight = np.divide(ink_alpha,total_alpha,out=np.zeros(shape,np.float32),where=total_alpha>0)
    mixed = (np.asarray(PINK,np.float32)*(1-ink_weight[...,None])
             + np.asarray(GHOST_INK,np.float32)*ink_weight[...,None])
    out[inside,:3] = np.clip(np.rint(mixed[inside]),0,255).astype(np.uint8)
    out[inside,3] = np.rint(total_alpha[inside]*255).astype(np.uint8)
    out[...,:3][out[...,3] == 0] = 0
    clipped_review = []
    for lab,sl in canvas_clipped_components:
        visible = (out[...,3][sl]>0) & (labels[sl]==lab)
        if visible.any():
            body_pixels = int(inside[sl].sum())
            clipped_review.append({
                "bounds_xyxy": [sl[1].start,sl[0].start,sl[1].stop,sl[0].stop],
                "retained_stroke_pixels": int(visible.sum()),
                "pink_body_pixels_in_bounds": body_pixels,
                "status": "no_supported_pink_body" if not body_pixels else "canvas_clipped_body_requires_review",
            })
    return out, {
        "closed_observed_loops": len(loops), "raw_observed_loops_preserved": raw_count,
        "pink_ghost_fill_pixels": int(inside.sum()),
        "source_supported_pink_body_pixels": int(source_fill.sum()),
        "protected_source_pink_eye_pixels": int(source_eye.sum()),
        "modeled_under_stroke_extension_pixels": int(modeled_edge.sum()),
        "fill_method": "raw_small_holes_and_observed_pink_islands; bounded_inner_ink_extension; single_object_opacity",
        "ghost_topology_method": "observed_islands_and_raw_loops_v2",
        "modeled_body_pixels_outside_observed_pink_islands": int((inside & ~source_fill).sum()),
        "canvas_clipped_contours": clipped_review,
        "partial_flags": ["canvas_clipped_body_not_completed"] if clipped_review else [],
    }


def _ghosts(c, frame_index):
    bright = _near(c,GHOST_INK,14) & (c[...,1]>220) & (c[...,2]>215)
    broad_white = (c.min(axis=2)>224) & (c.max(axis=2)<250) & ((c.max(axis=2)-c.min(axis=2))<15)
    thick = ndi.distance_transform_edt(broad_white)>8
    protected = ndi.binary_dilation(thick,STRUCTURE,iterations=8)
    text_near = ndi.binary_dilation(_near(c,(255,255,255),4),STRUCTURE,iterations=3)
    allowed = ~protected & ~text_near
    provisional = ndi.binary_closing(np.pad(bright & allowed,3),STRUCTURE,iterations=2)[3:-3,3:-3]
    labels, n = ndi.label(provisional,STRUCTURE)
    pink_near = ndi.maximum_filter(_near(c,PINK,7),size=13)
    sizes = np.bincount(labels.ravel(),minlength=n+1)
    pink_counts = np.bincount(labels[pink_near],minlength=n+1)
    keep = (sizes>=30) & (pink_counts>=sizes*.40)
    keep[0] = False
    allowed &= ndi.binary_dilation(keep[labels],STRUCTURE,iterations=6)
    stroke, info = _flat(c,GHOST_INK,allowed,
                         backgrounds=(PINK,RED,(218,207,210),DARK,BLACK),
                         radius=6,residual_limit=12)
    out, geometry = _ghost_composite(stroke,frame_index,c)
    info.update(geometry)
    info["garment_white_protected_pixels"] = int(protected.sum())
    return out, info


def _petals(c):
    rgba, info = _flat(c,PETAL,backgrounds=UNDERLAYS,radius=24,residual_limit=10)
    alpha = rgba[...,3].astype(np.float32)/255
    visible = alpha>.02
    closed = ndi.binary_closing(np.pad(visible,5),STRUCTURE,iterations=3)[5:-5,5:-5]
    target = (closed | ndi.binary_fill_holes(visible)) & ~visible
    target &= ndi.distance_transform_edt(~visible) <= 5
    if target.any():
        known = (~target).astype(np.float32)
        smooth = ndi.gaussian_filter(alpha*known,2)/np.maximum(ndi.gaussian_filter(known,2),.001)
        alpha[target] = smooth[target]
        rgba = _rgba_colour(PETAL,alpha)
    info["locally_interpolated_alpha_pixels"] = int(target.sum())
    info["interpolation_limit"] = "only <=5px surrounded alpha cracks; no hidden underlay RGB reconstructed"
    return rgba, info


def _temporal_dark(c, relative, foreground, *, reveal=False):
    background = _reference(relative)
    shape = c.shape[:2]
    if background.shape != c.shape:
        return np.zeros((*shape,4),np.uint8), {
            "status":"unsupported_non_native_reference_shape", "reference":relative}
    f = np.asarray(foreground,np.float32)
    v = f-background
    den = np.sum(v*v,axis=2)
    alpha = np.divide(np.sum((c-background)*v,axis=2),den,
                      out=np.zeros(shape,np.float32),where=den>100)
    residual = np.max(np.abs(c-(background+np.clip(alpha,0,1)[...,None]*v)),axis=2)
    supported = (den>100) & (alpha>.025) & (alpha<1.1) & (residual<=12)
    alpha = np.where(supported,np.clip(alpha,0,1),0)
    if reveal:
        ambiguous = (den<=100) & (c.max(axis=2)<20)
        local = ndi.minimum_filter(alpha,size=3)>.9
        continuous = ndi.maximum_filter(local,size=13) & ambiguous
        alpha[continuous] = 1
        edge = np.zeros(shape,bool)
        edge[0] = edge[-1] = True
        edge[:,0] = edge[:,-1] = True
        connected = ndi.binary_propagation(edge & (alpha>.02),STRUCTURE,mask=alpha>.02)
        alpha[~connected] = 0
    else:
        enclosed = ndi.binary_fill_holes(alpha>.85)
        continuous = enclosed & _near(c,foreground,8) & (den<=100)
        alpha[continuous] = 1
        alpha[(np.max(abs(c-background),axis=2)<15) & ~continuous] = 0
    return _rgba_colour(foreground,alpha), {
        "reference":relative,
        "reference_kind":"observed_attachment1_frame; not painted clean plate",
        "alpha_method":"temporal_same_layout_palette_projection",
        "unsupported_difference_pixels":int(((residual>12)&(np.max(abs(c-background),axis=2)>15)).sum()),
        "local_constant_black_continuation_pixels":int(continuous.sum()),
        "partial_alpha_pixels":int(((alpha>0)&(alpha<1)).sum()),
    }


def extract_overlay(rgb: np.ndarray, frame_index: int, chapter: str, group: str):
    """Return native-size straight RGBA and JSON-native bounded metadata."""
    if not isinstance(rgb,np.ndarray) or rgb.dtype!=np.uint8 or rgb.ndim!=3 or rgb.shape[2]!=3:
        raise ValueError("expected H×W×3 uint8 RGB")
    if not isinstance(frame_index,int) or isinstance(frame_index,bool) or not 0<=frame_index<4763:
        raise ValueError("frame_index must be an integer in the original interval [0,4763)")
    if not isinstance(chapter,str) or not isinstance(group,str):
        raise ValueError("chapter and group must be strings")
    shape = rgb.shape[:2]
    out = np.zeros((*shape,4),np.uint8)
    categories: list[dict[str, Any]] = []
    limitations = ["Estimated matte in decoded RGB, not recovered author alpha.",
                   "Pixels hidden by higher overlays and colour-indistinguishable contacts are not reconstructed.",
                   "Very faint values at compression-noise level remain unobservable."]
    unsupported = []
    subtitle_relation = "mixed_or_uncertain"
    if (422<=frame_index<679 or 790<=frame_index<847 or 2221<=frame_index<2278
            or 1944<=frame_index<1976):
        subtitle_relation = "below_subtitles"
    if (3361<=frame_index<3373 or 1908<=frame_index<1924
            or 2139<=frame_index<2153):
        subtitle_relation = "above_subtitles"
    if chapter not in {f"M{i:02}" for i in range(37)}:
        return out, {"status":"unsupported_scene", "method":METHOD_VERSION,
                     "categories":[], "limitations":limitations+["Unknown chapter."],
                     "frame_index":frame_index, "chapter":chapter, "group":group,
                     "subtitle_relation":"mixed_or_uncertain"}
    c = rgb.astype(np.float32)

    def add(name, result):
        nonlocal out
        layer, info = result
        out = _over(out,layer)
        alpha = layer[...,3]
        categories.append({**info, "name":name,
                           "visible_pixels":int((alpha>0).sum()),
                           "partial_alpha_pixels":int(((alpha>0)&(alpha<255)).sum())})

    if 422<=frame_index<679:
        add("white_ghost_strokes_and_observed_closed_fills",_ghosts(c,frame_index))
        unsupported.append("Ghost contours touching clothes/plate or 255-white lyrics may be incomplete; open/canvas-cropped bodies are not invented.")
    if 790<=frame_index<847:
        key1, key2 = int(_near(c,ORANGE,8).sum()), int(_near(c,(255,158,22),8).sum())
        colour = ORANGE if key1>=key2 else (255,158,22)
        allowed = np.ones(shape,bool)
        if frame_index>=834:
            protected = _protect_components(_near(c,colour,8),
                _rect(shape,(.38,.30,.66,.80)),retain_large=shape[0]*shape[1]*.008)
            allowed &= ~ndi.binary_dilation(protected,iterations=3)
            unsupported.append("Compact costume gold is protected; matching-colour wipe/costume contacts remain ambiguous.")
        add("orange_splash_and_reveal",_flat(c,colour,allowed))
    if 2221<=frame_index<2278:
        core = _near(c,RAY,10)
        yy,xx = np.ogrid[:shape[0],:shape[1]]
        cameo = ((xx/shape[1]-.5104)/.075)**2 + ((yy/shape[0]-.441)/.17)**2 <= 1
        labels,n = ndi.label(core,STRUCTURE)
        total = np.bincount(labels.ravel(),minlength=n+1)
        inner = np.bincount(labels[cameo],minlength=n+1)
        reject = (total==inner) & (inner>0)
        reject[0] = False
        allowed = ~ndi.binary_dilation(reject[labels],iterations=3)
        add("orange_radial_wipe",_flat(c,RAY,allowed))
        unsupported.append("Cameo gold components are excluded until connected to ray colour; the touching gold/ray boundary is ambiguous.")
    if 2139<=frame_index<2153:
        # Actual M16 tail: two horizontal orange shutters (F2139–2143),
        # then observed full orange (F2144–2152), cut to brooch at F2153.
        # A border-connected colour field avoids recruiting an isolated gold
        # prop. Only witnessed source pixels and their local AA skirt are used.
        core = _near(c,RAY,10)
        boundary = np.zeros(shape,bool)
        boundary[0] = boundary[-1] = True
        boundary[:,0] = boundary[:,-1] = True
        field = ndi.binary_propagation(core & boundary,STRUCTURE,mask=core)
        allowed = ndi.binary_dilation(field,STRUCTURE,iterations=6)
        layer,info = _flat(c,RAY,allowed)
        info.update({"observed_phase_frames":[2139,2153],
                     "phase_end_exclusive":True,
                     "support_method":"observed_canvas_border_connected_orange_field_and_local_antialias"})
        add("orange_horizontal_shutter",(layer,info))
    if 3288<=frame_index<3373:
        protected = _protect_components(_near(c,ORANGE,9),
            _rect(shape,(.42,.22,.60,.56)),retain_large=shape[0]*shape[1]*.015)
        add("outlined_orange_stars",_outlined(c,ORANGE,~ndi.binary_dilation(protected,iterations=5)))
        unsupported.append("Bread shares star colours: protected small basket-region components may include an overlapping sparkle; the giant star is retained.")
    if 1944<=frame_index<1976:
        allowed = np.ones(shape,bool)
        if 1951<=frame_index<1961:
            # Native F1951–1960: the word is left of canvas centre, not at x=.5.
            # Observed glyph support is x860:918,y385:691; retain a small AA
            # margin without masking the detached ring fragments around it.
            allowed &= ~_rect(shape,(852/1920,378/1080,926/1920,699/1080))
        add("white_ring_and_dispersing_strokes",_flat(c,WHITE,allowed,backgrounds=(PINK,),radius=5))
        unsupported.append("Central lyric region excluded during ring-to-text phase; touching effect pixels are not inferred.")
    if 3945<=frame_index<4763:
        add("magenta_petals",_petals(c))
        unsupported.append("Petal edges over textured/unknown underlays require a local palette fit; <=5px surrounded alpha cracks are explicitly interpolated.")
    if 4304<=frame_index<4337:
        add("outlined_red_heart",_outlined(c,RED,_rect(shape,(.43,.32,.57,.64))))
    if frame_index==1821:
        if np.all(c.max(axis=2)<12):
            add("black_reveal",(_rgba_colour(BLACK,np.ones(shape,np.float32)),
                                {"alpha_method":"observed_uniform_full_black_transition"}))
        else:
            unsupported.append("Expected full-black source transition not observed; no matte invented.")
    elif 1822<=frame_index<1828:
        add("black_reveal",_temporal_dark(c,"cels/G26-04/source.png",BLACK,reveal=True))
        unsupported.append("Black-on-black ink and later caption-card footprint are ambiguous in temporal reveal; no character is reconstructed.")
    if 1908<=frame_index<1924:
        add("black_dripping_transition",_temporal_dark(c,"cels/X03-03/source.png",DARK))
        unsupported.append("Drips use observed F1927 clear cards; fully enclosed constant-dark holes are explicit effect-field inference, not original alpha.")
    nonzero = int((out[...,3]>0).sum())
    status = "partial_supported_effects" if categories else "no_routed_effect_family"
    if unsupported and not categories:
        status = "unsupported_visible_effect"
    if categories and not nonzero:
        status = "no_supported_pixels_in_effect_phase"
    return out, {"status":status, "method":METHOD_VERSION,
                 "frame_index":frame_index, "chapter":chapter, "group":group,
                 "categories":categories, "visible_pixels":nonzero,
                 "subtitle_relation":subtitle_relation,
                 "limitations":limitations+unsupported,
                 "clean_alpha_claim":False, "full_source_fallback":False,
                 "hidden_pixels_reconstructed":False,
                 "colour_space":"decoded_source_RGB; straight_alpha"}
