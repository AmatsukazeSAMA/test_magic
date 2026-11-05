"""One fresh coherent API redraw: retain geometry, unify unlit hair colors."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/full_character_redraw_1080p_v01'
RUN = BASE / 'drawings/ART-G12-34/v03'


def main():
    if (RUN / 'attempt.json').exists():
        raise RuntimeError('Attempt exists. Never auto retry.')
    palette = RUN / 'inputs/unlit_hair_material_palette.png'
    im = Image.new('RGB', (720, 210), 'white')
    draw = ImageDraw.Draw(im)
    for n, (name, color) in enumerate([
        ('UNLIT GRAY HAIR', '#B6B4B2'),
        ('MINT MATERIAL BAND', '#B0C8BA'),
        ('CONTOUR INK', '#171717'),
    ]):
        draw.rectangle((n * 240 + 12, 40, n * 240 + 227, 190), fill=color)
        draw.text((n * 240 + 12, 12), name, fill='black')
    im.save(palette)
    images = [
        BASE / 'drawings/ART-G12-34/v02/character_api_original.png',
        RUN / 'inputs/source_pose_guide.png',
        BASE / 'inputs/PV_face_style_no_headgear.png',
        palette,
    ]
    prompt = '''Redraw this ENTIRE current visible animation character as ONE coherent PNG with REAL TRANSPARENT background, 880x1008. This is a complete coherent cel redraw, not a local patch or compositing operation. Do not expand the framing.

REFERENCE 1 is the current geometric template. Keep its exact head angle, half-open single dark-charcoal irises and white eye glints, small closed smile, overlapping upturned hands at upper right, wrist/cuff/arm silhouettes, half-body crop, cap with exactly two black leaves, costume, healthy warm-peach skin and body position. Its NEW gray/mint lock is correctly placed beside the ear/neck, with the lower lock hidden BEHIND the white shoulder frill and crossing foreground black sleeve. KEEP that corrected spatial relationship. No long tail or lower coil drawn over the forearm, elbow or chest. The complete lower coil remains hidden, not amputated. Keep the two bead root in the same ear-side attachment, naturally partly behind the bob.
REFERENCE 2 is original PV F0944. Preserve its exact source pose/costume/half-open eye state and economical flat animation rendering; its red twin-drill identity, background and lettering are removed. The tiny red/gold chest bow region stays as in reference 1. Do not copy source red hair or its black tail inserts.
REFERENCE 3 is the FLAT PV BOB rendering method ONLY. Ignore its closed eyes and pose. Its unlit uniform-gray hair, not polished concept-art lighting, is the rendering authority for BOTH bob and corkscrew.
REFERENCE 4 is a material-color key only: one uniform ash-gray hair fill, one uniform desaturated pale-mint structural stripe fill, dark contour ink. These are flat pigment colors, not light/shadow levels.

THE SINGLE NEEDED CORRECTION IS HAIR RENDERING: remove ALL existing drill lighting so the added lock and bob look drawn in the SAME unlit flat PV style. Paint BOTH the bob and every visible gray drill surface with ONE constant gray fill. Paint the mint material ribbon with ONE constant muted mint fill. Separate turns with economical black contour lines only. Coil volume is expressed solely by silhouette, overlaps and ink, never by brightness.
NO white highlight streak, no pale reflective lines, no shiny patches, no glossy/satin sheen, no green glow, no rim light, no gradients, no airbrushed transitions, no dark volume underside panels. Do not transfer lighting from a polished identity drawing; no polished identity rendering is supplied in this request. Do not replace a shiny bright stripe with a differently colored shiny stripe. Keep the mint band's material coloring, broad connected upper turns and natural arm/frill occlusion. Do not erase all mint, erase the lock, shrink it to a tiny tip, move it onto the forearm or make it a white plastic spring.

Retain the simple small white glints INSIDE THE EYES and the two red bead colors; the no-hair-gloss instruction is about HAIR, not erasing facial expression. Keep the source black stand collar, RED bow, gold center where source-visible, long black sleeves, white cuffs/frills/apron and current skirt/ribbon contour. Restrained continuous dark hand-drawn PV outlines, untextured flat fills, no beauty rendering, no added white border. Nothing outside the current visible character: no pink/white/black opaque background, captions, props, effects, labels, palette blocks or collage.
'''
    (RUN / 'prompt.txt').write_text(prompt, encoding='utf-8')
    request = {
        'PromptFile': str(RUN / 'prompt.txt'), 'InputImages': [str(p) for p in images],
        'OutputDirectory': str(RUN), 'Size': '880x1008', 'Quality': 'high',
        'Background': 'transparent', 'OutputFileName': 'character_api_original.png',
        'Stage': 'F0944 fresh coherent whole-character high redraw, flat unlit gray/mint hair',
    }
    (RUN / 'API_PREPARED_REQUEST.json').write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding='utf-8')
    facts = {
        'id': 'ART-G12-34', 'source_frame': 944,
        'hypothesis_change': 'Omit the polished identity completely as a lighting reference; use current corrected geometry plus unlit PV bob and flat material key.',
        'scope': 'Fresh coherent whole-character API drawing, not a local masked edit.',
        'user_correction': 'Head hair has no lighting, but added drill has lighting; unify the drawing style.',
        'geometry_template_status': 'v02 rejected for lighting only; position/arm occlusion preserved for correction, not claimed adopted.',
        'actual_continuous_playback_review': False,
        'inputs': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in images],
    }
    (RUN / 'FLAT_HAIR_REDRAW_SPEC.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'request': str(RUN / 'API_PREPARED_REQUEST.json'), 'palette': str(palette), 'api_calls': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
