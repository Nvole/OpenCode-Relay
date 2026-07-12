[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Manifest,
    [switch]$DryRun,
    [switch]$Restart,
    [switch]$ValidateThenRun
)

$ErrorActionPreference = 'Stop'
$python = Get-Command python -ErrorAction Stop
$script = Join-Path $PSScriptRoot 'router.py'
$manifestPath = (Resolve-Path -LiteralPath $Manifest).Path
if ($ValidateThenRun) {
    & $python.Source $script '--manifest' $manifestPath '--dry-run' '--restart'
    if ($LASTEXITCODE -ne 0) { throw "OpenCode Router dry-run exited with code $LASTEXITCODE" }
    & $python.Source $script '--manifest' $manifestPath '--restart'
    if ($LASTEXITCODE -ne 0) { throw "OpenCode Router live run exited with code $LASTEXITCODE" }
    return
}
$arguments = @($script, '--manifest', $manifestPath)
if ($DryRun) { $arguments += '--dry-run' }
if ($Restart) { $arguments += '--restart' }
& $python.Source @arguments
if ($LASTEXITCODE -ne 0) { throw "OpenCode router exited with code $LASTEXITCODE" }
