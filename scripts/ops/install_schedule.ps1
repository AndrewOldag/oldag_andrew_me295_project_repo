# Install the VM heartbeat (every 5 min) and the nightly backup (02:10) as
# Windows scheduled tasks. Copies scripts/ops to OPS_DIR first, so the tasks
# do not depend on which branch or worktree is checked out. Re-run after any
# change to scripts/ops.
#
# Usage (PowerShell):  powershell -File scripts/ops/install_schedule.ps1 [-Conf FILE] [-S4U] [-Remove]
#   -Conf   default: private/backup.conf of the main repo folder
#   -S4U    run whether or not the user is logged on (needs an elevated shell).
#           Default: run only while the user is logged on (a disconnected
#           session counts as logged on)
#   -Remove unregister both tasks
param([string]$Conf = "", [switch]$S4U, [switch]$Remove)
$ErrorActionPreference = "Stop"
$names = @("me295-heartbeat", "me295-backup")

if ($Remove) {
    foreach ($n in $names) { Unregister-ScheduledTask -TaskName $n -Confirm:$false -ErrorAction SilentlyContinue }
    "removed: $($names -join ', ')"
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
foreach ($k in "OPS_DIR", "HEARTBEAT_LOG", "BACKUP_LOG", "BASH") {
    if (-not $c[$k]) { throw "$k not set in $Conf" }
}
if (-not (Test-Path $c.BASH)) { throw "BASH not found" }

New-Item -ItemType Directory -Force $c.OPS_DIR | Out-Null
foreach ($f in "heartbeat.sh", "backup_vm.sh", "hidden.vbs") { Copy-Item (Join-Path $here $f) $c.OPS_DIR -Force }
$ops = (Resolve-Path $c.OPS_DIR).Path
$vbs = Join-Path $ops "hidden.vbs"
$confFull = (Resolve-Path $Conf).Path

$user = "$env:USERDOMAIN\$env:USERNAME"
$logon = if ($S4U) { "S4U" } else { "Interactive" }
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType $logon -RunLevel Limited

function Q([string]$s) { '"' + $s + '"' }

# Heartbeat: every 5 min, indefinitely
$a1 = New-ScheduledTaskAction -Execute "wscript.exe" -Argument ("//B //Nologo " + (Q $vbs) + " " + (Q $c.BASH) + " " + (Q (Join-Path $ops "heartbeat.sh")) + " " + (Q $c.HEARTBEAT_LOG))
$t1 = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddMinutes([math]::Ceiling((Get-Date).TimeOfDay.TotalMinutes / 5) * 5) -RepetitionInterval (New-TimeSpan -Minutes 5)
$s1 = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $names[0] -Action $a1 -Trigger $t1 -Settings $s1 -Principal $principal -Force | Out-Null

# Backup: daily at 02:10; a missed run starts when the VM is next up
$a2 = New-ScheduledTaskAction -Execute "wscript.exe" -Argument ("//B //Nologo " + (Q $vbs) + " " + (Q $c.BASH) + " " + (Q (Join-Path $ops "backup_vm.sh")) + " --conf " + (Q $confFull) + " --log " + (Q $c.BACKUP_LOG) + " run")
$t2 = New-ScheduledTaskTrigger -Daily -At "02:10"
$s2 = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 3) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $names[1] -Action $a2 -Trigger $t2 -Settings $s2 -Principal $principal -Force | Out-Null

Get-ScheduledTask -TaskName $names | ForEach-Object {
    $i = $_ | Get-ScheduledTaskInfo
    "{0}: {1}, logon {2}, next run {3}" -f $_.TaskName, $_.State, $logon, $i.NextRunTime
}
