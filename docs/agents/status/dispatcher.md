# dispatcher
Updated: 2026-11-23 17:06 (local)
Lane: course
Branch: wip/audit-fixes
Last inbox item done: 60
State: working
Now: inbox 61 (c036): S2-1 report-only impact running (detached, scripts/integrity_impact.py over c027, c029, c029b, freeze v4 caches); then results README, log, ready to merge
Done since last update:
- S1-3, S1-4: 61 files masked (scripts/mask_bio.py), report masker covers strain_rate, tests/test_no_real_bio_values.py; suite 501 passed, 3 skipped (1b6074c)
- S2-1: integrity gate fails frames with < 3 centre points (new integrity_lost_frames), measures gaps and order across lost points, fails NaN values; 5 new tests (97846cf)
- S3-1: real frame_quality reference from the 23 in-rule windows (0.0641/0.0439, 0.0285/0.0213); impact: 2 of 102 scored frame values between old and new median, no outcome changed (20e5af3)
- S6-3, S7-1, S7-2: READMEs for demo_diagnostician and heldout_faults; full run_batch commands; real-subset report/agreement read staging, --out; reproduce committed files (ccd1d56)
- Status times 17:40 and 18:10 in earlier pushes were wrong (clock misread); real times from now on
Needs Andrew:
- docs/proposals/2026-10-23_real-midline-smoothing.md:7 flank-difference range masked; audit asks Andrew to rule whether it is a check value (unmask) or biology (keep masked)
- Before the history rewrite: the real-subset traces and summaries (035e8fc) exist only in git history and the VM copy staging/c019/real_subset_runs/; keep a private copy if wanted
