# Spec: auditor v1 on the scored runs, real-movie frame-quality labeling set, no deletes on the lab server

From: planning account. Date: 2026-10-13. Status: open. Decisions by Andrew on 2026-10-13, on the scored-v1 log entry and `results/2026-10-12b_scored_v1/README.md`.

Two tasks, two sessions, run in parallel:
- Task A, auditor v1: branch `wip/auditor-v1`. No tracker runs, no lab server use
- Task B, real-movie frame-quality labeling set: branch `wip/fq-real`. Reads from the lab server; writes nothing there

Start both only after the coordinator has merged `wip/scored-v1` into `main`. Branch from that `main`.

## Decisions
- No Claude session deletes, moves or renames any file or folder on the lab server, by any means (`rm`, `rmtree`, `unlink`, `rsync --delete`, `mv`, a script that does any of these). Andrew deletes on the server himself, at the end of the project. Exception: the lock files that `scripts/synth/sweep.py` creates and removes for its own sweep. Where a step would need a server delete (space limit, stale outputs), stop and tell Andrew. Deletes on the VM are unchanged (staged images, per `CLAUDE.md`)
- `second_root` held-out label stays not repairable. It was set before any agent run; changing it after the results would leak the held-out set. The 9 runs that applied `use_width_free_ratio` and accepted a good centre are reported as their own row: alternative repair, measurement within tolerance, fault named `width_change` (wrong name). They count neither correct nor false accept, as now
- For any new labelled set made after today, `use_width_free_ratio` is a fitting state in the label sweep. This is decided before those runs
- Real-movie `frame_quality` reference: from real 1 h windows that Andrew labels clean by eye, median and lowest over the clean ones, as for the synthetic reference. Fixed in config before any agent run on a real movie. Until then real movies run checker only
- Old shared code copies on the lab server stay in place (decision above)

## Task A: auditor v1 (`wip/auditor-v1`)

Role, from `CLAUDE.md` and `docs/context/project_summary.md`: the auditor sees all roots of a batch but not the diagnostician's reasoning. Here a batch is the final records of one method on one set in `results/2026-10-12b_scored_v1/` (dev: 25 runs, held-out: 15 runs; 8 batches).

### A1. Auditor view (deterministic code, no LLM)
- `audit/view.py`: per run, build the record the auditor sees: status (accept, decline, not_reported), final checks (value, threshold, passed), remedies kept, roll backs, steps, final settings, and field summaries from the final measurement record: centre REGR peak and its position, growth-zone length (REGR above 10 % of peak), flank-difference largest value and position, width-free ratio when used
- Field summaries come from the cached final records. If a run's final record is not in the cache, stop and ask; do not start tracker runs for it
- Withheld from the view: fault, size, seed, label, truth, error_before, error_after, category, correct, good, named fault, traces. Test: no withheld key or value reaches the view (same form as the single-agent leak test)
- Batch statistics in code: per summary, batch median, MAD and robust z per run

### A2. Rule auditor (baseline, written before any LLM auditor run)
- Flags an accepted run if any final check failed, or if any summary has |robust z| > 3
- Write the rule in `docs/proposals/2026-10-13_auditor-v1.md` and commit before running it. The z cutoff 3 is provisional; list it for Andrew

### A3. LLM auditor
- Typed actions through the existing orchestrator, as for the diagnostician: `request_info` (kinds: `batch_table`, `run_record`), `flag` (run id, reason from a fixed list, evidence fields), `clear` (run id), `report` (batch text). Reasons: `check_failed_but_accepted`, `summary_outlier`, `remedy_pattern`, `width_free_ratio_used`, `other`. Every accepted run ends flagged or cleared
- Prompt `agents/prompts/auditor.md`. Model and Claude Code version as in freeze v2. Step limit 20 per batch
- Write the definition (view, actions, prompt, step limit) into the same proposal and commit before any held-out batch run

### A4. Runs and scoring
- Develop the prompt on the 4 dev batches only. At most 40 auditor calls on dev
- Then commit the prompt, record the commit, and run the 4 held-out batches 3 times each (12 runs). No prompt change between held-out runs
- Score per batch: false accepts flagged / false accepts; good reports flagged / good reports (false flags); `second_root` alternative-repair runs flagged, reported apart. Same for the rule auditor
- Results in `results/2026-10-13_auditor_v1/`: table per method and set, both auditors, tokens and call time per run
- Known limit, state it in the results: on dev only the script batch has false accepts (10); on held-out, script 12 and remedy tree 3

### A5. Out of scope for v1
- Control vs stressed comparison (synthetic batches have no condition). Next step on real movies
- No change to anything in freeze v2

## Task B: real-movie frame-quality labeling set (`wip/fq-real`)

Goal: a labeling set on the VM for Andrew, then the real reference once he has labelled it.

### B1. Pick windows (manifest only, no images yet)
- From `manifest/root_manifest.csv`, 1 h windows, spread over the five experiments and over 0-24 h:
  - 20 windows from control roots with `include` yes, inside the usable hours
  - 10 windows likely poor: roots with `include` no, or notes or flags that point to image problems (dark region, focus, debris)
- 30 windows in all. Window ids `fq01`-`fq30` in shuffled order, so the id does not show why a window was picked
- Write the window list with root, hours and reason to `private/fq_real_candidates.csv` (git-ignored). Not in any tracked file

### B2. Pull frames (read-only on the server)
- 3 frames per window (start, middle, end of the hour), from the image folder the tracker uses for real movies. 90 frames
- Copy with `scp` or `sftp`, bandwidth capped, lowest priority, load checked before starting as for the data steward. One transfer from the server at a time: if the data steward's transfer is running, wait for it to finish
- Nothing written, moved or deleted on the server
- Check `df` first; stop at 5 GB used by this task
- Into the main repo folder, git-ignored: `staging/fq_real_labeling/`
  - `frames/<id>_{a,b,c}.<ext>`: the original frames
  - `view/<id>.png`: the 3 frames side by side, contrast as stored (no auto-levels), downscaled to fit a screen
  - `labels.csv`: columns `id`, `label` (empty; Andrew writes `clean`, `not_clean` or `unsure`), `note`
  - `HOW_TO_LABEL.txt`: label each window by eye from `view/`; clean means texture and focus good enough to track the whole growth zone

### B3. Compute values, hidden from the labeling
- `frame_quality` (texture_contrast, focus) per frame, same code as `measure/info.py`, into `private/fq_real_values.csv`. Not shown in `view/` or `labels.csv`
- Log entry: where the set is, how many windows and frames, size on disk. Then stop: Andrew labels

### B4. After Andrew labels (same branch, when he says the labels are done)
- Reference = median and lowest of each measure over the frames of windows labelled `clean`. `unsure` windows are left out
- Report separation: values for `not_clean` windows against the clean lowest, per measure. If any `not_clean` window is above the clean lowest on both measures, or any `clean` window falls below the synthetic lowest, report it and stop and ask
- Add a `real:` section to `config/frame_quality_reference.yaml` (basis line, median, lowest). `measure/info.py` gives the `real` reference for records from real movies and the synthetic one for synthetic rods. Test both
- Numbers may be committed. Images, root paths and the candidate list may not

## Limits
- Task A: no tracker runs; at most 52 auditor calls
- Task B: read-only on the lab server; at most 5 GB on the VM
- Stop and ask: a step needs a server delete; a final record is missing from the cache (A1); labels done but separation fails (B4)
- Logs: `docs/running_log_pending/auditor-v1.md` and `docs/running_log_pending/fq-real.md`
