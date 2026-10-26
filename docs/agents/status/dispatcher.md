# dispatcher
Updated: 2026-10-25 20:20 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 38
State: working
Now: item 39 (task c022): agent run over the 126 first-batch windows restarted after a collect fix; status every 20 windows
Done since last update:
- First run failed: stopped after 3 of 126 windows. The tracker error on 0711_m1 w0-2 ('arange', one of real-calib's 3 unmeasured windows) aborted every collect call; the dispatcher agent narrowed it to one window and finished. Traces in staging/c022/failed_run_1/
- Fix: a collector error fails that window only (agents/dispatcher.py); test added; suite 314 passed, 1 skipped; decisions entries for the fix and for --moved-span (b7bbede)
Needs Andrew:
- none
