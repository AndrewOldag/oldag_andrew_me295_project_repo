# compound
Updated: 2026-11-23 04:55 (local)
Lane: course
Branch: wip/compound
Last inbox item done: 11
State: working
Now: item 10 step 4: c029b LLM methods running (detached runner from 03:47, now diagnostician repeat 2; 83 of 120 LLM runs written); arrays 7908864 and 7908996 queued for paused states
Done since last update:
- Array 7902231 fetched, 6 of 6, 0 failed; rules rerun: remedy tree 2 paused runs redone from step 0; 1 paused again on a further state (low_texture_fast s60 st1_r21)
- Arrays submitted after ledger check: 7908864 (2 runs, drift_low_texture s61 register_v2 state), 7908996 (2 runs, low_texture_fast s60 st1_r21); spend $8.25 of $15 before these, worst case $0.048
- Rule-method runs committed: script 20 of 20, remedy tree 19 of 20 (8b4e232)
Needs Andrew:
- Keep the cluster connection master open until arrays 7908864 and 7908996 are fetched
- Decision: LLM runs whose remedy needs a state not cached do not pause; the agent gets a "Missing" tool error and finishes the run. c029b: 2 runs so far (diagnostician drift_low_texture s61 r0, r2). c029: 3 runs (diagnostician drift_jitter s40 r1; single agent low_texture_fast s42 r1, s43 r0), committed and reported as they are. Proposal: c029b set these runs aside in runs/missing_state/ (kept, not scored) and redo them from step 0 once the state is fetched; c029 stays unchanged, with one line naming the 3 runs in its README. Until you answer, both are kept and scored as written, and the count is reported beside the metrics
