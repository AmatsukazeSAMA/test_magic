"""Upright-dance projections of the user's fixed anatomical-left drill root.

Prompt constraints only: returned art still needs actual laterality inspection.
An inverted shot needs its actual rotated projection, not these upright labels.
"""

DRILL_PROJECTIONS = {
    "front": "Bead/root/coil attach on IMAGE RIGHT below the right bob edge. IMAGE LEFT has no second bead/coil group.",
    "left_three_quarter": "Bead/root/coil remain on IMAGE RIGHT, on the near anatomical LEFT side. Do not relocate them to IMAGE LEFT.",
    "right_three_quarter": "Bead/root/coil remain on IMAGE RIGHT below that bob edge, on the FAR anatomical LEFT side. IMAGE LEFT near-ear bead/coil attachment is WRONG; keep that bob side plain. Let the right bob, neck, white shoulder and foreground arm occlude the far lock naturally.",
    "left_profile": "The anatomical LEFT side is near. The single lock attaches below the near ear/nape, usually toward IMAGE RIGHT behind a left-facing head; preserve natural bob and shoulder occlusion.",
    "right_profile": "The anatomical LEFT root is FAR, behind the opaque bob/nape and neck/shoulder. Do not hang visible beads or the coil from the near RIGHT ear. A visible trailing portion may project behind the head toward IMAGE LEFT; that does not make its root near-side.",
    "rear": "Bead/root/coil project on IMAGE LEFT of the back of the head. IMAGE RIGHT has no second bead/coil group.",
    "back_left": "In this rear three-quarter view the anatomical LEFT attachment projects on IMAGE LEFT of the back head; keep the same root through the turn and let original geometry determine occlusion.",
    "back_right": "In this rear three-quarter view the anatomical LEFT attachment projects on IMAGE LEFT of the back head; do not move it to the visible right ear. Preserve original geometry and natural occlusion.",
}
