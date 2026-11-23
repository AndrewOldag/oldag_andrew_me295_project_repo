# Section 5: decisions from 2026-11-18 on

Scope: `docs/decisions.md` lines 232-283 (52 entries, 2026-11-18 to 2026-11-23, main at 7514ec3). The two Andrew entries added on origin/main after it (hand review; growth-zone checks) do not affect the results in scope. For each entry: applied as written (code, config, run outputs, commit order), and disclosed where it affects a result (results README, spec 2026-11-18, Lab report 4 draft). There is no Lab report 4 draft in `docs/reports/` (latest: lab report 3), so (b) is checked against the results READMEs and the spec only.

Severity counts: blocker 0, major 1, minor 9.

## Findings

### S5-1 (major) c029 and c030 caps changed from LLM calls to agent runs without Andrew
- Where: decisions:235 (5778e1d); spec 2026-11-18 D3 (:56) "Cap 450 LLM calls", E2 (:62) "Cap 150 LLM calls"; inbox compound item 3 (planning, 2026-11-20)
- Evidence: the planning account approved counting runs. Counted as calls, c029 scored runs used 1,031 `claude -p` calls (499 + 532) against 450, and c030 used 382 against 150. Counted as runs, 153 of 450 and 90 of 150. The proposals (fa459b7; auditor check 6150856) state the run count and were committed before the runs. Both READMEs give both counts
- Approval: the planning account changed the unit of a cap that Andrew set in the spec. Andrew was reachable at the time. There is no Andrew entry
- Fix: Andrew confirms or rejects; amend spec D3 and E2; Lab report 4 states the unit

### S5-2 (minor) c027 cap raised to 1,300 after results were seen; spec and proposal still say 900
- Where: decisions:276; spec B1 (:36) "nothing changes after the first result is seen", B6 (:41); proposal `2026-11-18_integrated-run.md`:24
- Evidence: the run stopped at 782 calls at 01:48 (`staging/c027/after_wave.log`, dispatcher worktree). Inbox dispatcher 59 came at 02:20. The restart at 02:50 used `--llm-cap 1300` (`run_cap.log`) and ended at 03:26 with 1,007 calls; 1,015 after the final-now audit (wip/dispatcher bc36328). The worst case in item 59 (33 x 8 + 5 per root, on top of 782) stays under 1,300. The entry was lost in a merge and restored at 06:22 (b052925)
- Applied as written: yes (prompts, gate and thresholds unchanged across the restart). Disclosed: README:14, :58. Approval: planning, under the overnight delegation (:272). No later Andrew confirmation is recorded
- Cross-ref S4-4 (tables print "(cap 900)"; fixed on wip/dispatcher, not on main)

### S5-3 (minor) Integrated README omits 20 set-aside final records and the pre-pause changes
- Where: README:24, :58; decisions:239, :242, :257, :267
- Evidence: `staging/c027/run/voided_register/` holds 8 window records and the auditor runs of 3 roots. `held_remedy/` holds 12 records and the auditor runs of 5 roots. The decisions say "their 6 roots" and "their 8 roots"; the other roots had no auditor run yet. Calls in these records count in the 1,007 / 1,015 total and toward the cap (proposal :24). The pre-pause rule was added after 12 windows (:239) and changed on 11-22 (:267). Code at `scripts/run_all.py:357-376` matches :267
- Fix: name both folders, their counts and the pre-pause rule in Known limits

### S5-4 (minor) Two overnight deviations from spec B4/B5 taken by the build session alone
- Where: decisions:278 (57044f4, 06:48), :279 (9b352c9, 06:56)
- Evidence: the demo copies remedy tracks from the c027 cache (spec B5: "no cache"). Reruns replace the tree's c026 records (spec B4: "c026 records count"). No inbox item precedes either decision; :272 routes Needs-Andrew items to planning through status. The reason given for :279 follows spec 2026-11-20 (rescore windows that used registration). Disclosed: README:10, :41, :59
- Fix: record planning or Andrew approval; Lab report 4 states both

### S5-5 (minor) Zero-base lateral floor: attribution and README
- Where: decisions:263, :269; `checker/checks.py:253-260` (e0d067d); registration-fix README:54-56
- Evidence: entry :263 has no attribution, but the docstring says "(Andrew, 2026-11-22)". The only trace of approval is Andrew's inbox real-calib 27, which reports the fix as already made by planning. The gate description in the registration-fix README does not mention the floor
- Effect checked: no scored result is affected. c029 and c029b use `RemoteRunner` subclasses (form `remote_job`), and real and rendered-rod bases are nonzero. c029 (960cf04..043f8eb) and c029b (701442d..0c71f4b) ran on wip/compound without ed5b2ad, so their code still had the tracker-only exception of :266. That has no effect, for the same reason. A NaN base gets no floor (cf. S2-1)
- Fix: attribute :263; add the floor to the gate description

### S5-6 (minor) register_v2 known limit missing from the integrated run's failure modes
- Where: decisions:262, :271; `results/2026-11-18_integrated_run/failure_modes.md`, README Known limits
- Evidence: Andrew (inbox real-calib 27) asked for the limit in the R5 README and in the Lab report 4 failure modes. R5 README:93 has it. failure_modes.md has no registration row, and README:13 names register_v2 without the limit. For c029/c029b see S3-2
- Fix: add a failure-mode row and a known-limit line

### S5-7 (minor) "All windows final" in decision 283
- Where: decisions:283; README:57 on main
- Evidence: 4 integrated windows (7 tree) stay paused, and 0727_cc7 has no auditor run (wip/dispatcher bc36328). The README on main still says the audit waits for the cut-off. The updated README is not merged
- Fix: reword :283 (no paused window can become final); merge wip/dispatcher

### S5-8 (minor) 101 vs 102 roots
- Where: decisions:232, :276; spec 2026-11-18 title and :7, :35, :37
- Evidence: 102 manifest rows have include yes. windows.csv has 1,189 windows over 102 roots. Proposal :6 and README:6 say 102. 101 roots are audited
- Fix: correct the count or add a correction line

### S5-9 (minor) 2.5 GB rule superseded without an entry
- Where: decisions:234; `scripts/synth/heldout_compound.py:54`
- Evidence: Andrew's inbox compound item 4 (2026-11-20) set 3 GB for LLM runs again. The code uses 3.0 and cites that item; c029b proposal :7 says 3 GB. There is no decisions entry, and :234 is not marked superseded
- Fix: mark :234 and add the entry

### S5-10 (minor) Spec 2026-11-18 not amended for the decisions that change it
- Where: `docs/specs/2026-11-18_lab-report-4.md`
- Evidence: the spec is amended only for the deadline (604c7ab) and the $15 stop (ceb107a). Not reflected: cap 1,300 (B6), cap unit (D3, E2), demo cache (B5), tree rerun (B4), whole-imgdir staging (A1; :236), C3 checked rather than retracked and the column name (:253), c029b (D), integrity gate and register_v2 (spec 2026-11-20). The planning account drafts Lab report 4 from this spec
- Fix: add an amendments list with decision line numbers before drafting

## Entries

"ok" means checked, no finding.

### :232 2026-11-18 (Andrew) Lab report 4 plan
- Applied: run_all.py, retrack_queue.py and the c028-c030 results exist. Andrew later raised the $12 stop (:248). Root count 101 vs 102: S5-8

### :233 2026-11-20 c029 tracker runs on the VM
- Applied: equivalence 6.9e-18 / 4.2e-13 px stated. Superseded by :247/:254 (cluster). Disclosed: c029 README:23 (VM before spec 2026-11-20, cluster after). ok

### :234 2026-11-20 (Andrew) VM memory 2.5 GB
- Superseded by Andrew's inbox item 4 without an entry: S5-9

### :235 2026-11-20 c029/c030 caps counted as agent runs
- S5-1

### :236 2026-11-20 retracks stage whole root imgdirs
- Deviates from spec A1, with a recorded reason (decisions 2026-10-23, 2026-10-25). No result change. Spec not amended: S5-10

### :237 2026-11-20 wave 1 enumerated from REMEDIES
- Applied: proposal :20 has 461 jobs, $1.674. ok

### :238 2026-11-20 SSHException as lost channel
- Applied (4e8ec3b). No result change. ok

### :239 2026-11-20 pre-pause before any LLM call
- Applied after 12 windows: first trace 14:01, commit 044bf66 14:04. Proposal cf10046 (13:32) predates the run. Paused traces are not scored. Not in README: S5-3

### :240 2026-11-20 batch-1 c022 retracks seeded
- Applied (044bf66). ok

### :241 2026-11-20 checks_dir setting
- Applied (9dea3ed); the demo used its own folder (README:40). ok

### :242 2026-11-20 registration hold; 8 records voided
- Applied: 8 records in `voided_register/`; `REGISTER_HOLD = True` (v1 only) in run_all.py:53 and retrack_queue.py:55. Not in README: S5-3

### :243 2026-11-20 retrack tasks create output folder
- Ops. ok

### :244 2026-11-20 arange crash fixed in record code
- Applied: dc1cfe6, with the test named in arange README:15; 5 of 5 records identical. Spec C2 asked for retracks; README:20 says they were not needed because the fix is outside the tracker. ok

### :245 2026-11-20 (Andrew) LR4 due 29 Nov
- Spec and CLAUDE.md amended (604c7ab). ok

### :246 2026-11-20 (Andrew) register_frames held and fixed
- Applied: register_v2, integrity check and rescore (c031, c027). Disclosed: registration-fix README; integrated README:12-13. For c029/c029b see S3-2

### :247 2026-11-20 (Andrew) tracking on the cluster
- c029 tracker runs moved to the cluster. c029b proposal :6 says "No tracker run on the VM"; renders stay on the VM (rendering is not tracking). ok

### :248 2026-11-20 (Andrew) spend stop $15
- Spec A3 amended. For the spend source see S1-7, S4-3. ok

### :249 2026-11-20 (Andrew) headless sessions
- CLAUDE.md updated (a8fbedc). ok

### :250 2026-11-20 register_frames_v2 parameters
- Applied: `measure/preprocess.py:133` max_rot_deg 2.0; `measure/remedies.py:112` bound = ceil(2 x miss x hours). The tag `regv2p<from>b<bound>` is in `measure/remedies.py:62` and in the tables.md tags. ok

### :251 2026-11-20 integrity check separate from run_checks
- Applied: `track_integrity` and `integrity_gate` in checker/checks.py. ok

### :252 2026-11-20 absolute thresholds, reported not changed
- Applied; the decision went to Andrew (:255). Disclosed: registration-fix README:41-54. ok

### :253 2026-11-20 (planning) C3 without retracks
- Applied: arange README:22-27; 33 rows appended with `checked_after_fix`. Spec C3 asked for the append to the committed results file. Spec not amended: S5-10

### :254 2026-11-20 c029 on cluster, 2-rod equivalence
- Applied: cluster_equivalence.json gives 3.48e-7 and 1.55e-12 px (47e8eef, 11-20 23:11), before the c029 labels (a9445d2, 11-22 17:07). ok

### :255 2026-11-21 (Andrew) option A relative gate
- Applied: relative_integrity, config/integrity_relative_k.yaml. ok

### :256 2026-11-21 c027 register_v2 submitted, v1 held
- Applied: REGISTER_HOLD; tables.md shows only `regv2` tags. ok

### :257 2026-11-21 c027 remedy hold; 12 records held
- Applied: 12 records in `held_remedy/`; REMEDY_HOLD is now False (run_all.py:56). Not in README: S5-3

### :258 2026-11-21 stuck tasks cancelled, requeue once
- Applied; README:47 says "a task that fails twice is not requeued". ok

### :259 2026-11-21 status pusher stopped
- Ops. ok

### :260 2026-11-21 option A k values
- Applied: relative_k.json, 9 pairs. The 99.5th percentile x 1.5, rounded up, gives 1.5, 1.5, 3.0 (lateral max 1.95). 3 of the 9 pairs are identical tracks (disclosed, README:56)
- The config commit 47ec6e8 (10:20:55) precedes the 44-track check f4190cf (10:22:06). Which was computed first cannot be shown beyond commit order
- k comes from register v1 pairs; the v2 synthetic tracks pass the gate (regression.md, 6 of 6). ok

### :261 2026-11-22 (Andrew) c029 labels not gated
- Applied: no integrity call in the label code of heldout_labels.py, heldout_compound.py or heldout_supplement.py. The decision (f12675c 14:20) came before the labels (a9445d2 17:07). Disclosed: c029 README:85, c029b README:77. ok

### :262 2026-11-22 (Andrew) register_v2 kept
- Applied. Disclosed in R5 README:93; not in the integrated failure modes: S5-6

### :263 2026-11-22 zero-base lateral floor
- S5-5

### :264 2026-11-22 R1 answer, flagged window
- Disclosed in registration-fix README:14-15 (frame range: S4-9). ok

### :265 2026-11-22 c031 staged root deleted on the cluster
- Approved by Andrew's inbox real-calib 27 ("clear the staged root (md5 first, DELETED.log)"). It was a Claude-written copy in the cluster's own folder. ok

### :266 2026-11-22 gate wired into Slice.apply_remedy, tracker tracks only
- Applied (5a2e15e). :269 removed the exception on main. See S5-5 for the code state of the c029/c029b runs

### :267 2026-11-22 remedy hold lifted, pre-pause while any single remedy is missing
- Applied (run_all.py:357-376). Not in README: S5-3

### :268 2026-11-22 packing margin 1.1 x du
- Applied (e33c8f1). ok

### :269 2026-11-22 gate on every step, field-level rods included
- Applied on main (ed5b2ad; agents/executors.py on main has no `in_process` test). It was not on wip/compound when c029/c029b ran; no effect (S5-5)

### :270 2026-11-22 (Andrew) c029b supplement and selection rule
- Applied: the selection reproduces from labels.json (candidate order seed then kind; quotas 10/4/6): 20 of 20 equal to selected.json, in the same order
- Commit order: proposal bd3c2ce 20:11, correction ce0a3cf 20:14, first render 20:15 (staging/rods_c029b), labels and selection 701442d 03:46:57, methods start 03:47
- Decided after the c029 labels were seen and before the c029 LLM results were complete. c029 results unchanged. Disclosed in both READMEs. ok

### :271 2026-11-22 flagged window under option A
- Disclosed in the registration-fix README. Not in the integrated failure modes: S5-6

### :272 2026-11-22 (Andrew) overnight delegation
- Planning took the overnight decisions :276 and :277. The build session took :278 and :279 alone (S5-4). No overnight decision changed labels, thresholds or scored results. Andrew's confirmation of :276 is not recorded (S5-2)

### :273 2026-11-22 (Andrew) supervisor
- Built (692ce7e); not part of the results. ok

### :274, :275 2026-11-22 supervisor limits and status source
- Ops. ok

### :276 2026-11-23 (planning) LLM cap 900 to 1,300
- S5-2

### :277 2026-11-23 (planning) missing-state runs
- Applied: c029 README:41-51 names the 3 runs and gives both tables. A grep for "Missing" in the traces finds exactly those 3 in c029 and none in the c029b scored runs. c029b `runs/missing_state/` holds 2 runs (README:10, :40)
- Approved in inbox compound 12 (06:30), during the c029b run (03:50-07:47). Runs were set aside by kind, not by outcome
- In c029 the tree run that paused was redone (README:82), while the 3 LLM runs were scored. The treatment differs but is disclosed. ok

### :278 2026-11-23 B5 demo reuses cached remedy tracks
- S5-4. Cap: the demo ran with `--llm-cap 293` = 1,300 - 1,007. The final-now audit added 8 calls afterwards. The demo used 6 auditor calls plus its diagnostician calls, so B stays under 1,300

### :279 2026-11-23 tree reruns 38 c026 windows
- S5-4

### :280 2026-11-23 README before cut-off; final-now at cut-off
- Superseded by :283. README updated on wip/dispatcher (bc36328), not merged: S5-7

### :281 2026-11-22 flicker labels decline
- Disclosed: c029 README:79, flicker.md; the c029b proposal uses it. ok

### :282 2026-11-22 (Andrew) c029b beside c029
- Same as :270. "Candidate order" matches proposal section 3; c029b README:20 says "seed order", which is the same order. ok

### :283 2026-11-23 (Andrew) audit; final audit now
- S5-7

## Checked, no finding
- Approvals under CLAUDE.md:
  - Thresholds: k set by Andrew's rule (:255); absolute thresholds reported only
  - Budget: $15 by Andrew (:248); cap unit S5-1; cap raise S5-2
  - Deletes: :265 approved by Andrew; :242/:257 are moves inside git-ignored staging, records kept
  - Overwrites: the batch-2 windows.csv append was asked for by spec C3
  - Sources: `docs/decisions.md`, inbox files
- c029b selection rule: `labels.json`, `selected.json`; 48 candidates, 20 selected, equal
- c029b commit order: bd3c2ce < ce0a3cf < render 20:15 < 701442d < methods 03:47
- c029 commit order: :261 (14:20) < labels a9445d2 (17:07) < rule methods 17:15
- c027 restart at cap 1,300 came after the decision: after_wave.log 01:48, inbox 02:20, run_cap.log 02:50
- register_v2 bounds: preprocess.py:133, remedies.py:112
- option A k recompute: relative_k.json, 9 pairs
- Missing-state runs, grep of traces: 3 (c029), 0 (c029b scored), 2 set aside
- Gate code at the c029/c029b run commits: `git show 960cf04:agents/executors.py`; runner form `remote_job`
- Set-aside c027 records: staging/c027/run holds 8 and 12 window records
