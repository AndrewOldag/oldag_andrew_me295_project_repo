# VM supervisor (spec 2026-11-22, task c032). No LLM: it only watches and starts.
# One long-running hidden process, started at logon by install_supervisor.ps1.
#
# Each tick (every IntervalMin):
#   1. git fetch origin in the main checkout
#   2. for each course session: running? (pid file from agents.ps1, process alive, name claude)
#      pending? inbox last item on origin/main > `Last inbox item done` in its newest status
#      (newest `Updated:` over all origin branches), or `State: working` with `Updated:`
#      older than StaleHours and no live process
#   3. starts at most one session that is not running and has pending work, with
#      `agents.ps1 -Names <name> -Fresh`; GapSec since the last start, and the same
#      session not again within RestartMin of its last start by the supervisor
#   4. free memory under MinFreeGB: starts nothing
#   5. reports dead entries of the detached registry (detached.json); never restarts them
#   6. heartbeat: one line appended to docs/agents/status/supervisor.md on branch
#      ops/heartbeat (git plumbing with a temporary index; no checkout is touched), last
#      KeepLines lines kept, pushed
# It never deletes data, never stops a process, never touches the cluster or the lab server.
# A second supervisor exits at once (lock file with pid and process start time).
#
# Files in StateDir (default %USERPROFILE%\claude_agents): supervisor.lock, supervisor.log,
# supervisor_state.json, detached.json, <name>.pid (written by agents.ps1).
#
# Usage (PowerShell):  powershell -File scripts/ops/supervisor.ps1 [-Repo DIR] [-Once]
#   -Repo   main checkout. Default: the main folder of the repo this script is in
#   -Once   one tick, then exit
#   -Now, -ProcTable, -FreeGB, -Git, -Agents, -NoPush: overrides (tests)
#     -Now: UTC time, ISO 8601. -ProcTable: JSON {"<pid>": {"name": "...", "start": <ticks>}}
param(
    [string]$Repo = "",
    [string]$StateDir = "",
    [string[]]$Names = @('dispatcher', 'real-calib', 'compound'),
    [int]$IntervalMin = 10,
    [int]$GapSec = 60,
    [int]$RestartMin = 60,
    [double]$StaleHours = 2,
    [double]$MinFreeGB = 3,
    [int]$KeepLines = 48,
    [string]$StatusTz = "Pacific Standard Time",
    [string]$Branch = "ops/heartbeat",
    [string]$Git = "git",
    [string]$Agents = "",
    [string]$Now = "",
    [string]$ProcTable = "",
    [double]$FreeGB = -1,
    [switch]$NoPush,
    [switch]$Once
)
$ErrorActionPreference = "Stop"
$Names = @($Names | ForEach-Object { $_ -split ',' } | Where-Object { $_ })   # -File passes "a,b" as one string
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Repo) {
    $common = (& $Git -C $here rev-parse --path-format=absolute --git-common-dir).Trim()
    $Repo = Split-Path -Parent $common
}
if (-not $StateDir) { $StateDir = Join-Path $env:USERPROFILE "claude_agents" }
if (-not $Agents) { $Agents = Join-Path $Repo "scripts\ops\agents.ps1" }
New-Item -ItemType Directory -Force $StateDir | Out-Null
$log = Join-Path $StateDir "supervisor.log"
$lock = Join-Path $StateDir "supervisor.lock"
$stateFile = Join-Path $StateDir "supervisor_state.json"
$registry = Join-Path $StateDir "detached.json"
$hbPath = "docs/agents/status/supervisor.md"

function NowUtc {
    if ($Now) { return [DateTime]::Parse($Now, [Globalization.CultureInfo]::InvariantCulture,
                                         [Globalization.DateTimeStyles]::AdjustToUniversal -bor [Globalization.DateTimeStyles]::AssumeUniversal) }
    return [DateTime]::UtcNow
}
function NowLocal { [TimeZoneInfo]::ConvertTimeFromUtc((NowUtc), [TimeZoneInfo]::FindSystemTimeZoneById($StatusTz)) }

function Log([string]$msg) {
    Add-Content -Path $log -Encoding utf8 -Value ("{0} {1}" -f (NowLocal).ToString("yyyy-MM-dd HH:mm:ss"), $msg)
}

# git in the main checkout; stderr dropped, exit code in $script:gitCode
function G {
    $ErrorActionPreference = "Continue"
    $out = & $Git -C $Repo @args 2>$null
    $script:gitCode = $LASTEXITCODE
    return $out
}

# Process table: pid -> @{ name; start } (start = StartTime.Ticks)
function Proc([int]$id) {
    if ($ProcTable) {
        $t = Get-Content $ProcTable -Raw | ConvertFrom-Json
        $e = $t.PSObject.Properties["$id"]
        if (-not $e) { return $null }
        return @{ name = [string]$e.Value.name; start = [long]$e.Value.start }
    }
    $p = Get-Process -Id $id -ErrorAction SilentlyContinue
    if (-not $p) { return $null }
    $start = 0L
    try { $start = $p.StartTime.Ticks } catch { }
    return @{ name = $p.ProcessName; start = $start }
}

function FreeMemGB {
    if ($FreeGB -ge 0) { return $FreeGB }
    return (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
}

function Running([string]$n) {
    $pidFile = Join-Path $StateDir "$n.pid"
    if (-not (Test-Path $pidFile)) { return $false }
    $id = 0
    if (-not [int]::TryParse((Get-Content $pidFile -Raw).Trim(), [ref]$id)) { return $false }
    $p = Proc $id
    return [bool]($p -and $p.name -eq "claude")
}

function InboxLast([string]$n) {
    $text = G show "origin/main:docs/agents/inbox/$n.md"
    $last = 0
    foreach ($ln in @($text)) { if ($ln -match '^(\d+)\.\s') { $last = [math]::Max($last, [int]$Matches[1]) } }
    return $last
}

# Newest status of a session over all origin branches: @{ done; state; updated; ref } or $null
function Status([string]$n) {
    $best = $null
    foreach ($ref in @(G for-each-ref '--format=%(refname:short)' refs/remotes/origin)) {
        if (-not $ref -or $ref -eq "origin/HEAD" -or $ref -eq "origin") { continue }
        $text = @(G show "${ref}:docs/agents/status/$n.md")
        if ($script:gitCode -ne 0 -or -not $text) { continue }
        $s = @{ done = 0; state = ""; updated = [DateTime]::MinValue; ref = $ref }
        foreach ($ln in $text) {
            if ($ln -match '^Last inbox item done:\s*(\d+)') { $s.done = [int]$Matches[1] }
            elseif ($ln -match '^State:\s*(.+?)\s*$') { $s.state = $Matches[1] }
            elseif ($ln -match '^Updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})') {
                $s.updated = [DateTime]::ParseExact($Matches[1], "yyyy-MM-dd HH:mm", [Globalization.CultureInfo]::InvariantCulture)
            }
        }
        if (-not $best -or $s.updated -gt $best.updated) { $best = $s }
    }
    return $best
}

# "inbox" | "stale" | ""
function Pending([string]$n) {
    $s = Status $n
    $done = if ($s) { $s.done } else { 0 }
    if ((InboxLast $n) -gt $done) { return "inbox" }
    if ($s -and $s.state -match '^working' -and ((NowLocal) - $s.updated).TotalHours -ge $StaleHours) { return "stale" }
    return ""
}

function DeadDetached {
    if (-not (Test-Path $registry)) { return @() }
    $dead = @()
    # PowerShell 5.1 emits a JSON array as one object: assign first, then enumerate
    try { $parsed = Get-Content $registry -Raw | ConvertFrom-Json; $entries = @($parsed | ForEach-Object { $_ }) } catch { return @("registry unreadable") }
    foreach ($e in $entries) {
        if (-not $e) { continue }
        $p = Proc ([int]$e.pid)
        $alive = $p -and (-not $e.start_ticks -or [long]$e.start_ticks -eq $p.start)
        if (-not $alive) { $dead += "$($e.name)($($e.pid))" }
    }
    return $dead
}

function LoadState {
    $st = @{ last_start = ""; starts = @{} }
    if (Test-Path $stateFile) {
        $j = Get-Content $stateFile -Raw | ConvertFrom-Json
        $st.last_start = [string]$j.last_start
        if ($j.starts) { foreach ($p in $j.starts.PSObject.Properties) { $st.starts[$p.Name] = [string]$p.Value } }
    }
    return $st
}

# Append one line to the heartbeat file on $Branch and push. No working tree or index of
# the checkout is used: a temporary index file, then commit-tree and push of the commit.
function Heartbeat([string]$line) {
    $parent = @(G rev-parse --verify -q "refs/remotes/origin/$Branch")[0]
    $old = @()
    if ($parent) { $old = @(G show "${parent}:$hbPath") | Where-Object { $_ -match '^\d{4}-' } }
    $lines = @($old) + $line
    if ($lines.Count -gt $KeepLines) { $lines = $lines[($lines.Count - $KeepLines)..($lines.Count - 1)] }
    $body = @("# supervisor", "Heartbeat of scripts/ops/supervisor.ps1, one line per tick, last $KeepLines lines. Times local.", "") + $lines
    $tmp = Join-Path $StateDir "heartbeat.tmp"
    $idx = Join-Path $StateDir "heartbeat.index"
    [IO.File]::WriteAllText($tmp, (($body -join "`n") + "`n"), (New-Object Text.UTF8Encoding $false))
    $blob = @(G hash-object -w $tmp)[0]
    $env:GIT_INDEX_FILE = $idx
    try {
        if ($parent) { G read-tree $parent | Out-Null } else { G read-tree --empty | Out-Null }
        G update-index --add --cacheinfo "100644,$blob,$hbPath" | Out-Null
        $tree = @(G write-tree)[0]
    } finally { Remove-Item Env:GIT_INDEX_FILE }
    $cargs = @("commit-tree", $tree, "-m", "supervisor heartbeat $($line.Substring(0, 16))")
    if ($parent) { $cargs += @("-p", $parent) }
    $commit = @(G @cargs)[0]
    if ($script:gitCode -ne 0 -or -not $commit) { return "commit failed" }
    if ($NoPush) { G update-ref "refs/remotes/origin/$Branch" $commit | Out-Null; return "not pushed" }
    G push -q origin "${commit}:refs/heads/$Branch" | Out-Null
    if ($script:gitCode -ne 0) { return "push failed" }
    return "pushed"
}

function Tick {
    $notes = @()
    G fetch -q origin | Out-Null
    if ($script:gitCode -ne 0) { $notes += "fetch failed"; Log "fetch failed ($script:gitCode)" }
    $free = FreeMemGB
    $st = LoadState
    $nowL = NowLocal
    $parts = @()
    $candidates = @()
    foreach ($n in $Names) {
        if (Running $n) { $parts += "$n=running"; continue }
        $why = Pending $n
        if ($why) { $parts += "$n=exited,pending:$why"; $candidates += $n } else { $parts += "$n=exited" }
    }

    $started = "none"
    if ($candidates.Count -gt 0) {
        if ($free -lt $MinFreeGB) {
            $started = "none (free memory under $MinFreeGB GB)"
        } elseif ($st.last_start -and ($nowL - [DateTime]::Parse($st.last_start)).TotalSeconds -lt $GapSec) {
            $started = "none (last start under $GapSec s ago)"
        } else {
            # least recently started first; a session started under RestartMin ago waits
            $ready = @($candidates | Where-Object {
                -not $st.starts[$_] -or ($nowL - [DateTime]::Parse($st.starts[$_])).TotalMinutes -ge $RestartMin
            } | Sort-Object @{ Expression = { if ($st.starts[$_]) { [DateTime]::Parse($st.starts[$_]) } else { [DateTime]::MinValue } } },
                            @{ Expression = { [array]::IndexOf($Names, $_) } })
            if ($ready.Count -eq 0) {
                $started = "none (pending sessions started under $RestartMin min ago)"
            } else {
                $n = $ready[0]
                $ps = (Get-Process -Id $PID).Path
                $out = & $ps -NoProfile -ExecutionPolicy Bypass -File $Agents -Names $n -Fresh -GapSec 0 2>&1
                Log "start $n (exit $LASTEXITCODE): $(($out | Out-String).Trim())"
                $started = $n
                $st.last_start = $nowL.ToString("s")
                $st.starts[$n] = $nowL.ToString("s")
                $st | ConvertTo-Json | Set-Content -Path $stateFile -Encoding utf8
            }
        }
    }
    $dead = @(DeadDetached)
    $deadText = if ($dead.Count) { $dead -join "," } else { "none" }
    $line = "{0} free={1:N1}GB {2} start={3} dead={4}" -f $nowL.ToString("yyyy-MM-dd HH:mm"), $free, ($parts -join " "), $started, $deadText
    if ($notes.Count) { $line += " note=" + ($notes -join ",") }
    $pushed = Heartbeat $line
    Log "$line heartbeat=$pushed"
}

# Single instance: "<pid> <process start ticks>"; a lock whose process is gone is stale
$me = Get-Process -Id $PID
$mine = "{0} {1}" -f $PID, $me.StartTime.Ticks
if (Test-Path $lock) {
    $held = (Get-Content $lock -Raw).Trim() -split ' '
    $p = Proc ([int]$held[0])
    if ($p -and $p.start -eq [long]$held[1]) {
        Log "exit: another supervisor is running (pid $($held[0]))"
        exit 0
    }
    Log "stale lock from pid $($held[0]), taken over"
}
Set-Content -Path $lock -Value $mine -Encoding ascii
Log "supervisor started (pid $PID)"
try {
    while ($true) {
        try { Tick } catch { Log "error: $($_.Exception.Message)" }
        if ($Once) { break }
        Start-Sleep -Seconds ($IntervalMin * 60)
    }
} finally {
    if ((Test-Path $lock) -and ((Get-Content $lock -Raw).Trim() -eq $mine)) { Remove-Item $lock }
}
