# Spec audit 2026-10-23: reviewer `rules`

Spec `docs/specs/2026-10-23_spec-audit.md`, Reviewers item 2. Rules: `CLAUDE.md` lines 29-39. Worked from `origin/main` (worktree `wip/spec-audit`) and the other branches by `git show` / `git log`. `private/` read only; nothing from it is quoted here.

## Findings

### rules-1: STOP: Andrew. Pre-push scan finds 1 hit in pushed history, on every branch
- Ours: commit 304a3cb, `scripts/manifest/open_review.bat:5`, rule "absolute path"
- Source: spec "Stop and ask Andrew", item 2 (pre-push scan finds a hit in history); `CLAUDE.md:29`
- Evidence: `python scripts/hooks/pre_push_check.py --commits <ref>` over 18 local branches and 18 `origin/` refs (36 refs). Each ref: 1 hit, the same commit and file line; 68-182 commits scanned per ref (`origin/main` 175). No other rule hit on any ref. The line was removed in 80e8a4b. The same hit was logged on 2026-10-12 and left as is by Andrew (`docs/running_log.md:215`). History not rewritten since
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action (Andrew's 2026-10-12 decision stands)

### rules-2: Code run on the lab server renames files there; only `sweep.py` lock files are excepted
- Ours: `scripts/remote/qb_track.py:134` (`origin/main`) and `:154` (`origin/wip/dispatcher`): output written as `.part.npz`, then `os.replace` to the final name; `measure/runner.py:160-166` `sync_code`: `tar xf` into the code directory overwrites existing code files; `measure/runner.py:197`: plan file written with `cat >`
- Source: `CLAUDE.md:35` (no session deletes, moves or renames any file on the lab server; only exception: lock files of `scripts/synth/sweep.py`); `CLAUDE.md` Human approval ("any action that deletes or overwrites data")
- Evidence: rule dated 2026-10-13. Server tracker runs after that date: dispatcher timing runs t1 and t2 on 2026-10-23 (`origin/wip/dispatcher:results/2026-10-23_tracker_timing/README.md`), each through `qb_track.py`, so each ended in one rename. Rename design recorded in `docs/decisions.md:54` (2026-10-11, before the rule). The rule text does not except it. No log entry names it as a rename
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, handled (freeze v3)

### rules-3: Paths outside the repo in tracked files, not caught by the hook
- Ours: `docs/agents/README.md:9`; `docs/agents/inbox/data-steward.md:3`; `docs/agents/inbox/gate2.md:3`, `:17`, `:22`; `docs/agents/inbox/litreview.md:3`; `docs/agents/inbox/spec-audit-r.md:3`; `origin/status/gate2:docs/agents/status/gate2.md:16`
- Source: `CLAUDE.md:29` (no path outside the repo in a tracked file)
- Evidence: `git grep -n -E "~/"` on `origin/main` and the unmerged branches: 8 lines with home-directory paths. `pre_push_check.py` `PATH_RE` (`scripts/hooks/pre_push_check.py:49`) matches three Unix mount and home prefixes and drive letters only; it does not match a tilde home path
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, fixed (069d5e8; the `status/gate2` line goes with that branch)

### rules-4: Research-lane work (other lab work) described in tracked files on the public remote
- Ours: `docs/agents/inbox/gate2.md` (26 lines: plan items, settings, roots, review steps); `origin/status/gate2:docs/agents/status/gate2.md` (16 lines: run counts and a pass/fail outcome of the research gate); `docs/agents/inbox/data-steward.md`, `litreview.md`, `spec-audit-r.md` (research-lane sessions)
- Source: `CLAUDE.md:31` (nothing unpublished from other lab work; if unsure whether published, ask Andrew); `CLAUDE.md` Rules, course paper scope (tracker comparisons and biology results out of scope)
- Evidence: read the files. Whether the research-lane content is published is not stated in the repo. Needs Andrew to decide
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, fixed (branch `status/gate2` removed from the remote, inbox audit-marks item 2)

### rules-5: Access methods and another person's statement named in tracked files
- Ours: access methods: `docs/running_log.md:17`, `:337`, `:382`, `:383`, `:384`, `:386`, `:388`, `:402`; `docs/reports/2026-10-16_lab-report-1.md:59`, `:60`, `:61`; `docs/specs/2026-10-13_auditor-v1-real-frame-quality-labels.md:61`; `README.md:41`. Another person's statement: `docs/running_log.md:17`
- Source: `CLAUDE.md:29` (no access method; no comments or feedback from other people)
- Evidence: `git grep -n -oiE "ssh|sftp|scp|gitlab|enterprise seat|..."` on `origin/main`: protocol, transfer tool, remote host type and account type named in log and report lines. Generic uses in code (`measure/runner.py`, `scripts/ops/backup_vm.sh`, `config/*.example.*`) not listed. `docs/running_log.md:17` paraphrases an instruction from the course instructor
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (3378952)

### rules-6: Shared-machine transfer above the 50 MB/s cap on 2026-10-16
- Ours: `docs/running_log.md:386`; `docs/reports/2026-10-16_lab-report-1.md:60`
- Source: `CLAUDE.md:36`; `docs/decisions.md:116` (50 MB/s limit, the 2026-10-16 copy exceeded it)
- Evidence: log: one 1.14 GB file at 74 MB/s for 15 s; other files "under 54 MB/s" (so some above 50). Logged as a deviation. Later backup capped at 40 MB/s; test run about 28 MB/s (`docs/running_log.md:400`)
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### rules-7: Agent single jobs on the lab server do not check the sweep lock
- Ours: `measure/runner.py:176-180`, `:240`, `:258` (single jobs: load check, nice 19, ionice idle; no lock check); `scripts/synth/scored_v1.py` `agents` command (no `sweep_status` check; the `next` and `fetch` commands check at `:355`, `:374`)
- Source: `CLAUDE.md:36` (at most 4 workers, one sweep at a time); `docs/decisions.md:53-54`
- Evidence: scored runs v1: 96 tracker runs in 9 sweep rounds at 4 workers, plus 22 single jobs from agent runs (`docs/running_log.md:304`). `staging/tracks_scored_v1/sweeps.jsonl` (32 lines) has no timestamps, so overlap of single jobs with a running sweep cannot be checked from disk. Agent traces start 2026-10-12T22:55:35
- Severity: would change a design choice
- Frozen item: no
- Andrew: accepted, handled (freeze v3)

### rules-8: Sweeps before the shared-machine limits ran without them
- Ours: commit 52e8064 (2026-10-10, `scripts/synth/sweep.py`, `--workers 4`, no thread cap, nice or load gate); `docs/running_log.md:113`, `:130` (22 and 354 tracker runs, 2026-10-10)
- Source: `CLAUDE.md:36`; `docs/decisions.md:53` (limits set 2026-10-11)
- Evidence: worker count 4 in 52e8064. Thread variables, nice, ionice and load gates added in b04ca85 (2026-10-11 11:21). The runs precede the rule
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### rules-9: Real-movie frames staged from 7 windows of roots not `include` yes; not labelled or used
- Ours: `private/fq_real_candidates.csv` status "replaced", `private/fq_real_frames.json`; `docs/running_log.md:350`
- Source: `CLAUDE.md:33` (rule dated 2026-10-13)
- Evidence: 37 candidate windows, 111 frames. 30 windows (90 frames) inside the usable window of an `include` yes root. 7 windows (21 frames) on roots with `include` unsure or no, staged by the first labeling set (e6c3b78), then replaced (18e45ce): 0714_m3 10.0-11.0 h; 0708_m5 21.0-22.0 h; 0714_c8 5.0-6.0 h; 0714_c3 15.0-16.0 h; 0711_m8 20.0-21.0 h; 0721_c12 17.0-18.0 h; 0708_c1 14.0-15.0 h. Their frames and views were removed from the VM staging; no label was written; `staging/fq_real_labeling/frames/` now holds only the 30 kept windows; none is in `private/fq_real_values.csv` or `labels.csv`
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### rules-10: Prompts and thresholds changed after the first held-out result, before freeze-v2 was tagged
- Ours: commit order (`git log --all --date=iso`, Pacific time, 2026-10-12 unless noted):
  - 20:19:54 fe7dda1 first held-out result: checker-only fault sizes, `results/2026-10-12_heldout_faults` (no agent run)
  - 20:24:01 9ef68f1 `config/scoring_tolerance.yaml`, `measure/remedies.py` (flank tolerance 1.00; `strong` rejected)
  - 20:24:12 f4f9a74 `config/scoring_seeds.yaml`
  - 20:32:31 5b896cb `agents/prompts/diagnostician.md`, `config/frame_quality_reference.yaml` (P1-P5)
  - 22:10:00 5b64897 tag `freeze-v2`
  - 22:38:23 1e5e2c2 held-out labels (tracker only)
  - 22:40:50 4192747 `agents/prompts/single_agent.md`, `agents/actions.py`, `config/models.yaml` (single-agent baseline)
  - 22:55:35 first scored agent run; 2026-10-13 00:00:01 f2b727e scored runs v1 committed (first held-out agent result)
  - 2026-10-13 21:30-21:40 99d70bd, c708fb0, aa8483a auditor prompt rounds 1-3 (dev batches); 21:45:31-21:56:05 auditor held-out runs; 2026-10-14 04:58 46a9d6f committed
  - 2026-10-13 23:58 c8eeedd `config/frame_quality_reference.yaml` `real:` section only; 2026-10-17 519a3b1 `config/models.yaml` Claude Code re-pin
- Source: spec Reviewers item 2 (held-out separation); `docs/proposals/2026-10-12_freeze-v2.md`; `docs/proposals/2026-10-12_single-agent-baseline.md:3`; `docs/proposals/2026-10-13_auditor-v1.md:41`, `:51-52`
- Evidence: changes at 20:24-20:32 follow the checker-only held-out sizes and are inside freeze-v2. The single-agent prompt (4192747) is after the freeze-v2 tag and the held-out labels, before any scored run; no freeze version names it; its proposal (51f1598) says committed before any run. Auditor prompt rounds ran after the held-out scored records were committed (f2b727e); the proposal states development on the 4 dev batches only. Diagnostician prompt sha256 prefix 83ba54768d332ae4 at freeze-v2, c9d5a0c and `origin/main`, and in all 210 diagnostician steps of scored runs (dev and held-out). Single-agent prompt c8a9d43830928498 at 4192747 and `origin/main`, in all 272 steps. Auditor held-out prompt 2541926380a9e924 = aa8483a = `origin/main`, in all 12 held-out auditor traces. `git diff freeze-v2 origin/main` on `checker/`, `measure/remedies.py`, `config/checker_thresholds.yaml`, `agents/prompts/diagnostician.md`: no change. On `agents/actions.py`: 1 line (`ACTION_SETS["single_agent"]`). No change to prompts, thresholds or remedies after the first held-out agent result except the `real:` frame-quality section and the version re-pin
- Severity: record only
- Frozen item: yes (freeze-v2: diagnostician prompt, remedies, thresholds); no for the single-agent and auditor prompts
- Andrew: accepted, no action

### rules-11: Staged real frames kept on the VM after use
- Ours: `staging/fq_real_labeling/frames/` (90 frames, 30 windows) and `view/` (30 files) in the main checkout; `docs/running_log.md:374`
- Source: `CLAUDE.md:32` (delete staged images after use)
- Evidence: frames listed on disk 2026-10-23. Log: kept until Andrew says to delete (fq-real inbox item 6)
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

## Checked, no finding
- Pre-push scan, other rules: `pre_push_check.py --commits <ref>` on 36 refs: 0 hits besides rules-1
- Usable windows, fq-real labelling set: 30 labelled windows (24 clean, 5 unsure, 1 not_clean), 90 frames, against `manifest/root_manifest.csv`: 30 of 30 on `include` yes roots, 90 of 90 frame times inside `usable_from_h`-`usable_to_h`
- Usable windows, real frame-quality reference: recomputed from the 24 clean windows, 72 values: texture_contrast median 0.0648, lowest 0.0439; focus median 0.0286, lowest 0.0213; equal to `config/frame_quality_reference.yaml` `real:`
- Usable windows, results and tests: `grep -rE` for root ids and `movie: real` in `results/`, `tests/`, `config/`, `scripts/`, `measure/`, `agents/`, `audit/`: 0 real-movie frames (test `tests/test_frame_quality_reference.py` uses a synthetic record); `git grep` root ids in `results/`, `tests/`, `docs/reports/` on 9 unmerged refs: 0
- Usable windows, dispatcher timing (`origin/wip/dispatcher`): root 0708_m12, window 2-4 h; manifest `include` yes, usable 0-24.01 h: inside
- Checker has no LLM calls: `grep -nE "anthropic|claude|subprocess|agents|audit\.llm|Popen|requests|http"` in `checker/`: 0 imports or calls (1 docstring); imports numpy, yaml, `measure.record` (stdlib and numpy only). Same `git grep` on `checker/` in 17 refs: docstring only
- Model ID pin: `config/models.yaml` model `claude-opus-5-5`, Claude Code 2.1.302 (re-pinned 2026-10-17, was 2.1.293, `docs/running_log.md:423`). `git log --all -- config/models.yaml`: 6 commits, model line unchanged
- Model and version per run: result traces in `results/`: 738 model fields, all `claude-opus-5-5`; 184 `claude_code` fields, all 2.1.293 (scored v1: 80 runs; auditor v1: 24 runs). Log: 2026-10-12 freeze-v2 check 2.1.293 (`:273`), scored v1 2.1.293 (`:303`), 2026-10-17 CLI check 2.1.302 after re-pin (`:424`). 0 mismatches. No agent run recorded after 2026-10-17 besides the CLI check
- Remedies in scored runs: 320 files of `results/2026-10-12b_scored_v1/`: 479 remedy records, 198 `apply_remedy` actions executed; pairs used: register_frames, change_frame_stride half, smooth_midline light, crop_or_mask mask_second_root, enlarge_patch 1.5x and 2x, use_width_free_ratio. 0 outside the freeze-v2 list (`docs/proposals/2026-10-12_freeze-v2.md:25-33`). Other `results/` folders: 0 remedy names outside the list (`smooth_midline strong` absent)
- Scored runs record `freeze_tag` freeze-v2 and commit c9d5a0c: 160 of 160 summaries
- Server limits, worker cap: every logged sweep after 2026-10-11 at 4 workers or fewer on 32 cores (`docs/running_log.md:151`, `:181`, `:202`, `:238`, `:270`, `:285`, `:298`, `:304`); 0 over the cap
- Server limits, one sweep at a time: held-out sweep waited 245 s for the baselines lock (`:285`); baselines: no round found the lock held (`:238`); 0 overlaps logged
- Server limits, load rule: load logged before, during or after each sweep (`:151`-`:304`); dispatcher timing load 0.62-0.74 before on 32 cores
- Server deletes, moves, renames logged: 0. Stale lock left in place (`:379`); old code copies left (`:296`); verify clones left for Andrew (`:385`). Removals at `:350`, `:403`, `:422` are on the VM
- Cluster: 0 cluster runs (`origin/wip/dispatcher` timing README: lab-server timing only)
- Tracked files naming a machine or account: tokens from 7 private context files (83 identifier-like tokens not on the blocklist) searched in all tracked files: 45 tokens hit; first hit line read for 21 of them: config keys, key-file exclude patterns, scheduled-task and env names, experiment or folder names already in the manifest, the public repository URL, common words; 0 machine or account names found in the lines read. The other 24 not read line by line
