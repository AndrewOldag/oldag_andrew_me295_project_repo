## 2026-10-23 (build account, session freeze-v3)
- Done, item 1: status and task c011 started (first commit on `wip/freeze-v3`)
- Done, item 2: `docs/proposals/2026-10-23_freeze-v3.md`. Scoring set 48 rods on new seeds 20-22: accept_clean 15, accept_repaired 15, decline 18 (expected; labels from a tracker-only sweep). All-decline 18 of 48, balanced accuracy 1/3
- Proposal: metrics in `measure/metrics.py` (per-class accuracy, balanced accuracy, false-accept rate, coverage, abstention precision and recall); 3 repeats per rod for the LLM methods, unanimity rate and Fleiss kappa
- Proposal: v3 rods at 2.105 um/px, tip 96 px/h (2.4 px/frame, from the timing run on `wip/dispatcher`), growth zone s_mid 200 px, width 45 (peak REGR 54.0 %/h at 421 um, zone 543 um; computed from `measure.rod.richards_velocity`), tracked length 500 px, stage follows the tip every frame; bent rods 16, 20, 24 and 30 deg/h
- Proposal: kinematics-1, width-free ratio corrected for curvature (exact on field-level rods); not dropped. Claude Code 2.1.302 recorded in v3. New held-out injector `stage_log_missing`
- Proposal: about 490 tracker runs (over the 300 limit; asks a cap of 600), 288 LLM runs. No run made
- Demo: `cat docs/proposals/2026-10-23_freeze-v3.md`
- Remaining: Andrew approves or changes the proposal (5 open items); then implement, clean basis check, held-out sizing, labels, tag `freeze-v3`, rerun all methods, results README
- Bottlenecks: proposal approval (Andrew); tracker-run cap above 300 (Andrew)
