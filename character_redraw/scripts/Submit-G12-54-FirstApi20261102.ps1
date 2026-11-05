#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$base=Join-Path $root 'art/full_character_redraw_1080p_v01'
$parent=Join-Path $base 'drawings/ART-G12-54/v01'
$draft=Join-Path $parent 'draft_first_api_unmasked_source54_curl_assessment_v02_v01/DRAFT_API_REQUEST.json'
$q=Get-Content -LiteralPath $draft -Raw | ConvertFrom-Json
$run=Join-Path $parent 'api_first_source54_correct11_volume_upper_returns_v01'
if(Test-Path -LiteralPath (Join-Path $run 'attempt.json')) {throw 'Existing attempt; no automatic retry.'}
if(Test-Path -LiteralPath (Join-Path $run 'ROOT_RELEASE.json')) {throw 'Existing release preserved; inspect before any new submission.'}
$registry=Get-Content -LiteralPath (Join-Path $base 'ASSET_REGISTRY.json') -Raw | ConvertFrom-Json -AsHashtable
if($registry.ContainsKey('ART-G12-54')) {throw 'Drawing now has a selected asset; inspect before submitting.'}
$refs=@($q.InputImages)
for($i=0;$i -lt $refs.Count;$i++) {
    if((Get-FileHash -LiteralPath $refs[$i] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $q.reference_sha256[$i]) {throw 'Prepared reference hash changed.'}
}
$refs[2]=Join-Path $base 'drawings/ART-G12-51/v01/draft_first_api_source11_volume_graydetail_v02/inputs/ref3_USER_CORRECT11_HEAD_CAP_LOW_BEADS_FULL_SPIRAL_VOLUME_CONTEXT_white.png'
if((Get-FileHash -LiteralPath $refs[2] -Algorithm SHA256).Hash.ToLowerInvariant() -ne '216fd23b944b9da8b1234de207b6cfe75f29753bd9fefbd459ef2c8aa1919528') {throw 'Correct11 context hash changed.'}
$prompt=@'
以参考1原PV1054为唯一动作与裁切基准，画一个完整实际可见半身人物，720x1072，真实透明RGBA。保留原向画右的头身倾斜、圆睁双眼及视线、小波浪闭口、画右竖腕的拇食菱形闭环与另外三根分开的手指、另一手在胸前下垂分指、手和袖口接触叠压；保原高领黑长袖、黑白肩褶围裙腰带背结尾带、红胸结金扣、白帽及恰好两片黑叶。到原裙底裁停止，不补腿鞋、不画字和背景，不复制原红头发或双高卷。替换为短中性灰bob、暖桃肤和唯一人物解剖LEFT低耳后/颈侧双红珠罗马卷，不镜像人物。
参考2仅R177颈侧压紧回收、肩褶和手臂遮挡的摆动相位，不给动作、根侧、固有发量或结构。参考3给用户认可的完整头部与卷体相对大小、低珠连接、连续回绕和渐细末C，不照搬它的脸眼、抬手或竖直卷轴。当前画左可见近耳属于人物RIGHT，LEFT珠根应在远侧低耳后，结合bob/nape自然遮挡；不能移到可见近耳。手臂/白褶实际挡住下段时自然挡住，不把整根尾巴强拉到前面，也不缩发或扩大服装假装遮挡。
参考4是最新用户细节，只取宽灰发带的前面、向内/后的返回面和各圈连接。从根部第一圈到末梢都是同一束宽灰发带连续绕回，尤其上端不能是封口椭圆圆盘、实心灰筒上贴绿色螺线或分节帽堆。下端逐渐收细并连续回勾，不能截断、画小挂件或薄S线。真正露出的空气透明，应有的灰返回面保留不透明，不规定孔数或圈数。卷径和长度先与整颗头、肩、上臂核对，既不粗大压过头，也不缩成小挂件；不用统一固定头发比或缩放比例。AI微小露出裁图不代表整束很小。
参考5只给G02单色charcoal平填眼法和普通小圆白点，原1054的圆睁程度优先，不抄半睑或心形高光。参考6只定灰#B6B4B2、灰绿#B0C8BA与墨#171717。bob与卷体全部前面和返回面是相同无打光灰色，遮叠靠黑线，灰绿只材料条；不要体积暗块、渐变、银亮边或独立高光，不整束变绿。参考4精修图的打光不要移植。黑简笔PV线、平涂、原暖桃肤。整个可见人物一次连贯画完，bob、红珠、发卷、脖子、衣领、肩褶和原手势自然接合，无贴片接缝。只画一个人物，真实透明，不画背景字幕、棋盘格、色卡或新道具。
'@
if($Preview) {
    [PSCustomObject]@{id='ART-G12-54';n=1;Quality='high';Size='720x1072';Background='transparent';input_count=$refs.Count;submitted=$false;output=$run}
    return
}
[void][IO.Directory]::CreateDirectory((Join-Path $run 'inputs'))
$utf8=[Text.UTF8Encoding]::new($false)
function Save-Json($path,$value) {[IO.File]::WriteAllText($path,($value|ConvertTo-Json -Depth 30),$utf8)}
$copied=@()
for($i=0;$i -lt $refs.Count;$i++) {
    $dest=Join-Path $run ('inputs/ref'+($i+1)+'_'+[IO.Path]::GetFileName($refs[$i]))
    Copy-Item -LiteralPath $refs[$i] -Destination $dest -ErrorAction Stop
    $copied+=$dest
}
$promptFile=Join-Path $run 'prompt_api.txt'
[IO.File]::WriteAllText($promptFile,$prompt,$utf8)
$requirements=Join-Path $base 'GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261102_v03.json'
$prepared=@{id='ART-G12-54';operation_kind='first_API_whole_source_visible_character_redraw';InputImages=$copied;PromptFile=$promptFile;OutputDirectory=$run;OutputFileName='character_api_original.png';Quality='high';Size='720x1072';Background='transparent';n=1;automatic_retries=0;endpoint='https://api.openai.com/v1/images/edits';reference_sha256=@($copied|ForEach-Object{(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()});requirements=$requirements;requirements_sha256=(Get-FileHash -LiteralPath $requirements -Algorithm SHA256).Hash.ToLowerInvariant();source_frame=1054;first_case_frames=@(1053,1057);motion_frame=177;prior_53_rejected_image_not_a_reference=$true;user_accepted=$false;dynamic_validated=$false}
Save-Json (Join-Path $run 'API_PREPARED_REQUEST.json') $prepared
Save-Json (Join-Path $run 'REGISTRATION_PLAN.json') @{note='Only original guide uniform crop mapping; generated image alignment still requires actual registration review.';guide_dimensions=@(720,1072);source_to_guide_scale=0.9642384105960264;source_to_guide_translation=@(-362.69668874172186,15.311258278145715);actual_output_alignment_verified=$false}
Save-Json (Join-Path $run 'ROOT_RELEASE.json') @{id='ART-G12-54';released_utc=[DateTime]::UtcNow.ToString('o');latest_user_instruction='按照要求，并行把缺的绘制帧补齐，注意钻发形态和大小2';scope='One first API high image; root reserves one global request slot, separate artist uses other slot for17.';actually_viewed='All six selected reference pixels including unmasked whole-head context; original1054, first1053, last1057, full AI R177, source guide; source and hair authority distinguished.';previous_53_status='Actually reviewed and rejected; no image or bad-root template copied. Adjacent trajectory validation remains pending after repair.';art_acceptance=$false;api_calls_authorized=1;retries_authorized=0;quota_reset_permitted=$false;consent_evidence=(Join-Path $base 'API_PROJECT_SCOPE_AUTHORIZATION_20261101.json')}
& (Join-Path $PSScriptRoot 'Invoke-ReferenceImage.ps1') -PromptFile $promptFile -InputImages $copied -OutputDirectory $run -Quality high -Size 720x1072 -Background transparent -OutputFileName character_api_original.png -Stage 'first_API_source1054_correct11_volume_upper_returns_user_parallel_20261102'
