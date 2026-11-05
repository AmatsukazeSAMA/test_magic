from pathlib import Path
B=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
D=B/"review/diagnostics/SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04"
D.mkdir(parents=True,exist_ok=True)
p=B/"review/diagnostics/SOL_PY_X01_14_ROUNDED_RIBBON_SMALLER_LIGHT_CAP_20261104_v02/INDEPENDENT_AUDIT_READONLY.py"
s=p.read_text(encoding="utf-8")
for old,new in [
("py_post_pass_user_round_ribbon_smaller_light_cap_v02","py_post_pass_thin_first_round_baseline_eyes_v04"),
("SOL_PY_X01_14_ROUNDED_RIBBON_SMALLER_LIGHT_CAP_20261104_v02","SOL_PY_X01_14_THIN_FIRST_ROUND_BASELINE_20261104_v04"),
("37ef8d2d63e3380c20b16854b59eeadcd758c78d89015941494455d9da567f81","50ddaba05f5411c3958effb6c597882ab55e2639aa9f9a265df9ce2bc9f0634e"),
("139526ab4dbd67d6a8b220231794c4e8d62fc4feeec997b55c510c9fc9fbfda0","8181037962aaa0624155fc5ac1af924536be55f5b4b35311f4cf78d748de29ae"),
("fdaf20a7430d5e2255ae338c088c3becb786ac85b215185f2f2cb066c9dde7f8","ca8c7fe058a6578b3562975387651052f73c87dc086f393d56f3f2663be5d5a7"),
("Light fraction is a recomputed ROOT trial measurement, not a user-specified mandatory ratio.","Independent current native-mask AA weight measurement adapted to the approved round-cap baseline; not a fixed user area rule.")
]:s=s.replace(old,new)
(D/"INDEPENDENT_AUDIT_READONLY.py").write_text(s,encoding="utf-8")

