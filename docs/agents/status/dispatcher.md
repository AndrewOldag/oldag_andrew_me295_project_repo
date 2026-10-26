# dispatcher
Updated: 2026-10-25 20:31 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 38
State: working
Now: item 39 (task c022): run 3, 20 of 126 windows collected (); status every 20 windows
Done since last update:
- Run 2 stopped by me after 5 of 126 windows: the ssh call of a register remedy retrack (0721_c2 w0-2) hung 20 min after the lab server had finished the track. Fix: ssh keepalive, and a lost tracking call fetches the finished host track; test added; suite 315 passed, 1 skipped; decisions entry (eb12715). Traces in staging/c022/stopped_run_2/
- Run 1 failed at collect after 3 windows (tracker 'arange' error on 0711_m1 w0-2 aborted the batch); fix: a collector error fails that window only (decisions)
Needs Andrew:
- none
