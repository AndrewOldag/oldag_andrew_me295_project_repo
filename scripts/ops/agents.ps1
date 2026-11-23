# Start, ping or list the course-lane Claude sessions as hidden background processes (no console window).
# Andrew, 2026-11-20: interactive windows cost VM memory and the sessions crashed.
#
# Each session runs `claude -p` (headless, auto mode) in its worktree .claude\worktrees\<name>,
# continuing that worktree's last conversation unless -Fresh. It does one `check github` pass, works
# until its items are done or blocked, pushes status and exits. Run the script again to ping it.
# A session that is still running is not started twice.
#
# Usage (PowerShell, from the main checkout):
#   powershell -File scripts\ops\agents.ps1                        # start or ping all three
#   powershell -File scripts\ops\agents.ps1 -Names dispatcher      # one session
#   powershell -File scripts\ops\agents.ps1 -Status                # running or exited, last output time
#   powershell -File scripts\ops\agents.ps1 -StopAll               # stop every Claude Code process
#   -Fresh: new conversation instead of continuing; -GapSec: wait between starts (default 60)
#   -Model: model for this start (overrides the per-session default; audit defaults to claude-fable-5-2)
# Names must be known sessions (comma lists are split). A known session with no worktree gets one
# (.claude\worktrees\<name> on wip/<name> from origin/main); the main checkout is never used.
# Logs: %USERPROFILE%\claude_agents\<name>.out.jsonl, <name>.err.txt, <name>.pid
param(
    [string[]]$Names = @('dispatcher', 'real-calib', 'compound', 'audit'),
    [switch]$Status,
    [switch]$StopAll,
    [switch]$Fresh,
    [int]$GapSec = 60,
    [string]$Model = ''
)
$known = @('dispatcher', 'real-calib', 'compound', 'audit')
$defaultModel = @{ 'audit' = 'claude-fable-5-2' }
$Names = @($Names | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
$bad = @($Names | Where-Object { $known -notcontains $_ })
if ($bad.Count -gt 0) { Write-Output "unknown session name(s): $($bad -join ', '); known: $($known -join ', ')"; exit 1 }
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$logs = Join-Path $env:USERPROFILE "claude_agents"
New-Item -ItemType Directory -Force $logs | Out-Null

function Running($n) {
    $pidFile = Join-Path $logs "$n.pid"
    if (-not (Test-Path $pidFile)) { return $null }
    $id = [int](Get-Content $pidFile)
    return Get-Process -Id $id -ErrorAction SilentlyContinue
}

if ($StopAll) {
    Get-CimInstance Win32_Process |
        Where-Object { $_.ProcessId -ne $PID -and
                       ($_.Name -eq 'claude.exe' -or $_.CommandLine -match 'claude-code') -and
                       $_.CommandLine -notmatch 'AnthropicClaude' } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Write-Output "stopped all Claude Code processes"
    exit 0
}

if ($Status) {
    foreach ($n in $Names) {
        $p = Running $n
        $out = Join-Path $logs "$n.out.jsonl"
        $last = if (Test-Path $out) { (Get-Item $out).LastWriteTime.ToString("ddd HH:mm") } else { "never" }
        $state = if ($p) { "running (pid $($p.Id), $([math]::Round($p.WorkingSet64 / 1MB)) MB)" } else { "exited" }
        Write-Output ("{0,-11} {1,-32} last output {2}" -f $n, $state, $last)
    }
    $os = Get-CimInstance Win32_OperatingSystem
    Write-Output ("free memory {0:N1} GB" -f ($os.FreePhysicalMemory / 1MB))
    exit 0
}

$claude = (Get-Command claude -ErrorAction Stop).Source
$first = $true
foreach ($n in $Names) {
    if (Running $n) { Write-Output "$n is still running; not started again"; continue }
    $wt = Join-Path $repo ".claude\worktrees\$n"
    if (-not (Test-Path $wt)) {
        git -C $repo fetch -q origin
        git -C $repo show-ref --verify --quiet "refs/heads/wip/$n"
        if ($LASTEXITCODE -eq 0) { git -C $repo worktree add -q $wt "wip/$n" }
        else { git -C $repo worktree add -q -b "wip/$n" $wt origin/main }
        if (-not (Test-Path $wt)) { Write-Output "${n}: could not create worktree $wt; not started"; continue }
        Write-Output "${n}: created worktree $wt on wip/$n"
    }
    if (-not $first) { Start-Sleep $GapSec }
    $first = $false

    $prompt = @"
You are the course-lane session named $n, running headless as a hidden background process with no one watching and no terminal.
- check github: follow docs/agents/README.md, On check github. Read your task file first.
- Work until your items are done or blocked. Commit and push status after each step and before you exit.
- Anything that runs longer than about 10 min (run_all.py, a sweep, a fetch loop) starts as its own detached hidden process that writes a log and survives your exit (Start-Process -WindowStyle Hidden). Never in a background shell of this session. A rerun of the same command must resume from disk.
- When you have nothing to do but wait, push status saying what you wait for, and exit. Andrew pings you by starting you again.
- Spec 2026-11-20: no tracking on this VM; at most one LLM run at a time while free memory is under 3 GB.
"@
    $promptFile = Join-Path $logs "$n.prompt.txt"
    Set-Content -Path $promptFile -Value $prompt -Encoding utf8
    $argv = @('-p', '--permission-mode', 'auto', '--output-format', 'stream-json', '--verbose')
    $m = if ($Model) { $Model } elseif ($defaultModel.ContainsKey($n)) { $defaultModel[$n] } else { '' }
    if ($m) { $argv += @('--model', $m) }
    if (-not $Fresh) { $argv = @('-c') + $argv }
    $out = Join-Path $logs "$n.out.jsonl"
    if (Test-Path $out) { Move-Item -Force $out (Join-Path $logs "$n.prev.out.jsonl") }
    $p = Start-Process -FilePath $claude -ArgumentList $argv -WorkingDirectory $wt `
        -RedirectStandardInput $promptFile -RedirectStandardOutput $out `
        -RedirectStandardError (Join-Path $logs "$n.err.txt") -WindowStyle Hidden -PassThru
    Set-Content -Path (Join-Path $logs "$n.pid") -Value $p.Id
    Write-Output "$n started (pid $($p.Id)) in $wt"
}
