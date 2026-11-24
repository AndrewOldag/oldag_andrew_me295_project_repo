# Held-out faults: checker-only sizes, 2026-10-12

README added 2026-11-23 (c033 audit S6-3). Results written 2026-10-12 (fe7dda1). Proposal: `docs/proposals/2026-10-12_heldout-faults.md`.

## Run
```
python scripts/synth/heldout_sweep.py start      # tracker machine, own code folder, sweep lock
python scripts/synth/heldout_sweep.py status
python scripts/synth/heldout_sweep.py fetch      # to staging/tracks_heldout/
python scripts/synth/heldout_sweep.py eval --out results/2026-10-12_heldout_faults
```
- Rods: growth_zone, seeds 0-2, 5 held-out faults (second_root, fast_rotation, bad_stage_correction, flank_swap, partial_occlusion; `measure/render_heldout.py`), 9 fault sizes in all; unremedied, uncoupled. 54 tracker runs, 0 failed, 204 s wall on 4 workers
- Checker only, no agent. Thresholds `config/checker_thresholds.yaml` (approved 2026-10-10)

## Files
- `checker_sizes.md`: per fault and size, seeds failing the checker and the checks that fail
- `checker_sizes.json`: the same rows with the check values
