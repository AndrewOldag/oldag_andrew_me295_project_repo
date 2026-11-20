# Held-out compound and novel faults

From: build account, session compound. Date: 2026-11-20 (spec dated 2026-11-18). Spec `docs/specs/2026-11-18_lab-report-4.md`, section D; task c029. Branch `wip/compound`. Committed before any sizing, label or method run. No stop for approval; nothing below changes after the first result is seen.

## 1. Faults (`measure/render_compound.py`)
- Injected on `v3_growth_zone` (freeze v4 geometry: 768 x 320 px, 41 frames 90 s apart, tracked length 500 px)
- Compound faults: two faults at their freeze v4 sizes in one movie. The remedy tree has a branch for each component, none for the pair

| Fault | Components (v4 sizes) | What it tests |
| :-- | :-- | :-- |
| `drift_low_texture` | rigid_drift 0.5 + low_texture 0.03 | a repairable fault hidden under an unrepairable one |
| `second_root_occlusion` | second_root 30 px + partial_occlusion 20 px (drop drawn over both roots) | two decline faults on the same zone |
| `drift_jitter` | rigid_drift 0.5 + midline_jitter 3 px | a repairable fault with a midline fault |
| `low_texture_fast` | low_texture 0.03 + displacement_exceeds_patch 2x6 | two faults with competing remedies (larger patch, smaller stride) |

- Novel single faults: not in the agents' fault list, not in the remedy tree
  - `focus_drift`: Gaussian blur rising linearly from 0 px at frame 0 to `size` px at the last frame. A real cause: the focal plane drifts as the root grows or the plate settles
  - `illumination_flicker`: every frame (background and root) times a gain 1 + size x N(0, 1), own random stream, clipped to 0.5-1.5. A real cause: lamp or LED intensity varying between frames
- With no fault the movie equals `render.render` exactly; each compound movie equals the movie of its components rendered by `render.py` or `render_heldout.py`, where those can render it (`tests/test_render_compound.py`, 13 tests)

## 2. Rods and seeds
- 6 faults x seeds 40-43 = 24 rods. Seeds 40-43 and 50-51 have not been used before (`config/scoring_seeds.yaml`, earlier results)
- Novel-fault sizes, before the labels: candidates focus_drift 3, 6 px; illumination_flicker 0.1, 0.3. Sizing seeds 50-51, unremedied only (16 tracker runs). Rule: the smallest candidate at which the checker fails on both sizing seeds; if none does, the largest candidate. Written to `sizing.md` and `sizing.json`

## 3. Expected outcomes (written before the labels; the labels decide)
- Compound faults: decline. Each pair contains a fault whose v4 label is decline (low_texture, second_root, partial_occlusion, midline_jitter, displacement_exceeds_patch)
- focus_drift: decline (texture lost late in the window, as low_texture)
- illumination_flicker: accept_clean (the tracker's correlation is normalised; a global gain should not move the tracks)
- Fault names counted correct (reported, not a main metric): any component's name; `low_texture` or `unknown` for focus_drift; `unknown` or `low_texture` for illumination_flicker

## 4. Labels (spec D2): tracker-only sweep, `scripts/synth/heldout_compound.py label-sweep`, then `labels`
- States per rod: unremedied; every single remedy step of the action schema (`agents/actions.py` `REMEDIES`, 9 steps); every pair of steps of two different remedies, applied in schema order (register_frames first, so its band start comes from the unremedied run). Settings from `measure/remedies.py` `apply_remedy`, as the agents use them. A step the remedy code refuses (half the stride at stride 1) gives no state. `use_width_free_ratio` needs no tracker run
- Tracker runs: 27 tracked states per stride-1 rod, 34 per stride-6 rod (low_texture_fast); each run on the rod and its rigidly moved copy. About 1,350 runs
- Label rule: freeze v4 (`measure.score.label_rod`, C3 option a: a check not computable after a remedy fails; scoring tolerance `config/scoring_tolerance.yaml`). accept_clean: the unremedied run passes all three checks and is good. accept_repaired: a state of one or two steps passes and is good; the repairing states are listed. decline: neither
- The labels are committed before any method runs; the driver refuses method runs until `labels.json` is committed
- Open with the TAs (spec D5, Andrew): whether labels from a tracker-only sweep are acceptable for compound faults. Proceeding with them; stated in the README

## 5. Methods (spec D3)
- Fixed script, remedy tree (step limit 8), diagnostician, single agent without the checker. Freeze v4: candidate v4 on, prompts `diagnostician_v4.md` and `single_agent_v4.md`, model `claude-opus-5-5`, Claude Code 2.1.310, step limits from `config/models.yaml`. No change to prompts, thresholds, remedies or settings
- 3 repeats for the LLM methods (72 runs each), one run for the rule methods. Order: repeat 0 diagnostician, repeat 0 single agent, then repeats 1 and 2
- LLM cap 450 (spec D3), counted as agent runs, as in freeze v4 ("LLM runs") and auditor v1 ("one call = one auditor run"). Planned 144. The `claude -p` calls (agent steps) are reported beside it
- A state an agent or the tree asks for that the label sweep did not run (three or more steps) is rendered and tracked on demand on the VM and counted
- At most one LLM run at a time from this session (spec: at most 2 on the VM, with dispatcher). Free VM memory at least 3 GB before every tracker run and every LLM run, else wait
- Runs ended by the account session limit are set aside and rerun, not scored (as freeze v4)

## 6. Metrics (spec D4), as freeze v4 (`measure/metrics.py`)
- Correct-outcome rate per class and balanced accuracy, false accepts (count per repeat and rate), repair correct (accept_repaired rods accepted with a good measurement), agreement across repeats (unanimity, Fleiss kappa), fault named correct, steps, tokens, call time
- References: all-decline and all-accept
- Results `results/2026-11-18_heldout_compound/`: `README.md`, `sizing.md`, `labels.md`, `labels.json`, `table_metrics.md`, `metrics.json`, `scores.json`, `runs/`

## 7. Where the runs happen
- VM only. Renders and tracker runs on the VM with the tracker env and the tracker commit the freeze runs used (d5f1829), source exported to `staging/qb_tracker` (git-ignored). `scripts/synth/local_qb.py` runs `make_rod.py` and `qb_track.py` there. The VM tracker env has no torch; `qb_track.py` imports it only to set its thread count, and the CPU tracking path does not use it, so a stand-in module with the thread calls is used
- Equivalence, before any run of this set: freeze v4 rod `v3_growth_zone_clean_s26`, rendered and tracked on the VM, against the v4 cache: truth arrays differ by at most 6.9e-18, tracks by at most 4.2e-13 px (limit 1e-6, as 2026-10-23). `scripts/synth/local_equivalence.py`
- Renders in `staging/rods_c029`, tracks in `staging/tracks_c029` (VM, git-ignored). The renders are deleted after the method runs; the tracks are kept
