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
