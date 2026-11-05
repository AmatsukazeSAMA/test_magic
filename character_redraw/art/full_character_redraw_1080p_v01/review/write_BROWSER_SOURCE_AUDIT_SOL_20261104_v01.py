from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageChops,ImageStat
import hashlib,json,re
B=Path('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01')
S=Path('D:/CODEX/手书素材/github_moshuzhixin_handoff/magic_maid_20261029')
E=B/'review/BROWSER_PLAYBACK_ROUTE_AND_G131112_SOURCE_AUDIT_SOL_20261104_v01'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
now=datetime.now(timezone.utc).isoformat()
def save(n,d):
 p=E/n;assert not p.exists(),str(p);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return p
plugin=Path('C:/Users/11515/.codex/plugins/cache/openai-bundled/browser/26.930.41038')
oldservice=Path('C:/Users/11515/.codex/plugins/cache/openai-bundled/browser/26.1016.61520/scripts/browser-service.mjs')
runtime=save('RUNTIME_PROBE.json',{
 'recorded_utc':now,'scope':'Current subagent supported tools and installed Browser plugin entry only; read-only',
 'actual_node_repl_calls':[{'code':'nodeRepl.write({cwd:nodeRepl.cwd,homeDir:nodeRepl.homeDir,tmpDir:nodeRepl.tmpDir,hasBrowser:typeof browser,hasBrowserClient:typeof browserClient,globalKeys:Object.keys(globalThis).filter(k=>/browser|play|client|runtime/i.test(k))});','result':{'cwd':'D:\\CODEX\\魔术之心','homeDir':None,'hasBrowser':'undefined','hasBrowserClient':'undefined','globalKeys':[]}}, {'code':'nodeRepl.write({browser:typeof browser,browserClient:typeof browserClient,agent:typeof agent});','result':{'browser':'undefined','browserClient':'undefined','agent':'undefined'}}],
 'actual_node_fs_stat_probe':[{'path':str(oldservice),'exists':False,'code':'ENOENT','message':"ENOENT: no such file or directory, stat 'C:\\Users\\11515\\.codex\\plugins\\cache\\openai-bundled\\browser\\26.1016.61520\\scripts\\browser-service.mjs'"},{'path':str(plugin/'scripts/browser-service.mjs'),'exists':True,'isFile':True},{'path':str(plugin/'skills/SKILL.md'),'exists':False,'code':'ENOENT','message':"ENOENT: no such file or directory, stat 'C:\\Users\\11515\\.codex\\plugins\\cache\\openai-bundled\\browser\\26.930.41038\\skills\\SKILL.md'"}],
 'current_filesystem_verification':{'installed_browser_versions':[p.name for p in plugin.parent.iterdir()if p.is_dir()],'manifest_declared_skills':load(plugin/'.codex-plugin/plugin.json')['skills'],'skills_directory_entries':[p.name for p in (plugin/'skills').iterdir()],'current_service_exists':(plugin/'scripts/browser-service.mjs').is_file(),'current_client_exists':(plugin/'scripts/browser-client.mjs').is_file(),'old_worker_service_exists':oldservice.exists()},
 'failure_limit':'ENOENT above is an actual filesystem stat error, not a new browser-worker launch failure. No worker/browser start attempted. Installed client/service alone is not evidence of an attached supported browser.',
 'status':'no_documented_supported_browser_entry_or_attached_binding_in_this_agent',
 'browser_started':False,'local_preview_opened':False,'video_playback_performed':False,'dynamic_validated':False,'new_install_or_bridge':False,'network_calls':0,
 'next_supported_action':'Use supported Browser plugin UI/runtime reload or repair so its declared skill/API entry and matched worker are present; or have root use an already documented attached browser in its own context. Do not guess client exports, launch raw CDP, import private service source, or build a bridge.'
})
ledger=load(B/'coverage/EXPOSURE_LEDGER.json')
timeline=load(S/'data/original_timeline.json')
rows={x['frame']:x for x in ledger['frames']}
pts={x['frame']:x['pts']for x in timeline}
cases=[];viewed=[];files=[runtime,E/'TOOLS_METADATA.json',B/'coverage/EXPOSURE_LEDGER.json',S/'data/original_timeline.json',S/'work_sections/s06/timeline.csv',plugin/'.codex-plugin/plugin.json',plugin/'docs/browser-troubleshooting.md']
for ident,canonical,first,wider in [('ART-G13-11',1209,1197,3647),('ART-G13-12',1200,1200,3650)]:
 r=B/'drawings'/ident/'v01';j=load(r/'JOB.json');reg=load(r/'REGISTRATION_PLAN.json');src=Path(j['source_image']);native=B/f'coverage/source_frames/F{canonical:06}.png';wide=B/f'coverage/source_frames/F{wider:06}.png';guide=r/'inputs/source_pose_guide.png';prov=S/'cels'/ident.removeprefix('ART-')/'PROVENANCE.json'
 assert pts[canonical]==j['source_pts'] and pts[wider]==reg['source_pts']
 assert sha(src)==j['source_image_sha256'] and sha(wide)==j['production_reference']['source_image_sha256']
 assert src.read_bytes()==native.read_bytes()
 c={'id':ident,'canonical_sample':{'frame':canonical,'pts':pts[canonical],'source':str(src),'native_bytes_equal':True},'first_M10_occurrence':{'frame':first,'pts':pts[first]},'existing_wider':{'frame':wider,'pts':pts[wider],'source':str(wide),'guide':str(guide)},'time_base':'1/16000','actual_source_observation':('1197/1209完整并看，睁眼O嘴、双腕转开向下指组及袖肩胸线共同可见处未见实质重描/动作变化；3647较宽摄影显示更多原腰/后带。'if ident.endswith('11')else'1200/3650完整并看，双闭睫、tiny O与胸前错层横铺指组均一致可读，非11的睁眼下垂手；3650扩展原帽顶和下apron/后带可见范围。'),'same_author_cel_certified':False,'photography_validated':False,'mapping_change_proposed':False}
 if ident.endswith('11'):
  a=Image.open(B/'coverage/source_frames/F001197.png').convert('RGB').crop((0,0,1320,1080));b=Image.open(native).convert('RGB').crop((0,0,1320,1080));diff=ImageChops.difference(a,b)
  c['visible_region_support_only']={'region_native_xyxy':[0,0,1320,1080],'pixel_difference_bbox':diff.getbbox(),'mean_absolute_RGB_difference':ImageStat.Stat(diff).mean,'limit':'Supporting comparison after actual viewing; excludes right subtitle bars, not author-cel identity proof.'}
  c['canonical_vs_first_clarification']='First occurrence1197 and representative sample1209 are distinct roles. Existing source provenance and reviewed exposure ledger already record reuse; frame-number difference is not a mapping bug or reason to add a state.'
  viewed.append(B/'coverage/source_frames/F001197.png')
 viewed += [src,native,wide,guide];files += [src,native,wide,guide,r/'JOB.json',r/'REGISTRATION_PLAN.json',prov]
 for q in r.glob('direct*/DIRECT_REQUEST.json'):files.append(q)
 cases.append(c)
viewed=list(dict.fromkeys(viewed))
ownership=save('SOURCE_OWNERSHIP.json',{'recorded_utc':now,'reviewer':'Sol xhigh read-only actual source check','actual_viewed_paths':[str(p)for p in viewed],'cases':cases,'selected_exposure_rows':[rows[x]for x in [1197,1209,1200,3647,3650]],'finding':'No source-ID swap or evidence requiring mapping repair found. Do not infer author-cel identity or camera equivalence; do not use fixed frame offset alone.','consumer_note':'Use reviewed resolved_canonical_ids/binding_review for current ownership; old M25 source CSV candidate labels remain historical unresolved inputs. No central edits made.','central_modified':False,'new_states_created':0})
D=Path('D:/CODEX/魔术之心/art/20261102_first_dance_66states_review_v01');receipt=load(D/'DELIVERY_RECEIPT.json');play=load(D/'PLAYBACK_MANIFEST.json')
files += [D/'DELIVERY_RECEIPT.json',D/'PLAYBACK_MANIFEST.json',D/'index.html',ownership]
report=save('REPORT.json',{'recorded_utc':now,'reviewer':'Sol xhigh independent read-only production check','runtime_probe':str(runtime),'source_ownership':str(ownership),'actual_source_viewed_paths':[str(p)for p in viewed],
 'existing_preview_limit':{'directory':str(D),'source_frame_range':receipt['source_frame_range'],'exposures':receipt['exposures'],'unique_artworks':receipt['unique_artworks'],'time_base':receipt['time_base'],'receipt_created_utc':receipt['created_utc'],'package_claim_actual_continuous_playback_validated':receipt['actual_continuous_playback_validated'],'scope':'Historical first-dance package F834..1133, not G13 source1197/1200/1209 or wider3647/3650. Its build-time all_bindings_current does not establish current latest-curl-policy acceptance. No current binding refresh/encoding audit performed here.'},
 'actionable_next_steps':['Restore the official documented Browser plugin entry/matched runtime through supported UI, or root may use a documented attached browser in its own context. Then actually watch local preview at1x and0.5x and save direct playback evidence.','Keep G13-11 canonical1209/PTS645440, first occurrence1197/PTS639040 and wider3647/PTS1947552 separately named. No mapping fix justified.','Keep G13-12 canonical1200/PTS640640 and wider3650/PTS1949152; retain closed-lash chest-spread-hand distinction from11.','For either state, perform separate native-camera whole-uniform photography after art repair; do not reuse the first-dance package or technical decode as their dynamic validation.'],
 'evidence_sha256':{str(p):sha(p)for p in dict.fromkeys(files)},'video_playback_performed':False,'actual_continuous_playback_validated':False,'dynamic_validated':False,'photography_validated':False,'user_accepted':False,'generation_calls':0,'network_calls':0,'central_modified':False,'bindings_modified':False,'installations_modified':False})
md=E/'README.md';assert not md.exists()
md.write_text('本轮实际制作检查：仍无本子线程可用的受支持播放入口，**未播放**。\n\n'
 'node_repl可调用，但browser/browserClient/agent均undefined。当前Browser26.930.41038的service/client存在，manifest声明skills目录却为空；实际stat技能入口及旧26.1016.61520服务路径均ENOENT。新探针原文/文件证据已存，不把这些stat结果伪称新worker启动失败，也未安装、建桥或猜私有API。\n\n'
 '源归属实际核查未发现需要改mapping的证据：G13-11的1197与代表1209共同人物线/眼口/下垂指组未见实质变化，3647为既有较宽范围；first与canonical不同不是bug。G13-12的1200/3650闭睫、胸前横铺长指属于12，未混11。两cels原图分别与native1209/1200字节一致，PTS匹配原timeline。不能据此认证author cel或摄影相同。\n\n'
 '下一步：通过受支持Browser插件UI恢复完整技能/API入口和匹配worker，或由root已有合法绑定实看本地1x/0.5x。历史首舞包仅F834–1133/300曝光，不含本11/12源范围，也不能继承最新卷政策通过。0生成/网络/中央/绑定修改。\n',encoding='utf8')
print(json.dumps({'report':str(report),'report_sha256':sha(report),'runtime_sha256':sha(runtime),'ownership_sha256':sha(ownership),'readme_sha256':sha(md),'cases':[{k:c[k]for k in ['id','canonical_sample','first_M10_occurrence','existing_wider','mapping_change_proposed']}for c in cases]},ensure_ascii=False,indent=2))
