# real-calib
Updated: 2026-10-24 21:45 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 4
State: waiting on Andrew
Now: item 5: 23 calibration windows measured; 15 planned windows and the 6 fallback windows (now needed: the planned set reaches at most 38) wait for ft2 midlines; the cluster folder is at its cap
Done since last update:
- 9 windows 11-13 h (dispatcher GPU job, $0.028; spend $0.96 of $15): 7 measured; 0714_c4 screen failed (third of three), 0714_c9 screened out
- Fallback roots 0708_c10, 0708_c11 now in play by the proposal rule; 17 of the 21 remaining windows must pass
- Re-screen of the 6 first-screen drop-outs: 0708_c9 w15-17, 0714_c13 w7-9, 0721_c5 w7-9, 0721_c6 w7-9 measured; 0714_c4 w7-9 screened out, w15-17 screen failed (probe error) again
- At most 40 measured if all 24 new windows pass; fallback roots 0708_c10, 0708_c11 (proposal) queued in the dispatcher's chain after the 24, measured only if fewer than 40 pass
- `measure/real_runner.py`: job count counts python processes only (one bash-wrapped midline build counted as 3 and blocked every RealRunner); `nproc --all`
Needs Andrew:
- Cluster work folder at its cap (about 40,900 of 40,960 MiB; if "40 GB" was meant as decimal, it is about 2.9 GB over). The 21 remaining windows need about 9 GB. Options: (a) raise the cap to about 50 GiB; (b) Andrew deletes cluster frames already used; (c) ft2 midlines on the lab server CPU, one at a time, 3 threads, nice 19, about 30 min per window (heavier than light jobs)
