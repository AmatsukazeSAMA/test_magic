#Requires -Version 7.0
$ErrorActionPreference='Stop'
$configPath='D:\CODEX\OPENAI\api\connection.json'
$usagePath='D:\CODEX\OPENAI\API_USAGE.md'
$config=[IO.File]::ReadAllText($configPath) | ConvertFrom-Json
$before=$config.defaults.quality
$config.defaults.quality='high'
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText($configPath,($config | ConvertTo-Json -Depth 10)+[Environment]::NewLine,$utf8)
$usage=[IO.File]::ReadAllText($usagePath)
$usage=$usage.Replace('默认质量为 `max`','默认质量为 `high`')
[IO.File]::WriteAllText($usagePath,$usage,$utf8)
$notes='C:\Users\11515\.codex\memories_v2\extensions\ad_hoc\notes'
[void][IO.Directory]::CreateDirectory($notes)
$notePath=Join-Path $notes '2026-10-30-api-image-quality-high.md'
$note=@'
# 2026-10-30：API 绘画默认 high

用户在《魔术之心》PV 人物三视图任务中明确要求：“使用API完成绘画，强度为high，以后默认为high强度”。今后使用用户已配置的图像 API 绘画时，默认请求 quality=high；用户另有指定时遵从最新指定。该要求适用于 API 图像输出质量，不推定为所有工具的其他“强度”参数。

本机共享接入 D:\CODEX\OPENAI\api\connection.json 的 defaults.quality 已按该明确要求设置为 high。生成三视图后，须等用户认可三视图，再尝试一张原 PV 重绘描改。
'@
if(-not (Test-Path -LiteralPath $notePath)) { [IO.File]::WriteAllText($notePath,$note+[Environment]::NewLine,$utf8) }
[PSCustomObject]@{previous_quality=$before;default_quality=$config.defaults.quality;config=$configPath;memory_note=$notePath}
