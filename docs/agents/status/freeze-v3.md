# freeze-v3
Updated: 2026-10-23 15:15 (local)
Lane: course
Branch: wip/freeze-v3
Last inbox item done: 6
State: waiting on Andrew
Now: labels done; stopped on a stop rule (clean scored rod not accept_clean). No method run, no tag yet
Done since last update:
- Item 5: work space freed (read); item 6: runner starts a job only with fewer than 2 jobs of this account and 1-min load below half the cores (e454378); suite 243 passed, 5 skipped
- Held-out sizing at v3 geometry: 36 tracker runs, 0 failed; all six faults fail 3 of 3 at the v2 sizes; no size changes (f599564)
- Labels of the 51 scored rods: 228 tracker runs in 2 sweeps, 0 failed, 663 s and 315 s wall, load at most 6.02 on 32 cores, work space 5.4 -> 8.0 GB. Tracker runs used 364 of 600 (6ebc9db, `results/2026-10-23_freeze_v3/labels.md`)
- Classes: accept_clean 17, accept_repaired 12, decline 21, clean_fails 1. All-decline would score 21 of 51 (under half: that stop rule holds)
- Differs from expected (4 rods): `v3_bend30_clean_s20` and `displacement_exceeds_patch` 2x6 s20-s22
Needs Andrew:
- STOP, clean scored rod `v3_bend30_clean_s20` (30 deg/h, the rate above the reported range): closure 4.51 px/h (threshold 1.0); rigid_invariance 1.14 and plane_sections 1.50 pass; measurement good (centre 0.44 vs 1.35 %/h, flank 0.35 vs 1.00). A checker false alarm; the 5 basis seeds of the same rod reached at most 0.36. Choose: (a) keep it as accept_clean (accepting the good measurement is correct; methods that trust the checker score it wrong; reported as a checker false alarm), recommended; (b) label it by the repair criteria like a fault rod (remedy states run, about 10 tracker runs); (c) drop it (set of 50)
- For information, no stop: `displacement_exceeds_patch` 2x6 is not repairable at v3 speed (stride 6 -> 3 -> 1 leaves rigid_invariance 52-126 %/h at 4.8 px/frame); labels win, as in v2. accept_repaired is 12 rods, not 15
