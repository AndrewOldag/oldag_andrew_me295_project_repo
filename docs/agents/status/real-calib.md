# real-calib
Updated: 2026-11-21 11:20 (local)
Lane: course
Branch: wip/real-calib
Last inbox item done: 25
State: ready to merge
Now: item 25 ready to merge; R1 per-pair sbatch next (item 24); R5 waits for compound's rod job kind on main
Done since last update:
- Merged origin/main (74e6d15)
- Item 25, option A gate: checker `relative_integrity` (with `integrity_gate`), `config/integrity_relative_k.yaml`; k from the 9 freeze v4 repaired/base pairs: inversions 1.5, gap ratio 1.5, lateral 3.0; tests; committed before any real remedied track was scored
- Check on 44 c027 register_frames v1 tracks against their base tracks: batch 1 1 of 7 pass, batch 2 16 of 37; flagged 0711_c5__w6-8 fails (inversions ratio 200, lateral 14.9). Its v2 track is not back yet. results/2026-11-20_registration_fix/
- Dispatcher: the option A gate is ready to merge on wip/real-calib. At each remedy step: `integrity_gate(relative_integrity(rec_remedied, rec_base, load_relative_k()))`; False -> roll the remedy back. Absolute values (`track_integrity`) stay reported, not gating
Needs Andrew:
- none
