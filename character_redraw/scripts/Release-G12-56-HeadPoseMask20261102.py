"""Release the actually viewed head-pose mask under the existing project consent."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
template = (root / 'scripts/Release-G12-55-UpwardMask20261102.py').read_text(encoding='utf-8')
changes = {
    'F1058 curl repair': 'F1066 head-pose and aperture repair',
    'drawings/ART-G12-55/v01/mask_prep_user55_upturn_open_gray_v04': 'drawings/ART-G12-56/v01/mask_prep_source1066_headpose_aperture_v03',
    '7d089db64d6afcd038c29ce19560f87702cc8ab70b79c907a399ea1b76d87640': '0db21ab832cc772df6d4b63eacbe76893f7aab7ceacdf445d7ff633cb6db3bbd',
    'F1058 user-rejected solid curl masked repair, begin current-frame upswing; mandatory whole imggen pending': 'F1066 masked head-to-body posture and source aperture repair; preserve lowLEFT upturn, collar and both hands; mandatory whole imggen pending',
    'viewed = [run / f"readonly_QA/{n}.png" for n in [\n    "MASK_OVERLAY_FULL_white", "MASK_OVERLAY_ROOT_AIR_2x_white", "MASK_OVERLAY_ROOT_AIR_2x_black"]]': 'viewed = [run / f"qa_readonly/{n}.png" for n in [\n    "MASK_OVERLAY_FULL_white_v02_READONLY", "MASK_OVERLAY_LOCAL_CONNECTION_HANDS_2x_white_v02_READONLY", "MASK_OVERLAY_LOCAL_CONNECTION_HANDS_2x_black_v02_READONLY"]]',
    'one high transparent official API masked curl repair': 'one high transparent official API masked head-pose and eye-aperture repair',
    'Mask exposes the visible closed solid coil plus original-alpha-zero air upward on image-right. Correct low LEFT root/red beads, bob, face, two cap leaves, collar, hands and shoulder/frill stay protected. Air corridor is optional motion space, not a required silhouette or permission to shrink intrinsic hair volume.': 'Mask exposes the complete wrong-tilted head, cap, upper skin neck, lowLEFT beads and visible upturned curl plus air to rebuild original1066 head pose and its own eye aperture. Fixed collar, both hands, arms, shoulder frills, chest bow and body remain protected. Updated local white/black overlays were actually viewed after collar-edge tightening. Preserve the successful lowLEFT/upturned gray return design while reconnecting it to the more upright current head; no body rotation, air filling or intrinsic curl shrink.',
    'Input and mask preserved at 1103x1426; output 1104x1424 high near same aspect, no input art resize or patching.': 'Input and mask preserved at 1135x1386; output 1136x1392 high near same aspect, no input art resize or patching.',
    '1104x1424': '1136x1392',
    "operation_kind='local_curl_mask_repair'": "operation_kind='local_headpose_aperture_mask_repair'",
}
for old, new in changes.items():
    if old not in template:
        raise SystemExit('Template changed; inspect before release: ' + old[:100])
    template = template.replace(old, new)
if 'F1058' in template or 'ART-G12-55' in template or '1104x1424' in template:
    raise SystemExit('Old drawing-specific release data remained.')
exec(compile(template, str(Path(__file__).resolve()), 'exec'), globals())
