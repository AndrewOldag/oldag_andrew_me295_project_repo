# autotrace
Updated: 2026-10-23 21:20 (local)
Lane: course
Branch: wip/autotrace
Last inbox item done: 10
State: waiting on Andrew
Now: review set ready in the tracing pack folder, `review/` (lab data root, `me295/tracing_pack_20261023/review/`); waiting for Andrew's y/n and hand tracing. Nothing fine-tuned
Done since last update:
- Item 2, landmark rule: drafts end on the midline 35 px (74 um) behind the root apex. Measured on 9 July frames: median 35.3 px, range 23.4-63.5 px; 1 frame excluded (mask merged with a bubble). July traces run tip -> base; drafts run base -> tip as the inbox says
- Item 3, drafts: 140 of 140 frames; net found no root on 0. Run time: net 2338 s (16.7 s/frame, CPU, nice 19, 10 threads), conversion 81 s, previews 36 s
- Apex: net tip in 104 frames, root mask in 36; net tip vs mask apex median 5.0 px. Flags: 5 curled skeleton ends trimmed, 2 mask apex far ahead (#15 bubble at the tip, #135 crossing fibre); both show the flag in yellow on the preview
- Items 4, 9: 28 held-out frames (16 roots) drafted with review_only; previews `HELDOUT_TRACE-BY-HAND_<n>_<key>.png`, 40 px red border, banner; skipped by the review tool and listed at its end; `HELD_OUT_TRACE_BY_HAND.csv` and `held_out_worklist.json` (28 frames)
- Item 5: 140 previews (1200 px wide), `index.csv`; "||" in keys is "__" in file names
- Item 6: `review_traces.py` (y/n/b/q, k of 112, review.csv after every key, resumable, `--backend MacOSX`), `apply_review.py` (traces_reviewed.json with non-held-out frames only, accepted drafts as traced, keeps hand traces on re-run, `--frames-root` for a local copy). `README.txt` in the folder gives the steps
- Item 7: both tested headless on 3 frames + 1 held-out: all checks passed. MacOSX backend not testable here
- Item 10: nothing large on the VM (previews viewed as small samples in the session temp folder only); workstation work folder 11 GB of 20, 35 GB free; no deletes anywhere
- Results README `results/2026-10-23_autotrace/README.md`; log entry `docs/running_log_pending/autotrace.md`
Needs Andrew:
- Review: copy `review/` next to your pack copy, then `python review_traces.py . --backend MacOSX` (112 frames), then `python apply_review.py . --frames-root <your frames folder>`
- Hand-trace rejected frames (traces_reviewed.json) and the 28 held-out frames (held_out_worklist_local.json) with trace_midlines.py
- Two-root frames (#48, #49 held out; #57): the draft follows one root; check it is the one you want
- Data-use rule: net2_midline_ft.pt was fine-tuned on 115 July traces, 43 of them from roots not include-yes (c1, c7 no; c3, c12 unsure), 4 of those after the usable window (c3 19.4, 21.7, 24.0 h; c12 24.0 h). It is the accepted real-movie midline source. Proposed: the planned fine-tune starts from base net2 and uses only include-yes, in-window traces (72 July + reviewed pack); results from the current net stay provisional until then. Decide
- Say if drafts should run tip -> base like the July traces (order does not change the fine-tune)
