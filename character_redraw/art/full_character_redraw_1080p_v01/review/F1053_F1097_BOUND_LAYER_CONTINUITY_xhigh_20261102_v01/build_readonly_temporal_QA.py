from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
import json
import hashlib

R=Path(__file__).resolve().parent
B=R.parents[1]
H=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):
    p=Path(p);d={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix.lower()=='.png':
        with Image.open(p) as im:d.update(size=list(im.size),mode=im.mode)
    return d
def put(name,d):
    f=R/name;assert not f.exists(),f
    f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rec(f)
def save(name,im):
    p=R/name;assert not p.exists();im.save(p);return rec(p)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
bindings_path=B/'dance_first10_reference_redraw_v01/EXPOSURE_BINDINGS.json'
priority_path=B/'dance_first10_reference_redraw_v01/PRIORITY_SCOPE.json'
registry_path=B/'ASSET_REGISTRY.json'
timeline_path=H/'data/original_timeline.json'
bindings=read(bindings_path);byframe={x['source_frame']:x for x in bindings['frames']}
timeline={x['frame']:x for x in read(timeline_path)}
states=read(priority_path)['states'];registry=read(registry_path)
ids=['ART-G12-54','ART-G12-55','ART-G12-56','ART-G12-57','ART-G12-58','ART-G12-59','ART-G12-60','ART-G33-57','ART-G33-58','ART-G12-63']
expected_starts=[1053,1058,1062,1067,1071,1075,1079,1084,1088,1093]
source_records=[]
for n in range(1053,1098):
    f=B/'coverage/source_frames'/f'F{n:06d}.png';assert f.exists()
    assert byframe[n]['source_pts']==timeline[n]['pts']
    source_records.append({'frame':n,'pts':timeline[n]['pts'],**rec(f)})
rows=[];panels=[]
head_roi=[500,60,1450,760]
for id,first in zip(ids,expected_starts):
    state=next(s for s in states if s['id']==id)
    assert state['first_frame']==first
    b=byframe[first]['actual_selected_asset_binding'];assert b['id']==id
    layer=Path(b['layer_1080']);master=Path(b['master_image'])
    assert sha(layer)==b['layer_sha256'] and sha(master)==b['master_sha256']
    assert registry[id]['sha256']==b['master_sha256']
    last=state['last_frame'];group=[byframe[n] for n in range(first,last+1)]
    unique={json.dumps({'layer_sha256':g['actual_selected_asset_binding']['layer_sha256'],'scale':g['actual_selected_asset_binding']['scale'],'translation':g['actual_selected_asset_binding']['translation']},sort_keys=True) for g in group}
    assert len(unique)==1
    source=B/'coverage/source_frames'/f'F{first:06d}.png'
    with Image.open(source) as im:original=im.convert('RGB')
    with Image.open(layer) as im:rgba=im.convert('RGBA');assert rgba.size==(1920,1080)
    white=Image.new('RGBA',rgba.size,'white');white.alpha_composite(rgba);white=white.convert('RGB')
    black=Image.new('RGBA',rgba.size,'black');black.alpha_composite(rgba);black=black.convert('RGB')
    board=Image.new('RGB',(1920,1330),(243,243,240));d=ImageDraw.Draw(board)
    d.text((12,6),f'{id}  F{first}..{last}  PTS {state["first_pts"]}..{state["end_pts"]}  | SOURCE / EXACT BOUND LAYER',font=font,fill='black')
    d.text((12,42),'Source full: uniform 0.5 thumbnail',font=small,fill='black')
    d.text((972,42),'Bound current full: white alpha QA, uniform 0.5',font=small,fill='black')
    board.paste(original.resize((960,540),Image.Resampling.LANCZOS),(0,68))
    board.paste(white.resize((960,540),Image.Resampling.LANCZOS),(960,68))
    d.text((12,611),f'Source context 1x crop {head_roi}',font=small,fill='black')
    d.text((972,611),'Current same-canvas context 1x; no recenter/part transform',font=small,fill='black')
    board.paste(original.crop(head_roi),(5,640))
    board.paste(white.crop(head_roi),(965,640))
    # Source/current use identical fixed canvas ROI; only diagnostic compositing occurs.
    panel=save(f'{id}_F{first}_SOURCE_CURRENT_FULL_AND_CONTEXT.png',board)
    panels.append(panel)
    black_context=save(f'{id}_F{first}_CURRENT_CONTEXT_BLACK_1x.png',black.crop(head_roi))
    proposal=read(b['registration_proposal'])
    row={
        'id':id,'first_frame':first,'last_frame':last,'first_pts':state['first_pts'],'end_pts_exclusive':state['end_pts'],
        'canonical_source_frame':state['existing_source_canonical_frame'],'actual_source_first_full':rec(source),
        'canonical_full':rec(H/'cels'/id.removeprefix('ART-')/'source.png'),
        'exact_current_bound_layer':rec(layer),'exact_current_bound_master':rec(master),'binding_exact':b,
        'all_exposure_binding_entries':group,'same_exact_layer_and_uniform_transform_held_within_state':True,
        'registry_exact_snapshot':registry[id],'source_frame_priority_row':state,
        'proposal_source_head_region_xywh':proposal.get('scene_head_region_xywh'),
        'diagnostic_same_fixed_canvas_head_ROI':head_roi,'panel':panel,'black_context':black_context,
        'actual_view_declared_here':False,'note':'Evidence prepared only. Actual view list and new artistic findings are written separately after inspection.'
    }
    rows.append(row)
contacts=[]
for k in range(3):
    group=source_records[k*15:(k+1)*15]
    sheet=Image.new('RGB',(1920,2010),(243,243,240));d=ImageDraw.Draw(sheet)
    d.text((12,5),f'Original PV all-frame contact {k+1}/3  | no interpolation | static QA only',font=font,fill='black')
    for i,e in enumerate(group):
        x=(i%3)*640;y=42+(i//3)*392
        sid=byframe[e['frame']]['actual_selected_asset_binding']['id']
        d.text((x+8,y),f'F{e["frame"]}  {sid}  PTS {e["pts"]}',font=small,fill='black')
        with Image.open(e['path']) as im:thumb=im.convert('RGB').resize((640,360),Image.Resampling.LANCZOS)
        sheet.paste(thumb,(x,y+28))
    contacts.append(save(f'ALL45_SOURCE_FRAMES_CONTACT_{k+1:02d}.png',sheet))
blackboards=[]
for k in range(2):
    sheet=Image.new('RGB',(1900,2190),(243,243,240));d=ImageDraw.Draw(sheet)
    for i,e in enumerate(rows[k*5:(k+1)*5]):
        x=(i%2)*950;y=(i//2)*730
        d.text((x+10,y+2),f'{e["id"]} F{e["first_frame"]} current black 1x',font=small,fill='black')
        with Image.open(e['black_context']['path']) as im:sheet.paste(im,(x,y+30))
    blackboards.append(save(f'CURRENT_HEAD_CONTEXT_BLACK_CONTACT_{k+1:02d}.png',sheet))
oldboard=B/'review/F1058_UPTURN_SEQUENCE_COMPARISON_20261102_v01/F1053_F1071_source_vs_current.png'
assert sha(oldboard)=='e77739d28ed459276c11b64db670a1f708484f9bedb93c27556fc747baa6577f'
manifest=put('READONLY_INPUTS_AND_QA_MANIFEST.json',{
    'created_utc':datetime.now(timezone.utc).isoformat(),'scope_frames':[1053,1097],'source_frame_count':45,'drawing_state_count':10,
    'source_time_base':'1/16000','EXPOSURE_BINDINGS_at_read':rec(bindings_path),'PRIORITY_SCOPE':rec(priority_path),'original_timeline':rec(timeline_path),
    'current_selected_entries_only_snapshot':{id:registry[id] for id in ids},
    'user_F1058_policy':rec(B/'USER_CURL_F1058_UPSWING_START_AND_SOLID_REJECTION_20261102_v01.json'),
    'prior_source_motion_report_reference_only':rec(B/'review/SOURCE_MOTION_AUDIT_F1058_JUMP_20261102_v01.json'),
    'prior_5stage_board_reference_only':rec(oldboard),'all_original_source_frames':source_records,'states':rows,
    'new_source_contacts':contacts,'new_source_current_comparison_panels':panels,'new_black_context_contacts':blackboards,
    'thumbnail_transform':'Original/full-layer uniform0.5 or1/3 for diagnostic full-frame display only. Same fixed [500,60,1450,760] crop at1x for source/current contexts. No body/head recentering or nonuniform transformation.',
    'not_a_renderer_playback_or_artistic_acceptance_check':True,'old_actual_view_declarations_not_inherited':True,
    'new_art_generation_calls':0,'API_calls':0,'native_calls':0,'network_calls':0,'central_or_binding_or_asset_writes':0
})
print(json.dumps({'manifest':manifest,'panels':panels,'source_contacts':contacts,'black_contacts':blackboards},ensure_ascii=False))
