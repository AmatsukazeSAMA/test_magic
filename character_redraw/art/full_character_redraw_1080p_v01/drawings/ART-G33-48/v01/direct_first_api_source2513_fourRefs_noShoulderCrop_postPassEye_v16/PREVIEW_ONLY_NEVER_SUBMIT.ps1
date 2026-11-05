$ErrorActionPreference='Stop'
$prepRequest = Get-Content -LiteralPath 'D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16/DIRECT_REQUEST.json' -Raw | ConvertFrom-Json -AsHashtable
$dryArgs = $prepRequest.parameters
$previewResult = & $prepRequest.provider.path @dryArgs -Preview
if ($previewResult.submitted -ne $false) { throw 'Preview unexpectedly submitted.' }
$previewJson = $previewResult | ConvertTo-Json -Depth 12
[IO.File]::WriteAllText('D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01/drawings/ART-G33-48/v01/direct_first_api_source2513_fourRefs_noShoulderCrop_postPassEye_v16/DIRECT_PREVIEW.json', $previewJson + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
$previewJson

