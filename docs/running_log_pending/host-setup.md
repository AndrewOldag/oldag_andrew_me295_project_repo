## 2026-10-23 (build account, session host-setup)
- Done: workstation key login from the VM works; survey in `private/workstation.md`: 14 cores / 20 threads, 62 GB RAM, no usable GPU, 46 GB free disk, imaging drive not mounted
- Done: tracker environment built on the workstation from `envs/qb.yml` (micromamba, work folder, nice 19); tracker master d5f1829, gate2-windowed-coupling 52e9bd1 and stage-auxdata 888f972 copied there as git archives made on the VM
- Done: synthetic test, rod `v3_growth_zone_clean_s10`, state st1: render byte-identical, tracks max |d| 2.3e-13 px against the lab-server run (limit 1e-6); tracking loop 4.4 s against 6.2 s (`results/2026-10-23_host_setup/README.md`)
- Failed: real-window test (0708_m12, 4-6 h) not run; frame transfer to the workstation refused by the session's permission check, both routes
- Done: optional `host:` field on the task board (`scripts/board.py`, `tasks/README.md`), set on every open course task; `tests/test_board.py` 10 passed; full suite 205 passed
- Done: decisions entries for host roles, the one-host-per-part rule and the synthetic reproduction
- Demo: `python scripts/board.py` prints the board with a host column
- Remaining: real-window test once Andrew allows a transfer route; then status ready to merge and the coordinator applies the host assignment (spec item 6)
- Bottlenecks: on Andrew: permission for lab-server to workstation frame transfer
