# Install the VM heartbeat (every 5 min) as a Windows scheduled task. Copies
# heartbeat.sh and hidden.vbs to OPS_DIR first, so the task does not depend on
# which branch or worktree is checked out. Re-run after any change to them.
# There is no scheduled backup (Andrew, 2026-10-16); scripts/ops/backup_vm.sh
# is run by hand only.
#
# Usage (PowerShell):  powershell -File scripts/ops/install_schedule.ps1 [-Conf FILE] [-S4U] [-Remove]
#   -Conf   default: private/backup.conf of the main repo folder
#   -S4U    run whether or not the user is logged on (needs an elevated shell).
#           Default: run only while the user is logged on (a disconnected
#           session counts as logged on)
#   -Remove unregister the heartbeat (and a leftover me295-backup task, if any)
param([string]$Conf = "", [switch]$S4U, [switch]$Remove)
$ErrorActionPreference = "Stop"
$name = "me295-heartbeat"

if ($Remove) {
    foreach ($n in $name, "me295-backup") { Unregister-ScheduledTask -TaskName $n -Confirm:$false -ErrorAction SilentlyContinue }
    "removed: $name"
    exit 0
}

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Conf) {
    $common = (& git -C $here rev-parse --path-format=absolute --git-common-dir).Trim()
    $Conf = Join-Path (Split-Path -Parent $common) "private\backup.conf"
}
if (-not (Test-Path $Conf)) { throw "conf not found: $Conf" }
$c = @{}
foreach ($line in Get-Content $Conf) {
    if ($line -match '^\s*([A-Z_]+)=(.*)$') { $c[$Matches[1]] = $Matches[2].Trim('"') }
}
foreach ($k in "OPS_DIR", "HEARTBEAT_LOG", "BASH") {
    if (-not $c[$k]) { throw "$k not set in $Conf" }
}
if (-not (Test-Path $c.BASH)) { throw "BASH not found" }

New-Item -ItemType Directory -Force $c.OPS_DIR | Out-Null
foreach ($f in "heartbeat.sh", "hidden.vbs") { Copy-Item (Join-Path $here $f) $c.OPS_DIR -Force }
$ops = (Resolve-Path $c.OPS_DIR).Path
$vbs = Join-Path $ops "hidden.vbs"

$user = "$env:USERDOMAIN\$env:USERNAME"
$logon = if ($S4U) { "S4U" } else { "Interactive" }
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType $logon -RunLevel Limited

function Q([string]$s) { '"' + $s + '"' }

# Heartbeat: every 5 min, indefinitely
$a = New-ScheduledTaskAction -Execute "wscript.exe" -Argument ("//B //Nologo " + (Q $vbs) + " " + (Q $c.BASH) + " " + (Q (Join-Path $ops "heartbeat.sh")) + " " + (Q $c.HEARTBEAT_LOG))
$t = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddMinutes([math]::Ceiling((Get-Date).TimeOfDay.TotalMinutes / 5) * 5) -RepetitionInterval (New-TimeSpan -Minutes 5)
$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $name -Action $a -Trigger $t -Settings $s -Principal $principal -Force | Out-Null

$i = Get-ScheduledTaskInfo -TaskName $name
"{0}: {1}, logon {2}, next run {3}" -f $name, (Get-ScheduledTask -TaskName $name).State, $logon, $i.NextRunTime
