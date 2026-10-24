# Coordinator tick: one scheduled check instead of a long-lived coordinator
# session (Andrew, 2026-10-24). Run every 10 min by the scheduled task from
# scripts/ops/install_coordinator_tick.ps1.
#
# Each tick:
#   1. takes the lock in the tick folder (two ticks never overlap)
#   2. git fetch origin in the main checkout
#   3. hashes `git ls-remote origin` (sorted) and compares with the hash kept
#      from the last full pass
#   4. unchanged and less than FullEveryMin since the last full pass: logs one
#      line and exits, no Claude call
#   5. otherwise runs one headless coordinator pass (claude -p) from the main
#      checkout, stopped after TimeoutMin
# The tick never runs tracker or server jobs and never starts sessions.
#
# Tick folder: <OPS_DIR>\coordinator_tick (OPS_DIR from private/backup.conf).
# It holds tick.log, state.json, tick.lock, prompt.txt and the last pass output.
#
# Usage (PowerShell):  powershell -File scripts/ops/coordinator_tick.ps1 [-Repo DIR] [-Conf FILE] [-Force]
#   -Repo   main checkout. Default: the main folder of the repo this script is in
#   -Conf   default: private/backup.conf of -Repo
#   -Force  run a full pass even if no ref changed
#   -TickDir, -Git, -Claude: overrides (tests)
param(
    [string]$Repo = "",
    [string]$Conf = "",
    [string]$TickDir = "",
    [string]$Git = "git",
    [string]$Claude = "",
    [int]$FullEveryMin = 60,
    [int]$TimeoutMin = 20,
    [switch]$Force
)
$ErrorActionPreference = "Stop"

$prompt = @'
You are the coordinator session for exactly one check, started by the scheduled
coordinator tick (scripts/ops/coordinator_tick.ps1). There is no live
coordinator loop.
- Do one check as the session named coordinator, per docs/agents/README.md
  (On check github), and every standing item in docs/agents/inbox/coordinator.md
  on origin/main. Work in this checkout, on main.
- Do not start a loop. Do not start, restart or stop any session. Do not run
  tracker jobs or lab-server jobs; reading done markers is allowed.
- Pings (items 8, 10, 16): if you have a tool that messages other local
  sessions, send `check github` to each session to ping, nothing else.
  If not, list the names under Needs Andrew.
- Update and push docs/agents/status/coordinator.md, then exit.
- The last line of your reply is exactly:
  PINGED: <names or none>; TO PING: <names or none>
'@

if (-not $Repo) {
    $here = Split-Path -Parent $MyInvocation.MyCommand.Path
    $common = (& $Git -C $here rev-parse --path-format=absolute --git-common-dir).Trim()
    $Repo = Split-Path -Parent $common
}
if (-not $Conf) { $Conf = Join-Path $Repo "private\backup.conf" }
$c = @{}
if (Test-Path $Conf) {
    foreach ($line in Get-Content $Conf) {
        if ($line -match '^\s*([A-Z_]+)=(.*)$') { $c[$Matches[1]] = $Matches[2].Trim('"') }
    }
}
if (-not $TickDir) {
    if (-not $c.OPS_DIR) { throw "OPS_DIR not set in $Conf" }
    $TickDir = Join-Path $c.OPS_DIR "coordinator_tick"
}
New-Item -ItemType Directory -Force $TickDir | Out-Null
$log = Join-Path $TickDir "tick.log"
$lock = Join-Path $TickDir "tick.lock"
$stateFile = Join-Path $TickDir "state.json"

function Log([string]$msg) {
    Add-Content -Path $log -Encoding utf8 -Value ("{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg)
}

function RefsHash([string[]]$lines) {
    $arr = @($lines | Where-Object { $_ -and $_.Trim() } | ForEach-Object { $_.Trim() })
    [Array]::Sort($arr, [StringComparer]::Ordinal)
    $bytes = [Text.Encoding]::UTF8.GetBytes(($arr -join "`n"))
    $sha = [Security.Cryptography.SHA256]::Create()
    -join ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") })
}

function RemoteRefs {
    $out = & $Git -C $Repo ls-remote origin
    if ($LASTEXITCODE -ne 0) { throw "git ls-remote failed ($LASTEXITCODE)" }
    RefsHash @($out)
}

# Lock: "<pid> <process start ticks>". A lock whose process is gone is stale
# (VM restart, killed tick) and is taken over; a live one makes this tick exit.
$me = Get-Process -Id $PID
$mine = "{0} {1}" -f $PID, $me.StartTime.Ticks
if (Test-Path $lock) {
    $held = (Get-Content $lock -Raw).Trim() -split ' '
    $p = Get-Process -Id ([int]$held[0]) -ErrorAction SilentlyContinue
    if ($p -and $p.StartTime.Ticks -eq [long]$held[1]) {
        Log "skip: previous tick still running (pid $($held[0]))"
        exit 0
    }
    Log "stale lock from pid $($held[0]), taken over"
}
Set-Content -Path $lock -Value $mine -Encoding ascii

try {
    & $Git -C $Repo fetch -q origin
    if ($LASTEXITCODE -ne 0) { throw "git fetch failed ($LASTEXITCODE)" }
    $mainSeen = (& $Git -C $Repo rev-parse origin/main | Select-Object -First 1).Trim()
    $hash = RemoteRefs

    $state = @{ refs_hash = ""; last_full = 0 }
    if (Test-Path $stateFile) {
        $s = Get-Content $stateFile -Raw | ConvertFrom-Json
        $state.refs_hash = [string]$s.refs_hash
        $state.last_full = [long]$s.last_full
    }
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $ageMin = [math]::Floor(($now - $state.last_full) / 60)
    $changed = $hash -ne $state.refs_hash

    if (-not $Force -and -not $changed -and $ageMin -lt $FullEveryMin) {
        Log "skip: refs unchanged, main=$($mainSeen.Substring(0, [math]::Min(10, $mainSeen.Length))), last full pass $ageMin min ago"
        exit 0
    }

    # Headless pass
    if (-not $Claude) { $Claude = $c.CLAUDE }
    if (-not $Claude) { $Claude = (Get-Command claude -ErrorAction Stop).Source }
    # The pass runs git hooks and pytest: put the agents env and bash first on PATH
    $extra = @((Split-Path -Parent $Claude))
    if ($c.CONDA -and $c.ENVS) {
        $envDir = Join-Path (Split-Path -Parent (Split-Path -Parent $c.CONDA)) ("envs\" + ($c.ENVS -split ' ')[0])
        $extra += $envDir, (Join-Path $envDir "Scripts"), (Join-Path $envDir "Library\bin")
    }
    if ($c.BASH) { $extra += (Split-Path -Parent $c.BASH) }
    $env:PATH = (($extra | Where-Object { Test-Path $_ }) + $env:PATH) -join ';'

    $promptFile = Join-Path $TickDir "prompt.txt"
    $outFile = Join-Path $TickDir "last_pass.json"
    $errFile = Join-Path $TickDir "last_pass.err"
    Set-Content -Path $promptFile -Value $prompt -Encoding utf8
    $why = if ($Force) { "forced" } elseif ($changed) { "refs changed" } else { "last full pass $ageMin min ago" }
    Log "start: full pass ($why)"
    Log "commit: main=$mainSeen"
    $t0 = Get-Date
    $proc = Start-Process -FilePath $Claude -ArgumentList @("-p", "--permission-mode", "auto", "--output-format", "json") `
        -WorkingDirectory $Repo -RedirectStandardInput $promptFile -RedirectStandardOutput $outFile `
        -RedirectStandardError $errFile -NoNewWindow -PassThru
    $null = $proc.Handle        # keeps ExitCode readable after exit (PowerShell 5.1)
    if (-not $proc.WaitForExit($TimeoutMin * 60 * 1000)) {
        & taskkill.exe /PID $proc.Id /T /F | Out-Null
        $code = "timeout"
        Log "stopped: pass ran longer than $TimeoutMin min"
    } else {
        $code = $proc.ExitCode
    }
    $secs = [math]::Round(((Get-Date) - $t0).TotalSeconds)

    $tokens = "tokens=?"
    $pings = "pings: ?"
    try {
        $r = Get-Content $outFile -Raw | ConvertFrom-Json
        $u = $r.usage
        $tokens = "tokens in=$($u.input_tokens) out=$($u.output_tokens) cache_read=$($u.cache_read_input_tokens) cache_write=$($u.cache_creation_input_tokens) cost_usd=$($r.total_cost_usd) turns=$($r.num_turns)"
        $last = ([string]$r.result).Trim() -split "`n" | Where-Object { $_ -match '^\s*PINGED:' } | Select-Object -Last 1
        if ($last) { $pings = "pings: " + $last.Trim() }
    } catch { }
    Log "exit: $code"
    Log "end: $secs s, $tokens"
    Log $pings

    # Hash after the pass, so the pass's own status push does not trigger the next tick
    & $Git -C $Repo fetch -q origin
    $state.refs_hash = RemoteRefs
    $state.last_full = $now
    $state | ConvertTo-Json | Set-Content -Path $stateFile -Encoding utf8
    if ($code -ne 0) { exit 1 }
} catch {
    Log "error: $($_.Exception.Message)"
    exit 1
} finally {
    if ((Test-Path $lock) -and ((Get-Content $lock -Raw).Trim() -eq $mine)) { Remove-Item $lock }
}
