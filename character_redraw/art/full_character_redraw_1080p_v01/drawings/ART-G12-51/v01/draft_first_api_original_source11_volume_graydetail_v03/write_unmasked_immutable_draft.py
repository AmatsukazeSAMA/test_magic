from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
import json,hashlib,difflib,copy
R=Path(__file__).parent;CEL=R.parent;OLD=CEL/'draft_first_api_source11_volume_graydetail_v02'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);v={'path':str(p),'sha256':sha(p)}
 if p.suffix=='.png':v['size']=list(Image.open(p).size)
 return v
def put(p,v):assert not p.exists(),p;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
oldq=OLD/'DRAFT_API_REQUEST.json';assert sha(oldq)=='c5ea4be05c7f3c362a7d98ca3f85e91c4e9a244c2346325c320314df32b0e477'
parent=json.loads(oldq.read_text(encoding='utf-8'));oldprompt=Path(parent['PromptFile']).read_text(encoding='utf-8')
assert sha(parent['PromptFile'])=='6e124df3dbc1de8dead1d3cbe0aeb1fc71c3605048f927e4bf52980cec37edf9'
changes=[
 ('参考1是原PV1033同一坐标的脸、帽叶、双手、身体、腰裙原像素，','参考1是原PV1033完整guide，仅整幅裁空[16,0,736,992]，未挖除头像、未做颜色像素选择；原帽褶与两黑叶、脸眼、双手、身体和腰裙全部源像素保持同一坐标，'),
 ('参考1去掉原红高卷的透明选区只是技术选择边，不能画成头/帽/手断面；连续补齐新灰bob和完整帽褶，不能抄原红发残线。','参考1保留完整红头和原双高卷，仅作动作、头饰和比例依据；请一次连贯重建灰bob、低耳后两珠及参考3/4的一束连续钻发，不能复制原红发、双高卷或高根，不做拼贴接头。')]
newprompt=oldprompt
for before,after in changes:assert newprompt.count(before)==1;newprompt=newprompt.replace(before,after,1)
restored=newprompt
for before,after in reversed(changes):restored=restored.replace(after,before,1)
assert restored.encode('utf-8')==oldprompt.encode('utf-8')
pf=R/'DRAFT_prompt.txt';assert not pf.exists();pf.write_text(newprompt,encoding='utf-8')
sourceprov=R/'UNMASKED_SOURCE_PROVENANCE.json';sp=json.loads(sourceprov.read_text(encoding='utf-8'));first=sp['reference']['path']
q=copy.deepcopy(parent);q['InputImages'][0]=first;q['reference_sha256'][0]=sha(first)
q['reference_roles'][0]='Original1033 FULL unmasked guide, only whole-canvas trim[16,0,736,992]; all original head/cap/2blackleaves/face/eyes/hands/body/waist/apron pixels retained, no colorpixel selection or headholes. Sole originalpose/headbody/headtilt/neutraldotmouth/fingercontact/costume/occlusion/realhalfbodycrop authority; oldredidentity/twohighcoils/highroot NOT copied. Coherent whole grayidentity rebuilding, no pastedhead.'
q['PromptFile']=str(pf);q['prompt_sha256']=sha(pf)
q['source_commonlayout']['sourcehead_not_masked']=True
q['source_reference_method_override']={'source_full_head_cap_leaves_retained':True,'source_color_pixel_selection':False,'source_head_mask':False,'only_crop_xyxy':[16,0,736,992],'source_original_size':[768,992],'source_reference_size':[720,992],'per_part_transform':False,'source_pixels_all_unchanged':True,'parent_masked_preparation_preserved_not_used':str(OLD)}
assert q['Size']=='720x992' and q['InputImages'][1:]==parent['InputImages'][1:]
assert q['reference_sha256'][1:]==parent['reference_sha256'][1:] and q['reference_roles'][1:]==parent['reference_roles'][1:]
assert [sha(x) for x in q['InputImages']]==q['reference_sha256']
assert Image.open(first).convert('RGBA').tobytes()==Image.open(CEL/'inputs/source_pose_guide.png').convert('RGBA').crop([16,0,736,992]).tobytes()
now=datetime.now(timezone.utc).isoformat()
refs=[{'path':p,'sha256':h,'role':role} for p,h,role in zip(q['InputImages'],q['reference_sha256'],q['reference_roles'])]
prov=R/'SIX_REFERENCE_PROVENANCE.json';put(prov,{'id':'ART-G12-51','created_utc':now,'parent_immutable_draft':ev(oldq),'source_unmasked_provenance':ev(sourceprov),'references':refs,'sourcechange':'Onlyref1 switches to fulloriginalguide compactcrop. Other5 exactrefs/roles unchanged. No colorselection/headhole/sourceparttransform.','parent_v02_provenance_retained':parent['references_provenance'],'prompt_only_two_source_method_replacements':changes,'input_hypothesis':'Preserve original fullhead/cap/2leaves context during coherent identity transfer; maskedhead can compete with cap continuity, a process inference from prior13returns, not a proven model bug.','API_calls':0,'native_calls':0,'central_write':False})
actual=[first,R/'diagnostics/REF1_UNMASKED_white_1x.png',R/'diagnostics/REF1_UNMASKED_black_1x.png',R/'diagnostics/ORIGINAL51_HEAD_CAP_TWO_LEAVES_EYES_2x.png']
review=R/'ARTIST_REFERENCE_REVIEW.json';put(review,{'id':'ART-G12-51','created_utc':now,'state':'ACTUAL_SOURCE_VIEW_PREPARATION_ONLY','actual_fresh_viewed':[ev(p) for p in actual],'other5_reviewed_sameSHA_inputs_unchanged':refs[1:],'parent_actual_review_retained':parent['artist_actual_review'],'source_observation':'Fulloriginal cap/frill andexact2blackleaves visible. Original unequal roundopeneyes andtinyneutralcloseddotmouth preserved. IMAGELEFT raisedthumb/indexloop plus3fingers andothercrossbowdownbentwrist separatedfingers remain. All sourcewaist/apron/backtails/halfbodybottom retained. Originalred2highcoils are actioncontext, not newgrayidentity/root.','root_rule':'AnatomicalLEFT at IMAGERIGHT lowearbehindbobnape,2beads plus1continuouscoil. Source root/hairidentity not copied.','motion_volume_rule_unchanged':'R163 onlycoilcompression/recoil; preserve comparable bundleamount toR157 withlowerfrillocclusion. Correct11fullheadcoil volume plus latestbroadGRAYdetail remain geometry/volumeauthority, not miniaturecolumn.','sourceguide_unmasked':True,'no_source_colorselection':True,'all_sourcepixel_positions_unchanged':True,'source_only_hypothesis_changed_not_art_pass':True,'API_calls':0,'native_calls':0,'central_write':False})
q['references_provenance']=ev(prov);q['artist_actual_review']=ev(review)
dp=R/'DRAFT_API_REQUEST.json';put(dp,q)
diff=R/'UNMASKED_SOURCE_METHOD_DIFF.txt';assert not diff.exists()
diff.write_text(''.join(difflib.unified_diff(oldprompt.splitlines(keepends=True),newprompt.splitlines(keepends=True),fromfile='v02/DRAFT_prompt.txt',tofile='v03/DRAFT_prompt.txt'))+'\nRequest changed fields: '+', '.join(k for k in sorted(set(parent)|set(q)) if parent.get(k)!=q.get(k))+'\n',encoding='utf-8')
for name in ['API_PREPARED_REQUEST.json','attempt.json','character_api_original.png']:assert not (CEL/name).exists(),name
validation=R/'PRIVATE_PREP_VALIDATION.json';put(validation,{'id':'ART-G12-51','created_utc':now,'draft':ev(dp),'Size':'720x992','source_ref_crop_equals_originalpixels':True,'all_sourcehead_cap_leaves_face_hands_body_retained':True,'other5_ref_paths_hashes_roles_unchanged':True,'prompt_outside_two_source_method_replacements_identical':True,'all_currentrefs_SHA_verified':True,'oldimmutable_preserved':ev(oldq),'formal_attempt_raw_absent':True,'calls':0,'inflight':0,'central_write':False,'technical_not_artistic_approval':True})
hp=R/'ARTIST_PREPARATION_HANDOFF.json';put(hp,{'id':'ART-G12-51','created_utc':now,'status':'PREP_ONLY_WAIT_ROOT_SPECIFIC_RELEASE','draft':ev(dp),'prompt':ev(pf),'source_ref':ev(first),'provenance':ev(prov),'artist_actual_review':ev(review),'diff':ev(diff),'Size':'720x992','other5_refs_unchanged':True,'API_calls':0,'native_calls':0,'inflight':0,'central_write':False})
print(json.dumps({'draft':ev(dp),'prompt':ev(pf),'source_ref':ev(first),'provenance':ev(prov),'handoff':ev(hp),'Size':q['Size'],'calls':0},ensure_ascii=False))
