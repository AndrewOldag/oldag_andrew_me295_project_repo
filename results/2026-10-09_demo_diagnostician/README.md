# Diagnostician demo on a made-up task, 2026-10-09

README added 2026-11-23 (c033 audit S6-3). Trace written 2026-10-09 (697d718, refreshed in df38612).

## Run
```
python scripts/demo_diagnostician.py
```
- Agents env, live model calls (model pinned in `config/models.yaml`). Writes `results/<today>_demo_diagnostician/trace.jsonl` and prints the outcome, call count, tokens and call time
- The task and every executor answer are invented to exercise the loop (`scripts/demo_diagnostician.py` docstring). Not data, not an evaluation case. Hidden cause: per-frame displacement larger than the patch radius; only `change_frame_stride` `half` fixes it

## Files
- `trace.jsonl`: one line per orchestrator step and one task_end line. This trace: 3 steps (request_info displacement_vs_patch_radius; apply_remedy change_frame_stride half; accept)
