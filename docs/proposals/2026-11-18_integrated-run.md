# Proposal: integrated run over every include-yes root, with the remedy tree and fixed script as baselines (task c027)

Spec `docs/specs/2026-11-18_lab-report-4.md`, section B (Andrew, 2026-11-18). Dispatcher inbox item 46. Committed 2026-11-20, before any run. No stop for approval. Nothing here changes after the first result is seen.

## Windows
- The 102 include-yes rows of `manifest/root_manifest.csv`, split by the fixed-script dispatcher into their usable windows: 1,189 windows (`python scripts/run_all.py windows`). The split equals the windows of the two batch runs: 126 of batch 1 (`results/2026-10-25_full_batch_1/`), 1,061 of batch 2 (`results/2026-10-25_full_batch_2/`), and the 2 windows of 0727_cc7, which no batch measured
- Base track of each window: the batch track (1000 px, stride 1, ft2 net midline), copied from storage to the VM cache with md5 checks (`run_all.py fetch`). A window has the whole-pixel moved copy (rigid invariance) where its batch run had one: 11 batch-1 and 85 batch-2 windows
- Windows with no batch track (3 batch-1 and 34 batch-2 tracker errors, 0727_cc7) start paused. The 36 batch-2 ones enter like any other window once real-calib's fixed tracks are cached (spec C3)
- A new run. The batch-1, c022, c023 and c026 results are kept and not overwritten

## Methods
Same windows, same cache, same remedy executors (`agents/executors.py` Slice, `measure/remedies.py`), same checker and real profile: closure gates at 19 px/h (`config/checker_thresholds_real.yaml`); rigid invariance and plane sections reported, not gating. No change to prompts, thresholds, remedies or the real profile.

1. Integrated (`scripts/run_all.py run`): fixed-script dispatcher (`agents/dispatcher.py` `run_script_batch`, manifest order) -> cached track -> checker -> decline by rule if a gating check is not computable (decisions 2026-10-26) -> diagnostician on every failing window (model `claude-opus-5-5`, Claude Code 2.1.310, step limit 8) -> auditor per root over its accepted windows once every window of the root is final. A root with no accepted window gets no auditor call
2. Remedy tree (`run_all.py tree`): `agents/baselines.py` `run_tree`, step limit 8, on every window whose first check fails, through the same cache. The c026 tree records stand for the 38 windows it reached; the tree runs on the rest
3. Fixed script: no remedy; closure fail -> decline. Read from the first check of each window; no run

## Cluster path (spec A)
- No agent or tree step waits on the cluster. A remedy whose track is not cached pauses the window: record `paused: needs <settings tag>`, trace set aside in `paused/`, settings appended to `paused.jsonl`. The window reruns from step 0 once its tracks are cached. A paused trace is not scored
- Missed settings go into the next `scripts/retrack_queue.py submit` (`jobs --paused RUN_DIR`). Wave 1 covers every single remedy on the base settings of the 84 batch-2 failing windows: 461 jobs, worst case $1.674 (`staging/c027/wave1.csv`)
- Stop and Needs Andrew if the projected cluster spend since 2026-10-23 passes $12 (ledger figure before wave 1: $7.405, with one job after it of worst case $0.012)

## Caps and order
- LLM calls: 900 in total for the diagnostician and the auditor. A diagnostician window starts only if the calls so far plus 8 plus 5 per root not yet audited stay within the cap; an auditor run starts only if the calls so far plus 10 stay within it. Calls in paused and set-aside traces count
- A trace with the seat's session-limit message is set aside, not recorded, and the run stops; it reruns on the next start (as in c023)
- At most 2 LLM runs at once on the VM (this run and compound's). Free VM memory at least 3 GB before each window
- Windows run in dispatcher order. Restartable: a window with a final record is skipped
- Results READMEs pushed by Sat 21 Nov 20:00 local. At the cut-off: an auditor pass over roots whose paused windows remain (`run_all.py audit --final-now`, over their final windows; marked in the record). Whatever has finished is reported; paused windows are listed as paused at the cut-off

## Fresh end-to-end demo (B5)
- Root: the first in manifest order with at least one passing and one failing batch-2 window and no tracker error
- From the montage images, no cache: midline net (cluster GPU, V100 or lower) -> QC -> track -> checker -> agents -> auditor. Wall time per stage; outcomes compared with the cached run window by window
- Run only when the cluster master is up and after wave 1 is submitted

## Metrics (computed in code, `run_all.py report`)
- Per method: accepted, accepted after a kept remedy, declined (by rule, by check, by agent), step limit, errors, paused at the cut-off; per condition and per experiment
- Diagnostician vs tree agreement per window (same outcome; same remedy kept); disagreement list with closure before and after each remedy
- Remedies tried, kept, rolled back; auditor flags; LLM calls, tokens, time; cluster jobs and spend
- Failure modes from the run: every tracker error, decline by rule, step limit, paused window, rolled-back remedy that made closure worse, auditor flag and link-down event, each with count and one example window. Synthetic findings from section C in separate rows
- Real windows have no ground truth. "Recovered" means the checker passes after a kept remedy; nothing more

## Outputs
- `results/2026-11-18_integrated_run/`: README (setup, one command per step, tables, failure modes, known limits), `windows.csv` (outcome and check values only), `example_traces.md` (one accepted after repair, one declined by the agent, one auditor flag). REGR, growth-zone and flank values masked as `[masked]`
- Records, traces and the cache stay in `staging/c027/` (git-ignored)
- Status pushed after every 100 windows
