# Section 1: rules over the whole history (task c033)

Scope: `git log --all` (1,107 commits, 16 remote branches), private ledger and configs read only. Date of the check: 2026-11-23. Strings that are themselves sensitive are not quoted; findings give commit, file and line only. Scripts: `results/2026-11-23_audit/scripts/s1_blocklist_map.py`, `s1_bio_tip.py`, `s1_spend.py`.

Counts: blocker 0, major 6, minor 2.

## Findings

### S1-1 (major): commit author identity names a user account and a machine domain
- Where: 19 commits, author and committer `unknown`, all on `origin/main` (and other branches): 14 `turn-long` status commits (b7fb643 to a018a8e, 2026-10-23/24) and 5 `spec-audit-r` status commits (ae74d81 to 06a4fd7, 2026-10-23)
- Evidence: the author and committer email of these 19 commits has the form (account) at (machine domain). The local part is a user account. The domain is a machine domain that also contains a person's name. This string occurs in no tracked file and in no commit message (`git log --all -G`, `--grep`: 0). The pre-push hook scans only file contents and commit messages, not author or committer fields, so it reported 0 hits for these commits
- Fix: Andrew decides whether to rewrite the history of these 19 commits before the repository is public, or to accept them and record that. Add an author/committer email check to `scripts/hooks/pre_push_check.py`. Set `user.name`/`user.email` in the environment of every headless session

### S1-2 (major): cluster name in pushed history, not recorded as a known hit
- Where: blocklist entry for the cluster name, 12 hits in 7 commits on `origin/main`: `docs/agents/inbox/autotrace.md:22` in f4e8fbd, 4285985, 8c5bcff, eabd9be (2026-10-23/24); `docs/agents/inbox/real-calib.md:18,19,24` in c8c17d5, 64145b9, a70ca64 (2026-10-25/26)
- Evidence: `python scripts/hooks/pre_push_check.py --commits=--all`: 1,107 commits, 14 hits (12 blocklist, 1 absolute path, 1 user-at-host). Both files are clean at the tip (removed in b8bf79e and 3edb757). The only history hit Andrew accepted is 304a3cb (spec audit rules-1, 2026-10-23). These 12 are not recorded in `docs/decisions.md` or `docs/running_log.md`. Coordinator and coord-tick status lines report "0 hits" for pushes only
- Fix: Andrew decides whether to rewrite or accept these commits. Record the decision in `docs/decisions.md`, as was done for 304a3cb

### S1-3 (major): real-root strain-rate profile at the tip of main in a file that says it is masked
- Where: `results/2026-11-18_integrated_run/example_traces.md:17` (added in 854d06a, 2026-11-23). Line 3 of the same file says REGR, growth-zone and flank values are `[masked]`
- Evidence: the velocity_profile result of a real window (step 2 of the first example) has the strain-rate profile array (`strain_rate_pct_per_h`, 43 numeric values) and `negative_strain_rate_min_pct_per_h` unmasked. The other biology keys on that line are masked. No other line of the file has an unmasked biology key. `windows.csv`, `tables.md`, `demo.md` and `failure_modes.md` have none
- Fix: mask the strain-rate array and its minimum on line 17, as the other keys are masked. Check the masking code that wrote the file and apply it to every profile array

### S1-4 (major): real-root biology values in older real-slice traces at the tip of main
- Where, at `origin/main`:
  - `results/2026-10-24_real_slice_3roots/diagnostician_trace.jsonl:2,11` (4c936a9): velocity profile, peak strain rate and its position, flank spacing rate
  - `results/2026-10-24_real_slice_3roots_c2/diagnostician_trace.jsonl:2` (918ae13): the same keys
  - `results/2026-10-24_real_slice_closure_gate/auditor_trace.jsonl:1` (65a6980): centre peak REGR, growth-zone length, flank difference
  - `docs/proposals/2026-10-23_real-midline-smoothing.md:7`: flank difference range on a real window
- Evidence: `scripts/s1_bio_tip.py origin/main` (keys with numeric values, real-movie result folders). 14 of the 16 remote branch tips have the three trace files. 4 tips have the S1-3 file. The 2026-10-26 strip decision (`docs/decisions.md:182`) covered only `results/2026-10-25_real_subset/`
- Fix: strip or mask these values as was done for the real subset. Record it in decisions. Andrew decides whether the proposal line is a check value or a biology value

### S1-5 (major): real-subset biology values remain in pushed history
- Where: `results/2026-10-25_real_subset/` before a70ca64: columns `peak_regr_pct_h` and `growth_zone_um` in `windows.csv`, condition medians in the README and `tables.md`, `summary.json` and traces (commits 035e8fc, 2ea98bd, 97f2eb0, 2026-10-25). Heuristic history scan (added lines with REGR, growth-zone or flank keys and a number, real-movie folders): 609 lines in real_subset, and smaller counts in other real folders (full_batch_1 122, midline_fit_validation 50, real_calibration 41, closure_definition 28, registration_fix 25, the 10-23/24 real slices 2-17 each). Some of these lines are thresholds, not biology values
- Evidence: `docs/decisions.md:182` (Andrew, 2026-10-26) says the removed files are "kept in git history". So the values are disclosed but still in the history of the repository that will be public. CLAUDE.md: nothing unpublished from other lab work appears in this repo
- Fix: Andrew decides whether to rewrite the real-subset history (and the other real folders) before the repository is public, or to accept it and record that in `docs/decisions.md` under the public-repo rule

### S1-6 (major, disclosed and fixed): renames on the lab server, 2026-10-13 to 2026-10-25
- Where: `scripts/remote/qb_track.py` (`.part.npz` then `os.replace`, tracker runs on the lab server up to 2026-10-23; spec audit rules-2, fixed 7eb7cc3). `scripts/remote/real_moved.py` (`.part` then rename, commits 4875874, 3cb0775, 65a6980, ce70876 of 2026-10-24; moved copies on the lab server for the real slices and real calibration; fixed b5dc210, 2026-10-25)
- Evidence: `docs/decisions.md:127` and `:177` ("a rename-era copy without markers counts as complete"); `docs/reviews/2026-10-23_spec-audit/rules.md:15-18`; `docs/agents/inbox/closure-fix.md` item 3. The rule (CLAUDE.md, 2026-10-13) allows only the sweep lock files. No delete on the lab server by a session was found
- Fix: none to the code (fixed). State it once in the failure-mode or AI-use section of Lab report 4 as a rule breach that the code allowed

### S1-7 (minor): spend ledger rows incomplete and out of order
- Where: private ledger (323 rows, 2026-10-23 22:49 to 2026-11-23 07:49); tracked `results/2026-10-25_full_batch_2/audit/ledger.csv` (98 rows)
- Evidence: 63 rows have no actual cost (1 on 10-25, 2 on 11-13, 60 from 11-20 to 11-23: the c027, c029, c031 and supplement arrays). Job 5469410 has no actual in the private ledger ($0.067 in the tracked one). Running total falls five times between consecutive rows (rows not in time order on 2026-11-05). Jobs of 2026-10-23 before the first row ($0.45) have no rows. No tracked per-job ledger covers spend after 2026-11-05, so the integrated-run figure ($8.248) has no committed source
- Totals: last running total (sacct actual plus worst case of jobs still live) $8.33 of $15; highest $8.51 (11-23 06:53). No row is above $15 or the $12 stop. Recorded actual costs: $6.93 in rows, plus $0.45 before the first row and $0.067 for 5469410, $7.44 in total. Worst case summed over all rows: $36.94 (worst cases of finished jobs are not counted again in the running total). Stated values agree with the ledger: $7.24 (decisions:217, LR3:76, batch 2 README; private actual plus $0.45 plus 5469410 = $7.24 at 2026-11-05), $7.37 (LR3:85), $8.248 before the demo GPU job and $8.50 after it (integrated run README:37, dispatcher pending log)
- Fix: write the actual costs (sacct) of the 63 rows and of 5469410 into the ledger. Sort the rows by submit time. Commit a per-job ledger extract (job id, partition, type, array size, worst case, actual) for c027 to c031, as was done for batch 2

### S1-8 (minor): backup script still runs a niced job on the lab server
- Where: `scripts/ops/backup_vm.sh:169,181` (last change 33dd56d, 2026-10-16)
- Evidence: the script runs `nice -n 19 ionice ... cat` and `nice -n 19 sha256sum -c` on the server. Spec 2026-11-04 forbids "any `nice`d job" there. The script has not run since 2026-11-04 (no log, status or commit mentions it after that date). The VM-setup status says the backup is run by hand only
- Fix: drop `nice`/`ionice` from the remote commands, or mark the script as not to be run until Andrew approves. Record either in decisions

## Checked, no finding
- Absolute path in history: 304a3cb `scripts/manifest/open_review.bat:5`, removed in 80e8a4b; accepted by Andrew 2026-10-12 and 2026-10-23 (spec audit rules-1). The path names a Python env, not a user account
- user-at-host hit 708a386 `AGENTS.md:22`: a placeholder `noreply.invalid` address in a co-author trailer. False positive
- Storage-only host name: the same word as the plant species name. 8 tracked files use it as the species name; 0 lines in any commit use it in a host context (ssh, server, @, login, rsync, storage): `git log --all -p -G`
- People's names: blocklist names 0 hits in 1,107 commits (hook). Titles and roles (Prof., Dr., advisor, postdoc) at the tip: 0 outside course guideline text
- Commit messages: scanned by the hook, 0 hits
- Files under `private/`, `data/`, `staging/` ever tracked: 0. Image or data files and files over 5 MB: 0 hook hits
- Secrets: hook key/token rules 0 hits. `git log --all -G`: `sk-ant` 1 commit and `github_pat_` 1 commit (both db2ad99, the hook's own regex); `IdentityFile` 1 (832272c, a docstring); private key blocks, `ANTHROPIC_API_KEY=`, `ghp_`, AWS keys, `ssh-rsa AAAA`, password or token assignments: 0. Secret-like file names (`.env`, `id_rsa`, `.pem`, `.key`, `credentials`): 0
- Deletes on the cluster: every remote `rm` in code at the tip appends to `DELETED.log` in the cluster work folder (`measure/cluster_compute.py:114`, `scripts/retrack_queue.py:263`, `scripts/full_batch_2_driver.py:165`). Delete records in inbox, decisions and results (2026-10-24, 10-25, 10-26, 11-04 batch 2: 170 deletes, all md5-checked first per `audit/reverify.md`, 11-12: 24, 11-20, 11-22) each name `DELETED.log`. `DELETED.log` itself is on the cluster and was not read (no cluster access in this audit)
- Deletes on the lab server: none found. Other removals in code (`shutil.rmtree`, `unlink`, `shutil.move`, `Remove-Item`) act on VM staging, VM result folders or lock files. The freeze-v31 render-file delete exception (decisions:144) was on the workstation
- GPU type: required "P100 or V100 only, never L40S, H100, H200" (spec 2026-10-23 next-steps:43; spec 2026-11-04:7); "V100 or lower" (spec 2026-11-18:40,72). Requested: tracked `scripts/remote/full_batch_2_root_job.sh:7` P100; private runner configs P100 or V100; ledger 108 P100 jobs, 1 V100, 214 CPU, 0 other. The only GPU job after 2026-11-05 (7918920, 2026-11-23, demo midline) is P100. `tests/` use a fake `gpu:1`. No mismatch
- Cluster spend against the $15 stop: highest running total $8.51; no submit above $12 or $15 (S1-7 for gaps)
- Jobs on the lab server after 2026-11-04 15:12 (spec b6eaef7): added lines in running log, pending logs, status files, task files, results READMEs and decisions that name the lab server together with run, track, checker, midline, sweep, job or process: 9 lines, none a run there (cluster master requests, reused batch-1 tracks from October, an equivalence note). Commit messages after that date: 1 match (6a77cde, the change that makes the code refuse compute on storage-only hosts). Commands sent to the storage link in code at the tip: `md5sum`, `cat`, `du`, `mkdir`, `test`, `ssh -O check` only
