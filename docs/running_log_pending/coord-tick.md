## 2026-10-24 (build account, session coord-tick)
- Done: `scripts/ops/coordinator_tick.ps1` (lock, fetch, sorted ls-remote hash, skip under 60 min, headless `claude -p` pass stopped at 20 min, log lines start/commit/exit/end/pings) and `scripts/ops/install_coordinator_tick.ps1` (task `me295-coordinator-tick`, 10 min, S4U, IgnoreNew); 2adff36
- Done: 3 tick tests in `tests/test_ops.py` with stubbed git and claude (skip on unchanged refs, order-independent hash, hourly full pass, live lock); `tests/test_ops.py` 8 passed
- Done: docs: `CLAUDE.md` Agents, `docs/agents/README.md`, `docs/decisions.md`, coordinator inbox item 19, `README.md`
- Done: hand test (Andrew, main repo folder): full pass 168 s, exit 0, 15 turns, out 5816 tokens, cache read 625818, 0.56 USD; merged wip/freeze-v31 (2c373d1, suite 256 passed), status 6608cca. Skip tick 13:08: no Claude call
- Demo: `powershell -File scripts/ops/coordinator_tick.ps1` appends to `OPS_DIR/coordinator_tick/tick.log` (skip line, or start/commit/exit/end/pings)
- Remaining: Andrew installs the task elevated; check the first scheduled (S4U) full pass in the log; stop live coordinator sessions
- Bottlenecks: install on Andrew (elevated shell)
