# real-calib
Updated: 2026-10-24 23:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 4
State: working
Now: items 5-6: all 48 calibration midlines built (dispatcher GPU, spend $1.03 of $15); `real_calib.py run --ext --fallback` on the lab server: 30 of 36 extension windows done; summary and threshold when the last lands
Done since last update:
- Item 6 read: cluster folder 6.8 of 40 GB after the planning account's approved delete; dispatcher asked to copy and run the 21 windows
- 9 windows 11-13 h (dispatcher GPU job, $0.028; spend $0.96 of $15): 7 measured; 0714_c4 screen failed (third of three), 0714_c9 screened out
- Fallback roots 0708_c10, 0708_c11 in play by the proposal rule (the planned set reaches at most 38)
- Re-screen of the 6 first-screen drop-outs: 4 measured; 0714_c4 w7-9 and w15-17 out again
- `measure/real_runner.py`: job count counts python processes only (one bash-wrapped midline build counted as 3 and blocked every RealRunner); `nproc --all`
Needs Andrew:
- none
