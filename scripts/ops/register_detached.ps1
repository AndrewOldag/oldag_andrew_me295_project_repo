# Register a detached process in the supervisor's registry (spec 2026-11-22, task c032).
# Sessions call this right after Start-Process of anything that outlives them. The
# supervisor reports dead entries in its heartbeat; it never restarts them.
# One entry per (name, pid); registering the same pair again replaces it.
#
# Usage (PowerShell):
#   $p = Start-Process ... -WindowStyle Hidden -PassThru
#   powershell -File scripts\ops\register_detached.ps1 -Name dispatcher-c027 -ProcessId $p.Id -Command "python scripts/run_all.py ..." -Log <log file>
#   powershell -File scripts\ops\register_detached.ps1 -Name dispatcher-c027 -ProcessId <pid> -Unregister   # own entry, when done
# Registry: %USERPROFILE%\claude_agents\detached.json (-StateDir overrides)
param(
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][int]$ProcessId,
    [string]$Command = "",
    [string]$Log = "",
    [string]$StateDir = "",
    [switch]$Unregister
)
$ErrorActionPreference = "Stop"
if (-not $StateDir) { $StateDir = Join-Path $env:USERPROFILE "claude_agents" }
New-Item -ItemType Directory -Force $StateDir | Out-Null
$registry = Join-Path $StateDir "detached.json"

$entries = @()
if (Test-Path $registry) {
    $raw = Get-Content $registry -Raw
    # PowerShell 5.1 emits a JSON array as one object: assign first, then enumerate
    if ($raw -and $raw.Trim()) { $parsed = $raw | ConvertFrom-Json; $entries = @($parsed | ForEach-Object { $_ }) }
}
$entries = @($entries | Where-Object { $_ -and -not ($_.name -eq $Name -and [int]$_.pid -eq $ProcessId) })

if (-not $Unregister) {
    $p = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
    if (-not $p) { throw "no process with pid $ProcessId" }
    $entries += [pscustomobject]@{
        name        = $Name
        pid         = $ProcessId
        start_ticks = $p.StartTime.Ticks
        command     = $Command
        log         = $Log
        started     = $p.StartTime.ToString("s")
    }
}
$json = if ($entries.Count) { ConvertTo-Json -InputObject @($entries) -Depth 3 } else { "[]" }
[IO.File]::WriteAllText($registry, $json, (New-Object Text.UTF8Encoding $false))
if ($Unregister) { "unregistered $Name ($ProcessId)" } else { "registered $Name ($ProcessId)" }
