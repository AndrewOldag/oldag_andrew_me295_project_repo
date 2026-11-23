---
id: c027
title: submit-and-forget cluster path; integrated run over all 101 roots with tree baseline and fresh one-root demo
lane: course
owner: dispatcher
state: working
branch: wip/dispatcher
host: VM (LLM runs), cluster (retrack arrays on CPU; one GPU midline job), lab server (storage and relay)
created: 2026-11-18 14:20
last_update: 2026-11-23 08:05
blocker: waiting for the cut-off Thu 26 Nov 12:00 (final-now audit)
done_marker: results/2026-11-18_integrated_run/README.md
---

Spec `docs/specs/2026-11-18_lab-report-4.md`, section A and B.

## Parts
- [x] New wip/dispatcher from origin/main
- [x] scripts/retrack_queue.py submit and fetch, with tests (A1)
- [x] Ledger: final c026 figure; wave 1 job list and worst-case cost (A2, A3)
- [x] Proposal docs/proposals/2026-11-18_integrated-run.md committed before any run (B1)
- [x] scripts/run_all.py, README command; start on cached windows (B2, B3)
- [ ] Status ready to submit; wave 1 submitted when the master is up; fetch (submitting since 2026-11-20 14:30; register held)
- [x] Remedy tree on every failing window (B4): first pass 4 accept, 43 decline, 8 paused; 8 rounds ended 2026-11-23 05:48, 2 windows stay paused; rescore of the 38 c026 windows ended 07:20, 3 paused (0714_c9__w10-12 register_v2 jobs failed twice: stage file missing in the staged window)
- [x] Fresh one-root end-to-end demo (B5): 0708_c4, same outcome 12 of 12 windows and same auditor flag as the cached run (results demo.md)
- [x] Results README, windows.csv, example_traces.md, failure modes (B7-B9); final-now audit of 0708_m9, 0721_m5, 0727_cc7 at the cut-off Thu 26 Nov 12:00
- [ ] Decisions, log, status ready to merge
