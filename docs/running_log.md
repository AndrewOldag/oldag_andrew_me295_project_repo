# Running log

Required by the course. One entry per work session: done, remaining, bottlenecks.

## 2026-10-08
- Done: project summary final. Data uploaded to the lab server and verified. Build machine can reach the server. Shared repo created. Context files drafted
- Remaining: install Python on the build machine; Python environment on the server; install Quantum Borland there; data manifest; time one root
- Bottlenecks: cluster not reachable from the build machine directly; .imgdir count differs from root count

## 2026-10-08 (build account, session 2)
- Done: read all context files and summarized project and next steps. Miniforge 26.7.2-0 installed on the build machine and the lab server; installers checked against GitHub SHA-256 digests. Env `me295` (Python 3.12, numpy, scipy, pyyaml, pytest, anthropic 1.12.1) created on both. Added `environment.yml`, `config/models.yaml` (pinned `claude-opus-5-5`), `.env.example`, `scripts/check_api.py`, README setup section
- Remaining: Andrew sets `ANTHROPIC_API_KEY`, then run `scripts/check_api.py`. Andrew grants read access to the Quantum Borland repo, then clone it on the server and add its dependencies to the env. Confirm the remote copy is current
- Bottlenecks: Quantum Borland repo is private; neither machine has credentials. Windows Miniforge installer fails with "not writable" unless the target folder exists first
- Update, same session: Andrew added read-only access. Quantum Borland cloned on the server (HEAD 2c6cebd, 21 Aug 2026), installed in env `qb`. Its tests: 24 passed, 7 skipped (sample data not in repo). All five midline-cascade weight files load on CPU
- Remaining now: API key (Andrew's Console account shows no Billing page; likely a non-admin org seat, being checked)
- Update: Andrew pushed his Oct edits to the Quantum Borland repo (d5f1829, 8 Oct: coupling fixes, two-side pipeline, `root_kinematics/paths.py`, affine readout test). Pulled on the server. No dependency changes. Tests: 35 passed, 7 skipped (sample data absent). `paths.py` defaults to a local Windows layout; on the server set `QB_DATA_ROOT` and related variables or its config file before running
- Update: instructor says no API keys; agents must run through Claude Code under Andrew's Enterprise seat. Build machine CLI signed in. One test call with `claude -p --safe-mode --model claude-opus-5-5 --json-schema ...` succeeded; `modelUsage` showed only the pinned model. Code changes wait for approval
- Done: draft root manifest. `scripts/manifest/scan_imgdirs.py` (runs on the server, reads metadata and a few frames, writes nothing in the data folders) found 192 .imgdir in 123 root positions (the earlier inventory said 118; per-folder counts disagree: 23/19/28/25/28 found vs 10/28/24/28/28). Each position has a stitched Montage folder; drought positions also have a raw two-position folder. Outputs in `data/manifest/` (git-ignored). Review app: `scripts/manifest/open_review.bat` or `python scripts/manifest/review_server.py`, saves to `data/manifest/manifest_reviewed.csv`
- Found: 27 Jul roots each have one ~40 min gap (likely the transfer). 21 Jul `test1.dir` is empty. `0714_m6` has no montage. Two 21 Jul roots labelled 3DMontage. The context note's "2-tile montage" is right: raw folders alternate between two stage x positions 2.27 mm apart, stitched into 2400x1200 montages
- Remaining: Andrew reviews the 123 roots and confirms the c/m, cc/mc/mm meanings
- Done: Andrew reviewed all 123 roots in the review app: 101 keep, 14 unsure, 8 drop. Conditions left as guessed. Notes record second roots, growth out of frame or focus, lighting and banding artifacts, and roots hitting the chamber wall late in 27 Jul runs. Saved in `data/manifest/manifest_reviewed.csv` (git-ignored)
- Done: conditions confirmed; manifest committed as `manifest/root_manifest.csv` via `scripts/manifest/export_manifest.py` (validates answers and windows). Review app gained usable-window fields and a filter for notes that mention a time limit (20 roots).
- Remaining: Andrew fills usable windows, then re-run the export

## 2026-10-09 (planning account)
- Done: this GitHub repository set as the project repository. First commit holds code, setup, the root manifest, paper digests and directions. Machine names, paths, access details and other people's comments are kept out of the repo, in a git-ignored `private/` folder
- Remaining: build account points its remote at this repository; related-work note; draft proposal
- Bottlenecks: commit history from 8 Oct is not carried over; the log entries above cover that work

## 2026-10-09 (build account, session 3)
- Done: Andrew finished usable windows in the review app. `python scripts/manifest/export_manifest.py`: 123 roots, 102 keep, 9 with a usable window (0708_c12, 0708_c3, 0711_c8, 0714_m11, 0727_cc1, cc2, cc5, cc6, cc7). Three unsure roots settled: 0711_c9 and 0714_c3 dropped, 0714_m11 kept to 18 h. Earlier the same day: review app movie player with time stamps, one frame every 15 min per root, with Set start / Set end buttons that fill the usable window (`scripts/manifest/make_scrub.py`, `review.html`)
- Done: moved to this repository. New clone next to the old one; repo-local git identity set; private context and the git-ignored `data/manifest/` copied into `private/` and `data/`, both git-ignored. Old repository not pushed to
- Done: ported `make_scrub.py` and the player version of `review.html`, which were missing here, with machine paths removed. `open_review.bat` no longer names a Python path; it uses `ME295_PYTHON`, then the `me295` conda env, then `python` on PATH
- Demo: `python scripts/manifest/review_server.py`, then open http://localhost:8295; each card plays the root with elapsed time and fills the usable window
- Remaining: the CLI agent conditions (MCP tool test under `--safe-mode` first); replace `check_api.py` and the API-key README steps
- Bottlenecks: none open. The build account's command runner blocked shell commands in this clone until Andrew allowed them
- Done: CLI condition 1, safe-mode MCP test. `python scripts/cli_probe/test_safe_mode_mcp.py --variant A` and `--variant C` (control without `--safe-mode`): both failed. No MCP server in the init event, only `StructuredOutput` listed, model reported NO_TOOL; model check passed; exit 0, 2 turns, about 2.4 s. Probe server answers MCP `initialize` by hand. Cause: the account's organization-managed settings allow only listed MCP servers. Results in `results/2026-10-09_safe_mode_mcp/`
- Remaining: decision on the agent tool interface (planning account and Andrew), then agent code
- Done: Andrew chose agents that return typed actions, executed by the orchestrator, with no MCP. Proposal for the planning account: `docs/proposals/2026-10-09_structured-action-agents.md`. Andrew asks course staff whether a project MCP server can be allowed
- Bottlenecks: local MCP tools are blocked by organization policy; needs either an administrator allowlist entry or a design without MCP

## 2026-10-09 (planning account, session 2)
- Done: reviewed the build account's six commits and the safe-mode MCP test. Approved the typed-action proposal with seven conditions, recorded in `docs/proposals/2026-10-09_structured-action-agents.md` and `docs/decisions.md`
- Demo: none; review only
- Remaining: build account runs the schema test (condition 2), then builds `agents/`; Andrew asks course staff whether a typed-action loop counts as tool use
- Bottlenecks: course staff answer on tool use
## 2026-10-09 (build account, session 4)
- Done: typed-action orchestrator, built on branch `wip/orchestrator` before the review below arrived; proposal `docs/proposals/2026-10-09_structured-action-agents.md`
- Done: `agents/launcher.py` (clean environment from a fixed list, pinned Claude Code 2.1.293, strict model check, prompt on stdin, built-in CLI tools off; the typed actions are the tool interface), `agents/actions.py` (draft fault, remedy and info lists; flat strict JSON schema; validation), `agents/orchestrator.py` (step loop, trace JSONL, step limit, stop after two failed calls), `agents/prompts/diagnostician.md`. Commit 0f2cff0 (after rebase)
- Done: `python -m pytest -q tests`: 7 passed in 0.10 s (scripted launcher, no LLM)
- Done: `scripts/check_cli.py` replaces `check_api.py`: Claude Code 2.1.293, login claude.ai (enterprise), model claude-opus-5-5, 2 turns, 1.6 s, OK. `anthropic` and `.env.example` removed; README setup uses `claude auth login`. Commit 74801a8 (after rebase)
- Done: `python scripts/demo_diagnostician.py` on a made-up task: request_info(displacement_vs_patch_radius), apply_remedy(displacement_exceeds_patch, change_frame_stride, half), accept(0.85). 3 steps, 0 failed calls, 21 s, about 3.5k input and 0.5k output tokens per step. Trace in `results/2026-10-09_demo_diagnostician/`. Commit 697d718 (after rebase)
- Demo: `python scripts/demo_diagnostician.py` prints `outcome: accept {'confidence': ...}; steps 3` and writes the trace
- Remaining: planning-account approval, then merge to main; fix the fault, remedy and info lists with a decisions entry; checker on synthetic rods; real executors for request_info and apply_remedy
- Bottlenecks: approval of the typed-action proposal (planning account); MCP allowlist question with course staff (Andrew)
- Done: planning-account review of the typed-action proposal received (approved, seven conditions). Branch rebased onto it; all seven met:
- Condition 2, schema test: `python scripts/cli_probe/test_action_schema.py`, 12 calls. `optional` 4 of 4 valid (2 turns, 3.7-4.7 s), `nullable` 4 of 4 (two calls needed 3 turns, up to 12.7 s), `union` 0 of 4 (API 400: top-level schema needs `type`). `optional` kept as default. `results/2026-10-09_action_schema/`. Commits 5639f1c, 867278b. Built after the orchestrator, not before; the review arrived after the first build
- Condition 5: launcher records a failure cause (timeout, exit_code, max_turns, schema, result_error, model_check); orchestrator logs failed steps with cause, including invalid_action. Condition 4: per-task calls, tokens and call time in the outcome and a `task_end` trace line. Commit 5639f1c
- Condition 3: `agents/views.py` builds the auditor's input without `rationale`, raw output or free-text arguments; `tests/test_views.py` checks it. Commit 60627bd
- Condition 1: README and code describe the typed actions as the agents' tool interface. Commit 1e0e2ac
- Condition 6: MCP results README corrected (`--safe-mode` disables MCP by itself; variant C shows the policy; an allowlist entry would be machine-specific) and policy confirmed with `claude mcp list` / `claude mcp get probe` (probe absent; `No MCP server named "probe"`) and the managed setting `allowManagedMcpServersOnly`. Commit 1f14abc. Condition 7: variant B removed from the MCP script. Commit 25b2d35
- Done: `python -m pytest -q tests`: 16 passed in 0.16 s. `python scripts/check_cli.py`: OK, 1.5 s. `python scripts/demo_diagnostician.py`: accept (0.9), 3 steps, 0 failed, 3 calls, 10,081 input and 1,427 output tokens, 16.1 s. Commit df38612
- Demo: `python scripts/demo_diagnostician.py` prints the outcome and per-task call totals and writes the trace
- Remaining: merged to main this session; fix the fault, remedy and info lists with a decisions entry; checker on synthetic rods; real executors for `request_info` and `apply_remedy`; call-budget estimate and approval step before any all-roots run (condition 4)
- Bottlenecks: course staff answer on whether typed actions count as tool use (Andrew)

## 2026-10-09 (planning account, session 3)
- Done: reviewed build session 4 (12 commits). Seven conditions confirmed met; `python -m pytest -q tests` gives 16 passed on a second machine. Wrote the next spec, approved by Andrew: `docs/specs/2026-10-09_checker-and-synthetic-rods.md`
- Demo: none; review and spec only
- Remaining: build account works the spec in order (branch cleanup, measurement record, synthetic rods, checker, real executors, freeze). Planning account drafts the related-work note and the draft proposal for Lab report 1 (due 16 Oct)
- Bottlenecks: course staff answer on whether typed actions count as tool use (Andrew)


## 2026-10-10 (build account, session 5)
- Done: pulled spec `docs/specs/2026-10-09_checker-and-synthetic-rods.md`. Worked items 1-4; stopped at item 4 for threshold approval
- Done: item 1. Remote `wip/orchestrator` was already gone; `git branch -r` lists `origin/main` only
- Done: agents env switched to OpenBLAS; with MKL every numpy matrix product exited Python (0xc06d007f). Commit 576ebfb
- Done: item 2. Measurement record `measure/record.py`, `docs/context/measurement_record.md`: three tracked chains, stage log, frame times, per-frame midline; strain rates from chain segment stretch, not the tracker's logistic fits. Commit 6547010. Tracker-output test with a fixture from a clean rod: `tests/test_record_tracker.py`. Commit 7e339e3
- Done: item 3, field level. `measure/rod.py`: six cases. Derived strain rates within 0.08 %/h of the analytic truth; integrated strain rate equals tip-relative base velocity to 0.01 px/h. Commit 6547010
- Done: item 3, image level. `measure/render.py`: textured rod movies in the tracker's input format, injectors for the five development faults only. `scripts/remote/qb_track.py`, `scripts/synth/run_batch.py`. Commit 4337285
- Done: item 4. Check definitions and costs in `docs/decisions.md` (rigid invariance: one extra tracker run; closure and plane sections: none). Commit 6547010; checker `checker/` in f606fb1; coverage rule in e25bb03. Definitions were worked out alongside the code, then committed before it
- Done: 70 tracker runs on the lab server, 0 failed, 6-7 s each; about 20 min wall time in total. Clean REGR error 0.40-0.44 %/h RMS, max 1.42 %/h, peak 43 %/h. Field level: 18 of 18 check outcomes as expected. `results/2026-10-10_checker_synthetic/`. Commit aebc749
- Done: proposed thresholds in `config/checker_thresholds.yaml` (status: proposed): rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.0 %/h. Not used to score anything
- Done: `python -m pytest -q tests`: 42 passed, 1.3 s
- Demo: `python scripts/synth/eval_rods.py --tracks <tracks dir> --out results/2026-10-10_checker_synthetic` prints the per-group check table; `python -m pytest -q tests` covers the field-level pass/fail table and the tracker fixture
- Remaining: Andrew approves or changes the three thresholds; decide on width_change (not detected at the injected size: 1.93-2.33 %/h against clean up to 2.36 %/h); then item 5 (real executors, runner interface, remedy-to-tracker-parameter table, `scripts/demo_slice.py`), then item 6 (freeze)
- Bottlenecks: threshold approval and the width_change decision (Andrew); course staff answer on tool use (Andrew)

## 2026-10-10 (planning account, session 4)
- Done: reviewed build session 5 (8 commits). Andrew approved the checker thresholds: rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h (raised from the proposed 3.0). `config/checker_thresholds.yaml` marked approved, decisions logged
- Done: wrote spec `docs/specs/2026-10-10_bent-rods-width-change-rotation.md` from Andrew's answers: larger width-change injection, whole-rod rotation flagged by closure, two strongly bent clean cases. Field-level trial of the two bent cases with the existing code: plane_sections at most 0.22 %/h, the other two 0.0000
- Demo: none; review and spec only
- Remaining: build account works parts A and B of the new spec, then item 5 of the 2026-10-09 spec, with part C before item 6
- Bottlenecks: course staff answer on tool use (Andrew)

## 2026-10-10 (build account, session 5, continued)
- Done: pulled planning session 4: thresholds approved (2.0 %/h, 1.0 px/h, 3.25 %/h), spec `docs/specs/2026-10-10_bent-rods-width-change-rotation.md`. Worked parts A and B
- Done: code. `width_change_spec(kappa_inv)`, `rigid_rotation_spec(rate, pivot_offset)`, new field case `rotation_basal_pivot`, `IMAGE_EXPECTED` (rigid_rotation: closure fails), `--width-kappa-inv` and `--rotation-deg` options, test `tests/test_image_expected.py` with seed-0 fixtures. Commit 4188ad8. Threshold basis comment now 15 clean rods. Commit d1b6100
- Done: 30 tracker runs on the lab server, 0 failed, 0 frozen points; render 21 s and track 7-8 s per width run. `results/2026-10-10_width_rotation/`. Commit bb5e1f7
- Done: part A. plane_sections at curvature 1/400 (true 3.0 %/h): 4.30, 3.43, 3.55, 3 of 3 above 3.25. At 1/267 (true 4.5 %/h): 6.04, 4.98, 5.15, 3 of 3. Other checks pass. Four of six peaks at s = 40-75 px
- Done: part B. Field level: rotation_basal_pivot closure 13.96 px/h (= rate x 200 px), others 0. Image level, closure at 0.1 / 0.03 / 0.01 deg/frame: 5.58 / 1.71 / 0.57 px/h median, predicted 5.58 / 1.68 / 0.56. Slowest rate flagged: 0.03 deg/frame. 0.01 deg/frame is not flagged
- Done: `python -m pytest -q tests`: 49 passed, 1.8 s
- Demo A: `python scripts/synth/eval_rods.py --tracks <tracks dir> --out results/2026-10-10_width_rotation` writes `per_seed.md` with the plane-sections value per seed and size
- Demo B: the same command prints the closure-against-rate table (`rotation.md`); `python -m pytest -q tests/test_image_expected.py` checks rigid_rotation fails closure only at the approved thresholds
- Remaining: Andrew picks the width_change size (1/400 clears 3.25 by 0.18 %/h at worst; 1/267 by 1.73); then item 5 of the 2026-10-09 spec; part C (bent rods) before item 6
- Bottlenecks: width_change size choice (Andrew); course staff answer on tool use (Andrew)

## 2026-10-10 (build account, session 6)
- Done: width_change set to curvature 1/400 px (Andrew's choice). Commit f3afee9 went in with one failing test (end-of-chain point in the field truth comparison); fixed in cef215a
- Done: item 5 of the 2026-10-09 spec, built. Preprocessing before tracking (`measure/preprocess.py`: frame registration, midline smoothing, band mask, frame quality). Commit c6abc76
- Done: real executors `agents/executors.py`; remedy table `measure/remedies.py` and `docs/decisions.md`; info kinds `measure/info.py`; runner `measure/runner.py` (in process and remote job; config in `private/runner.yaml`, template `config/runner.example.yaml`). Commit c77ff40
- Done: `python -m pytest -q tests`: 61 passed, 2.3 s
- Done: remedy sweep, each development fault with its natural remedy, no agent, 22 tracker runs: no fault reaches three passes. displacement_exceeds_patch stride 12 -> 6 -> 3: REGR error 11.37 -> 3.87 -> 1.43 %/h; rigid_drift register_frames: closure 16.27 -> 1.26 px/h; midline_jitter smooth strong: plane_sections 35.3 -> 8.8 %/h; low_texture enlarge 2x: invariance 255 -> 65 %/h. `results/2026-10-10_demo_slice/`. Commit e62b17b
- Done: `python scripts/demo_slice.py --fault displacement_exceeds_patch`: halved stride, then five info requests and register_frames; outcome step_limit at 8 steps, 0 failed steps, 35.9k input and 3.7k output tokens, 43.7 s call time. REGR error 11.37 -> 5.51 %/h RMS. Commit e62b17b
- Demo: `python scripts/demo_slice.py --fault displacement_exceeds_patch` prints the truth, the checks and error before and after, and the outcome; writes `results/<date>_demo_slice/`
- Remaining: Andrew decides on removing `switch_midline_source` and `use_width_free_ratio` (they return "not available"); Andrew and planning decide what to do about remedies that improve but never repair a dev fault (remedy settings, the 6 h window of the stride fault, step limit); part C (bent rods) before item 6; item 6 freeze
- Bottlenecks: the two list decisions above (Andrew); course staff answer on tool use (Andrew)

## 2026-10-10 (planning account, session 4, continued)
- Done: reviewed build session 5 continued (4 commits) and session 6 (6 commits). Read the demo trace and the remedy sweep
- Done: wrote spec `docs/specs/2026-10-10_repair-criteria.md`, approach agreed by Andrew: clean rods through each remedy, fault sizes a remedy can repair, correct outcome per rod, diagnostician may repeat a working remedy. Decisions logged
- Demo: none; review and spec only
- Remaining: build account works the new spec (A, B, C, then D after Andrew approves the sizes and the tolerance), then the bent rods, then item 6
- Bottlenecks: `width_change` outcome and the two unavailable remedies (Andrew); fault sizes and tolerance once proposed (Andrew); course staff answer on tool use (Andrew)


## 2026-10-10 (build account, session 7)
- Done: Andrew's decisions applied: `switch_midline_source` removed; `use_width_free_ratio` reports centre strain rate and width-free ratio and skips plane sections. Commit 9dddf46
- Done: fault size options and a no-agent sweep runner. Commit 52e8064. Outcome categories, labels and diagnosis scoring in `measure/score.py`, one test per table row. Commit 9e6494b. Evaluation script. Commit a1a7f2c
- Done: repair-criteria sweep, parts A-C: 354 tracker runs, 0 failed, 52 min. `results/2026-10-10_repair_criteria/`. Commit 51de646
- Done: part A stop condition met: clean rods fail approved thresholds after register_frames (closure 1.05-1.22 px/h, 0 of 6), smooth_midline strong (closure about 3.0, 0 of 6), smooth_midline light (3 of 6 pass) and stride 2 (one of 6 runs fails rigid invariance at 23.2 %/h)
- Done: part B: sizes meeting the criteria: displacement_exceeds_patch 2x6 (tip speed x2, stride 6; two halvings, 3 of 3) and width_change (use_width_free_ratio, 3 of 3). No size works for rigid_drift, midline_jitter or low_texture
- Done: part C: proposed tolerance REGR RMS <= 1.0 %/h, flank-difference RMS <= 0.5 %/h. Labels written for the sizes tried
- Done: `python -m pytest -q tests`: 75 passed. An evaluation bug (stride halving counted 3 steps for 6 -> 3 -> 1) was found and fixed before the tables were committed
- Demo A, B, C: `python scripts/synth/eval_repair.py --out results/2026-10-10_repair_criteria` prints the three tables from the fetched sweep
- Remaining: Andrew decides on the part A failures (remedies that make clean rods fail: register_frames, smooth_midline); approves sizes and tolerance; then part D
- Bottlenecks: the decisions above (Andrew); course staff answer on tool use (Andrew)

## 2026-10-11 (planning account, session 5)
- Done: reviewed build session 7 (5 commits) and the repair-criteria sweep. Andrew's decisions logged: fix `register_frames` and `smooth_midline`; tolerance approved (centre 2.5 % of true peak REGR, flank difference 0.5 %/h); sizes approved for `displacement_exceeds_patch` (2x6) and `width_change` (1/400); coupled mode added as a run setting, both modes run; limits for the shared tracker machine
- Done: wrote spec `docs/specs/2026-10-11_remedy-fixes-coupled-mode-shared-compute.md`. Two rule lines added to `CLAUDE.md`
- Done: calculated, not run: the registration band (240-400 px from the tip) still holds growing tissue, band mean 0.97 px/h, against 1.1 px/h added to closure. Item 3 of the spec confirms it first
- Done: searched the tracked files for machine names, outside paths and people's names. None found
- Demo: none; review and spec only
- Remaining: build account works the new spec in order (compute limits, the two fixes, uncoupled re-run, tolerance, coupled mode, bent rods, part D code). About 610 tracker runs. Planning account drafts the related-work note and the draft proposal for Lab report 1 (due 16 Oct)
- Bottlenecks: sizes for `rigid_drift`, `midline_jitter` and a repairable `low_texture` once proposed (Andrew); tracking mode for the real movies (Andrew); course staff answer on tool use (Andrew)


## 2026-10-11 (build account, session 8)
- Done: spec `2026-10-11_remedy-fixes-coupled-mode-shared-compute.md`, items 1-5, 7 (uncoupled) and 8 (code). Item 6 stopped at the clean basis (coupled growing rods fail closure). Spec not done
- Done: item 1, shared-machine limits in `scripts/synth/sweep.py` and `measure/runner.py`. Check: 8 clean runs, 0 failed, 8.7-10.5 s each, CPU share 0.83-0.92 of a core, 504-507 MB, load 1.92 / 3.07 / 3.07 before / during / after. One-thread output equal to earlier runs to 1e-13 px. Commit b04ca85
- Done: item 2, `smooth_midline` padded by linear extrapolation (odd reflection). Translating midline unchanged to < 0.01 px (was 3.7 / 9.8 px). Commit 6064dd0
- Done: item 3, registration cause confirmed: closure 1.16 / 0.21 / 0.08 px/h at band 0.6 / 0.8 / 0.9. New band: record's REGR under 5 % of peak to the midline end, 25 px inside the frames. 6 of 6 clean pass (closure 0.09-0.16), 3 of 3 rigid_drift size 1 pass. Commit 346388c
- Done: item 4, uncoupled re-run, 216 runs. Clean: 24 of 24 pass after the fixed remedies. rigid_drift meets the criteria at all four sizes; midline_jitter and low_texture 0.2 / 0.25 at none. Proposed (not adopted): rigid_drift 0.5. Commits 9f73915, eebc229
- Done: item 5, tolerance in `config/scoring_tolerance.yaml`; part C labels unchanged. Commit 9f73915
- Done: item 6, `couple` run setting (tag `_cpl`). Coupled 9.4-9.6 s against 9.3 s per run, same memory. Clean basis coupled: 10 of 10 growing rods fail closure (1.46-1.99 px/h), REGR error 4.4-5.3 %/h; rigid_translation 5 of 5 pass. Tracker's own coupled peak 31.9 %/h against truth 43.4. Stopped. Commit eebc229
- Done: item 7, `bend_continue` and `bend_reverse` added; uncoupled 6 of 6 pass all checks. Commit eebc229
- Done: item 8, prompt rules, before-and-after check values, roll back. Commit 9d27233
- Done: `python -m pytest -q tests`: 97 passed. 356 tracker runs this session, 12 failed (report-line bug, fixed and re-run), 19 min wall in total; work space 4.46 -> 5.5 GB
- Demo 1: `python scripts/synth/fix_sweep.py start --part check`, then `status --part check` prints the preflight line, 8 runs and the end line (load, peak workers, wall time)
- Demo 2: `python -m pytest -q tests/test_preprocess.py` checks the translating midline is unchanged after both smoothing levels
- Demo 3, 4, 6, 7: `python scripts/synth/eval_fix.py --out results/2026-10-11_remedy_fixes` writes the item 3, 4, 6 and 7 tables from the fetched sweeps
- Demo 5: `python -m pytest -q tests/test_score.py` checks the tolerance just inside and outside for a clean and a 2x6 rod
- Demo 8: `python -m pytest -q tests/test_executors.py -k "roll_back or no_progress"`
- Remaining: Andrew's two answers (below); then the coupled sweeps (about 420 runs) and coupled bent rods, if continued; Andrew approves sizes; then the diagnostician runs (part D)
- Bottlenecks: whether to change the smoothing end padding, which leaves midline_jitter not repairable (Andrew); whether to continue coupled runs (Andrew); sizes for rigid_drift, midline_jitter, low_texture (Andrew); course staff answer on tool use (Andrew)

## 2026-10-11 (planning account, session 6)
- Done: reviewed build session 8 (7 commits) and `results/2026-10-11_remedy_fixes/`. Andrew's answers logged: `rigid_drift` 0.5 approved; smoothing padding changed to a fitted line; no further coupled sweeps at the default setting, a coupling-weight sweep on clean rods instead; flank tolerance from the same basis rule with the bent rods included
- Done: wrote spec `docs/specs/2026-10-11b_padding-flank-tolerance-coupling-weight.md`
- Done: reading of the coupled clean basis: peak 31.9 against 43.4 %/h but closure short by only 1.5-2.0 px/h of 60, so the profile is spread along the root and the integrated growth is nearly kept
- Demo: none; review and spec only
- Remaining: build account works the new spec in order (padding, flank tolerance, four diagnostician runs, coupling weight). About 370 tracker runs. Item 6 of the earlier spec is closed by this one. Planning account drafts the related-work note and the draft proposal for Lab report 1 (due 16 Oct)
- Bottlenecks: sizes for `midline_jitter` and a repairable `low_texture` once proposed (Andrew); tracking mode for the real movies (Andrew); course staff answer on tool use (Andrew)


## 2026-10-11 (build account, session 9)
- Done: spec `2026-10-11b_padding-flank-tolerance-coupling-weight.md`, item 1 run and stopped; item 4 done; items 2 and 3 not started. Spec not done. Spec `2026-10-11_remedy-fixes-coupled-mode-shared-compute.md` is closed by 11b (item 6 replaced by 11b item 4)
- Done: item 1, `smooth_midline` time padding by a line fitted to 3 (light) or 7 (strong) end frames, tag `ms*3`. End-frame jitter 0.97 / 0.73 of the odd-reflection value. 72 runs: clean light 6 of 6 pass, clean strong 0 of 6 (closure 1.55-1.60 px/h): stop. Cause: smoothing in image coordinates across 10.5 px stage steps; in world coordinates the net tip error is 0.00 px/h. midline_jitter: no size meets the criteria. Commit 4db4b0c
- Done: item 4, coupling weight (`couple_lambda`, `couple_mu`, defaults 2.0) x 0, 0.01, 0.03, 0.1, 0.3, 1 on 6 rod groups, 252 runs. x0 equals uncoupled. Peak growth_zone 42.4 (uncoupled) -> 30.7 %/h (x1), truth 43.4. All growing rods pass the thresholds up to x0.03. Peak loss larger at twice the tip speed at every weight
- Done: `python -m pytest -q tests`: 99 passed. 324 tracker runs, 0 failed, 11.5 min wall; load at most 6.22 on 32 cores; work space 5.42 -> 5.62 GB
- Demo 1: `python -m pytest -q tests/test_preprocess.py` (translating midline unchanged; end-frame jitter ratio); `python scripts/synth/eval_fix.py --out results/2026-10-11b_padding_tolerance_coupling --parts b_smooth` prints the clean and midline_jitter tables
- Demo 4: `python scripts/synth/eval_fix.py --out results/2026-10-11b_padding_tolerance_coupling --parts b_weight` prints the weight table, the passing range and the peak loss at 1x and 2x speed
- Remaining: Andrew's answer on smoothing in world coordinates; then item 1 re-run, item 2 (flank tolerance, about 84 runs), item 3 (4 diagnostician runs)
- Bottlenecks: smoothing in world coordinates (Andrew); midline_jitter and repairable low_texture sizes (Andrew); tracking mode for the real movies (Andrew); course staff answer on tool use (Andrew)

## 2026-10-11 (planning account, session 7)
- Done: reviewed build session 9 (2 commits), `b1_smoothing.md` and `b4_coupling_weight.md`. Andrew's answers logged: smooth in world coordinates, final change to that remedy; system uncoupled, no further coupled runs
- Done: wrote spec `docs/specs/2026-10-11c_world-coordinate-smoothing-uncoupled.md`. It also asks for a freeze list for approval
- Demo: none; review and spec only
- Remaining: build account works 11c in order (world-coordinate smoothing, items 2 and 3 of 11b, uncoupled note in the README, freeze list). About 160 tracker runs, at most 5 diagnostician runs. Planning account drafts the related-work note and the draft proposal for Lab report 1 (due 16 Oct)
- Bottlenecks: sizes for `midline_jitter` and a repairable `low_texture` if proposed (Andrew); the freeze (Andrew); course staff answer on tool use (Andrew)


## 2026-10-11 (build account, session 10)
- Done: spec `2026-10-11c_world-coordinate-smoothing-uncoupled.md`: item 1 done; item 2 run with the flank tolerance stopped (1.00 %/h, not 0.75); 5 diagnostician runs made; items 3 and 4 done. 11c and 11b not done: the flank tolerance and three questions wait for Andrew
- Done: item 1, `smooth_midline` time smoothing in world coordinates, tag `ms*4`. 72 runs: clean 12 of 12 pass light and strong; midline_jitter 0.5 px met the criteria on 3 of 3 (2 by strong). Commit 8891942
- Done: item 2 (11b item 2), bent rods through 7 remedy settings, 84 runs: strong fails plane_sections on 6 of 6 bent clean rods (3.43-4.69 %/h), so `strong` withdrawn by the 11c rule; midline_jitter then not repairable at 3 px. Basis rule gives flank tolerance 1.00 %/h (0.797 max, enlarge_patch 2x): stop. Largest centre error 2.45 % of peak
- Done: 11b item 3 plus the midline_jitter run: 5 diagnostician runs, seed 0. 1 correct outcome (low_texture decline), 2 unnecessary declines (width_change, rigid_drift), 2 step limits (displacement_exceeds_patch 2x6, midline_jitter). 0 of 5 faults named correctly. 37 steps, 159k / 18k tokens, 207 s call time
- Done: fixes found by those runs: `demo_slice.py` relative `--out` crash (summaries rebuilt by the new `--replay`, no agent call repeated); `truth_error` with no coverage; roll back counted an uncomputable check as resolved
- Done: item 3 README line (uncoupled); item 4 `docs/proposals/2026-10-11_freeze-v1.md`
- Done: `python -m pytest -q tests`: 102 passed. 156 sweep runs, 0 failed, 6.8 min wall; load at most 6.32 on 32 cores; work space 5.62 -> 5.67 GB
- Demo 1: `python -m pytest -q tests/test_preprocess.py`; `python scripts/synth/eval_fix.py --out results/2026-10-11c_world_smoothing_freeze --parts c_smooth`
- Demo 2: `python scripts/synth/eval_fix.py --out results/2026-10-11c_world_smoothing_freeze --parts c_tolerance` prints the basis rule per setting and the result 1.00 %/h
- Demo 3: `python scripts/demo_slice.py --fault rigid_drift --size 0.5 --out results/2026-10-11c_world_smoothing_freeze/diagnostician --replay` re-applies the recorded remedies and prints the outcome without an agent call
- Demo 4: `docs/proposals/2026-10-11_freeze-v1.md`
- Remaining: Andrew's answers (flank tolerance; confirm `strong` withdrawn; re-run of the low_texture diagnostician run); then labels under the tolerance, the low_texture size question, and the freeze
- Bottlenecks: flank tolerance, `strong`, the extra diagnostician run, freeze approval (Andrew); course staff answer on tool use (Andrew)

## 2026-10-12 (build account, gatekeeper session)
- Done: `scripts/hooks/pre_push_check.py`: scans commits being pushed (added or changed files at each commit, and commit messages). Rules: private blocklist, host names, IPv4 addresses, user-at-host, absolute paths, keys and tokens, .tif/.tiff/.npy/.sldy/.h5/.hdf5 files, files over 5 MB, files under private/, data/, staging/. Prints rule, commit, file and line only. Commit db2ad99
- Done: `scripts/hooks/install.sh` writes the pre-push hook; refuses to overwrite a different hook without `--force`. README setup step 6. `.gitattributes` keeps `.sh` files LF. Commit caa1f09
- Done: `tests/test_pre_push_check.py`: 29 passed (clean commit passes; one failing case per rule; blocklist match not printed; missing blocklist blocks; installed hook blocks a push to a bare repo and scans only new commits). Full suite `python -m pytest -q tests`: 131 passed
- Done: blocklist read from `private/blocklist.txt` beside the git common dir (main repo folder); temp blocklist in tests
- Done: history scan `pre_push_check.py --commits main`: 64 commits, 6.7 s, 1 hit. Commit 304a3cb, file `scripts/manifest/open_review.bat` (absolute path rule). The line was removed in 80e8a4b; 304a3cb is on origin/main. History not rewritten. The path is a conda env Python location with no account or machine name; left as is (Andrew, 2026-10-12)
- Not done: hook not installed in the shared repo. The hook runs the script from the pushing checkout; other worktrees' branches do not have it yet and would be blocked until this branch is merged
- Choice: blocklist patterns match case-insensitively (broader than the task asked); recorded in `docs/decisions.md`
- Demo: `python scripts/hooks/pre_push_check.py --commits main` prints the one hit and "64 commits scanned, 1 hits"
- Remaining: merge wip/gatekeeper to main; run `sh scripts/hooks/install.sh` in the main repo folder with the agents env active
- Bottlenecks: none; merge and hook install wait for Andrew

## 2026-10-12 (build account, diag-review session)
- Done: read the 5 diagnostician traces of build session 10 (all seed 0) against `agents/prompts/diagnostician.md`, `agents/actions.py`, `measure/info.py`, `checker/checks.py`, `agents/executors.py`. No code changed. 0 diagnostician calls; no `--replay` run (traces were enough)
- Done: `docs/proposals/2026-10-12_diagnostician-misses.md`. Per run: true fault, info asked, answers, fault named, first divergence
- Result: terminal fault correct 0 of 5; correct outcome 1 of 5 (low_texture decline); true fault named in a remedy 2 of 5 (displacement_exceeds_patch step 2, midline_jitter steps 3 and 8)
- Result: causes: a (missing measurement) 2: width_change (no width in any info kind; the "osmotic treatment" rule cannot fire, the task has no treatment field), low_texture (frame_quality has no reference). b (prompt led away) 3: rigid_drift, displacement_exceeds_patch, midline_jitter. c (step limit) 0: the two step-limit runs needed 4-5 and 3-4 steps. d 0; one flag on the midline_jitter label under a 1.00 %/h flank tolerance
- Result: one belief drives 3 misses: the agent reads "rigid-body invariance" as a drift test. The check adds a known rigid motion; unlogged drift passes it and fails closure
- Proposals P1-P5 (prompt wording for b, one info field each for a). All change a proposed freeze item: listed as needs Andrew before the freeze. Scoring seeds proposed: seed 0 development only; seeds 1-2 held out (10 runs, labels exist)
- Done: `python -m pytest -q tests`: 131 passed
- Demo: `docs/proposals/2026-10-12_diagnostician-misses.md`, summary table at the top
- Remaining: Andrew's answers on P1-P5 and the seeds; then apply the approved changes before the freeze; score on seeds 1-2
- Bottlenecks: P1-P5 approval, held-out seeds, frame_quality reference for real movies (Andrew)

## 2026-10-12 (build account, baselines session)
- Done: remedy tree written and committed before any run: `docs/proposals/2026-10-12_remedy-tree.md`, commit ea95149. Uses only freeze-list remedies, pass or fail of the approved checks, the 3/4 roll-back rule and step limit 8. No new remedy or threshold needed
- Done: `agents/baselines.py`: fixed-parameter script (base run, checks recorded not acted on, accept) and remedy tree. Both act on the diagnostician's `Slice` and return its `Outcome`; trace lines in the orchestrator format. `tests/test_baselines.py`: 7 tests. Commit 720f7da
- Done: `scripts/synth/baselines.py` runs both in rounds from a local cache; each round's missing tracker runs go out as one sweep (`sweep.py` lock and limits; refuses while another sweep runs, and past 200 runs). `scripts/synth/eval_baselines.py` scores summaries with `measure/score.py` unchanged against the freeze labels. README section and two decisions entries. Commits 720f7da, 8dcba30
- Done: 5 rounds, 108 tracker runs, 0 failed, 472 s sweep wall time; load at most 5.03 on 32 cores; work space 5.67 -> 5.83 GB. No round found the lock held
- Done: results in `results/2026-10-12_baselines/` (commit 9a2cc03). Correct outcomes: script 6 of 15, remedy tree 15 of 15, diagnostician 1 of 5 (seed 0 runs of 2026-10-11, rescored with the same code; categories unchanged)
- Done: script: 3 false_accept displacement_exceeds_patch, 3 false_accept low_texture, 2 false_accept and 1 good_report midline_jitter, 3 good_report each for width_change and rigid_drift (accepts with checks failing; the base measurement is within tolerance)
- Done: tree: 57 steps, 42 remedies applied, 20 roll backs, at most 5 steps, no step limit. Its fault naming (15 of 15) follows from its lists, not from diagnosis
- Found: `diagnosis_correct` on the last `apply_remedy` gives the diagnostician 1 of 5 (midline_jitter, step-limit run); the 2026-10-11 log says 0 of 5
- Found: the midline_jitter script result depends on the open flank tolerance: at 0.5 %/h 2 false accepts, at 1.00 all 3 good_report
- Note: the freeze is still a proposal; the table is scored against it as written. `python -m pytest -q tests`: 138 passed
- Demo: `python scripts/synth/eval_baselines.py --runs results/2026-10-12_baselines/runs --agent-runs results/2026-10-11c_world_smoothing_freeze/diagnostician --out results/2026-10-12_baselines` prints the fault x method table and totals (needs `staging/tracks_baselines/` for the truth)
- Remaining: merge wip/baselines; re-score after the freeze is approved (flank tolerance); single-agent baseline after the freeze; diagnostician seeds 1-2 for a like-for-like comparison
- Bottlenecks: freeze approval and flank tolerance (Andrew). Shared remote code directory: every sweep start syncs this checkout's `measure/` and `scripts/` there, so parallel sessions with different code can overwrite each other's code mid-sweep (Andrew, to decide)

## 2026-10-12 (build account, lab-report-1 session)
- Done: draft `docs/reports/2026-10-16_lab-report-1.md` from `docs/reports/TEMPLATE.md`: repository, progress, demo, next two weeks, related-work note, draft proposal. Numbers taken from the log and results READMEs, each with its commit hash
- Done: related-work note part 2 (setting) cites KymoRod, PatchTrack, Chavarria-Krauser 2008, Krupar 2026, plus Youssef 2018, Platre 2024 and the kinematics papers, all from the digests. No tracker comparison
- Found: the digests hold no paper on agent systems, so part 1 has no citations. It is an outline marked [ANDREW], with a to-read list of 9 papers (references from memory, not checked)
- Not done: README run steps not re-run (no conda on PATH in this session). Report cites the last logged suite result, 131 passed
- Demo: open `docs/reports/2026-10-16_lab-report-1.md`; [ANDREW] marks show what Andrew must write or decide
- Remaining: Andrew reads and digests 2-3 agent-systems papers, writes part 1; fills the [ANDREW] marks (README check date, research question, intended users, root count 118 vs 123/102, demo choice, next-steps order); confirms pre-push hook install
- Bottlenecks: agent-systems reading (Andrew)

## 2026-10-12 (planning account, freeze decisions spec)
- Done: wrote spec `docs/specs/2026-10-12_freeze-decisions-diagnostician-fixes.md` from Andrew's decisions on the open items of freeze v1, the session 10 questions and P1-P5. Committed on wip/freeze-v2 (769d97f)
- Decisions in it: flank tolerance 1.00 %/h; `strong` withdrawn; midline_jitter 3 px and low_texture 0.03 are declines; P1-P5 approved; scoring seeds 1-5, seed 0 development only; freeze approved from v2, not v1
- Demo: none; spec only
- Remaining: build account works the spec in order (done on wip/freeze-v2, entry below)
- Bottlenecks: `frame_quality` reference for real movies (Andrew)

## 2026-10-12 (build account, freeze-v2 session)
- Start: spec `docs/specs/2026-10-12_freeze-decisions-diagnostician-fixes.md` was not in Git (683a6d1 logged the miss). Andrew pasted the text; saved and committed alone as given (769d97f). Spec worked in order, items 1-6; done. No stop condition hit
- Done, item 1 (9ef68f1): 9 decision lines in `docs/decisions.md`; `config/scoring_tolerance.yaml` flank difference 1.00 %/h. `strong` already absent from `REMEDIES` and `describe()`; `measure/remedies.py` accepted any `smooth_midline` setting and now rejects all but `light`; test `test_smooth_midline_strong_rejected`
- Done, item 1: seeds 0-2 labels recomputed from existing runs under 0.5 and 1.00 %/h (`scripts/synth/eval_freeze.py --parts relabel`): 15 rods, 36 runs, 0 tracker runs; no label changes (`results/2026-10-12_freeze_v2/item1_labels.md`)
- Done, item 2 (f4f9a74): `config/scoring_seeds.yaml`: development [0], scoring [1, 2, 3, 4, 5]
- Done, item 3 (2a5baa5): seeds 3-5 labelled tracker only, `scripts/synth/freeze_sweep.py` parts seeds35 and seeds35_reg. 66 tracker runs (spec estimate 105-150; `strong` not run, width_change needs one run), 0 failed, 316 s sweep wall time, peak 4 workers, load 1 min max 5.44 on 32 cores, work space 6.7 -> 7.28 GB. No seed 3-5 label differs from seeds 0-2 (`item3_seeds35.md`)
- Done, item 4 (5b896cb): P1-P5 as written. Prompt lines; `stage_log_summary` closure residual per hour at moves and elsewhere; `velocity_profile` flank spacing rate and its largest absolute value; `frame_quality` reference (`config/frame_quality_reference.yaml`: contrast median 0.193, lowest 0.155; focus 0.090, 0.073; 45 frames of the 15 clean basis rods); `settings_left` "no further setting" note in remedy results. `tests/test_info_p1_p5.py`, 5 tests; 4 seed-0 tracker outputs added as fixtures
- Done, item 5 (a3a0dbf): `docs/proposals/2026-10-12_freeze-v2.md`. Open: real-movie `frame_quality` reference only
- Done, item 6 (da93690): development check, seed 0, 5 diagnostician runs (not a score): 5 of 5 correct outcomes, 5 of 5 terminal faults correct (build session 10: 1 of 5, 0 of 5). 28 steps, 124k input and 13k output tokens, 148 s call time, Claude Code 2.1.293. Table in `results/2026-10-12_freeze_v2/README.md`
- Done: `python -m pytest -q tests`: 137 passed
- Setup, not tracked: the worktree reaches `staging/tracks`, `staging/tracks_2026-10-11` and `private/` through directory links to the main checkout. New seed 3-5 outputs are in this worktree's `staging/tracks_2026-10-12/`
- Demo: `python scripts/synth/eval_freeze.py --out results/2026-10-12_freeze_v2 --parts relabel seeds35` prints both label tables and "Labels that change: none"
- Done: freeze v2 approved by Andrew, 2026-10-12. Recorded in the proposal header and `docs/decisions.md`. Not tagged
- Remaining: merge wip/freeze-v2; then the scored runs on seeds 1-5 (25 runs), as a new spec
- Bottlenecks: the real-movie `frame_quality` reference (Andrew)

## 2026-10-12 (build account, held-out faults session)
- Done: `measure/render_heldout.py`: injectors for second_root, fast_rotation, bad_stage_correction (agent fault names with no injector) and flank_swap, partial_occlusion (new). Same interface as `measure/render.py`; `make_rod.py` renders them. Commit 8109764
- Done: `tests/test_render_heldout.py`: 14 passed (each injector changes the movie only where it should; size 0 equals `render.render` exactly). Full suite `python -m pytest -q tests`: 145 passed
- Done: `scripts/synth/heldout_sweep.py`, checker only, no agent, own code directory on the tracker machine, same sweep lock. Commit d9a631c
- Done: sweep, growth_zone seeds 0-2, 9 sizes, 54 tracker runs, 0 failed, 204 s wall, 4 workers; waited 245 s for the baselines sweep's lock; load 4.30 -> 5.63 max -> 4.99 on 32 cores; work space 5.83 -> 6.70 GB
- Result: checker fails 3 of 3 at second_root 30 px (15 px: 0 of 3), fast_rotation 2 and 4 deg/frame, bad_stage_correction 3 and 10 px, flank_swap 0.5, partial_occlusion 20 and 30 px. `results/2026-10-12_heldout_faults/checker_sizes.md`
- Proposed sizes (smallest failing 3 of 3): second_root 30, fast_rotation 2, bad_stage_correction 3, flank_swap 0.5, partial_occlusion 20. Not used in any scored run. `docs/proposals/2026-10-12_heldout-faults.md`
- Demo: `python scripts/synth/heldout_sweep.py eval --out results/2026-10-12_heldout_faults` (after `fetch`) prints the per-fault table of seeds failing the checker
- Remaining: Andrew approves sizes, names and outcomes; then the remedy label sweep (about 90 runs, no agent); then merge at the freeze
- Bottlenecks: size, name and outcome approval (Andrew); branch not merged until the freeze (Andrew)

## 2026-10-12 (build account, scored-v1 session)
- Start: spec `docs/specs/2026-10-12b_heldout-labels-single-agent-scored-runs.md` pasted by Andrew; saved and committed alone (8d2cda7). Branch wip/scored-v1 from main 5b64897. Items 1-7 done in order
- Done, item 1 (625b461): code syncs to `<code_dir>/<branch with / replaced by _>` (`measure/runner.py`, `branch_code_dir`; detached HEAD refused). Held-out sweep's `_heldout` suffix removed. Work directory, sweep lock and 10 GB limit unchanged. `tests/test_runner_code_dir.py`, 6 tests
- Coordinator: merge item 1 (625b461) to main early, so later branches pick it up
- For Andrew: old code copies left in place on the tracker machine, not deleted: the shared copy at `code_dir` itself and `<code_dir>_heldout` (`code_dir` in `private/runner.yaml`)
- Done, item 2: tag `freeze-v2` on main 5b64897, pushed
- Done, item 3 (1e5e2c2): `scripts/synth/heldout_labels.py`. 84 tracker runs, 0 failed, 212 s sweep wall, 4 workers, load at most 5.71 on 32 cores. Labels: second_root, fast_rotation, flank_swap, partial_occlusion not repairable 3 of 3; bad_stage_correction repairable (register_frames) 3 of 3. `results/2026-10-12b_heldout_labels/`
- Found: fast_rotation label differs from the proposal (accept after register_frames): register_frames leaves all checks failing; correct outcome decline. Label wins; size unchanged
- Found: `use_width_free_ratio` (not a fitting state) on second_root passes the other two checks with a good centre on 3 of 3. Label kept from fitting states, as for the development labels. For Andrew
- Item 4: stopped and asked (the `check_report` info kind, remedy results and the prompt carry checker output). Andrew chose: check_report listed, answered not available; remedy results give the change only; no roll back; one prompt sentence replaced; no check value in any message, with a test
- Done, item 4: definition `docs/proposals/2026-10-12_single-agent-baseline.md` (51f1598, before any run). `BlindSlice` in `agents/executors.py`, `agents/prompts/single_agent.md`, `single_agent` entry in `config/models.yaml` equal to the diagnostician's (4192747). `tests/test_single_agent.py`, 5 tests; the leak test also flags the diagnostician's view when pointed at it
- Done, items 5-6 (c9d5a0c harness, f2b727e results): `scripts/synth/scored_v1.py`. 160 runs: 4 methods x (25 dev + 15 held-out). 80 agent runs, 0 harness errors, 0 orchestrator errors. All runs record freeze-v2 and commit c9d5a0c; Claude Code 2.1.293
- Done: tracker runs for the scored runs: 96 in 9 sweep rounds (0 failed, 445 s wall, load at most 4.73), 22 as single jobs from agent runs. Spec total 202 tracker runs, 657 s sweep wall time
- Result, dev seeds 1-5, correct of 25: script 10, remedy tree 24, diagnostician 24, single agent 11. False accepts: script 10, others 0. Not reported (step limit): diagnostician 1, single agent 13
- Result, held-out seeds 0-2, correct of 15: script 3, remedy tree 9, diagnostician 11, single agent 7. False accepts: script 12, tree 3 (partial_occlusion), agents 0. Terminal fault correct: tree 1, diagnostician 3, single agent 1
- Result: second_root: tree, diagnostician and single agent applied the width-free ratio, named width_change and accepted a good centre on 3 of 3 each; counted neither correct nor false accept under the label
- Result, both sets, per run mean: diagnostician 5.2 steps, 23.0k tokens in, 2.7k out, 31.6 s call time; single agent 6.8 steps, 28.4k, 3.3k, 38.8 s. Totals 0.92M and 1.14M tokens in
- Done, item 7 (30b78e1): `results/2026-10-12b_scored_v1/README.md`, `table_dev.md`, `table_heldout.md`, `scores.json`. Lab report 1 root-count mark replaced as the spec gives it
- Done: `python -m pytest -q tests`: 169 passed
- Setup, not tracked: worktree links to `private/` and the staging caches of the main checkout and the baselines, freeze-v2 and held-out worktrees
- Demo: `python scripts/synth/scored_v1.py eval` prints both method x fault tables and totals (needs the staging caches for the truth)
- Remaining: merge item 1 early, then the branch; Andrew decides whether the width-free ratio is a label state for second_root (changes 9 runs from uncounted to correct); auditor next
- Bottlenecks: second_root label question (Andrew); real-movie `frame_quality` reference (Andrew)
