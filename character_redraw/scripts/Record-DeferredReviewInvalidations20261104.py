"""Commit already completed actual source/WB reviews; preserve prior decisions."""
from pathlib import Path
from datetime import datetime, timezone
import json, shutil, subprocess, sys, hashlib

root = Path(__file__).resolve().parent.parent
b = root / 'art/full_character_redraw_1080p_v01'
folder = b / 'review/ROOT_DEFERRED_REVIEW_INVALIDATIONS_20261104_v01'
folder.mkdir(exist_ok=False)
shutil.copy2(b / 'ASSET_REGISTRY.json', folder / 'ASSET_REGISTRY.before.json')
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
registry = read(b / 'ASSET_REGISTRY.json')
rows = []
reports = {
    'first': b / 'review/SOL_FIRST_G13_13_SAMEGRAY_MATERIAL_FACTOR_20261104_v01.json',
    'returns': b / 'review/SOL_SPOTCHECK_TWO_FULLBODY_CANDIDATES_UNLIT_RETURNS_20261104_v01.json',
    'loose': b / 'review/SOL_LOOSE_HAIR_THREE_USER_EXAMPLES_SOURCE_LOOKUP_20261104_v01.json'}
for ident in ['ART-G13-13','ART-G33-31','ART-G51-18','ART-G26-04','ART-G27-01','ART-G28-01','ART-G29-01','OPT-BROOCH-PORTRAIT']:
    if ident == 'ART-G13-13':
        run = b / 'drawings/ART-G13-13/v01/direct_first_api_source1211_samegray_return_material_factor_v04'
        report = reports['first']
        note = 'Root actually viewed own canonical/guide, returned full white/black: same-gray opaque return material improved and true small+C present, but actual alpha contains pink-gray exterior clouds/blocks; body/bob unrequested gradient persists. FIRST saved, repair queued; not acceptance.'
        opts = ['--curl-policy-id','hollow_two_large_one_small_20261102_v04']
    elif ident in ['ART-G33-31','ART-G51-18']:
        run = Path(registry[ident]['selected_run']); report = reports['returns']
        note = 'Fresh limited material recheck: root actually viewed own guide and full white/black. Inner/back gray returns are visibly darker than the broad front, so latest unlit same-gray rule is not met. Old candidate reviews preserved, this reopens material only; no new geometry/dynamic certification.'
        opts = ['--curl-policy-id','hollow_two_large_one_small_20261102_v04']
    else:
        run = Path(registry[ident]['selected_run']); report = reports['loose']
        note = 'Root actual own PV guide and selected full white/black showed this OLD selected art uses short-bob/drill while source is loose. Reopen under latest original loose silhouette/face/gray-clothes with gray+mint color only. User canceled white-dress trial. New loose previews and portrait redraw remain separate and not silently selected; user eye-color-only no-API rule queued after missing FIRSTs.'
        opts = ['--hairstyle-mode','loose_recolor','--hairstyle-policy-id','source_loose_recolor_only_20261104_v03']
    q = read(report)
    entries = q.get('records', q.get('entries', [q]))
    entry = next(x for x in entries if x['id'] == ident)
    raw = next((run/n for n in ['character_imggen_original.png','character_api_original.png','character_api_cel.png'] if (run/n).exists()))
    assert sha(raw) == entry['image_sha256']
    cmd = [sys.executable, '-X','utf8',str(root/'scripts/Set-GoalCharacterReview.py'),'--id',ident,'--run',str(run),'--decision','repair','--independent',str(report),'--note',note,*opts]
    result = subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',check=True)
    rows.append({'id':ident,'result':json.loads(result.stdout),'reviewed_raw_sha256':sha(raw),'independent_report':str(report),'independent_sha256':sha(report)})
(folder/'RESULTS.json').write_text(json.dumps({'recorded_utc':datetime.now(timezone.utc).isoformat(),'records':rows,'generation_calls':0,'new_art_selected':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))
