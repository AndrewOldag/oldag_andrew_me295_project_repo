# Install the coordinator tick (every 10 min) as a Windows scheduled task.
# Copies coordinator_tick.ps1 and hidden.vbs to OPS_DIR first, so the task does
# not depend on which branch or worktree is checked out. Re-run after any
# change to them. Needs an elevated shell (S4U: runs whether or not the user
# is logged on). Andrew runs it; sessions do not.
#
# Usage (PowerShell, elevated):  powershell -File scripts/ops/install_coordinator_tick.ps1 [-Conf FILE] [-Remove]
#   -Conf   default: private/backup.conf of the main repo folder
#   -Remove unregister the task
# Check:  Get-ScheduledTask me295-coordinator-tick | Get-ScheduledTaskInfo
param([string]$Conf = "", [switch]$Remove)
$ErrorActionPreference = "Stop"
$name = "me295-coordinator-tick"

if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
    "removed: $name"
    exit 0
}

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$common = (& git -C $here rev-parse --path-format=absolute --git-common-dir).Trim()
$repo = Split-Path -Parent $common
if (-not $Conf) { $Conf = Join-Path $repo "private\backup.conf" }
if (-not (Test-Path $Conf)) { throw "conf not found: $Conf" }
$c = @{}
foreach ($line in Get-Content $Conf) {
    if ($line -match '^\s*([A-Z_]+)=(.*)$') { $c[$Matches[1]] = $Matches[2].Trim('"') }
}
if (-not $c.OPS_DIR) { throw "OPS_DIR not set in $Conf" }
$claude = if ($c.CLAUDE) { $c.CLAUDE } else { (Get-Command claude -ErrorAction Stop).Source }

New-Item -ItemType Directory -Force $c.OPS_DIR | Out-Null
foreach ($f in "coordinator_tick.ps1", "hidden.vbs") { Copy-Item (Join-Path $here $f) $c.OPS_DIR -Force }
$ops = (Resolve-Path $c.OPS_DIR).Path

function Q([string]$s) { '"' + $s + '"' }

$user = "$env:USERDOMAIN\$env:USERNAME"
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType S4U -RunLevel Limited
$ps = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$arg = "//B //Nologo " + (Q (Join-Path $ops "hidden.vbs")) + " " + (Q $ps) + " -NoProfile -ExecutionPolicy Bypass -File " +
    (Q (Join-Path $ops "coordinator_tick.ps1")) + " -Repo " + (Q $repo) + " -Conf " + (Q (Resolve-Path $Conf).Path) + " -Claude " + (Q $claude)
$a = New-ScheduledTaskAction -Execute "wscript.exe" -Argument $arg
$t = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddMinutes([math]::Ceiling((Get-Date).TimeOfDay.TotalMinutes / 10) * 10) -RepetitionInterval (New-TimeSpan -Minutes 10)
# The tick stops its own pass at 20 min; the task limit is a backstop
$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $name -Action $a -Trigger $t -Settings $s -Principal $principal -Force | Out-Null

$i = Get-ScheduledTaskInfo -TaskName $name
"{0}: {1}, logon S4U, next run {2}" -f $name, (Get-ScheduledTask -TaskName $name).State, $i.NextRunTime
"tick log: " + (Join-Path $ops "coordinator_tick\tick.log")
