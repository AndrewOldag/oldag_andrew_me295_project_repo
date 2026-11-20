---
id: c027
title: submit-and-forget cluster path; integrated run over all 101 roots with tree baseline and fresh one-root demo
lane: course
owner: dispatcher
state: waiting on Andrew
branch: wip/dispatcher
host: VM (LLM runs), cluster (retrack arrays on CPU; one GPU midline job), lab server (storage and relay)
created: 2026-11-18 14:20
last_update: 2026-11-20 14:40
blocker: cluster master to submit wave 1
done_marker: results/2026-11-18_integrated_run/README.md
---

Spec `docs/specs/2026-11-18_lab-report-4.md`, section A and B.

## Parts
- [x] New wip/dispatcher from origin/main
- [x] scripts/retrack_queue.py submit and fetch, with tests (A1)
- [x] Ledger: final c026 figure; wave 1 job list and worst-case cost (A2, A3)
- [ ] Proposal docs/proposals/2026-11-18_integrated-run.md committed before any run (B1)
- [ ] scripts/run_all.py, README command; start on cached windows (B2, B3)
- [ ] Status ready to submit; wave 1 submitted when the master is up; fetch
- [ ] Remedy tree on every failing window (B4)
- [ ] Fresh one-root end-to-end demo (B5)
- [ ] Results README, windows.csv, example_traces.md, failure modes (B7-B9)
- [ ] Decisions, log, status ready to merge
