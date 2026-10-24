# autotrace
Updated: 2026-10-23 20:31 (local)
Lane: course
Branch: wip/autotrace
Last inbox item done: 2
State: working
Now: item 3, net on the 140 pack frames (workstation, nice 19, 10 threads, about 14.5 s per frame; 44 of 140 done at 20:29)
Done since last update:
- Item 2, landmark (as before): drafts end on the midline 35 px behind the apex; July traces run tip -> base
- Draft converter: picks the valley component that ends nearest the net tip (tip_val >= 0.3), else the largest; trims a skeleton end that curls back; apex = net tip when confident and within 120 px of the midline end, else the classical darkness mask walked out to the first background gap
- Net tip vs mask apex on the first 28 frames: 20 frames, median 5.9 px, max 12.5 px
- Items 6-7 tools written: review_traces.py (y/n/b/q, skips held-out, review.csv after every key, resumable), apply_review.py (traces_reviewed.json, non-held-out only, keeps hand traces on re-run, --frames-root for a local copy)
- 3-frame test (+1 held-out), headless: resume, last decision wins, held-out skipped and listed, hand trace kept, trace_midlines.py opens both output files: all passed. MacOSX backend not testable here
Needs Andrew:
- none yet
