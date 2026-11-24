# After the history rewrite of 2026-11-24 (Andrew approved 2026-11-23): point this VM's checkout and
# worktrees at the rewritten history without touching untracked or ignored files (private\, staging\,
# caches, overlays). Run once, in PowerShell, from the repo root, with every session exited.
#   git fetch origin
#   git show origin/main:scripts/ops/after_rewrite.ps1 | Out-File -Encoding utf8 $env:TEMP\after_rewrite.ps1
#   powershell -ExecutionPolicy Bypass -File $env:TEMP\after_rewrite.ps1
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
if (-not (Test-Path (Join-Path $repo '.git'))) { throw 'Run this from the repo root.' }
$oldMain = '73668b3a2527604a0d8395faeebb7fa6c5cfebdb'   # main before the rewrite

$env:GIT_ASK_YESNO = 'false'   # never stop on 'Unlink ... failed. Should I try again? (y/n)'
function Invoke-GitChecked { & git.exe @args; if ($LASTEXITCODE -ne 0) { throw "git $args failed ($LASTEXITCODE)" } }

# 1. Nothing may be running, and no tracked file may have unpushed edits
$st = & powershell -File (Join-Path $repo 'scripts\ops\agents.ps1') -Status
if ($st -match 'running') { Write-Output $st; throw 'A session is still running. Wait for it to exit, then run this again.' }
$wts = @()
$cur = $null
foreach ($l in (& git.exe worktree list --porcelain)) {
    if ($l -like 'worktree *') { $cur = @{ path = $l.Substring(9); branch = $null } ; $wts += $cur }
    elseif ($l -like 'branch refs/heads/*') { $cur.branch = $l.Substring(18) }
}
foreach ($w in $wts) {
    $dirty = & git.exe -C $w.path status --porcelain --untracked-files=no
    if ($dirty) { Write-Output "Tracked changes in $($w.path):"; Write-Output $dirty; throw 'Commit and push (or discard) those first.' }
}

# 2. Recreate the three freeze tags on the rewritten commits (same message and date), then fetch
Invoke-GitChecked tag -l | ForEach-Object { & git.exe tag -d $_ | Out-Null }
Invoke-GitChecked fetch origin --prune --force --no-tags
$env:GIT_COMMITTER_DATE = '1791868618 -0700'; Invoke-GitChecked -c user.name='Andrew Oldag' -c user.email='andrewnoldag@gmail.com' tag -a freeze-v2 d7220663e547bdc37fe38113e12c043342684932 -m 'Freeze v2, approved by Andrew 2026-10-12 (docs/proposals/2026-10-12_freeze-v2.md)'
$env:GIT_COMMITTER_DATE = '1792805637 -0700'; Invoke-GitChecked -c user.name='Andrew Oldag' -c user.email='andrewnoldag@gmail.com' tag -a freeze-v3 e34bd075a4171b607d6d56d5ad09edd64ab262ec -m 'Freeze v3: docs/proposals/2026-10-23_freeze-v3.md; labels results/2026-10-23_freeze_v3/labels.json; Claude Code 2.1.310'
$env:GIT_COMMITTER_DATE = '1792976670 +0000'; Invoke-GitChecked -c user.name='Andrew Oldag' -c user.email='andrewnoldag@gmail.com' tag -a freeze-v4 bb891bba937cf7e8a719f68d4a9f31d94ce0c82c -m 'Freeze v4: docs/proposals/2026-10-25_freeze-v4-candidate.md; labels results/2026-10-25_freeze_v4/labels.json; candidate v4; Claude Code 2.1.310'
Remove-Item Env:GIT_COMMITTER_DATE
Invoke-GitChecked push --force origin 'refs/tags/*:refs/tags/*'

# 3. Reset every checkout to its rewritten branch (untracked and ignored files stay)
foreach ($w in $wts) {
    $b = $w.branch
    if (-not $b) { Write-Output "skip (detached): $($w.path)"; continue }
    & git.exe show-ref --verify --quiet "refs/remotes/origin/$b"
    $target = if ($LASTEXITCODE -eq 0) { "origin/$b" } else { 'origin/main' }
    Invoke-GitChecked -C $w.path reset --hard $target
    Write-Output "$($w.path) [$b] -> $target"
}

# 4. Other local branches: follow the remote, or drop the old ref if the remote has no such branch
$inUse = $wts | ForEach-Object { $_.branch }
foreach ($b in (& git.exe for-each-ref --format='%(refname:short)' refs/heads)) {
    if ($inUse -contains $b) { continue }
    & git.exe show-ref --verify --quiet "refs/remotes/origin/$b"
    if ($LASTEXITCODE -eq 0) { Invoke-GitChecked branch -f $b "origin/$b"; Write-Output "branch $b -> origin/$b" }
    else { Invoke-GitChecked branch -D $b; Write-Output "branch $b removed (no rewritten copy on origin; its old commits must not be pushed)" }
}

# 5. Drop every reference to the old commits. No gc: on this VM git cannot unlink object files
#    (Invalid argument), so old objects stay as unreachable loose files. A push sends only reachable
#    commits, so they can never reach GitHub again. Auto gc is turned off for this clone.
Invoke-GitChecked config gc.auto 0
Invoke-GitChecked reflog expire --expire=now --all
$ErrorActionPreference = 'Continue'
$refs = & git.exe for-each-ref --contains $oldMain 2>$null
$ErrorActionPreference = 'Stop'
if ($refs) { Write-Output $refs; throw 'A ref still contains old main. Tell the planning account.' }
Write-Output 'Done: no branch or tag here reaches the old history. Re-enable the hourly task:'
Write-Output '  schtasks /Change /TN "ME295 agents ping" /ENABLE'
