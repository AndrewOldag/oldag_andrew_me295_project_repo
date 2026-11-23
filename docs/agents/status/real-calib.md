# real-calib
Updated: 2026-11-23 14:45 (local)
Lane: course
Branch: wip/zone-checks
Last inbox item done: 30
State: ready to merge
Now: c034 done; results/2026-11-23_zone_checks/README.md
Done since last update:
- Proposal before any run (e385ae2); amended before any v4 or real record: plateau tip speed along the midline, not the tip's world path (bending turns the tip; f5cc997)
- checker/zone_checks.py, tests 10 passed; thresholds from 18 freeze v4 clean tracks committed before the real run (3cf728b)
- Synthetic: particle path flags 15 of 15 at every shift (+-15, 30, 60 px); plateau 0 of 15 (v4 zone reaches the basal third); 0 false alarms on 18 clean and 9 repaired
- Real, 1,186 c027 windows computed: every accepted window flagged at the synthetic thresholds (pp_rms_rel median 7x the threshold); large residuals are the first chain point's distance from the midline tip changing over the window. Report-only, no outcome changed
- Tests 487 passed, 3 skipped; test_board.py 2 failed on main's c033-audit.md host field (not this branch)
Needs Andrew:
- none for merge. Option for planning: a real threshold would need a real reference set and approval; not done
- wip/supervisor (c032) still ready to merge, unchanged
