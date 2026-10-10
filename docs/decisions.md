# Decisions log

One entry per decision: date, decision, reason. Decisions made before this repository was created are recorded outside it.

- 2026-10-09: Review launcher `open_review.bat` finds Python from `ME295_PYTHON`, then the `me295` conda env, then `python` on PATH. Reason: the repository must not name paths outside itself
- 2026-10-09: Review app movie player uses pre-made frames every 15 min with the elapsed time printed on each, made by `scripts/manifest/make_scrub.py`. Reason: the 2 h GIF was too coarse to see when a root leaves the frame; a slider with time sets usable windows directly
