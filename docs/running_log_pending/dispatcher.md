## 2026-10-25 (build account, dispatcher session, task c022)
- Done: agent run over real-calib's first batch (dispatcher inbox item 39): 126 windows, 11 roots; run 4 reported, wall 1892 s: 114 accepted, 9 declined (all at closure; bad stage correction 8, midline jitter 1), 3 not collected (tracker 'arange' error, same 3 as real-calib); auditor 91 cleared, 23 flagged. `results/2026-10-25_full_batch_1_agents/`
- Done: runs 1-3 failed, each on a run-code fault, fixed and tested: collect error fails one window not the batch (`agents/dispatcher.py`); ssh keepalive and fetch of a finished host track (`measure/real_runner.py`); summary.json written before printing, console escapes (`scripts/real_slice.py`). Decisions 2026-10-25
- Done: `scripts/real_slice.py --moved-span`; `scripts/full_batch_agents_report.py` (public tables, auditor text reduced to agent behaviour, numbers masked); tests; suite 317 passed, 1 skipped
- Found: 4 windows with no computable closure were accepted with no check gating; the auditor flagged all 4
- Demo: `python scripts/full_batch_agents_report.py --run staging/c022/run4 --out results/2026-10-25_full_batch_1_agents` prints "123 windows" and writes windows.csv and tables.md
- Remaining: Andrew to decide whether a window with no computable gating check should be declined instead of accepted; whether REGR and flank values already on main in `results/2026-10-25_real_subset/` (tables.md, README) stay
- Bottlenecks: none
