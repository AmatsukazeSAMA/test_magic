const {chromium}=require('C:/Users/11515/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..','magic_maid_20261029'),errors=[];
const check=(ok,message)=>{if(!ok)throw new Error(message)};
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,
  args:['--allow-file-access-from-files','--disable-background-networking','--no-first-run'],
  env:{...process.env,TEMP:path.join(root,'logs'),TMP:path.join(root,'logs')}});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1100}});page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root,'index.html')).href,{waitUntil:'load'});
  check(await page.locator('#chapterCards .card').count()===37,'37 chapter cards');
  check(await page.locator('#exposureRows tr').count()===26,'26 exposure rows');
  check(await page.locator('#reminderCards .card').count()===6,'6 reminder cards');
  check(await page.evaluate(()=>magicMaid.data.panels.length)===411,'411 reference panels');
  await page.locator('#goto').fill('0');await page.locator('#go').click();
  check(await page.locator('#frame').getAttribute('src')==='frames/F000000.png','zero-based first PNG');
  await page.locator('#next').click();check((await page.locator('#sourceCounter').textContent()).startsWith('F000001'),'next video frame');
  await page.locator('#goto').fill('4762');await page.locator('#go').click();await page.locator('#frame').evaluate(im=>im.decode());
  check(await page.locator('#frame').evaluate(im=>im.naturalWidth)===1920,'native 1080p source');
  await page.locator('#next').click();check((await page.locator('#sourceCounter').textContent()).startsWith('F004762'),'end boundary clamp');
  await page.locator('[data-tab="library"]').click();await page.locator('#groupFilter').selectOption('G12');
  check((await page.locator('#libraryCount').textContent()).startsWith('75张'),'G12 75 reference panels');
  check(await page.locator('#libraryCards .card').count()===24,'library pagination size');await page.locator('#nextPage').click();
  check(await page.locator('#libraryCards .card').first().getAttribute('data-id')==='G12-25','second page starts at 25');
  await page.locator('#resetFilters').click();await page.locator('#originFilter').selectOption('supplement');
  check((await page.locator('#libraryCount').textContent()).startsWith('71张'),'71 source supplements');
  await page.locator('#typeFilter').selectOption('character');check((await page.locator('#libraryCount').textContent()).startsWith('49张'),'49 red costume poses');
  await page.locator('#search').fill('X01-01');check(await page.locator('#libraryCards .card').count()===1,'search exact supplement');
  await page.locator('#libraryCards [data-id="X01-01"]').click();
  check((await page.locator('#sourceCounter').textContent()).startsWith('F004021'),'one-frame red pose navigation');
  check(await page.locator('#referenceEmpty').isVisible(),'supplement has explicit missing tutorial state');
  await page.locator('#seekBoth').click();
  const sourceTime=await page.locator('#sourceVideo').evaluate(v=>v.currentTime);
  check(Math.abs(sourceTime-134.201)<.03,'actual PTS seek');
  await page.evaluate(()=>magicMaid.goPanel('G33-13'));
  await page.locator('#referenceImage').evaluate(im=>im.decode());check(await page.locator('#referenceImage').evaluate(im=>im.naturalWidth)===1920,'native reference PNG');
  const playback=await page.evaluate(async()=>{
    const result=[];
    for(const id of ['sourceVideo','referenceVideo']){
      const v=document.getElementById(id);v.muted=true;v.currentTime=2;await v.play();const before=v.currentTime;
      await new Promise(r=>setTimeout(r,350));v.pause();result.push({id,advanced:v.currentTime>before,width:v.videoWidth,height:v.videoHeight,error:v.error?.message??null});
    }return result;
  });check(playback.every(r=>r.advanced&&r.width===1280&&r.height===720&&!r.error),'both H264 video previews play');
  await page.locator('[data-tab="chapters"]').click();await page.evaluate(()=>{document.getElementById('mediaDetails').open=false;window.scrollTo(0,0)});
  await page.screenshot({path:path.join(root,'logs/workbench_desktop.png')});
  await page.evaluate(()=>magicMaid.showChapter('M24',true));
  check((await page.locator('#libraryCount').textContent()).startsWith('75张'),'reprise chapter refers back to original reference group');
  await page.locator('#clearScope').click();await page.locator('#resetFilters').click();await page.locator('#groupFilter').selectOption('G33');
  check((await page.locator('#libraryCount').textContent()).startsWith('68张'),'G33 68 whole-body references');
  await page.screenshot({path:path.join(root,'logs/library_desktop.png')});
  await page.setViewportSize({width:390,height:844});await page.evaluate(()=>{magicMaid.setTab('chapters');window.scrollTo(0,0)});
  await page.screenshot({path:path.join(root,'logs/workbench_mobile.png')});
  check(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'no mobile horizontal overflow');
  await page.locator('[data-tab="library"]').click();await page.locator('#libraryCards').scrollIntoViewIfNeeded();
  check(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'no mobile library overflow');
  await page.screenshot({path:path.join(root,'logs/library_mobile.png')});
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(pathToFileURL(path.join(root,'打开参考库.html')).href,{waitUntil:'load'});
  check(await page.evaluate(()=>magicMaid.data.portable),'portable viewer mode');
  await page.evaluate(()=>magicMaid.goPanel('X01-01'));await page.locator('#frame').evaluate(im=>im.decode());
  check((await page.locator('#frame').getAttribute('src')).startsWith('cels/'),'portable uses included native files');
  await page.locator('#goto').fill('4762');await page.locator('#go').click();await page.locator('#frame').evaluate(im=>im.decode());
  check((await page.locator('#sourceCounter').textContent()).startsWith('F004762'),'portable includes final source frame');
  check(errors.length===0,'browser errors: '+errors.join('; '));
  const result={status:'PASS',local_file_open:true,chapter_cards:37,reference_panels:411,opening_exposure_rows:26,reminder_cards:6,
    native_source_dimensions:[1920,1080],native_reference_dimensions:[1920,1080],exact_frame_navigation:true,actual_pts_seek:true,
    group_filter_pagination_and_search:true,chapter_reprise_reference_navigation:true,one_frame_red_pose_navigation:true,
    mobile_no_horizontal_overflow:true,portable_viewer_uses_included_files:true,both_video_playbacks:playback,
    page_errors:errors,human_full_continuous_viewing_claimed:false,
    screenshots:['logs/workbench_desktop.png','logs/library_desktop.png','logs/workbench_mobile.png','logs/library_mobile.png']};
  fs.writeFileSync(path.join(root,'data/BROWSER_CHECK.json'),JSON.stringify(result,null,2),'utf8');console.log(JSON.stringify(result));
 }finally{await browser.close();}
})().catch(e=>{fs.writeFileSync(path.join(root,'logs/browser_error.txt'),e.stack,'utf8');console.error(e);process.exitCode=1});
