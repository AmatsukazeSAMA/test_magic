#Requires -Version 7.0
[CmdletBinding()]
param([switch]$Preview)
$ErrorActionPreference='Stop'
& 'D:\CODEX\魔术之心\scripts\Invoke-ReviewedMissingFirst.ps1' -Run $PSScriptRoot -Preview:$Preview
