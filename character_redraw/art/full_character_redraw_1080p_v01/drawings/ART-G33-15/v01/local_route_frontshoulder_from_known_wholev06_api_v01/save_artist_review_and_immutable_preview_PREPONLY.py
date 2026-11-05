from pathlib import Path
from PIL import Image
import json,hashlib,datetime

P=Path(__file__).resolve().parent
PROJECT=P.parents[5];B=P.parents[3];OLD=P.parent/'whole_imggen_source2365_frontshoulder_headcrop_puregray_v06'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
 p=Path(p);return dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
provenance=load(P/'INPUT_PROVENANCE_INITIAL_PREPONLY.json');refs=provenance['reference_inputs']
maskprov=load(P/'MASK_PROVENANCE_PREPONLY_v02.json');formal=load(P/'API_PREPARED_REQUEST.json')
prefix=load(PROJECT/'image_defaults.json')['generation_prompt_prefix']['text']
prompt=(P/'prompt_api.txt').read_text(encoding='utf-8')
assert prompt.startswith(prefix)
sol=B/'review/sol_xhigh_round174.json'
solrecord=rec(sol) if sol.exists() else dict(path=str(sol),exists=False,not_inherited=True,status='awaiting_fresh174_and_ROOT_release; add any newly demonstrated non-route P1 before generation')
# Listed files were actually shown in this agent turn; this does not copy a
# previous reviewer's claims, nor claim any unseen future intermediate.
viewed=[OLD/'qa_white.png',OLD/'qa_black.png',Path(refs[0]['path']),Path(refs[1]['path']),Path(refs[2]['path']),Path(load(B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json')['reference_image']),Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029/cels/G33-15/source.png'),P/'PREP_PRIOR_CANDIDATE_c03c252b_NAPE_ROUTE_COORDINATE_GRID_5x.png',P/'PREP_PRIOR_CANDIDATE_c03c252b_NAPE_OLD_ROUTE_FRONTSPACE_black_5x.png']
viewed += [Path(q['path']) for q in maskprov['qa']]
dump(P/'ACTUAL_VIEWED_INPUTS_AND_MASK_QA_PREPONLY.json',dict(id='ART-G33-15',reviewer='xhigh_pending_artist actual image inspection',actual_view_method='view_image tool in this turn, original+known current full white/black, exact3 refs, coordinate QA, final v02 mask fullWB/route5x/alpha5x/protection QA',actual_files=[rec(p) for p in viewed],prompt_actual_readback=rec(P/'prompt_api.txt'),prepared_before_future_return=True,source_raw_sha256=refs[0]['sha256'],future_API_return_actual_viewed=False,future_whole_return_actual_viewed=False,technical_preview_not_art_acceptance=True))
review=dict(id='ART-G33-15',reviewer='artist actual preparation, not ROOT or Sol',current_target=rec(refs[0]['path']),source_frame=2365,source_pts=1262592,first_exposure=[889,891],source_observation='Rear3quarter body with head turned toward image-right, only face-edge/no readable iris/mouth; original cap and two main black leaves; black highcollar/puff sleeves, distinct bent back-waist arms/cuffs, white frills/X/bow+tails, right-swing black skirt, unequal legs and two complete shoes. No source body/face change permitted.',current_observation='Known v06 retains source body/cap/costume/legs/shoes and graybob identity. Current visible rear near-nape pair of beads connects diagonal gray/mint turns across back-white-frill and blackpuff, still not shoulder-FRONT. User explicitly calls this reversed; current root route is invalid, not a correct anchor.',changed_hypothesis='Replace whole-generation competition with exact-input editing capacity: open old wrong bead/root+diagonalcoil and necessary underlying restoration, separately permit anterior screen-right neck/shoulder/chest outer-edge exposure. Exclude old14/back-curl/gloss/otherbody references. Mask success/route geometry remains untested.',mask_observation='Final v02 white/black full overlays and 5x route/alpha/protected QA actually viewed. Pink old-route region includes both old beads, all visible diagonalcoil and C, plus narrow restoration margin; cyan window includes current air beyond source shoulder-front edge and <=12px black outercontour overlap. Main bob/cap/face and unneeded whitefrill/body remain protected; all y>=580 protected. Explicit face/chin polygon corrects v01 technical assertion, previous files retained.',protected_observed=['face/chin contour','cap and main two black leaves','nonnecessary graybob','white frill outside required old-curl restoration footprint','blackpuff interior except old-C restoration or extreme natural front overlap','white X cross','all waistback hands/cuffs','waistbow/tails','skirt/legs/complete two shoes'],known_risks=['Mask region alone does not establish 3D front routing; require future fullWB and same source actual inspection.','New visible coil must remain substantial and broadgray, without filling entire edit capacity, enlarging shoulder or attaching another near-side root.','Cleanup requires reconstructing surfaces actually hidden by the rejected rear coil; do not treat all old gray as new air.','Output960x1648 differs slightly from957x1644 target; input mask remains exact target size, overall fit only, no partwise transformation.','Latest fresh174 not assumed read or passed; root must check added P1 before release if report not yet available.'],fresh174_status=solrecord,user_rejection_readback=rec(P/'USER_EXPLICIT_V06_REVERSED_ROUTE_READBACK_PREPONLY.json'),mandatory_whole_after_local=True,whole_future_dispatchable=False,PREPONLY=True,root_release_received=False,API_calls=0,native_calls=0,HTTP_calls=0,artistic_pass=False,user_accepted=False,dynamic_tested=False)
dump(P/'ARTIST_SOURCE_ROUTE_MASK_REVIEW_PREPONLY.json',review)
config=Path('C:/Users/11515/.agents/skills/openai-api/api/connection.json')
assert load(config)['model']=='gpt-image-2.5-sunburst'
lock=dict(id='ART-G33-15',formal=rec(P/'API_PREPARED_REQUEST.json'),request=rec(P/'request_api_PREPONLY.json'),prompt=rec(P/'prompt_api.txt'),mask=rec(formal['MaskFile']),mask_provenance=rec(P/'MASK_PROVENANCE_PREPONLY_v02.json'),refs=[rec(r['path']) for r in refs],provenance=rec(P/'INPUT_PROVENANCE_INITIAL_PREPONLY.json'),artist_review=rec(P/'ARTIST_SOURCE_ROUTE_MASK_REVIEW_PREPONLY.json'),actual_view_list=rec(P/'ACTUAL_VIEWED_INPUTS_AND_MASK_QA_PREPONLY.json'),history=rec(P/'KNOWN_RETURN_AND_HISTORY_BOUNDARY_PREPONLY.json'),user_rejection=rec(P/'USER_EXPLICIT_V06_REVERSED_ROUTE_READBACK_PREPONLY.json'),scope=rec(P/'PROJECT_SCOPE_REFERENCE_RELEASE_PREPONLY.json'),auth=rec(B/'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json'),front_policy=rec(B/'USER_FRONT_SHOULDER_CURL_G33_15_G12_20_20261102_v01.json'),provider=rec(PROJECT/'scripts/Invoke-ReferenceImage.ps1'),provider_configuration=rec(config),local_status=rec(P/'LOCAL_REPAIR_STATUS.json'),future_whole=rec(P/'future_mandatory_whole_PREPONLY/request_imggen_DRAFT.json'),prefix_text=prefix,prefix_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),PREPONLY=True,root_release_received=False,api_calls_authorized_this_prep=0,API_calls=0,native_calls=0,HTTP_calls=0,automatic_retries=0)
if sol.exists():lock['fresh174']=rec(sol)
lockpath=P/'REQUEST_LOCK_PREPONLY.json';assert not lockpath.exists();dump(lockpath,lock)
expected=sha(lockpath)
ps='''#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$lockPath=Join-Path $PSScriptRoot 'REQUEST_LOCK_PREPONLY.json'
if((Get-FileHash -LiteralPath $lockPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '__LOCK__'){throw 'Immutable lock changed.'}
$locked=Get-Content -LiteralPath $lockPath -Raw|ConvertFrom-Json
$entries=@($locked.formal,$locked.request,$locked.prompt,$locked.mask,$locked.mask_provenance,$locked.provenance,$locked.artist_review,$locked.actual_view_list,$locked.history,$locked.user_rejection,$locked.scope,$locked.auth,$locked.front_policy,$locked.provider,$locked.provider_configuration,$locked.local_status,$locked.future_whole)+@($locked.refs)
if($locked.fresh174){$entries+=@($locked.fresh174)}
foreach($item in $entries){if((Get-FileHash -LiteralPath $item.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256){throw ('Changed prepared input: '+$item.path)}}
$request=Get-Content -LiteralPath $locked.formal.path -Raw|ConvertFrom-Json -AsHashtable
if($request.Count -ne 8 -or $request.InputImages.Count -ne 3 -or $request.MaskFile -ne $locked.mask.path -or $request.Size -ne '960x1648' -or $request.Quality -ne 'high' -or $request.Background -ne 'transparent' -or $request.OutputDirectory -ne $PSScriptRoot){throw 'Exact request parameters changed.'}
for($i=0;$i -lt 3;$i++){if($request.InputImages[$i] -ne $locked.refs[$i].path){throw 'Reference order changed.'}}
$cfg=Get-Content -LiteralPath $locked.provider_configuration.path -Raw|ConvertFrom-Json
if($cfg.model -ne 'gpt-image-2.5-sunburst'){throw 'Configured provider model changed.'}
$defaults=Get-Content -LiteralPath 'D:/CODEX/魔术之心/image_defaults.json' -Raw|ConvertFrom-Json
if(-not $defaults.generation_prompt_prefix.enabled -or $defaults.generation_prompt_prefix.text -ne $locked.prefix_text -or -not ([IO.File]::ReadAllText($request.PromptFile)).StartsWith($locked.prefix_text,[StringComparison]::Ordinal)){throw 'Mandatory LEFT prefix changed.'}
foreach($name in @('attempt.json','result.json','request_manifest.json','prompt_effective.txt','character_api_original.png')){if(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name)){throw ('Existing attempt/result: recover, do not resubmit: '+$name)}}
# Preview ONLY: provider returns before key loading/output attempt/network.
$preview=& $locked.provider.path @request -Preview
if($preview.submitted -or $preview.n -ne 1 -or -not $preview.mask_provided -or $preview.input_count -ne 3 -or $preview.endpoint -ne 'https://api.openai.com/v1/images/edits'){throw 'Preview boundary changed.'}
$path=Join-Path $PSScriptRoot 'API_PREVIEW_VALIDATION.json'
if(Test-Path -LiteralPath $path){throw 'Preserve existing preview.'}
$data=@{id=$locked.id;PREPONLY=$true;actual_preview=$preview;exactlocksha='__LOCK__';request_sha256=$locked.formal.sha256;mask_sha256=$locked.mask.sha256;execution_released=$false;root_release_received=$false;transparent_background=$true;api_calls=0;native_calls=0;HTTP_calls=0;automatic_retries=0;no_key_decryption_or_network=$true;technical_preview_not_art_acceptance=$true}
[IO.File]::WriteAllText($path,($data|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))
$preview
'''.replace('__LOCK__',expected)
(P/'Preview-ExactRouteMaskOnly.ps1').write_text(ps,encoding='utf-8')
print(json.dumps(dict(lock=rec(lockpath),formal=lock['formal'],request=lock['request'],prompt=lock['prompt'],mask=lock['mask'],fresh174=solrecord,review=lock['artist_review']),ensure_ascii=False))
