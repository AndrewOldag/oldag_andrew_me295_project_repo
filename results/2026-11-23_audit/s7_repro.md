# Section 7: reproducibility of results README commands

Scope: every folder under `results/` except `2026-11-23_audit` (47 folders, 45 with a README). For each, the commands given were read and checked against the scripts at HEAD of `wip/audit`: script path tracked, subcommands and flags in `--help` (agents env `me295`; 47 scripts plus 11 subcommands, each under 1 min, no network, LLM, cluster or tracker), inputs tracked or git-ignored, outputs written, environment named. Nothing that does real work was run, except three pure checks listed at the end.

Classes:
- R = reproducible from repo (repo, agents env and the Claude Code setup steps of `README.md` only)
- E = needs stated external inputs (tracker, tracker host, cluster, staged or cached data, `private/` config). `E*` = the results README does not state that the inputs are external (S7-5)
- B = broken: the command fails or does something else as written
- N = no command given

Counts: R 4, E 34 (of which E* 11), B 3, N 6.

| Folder | Class | Note |
| :-- | :-- | :-- |
| 2026-10-09_action_schema | R | `scripts/cli_probe/test_action_schema.py` exists, no flags needed; needs Claude Code (setup) |
| 2026-10-09_demo_diagnostician | N | No README (S6-3) |
| 2026-10-09_safe_mode_mcp | R | Both probe scripts exist; `--variant` exists; needs Claude Code |
| 2026-10-10_checker_synthetic | B | `run_batch.py` given with no arguments; `--work` is required (S7-1). Tracker machine stated |
| 2026-10-10_demo_slice | E* | `demo_slice.py --fault` valid; default runner `remote` needs tracker host and `private/runner.yaml`, not stated; default `--out` is `results/<today>_demo_slice` (S7-4); no command for `remedy_sweep.jsonl` (S7-8) |
| 2026-10-10_repair_criteria | E* | `repair_sweep.py start/status/fetch`, `eval_repair.py --out` valid; tracker host and `private/runner.yaml` not stated; `eval_repair` reads `staging/tracks` by default |
| 2026-10-10_width_rotation | B | `run_batch.py` lacks required `--work`, and lacks `--seeds 0 1 2` and `--moved-too` for the runs described (S7-1) |
| 2026-10-11_remedy_fixes | E* | `fix_sweep.py start/status/stop/fetch --part`, `eval_fix.py --out` valid; tracker host not stated (machine described, config not) |
| 2026-10-11b_padding_tolerance_coupling | E* | Parts `b_smooth`, `b_weight` valid for both scripts; tracker host not stated |
| 2026-10-11c_world_smoothing_freeze | E | Parts valid (`c_smooth`, `c_bent` sweep; `c_smooth`, `c_tolerance` eval); RemoteRunner and cache stated |
| 2026-10-12_baselines | E | `baselines.py next/status/fetch/write --out`, `eval_baselines.py --runs --agent-runs --out` valid; both input folders tracked; staging stated |
| 2026-10-12_freeze_v2 | E | `freeze_sweep.py --part seeds35/seeds35_reg`, `eval_freeze.py --parts relabel seeds35`, `demo_slice.py --size --seed --out` valid; test file exists |
| 2026-10-12_heldout_faults | N | No README (S6-3) |
| 2026-10-12b_heldout_labels | E* | `heldout_labels.py start/status/fetch/eval --out` valid; tracker host not stated |
| 2026-10-12b_scored_v1 | E | All subcommands and `--set`, `--method` valid; staging cache stated |
| 2026-10-13_auditor_v1 | E | `views/rule/llm/eval`, `--set`, `--method`, `--repeat` valid; reads staging caches (cache stated) |
| 2026-10-23_autotrace | N | No command; no script named (S7-8) |
| 2026-10-23_freeze_v3 | E | Points to `README.md` section "Freeze v3 scored runs"; section exists; its subcommands and `--phase` values match `scored_v3.py --help` |
| 2026-10-23_host_setup | N | Describes tracker runs on a second host; no repo command (S7-8) |
| 2026-10-23_midline_fit_validation | E* | Flags valid; `--cache <freeze-v3 tracker cache>` placeholder, location (`staging/tracks_freeze_v3/`) not stated |
| 2026-10-23_real_slice | E | Flags valid; needs `private/real_runner.yaml` and compute host (stated); default `--out` is `results/<today>_real_slice`, not this folder (S7-4) |
| 2026-10-23_real_slice_noagent | E | `--no-agent --out` valid; compute host stated; `private/real_runner.yaml` implied by default |
| 2026-10-23_tracker_timing | R | `estimate.py` rerun: output identical to `estimate.md`. Timing runs themselves need the remote driver (stated) |
| 2026-10-24_closure_ft_vs_ft2 | E* | `--net NAME TRACK NETMID` valid; inputs are placeholders for cached tracks, location not stated |
| 2026-10-24_freeze_v3.1 | N | Driver named only; no command and no pointer to the `README.md` section (S7-8) |
| 2026-10-24_real_slice | E | Flags valid; compute host stated; first command writes `results/<today>_real_slice`, second audits the tracked folder and overwrites its auditor files (S7-4) |
| 2026-10-24_real_slice_3roots | E | Flags valid; `private/real_runner_lab.yaml` not in main `private/` (S7-6) |
| 2026-10-24_real_slice_3roots_c2 | E | As above (S7-6) |
| 2026-10-24_real_slice_closure_gate | E* | `--out` valid; private config, compute host and movies not stated |
| 2026-10-24_rigid_cause_test | E* | Script defaults valid; reads `staging/tracks_real` by default, not stated; `real_moved.py --shift-scale`, `--pad` valid |
| 2026-10-24_rigid_whole_pixel | E* | Flags valid (`real_moved.py --mode whole_pixel`); host not stated; step 1 depends on the code before the rule commit (S7-11) |
| 2026-10-24_rigid_window | E | Points to rigid_whole_pixel README for the command (step 2) |
| 2026-10-25_closure_definition | E | `closure_v3_validate.py`, `net_tip_points.py` (argv), `closure_base_test.py` flags valid; `closure_definitions.py --track` form (S7-10); `private/closure_runner_lab.yaml` not in main `private/` (S7-6) |
| 2026-10-25_freeze_v4 | E | Points to `README.md` section "Freeze v4 candidate"; subcommands match `scored_v4.py --help` |
| 2026-10-25_full_batch_1 | E | `full_batch.py run --config`, `summary` valid; lab server and git-ignored `staging/full_batch_1/` stated |
| 2026-10-25_full_batch_1_agents | E | Flags valid (`--moved-span`, `--min-free-gb`, `--rescore`); `<126 windows>` placeholder; staging stated; `private/real_runner_c022.yaml` not in main `private/` (S7-6) |
| 2026-10-25_full_batch_2 | N | No command; `README.md` has the driver and `full_batch.py summary --batch 2` (S7-8, S7-9) |
| 2026-10-25_real_calibration | E | `real_calib.py run --config --replacements --ext --fallback`, `summary` valid; lab server stated |
| 2026-10-25_real_subset | B | `real_subset_report.py --run` and `real_subset_agreement.py` read `summary.json` from folders not in the tree (S7-2); rerun writes traces into a non-ignored results folder (S7-3) |
| 2026-11-02_dispatcher_eval | R | `run`, `report` valid; FakeQueue, VM only; needs Claude Code |
| 2026-11-02_rag | E | `build/gold/retrieval/run --repeat 1-3/report` valid; corpus in git-ignored staging stated; `rag/gold.yaml`, `rag_corpus.csv` tracked |
| 2026-11-12_batch2_agents | E | `fetch`, `tree --out --stop-at`, `report --tree --agents --out` valid; report tolerates the missing agents folder; staging and cluster stated; default config `private/real_runner_c026.yaml` not in main `private/` (S7-6) |
| 2026-11-18_auditor_check | E* | `plan/views/rule/llm --repeat/score` valid; needs `staging/tracks_freeze_v4/`, stated in `README.md` only; results README says "VM only, no tracker runs" |
| 2026-11-18_heldout_compound | E | Subcommands valid; `compound_queue.py` given without folder (it is `scripts/synth/`); cluster stated |
| 2026-11-18_integrated_run | E | `run_all.py` subcommands and flags valid; staging/c027 (S4-3); default config `private/real_runner_c027.yaml` not in main `private/` (S7-6) |
| 2026-11-20_arange_fix | E | `check_after_fix.py --tracks`, `check_window.py --window --track --out` valid; tracker and tracks are placeholders, stated; test passes (5 passed) |
| 2026-11-20_registration_fix | E | `integrity_thresholds.py thresholds/report/relative/pairs` flags valid; tests in agents env pass (30 passed); tracker env stated for the register test |

## Findings

### S7-1 (major) Synthetic rod batch commands omit a required flag
- Where: `results/2026-10-10_width_rotation/README.md:14`; `results/2026-10-10_checker_synthetic/README.md:14`
- Evidence: `scripts/synth/run_batch.py:19` has `--work` with `required=True`, also at 4188ad8 (2026-10-10). Both READMEs give the command without `--work`, so argparse exits with an error. width_rotation describes 3 seeds, each tracked twice (as rendered and moved); the command also lacks `--seeds 0 1 2` (default `[0]`) and `--moved-too`. checker_synthetic gives `run_batch.py` with no arguments at all
- Fix: give the full command with `--work <dir>`, `--seeds`, `--moved-too`, the case and fault flags, and state that it runs with the tracker env on the tracker machine

### S7-2 (major) Real-subset report and agreement commands read files that are not in the tree
- Where: `results/2026-10-25_real_subset/README.md:16` and `:61`
- Evidence: `scripts/real_subset_report.py:48` reads `<run>/summary.json`; `scripts/real_subset_agreement.py:25` reads `summary.json` in each run folder. `git ls-files results/2026-10-25_real_subset` lists no `summary.json` and nothing under `run2/` or `run3/`; the README says they were taken off the public tree and are in git history and a staging copy. Both commands fail with a missing file as written, even with the staging copy present
- Fix: point `--run` and the agreement arguments at the staging copy (or at a checkout of the named commits), and write the report output to the results folder with an explicit option

### S7-3 (minor) Rerunning the real-subset agent command writes traces into a non-ignored results folder
- Where: `results/2026-10-25_real_subset/README.md:15` (also the `--cached-only --out .../runN` repeats in `README.md:100`)
- Evidence: the command writes `summary.json` and agent traces to `results/2026-10-25_real_subset`. The same README says these files stay off the public tree because the auditor text quotes field values. `git check-ignore` matches neither `results/2026-10-25_real_subset/summary.json` nor `run2/summary.json`, so a rerun leaves them untracked but committable
- Fix: `--out staging/...` as in full_batch_1_agents, then the report step to the results folder

### S7-4 (minor) Date-based default outputs: commands do not write to the folder they document
- Where: `results/2026-10-23_real_slice/README.md:3`; `results/2026-10-24_real_slice/README.md:3`; `results/2026-10-10_demo_slice/README.md:6`
- Evidence: `scripts/real_slice.py:213,218` and `scripts/demo_slice.py:57` default `--out` to `results/<today>_...`. Run on any later day, `python scripts/real_slice.py` writes a new folder. For 2026-10-24 the second command (`--audit-only --out results/2026-10-24_real_slice`) then reviews the old tracked batch, not the new run, and overwrites the tracked `auditor_trace.jsonl` and `summary.json`. For 2026-10-23 the `--audit-only` command without `--out` reviews the new folder
- Fix: give `--out results/<folder>` on every command, or state that reruns go to a new dated folder

### S7-5 (minor) External inputs not stated in 11 results READMEs
- Where: demo_slice, repair_criteria, remedy_fixes, padding_tolerance_coupling, heldout_labels (tracker host and `private/runner.yaml`); midline_fit_validation, closure_ft_vs_ft2, rigid_cause_test (cached tracks in `staging/`, location not given); real_slice_closure_gate, rigid_whole_pixel (private runner config, compute host, movies); auditor_check (`staging/tracks_freeze_v4/`, stated only in `README.md:89`)
- Evidence: per-folder notes in the table. Each command's flags are valid, but the README does not say what must exist outside the repo
- Fix: one "Needs" line per README naming the host, config and cache folder, or a pointer to the `README.md` section that does

### S7-6 (minor) Private configs named by commands are not in the main `private/` folder
- Where: `results/2026-10-24_real_slice_3roots/README.md:3`, `..._3roots_c2/README.md:3` (`private/real_runner_lab.yaml`); `results/2026-10-25_closure_definition/README.md:58` (`private/closure_runner_lab.yaml`); `results/2026-10-25_full_batch_1_agents/README.md:14` (`private/real_runner_c022.yaml`); script defaults `scripts/batch2_agents.py:219` (`real_runner_c026.yaml`), `scripts/run_all.py:46` and `scripts/retrack_queue.py:46` (`real_runner_c027.yaml`)
- Evidence: none of these five files is in the main repo `private/`; each exists only in a session worktree's own `private/` under `.claude/worktrees/` (git-ignored). A worktree cleanup removes them. Only `config/real_runner.example.yaml` serves as a template; the multi-config (`--config A B`) and closure-runner forms have none
- Fix: copy the configs to the main `private/` (Andrew), and name the template each one is built from in the README

### S7-7 (minor) Environment not named in 42 of 45 results READMEs
- Where: all results READMEs except `2026-10-23_host_setup`, `2026-11-20_registration_fix` (agents env and tracker env named) and `2026-10-23_tracker_timing` (folder name only)
- Evidence: grep for `agents env|me295|environment.yml|qb.yml|tracker env` per README. Several commands need the tracker env, not the agents env: `scripts/remote/real_midline.py` (needs `skimage`) and `scripts/remote/register_diag.py` (needs `cv2`) fail on import in `me295`; `run_batch.py` calls `scripts/remote/qb_track.py`
- Fix: one line per README, or one rule in `README.md`: scripts under `scripts/remote/` and tracker runs use `envs/qb.yml`, everything else `environment.yml`

### S7-8 (minor) No command for 4 READMEs and one output file
- Where: `results/2026-10-23_autotrace/README.md`, `results/2026-10-23_host_setup/README.md`, `results/2026-10-24_freeze_v3.1/README.md`, `results/2026-10-25_full_batch_2/README.md`; `results/2026-10-10_demo_slice/remedy_sweep.jsonl` (`README.md:7`). The two folders with no README are S6-3
- Evidence: autotrace names no script; host_setup names only the tracker's `qb_track.py --stride 1`; freeze_v3.1 names the driver only, with no pointer to `README.md` section "Freeze v3.1 sizing" (freeze_v3 and freeze_v4 do point to theirs); full_batch_2 names `scripts/remote/check_window.py` only, while `README.md:101` has the driver and summary commands
- Fix: add a Commands line or a pointer to the `README.md` section

### S7-9 (minor) The batch-2 summary command would drop the rows added after the arange fix
- Where: `README.md:101` (`python scripts/full_batch.py summary --batch 2`); `results/2026-10-25_full_batch_2/README.md:18`; `results/2026-11-20_arange_fix/README.md`
- Evidence: `scripts/check_after_fix.py` appends 33 rows with `checked_after_fix` yes to the tracked `results/2026-10-25_full_batch_2/windows.csv` (its rerun is idempotent: it drops and re-adds those rows). `scripts/full_batch.py` `summary` (line 194, writes `windows.csv` at line 230) has no `checked_after_fix` column and rewrites the file from the batch records, so running the documented summary after the fix removes the 33 rows without a message
- Fix: state the order (summary, then `check_after_fix.py`) in both READMEs, or make `summary` keep the column

### S7-10 (minor) `closure_definitions.py --track` form as written is rejected
- Where: `results/2026-10-25_closure_definition/README.md:57`
- Evidence: the README gives `--track ROOT TRACK.npz ...`. `scripts/closure_definitions.py:97` defines `--track` with `nargs=2, action="append"`: one root and track per flag. Further pairs after one `--track` are unrecognized arguments. Read from the source; not run
- Fix: write `--track ROOT1 TRACK1.npz --track ROOT2 TRACK2.npz ...`

### S7-11 (minor) Step-1 rigid invariance command needs the code before the rule commit; commit not given
- Where: `results/2026-10-24_rigid_whole_pixel/README.md:3`
- Evidence: steps 1 and 2 use the same command with a different `--out`; step 2 ran "after the rule was committed" (profile window, decisions 2026-10-24). At HEAD the step-1 command applies the rule, so it reproduces step 2, not step 1. The README names the tracker commit, not the course-code commit of step 1
- Fix: give the course-code commit for each step

## Checked, no finding
- Script paths named in results READMEs: 68 distinct `scripts/`, `measure/`, `agents/`, `audit/`, `results/` paths; 68 tracked, 0 missing. Plus `scripts/synth/compound_queue.py`, tracked
- `--help` on 47 scripts in the agents env: 45 exit 0; 2 fail on import, both `scripts/remote/` tracker-env scripts (S7-7)
- Subcommands and flags against `--help`: all subcommands and flags in the 45 READMEs exist, except S7-1 (missing required flag) and S7-10 (flag form); including subparser help of `full_batch.py`, `dispatcher_eval.py`, `rag.py`, `integrity_thresholds.py`, `sweep.py`
- Argv scripts without argparse: `net_tip_points.py` usage line matches the README; `real_subset_agreement.py` takes run folders
- Tracked inputs named in commands: `results/2026-10-11c_world_smoothing_freeze/diagnostician`, `results/2026-10-12_baselines/runs`, `results/2026-10-25_full_batch_2/audit/outputs.csv`, `rag/gold.yaml`, `docs/context/literature/rag_corpus.csv`, tests `test_record_tracker.py`, `test_integrity.py`, `test_executors.py`, `test_register_v2.py`, `test_info_p1_p5.py`: all tracked
- `README.md` sections referenced by freeze_v3 and freeze_v4 results READMEs: both exist; subcommands match the drivers
- `staging/` and `private/` are git-ignored (`.gitignore:3`, `:12`); `private/real_runner.yaml`, `real_runner_c018.yaml`, `real_runner_c019.yaml`, `real_runner_fb1.yaml` present in main `private/` (names only read)
- `python results/2026-10-23_tracker_timing/estimate.py`: stdout identical to the tracked `estimate.md` (line endings ignored)
- `python -m pytest tests/test_record_tracker.py`: 5 passed (arange_fix test command)
- `python -m pytest tests/test_integrity.py tests/test_executors.py`: 30 passed (registration_fix test command)
- `batch2_agents.py report` with no `staging/c026/agents/summary.json`: `scripts/batch2_agents_report.py:137` skips the agent rows; the documented command does not need the agents run that did not happen
- `check_after_fix.py` rerun: drops and re-adds its own rows, so the README's "a rerun writes the same file" holds
- Commands that write into their own tracked results folder (eval and report steps): intended reproduction in place; the LR3 demo case is S6-10
