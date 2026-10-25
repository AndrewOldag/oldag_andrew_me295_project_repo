# Real slice, end to end with agents: 0708_m12, 4-6 h

Command: `python scripts/real_slice.py` (defaults), then `python scripts/real_slice.py --audit-only` (see below). Branch wip/dispatcher after the merge of main with the Claude Code re-pin (2.1.310); model claude-opus-5-5. 2026-10-23.

All real-movie numbers here use the current fine-tuned midline net: PROVISIONAL (the net was trained partly on traces outside the include-yes, in-window rule; decisions 2026-10-23).

## Chain
| Stage | What happened |
| :-- | :-- |
| Dispatcher (agent) | Round 1: split_root, submit (free backend), wait 15. Round 2: collect, finish. 2 rounds, 1 window collected, 0 cluster core-hours |
| Tracker | Compute host from `private/real_runner.yaml` (here the lab workstation; the dispatcher's free backend is named `lab_server`). Net midline, stage-corrected tracker 52e9bd1, uncoupled, 400 px, 80 frames |
| Checker | closure 0.945 px/h pass (threshold 1.0); plane_sections 133.6 %/h fail (3.25); rigid_invariance not run (no moved copy for real movies) |
| Diagnostician | request_info check_report, frame_quality, midline_jitter; apply_remedy smooth_midline light: plane_sections 133.6 -> 25.9 %/h, closure 0.945 -> 2.857 px/h; then decline, fault midline_jitter ("smoothing cannot be applied again ... cannot be trusted"). 5 steps, 5 calls, 21594 tokens in, 2077 out, 24.4 s of calls |
| Auditor | 1 run, 0 accepted. Report: r01 declined, both computed checks failed after the kept remedy; nothing from the batch is reported. 1 step |

- Wall time 71 s for the dispatcher, tracking and diagnostician (tracker runs cached after the first)
- The plane-sections failure is expected on real movies (midline curvature noise; `docs/proposals/2026-10-23_real-midline-smoothing.md`; option 1 failed its validation, `results/2026-10-23_midline_fit_validation/`)

## Auditor with no accepted run
- First call (in the full run) was skipped by the script's rule then in place (no accepted run). With the rule changed to always call the auditor, the first try failed: flag and clear take a list of accepted run ids; with none, the empty id list is not a valid JSON schema for the CLI (2 failed steps, outcome error)
- Fix in `scripts/real_slice.py` only (audit/llm.py unchanged): with no accepted run the auditor gets request_info and report. `--audit-only` re-ran the auditor on the recorded batch from cached tracker outputs (no tracker or diagnostician re-run)

## Files
- `dispatcher_trace.jsonl`, `diagnostician_trace.jsonl`, `auditor_trace.jsonl`, `summary.json`
