from pathlib import Path
from PIL import Image, ImageDraw
from datetime import datetime,timezone
import json,hashlib,shutil
B=Path(r'D:\CODEX\魔术之心\art\full_character_redraw_1080p_v01')
R51=B/'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02'
R14=B/'drawings/ART-G33-14/v01/draft_first_api_original_rear_cap11_volume_graydetail_v02'
O51=B/'drawings/ART-G12-51/v01/draft_first_api_source_commonlayout_locked11_v01'
O14=B/'drawings/ART-G33-14/v01/draft_first_api_rear_commonlayout_locked11_v01'
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p):
 p=Path(p);d={'path':str(p),'sha256':h(p)}
 if p.suffix=='.png':d['size']=list(Image.open(p).size)
 return d
def copy(src,dst):
 assert not dst.exists(),dst;shutil.copyfile(src,dst)
 return {**ev(dst),'source':ev(src),'operation':'exact byte copy of actual-reviewed readonly input'}
def save(im,p):assert not p.exists(),p;im.save(p);return ev(p)
def put(p,z):assert not p.exists(),p;p.write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rawp=B/'drawings/ART-G33-11/v01/character_api_original.png';raw=Image.open(rawp).convert('RGBA')
white=Image.new('RGBA',raw.size,(255,255,255,255));white.alpha_composite(raw)
contextbox=[120,65,375,400];context=white.crop(contextbox)
geom=raw.crop([274,228,351,382]);master=Image.open(B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png').convert('RGBA');assert geom.tobytes()==master.tobytes()
detailp=B/'inputs/user_Roman_curl_broad_gray_open_turns_20261101_v01.png';assert h(detailp)=='4a6340a1d810f93ce0111f6c66232cb92152627d5c64c1d904195254bd645cb4'
detailbox=[35,41,146,260];detail=Image.open(detailp).crop(detailbox)
refs51=[]
refs51.append(copy(O51/'inputs/ref1_ORIGINAL1033_COMMON_OPEN_EYES_NEUTRAL_MOUTH_FULL_HANDS_WAIST_APRON_v02_NO_RED_IN_FINGER_LOOP.png',R51/'inputs/ref1_ORIGINAL1033_COMMON_LAYOUT_FULL_HANDS_NEUTRAL_DOT_MOUTH.png'))
refs51.append(copy(O51/'inputs/ref2_R163_COIL_ONLY_MOTION_NO_FACE_ROOT_ACTION.png',R51/'inputs/ref2_R163_HAIR_ONLY_COMPRESSION_RECOIL.png'))
refs51.append({**ev(R51/'inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'),'source':ev(rawp),'source_crop_xyxy':contextbox,'operation':'original head+cap+beads+fullcoil kept in same coordinates; clean white alpha composite only; geometry and relative volume context, not sourcepose/expression/material highlights'})
refs51.append({**save(detail,R51/'inputs/ref4_LATEST_USER_WIDE_GRAY_RETURN_THIN_MINT_DETAIL_NO_ROOT.png'),'source':ev(detailp),'crop_xyxy':detailbox,'operation':'readonly crop to exclude beads/root/face; costume edge context not authoritative'})
refs51.append(copy(B/'inputs/eye_G02-01_F100.png',R51/'inputs/ref5_G02_SINGLE_CHARCOAL_METHOD_SOURCE_EYES_WIN.png'))
refs51.append(copy(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',R51/'inputs/ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png'))

refs14=[]
guidep=B/'drawings/ART-G33-14/v01/inputs/source_pose_guide.png';guide=Image.open(guidep)
refs14.append({**save(guide.crop([64,0,544,1072]),R14/'inputs/ref1_ORIGINAL2362_FULL_REAR_GUIDE_HEAD_CAP_UNCUT_COMMON_LAYOUT.png'),'source':ev(guidep),'crop_xyxy':[64,0,544,1072],'operation':'whole-canvas compact crop only, all original head/cap pixels retained; no source head holes, masks or per-part moves'})
refs14.append(copy(O14/'inputs/ref2_R043_COIL_ONLY_MOTION_NO_BEADS_FACE_ROOT_ACTION_v02.png',R14/'inputs/ref2_R043_HAIR_ONLY_COMPRESSION_NO_BEADS_ROOT_FACE.png'))
capbox=[161,39,347,113]
refs14.append({**save(guide.crop(capbox),R14/'inputs/ref3_ORIGINAL_REAR_WHITE_MAIDCAP_TWO_BLACK_LEAVES_COMPLETE.png'),'source':ev(guidep),'crop_xyxy':capbox,'operation':'readonly complete sourcecap+2blackleaves crop. Redhair rim only context; never root/hairidentity authority'})
mask=Image.new('L',context.size,255);draw=ImageDraw.Draw(mask)
facepoly=[(57,145),(66,119),(83,99),(91,105),(105,130),(113,144),(125,151),(129,115),(139,96),(154,104),(166,119),(177,129),(184,135),(187,121),(202,142),(210,150),(210,164),(200,179),(183,194),(158,206),(137,213),(118,217),(94,209),(75,195),(62,176)]
draw.polygon(facepoly,fill=0)
masked=Image.new('RGBA',context.size,(0,0,0,0));masked.paste(context,(0,0),mask)
# Keep the complete exact geometry area in original context; this restores tiny cheek/garment context, never eyes/mouth.
gbox=[154,163,231,317];masked.paste(context.crop(gbox),gbox[:2]);mask.paste(255,gbox)
mp=R14/'inputs/CORRECT11_CONTEXT_FACE_EXCLUSION_MASK.png';save(mask,mp)
refs14.append({**save(masked,R14/'inputs/ref4_CORRECT11_BOB_CAP_FULL_COIL_VOLUME_CONTEXT_EYES_MOUTH_EXCLUDED.png'),'source':ev(rawp),'source_crop_xyxy':contextbox,'operation':'readonly fullhead/fullcoil context, face performance excluded with original-pixel mask; same scale/coordinates; exact geometry area retained; no art repaint','face_exclusion_polygon_context_xy':facepoly,'geometry_restore_context_xyxy':gbox,'mask':ev(mp)})
refs14.append({**save(detail,R14/'inputs/ref5_LATEST_USER_WIDE_GRAY_RETURN_THIN_MINT_DETAIL_NO_ROOT.png'),'source':ev(detailp),'crop_xyxy':detailbox,'operation':'readonly detail crop, no bead/root/face; costume context does not own new pose'})
refs14.append(copy(B/'drawings/ART-G12-34/v03/inputs/unlit_hair_material_palette.png',R14/'inputs/ref6_UNLIT_GRAY_MINT_PIGMENTS_ONLY.png'))

for ident,run,old,refs in [('ART-G12-51',R51,O51,refs51),('ART-G33-14',R14,O14,refs14)]:
 diags=[]
 for i,ref in enumerate(refs):
  im=Image.open(ref['path']).convert('RGBA')
  if i in ([0,2,3] if ident=='ART-G12-51' else [0,2,3,4]):
   for name,c in [('white',(255,255,255)),('black',(0,0,0))]:
    out=Image.new('RGBA',im.size,(*c,255));out.alpha_composite(im)
    p=run/'diagnostics'/f'REF{i+1}_{name}_1x.png';save(out.convert('RGB'),p);diags.append(ev(p))
    if i>0:
     p=run/'diagnostics'/f'REF{i+1}_{name}_3x.png';save(out.convert('RGB').resize((im.width*3,im.height*3),Image.Resampling.NEAREST),p);diags.append(ev(p))
  if i==1:
   p=run/'diagnostics/REF2_HAIR_ONLY_5x.png';save(im.resize((im.width*5,im.height*5),Image.Resampling.NEAREST),p);diags.append(ev(p))
 put(run/'SIX_REFERENCE_PROVENANCE.json',{'id':ident,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'LATEST_REFERENCE_PREPARATION_ONLY_NOT_SUBMITTED','references':refs,'previous_preparation_preserved':str(old),'previous_readonly_provenance':ev(old/'READONLY_REFERENCE_PROVENANCE.json'),'change_reason':'Latest user detail has wideGRAYmain/ thinmint/continuous returns; full correct11headcoil context prevents miniaturecolumn. For14 originalsourcehead/cap untouched and sourcecap-leaves explicit; plainbackbob removed after13capfailure lesson.','headcoil_context_source':ev(rawp),'headcoil_context_crop_xyxy':contextbox,'context_white_composite':'clean QA composite, no retained visible art pixels altered','exact_geometry_lock':ev(B/'inputs/user_approved_G33-11_curl_geometry_only_20261101_v01.png'),'geometry_embedded_raw_crop_xyxy':[274,228,351,382],'embedded_raw_crop_pixels_exact':True,'embedded_raw_crop_png_sha256':'13e5094fc0cec20d4e34d42f75a2c5b28f05edde67654935988fad3e49c69959','latest_user_original':ev(detailp),'latest_detail_crop_xyxy':detailbox,'source_guide_compact_crop_xyxy':[16,0,736,992] if ident=='ART-G12-51' else [64,0,544,1072],'source_canvas':[720,992] if ident=='ART-G12-51' else [480,1072],'source_transform':{'uniform_scale':1,'translation':[-16,0] if ident=='ART-G12-51' else [-64,0],'per_part_transform':False},'G02_omitted':ident=='ART-G33-14','plain_backbob_omitted':ident=='ART-G33-14','source_first_ref_head_not_masked':ident=='ART-G33-14','diagnostics':diags,'rejected13_49a3_ead15c_not_used':True,'API_calls':0,'native_calls':0,'formal_written':False,'central_write':False})
 print(json.dumps({'id':ident,'refs':[{'sha256':r['sha256'],'size':r['size']} for r in refs],'provenance':ev(run/'SIX_REFERENCE_PROVENANCE.json'),'calls':0},ensure_ascii=False))
