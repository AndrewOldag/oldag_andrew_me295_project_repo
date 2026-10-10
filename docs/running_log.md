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
