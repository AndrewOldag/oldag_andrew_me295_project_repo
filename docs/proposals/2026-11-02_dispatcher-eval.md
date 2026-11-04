# Dispatcher agent vs fixed script on the fake queue: proposal

From: build account, dispatcher session. Date: 2026-11-02. Spec `docs/specs/2026-11-02_lab-report-3.md`, section A3 (approved by Andrew 2026-11-02); task c023, dispatcher inbox item 43. Committed before any evaluation code runs. Nothing below changes after the first result is seen.

## Question
- Does the dispatcher agent finish a full batch as well as the fixed script under job failures, preemption, a cluster budget and a persistent fault, inside the same engine limits?
- Agent behaviour only. No real job; no lab server, no cluster. VM only

## Task set
- The 102 include-yes roots of `manifest/root_manifest.csv` and their usable windows: 1189 windows of 2 h (last window kept if at least 1 h), 51.1 core-hours in total
- Timing model: `config/dispatcher.yaml` `timing` (from `results/2026-10-23_tracker_timing/`): 1.04 core-s per frame, 2 copies per window; cluster $0.012 per core-hour
- Backend: `agents/dispatcher.py` `FakeQueue` (minutes of simulated time; lab jobs single-thread, at most 4 workers, load rule; cluster jobs 8 cores each). Lab-server load is constant at 1.0 of 32 cores (never pauses). A crashed job ends at half its run time

## Scenarios (seeded; same draws for both methods)
- Fault draws are made per window and per attempt before the batch starts, from `random.Random("<scenario>-<seed>")`: attempt k of window w fails or not, the same whichever method submits it and whenever
- S0: no failures
- S1: each job attempt crashes with probability 0.10
- S2: each job attempt crashes with probability 0.25; plus one preemption burst at a seeded minute, uniform in [60, 300]: every job running at that minute fails then (cause `preempt`) and must be retried
- S3: S1, plus an approved cluster budget of 70 % of the full batch: 35.77 core-hours ($0.43)
- S4: no random failures; one root, drawn from the 102 by the seed, whose every job attempt crashes (persistent fault)
- Seeds 0-4 for each scenario. 25 scenario-seed pairs

## Methods
- Dispatcher agent: `run_agent_batch` (`agents/dispatcher.py`), prompt `agents/prompts/dispatcher.md`, model and CLI pinned in `config/models.yaml` (step_limit 4 actions per round). One run per scenario-seed pair
- Fixed script: `run_script_batch` as it stands: split every root, submit all to the lab server in manifest order, poll every 30 min, collect, retry a failed window once, then give up on it. Deterministic, one run per pair
- S3 only, the script uses the budget by a fixed rule: in manifest order, a root's pending windows go to the cluster if their core-hours fit the budget left, else to the lab server; a retry that the budget refuses goes to the lab server. Otherwise as above
- Same engine for both: include-yes rows and windows only, 4 lab workers, the cluster only inside the approved budget, at most 2 retries per window (`retries_per_task`; the script's own rule is 1)
- Approval requests: in this evaluation the harness answers every `request_approval` with "no change" (budget unchanged) and the batch goes on; the next view shows the answer. Counted per batch. The default batch loop (stop and wait for Andrew) is unchanged

## Metrics (computed in code from the engine)
- Simulated time to finish, h (engine clock when the batch ends)
- Windows collected / 1189
- Retries used (resubmits)
- Jobs wasted on the persistent-fault root (S4): job starts for that root's windows
- Budget overrun: cluster core-hours used above the approved budget (must be 0); budget requests made
- Rounds and LLM calls per batch (calls from the dispatcher trace)
- Batch end status: finish, round limit, error

## Caps and order
- At most 200 dispatcher rounds per batch (`round_limit`); at most 60 agent batches in total, including any rerun after a CLI error
- Free VM memory at least 3 GB before each batch; wait otherwise
- Order: S0 to S4, seeds 0-4 within each. Each batch writes its metrics file when it ends; a restarted run skips finished batches. Status after each scenario

## Output
- `results/2026-11-02_dispatcher_eval/`: README with one table per scenario and method (median and range over the 5 seeds); `batches.csv`, one row per batch with every metric. Dispatcher traces stay in `staging/c023/` (git-ignored, large)

## Not in scope
- Real tracking times at 1000 px, real failure rates, lab-server load from other users
- Tuning the prompt or settings on these results
