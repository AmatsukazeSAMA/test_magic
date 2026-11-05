from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
B = HERE.parents[3]
PROJECT = B.parents[1]

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def rec(p):
    return {'path': str(p), 'sha256': sha(p)}

def put(r, name, obj):
    p = r/name
    assert not p.exists(), p
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return rec(p)

runs = [
    HERE,
    B/'drawings/ART-G33-63/v01/prep_first_api_source2589_graybob_fullshoes_v01',
]
auth = B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'
wrapper = PROJECT/'scripts/Invoke-ReferenceImage.ps1'
defaults = PROJECT/'image_defaults.json'
prefix = read(defaults)['generation_prompt_prefix']['text']
now = datetime.now(timezone.utc).isoformat()
assert sha(auth) == 'f26198f684f4b38bb39b999f5e46811ac086f47e6ea83a93b73bf068672b6d8e'
assert read('C:/Users/11515/.agents/skills/openai-api/api/connection.json')['model'] == 'gpt-image-2.5-sunburst'

preview_template = '''#Requires -Version 7.0
$ErrorActionPreference='Stop'
$r=$PSScriptRoot
$l=Get-Content -LiteralPath (Join-Path $r 'REQUEST_LOCK.json') -Raw | ConvertFrom-Json
function Assert-Exact([string]$p,[string]$h){if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $h){throw "Payload mismatch: $p"}}
foreach($x in @($l.prepared_request,$l.draft,$l.prompt,$l.wrapper,$l.authorization,$l.JOB,$l.REGISTRATION_PLAN)){Assert-Exact $x.path $x.sha256}
foreach($x in $l.references){Assert-Exact $x.path $x.sha256}
foreach($x in $l.read_only_predecessor_sentinels){Assert-Exact $x.path $x.sha256}
$d=Get-Content -LiteralPath $l.project_defaults_path -Raw | ConvertFrom-Json
if([string]$d.generation_prompt_prefix.text -cne [string]$l.mandatory_prefix){throw 'LEFT prefix changed'}
foreach($n in @('attempt.json','result.json','character_api_original.png','EXECUTION_LOCK.json')){if(Test-Path -LiteralPath (Join-Path $r $n)){throw 'Existing execution evidence: recovery only'}}
$p=Get-Content -LiteralPath $l.prepared_request.path -Raw | ConvertFrom-Json -AsHashtable
if($p.Count -ne 8 -or $p.Size -ne '__SIZE__' -or $p.Quality -ne 'high' -or $p.Background -ne 'transparent' -or $p.InputImages.Count -ne 6){throw 'Payload arguments mismatch'}
# PREPONLY: the sole wrapper invocation includes Preview. This script has no submission branch.
$report=& $l.wrapper.path @p -Preview
if($report.submitted -ne $false -or $report.endpoint -ne $l.endpoint -or $report.model -ne $l.model -or $report.size -ne $l.size -or $report.n -ne 1 -or $report.input_count -ne 6 -or $report.mask_provided){throw 'Unexpected preview'}
$dest=Join-Path $r 'API_PREVIEW_PROOF_PREPONLY.json'
if(Test-Path -LiteralPath $dest){throw 'Preserve existing preview'}
[IO.File]::WriteAllText($dest,($report | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$report
'''

for r in runs:
    d = read(r/'DRAFT_API_REQUEST.json')
    prov = read(r/'INPUT_PROVENANCE.json')
    obs = read(r/'SOURCE_OBSERVATION_PRIVATE_PREPONLY.json')
    id = d['id']
    assert read(B/'ASSET_REGISTRY.json').get(id) is None
    assert len(d['InputImages']) == 6 and not d['dispatchable_by_artist']
    assert d['Quality'] == 'high' and d['Background'] == 'transparent' and d['n'] == 1 and d['automatic_retries'] == 0
    assert sha(d['PromptFile']) == d['prompt_sha256']
    assert Path(d['PromptFile']).read_text(encoding='utf-8').startswith(prefix+'\n\n主角换成图3的中性灰短圆润bob女孩身份')
    assert not any(r.parent.rglob('attempt.json'))
    assert not any(r.parent.rglob('character_api_original.png'))
    assert not any(r.parent.rglob('character_imggen_original.png'))
    refs = [{'path': f, 'sha256': h} for f,h in zip(d['InputImages'],d['reference_sha256'])]
    for x in refs + [prov['source_JOB'],prov['source_REGPLAN']] + prov['read_only_63_64_65_sentinels']:
        assert sha(x['path']) == x['sha256'], x['path']
    dimensions = [int(x) for x in d['Size'].split('x')]
    assert all(x % 16 == 0 for x in dimensions)
    assert dimensions[0]*dimensions[1] >= 655360
    review = put(r, 'ARTIST_REFERENCE_REVIEW.json', {
        'id': id, 'created_utc': now,
        'reviewer': 'xhigh_pending_artist actual source/reference observation only',
        'actual_viewed': refs+[prov['source_full'],prov['source_guide'],prov['first_scene_source'],prov['motion_reference']],
        'exact_reference_roles': [{'number': i+1, **x} for i,x in enumerate(prov['refs'])],
        'observations': {
            'canonical_real_pts': [d['source_frame'],d['source_pts']], 'time_base': '1/16000',
            'first_exposure_frames': d['first_case_frames'], 'first_exposure_pts': d['first_case_pts'],
            'source_action': obs['action'], 'source_eyes_mouth': obs['eyes_mouth'],
            'source_specific_difference': obs['source_difference'], 'source_visible_extent': obs['source_canvas_cutoff'],
            'root_continuity': obs['LEFT_root_and_continuity'], 'AI_phase_limit': obs['AI_hair_only_observation'],
            'identity': 'LEFT mandatory first paragraph followed immediately by explicit gray short rounded bob OC replacement. Source red/sharp long forelocks/high dual coils are not target; source still owns all own eye/mouth/body/hands/clothes/crop.',
            'geometry_material': 'Both exact correct11 whole head/coil context and gray return detail viewed. Wide gray front/inner/back-return must connect and taper to C; reasonable head/shoulder volume; tiny hair ROI cannot set intrinsic size. Opaque returns must not be deleted as air. No closed caps/disks/solid cone/giant or micro. Flat gray and muted mint only; no directional gray underside/silver/highlight/gradient.',
            'cap': 'Original current white cap and two main black leaves retained; source common small attachment remains natural, not extra long third leaf. No unmasked source identity copying.',
            'source_only_eye_method': 'Reference5 is this source only; source round-open eye aperture/gaze and closed smile govern. Single charcoal solid fill plus normal round small white point; no G02 half-lid bitmap and no black pupil plus gray ring.',
            'prior_status': 'ID absent from current central registry and has no local raw/attempt/result. Project target result/attempt/BUILTIN/release search returned no match. Original40 membership verified. No prior unknown request is retried.',
            'canvas_size_limit': 'Original JOB guide and REGPLAN unchanged; no compact crop override. Both dimensions multiples16 and area exceeds655360 as conservative skill convention. This is not proof of a Sunburst-specific minimum, no boundary probing call.',
        },
        'source_JOB_and_REGPLAN_unchanged': True,
        'predecessor_current_images_not_yet_available_no_dynamic_pass': True,
        'API_calls':0,'HTTP_calls':0,'native_calls':0,
        'dispatchable_by_artist':False,'root_only_actual_network_submission':True,
        'art_accepted':False,'dynamic_validated':False,
    })
    formal = put(r, 'API_PREPARED_REQUEST.json', {
        k:d[k] for k in ['PromptFile','InputImages','OutputDirectory','Size','Quality','Background','OutputFileName','Stage']
    })
    lock = put(r, 'REQUEST_LOCK.json', {
        'id':id,'created_utc':now,'prepared_request':formal,
        'draft':rec(r/'DRAFT_API_REQUEST.json'),'prompt':rec(d['PromptFile']),
        'prompt_sha256':d['prompt_sha256'],'references':refs,
        'wrapper':rec(wrapper),'authorization':rec(auth),
        'JOB':prov['source_JOB'],'REGISTRATION_PLAN':prov['source_REGPLAN'],
        'read_only_predecessor_sentinels':prov['read_only_63_64_65_sentinels'],
        'artist_actual_reference_review':review,
        'size':d['Size'],'quality':'high','background':'transparent',
        'model':'gpt-image-2.5-sunburst','endpoint':'https://api.openai.com/v1/images/edits',
        'n':1,'retry':0,'PREPONLY':True,'artist_may_submit':False,
        'root_must_actual_view_and_personally_send':True,
        'no_execution_lock_or_attempt_created':True,
        'mandatory_prefix':prefix,'project_defaults_path':str(defaults),
    })
    put(r, 'PARENT_PREPONLY_SCOPE.json', {
        'id':id,'recorded_utc':now,
        'parent_instruction': 'PREPONLY G12-66 and G33-63; verify actual canonical/first PTS/current status and source action; do not duplicate known candidate. Fresh private missing-first preparation only. Actual own full source and eye/mouth/hands plus all6 refs. high/transparent/n1/retry0/formal8/lock/Preview only. Explicit gray short bob identity, fixed anatomical LEFT low nape root, 63-65 turn/front-shoulder continuity pending actual preceding states. No API/imggen/network/attempt/execution/central/JOB/REG/63-65 lock changes, do not expand another item.',
        'project_user_broad_scope':rec(auth),'prepared_request':formal,'request_lock':lock,
        'generation_release_this_record':False,'network_calls_authorized_to_artist_this_turn':0,
        'not_a_root_send_release':True,
    })
    script_path = r/'Preview-PreparedOnly.ps1'
    assert not script_path.exists()
    script_path.write_text(preview_template.replace('__SIZE__',d['Size']),encoding='utf-8')
    print(json.dumps({'id':id,'formal':formal,'request_lock':lock,'draft':rec(r/'DRAFT_API_REQUEST.json'),
        'prompt':rec(d['PromptFile']),'preview_only_script':rec(script_path),'calls':0},ensure_ascii=False))
