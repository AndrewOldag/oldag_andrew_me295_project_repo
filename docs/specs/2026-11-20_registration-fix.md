# Spec: registration fix, track-integrity check, all tracking on the cluster

From: planning account. Date: 2026-11-20. Approved by Andrew 2026-11-20. Lane: course. Adds to spec 2026-11-18.

## Why
- A window failing closure (22.8 px/h, gate 19) was "repaired" by `register_frames`: final rotation 9.23 deg, shift 100.6 px; closure on the retrack 14.0 px/h, accepted. On the registered frames the tracker lost the tissue: by 7.98 h neighbour spacing 1-166 px and lateral scatter about 18 px (3 px on the base track). Closure is one summed value and does not see point order
- Likely cause, not yet shown: `measure/preprocess.py` `register_frames` chains pairwise ECC fits, $C_t = E_t \cdots E_1$, so small per-pair errors accumulate over 80 frames. The fitted motion is about twice the drift the closure miss implies (22.8 px/h over 2 h, about 46 px)
- `register_frames` is the tree's first closure remedy, so it touches most repaired windows (c022, c026, c027)
- The VM is short of memory and cores. Andrew, 2026-11-20: all tracking, sweeps and retracks go to the cluster; the VM runs the Claude sessions, LLM calls, git and the checker only

## Budget
- Andrew, 2026-11-20: stop at $15 total since 2026-10-23 (was $12). Ledger check before every submit as before

## R. Registration and integrity (real-calib, c031)
1. Diagnose on the flagged window first: per-pair rotation and shift, ECC value per pair, cumulative path; and the same window registered directly to frame 0. Report which explains the 9.23 deg. Results in `results/2026-11-20_registration_fix/`
2. Fix `register_frames`, new settings tag (`register_v2`), tracks with the old tag never reused:
   - each frame registered directly to one reference frame (frame 0), initialised from the previous frame's fit; no chaining
   - plausibility bound: if the fitted motion of the last frame exceeds what the closure miss allows (implied tip drift over the window, times 2), or the rotation exceeds 2 deg, the remedy returns `not plausible` and is rolled back
   - tests: chained vs direct on a synthetic rod with known rigid drift; a pure-growth rod gives near-identity; the bound trips on an injected 9 deg rotation
3. Track-integrity check in `checker/checks.py`, deterministic, no LLM: (a) order of points along arc length kept in every frame (count of inversions); (b) largest neighbour gap over median gap; (c) lateral scatter of centre points from the midline. Reported on every track; gates only tracks made by a remedy (a remedied track that fails it is rolled back)
4. Thresholds by a fixed rule, committed before any real window is checked: from clean synthetic rods (freeze v4 seeds, all fault-free and repaired-correct tracks), the 99.5th percentile of each value times 1.5; inversions threshold 0. Then the same rule's values reported on batch-1 base tracks as a sanity check, not used to set anything
5. Synthetic regression: rigid-drift rods of freeze v4 with `register_v2`; repair outcome against truth vs the old remedy. All tracker runs on the cluster CPU through `retrack_queue.py`
6. Proposal before any run (items 1-5, thresholds rule), committed; no stop for approval. Decisions, log, ready to merge

## Cluster for everything (dispatcher, compound)
- dispatcher: put `scripts/retrack_queue.py` and its tests on a new branch `wip/retrack-queue` from `origin/main` (that change only), status ready to merge, so real-calib and compound can use it. Registration hold stays until `register_v2` is on main; then submit `register_v2` retracks for every window whose decision used or needs registration, and rescore those windows (c022, c026 and c027 records kept; new records under the c027 run). Integrity gate applied at every remedy step from then on
- compound: stop the VM label sweep after its current run; finished runs stay cached. Remaining c029 tracker runs as cluster CPU arrays (many runs per array task, to keep task count low), through `retrack_queue.py`. Rods are rendered on the VM and pushed to the cluster folder; equivalence first: 2 rods tracked on the cluster equal the VM tracks (within 1e-6 px). c030 LLM runs stay on the VM, one at a time
- At most one LLM run on the VM at a time across all sessions when free memory is under 3 GB

## Limits
- As in spec 2026-11-18. Cluster folder at most 30 GB. No deletes on the lab server
