#!/bin/bash
# Heartbeat: append the date and the uptime to the VM health log.
# Run every 5 min by the scheduler (scripts/ops/install_schedule.ps1).
#
# Usage: heartbeat.sh LOG [MAX_GAP_S]
# Line:  YYYY-MM-DD HH:MM:SS epoch=<s> up=<s> boot=YYYY-MM-DD HH:MM:SS
# If the previous line is more than MAX_GAP_S old (default 600, two missed
# beats), a GAP line goes in first. The first gap ever also writes FIRST_GAP
# beside the log, for the coordinator to report to Andrew. Nothing here keeps
# the VM awake: one short write, then exit.
export PATH=/usr/bin:$PATH
log=${1:?usage: heartbeat.sh LOG [MAX_GAP_S]}
max_gap=${2:-600}
mkdir -p "$(dirname "$log")"

now=${HEARTBEAT_NOW:-$(date +%s)}          # HEARTBEAT_NOW: tests only
up=$(cut -d' ' -f1 /proc/uptime | cut -d. -f1)
fmt () { date -d "@$1" '+%Y-%m-%d %H:%M:%S'; }

prev=$(grep -o 'epoch=[0-9]*' "$log" 2>/dev/null | tail -n 1 | cut -d= -f2)
if [ -n "$prev" ] && [ $((now - prev)) -gt "$max_gap" ]; then
    gap="GAP from $(fmt "$prev") to $(fmt "$now") ($(( (now - prev) / 60 )) min)"
    echo "$gap" >> "$log"
    first="$(dirname "$log")/FIRST_GAP"
    [ -e "$first" ] || echo "$gap" > "$first"
fi
echo "$(fmt "$now") epoch=$now up=$up boot=$(fmt $((now - up)))" >> "$log"
