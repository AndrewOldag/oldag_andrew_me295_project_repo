# real-calib
Updated: 2026-11-20 23:10 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 23
State: ready to merge
Now: item 22 (c031) code parts ready to merge; R1 per-pair job and R5 wait (see Needs Andrew); no tracker run, cluster job or LLM run this pass
Done since last update:
- Merged origin/main (08de5b4). Tests 421 passed, 3 skipped; register tests 5 passed in the tracker env (240 x 240 synthetic arrays, no tracking)
- Proposal before any run; flagged window 0711_c5__w6-8 (c027, st1_reg2p1075)
- R3 integrity check (336be10): flagged registered track 798 inversions, gap ratio 6.43, lateral 15.26 px; its base track 3, 1.76, 1.03 px
- R4 thresholds by the rule (4ec36af): inversions 0, gap ratio 2.4, lateral 0.081 px. Batch-1 base tracks: 0 of 115 pass all; lateral 0 of 115
- R2 register_v2 (ea255ed, wiring commit after it): direct to frame 0, bound on band motion and rotation; synthetic test direct 0.03 deg vs chained 1.2 deg error. register_frames remedy now gives v2 (tag regv2p<from>b<bound>); v1 tags, args, dicts, description unchanged
- R1 scripts/remote/register_diag.py written and tested (chain equals register_frames), not run
- results/2026-11-20_registration_fix/README.md, decisions, log entry, task c031
- Compound and dispatcher: register_v2 (measure/preprocess.py, measure/remedies.py, qb_track.py) and the integrity check (checker track_integrity, integrity_gate, config/integrity_thresholds.yaml) are ready to merge on this branch. Gate not usable on real tracks until the lateral question below is settled
Needs Andrew:
- Lateral threshold: the fixed rule gives 0.081 px from synthetic rods; real base tracks have median 1.37 px (synthetic midlines are the render's own, real ones come from the net). As a gate every remedied real track would be rolled back. Options: keep the rule (gate rolls back everything), drop lateral from the gate (report only), or a new rule on real base tracks. Inversions 0 also fails 40 of 115 base tracks
- R1 per-pair run: register_diag.py needs one cluster CPU job; retrack_queue.py has no job kind for it. Add a 'diag' kind (dispatcher's file) or one sbatch through the relay?
- R5 waits for register_v2 on main (register hold; code folder synced from main) and compound's synthetic-rod job kind
