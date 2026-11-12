# Spec: agents over the batch-2 windows that fail closure, against the remedy tree (Lab report 3)

From: planning account. Date: 2026-11-12. Approved by Andrew 2026-11-12. Lane: course. Task c026. Session: dispatcher. Branch: `wip/dispatcher`, new from `origin/main`.

## Why
- Lab report 3 asks for the agent's decision in a loop on real tool output, an LLM-free check in the loop, and a baseline with the same tools and no agent. On real windows this is the remaining item of the Lab report 2 plan: agents over every batch-2 window with a failing check
- Deadline: results README pushed by Sat 14 Nov 20:00 local. Whatever has finished by then is reported; the run may continue after

## Windows
- The 84 windows of `results/2026-10-25_full_batch_2/windows.csv` with `outcome = fail` (closure above 19 px/h), 50 roots. List them in the proposal with root, window and closure value
- Not in scope: the 18 not-computable windows (declined by rule, no agent), the 34 failed and 2 not-run windows, the 925 passes

## Methods (same windows, same tracks, same remedy executors, same checker)
1. Fixed script: no remedy; closure fail -> decline. This is the batch-2 result as it stands; no run needed
2. Remedy tree (`agents/baselines.py` `run_tree`, step limit 8) on the real slice. If `run_tree` needs an adapter to run on a real window, write the smallest one, with a test, before any run
3. Diagnostician (pinned model and Claude Code version, real profile), through `scripts/real_slice.py` with cached tracks: dispatcher agent -> checker -> diagnostician -> auditor. One run
- Run the tree first. Remedy retracks are cached by window and settings tag, so the diagnostician reuses any retrack the tree already made, and the two methods see identical tool output for the same remedy

## Compute
- Lab server storage only; remedy retracks as Slurm CPU jobs on cluster nodes (`compute: cluster`), as in batch 2. Ledger check before every submit. Stop and Needs Andrew if the projected total since 2026-10-23 passes $12 (now $7.24 of $15)
- Stage one root at a time within the 35 GB cluster folder; clear a staged root copy only after its retrack outputs are md5-checked on storage, logged in `DELETED.log` (standing rule)
- Caps: 700 LLM calls in total; free VM memory 3 GB before each window. Session-limit stops are set aside and rerun, not recorded (as in c023)

## Proposal first
- `docs/proposals/2026-11-12_batch2-agents.md`, committed before any run: windows, methods, metrics, caps. No stop for approval; nothing changes after the first result is seen

## Metrics, computed in code
- Per method: accepted after a kept remedy (closure passes on the recheck), declined, step limit, errors
- Remedies tried, kept, rolled back; retracks run; cluster jobs and spend
- Diagnostician: LLM calls, tokens in and out, call time; fault named per window
- Agreement, diagnostician vs tree, per window (same outcome; same remedy kept)
- Disagreement list: every window where the two differ, with closure before and after each remedy tried
- Real windows have no ground truth. "Recovered" means the checker passes after a kept remedy; say so in the README

## Transcript for the report
- `results/2026-11-12_batch2_agents/example_traces.md`: two windows, one with a remedy kept and one declined. For each step: the action the agent sent (name, arguments, rationale), the tool result (check values before and after), and the final outcome. Mask any REGR, growth-zone or flank value as `[masked]`

## Results
- `results/2026-11-12_batch2_agents/`: README (setup, one command per step, the table per method, agreement, disagreement list, auditor flags on windows accepted after repair, known limits), `windows.csv` (outcome and check values only), `example_traces.md`. Traces and summaries stay in staging
- Then decisions and log entries; status ready to merge. Push status after every 20 windows

## Limits
- No REGR, growth-zone or flank values in the public repo. No host names. No deletes on the lab server
- No change to prompts, thresholds, remedies or the real profile
