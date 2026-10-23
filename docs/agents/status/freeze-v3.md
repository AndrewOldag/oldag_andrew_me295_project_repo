# freeze-v3
Updated: 2026-10-23 14:55 (local)
Lane: course
Branch: wip/freeze-v3
Last inbox item done: 6
State: working
Now: item 5 read (work space freed); held-out sizing sweep
Done since last update:
- Item 4: approval recorded (d9d5318)
- v3 rods, `stage_log_missing`, curvature-corrected width-free ratio (field-level error under 1e-3; v2 width_change 0.435 -> 0.000), no-growth tolerance 0.5 %/h, `measure/metrics.py` (1a16f11)
- No rename or overwrite on the lab server (rules-2): write-once outputs with `.ok`, code folder per commit, new plan and log names per sweep (7eb7cc3); `qb_track.py` track length from the rod (500 px v3, 400 v2)
- Driver `scripts/synth/scored_v3.py` (47a3c47, ece537c); README steps (9eb747d); suite 242 passed, 5 skipped
- Clean basis at v3 geometry: 100 tracker runs, 0 failed, 405 s + 149 s sweep wall, load at most 6.13 on 32 cores. No clean value over a threshold (max rigid_invariance 1.42, closure 0.36, plane_sections 2.97); largest flank error 0.575 %/h. Thresholds and tolerance stay (433fdcf, `results/2026-10-23_freeze_v3/basis.md`)
- Tracker runs used: 100 of the 600 cap. Disk radius on v3 rods is 14 px (tracker default); label states scale `enlarge_patch` from it, as the executors do
Needs Andrew:
- Work space on the lab server: 9.47 GB of the 10 GB sweep limit after the basis. Still needed: about 3.5 GB of rendered rods (sizing 0.7, labels 2.7) plus outputs. Sessions may not delete there. Choose: (a) raise the limit to 16 GB for freeze v3, or (b) delete the old rendered v2 rods (4.77 GB, shared rods folder) yourself. Then `check github` and I continue with sizing
