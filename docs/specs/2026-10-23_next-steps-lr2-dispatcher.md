# Spec: Lab report 2 proposal, dispatcher, first real-movie slice

From: planning account. Date: 2026-10-23. Status: open. Lane: course.

## Where the project is
- Built: checker, synthetic rods and faults, diagnostician, three baselines, held-out faults, freeze v2, scored runs v1, auditor v1, provisional real frame_quality reference, task board, VM backup and restore
- Not built: dispatcher. No real drought or recovery movie has gone through the pipeline
- Due: Lab report 2 Fri 30 Oct (1-page proposal; commitment point). Lab report 3 Fri 13 Nov (smallest slice running end to end). Lab report 4 Mon 23 Nov. Presentation Wed 2 Dec. Final Wed 9 Dec
- Running in parallel: the spec audit (spec 2026-10-23_spec-audit). Its findings feed items A3 and B1

## Sessions
| Name | Lane | Branch | Task | Starts |
| :-- | :-- | :-- | :-- | :-- |
| lab-report-2 | course | wip/lab-report-2 | c009 | now |
| dispatcher | course | wip/dispatcher | c010 | now (B1-B4); B5 after Andrew approves |

## A. Lab report 2 (lab-report-2)
1. Read `docs/context/course/Lab-Guideline.md` (Lab Report 2), `Project-Guideline.md` (proposal content, viability checks), `docs/reports/2026-10-16_lab-report-1.md`, `docs/context/project_summary.md`, `docs/decisions.md`, the log since 18 Oct
2. Draft `docs/reports/2026-10-30_lab-report-2.md`, one page for the proposal itself:
   - Research question as in Lab report 1 (LLM agent guided by deterministic beam-kinematics checks decides repair vs decline, compared with scripted and single-agent baselines). Changes since Lab report 1 stated as changes
   - Intended users: high-throughput growth kinematics
   - Why an agent; tools and architecture (dispatcher, tracker, checker, diagnostician, auditor; typed actions, plain-Python orchestrator)
   - Evaluation: synthetic rods with known truth, held-out faults, real-movie subset; metrics as frozen in freeze v2
   - Risks, each with what is done about it. No risk attributed to course staff
   - Plan to Lab reports 3-5 with dates. Lab report 3 = section B slice
   - Then, outside the page: updated related-work note (Lab report 1 note plus any paper the audit adds), and a short "repo and log maintained" section with commit counts and dates from git
3. Every number from the log or a results README, with commit hash. Mark places Andrew must decide with `[ANDREW]`
4. Written to course staff. No "checked by Andrew", no messages addressed to Andrew, no to-read list
5. After the audit SUMMARY.md exists: add accepted findings that change the plan. Not before Andrew marks them
6. Ready for Andrew by Wed 28 Oct. Status ready to merge

## B. Dispatcher and first real-movie slice (dispatcher)
1. Proposal first: `docs/proposals/2026-10-23_dispatcher.md`. Contents:
   - Input: `manifest/root_manifest.csv` (include yes, usable windows only), a cost budget, the queue state
   - Output: typed actions only (same pattern as `agents/actions.py`): split root into root-by-window tasks, estimate cost, request approval, submit, wait, collect. The orchestrator executes; the agent submits nothing itself
   - Human approval point: the budget, before any cluster job. Lab server runs need no budget approval but obey the shared-machine limits, which the orchestrator enforces, not the agent
   - Baseline for the dispatcher: a fixed script that splits and submits in manifest order
   - Tests with a fake queue; no real jobs in tests
   - Commit the proposal and stop for Andrew's approval before writing dispatcher code
2. Tracker timing, now, on the lab server under the shared-machine limits: one include-yes drought root, one 2 h window inside its usable hours, uncoupled, current settings. Record wall time, peak memory, output size, frames. Extrapolate to 24 h and to 118 roots. This is the input to the cost estimate. One sweep at a time; check for other `oldag` jobs first
3. Cluster rules (Andrew, 2026-10-23):
   - Rate: lowest tier, $0.012 per compute unit (the lab is under the first tier this fiscal year). CPU core-hour = 1 unit ($0.012). P100 or V100 GPU-hour = 10 units ($0.12)
   - GPUs: P100 or V100 only. Never L40S, H100 or H200. Before each job, check which of P100/V100 has free nodes (`sinfo`, `squeue`) and request that type; if neither is free, wait or run CPU-only. Request a GPU only if the timing shows the tracker uses it
   - Budget for the initial trials (timing plus the first real slice): $5 total, CPU and GPU together. Hard cap
   - Each job's worst-case cost = requested resources x `--time` limit x rate. Set `--time` so that the worst case of every job submitted plus all spent so far stays within $5. Running total in `results/2026-10-23_tracker_timing/cluster_spend.csv` (job, resources, time limit, worst case, actual from `sacct`)
   - Each job still needs Andrew's direct approval before submission. The VM does not submit to the cluster itself; the job script and the cost line go to Andrew
4. Cost estimate for the computing cluster from the timing: core-hours and cost for (a) the 12-16 root evaluation subset with repeats and (b) all roots once. `results/2026-10-23_tracker_timing/`. Do not submit anything to the cluster
5. After Andrew approves the proposal and a budget: build the dispatcher, then the smallest real slice for Lab report 3: 2-3 include-yes roots (one control, one drought, one recovery), one window each, dispatcher -> tracker -> checker -> diagnostician -> auditor, end to end. Stage one root at a time on the VM; delete staged images after use

## Limits
- Real movies: include yes and usable windows only
- Lab server: shared-machine limits, no deletes, moves or renames
- Cluster: nothing submitted without Andrew's approval of a cost estimate. P100/V100 only. Initial trials capped at $5
- Freeze v2 items unchanged. Changes go through Andrew and a new freeze version

## Stop and ask Andrew
- Dispatcher proposal written (approval needed before code)
- Cost estimate written (budget needed before any cluster job)
- The timing root fails the checker in a way not in the fault list
- Lab report 2 draft ready

## Done means
- c009: report draft on `wip/lab-report-2`, `[ANDREW]` items listed in status
- c010: proposal, timing results and cost estimate committed; then, after approval, the slice runs end to end from one command in the README
