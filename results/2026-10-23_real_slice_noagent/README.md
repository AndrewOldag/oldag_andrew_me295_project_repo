# Real slice without agents: 0708_m12, 4-6 h

Command: `python scripts/real_slice.py --no-agent --out results/2026-10-23_real_slice_noagent` (dispatcher script baseline, tracker on the compute host, checker). Branch wip/dispatcher, 2026-10-23.

- Dispatcher (script): finish in 1 round; 1 window, collected
- Tracker: net midline (tile mode, fine-tuned net2, low 0.1 %), stage-corrected tracker 52e9bd1, uncoupled, 400 px tracked, 80 frames
- Checker: closure 0.945 px/h, pass (threshold 1.0); plane_sections 134 %/h, fail (threshold 3.25; expected, midline curvature noise); rigid_invariance not run (no rigidly moved copy for real movies)
- Diagnostician and auditor not called: the installed Claude Code (2.1.310) differs from the pin in `config/models.yaml` (2.1.302); the launcher refuses. The re-pin is on wip/freeze-v3, not yet on main
- `summary.json`: dispatcher summary, initial and final checks, settings, runner log (load and free space before and after the run)
