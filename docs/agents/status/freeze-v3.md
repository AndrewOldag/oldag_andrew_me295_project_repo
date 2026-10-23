# freeze-v3
Updated: 2026-10-23 14:50 (local)
Lane: course
Branch: wip/freeze-v3
Last inbox item done: 2
State: working
Now: item 4: implementing; no tracker run yet. Runs need a decision on work space (below)
Done since last update:
- Item 4: approval recorded in `docs/decisions.md` and the proposal header (d9d5318)
- Item 4: v3 rods, `stage_log_missing`, curvature-corrected width-free ratio (field-level error under 1e-3; v2 width_change 0.435 -> 0.000), no-growth tolerance 0.5 %/h, `measure/metrics.py`; full suite 235 passed, 5 skipped (1a16f11)
- Next: no rename or overwrite on the lab server (spec audit rules-2), then `scripts/synth/scored_v3.py`
Needs Andrew:
- Work space on the lab server: 7.53 GB used of the 10 GB sweep limit (`docs/decisions.md`, 2026-10-11). Freeze v3 needs about 6.0 GB of rendered rods (v3 frames are 768 px tall, bent rods 640 px wide) plus about 0.3 GB of tracker outputs: about 13.9 GB in all. Sessions may not delete there. Choose: (a) raise the limit to 16 GB for freeze v3 (free disk is large), or (b) Andrew deletes old rendered v2 rods (4.77 GB in the shared rods folder). Until then no v3 sweep starts
- Tracker runs on the lab server rename `.part.npz` to the final name and code sync overwrites files (rules-2). I am changing this to write-once files with `.ok` markers, a code folder per commit and plan and log files that are never overwritten. Tell me if you want the old behaviour kept instead
