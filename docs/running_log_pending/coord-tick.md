## 2026-10-24 (build account, session coord-tick)
- Done: `scripts/ops/coordinator_tick.ps1` (lock, fetch, sorted ls-remote hash, skip under 60 min, headless `claude -p` pass stopped at 20 min, log lines start/commit/exit/end/pings) and `scripts/ops/install_coordinator_tick.ps1` (task `me295-coordinator-tick`, 10 min, S4U, IgnoreNew); 2adff36
- Done: 3 tick tests in `tests/test_ops.py` with stubbed git and claude (skip on unchanged refs, order-independent hash, hourly full pass, live lock); `tests/test_ops.py` 8 passed
- Done: docs: `CLAUDE.md` Agents, `docs/agents/README.md`, `docs/decisions.md`, coordinator inbox item 19, `README.md`
- Demo: `powershell -File scripts/ops/coordinator_tick.ps1` appends to `OPS_DIR/coordinator_tick/tick.log` (skip line, or start/commit/exit/end/pings)
- Remaining: hand test (one full pass, one skip tick); Andrew installs the task elevated; check the first scheduled full pass in the log
- Bottlenecks: hand test and install on Andrew (session guard blocks git on the main checkout; live coordinator must be stopped first)
