# Install the VM supervisor (spec 2026-11-22, task c032) as a logon scheduled task and
# remove the hourly "ME295 agents ping" task it replaces. -Uninstall reverses both.
# Copies supervisor.ps1 and hidden.vbs to OPS_DIR first, so the task does not depend on
# which branch or worktree is checked out; sessions are started with agents.ps1 of the
# main checkout. Re-run after any change to supervisor.ps1. Andrew runs it, on a
# planning inbox item (switch-over); sessions do not.
#
# Usage (PowerShell):  powershell -File scripts/ops/install_supervisor.ps1 [-Conf FILE] [-Uninstall]
#   -Conf   default: private/backup.conf of the main repo folder
# Check:  Get-ScheduledTask me295-supervisor | Get-ScheduledTaskInfo
param([string]$Conf = "", [switch]$Uninstall)
$ErrorActionPreference = "Stop"
$name = "me295-supervisor"
$ping = "ME295 agents ping"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$common = (& git -C $here rev-parse --path-format=absolute --git-common-dir).Trim()
$repo = Split-Path -Parent $common
$agents = Join-Path $repo "scripts\ops\agents.ps1"
$user = "$env:USERDOMAIN\$env:USERNAME"
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited

function Q([string]$s) { '"' + $s + '"' }

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
    # The hourly ping as it was before the switch-over
    $a = New-ScheduledTaskAction -Execute "powershell" -Argument ("-ExecutionPolicy Bypass -WindowStyle Hidden -File " + $agents + " -Fresh")
    $t = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours((Get-Date).Hour + 1) -RepetitionInterval (New-TimeSpan -Hours 1)
    $s = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 72) -MultipleInstances IgnoreNew
    Register-ScheduledTask -TaskName $ping -Action $a -Trigger $t -Settings $s -Principal $principal -Force | Out-Null
    "removed: $name; restored: $ping (hourly)"
    "the running supervisor, if any, stops at logoff or by hand (this script stops no process)"
    exit 0
}

if (-not $Conf) { $Conf = Join-Path $repo "private\backup.conf" }
if (-not (Test-Path $Conf)) { throw "conf not found: $Conf" }
$c = @{}
foreach ($line in Get-Content $Conf) {
    if ($line -match '^\s*([A-Z_]+)=(.*)$') { $c[$Matches[1]] = $Matches[2].Trim('"') }
}
if (-not $c.OPS_DIR) { throw "OPS_DIR not set in $Conf" }

New-Item -ItemType Directory -Force $c.OPS_DIR | Out-Null
foreach ($f in "supervisor.ps1", "hidden.vbs") { Copy-Item (Join-Path $here $f) $c.OPS_DIR -Force }
$ops = (Resolve-Path $c.OPS_DIR).Path

$ps = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$arg = "//B //Nologo " + (Q (Join-Path $ops "hidden.vbs")) + " " + (Q $ps) + " -NoProfile -ExecutionPolicy Bypass -File " +
    (Q (Join-Path $ops "supervisor.ps1")) + " -Repo " + (Q $repo) + " -Agents " + (Q $agents)
$a = New-ScheduledTaskAction -Execute "wscript.exe" -Argument $arg
$t = New-ScheduledTaskTrigger -AtLogOn -User $user
# No time limit: the supervisor runs until logoff; a second copy exits at once on its lock
$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Seconds 0) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $name -Action $a -Trigger $t -Settings $s -Principal $principal -Force | Out-Null
Unregister-ScheduledTask -TaskName $ping -Confirm:$false -ErrorAction SilentlyContinue
"{0}: {1}, at logon; removed: {2}" -f $name, (Get-ScheduledTask -TaskName $name).State, $ping
"start now without logging off: Start-ScheduledTask $name"
