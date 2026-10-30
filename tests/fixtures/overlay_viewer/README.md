# Offline overlay viewer — synthetic fixture only

This 8-frame, 2-S / 4-M fixture contains simple transparent bars and a flat
background. **It is not original PV footage, not extracted production art, and
not evidence for any production drawing budget.** It has two counted
drawings, one non-counted alias and one unconfirmed candidate.

Open `字幕特效与复用工作台.html` with the relative assets beside it. Regenerate:

```sh
python scripts/magic_maid_overlay_viewer.py --project tests/fixtures/overlay_viewer --verify-assets
python -m unittest discover -s tests -p 'test_magic_maid_overlay_viewer.py' -v
```

## Verification already covered by automated tests

- Frame ordering, continuous original PTS, exact end time, concatenated S-local
  frame/PTS, source-frame identity and mutually exclusive S ownership.
- Straight-alpha declaration, 8-bit RGBA PNG/canvas, content-addressed paths,
  alpha statistics, optional file SHA256, missing/unknown asset cases.
- Project-local HTML output; no traversal, remote URLs, symlinks, hard-linked
  output or overwrite of protected source/data directories. Existing root HTML
  is replaceable only with this builder’s dedicated generation marker; older
  reference/layer-viewer deliverables are rejected and preserved.
- JSON/script escaping, no network dependencies, alias and candidate counting.
- Audited D001–D003 source images are allowed only with an explicit same-frame,
  exact-PTS `source_samples` record. Reference PNGs and arbitrary nested PNGs
  remain forbidden, including inside otherwise allowed source directories.
- Work budgets, linework/color-only breakdowns, and pair totals come from manifests; candidates
  are not labelled confirmed additional drawings. Full-body-first scheduling
  is an editorial suggestion, not a quote from the reference tutorial. Confirmed
  crop-pair totals count unique reviewed pairs, not transitive alias records;
  local line variants and recolor-only work retain their separate scopes.
  Section linework/color-only IDs must partition the total work budget.
- Node syntax plus a **simulated DOM/Image contract test**: stale success/error
  callbacks, same-frame-only fallback, controls, S jumps and drawing filters.
  This simulation is **not a browser test or visual/layout acceptance**.

## Required real-browser checks (official Sites preview + CUA only)

Do these against the final production manifests before claiming UI/browser QA:

1. Check desktop and narrow mobile layouts, keyboard focus, frame slider/input,
   arrows, S/M jumps and final frame. Match displayed original/local PTS to JSON.
2. Toggle subtitle/FX independently over checker, white and dark backgrounds.
   Switch Auto / FX-above / FX-below: F0/F1 declare FX below, F2/F3/F7 above,
   F4 mixed, F5/F6 unknown. Mixed/unknown must visibly warn even under manual
   override. Subject/source placement metadata must not control two-track order.
   Switch overlay-only / split / source-only repeatedly. Verify current-frame
   PNGs, full-resolution links, alpha edges and correct canvas alignment.
3. Navigate rapidly while images load. Old images or errors must never replace
   a newer requested frame. Retry must retain frame, theme and display mode.
4. In this fixture, F0 has exact cache; F3 has only an explicit same-frame cel
   fallback; F2 has neither and must show an error, not F3. F6 has a missing
   subtitle asset with `unsupported_scene` and must not be labelled clean/empty.
5. Search/filter aliases, planned types and candidates. The S01 budget-item
   button must show only its newly assigned item. Conditional reuse remains
   unconfirmed; no candidate transform changes any image.
6. Verify production S package links, repeated clicks, opening/closing source
   file tabs and browser Back/Forward. Recheck failed loads after moving/copying
   the project folder. No external hosting or upload is part of this test.

The fixture deliberately omits most exact frame caches and S export folders so
missing-source and not-yet-generated-package states remain testable.
