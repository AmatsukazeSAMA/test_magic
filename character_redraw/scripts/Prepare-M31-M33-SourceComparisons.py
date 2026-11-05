"""Read-only explicit nominations after the root viewed all chapter frames."""
from pathlib import Path
import json
base=Path(__file__).resolve().parent.parent/'art/full_character_redraw_1080p_v01'
jobs={j['id']:j for j in json.loads((base/'REDRAW_PLAN.json').read_text(encoding='utf-8-sig'))['jobs']}
specs={
 'M31': [('ART-G48-01',4337,4339),('ART-G48-02',4340,4341),('ART-G48-03',4342,4344),('ART-G48-04',4345,4347),('ART-G48-05',4348,4351),('ART-G48-06',4352,4354)],
 'M33': [('ART-G49-01',4401,4405),('ART-G49-02',4406,4409),('ART-G49-03',4410,4414),('ART-G49-04',4415,4418),('ART-G49-05',4419,4423),('ART-G49-06',4424,4430)],
}
for chapter,rows in specs.items():
    target=base/f'coverage/review/{chapter}_SOURCE_REUSE_NOMINATIONS_v01.json'
    if target.exists(): raise SystemExit('Preserve existing nominations.')
    nominations=[]
    for id_,start,end in rows:
        crop=jobs[id_]['crop_xyxy']
        nominations.append({'canonical_id':id_,'start_frame':start,'end_frame':end,
          'canonical_diagnostic_crop_xyxy':crop,'current_diagnostic_crop_xyxy':crop})
    spec={'chapter':chapter,'output_directory':str(base/f'coverage/review/{chapter}_source_comparison_v01'),
      'scope':'Root actually viewed all chapter contact pages; source comparison nominations only, not acceptance or output registration.',
      'nominations':nominations}
    target.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)
