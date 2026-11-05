"""Apply the same actual future-project consent check to the known-unsent27 payload."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
code = (root / 'scripts/Record-G33-26-ExistingConsentReadback20261102.py').read_text(encoding='utf-8')
for old, new in {
    'G33-26': 'G33-27',
    'first_api_source2412_raisedindex_lowpalm_user11_v01': 'first_api_source2416_diagonalindex_lowhand_user11_v01',
    'a9948fa789eb4af7b901783c2eb3bc2a99a2d44af9f3952c599d9b6c88a6162f': '07d8980a112cca6046ec4faebb8cc4246909bbc537b7397b4fdee527e6959d9d',
    'source2412 own eyes/neutral closed mouth': 'source2416 own open eyes and tiny dot/short mouth',
    "'size': '640x1040'": "'size': '624x1072'",
}.items():
    assert old in code, old
    code = code.replace(old, new)
exec(compile(code, str(Path(__file__).resolve()), 'exec'), globals())
