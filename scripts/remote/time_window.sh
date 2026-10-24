#!/bin/sh
# Time the midline and the tracker on one window of one real movie (spec 2026-10-23, B2).
# Usage: sh time_window.sh PYTHON CODE_DIR IMGDIR OUT_DIR TAG FROM_H TO_H
# One job, one single-thread worker, lowest CPU and I/O priority. Starts only
# if the 1 min load is at most half the cores and no other tracker job of this
# account runs (decisions, 2026-10-11). Writes only under OUT_DIR.
# Log lines hold numbers only: no host name, account or path.
set -e
py=$1; code=$2; imgdir=$3; out=$4; tag=$5; h0=$6; h1=$7
cores=$(nproc)
l1=$(cut -d' ' -f1 /proc/loadavg)
if awk -v l="$l1" -v c="$cores" 'BEGIN {exit !(l > c / 2)}'; then
    echo "{\"status\": \"load_too_high\", \"load1\": $l1, \"cores\": $cores}"; exit 1
fi
if pgrep -u "$(id -u)" -f 'qb_track.py|real_midline.py|sweep.py run' >/dev/null; then
    echo '{"status": "other_job_running"}'; exit 1
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH="$code"
run() {
    nice -n 19 ionice -c 3 /usr/bin/time -v "$@"
}
echo "{\"step\": \"preflight\", \"cores\": $cores, \"loadavg\": \"$(cut -d' ' -f1-3 /proc/loadavg)\", \"mem_avail_kb\": $(awk '/MemAvailable/ {print $2}' /proc/meminfo)}"
run "$py" "$code/scripts/remote/real_midline.py" --imgdir "$imgdir" --from-h "$h0" --to-h "$h1" \
    --out "$out/${tag}_midline.npz" > "$out/${tag}_midline.log" 2>&1
echo "{\"step\": \"midline_done\", \"loadavg\": \"$(cut -d' ' -f1-3 /proc/loadavg)\"}"
run "$py" "$code/scripts/remote/qb_track.py" --imgdir "$imgdir" --midline "$out/${tag}_midline.npz" \
    --out "$out/${tag}_track.npz" --movie real --from-h "$h0" --to-h "$h1" > "$out/${tag}_track.log" 2>&1
echo "{\"step\": \"track_done\", \"loadavg\": \"$(cut -d' ' -f1-3 /proc/loadavg)\", \"out_bytes\": $(stat -c %s "$out/${tag}_track.npz")}"
