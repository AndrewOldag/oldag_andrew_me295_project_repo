# Held-out supplement c029b: milder compound and novel faults

Andrew, 2026-11-22 (inbox compound item 10). Written and committed before any rod of this set is rendered.

## 1. Why
- c029 does not separate the methods: 20 of 24 labels are decline, and all-decline scores 20 of 24
- c029b adds rods a single remedy could plausibly repair, so the methods can be scored on repair and on false declines
- c029's rods, labels and results stay as they are and are reported unchanged. c029b is reported beside c029, never merged into its numbers

## 2. Faults
Same six kinds as c029, milder. Renderer `measure/render_compound.py`; the compound sizes are new entries (`MILD`), c029's entries do not change.

| Kind | c029 | c029b | Rod fault name | Single remedy expected to repair |
| :-- | :-- | :-- | :-- | :-- |
| drift + low texture | rigid_drift 0.5 + low_texture 0.03 | rigid_drift 0.5 + low_texture 0.2 | `drift_low_texture_mild` | register_frames |
| second root + occlusion | second_root 30 + partial_occlusion 20 | second_root 10 + partial_occlusion 5 | `second_root_occlusion_mild` | crop_or_mask/mask_second_root |
| drift + jitter | rigid_drift 0.5 + midline_jitter 3 | rigid_drift 0.5 + midline_jitter 0.5 | `drift_jitter_mild` | register_frames |
| low texture + fast | low_texture 0.03 + displacement_exceeds_patch 2x6 | low_texture 0.2 + displacement_exceeds_patch 1x4 | `low_texture_fast_mild` | change_frame_stride/half |
| focus drift | 3 px | 1.5 px | `focus_drift`, size 1.5 | enlarge_patch/1.5x |
| illumination flicker | gain std 0.1 | gain std 0.03 | `illumination_flicker`, size 0.03 | enlarge_patch/2x |

- Sizes in the units of c029's proposal. low_texture keeps its blur 2 px and noise 40. second_root size: how far the second root's outline ends past the main root's near edge (smaller is milder). displacement_exceeds_patch `FxK`: tip speed F times the base, analysis stride K
- Basis: rigid_drift 0.5 alone is repaired by register_frames (freeze v4 labels). At speed 2 the halved stride still failed rigid invariance (freeze v3.1 sizing), so the fast component keeps speed 1 at stride 4. Flicker: the tracker matches raw intensity (`results/2026-11-18_heldout_compound/flicker.md`); 0.03 is a third of c029's size. The other sizes are guesses; the labels decide
- No new sizing sweep

## 3. Rods and seeds
- 6 kinds x seeds 60-67 = 48 candidate rods, v3_growth_zone, each with its rigidly moved copy. Seeds 60-67 have not been used before (c029: 40-43, 50-51)
- Candidate order: seed, then kind in the table order above (seed 60 drift_low_texture_mild, seed 60 second_root_occlusion_mild, ..., seed 67 illumination_flicker)

## 4. Labels
- Same as c029 (its proposal, section 4): tracker-only sweep over the unremedied state, every single remedy step of the action schema and every pair of steps of two different remedies; freeze v4 truth rule (`measure.score.label_rod`, C3 option a); scoring tolerance `config/scoring_tolerance.yaml`. The integrity gate is not applied to labels (inbox item 7)
- Expected class, before any label (reported, not used): accept_repaired for the four compound kinds; accept_clean for focus_drift 1.5 and illumination_flicker 0.03

## 5. Selection (fixed before any label exists)
- Walk the 48 candidates in candidate order. Keep the first 10 labelled accept_repaired, the first 4 labelled accept_clean and the first 6 labelled decline: 20 rods
- If a class has fewer rods than its quota, keep all of that class and state the shortfall. No other rods replace them
- A candidate whose label cannot be computed (tracker error on a needed state) is skipped and listed
- Written to `supplement/selected.json` with the label counts of all 48; committed with `labels.json` before any method run. The method driver refuses to run until both are committed

## 6. Where the runs happen
- Renders on the VM (`staging/rods_c029b`). Label tracker runs on the cluster through `scripts/rod_jobs.py` (CPU arrays), as c029's second array: rendered rod folders pushed whole, outputs fetched into `staging/tracks_c029b`
- Spend stop $15 total across the project; ledger check before every submit. Estimate: about 2,800 tracker runs (48 rods, moved copies, about 28 states each), worst case about $2
- No tracker run on the VM (spec 2026-11-20)

## 7. Methods
- As c029 (its proposal, section 5): fixed script, remedy tree (step limit 8), diagnostician, single agent without the checker; freeze v4 prompts and pinned model; option A integrity gate at every remedy step (`Slice.apply_remedy`, inbox item 7)
- Rule methods once; LLM methods 3 repeats on the 20 selected rods: 120 agent runs planned, cap 150. `claude -p` calls and tokens reported beside the count
- A state a method needs that the labels did not run pauses that run; the state goes to the cluster; the run is redone from step 0 (as c029)
- One LLM run at a time on the VM across all sessions; free VM memory at least 3 GB before each LLM run. Runs ended by the account session limit are set aside and rerun

## 8. Metrics
- As c029 (freeze v4 metrics, `measure/metrics.py`), on the 20 selected rods
- References on each set: all-decline score (c029: 20 of 24) and all-accept score
- Results in `results/2026-11-18_heldout_compound/supplement/`: `README.md`, `labels.md`, `labels.json`, `selected.json`, `table_metrics.md`, `metrics.json`, `scores.json`, `runs/`. Due Thu 26 Nov 20:00 local
