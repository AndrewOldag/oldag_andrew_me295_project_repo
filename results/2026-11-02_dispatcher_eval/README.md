# Dispatcher agent vs fixed script on the fake queue (task c023)

Spec `docs/specs/2026-11-02_lab-report-3.md` A3; dispatcher inbox item 43. Proposal `docs/proposals/2026-11-02_dispatcher-eval.md` (committed before any run, 10d74c1). No real job; VM only.

## Setup
- 102 include-yes roots, 1189 windows of 2 h, 51.1 core-hours; timing model `config/dispatcher.yaml` (from `results/2026-10-23_tracker_timing/`); `FakeQueue`, 4 lab-server workers, cluster jobs 8 cores
- Scenarios, seeds 0-4, fault draws per window and attempt shared by both methods: S0 no failures; S1 10 % of job attempts crash; S2 25 % crash plus one preemption burst (minute 60-300); S3 S1 plus an approved cluster budget of 35.77 core-hours (70 % of the batch); S4 one root whose every attempt crashes
- Dispatcher agent: `claude-opus-5-5`, Claude Code 2.1.310, step_limit 4, 1 run per seed; approval requests answered "no change" (none were made)
- Fixed script: `run_script_batch` (lab server, poll every 30 min, 1 retry per window); in S3 the proposal's budget rule (cluster in manifest order while the budget lasts, then the lab server)

## Run
```
python scripts/dispatcher_eval.py run          # 25 script batches (37 s) and 25 agent batches; restarts skip finished batches
python scripts/dispatcher_eval.py report       # batches.csv and tables.md
```
- Agent batches started: 43 of the 60 cap. 18 did not count: 17 on 2026-11-02 and 1 on 2026-11-03 ended on the Claude seat's session limit ("hit your session limit"), not agent behaviour; set aside (`staging/c023/limit_errors/`, git-ignored) and rerun. The harness now stops the run on that message
- Traces in `staging/c023/traces/` (git-ignored)

## Results (median, range over 5 seeds; full tables in `tables.md`, every batch in `batches.csv`)
| Scenario | Method | Time to finish, h | Collected / 1189 | Retries | Rounds | LLM calls |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| S0 | script | 15 | 1189 | 0 | 31 | 0 |
| S0 | agent | 15 (15-15.25) | 1189 | 0 | 18 (17-19) | 42 (37-44) |
| S1 | script | 16 | 1177 (1168-1180) | 123 (113-141) | 33 | 0 |
| S1 | agent | 16.5 (16.25-16.5) | 1187 (1187-1188) | 136 (125-162) | 21 (20-22) | 67 (67-70) |
| S2 | script | 17.5 (17-17.5) | 1111 (1099-1117) | 299 (285-309) | 36 (35-36) | 0 |
| S2 | agent | 18 (18-18.25) | 1168 (1160-1178) | 381 (357-391) | 23 (22-25) | 73 (72-78) |
| S3 | script | 6 (6-6.5) | 1175 (1170-1181) | 110 (93-135) | 13 (13-14) | 0 |
| S3 | agent | 6.5 (5.75-9) | 1188 (1185-1189) | 126 (101-149) | 15 (13-17) | 47 (39-52) |
| S4 | script | 15 | 1177 | 12 | 31 | 0 |
| S4 | agent | 15.5 (15.5-16) | 1177 | 24 | 19 (17-20) | 42 (40-46) |

- Every batch of both methods ended with `finish`. Budget overrun 0 in every batch; 0 budget requests by the agent in every scenario, including S0-S2 with no budget
- S3: the agent used 22.1-32.2 of 35.77 cluster core-hours (script 31.9-33.0); one cluster submit was refused by the engine (seed 2), none went over
- S4: jobs on the persistent-fault root: script 24 (12 windows x 2 starts), agent 36 (12 x 3) on every seed. The agent retried the root until the engine gave up on each window; its rationales call them "the 12 failed windows" to retry and do not name a persistent fault

## Reading
- The retry rule differs and is fixed by the proposal: the engine allows the agent 2 retries per window; the script's own rule is 1. Windows collected in S1-S3 are higher for the agent, and retries and S4 wasted jobs are higher, mainly for this reason. This is not evidence of better scheduling
- Time to finish, median: agent equal to the script in S0, 0.5 h slower in S1-S4. The extra retry wave is a likely cause (not measured separately). In S3 the agent's range is wider (5.75-9 h); the 9 h seed used the least cluster time (22.1 core-hours)
- The agent ends a batch in fewer rounds than the script's 30 min polls, at 37-78 LLM calls per batch
- Within the engine's limits: no budget overrun and no budget request in any batch; one cluster submit refused by the engine (S3 seed 2)

## Known limits
- Simulation only: timing model of 2026-10-23, constant lab-server load, fixed crash probabilities
- One agent run per seed; no repeat runs
- The script baseline with 2 retries was not run (not in the proposal)
