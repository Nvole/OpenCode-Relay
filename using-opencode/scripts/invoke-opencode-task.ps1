[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Manifest,
    [switch]$DryRun,
    [switch]$Restart
)

$ErrorActionPreference = 'Stop'
$python = Get-Command python -ErrorAction Stop
$script = Join-Path $PSScriptRoot 'router.py'
$arguments = @($script, '--manifest', (Resolve-Path -LiteralPath $Manifest).Path)
if ($DryRun) { $arguments += '--dry-run' }
if ($Restart) { $arguments += '--restart' }
& $python.Source @arguments
if ($LASTEXITCODE -ne 0) { throw "OpenCode router exited with code $LASTEXITCODE" }
