from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
BASE=Path(__file__).resolve().parent.parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
ev=lambda p:{'path':str(Path(p)),'sha256':sha(p)}
oldp=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01.json'
oldmd=oldp.with_suffix('.md')
assert sha(oldp)=='8a44b66322e453ee9b04f0414faa418be1b6e06a2e903757db93c993edfd68f0'
assert sha(oldmd)=='8f58209002bb249507ae0de3f91bb56a870a39f2b49815b1372ad08c77cb2c84'
old=read(oldp)
tp=BASE/'review/USER_EYE_CORNER_SHORT_MARK_TOLERANCE_20261103_v01/USER_TOLERANCE.json'
assert sha(tp)=='4cab79a370d2b4db5dbec2ddb45740cb60858ec8750bed50d5731e7ae1cccee7'
t=read(tp)
assert t['id']=='ART-G51-10' and t['user_statement_verbatim']=='这种没事'
assert t['approved_scope']=='small_eye_corner_short_marks_as_shown' and t['eye_detail_user_accepted']
assert not t['user_accepted_whole_art']
assert t['exact_current_artwork']['sha256']==old['image_sha256']==sha(old['image'])
assert sha(t['user_attached_evidence']['path'])==t['user_attached_evidence']['sha256']
assert sha(old['current_policy']['path'])=='93d4dff912d4ab7bf08dfe08dbbfe2becb77424364c4489a9e43ddfc7fdf33e0'
for p,h in old['evidence_sha256'].items():assert sha(p)==h,p
RUN=Path(old['image']).parent
E=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v01_evidence'
reopened=[t['user_attached_evidence']['path'],str(RUN/'qa_white.png'),str(RUN/'qa_black.png'),*[str(E/n) for n in ['NEW_ROOT_GRAY_RETURNS_C_WHITE_4x.png','NEW_ROOT_GRAY_RETURNS_C_BLACK_4x.png','NEW_ROOT_GRAY_RETURNS_C_ALPHA_4x.png']]]
actual=list(dict.fromkeys(old['actual_viewed_paths']+reopened))
readpaths=list(dict.fromkeys(old['actual_read_paths']+[str(tp),str(oldp)]))
evidence={str(p):sha(p) for p in dict.fromkeys([Path(x) for x in actual+readpaths])}
checks=[
 'After actual currentwholeWB and exact user-shown5x reinspection,the two small outercorner shortmarks remain visiblypresent at approximately(446,261)/(614,235). They are now expressly USER_PERMITTED under the latest exactimage tolerance. No claim that pixels were removed or marks became connected eyelashes.',
 'Own4625 unequal roundopen eyes,tinyneutralclosedmouth,singlecharcoaliris/ordinarywhiteglints and genuine connected upperouterlashes remain; no other eye P1 found.',
 'WholeWB rechecked:own two unequal lowgloves,viewerRIGHT longnearverticalarm/lowglove versus viewerLEFT waistconnection/downleftglove,obliqueapron,leftflaredskirt,rightbackties/differentlegangles and two complete shoes preserved. Graygreen/blackbow/gold/whitecostume,graybob and2MAINblackleaves retained.',
 'Actual coilWB/alpha4x rechecked:single lowLEFT viewerRIGHT bob/nape root with partlyoccluded redbeads;two broadgrayfronts connect actualopaquegrayreturns and tapering smallC,narrowmint. Cinnerair switcheswhite/black;grayreturn patches stayopaque. No new closedcap/solidcolumn/extramainturn P1 found.',
 'Visible graycoil/headshoulder volume remains moderate. Frontshoulderdepth/hiddenroot remains uncertified P2; no imagecleanup or inferred hiddengeometry. UserX01 approval remains curl drawing only.',
 'WholeWB has no opaque backgroundcloud/petal/caption. Fine lowalpha edge/hiddenRGB remnants are retained without cleaning; sourcepose/shoecrop photography and temporal continuity remain unvalidated.'
]
report={
 'id':'ART-G51-10','reviewer':'Sol xhigh independent actual scope re-review under latest explicit user tolerance; not wholePREP author',
 'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'retained_static_candidate','review_status':'retained_static_candidate','independent_static_pass':True,
 'review_scope':'Same unchanged currentwhole re-evaluated under explicit eye-corner tolerance; no freshgeneration and no whole-art useracceptance.',
 'image':old['image'],'image_sha256':old['image_sha256'],'dimensions':old['dimensions'],'source':old['source'],'current_policy':old['current_policy'],
 'curl_structure_policy_id':'hollow_two_large_one_small_20261102_v04',
 'user_tolerance':{'record':ev(tp),'user_statement_verbatim':'这种没事','approved_scope':'small_eye_corner_short_marks_as_shown','exact_user_shown_image':t['user_attached_evidence'],'eye_detail_user_accepted':True,'whole_art_user_accepted':False,'effect':'Withdraw prior eye-shortmark-only P1 for this exact whole. Actual two marks stillpresent; no further dot-onlygeneration required. Does not grant blanket permission for unrelated obviousdecorative moles.'},
 'prior_v01_review_preserved':{'json':ev(oldp),'markdown':ev(oldmd),'prior_status':'repair_required','withdrawn_P1_code':'ISOLATED_UNDER_EYE_POINTS_NOT_REMOVED','withdrawal_reason':'Latest user expressly permitted these exact two shortmarks; change of applicable acceptance criterion,not a claim that the removal succeeded.'},
 'actual_viewed_paths':actual,'actual_reopened_in_this_scope_review':reopened,'actual_read_paths':readpaths,'evidence_sha256':evidence,
 'key_actual_checks':checks,'P1':[],'P1_count':0,'P2':old['P2'],'P2_count':len(old['P2']),
 'eye_short_marks_present':True,'eye_marks_removed_by_whole':False,'eye_short_marks_user_permitted':True,
 'generation_receipt_readback':old['generation_receipt_readback'],'repair_required_under_current_scope':False,
 'front_shoulder_route_certified':False,'root_attachment_hidden_geometry_certified':False,'photography_validated':False,'dynamic_validated':False,'actual_playback':False,'user_accepted':False,
 'generation_calls_this_review':0,'network_calls_this_review':0,'central_registry_JOB_REG_binding_modified':False
}
p=BASE/'review/SOL_WHOLE_G51_10_UNDEREYE_CURLBASELINE_20261103_v02_USER_TOLERANCE.json';assert not p.exists();p.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
md=p.with_suffix('.md');assert not md.exists()
md.write_text('G51-10 whole v02容差复审：retained_static_candidate，当前P1=0，保留P2×2。\n\n'
 '同一raw：'+old['image_sha256']+'。用户针对此whole眼部5x明确“这种没事”，容差记录SHA：'+sha(tp)+'。\n\n'
 '两处眼角小短点实际仍在，并非删点成功或改判相连睫毛；依最新用户明确允许，仅撤销旧眼角短点P1。旧v01 JSON/MD原字节和退修历史保留。此许可不扩成整稿/钻发/摄影/动态接受，也不全面豁免其它明显装饰痣。\n\n'
 '重看完整WB与用户所示眼5x、coilWB/alpha4x：本10圆睁不等眼/tiny闭口、两不等低手套、完整鞋、灰绿衣装与低LEFT单束2大+smallC保持；宽灰返回opaque，C孔确为透明，无其它新P1。肩前深度/隐藏root、softgray规整返线/细低alpha残留P2保持，未清理。\n\n'
 '0调用/网络/中央/摄影修改。whole-useraccepted、photography、dynamic均false。\n\nJSON SHA256：'+sha(p)+'\n',encoding='utf-8')
assert sha(oldp)=='8a44b66322e453ee9b04f0414faa418be1b6e06a2e903757db93c993edfd68f0'
assert sha(oldmd)=='8f58209002bb249507ae0de3f91bb56a870a39f2b49815b1372ad08c77cb2c84'
print(json.dumps({'report':ev(p),'markdown':ev(md),'status':'retained_static_candidate','P1':0,'old_report_unchanged':True,'raw_sha256':old['image_sha256']},ensure_ascii=False,indent=2))
