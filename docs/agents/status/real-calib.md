# real-calib
Updated: 2026-10-24 21:00 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 4
State: waiting on Andrew
Now: item 5: 16 calibration windows measured (12 first + 4 of the 6 re-screened with the 50 px polyline-end rule); 24 new windows queued for ft2 midlines, about 6 fit under the 40 GB cluster cap; `real_calib.py run --ext` picks windows up as midlines appear
Done since last update:
- Re-screen of the 6 first-screen drop-outs: 0708_c9 w15-17, 0714_c13 w7-9, 0721_c5 w7-9, 0721_c6 w7-9 measured; 0714_c4 w7-9 screened out, w15-17 screen failed (probe error) again
- At most 40 measured if all 24 new windows pass; fallback roots 0708_c10, 0708_c11 (proposal) queued in the dispatcher's chain after the 24, measured only if fewer than 40 pass
- `measure/real_runner.py`: job count counts python processes only (one bash-wrapped midline build counted as 3 and blocked every RealRunner); `nproc --all`
Needs Andrew:
- Cluster work folder about 37.2 of 40 GB; the 24 new windows need about 10 GB (plus about 2.5 GB if the fallback is needed). Options: (a) raise the cap to about 50-53 GB; (b) Andrew deletes cluster frames already used; (c) ft2 midlines on the lab server CPU, one at a time, 3 threads, nice 19, about 30 min per window (heavier than light jobs)
