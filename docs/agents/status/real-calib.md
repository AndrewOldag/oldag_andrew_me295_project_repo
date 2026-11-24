# real-calib
Updated: 2026-11-23 20:58 (local)
Lane: course
Branch: wip/zone-reference
Last inbox item done: 32
State: working
Now: inbox 33 (c035): overlays for windows 25-150 running as a detached job (about 25 s per window, about 50 min); started 20:55. Rerun of the same command resumes from the PNGs made
Done since last update:
- Extension rule in `docs/proposals/2026-11-23_zone-reference.md` before the draw (c452959): seed 20261124, largest remainder 45/5/36/33/7, at most 2 windows per root counting the first 24
- `scripts/zone_reference.py extend`; labels.csv rows appended in sample order, existing labels kept; tests 6 passed (9cb2a3e)
- Refactored draw reproduces the first 24 exactly; extension drawn: 150 windows, all strata full, no root over 2 (b7d30ac)
- Andrew's 24 labels kept as written; no threshold computed
Needs Andrew:
- none yet. When all 150 overlays exist: label windows 25-150 (status will say)
