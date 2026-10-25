# real-calib
Updated: 2026-10-24 22:00 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 4
State: waiting on dispatcher
Now: items 5-6: 23 calibration windows measured; the cluster folder is cleared (item 6), so the 15 planned and 6 fallback windows go through the dispatcher's copy and GPU chain; `real_calib.py run --ext --fallback` measures each as its midline appears; 17 of the 21 must pass for 40
Done since last update:
- Item 6 read: cluster folder 6.8 of 40 GB after the planning account's approved delete; dispatcher asked to copy and run the 21 windows
- 9 windows 11-13 h (dispatcher GPU job, $0.028; spend $0.96 of $15): 7 measured; 0714_c4 screen failed (third of three), 0714_c9 screened out
- Fallback roots 0708_c10, 0708_c11 in play by the proposal rule (the planned set reaches at most 38)
- Re-screen of the 6 first-screen drop-outs: 4 measured; 0714_c4 w7-9 and w15-17 out again
- `measure/real_runner.py`: job count counts python processes only (one bash-wrapped midline build counted as 3 and blocked every RealRunner); `nproc --all`
Needs Andrew:
- none
