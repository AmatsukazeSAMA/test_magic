"""Annotated source reference for prop occlusion; never a deliverable matte."""
from pathlib import Path
from PIL import Image, ImageDraw
import json
import hashlib

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
source = base / 'drawings/ART-G45-01/v01/inputs/source_pose_guide.png'
out = base / 'review/diagnostics/G45-01_basket_occlusion_source_v01'
out.mkdir(parents=True, exist_ok=True)
im = Image.open(source).convert('RGB')
assert im.size == (816, 832)
# Only the original independent basket/bread visible footprint is annotated.
# The foreground hand and cuff are kept as original pixels inside their ROI.
occluder = [(311,205),(330,183),(347,217),(358,175),(380,172),(399,207),
 (406,230),(420,195),(439,190),(451,205),(454,225),(475,225),(486,249),
 (484,268),(511,263),(525,278),(526,293),(541,295),(551,309),(551,337),
 (537,374),(524,402),(494,425),(459,432),(422,421),(388,425),
 (349,411),(329,400),(314,377),(304,345),(299,310),(296,276),(301,254)]
hand = [(344,350),(356,337),(364,343),(371,354),(382,354),(390,364),
 (394,375),(408,385),(422,388),(430,397),(418,416),(407,411),(396,402),
 (388,392),(379,385),(372,387),(370,400),(359,396),(351,385),(345,375)]
mask = Image.new('L', im.size, 0)
d = ImageDraw.Draw(mask)
d.polygon(occluder, fill=255)
d.polygon(hand, fill=0)
annotated = im.copy()
annotated.paste((0, 220, 220), (0, 0), mask)
annotated.save(out / 'original_action_cyan_independent_occluder.png')
mask.save(out / 'source_occluder_annotation_only.png')
(out / 'GUIDE_PROVENANCE.json').write_text(json.dumps({
 'purpose': 'Annotated original action only: cyan means independent basket/bread and required alpha, not new character pixels.',
 'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
 'source_occluder_polygon_xy': occluder, 'source_foreground_hand_preserve_roi_xy': hand,
 'native_dimensions': list(im.size), 'not_final_artwork': True, 'not_production_prop_or_matte': True,
 'source_visible_foreground_hand_pixels_retained': True, 'art_pixels_painted': False,
 'actual_guide_review_pending': True, 'user_accepted': False
 }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(out)
