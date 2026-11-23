# dispatcher
Updated: 2026-11-22 16:43 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 55 (item 46, task c027, still working)
State: working
Now: c027 cycle running detached (register_v2 and remaining retracks, status line after every group); the run restarts by itself when the wave is done
Done since last update:
- Auto 11-22 16:43 (from logs): run 1189 records, accept by rule 1034, decline by diagnostician 23, decline by rule 58, paused 74; LLM calls 491; run ended: done; windows this start 74; LLM calls 491. Queue 442 tasks: done 3, failed 12, fetched 415, submitted 12; cycle last:  
- Item 55: main merged (option A gate, rod-jobs). `integrity_gate(relative_integrity(remedied, base, load_relative_k()))` wired into `Slice.apply_remedy`, which the diagnostician and the remedy tree both use; a failure rolls back as `rolled back: integrity: <change>`; test added. Suite 445 passed, 3 skipped
- Gate applies to tracker tracks only: on a field-level synthetic rod (in-process runner) the base lateral scatter is exactly 0, the ratio is infinite and every midline remedy fails (`test_info_p1_p5` failed that way). Real-calib may want to handle a zero base in `relative_integrity`
- Remedy hold lifted. A failing window now waits, before any LLM call, until every one of its single-remedy tracks is cached (register_v2 is not yet), so no calls are spent twice
- Cycle started 14:34: 0727_cc7 leftover in c019 cleared after its md5 check (9 output files, 4.7 GB, c019/DELETED.log); g016 fetched (24 tracks, md5 checked); g017 submitted, the first register_v2 group (4 tasks, array 7841537), 2 fetched
- Fixed: `stage_root`'s cap check refused 0714_c4 (the cluster copy is larger than the storage `du`); packing now uses 1.1 x and a refusal submits the roots already staged; test (queue tests 16 passed)
- Run: 1,189 records: 1,034 accepted by rule, 58 declined by rule, 23 declined by the diagnostician with no remedy tried, 74 paused (the 12 held records among them). 55 roots audited; LLM calls 491 of 900
- Detached `after_wave.sh` reruns run_all.py when the cycle logs `wave done`: paused windows from step 0 with the diagnostician and the gate, then the auditor runs of the roots that become complete (the 8 held roots among them)
- Cluster folder 28.5 GB of 30 GB at 14:28 (before g016's clear). Ledger spent $7.630
Needs Andrew:
- Keep the cluster master up until the cycle logs `wave done` (about 100 register_v2 and 120 other retracks left, in groups of 3-4 roots)
