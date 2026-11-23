# Integrated run over every include-yes root, with remedy tree and fixed script (task c027)

Spec `docs/specs/2026-11-18_lab-report-4.md`, section B; proposal `docs/proposals/2026-11-18_integrated-run.md` (committed before any run, cf10046). Run 2026-11-20 to 2026-11-23.

## Setup
- Windows: the 102 include-yes roots of `manifest/root_manifest.csv`, split by the fixed-script dispatcher into 1,189 usable windows
- Base track per window: the batch track (1000 px, stride 1, ft2 net midline), from storage to the VM cache with md5 checks. Missing base tracks and every remedy track were retracked on cluster CPU nodes through Slurm arrays (`scripts/retrack_queue.py`)
- Checker: real profile; closure gates at 19 px/h; rigid invariance and plane sections reported, not gating. Closure not computable -> decline by rule
- Integrated: diagnostician on every failing window (step limit 8); auditor per root once all its windows are final
- Remedy tree: `run_tree`, step limit 8, on the windows the diagnostician saw. Its 38 c026 records were rerun here (register v2, integrity gate; spec 2026-11-20)
- Fixed script: no remedy; closure fail -> decline
- Integrity gate (option A, Andrew 2026-11-21) on every remedy step of the diagnostician and the tree: a remedied track vs its own base track, k from `config/integrity_relative_k.yaml`; fail -> roll back
- Registration remedy: register_v2 only; no register v1 track reused
- LLM cap: 900 calls at the start; raised to 1,300 on 2026-11-23 at 782 calls (dispatcher inbox item 59; README "LLM call cap"). Prompts, gate, thresholds, methods and windows unchanged

## Run
```
python scripts/run_all.py windows
python scripts/run_all.py fetch
python scripts/run_all.py run --out staging/c027/run --llm-cap 1300
python scripts/run_all.py tree --run staging/c027/run --out staging/c027/tree
python scripts/run_all.py report --run staging/c027/run --tree staging/c027/tree --out results/2026-11-18_integrated_run --demo staging/c027/demo --roots 0708_c4
```
- Retracks: `python scripts/retrack_queue.py submit` / `fetch` (README, task c027). Records, traces and tracks in `staging/c027/` (git-ignored). A rerun skips finished windows

## Result (`tables.md`, `windows.csv`)
| method | accepted | accepted after repair | declined by rule | declined by check | declined by agent or tree | step limit | paused |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| integrated | 1034 | 2 | 58 | 0 | 85 | 6 | 4 |
| remedy tree | 1034 | 12 | 58 | 0 | 78 | 0 | 7 |
| fixed script | 1034 | 0 | 58 | 93 | 0 | 0 | 4 |

- "Accepted after repair" means the checker passes after a kept remedy. Real windows have no ground truth: it does not say the repaired measurement is right
- Diagnostician vs tree, 90 windows with both final: same outcome 74, same final kept settings 69. The 16 disagreements, with closure before and after each remedy, are in `tables.md`. In 10 the tree accepts after light midline smoothing or a disk-radius change where the diagnostician declined; in 6 the diagnostician hit its step limit and the tree declined
- Remedies tried: diagnostician 73 (kept 4, rolled back 69); tree 352 (kept 27, rolled back 325)
- LLM use: 1,007 calls in the main run (diagnostician 358 on recorded windows, auditor 439 over 99 roots; the rest in paused and set-aside traces). Auditor flags: 240
- Cluster: 616 retrack tasks in 47 arrays (fetched 576, failed 28, done 12). Spend $8.248 of $15 before the demo GPU job; demo job worst case $0.252

## Fresh one-root demo (B5, `demo.md`)
- Root 0708_c4 from its montage images: staged to the cluster, one P100 job (midline net, QC, track, checker), collect with md5, base tracks fetched fresh; agents and auditor with `--llm-cap 293` (1,300 - 1,007)
- Remedy tracks of the 2 failing windows came from the c027 cache (decision 2026-11-23); base tracks and checks are fresh
- Same outcome as the cached run in 12 of 12 windows; closure values equal to 2 decimals. Auditor flags the same run (r07, summary outlier) and clears the same 9; its wording differs. Diagnostician took a different remedy path on 0708_c4 0-2 h (2 vs 3 remedies) with the same outcome (step limit)
- Wall time: staging 2.6 min; cluster job and collect 27.8 min (queue wait included); fetch 0.1 min; agents and auditor 3.5 min

## Failure modes (`failure_modes.md`)
- Counted from the run records, the queue and its log: tracker errors, windows no batch measured, declines by rule, step limits, paused windows, remedies that made closure worse before roll back, auditor flags, failed retrack tasks, link down
- Paused at the run's end, 4 integrated windows: 0708_m9 10-12 h (register_v2 retrack failed twice), 0721_m5 0-2 h (no base track), 0727_cc7 0-2 and 2-4 h (no batch measured it). The tree has 3 more: 0708_m1 10-12 h, 0714_c9 10-12 h, 0727_cc6 10-12 h (their retracks failed twice; for 0714_c9 the staged window had no stage-position file). A task that fails twice is not requeued
- 28 failed retrack tasks: the last line of each cluster error is in `failure_modes.md`, folders dropped
- Synthetic findings (spec section C) are in the c029 and c030 results

## Example traces
`example_traces.md`: one window accepted after repair (0714_m7 18-20 h), one declined by the agent (0708_c10 0-2 h), one auditor flag. REGR, growth-zone and flank values masked as `[masked]`

## Known limits
- Real-movie profile: closure is the only gate. Rigid invariance needs a moved copy, which most windows lack
- The tree's remedy list starts with registration, which often raises closure before roll back; the start of the registration band comes from the failing window's own profile
- 3 roots have paused windows and no auditor run yet (0708_m9, 0721_m5, 0727_cc7). At the cut-off (Thu 26 Nov 12:00) `run_all.py audit --final-now` audits them over their final windows
- LLM cap raised mid-run (above). Session-limit stops were set aside and rerun, not recorded
- The demo reused cached remedy tracks for its 2 failing windows, so only the base path is fresh end to end
