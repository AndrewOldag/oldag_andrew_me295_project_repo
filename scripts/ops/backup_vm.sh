#!/bin/bash
# VM backup to the lab server, run by hand (no schedule). Same layout as the 2026-10-16 backup:
#   <REMOTE_ROOT>/<name>/course/   me295-all.bundle, me295-planning-clone.bundle,
#                                  me295-nongit.tar.gz, SHA256SUMS
#   <REMOTE_ROOT>/<name>/research/ qb-all.bundle, research-nongit.tar.gz, SHA256SUMS
#   <REMOTE_ROOT>/<name>/RESTORE.md
# <name> is today's date (YYYY-MM-DD), or YYYY-MM-DD_<tag> with --tag.
#
# Usage: backup_vm.sh --conf FILE [--tag TAG] [--log FILE] run
#
# All hosts and paths come from the conf file (private/backup.conf; template
# config/backup.example.conf). Nothing is overwritten: an existing <name> on
# the server stops the run. Nothing on the server is ever deleted; old copies
# stay until Andrew removes them. Left out: *.tif, *.tiff, *.sldy, keys, .git
# of working trees, Claude caches. Sends at most RATE_MB MB/s to a nice 19,
# idle-I/O receiver after a load check.
set -euo pipefail
export PATH=/usr/bin:$PATH
EXCLUDES=(--exclude='*.tif' --exclude='*.tiff' --exclude='*.sldy' --exclude='id_rsa*'
          --exclude='id_ed25519*' --exclude='id_ecdsa*' --exclude='*.key' --exclude='vm_key*'
          --exclude='.env' --exclude='__pycache__')

log () { echo "$(date '+%F %T') backup: $*"; }
trap 'log "FAILED at line $LINENO"' ERR
die () { log "FAILED: $*"; exit 1; }

conf="" tag=""
while [ $# -gt 0 ]; do
    case $1 in
        --conf) conf=$2; shift 2 ;;
        --tag) tag=$2; shift 2 ;;
        --log) mkdir -p "$(dirname "$2")"; exec >> "$2" 2>&1; shift 2 ;;
        run) shift; break ;;
        *) die "unknown argument $1" ;;
    esac
done
[ -n "$conf" ] && [ -f "$conf" ] || die "conf file not found"
# shellcheck disable=SC1090
. "$conf"
for v in HOST REMOTE_ROOT COURSE_REPO PLANNING_CLONE RESEARCH_REPO RESEARCH_ITEMS HOME_CLAUDE STAGE; do
    [ -n "${!v:-}" ] || die "$v not set in conf"
done
RATE_MB=${RATE_MB:-40} MIN_FREE_GB=${MIN_FREE_GB:-10}
CONDA=${CONDA:-} ENVS=${ENVS:-}
u () { cygpath -u "$1" 2>/dev/null || echo "$1"; }
COURSE_REPO=$(u "$COURSE_REPO") PLANNING_CLONE=$(u "$PLANNING_CLONE")
RESEARCH_REPO=$(u "$RESEARCH_REPO") HOME_CLAUDE=$(u "$HOME_CLAUDE") STAGE=$(u "$STAGE")

name=$(date +%F)${tag:+_$tag}
case $name in *[!A-Za-z0-9_-]*) die "bad tag" ;; esac
out=$STAGE/$name
remote () { ssh -o BatchMode=yes -o ConnectTimeout=30 -o LogLevel=ERROR "$HOST" "$@"; }

# ---- checks before writing
free_gb=$(df -P -BG "$(dirname "$STAGE")" | awk 'NR==2 {sub("G","",$4); print $4}')
[ "$free_gb" -ge "$MIN_FREE_GB" ] || die "VM free space ${free_gb} GB below ${MIN_FREE_GB} GB"
[ ! -e "$out" ] || die "local stage $name exists"
remote "cd && test -d '$REMOTE_ROOT' && test ! -e '$REMOTE_ROOT/$name'" \
    || die "server: backup root missing or $name exists"

load_ok () {  # $1: fraction of cores as num/den, e.g. 1/2
    remote "awk -v n=\$(nproc) '{exit !(\$1 <= n*$1)}' /proc/loadavg"
}
tries=0
until load_ok 1/2; do
    tries=$((tries + 1)); [ $tries -le 3 ] || die "server load above half the cores after 3 retries"
    log "server load high; retry $tries in 15 min"; sleep 900
done
log "start $name; VM free ${free_gb} GB; server $(remote cat /proc/loadavg | cut -d' ' -f1-3)"

# ---- build locally
mkdir -p "$out/course" "$out/research" "$out/stage_setup"
git -C "$COURSE_REPO" bundle create "$out/course/me295-all.bundle" --all 2>/dev/null
git -C "$PLANNING_CLONE" bundle create "$out/course/me295-planning-clone.bundle" --all 2>/dev/null
git -C "$RESEARCH_REPO" bundle create "$out/research/qb-all.bundle" --all 2>/dev/null

s=$out/stage_setup
for e in $ENVS; do
    [ -n "$CONDA" ] && "$CONDA" env export -n "$e" > "$s/env_$e.yml" 2>/dev/null || true
    [ -n "$CONDA" ] && "$CONDA" run -n "$e" python -m pip freeze > "$s/pip_$e.txt" 2>/dev/null || true
    [ -n "$CONDA" ] && echo "$e $("$CONDA" run -n "$e" python --version 2>&1)" >> "$s/python_versions.txt" || true
done
schtasks.exe //query //fo csv //v > "$s/scheduled_tasks.csv" 2>/dev/null || true
cp "$HOME/.ssh/config" "$s/ssh_config" 2>/dev/null || true
{ git --version; claude --version 2>/dev/null || true; } > "$s/tool_versions.txt"

# Course tarball: main repo private/ data/ staging/ .claude/ (not worktrees),
# each worktree's staging/ and ignored results/, the planning clone's
# .claude/, home .claude settings, skills, plugins, projects, sessions.
list=$out/course.list
: > "$list.pairs"   # lines: <dir to cd into>|<member>
add () { [ -e "$1/$2" ] && echo "$1|$2" >> "$list.pairs" || true; }
cr_parent=$(dirname "$COURSE_REPO") cr_base=$(basename "$COURSE_REPO")
for d in private data staging .claude; do add "$cr_parent" "$cr_base/$d"; done
while read -r wt; do
    wt=$(u "$wt"); [ "$wt" = "$COURSE_REPO" ] && continue
    case $wt in
        "$COURSE_REPO"/*) p=$cr_parent; m=${wt#"$cr_parent"/} ;;
        *) p=$(dirname "$wt"); m=$(basename "$wt") ;;
    esac
    add "$p" "$m/staging"
    git -C "$wt" ls-files -o -i --exclude-standard -- results 2>/dev/null \
        | while read -r f; do add "$p" "$m/$f"; done
done < <(git -C "$COURSE_REPO" worktree list --porcelain | sed -n 's/^worktree //p')
add "$(dirname "$PLANNING_CLONE")" "$(basename "$PLANNING_CLONE")/.claude"
for d in settings.json skills plugins projects sessions; do add "$(dirname "$HOME_CLAUDE")" ".claude/$d"; done
add "$out" stage_setup

tar_pairs () {  # $1: pairs file; $2: archive; rest: extra tar options
    local pairs=$1 archive=$2; shift 2
    local args=() p m
    while IFS='|' read -r p m; do args+=(-C "$p" "$m"); done < "$pairs"
    tar czf "$archive" "${EXCLUDES[@]}" "$@" "${args[@]}"
}
tar_pairs "$list.pairs" "$out/course/me295-nongit.tar.gz" \
    --exclude="$cr_base/.claude/worktrees" --exclude='.claude/*/cache' --exclude='.claude/*/telemetry'

# Research tarball: RESEARCH_ITEMS = "name=path ..." (name is the member path
# in the archive); .git of the tracker working tree is left out (bundled).
: > "$out/research.pairs"
xf=()
for item in $RESEARCH_ITEMS; do
    n=${item%%=*} p=$(u "${item#*=}")
    [ -e "$p" ] || { log "research item $n not found; skipped"; continue; }
    echo "$(dirname "$p")|$(basename "$p")" >> "$out/research.pairs"
    b=$(basename "$p")
    [ "$n" = "$b" ] || xf+=(--transform="s,^$b/,$n/,;s,^$b\$,$n,")
done
tar_pairs "$out/research.pairs" "$out/research/research-nongit.tar.gz" \
    --exclude="$(basename "$RESEARCH_REPO")/.git" "${xf[@]}"

for part in course research; do
    (cd "$out/$part" && sha256sum -b -- * > SHA256SUMS)
done

{
    echo "# Restore: VM backup $name"
    echo
    echo "Made $(date '+%F %T %Z') by scripts/ops/backup_vm.sh. Layout as the 2026-10-16 backup; restore steps as in its RESTORE.md."
    echo
    echo "## Sizes"
    (cd "$out" && du -h course/* research/* | sed 's/^/- /')
    echo
    echo "## Course repo heads"
    git -C "$COURSE_REPO" for-each-ref --format='- %(refname:short) %(objectname:short)' refs/heads refs/tags
    echo
    echo "## Planning clone heads"
    git -C "$PLANNING_CLONE" for-each-ref --format='- %(refname:short) %(objectname:short)' refs/heads
    echo
    echo "## Tracker repo heads"
    git -C "$RESEARCH_REPO" for-each-ref --format='- %(refname:short) %(objectname:short)' refs/heads
    echo
    echo "Left out: *.tif, *.tiff, *.sldy, keys, .git of working trees, Claude caches and telemetry."
} > "$out/RESTORE.md"
log "built: $(cd "$out" && du -sh course research | awk '{printf "%s %s; ", $2, $1}')"

# ---- send
send () {  # $1: local file; $2: remote path relative to REMOTE_ROOT/name
    local f=$1 chunk=16 size n i=0 t0 el need
    size=$(stat -c %s "$f"); n=$(( (size + chunk * 1048576 - 1) / (chunk * 1048576) ))
    need=$(( chunk * 1000000000 / RATE_MB ))
    {
        while [ $i -lt $n ]; do
            t0=$(date +%s%N)
            dd if="$f" bs=1M skip=$((i * chunk)) count=$chunk status=none
            i=$((i + 1)); el=$(( $(date +%s%N) - t0 ))
            [ $el -ge $need ] || sleep "$(awk -v d=$((need - el)) 'BEGIN {printf "%.3f", d / 1e9}')"
        done
    } | remote "cd && nice -n 19 ionice -c3 sh -c 'cat > \"$REMOTE_ROOT/$name/$2\"'"
}
remote "cd && mkdir '$REMOTE_ROOT/$name' && mkdir '$REMOTE_ROOT/$name/course' '$REMOTE_ROOT/$name/research'"
t_start=$(date +%s)
for f in course/me295-all.bundle course/me295-planning-clone.bundle course/me295-nongit.tar.gz \
         course/SHA256SUMS research/qb-all.bundle research/research-nongit.tar.gz research/SHA256SUMS RESTORE.md; do
    until load_ok 3/4; do log "server load above three quarters; pause 60 s"; sleep 60; done
    send "$out/$f" "$f"
done
log "sent in $(( $(date +%s) - t_start )) s"

# ---- verify on the server
remote "cd && cd '$REMOTE_ROOT/$name' && (cd course && nice -n 19 sha256sum -c --quiet SHA256SUMS) && (cd research && nice -n 19 sha256sum -c --quiet SHA256SUMS)" \
    || die "server SHA256SUMS check failed; local stage kept at $name"
log "verified on server: SHA256SUMS OK in course/ and research/"
rm -rf -- "${out:?}"
log "local stage removed"
log "done $name; server backup root holds $(remote "cd && du -sh '$REMOTE_ROOT' | cut -f1")"
