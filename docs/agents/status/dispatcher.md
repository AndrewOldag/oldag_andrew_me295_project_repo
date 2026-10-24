# dispatcher
Updated: 2026-10-23 22:40 (local)
Lane: course
Branch: wip/dispatcher
Last inbox item done: 17
State: waiting on Andrew
Now: item 17 done: fit failed its validation (not adopted); real slice ran end to end with agents
Done since last update:
- Item 17, fit: `measure/midline_fit.py` (residual 0.289 px rms), test 4 passed. v3 validation FAIL: 164 of 241 runs within 1e-3; all bending (0/54), width-change (0/6) and midline-jitter (0/15) rods changed; max change closure 1.14 px/h, plane_sections 10.7 %/h; 3 pass/fail flips (bend30 s12 plane_sections pass -> fail twice; one midline-jitter closure fail -> pass). Not adopted; rule not retuned. `results/2026-10-23_midline_fit_validation/` (b972c29)
- Item 17, for information (provisional): real t3 with the fit, plane_sections 134 -> 36 %/h; still about 10x the threshold
- Item 17, re-pin: main merged (2.1.310); check_cli OK; suite 234 passed
- Item 17, real slice with agents (provisional net): dispatcher agent 2 rounds -> tracker -> checker (closure 0.945 pass, plane_sections 133.6 fail) -> diagnostician (smooth_midline light; plane_sections 25.9, closure 2.857; decline, midline_jitter) -> auditor (0 accepted; report). `results/2026-10-23_real_slice/`
- Fixed: the auditor cannot be called with no accepted run (empty id list is not a valid schema); the slice script then offers request_info and report only (audit/llm.py unchanged)
- All real-movie numbers from the current fine-tuned net marked provisional in results
Needs Andrew:
- Plane sections on real movies after option 1 failed: no option now meets the "unchanged within 1e-3" criterion. Options: a criterion limited to the rods the fit should not affect, a smaller residual budget (a new rule, set before any real result), or accept that plane sections is not used on real movies for now
- Note: the diagnostician's smooth_midline light remedy on the real window lowered plane sections (133.6 -> 25.9 %/h) but broke closure (0.945 -> 2.857 px/h)
