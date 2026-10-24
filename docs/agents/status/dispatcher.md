# dispatcher
Updated: 2026-10-23 20:05 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 16
State: waiting on Andrew
Now: item 16: proposal written (stop for Andrew); B5 part 2 runs end to end without agents; the agent run waits for the Claude Code re-pin (freeze-v3)
Done since last update:
- Item 16, proposal: `docs/proposals/2026-10-23_real-midline-smoothing.md`: spatial spline fit per frame, time smoothing, centre-chain curvature; each with what changes, a fixed parameter rule and a v3 synthetic validation (all checker values unchanged within 1e-3). Recommends the spline fit (midline source only; residual = pixel quantization, 0.289 px rms). Not implemented
- Item 16, B5 part 2: `measure/real_runner.py`, `scripts/real_slice.py` (one command; README), `tests/test_real_slice.py` (6 passed); full suite 228 passed
- Item 16, run without agents (`--no-agent`): dispatcher script -> workstation tracker -> checker on 0708_m12 4-6 h: closure 0.945 px/h pass; plane_sections 134 %/h fail (expected); rigid invariance not run. `results/2026-10-23_real_slice_noagent/`
Needs Andrew:
- Approve, change or reject the smoothing proposal (option 1 recommended)
- Agent run of the real slice (dispatcher agent, diagnostician, auditor): blocked. Installed Claude Code is 2.1.310; `config/models.yaml` on main pins 2.1.302, so the launcher refuses. wip/freeze-v3 re-pins to 2.1.310; once that is on main, `python scripts/real_slice.py` runs the full chain
- Lab-server and workstation work folders left as they are (no deletes)
